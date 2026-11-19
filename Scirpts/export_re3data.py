"""Export NOMAD's published re3data record as dated XML.

Run python Scirpts/export_re3data.py. No credentials or third-party packages
are required. Exports default to the repository's NOMAD/Re3data folder.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

RECORD_ID = "r3d100011583"
API_URL = f"https://www.re3data.org/api/v40/repository/{RECORD_ID}"
DEFAULT_TARGET_FOLDER = Path(__file__).resolve().parent.parent / "NOMAD" / "Re3data"
NAMESPACE = "http://www.re3data.org/schema/4-0"


def export_re3data(target_folder=DEFAULT_TARGET_FOLDER):
    """Save the public record unchanged after checking XML and record identity.

    The filename uses the local execution date. A repeat export on the same
    date replaces that day's file only after a successful download and check.
    """
    request = Request(API_URL, headers={"Accept": "application/xml, text/xml"})
    try:
        with urlopen(request, timeout=30) as response:
            data = response.read()
    except HTTPError as exc:
        raise RuntimeError(f"re3data returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError):
        raise RuntimeError(f"Could not reach the re3data API at {API_URL}.") from None

    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError:
        raise RuntimeError("The re3data API did not return valid XML.") from None
    ns = {"r3d": NAMESPACE}
    record_id = root.findtext("r3d:repository/r3d:identifiers/r3d:re3data", namespaces=ns)
    if root.tag != f"{{{NAMESPACE}}}re3data" or (record_id or "").strip() != RECORD_ID:
        raise RuntimeError(f"The API response does not contain re3data record {RECORD_ID} in schema 4.0.")

    folder = Path(target_folder).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone()
    path = folder / f"NOMAD-Re3data-{RECORD_ID}_{now:%Y-%m-%d}.xml"
    temporary_path = None
    try:
        with NamedTemporaryFile(mode="wb", dir=folder, suffix=".tmp", delete=False) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(data)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-folder", type=Path, default=DEFAULT_TARGET_FOLDER,
        help="Output folder (default: repository's NOMAD/Re3data folder).",
    )
    args = parser.parse_args()
    try:
        path = export_re3data(args.target_folder)
    except (RuntimeError, OSError) as exc:
        print(f"Export failed: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Export cancelled.", file=sys.stderr)
        return 130
    print(f"Saved to: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
