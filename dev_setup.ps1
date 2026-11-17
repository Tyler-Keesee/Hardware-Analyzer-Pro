# Safe, repeatable Windows developer setup. Never deletes an existing venv.
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot ".venv")) {
        throw ".venv exists but has no Python executable. Rename it manually before retrying."
    }
    Write-Host "Creating isolated .venv..."
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Python venv creation failed. Check python --version." }
}
& $python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& $python -m pip install -r requirements.txt pytest
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed. Check Python version and pip output." }
& $python -m compileall -q run.py src tests
if ($LASTEXITCODE -ne 0) { throw "Source syntax checks failed." }
& $python -m pytest -q tests
if ($LASTEXITCODE -ne 0) { throw "Tests failed. Setup cannot be marked successful." }
Write-Host "Setup and tests completed. Run: .\.venv\Scripts\python.exe run.py"
