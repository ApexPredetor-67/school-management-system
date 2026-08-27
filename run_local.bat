@echo off
setlocal
if not exist .venv (
  echo Creating Python 3.12 virtual environment...
  py -3.12 -m venv .venv
)
call .venv\Scripts\activate
if not exist .env copy /Y .env.local.example .env >nul
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

REM Set LOCAL_HTTPS=true in .env.local to use local HTTPS (development certificate).
