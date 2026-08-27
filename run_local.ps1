if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
. .\.venv\Scripts\Activate.ps1
if (-not (Test-Path .env)) { Copy-Item .env.local.example .env }
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
