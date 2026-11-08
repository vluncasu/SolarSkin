# Publication tools

Run from the repository root with Python 3.11 or later.

```sh
python3 engineering/test_calculations.py
python3 tools/verify.py
python3 -m pip install -r tools/requirements.txt
python3 tools/build_manuals.py
python3 tools/package_release.py
```

The PDFs use Arial on macOS or DejaVu Sans on Linux. Render and inspect pages after rebuilding. Successful generation does not establish a readable layout. Release packaging excludes Git metadata, local secrets, generated builds and historical archives, then checks ZIP CRCs and computes SHA256.
