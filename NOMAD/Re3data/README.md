# NOMAD entry on Re3data

### Instructions for updating the entry:

1. Open the NOMAD entry page by visiting this [Link](https://www.re3data.org/search?query=NOMAD)
2. Click the ```submit a change request``` link at the bottom of the entry.
3. A form will open where you can enter the necessary changes.
4. Ensure you enter the content types according to the updated [Re3data schema](https://www.re3data.org/schema). The current content is based on [version 4](re3data-schema-documentation-V4-0.pdf).
5. Once submitted, the re3data team will review the information and send an email notification when the changes are published.

### Saved re3data record

The latest saved published re3data snapshot in this repository is the [XML export from 20 November 2026](NOMAD-Re3data-r3d100011583_2026-11-20.xml). It may not yet include the changes under review. Use the export instructions below to retrieve the current published record.

### Export the published record

The [export script](../../Scirpts/export_re3data.py) saves a dated snapshot of
NOMAD's published re3data metadata for tracking and comparing the entry over
time. It reads the entry without submitting changes to re3data.

Python and internet access are required; no credentials or additional packages
are needed. From a terminal at the repository root, run:

```powershell
python Scirpts/export_re3data.py
```

The script prints the saved file's path. It downloads NOMAD's
published XML from the public [re3data schema 4.0 API](https://www.re3data.org/api/doc/)
and checks that it contains record `r3d100011583` before saving it unchanged.

The default output is `NOMAD/Re3data/NOMAD-Re3data-r3d100011583_YYYY-MM-DD.xml`,
resolved relative to the script's location. Running again on the same date
replaces that day's export. Use `--target-folder PATH` to choose another folder.
The export contains the public record and may not yet include changes under
review.

Optional commands, also run from the repository root:

```powershell
# Save to a different folder
python Scirpts/export_re3data.py --target-folder "path/to/exports"

# Show all command-line options
python Scirpts/export_re3data.py --help
```
