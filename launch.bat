@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Missing .venv. Run dev_setup.bat first.
  exit /b 1
)
".venv\Scripts\python.exe" run.py
exit /b %errorlevel%
