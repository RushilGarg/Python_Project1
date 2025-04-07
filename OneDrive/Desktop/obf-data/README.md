## Requirements
Requires `node` and `npm` to be installed. Once `npm` is installed, run `npm install`. Verify using `npx javascript-obfuscator --version`.

Requires `python` to be installed. Run `pip install -r requirements.txt`. _Might_ need to create a virtual environment so, if so, run

```bash
python -m venv .\venv
.\.venv\Scripts\Activate.ps1                 # On Windows
```

Might need to enable scripts on Powershell. Read more [here](https://superuser.com/questions/106360/how-to-enable-execution-of-powershell-scripts).

## To run
Files to run
- `save.py` to download the dataset and randomly chose which files to save to disk. Should roughly download 2M files. Files saved to `data_cache/`
- `obf.py` which saves to `data_obf/`
- `zip.py` which ZIPs each batch in `data_obf/` and stores to `data_zipped/`

## Reminders
Remember to update `.gitignore` for any temporary files.

`data_zipped` is not "gitignored" since this needs to be pushed to Github.

## Git LFS
Git LFS should likely not be required since each ZIP file will likely be under 100Mb. Otherwise, push to git using LFS.