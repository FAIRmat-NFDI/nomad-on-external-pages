# NOMAD entry on FAIRsharing

### Export the record

The [export script](../../Scirpts/export_fairsharing.py) saves a dated snapshot of
NOMAD Central's FAIRsharing record (2501) for tracking and comparing the entry
over time. It combines the REST API response with supplementary information
from the public page, including data processes, organisations, and relationships.
It reads the entry without modifying it on FAIRsharing.

Python and internet access are required. Run the commands below in a terminal.
Install dependencies once from the repository root:

```powershell
python -m pip install playwright
python -m playwright install chromium
```

Create or edit `.fairsharing.ini` in the repository root with your credentials
(enter the values without quotes):

```ini
[fairsharing]
username = your-username-or-email
password = your-password
```

This local file is excluded by `.gitignore`. It stores credentials as plain text
on your computer. The script reads it automatically, regardless of your working
directory. `FAIRSHARING_TOKEN`, when set, takes precedence; missing credentials
are requested interactively.

Run from the repository root:

```powershell
python Scirpts/export_fairsharing.py
```

The script prints the saved file's path. The default output is
`NOMAD/FAIRsharing/NOMAD-Central-FAIRsharing-2501_YYYY-MM-DD.json`, resolved
relative to the script's location. Running again on the same local date replaces
that day's export.

Optional commands, also run from the repository root:

```powershell
# Save to a different folder
python Scirpts/export_fairsharing.py --target-folder "path/to/exports"

# Use an existing REST JSON export instead of authenticating to the API
python Scirpts/export_fairsharing.py --api-export "path/to/api-export.json"

# Show all command-line options
python Scirpts/export_fairsharing.py --help
```

With `--api-export`, the supplemental public-page information is still retrieved
live, so internet access and Playwright are still required.


### Instructions for updating the entry: 
The entries on FAIRsharing can be edited by maintainers. Currently Ahmed Mansour and NOMAD account (contact@nomad-lab.eu) are listed as maintainers. 

1. Open the NOMAD entry page by visiting this [Link](https://fairsharing.org/2501)
2. Log in to your account. 
3. On the record page, click on the action button, then select edit record.  
4. Click on the *actions* icon,  then go to the record. 
5. The fields can be modified directly in the browser. 

### The most recent information are included in the XML re3data template [NOMAD_Re3data](NOMAD_re3data.xml)
