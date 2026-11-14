# Hardware Analyzer Pro

A Python and PyQt6 desktop hardware-monitoring project with system metrics, performance graphs, and export utilities. Features and platform support should be verified against your hardware and the included tests.

## Key Features

- Real-time hardware monitoring
  - CPU usage and temperature
  - RAM utilization
  - GPU metrics (NVIDIA support)
  - Storage analysis
  - Network monitoring
- Professional UI with Dark/Light themes
- Live performance graphs
- Network interface monitoring
- Export capabilities (JSON, CSV, PDF)
- Auto-refresh functionality
- System alerts and notifications

## Testing and support status

The repository contains tests under `tests/`, but desktop rendering, sensors, and
NVIDIA-specific metrics depend on the operating system, permissions, and installed drivers.
Do not assume all monitors or export formats work on every machine without testing.
There is currently no confirmed multi-platform CI matrix.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Tyler-Keesee/Hardware-Analyzer-Pro.git
cd Hardware-Analyzer-Pro
```

2. Run the setup script:
```bash
# Windows (PowerShell)
powershell.exe -ExecutionPolicy Bypass -File .\dev_setup.ps1

# Windows (Command Prompt)
.\launch.bat

# Linux/macOS (experimental; not CI-verified)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

## Requirements

- Python 3.8 or higher
- Windows is the primary target; Linux/macOS behavior depends on available drivers and desktop support and has not been independently validated
- Dependencies (automatically installed):
  - PyQt6 ≥ 6.4.0
  - matplotlib ≥ 3.6.0
  - psutil ≥ 5.9.0
  - py3nvml ≥ 0.2.7 (for NVIDIA GPU support)
  - Additional requirements listed in requirements.txt

## Usage

1. Start the application:
```bash
python run.py
```

2. Features:
   - Use the toolbar for quick actions
   - Switch between tabs for different monitoring views
   - Adjust refresh rates in settings
   - Export data in various formats

## Development

```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
python -m pytest tests/

# Code quality checks
python -m black src/
python -m flake8 src/
python -m mypy src/
```

## Logs

Log files are stored in the `logs` directory:
- hardware_analyzer.log - Main application log
- cpu_manager.log - CPU monitoring
- gpu_manager.log - GPU monitoring
- ram_manager.log - Memory monitoring
- network_manager.log - Network monitoring
- storage_manager.log - Storage monitoring

## License

The `LICENSE` file is currently empty and does not provide a usable license grant. Add a complete license text before describing the project as MIT-licensed.

## Support

For issues and feature requests, please create an issue in the repository.
