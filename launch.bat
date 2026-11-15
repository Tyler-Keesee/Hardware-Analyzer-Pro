@echo off
setlocal
pushd "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo Python environment not found. Run setup.bat first.
    popd
    exit /b 1
)
"venv\Scripts\python.exe" "%~dp0run.py" %*
set "analyzerExitCode=%errorlevel%"
popd
exit /b %analyzerExitCode%
