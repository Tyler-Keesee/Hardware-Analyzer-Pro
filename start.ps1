Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Python environment not found. Run .\setup.bat first." -ForegroundColor Red
    exit 1
}
Push-Location $PSScriptRoot
try {
    & $venvPython (Join-Path $PSScriptRoot "run.py") @args
    $analyzerExitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
exit $analyzerExitCode
