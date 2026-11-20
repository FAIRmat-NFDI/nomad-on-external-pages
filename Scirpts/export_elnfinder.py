"""Export NOMAD ELN's published ELN Finder record as dated JSON.

Run python Scirpts/export_elnfinder.py. No credentials or third-party packages
are required. Exports default to the repository's NOMAD/ELN_Finder folder.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

RECORD_ID = "3e8ac43f-e6a3-437e-8a98-b2070d6cda8b"
API_URL = f"https://eln-finder.ulb.tu-darmstadt.de/server/api/core/items/{RECORD_ID}"
DEFAULT_TARGET_FOLDER = Path(__file__).resolve().parent.parent / "NOMAD" / "ELN_Finder"


def export_elnfinder(target_folder=DEFAULT_TARGET_FOLDER):
    """Save the public API record after checking its identity and metadata.

    A repeat export on the same local date replaces that day's file only after
    a successful download and check. Pending editorial changes are not exported.
    """
    request = Request(API_URL, headers={"Accept": "application/hal+json, application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"ELN Finder returned HTTP {exc.code}.") from None
    except (URLError, TimeoutError):
        raise RuntimeError(f"Could not reach the ELN Finder API at {API_URL}.") from None
    except ValueError:
        raise RuntimeError("The ELN Finder API did not return valid JSON.") from None

    if not isinstance(payload, dict) or payload.get("uuid") != RECORD_ID:
        raise RuntimeError(f"The API response does not contain ELN Finder record {RECORD_ID}.")
    if not isinstance(payload.get("metadata"), dict) or not payload["metadata"]:
        raise RuntimeError("The ELN Finder API response does not contain record metadata.")
    if payload.get("inArchive") is not True or payload.get("withdrawn") is not False:
        raise RuntimeError("The ELN Finder record is not currently published or has been withdrawn.")

    folder = Path(target_folder).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    now = datetime.now().astimezone()
    path = folder / f"NOMAD-ELN-Finder-{RECORD_ID}_{now:%Y-%m-%d}.json"
    temporary_path = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=folder, suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(payload, temporary, ensure_ascii=False, indent=2, allow_nan=False)
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
        help="Output folder (default: repository's NOMAD/ELN_Finder folder).",
    )
    args = parser.parse_args()
    try:
        path = export_elnfinder(args.target_folder)
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
