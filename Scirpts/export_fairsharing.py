"""Export NOMAD Central's FAIRsharing record as a dated JSON file.

Install dependencies with python -m pip install playwright and then
python -m playwright install chromium. Run python Scirpts/export_fairsharing.py.
Exports default to the repository's NOMAD/FAIRsharing folder.
"""

import argparse
import asyncio
import configparser
import getpass
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RECORD_ID = "2501"
API_URL = "https://api.fairsharing.org"
RECORD_URL = f"https://fairsharing.org/{RECORD_ID}/"
DEFAULT_TARGET_FOLDER = Path(__file__).resolve().parent.parent / "NOMAD" / "FAIRsharing"
CREDENTIALS_FILE = Path(__file__).resolve().parent.parent / ".fairsharing.ini"

# The public page supplies process, organisation and relationship fields that
# the single-record REST response can omit.
PUBLIC_FIELDS = r"""
() => {
    const general = document.querySelector("#generalInfo");
    const conditions = document.querySelector("#dataprocessesandconditions");
    const organisations = document.querySelector("#organisations");
    const people = [...general.querySelectorAll('a[href*="/users/"]')];
    const isChampion = link => link.parentElement.parentElement.parentElement.innerText
        .includes("community champions");
    const person = link => ({
        username: link.innerText.trim(),
        fairsharing_profile: link.href,
        orcid: link.parentElement.querySelector('a[href*="orcid.org/"]')?.href ?? null,
    });

    const processes = [...conditions.querySelectorAll("b")]
        .filter(label => label.innerText.trim() === "Name")
        .map(label => {
            const card = label.parentElement.parentElement.parentElement;
            const field = name => [...card.querySelectorAll("b")]
                .find(item => item.innerText.trim() === name)?.parentElement;
            return {
                name: field("Name")?.lastElementChild.innerText.trim() ?? null,
                url: field("Name")?.querySelector("a")?.href ?? null,
                access_method: field("Access Method")?.lastElementChild.innerText.trim() ?? null,
                documentation_url: field("Documentation URL")?.querySelector("a")?.href ?? null,
                example_url: field("Example URL")?.querySelector("a")?.href ?? null,
                read: Boolean(field("Read")?.querySelector(".fa-check")),
                write: Boolean(field("Write")?.querySelector(".fa-check")),
            };
        });

    const orgs = {};
    for (const role of ["maintaining", "funding"]) {
        const title = [...organisations.querySelectorAll(".v-card-title")]
            .find(item => item.innerText.trim() === "Organisations " + role + " this resource");
        const links = title?.parentElement.querySelectorAll('a[href*="/organisations/"]') ?? [];
        orgs[role] = [...links].map(link => {
            const row = link.parentElement.parentElement;
            const [name, ...badges] = link.innerText.split("\n");
            return {
                name: name.trim(),
                fairsharing_url: link.href,
                ror: row.querySelector('a[href*="ror.org/"]')?.href ?? null,
                lead: badges.some(line => line.trim() === "Lead"),
                displayed_details: row.innerText.trim(),
            };
        });
    }

    const citation = general.innerText.split("How to cite this record")[1] ?? "";
    return {
        general_information: {
            awaiting_curator_review: document.body.innerText.includes(
                "This record is awaiting review by FAIRsharing curators"
            ),
            maintainers: people.filter(link => !isChampion(link)).map(person),
            community_champions: people.filter(isChampion).map(person),
            last_editor: citation.match(/Last Editor:\s*([^,\n]+)/i)?.[1].trim() ?? null,
            last_reviewed_display: citation.match(/Last Reviewed:\s*([^\n]+)/i)?.[1].trim() ?? null,
        },
        data_processes: processes,
        licence_display: {
            spdx_urls: [...conditions.querySelectorAll('a[href*="spdx.org/licenses/"]')]
                .map(link => link.href),
        },
        organisations: orgs,
    };
}
"""

RELATIONSHIP_ROWS = r"""
element => [...element.querySelectorAll(".v-virtual-scroll__item a")].map(link => {
    const url = new URL(link.href);
    const recordId = url.pathname.split("/").filter(Boolean).at(-1);
    const statement = link.querySelector("p");
    return {
        name: link.querySelector(".underline-effect")?.innerText.trim() ?? null,
        record_id: /^\d+$/.test(recordId) ? Number(recordId) : null,
        fairsharing_url: url.href,
        relation: statement?.querySelector("span")?.innerText.trim() ?? null,
        statement: statement?.innerText.trim() ?? null,
    };
})
"""


def _local_credentials():
    """Read optional local credentials without interpolating password characters."""
    if not CREDENTIALS_FILE.exists():
        return "", ""
    config = configparser.ConfigParser(interpolation=None)
    try:
        with CREDENTIALS_FILE.open(encoding="utf-8-sig") as credentials:
            config.read_file(credentials)
        return (
            config.get("fairsharing", "username", fallback="").strip(),
            config.get("fairsharing", "password", fallback=""),
        )
    except configparser.Error:
        raise RuntimeError(
            "Invalid .fairsharing.ini: use a [fairsharing] section with username and password entries."
        ) from None


def _api_json(path, *, token=None, body=None):
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(
        f"{API_URL}/{path}",
        headers=headers,
        data=None if body is None else json.dumps(body).encode("utf-8"),
    )
    if token:
        request.add_unredirected_header("Authorization", f"Bearer {token}")
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"FAIRsharing {path} returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError):
        raise RuntimeError(f"Could not reach the FAIRsharing API at {path}.") from None
    except ValueError:
        raise RuntimeError(f"FAIRsharing {path} did not return JSON.") from None


