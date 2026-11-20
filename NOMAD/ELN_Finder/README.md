# NOMAD entry on ELN Finder

Changes submitted on **19 November 2026** are **under review by ELN Finder**. Publication is pending.

Ahmed Mansour has contributor access to maintain the NOMAD entry.

### Export the published record

The [export script](../../Scirpts/export_elnfinder.py) saves a dated snapshot of
NOMAD ELN's published ELN Finder metadata for tracking and comparing the entry
over time. It reads the entry without modifying it on ELN Finder.

Python and internet access are required; no credentials or additional packages
are needed. From a terminal at the repository root, run:

```powershell
python Scirpts/export_elnfinder.py
```

The script prints the saved file's path. It downloads NOMAD ELN's
published JSON from the public [ELN Finder API](https://eln-finder.ulb.tu-darmstadt.de/server/api/core/items/3e8ac43f-e6a3-437e-8a98-b2070d6cda8b)
and checks the record identity, metadata, and publication status before saving it.

The default output is `NOMAD/ELN_Finder/NOMAD-ELN-Finder-3e8ac43f-e6a3-437e-8a98-b2070d6cda8b_YYYY-MM-DD.json`,
resolved relative to the script's location. Running again on the same date
replaces that day's export. Use `--target-folder PATH` to choose another folder.
The export contains the specified public version and does not include changes
under review. If a new version receives a different item UUID, update `RECORD_ID`
in the script and the entry links here and in the main README.

Optional commands, also run from the repository root:

```powershell
# Save to a different folder
python Scirpts/export_elnfinder.py --target-folder "path/to/exports"

# Show all command-line options
python Scirpts/export_elnfinder.py --help
```

### Instructions for updating the entry:

1. Check the published [NOMAD entry](https://eln-finder.ulb.tu-darmstadt.de/items/3e8ac43f-e6a3-437e-8a98-b2070d6cda8b).
2. Select **Log In**, then **Login with ORCID**, using the ORCID linked to the contributor account.
3. Open **My workspace**. Choose **Your Submissions** in the **Show** menu.
4. For a draft, select **Edit**. For a published item, select **View**, use the branching icon to start a new version, describe the changes, and select **Create**.
5. Update the attributes and criteria, supplying supporting sources. Written permission is needed before naming an institution as a reference user.
6. Use **Save** or **Save for later** while preparing the entry. Select **Deposit** when it is ready for editorial review.
7. If revisions are requested, amend the entry and deposit it again. Publication follows approval.

The workspace labels distinguish drafts (**Workspace**), entries under review (**Workflow**), and published entries (**Archived**).

### Contact point

Use your usual editorial contact or write to [eln_finder_mailingliste@listserv.dfn.de](mailto:eln_finder_mailingliste@listserv.dfn.de). Beatrix Adam left the ELN Finder editorial team on **28 July 2026** and should no longer be used as the default contact.

### Further instructions

See the [ELN Finder manual for contributors](https://eln-finder.ulb.tu-darmstadt.de/docs/manual_contributors.pdf), updated **12 February 2026**, for the workflow and field guidance. Login and contact details above also reflect the editorial correspondence from January and July 2026.
