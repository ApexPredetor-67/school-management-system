@echo off
set "LOCAL_HTTPS=true"
set "SSL_ADHOC=true"
call venv\Scripts\activate
python app.py
pause