async def _relationship_tab(page, section_selector, label):
    section = page.locator(section_selector)
    tab = section.get_by_role("tab", name=re.compile(rf"^{re.escape(label)}\s*\(", re.I))
    title = await tab.inner_text()
    count = re.search(r"\((\d+)\)\s*$", title)
    if count is None:
        raise RuntimeError(f"Could not read the relationship count for {title!r}.")
    expected = int(count[1])
    if expected == 0:
        return []

    await tab.click()
    list_area = section.locator(".v-window-item--active .v-virtual-scroll")
    await list_area.locator(".v-virtual-scroll__item a").first.wait_for()
    rows = {}
    while True:
        for row in await list_area.evaluate(RELATIONSHIP_ROWS):
            rows[row["fairsharing_url"], row["statement"]] = row
        if len(rows) == expected:
            return list(rows.values())

        # FAIRsharing renders only the cards around the visible area.
        moved = await list_area.evaluate("""
            async element => {
                const before = element.scrollTop;
                element.scrollTop += Math.max(1, Math.floor(element.clientHeight / 2));
                await new Promise(resolve => requestAnimationFrame(() =>
                    requestAnimationFrame(resolve)
                ));
                return element.scrollTop !== before;
            }
        """)
        if not moved or len(rows) > expected:
            raise RuntimeError(f"{title}: found {len(rows)} of {expected} relationships.")


async def _public_record():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise RuntimeError(
            "Install Playwright with python -m pip install playwright, then run "
            "python -m playwright install chromium."
        ) from None

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        try:
            page = await browser.new_page()
            response = await page.goto(RECORD_URL, wait_until="domcontentloaded")
            if response is None or not response.ok:
                raise RuntimeError(f"Could not open {RECORD_URL}.")
            await page.locator("#generalInfo").get_by_role(
                "heading", name=re.compile("NOMAD Central", re.I)
            ).wait_for()
            await page.locator("#organisations a[href*='/organisations/']").first.wait_for()
            await page.locator("#dataprocessesandconditions").wait_for()
            public = await page.evaluate(PUBLIC_FIELDS)
            if not public["data_processes"]:
                raise RuntimeError("Could not read the data processes from the public record.")

            public["relationships"] = {
                "from_nomad": {
                    "standards": await _relationship_tab(page, "#relatedcontent", "related standards"),
                    "databases": await _relationship_tab(page, "#relatedcontent", "related databases"),
                    "fairassist_components": await _relationship_tab(
                        page, "#relatedcontent", "related fairassist components"
                    ),
                },
                "to_nomad": {
                    "collections": await _relationship_tab(page, "#collections", "in collections"),
                    "policies": await _relationship_tab(page, "#collections", "in policies"),
                },
            }
            return public
        finally:
            await browser.close()


def _public_record_in_thread():
    # Chromium uses subprocesses, which the Windows Jupyter event loop may not support.
    loop = asyncio.ProactorEventLoop() if os.name == "nt" else asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_public_record())
    finally:
        loop.close()


async def export_fairsharing(target_folder=DEFAULT_TARGET_FOLDER, *, api_export=None):
    """Save record 2501 to NOMAD/FAIRsharing and return the new path.

    Pass target_folder to override the repository-relative default folder.
    Pass api_export to use a previously downloaded REST JSON file. Otherwise
    the function uses FAIRSHARING_TOKEN, then the repository's .fairsharing.ini,
    then prompts for any missing FAIRsharing credentials.
    The supplemental public fields are retrieved live in both cases.
    """
    if api_export is not None:
        payload = json.loads(Path(api_export).expanduser().read_text(encoding="utf-8-sig"))
    else:
        token = os.environ.get("FAIRSHARING_TOKEN")
        if not token:
            login, password = _local_credentials()
            if not login:
                login = input("FAIRsharing username or email: ").strip()
            if not password:
                password = getpass.getpass("FAIRsharing password: ")
            try:
                session = await asyncio.to_thread(
                    _api_json, "users/sign_in", body={"user": {"login": login, "password": password}}
                )
            finally:
                del password
            token = session.get("jwt")
            if not token:
                raise RuntimeError("FAIRsharing sign-in did not return an access token.")
        payload = await asyncio.to_thread(_api_json, f"fairsharing_records/{RECORD_ID}", token=token)

    if str(payload.get("data", {}).get("id")) != RECORD_ID:
        raise ValueError(f"The API response does not contain FAIRsharing record {RECORD_ID}.")

    public = await asyncio.to_thread(_public_record_in_thread)
    now = datetime.now().astimezone()
    folder = Path(target_folder).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"NOMAD-Central-FAIRsharing-{RECORD_ID}_{now:%Y-%m-%d}.json"
    snapshot = {
        **payload,
        "sources": {
            "exported_at": now.isoformat(timespec="seconds"),
            "api_response": {
                "endpoint": f"{API_URL}/fairsharing_records/{RECORD_ID}",
                "retrieval": "saved file" if api_export is not None else "live request",
                "record_updated_at": payload["data"].get("attributes", {}).get("updated_at"),
            },
            "public_record_page": RECORD_URL,
            "coverage": "REST API response and supplementary fields visible on the public record.",
        },
        "public_record": public,
    }

    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=folder, suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(snapshot, temporary, ensure_ascii=False, indent=2, allow_nan=False)
            temporary.write("\n")
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-folder", type=Path, default=DEFAULT_TARGET_FOLDER,
        help="Output folder (default: repository's NOMAD/FAIRsharing folder).",
    )
    parser.add_argument(
        "--api-export", type=Path,
        help="Use a saved REST JSON file instead of signing in to the API.",
    )
    args = parser.parse_args()
    try:
        path = asyncio.run(export_fairsharing(args.target_folder, api_export=args.api_export))
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Export cancelled.", file=sys.stderr)
        return 130
    print(f"Saved to: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
