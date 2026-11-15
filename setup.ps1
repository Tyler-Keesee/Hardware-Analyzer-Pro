param([switch]$Development, [switch]$Verify)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-CheckedPython {
    param([string]$Executable, [string[]]$Arguments)
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE. Setup did not complete."
    }
}

Push-Location $PSScriptRoot
try {
    $venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        if (Test-Path "venv") {
            throw "The existing venv has no Windows python.exe. Rename that folder and run setup again."
        }
        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if ($null -ne $pythonCommand) {
            $basePython = $pythonCommand.Source
            Invoke-CheckedPython -Executable $basePython -Arguments @(
                "-c", "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required'"
            )
            Invoke-CheckedPython -Executable $basePython -Arguments @("-m", "venv", "venv")
        } else {
            $pyCommand = Get-Command py -ErrorAction SilentlyContinue
            if ($null -eq $pyCommand) {
                throw "Install Python 3.10 or newer with pip, then run setup again."
            }
            Invoke-CheckedPython -Executable $pyCommand.Source -Arguments @(
                "-3", "-c", "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required'"
            )
            Invoke-CheckedPython -Executable $pyCommand.Source -Arguments @("-3", "-m", "venv", "venv")
        }
    }
    Invoke-CheckedPython -Executable $venvPython -Arguments @(
        "-c", "import sys; assert sys.version_info >= (3, 10), 'Python 3.10 or newer is required'"
    )
    Invoke-CheckedPython -Executable $venvPython -Arguments @(
        "-m", "pip", "install", "-r", "requirements.txt"
    )
    if ($Development -or $Verify) {
        Invoke-CheckedPython -Executable $venvPython -Arguments @(
            "-m", "pip", "install", "-r", "requirements-dev.txt"
        )
    }
    Invoke-CheckedPython -Executable $venvPython -Arguments @(
        "-c", "import PyQt6.QtWidgets, matplotlib, psutil; print('Runtime imports passed.')"
    )
    if ($Verify) {
        Invoke-CheckedPython -Executable $venvPython -Arguments @("-m", "flake8", "src", "tests", "run.py", "setup.py")
        Invoke-CheckedPython -Executable $venvPython -Arguments @("-m", "mypy", "src", "--config-file", "mypy.ini")
        Invoke-CheckedPython -Executable $venvPython -Arguments @("-m", "pytest", "tests")
        Invoke-CheckedPython -Executable $venvPython -Arguments @("run.py", "--smoke-test")
    }
    Write-Host "Setup completed. Start the application with .\launch.bat" -ForegroundColor Green
    Write-Host "Direct launch: .\venv\Scripts\python.exe .\run.py"
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}
