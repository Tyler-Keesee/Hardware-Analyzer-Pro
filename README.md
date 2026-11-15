# Hardware Analyzer Pro

A Python/PyQt6 desktop application for CPU, RAM, GPU, storage, and network monitoring, live graphs, themes, and JSON/CSV/PDF reports.

## Windows installation

Install Python 3.10 or newer with pip first. Python 3.14 is supported by the verification workflow. Run each command separately in either Command Prompt or PowerShell:

```text
git clone https://github.com/Tyler-Keesee/Hardware-Analyzer-Pro.git
```

```text
cd Hardware-Analyzer-Pro
```

Install runtime dependencies into the project's `venv`:

```text
.\setup.bat
```

Start the application:

```text
.\launch.bat
```

The launcher always uses `venv\Scripts\python.exe`; activating a virtual environment is unnecessary. Setup reuses an existing environment, checks command failures, and does not reformat source files or install PowerShell modules.

If you already ran the old setup and `python run.py` says `No module named 'PyQt6'`, use the installed environment directly:

```text
.\venv\Scripts\python.exe .\run.py
```

Installing packages inside a child PowerShell process does not activate its environment in the parent Command Prompt. Running `python run.py` there can select a different Python installation.

PowerShell-only equivalents are available:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\setup.ps1
```

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start.ps1
```

## Linux/macOS

Windows is the primary target. These commands install the same runtime dependencies; available sensors and drivers vary by platform.

```sh
python3 -m venv .venv
```

```sh
.venv/bin/python -m pip install -r requirements.txt
```

```sh
.venv/bin/python run.py
```

## Verification and limitations

The GitHub Actions workflow covers Windows and Linux with Python 3.10 and 3.14. It runs lint, type checks, hardware-manager tests, report-export tests, and a desktop smoke test that opens the real four-tab window, refreshes hardware information, renders each tab, and closes it. Windows jobs additionally exercise setup and launcher behavior, including failure exit codes and paths containing spaces. Check the workflow results for the commit you use; a configured matrix alone is not proof of a passing run.

To run all development checks on Windows:

```text
.\dev_setup.bat -Verify
```

To run only the desktop smoke test:

```text
.\launch.bat --smoke-test
```

On a machine without a display, set `QT_QPA_PLATFORM=offscreen` in the test process. This checks application construction and rendering without proving physical sensor accuracy.

CPU temperature is currently available only where Linux `coretemp` sensors expose it; Windows displays `Not available`. NVIDIA readings require a working NVIDIA driver/NVML installation. The current GPU percentage is video-memory utilization, not GPU-engine utilization. OS restrictions may make network details unavailable; the report includes those errors while other views remain usable. macOS has no CI job. No hardware-specific NVIDIA or Windows temperature validation is claimed.

## Development

Developer setup installs tools without changing source formatting:

```text
.\dev_setup.bat
```

Run checks individually using the project's interpreter:

```text
.\venv\Scripts\python.exe -m pytest tests
```

```text
.\venv\Scripts\python.exe -m flake8 src tests run.py setup.py
```

```text
.\venv\Scripts\python.exe -m mypy src --config-file mypy.ini
```

Linux/macOS developers can install `requirements-dev.txt` with `.venv/bin/python -m pip install -r requirements-dev.txt` and use that interpreter for the same checks. Formatting is an explicit developer action, not part of installation.

An optional Flask interface is separate from the desktop launcher. Install its dependencies with `python -m pip install -e ".[web]"` in your chosen environment and run `python -m src.web_app`. Its endpoints are not covered by the desktop smoke test.

## Usage and logs

Use the Hardware, Network, Monitoring, and Settings tabs. The toolbar provides refresh, theme selection, and JSON/CSV/PDF exports. Logs are written under `logs/` in the project directory. The app does not need administrator privileges to launch; individual metrics can be restricted by the OS.

## License

The `LICENSE` file is empty. This repository does not currently include a usable license grant and should not be described as MIT-licensed.

## Support

Report issues with the full terminal error, operating system, Python version, and relevant files from `logs/`.
