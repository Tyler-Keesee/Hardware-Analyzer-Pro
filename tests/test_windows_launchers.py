"""Execute the actual Windows scripts; Linux cannot validate cmd.exe semantics."""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Requires Windows script hosts")


def prepare_project(tmp_path, scripts):
    project = tmp_path / "project with spaces"
    project.mkdir()
    for script in scripts:
        shutil.copy2(ROOT / script, project / script)
    subprocess.run(
        [sys.executable, "-m", "venv", "--without-pip", str(project / "venv")], check=True
    )
    return project


@pytest.mark.parametrize("launcher", ["launch.bat", "start.ps1"])
@pytest.mark.parametrize("exit_code", [0, 7])
def test_launcher_uses_own_environment_and_propagates_exit(tmp_path, launcher, exit_code):
    project = prepare_project(tmp_path, [launcher])
    (project / "run.py").write_text(
        "import pathlib, sys\n"
        "assert pathlib.Path(sys.prefix) == pathlib.Path(__file__).parent / 'venv'\n"
        "assert pathlib.Path.cwd() == pathlib.Path(__file__).parent\n"
        "assert sys.argv[1:] == ['--probe']\n"
        "print('PROJECT_VENV_USED')\n"
        f"raise SystemExit({exit_code})\n",
        encoding="utf-8",
    )
    if launcher.endswith(".bat"):
        command = ["cmd.exe", "/c", str(project / launcher), "--probe"]
    else:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(project / launcher),
            "--probe",
        ]
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=45)
    assert result.returncode == exit_code, result.stdout + result.stderr
    assert "PROJECT_VENV_USED" in result.stdout


@pytest.mark.parametrize("setup", ["setup.bat", "dev_setup.bat", "dev_setup.ps1"])
def test_setup_preserves_environment_and_reports_install_failure(tmp_path, setup):
    project = prepare_project(tmp_path, [setup, "setup.ps1"])
    sentinel = project / "venv" / "keep.txt"
    sentinel.write_text("preserve existing environment", encoding="utf-8")
    source = project / "source.py"
    source.write_text("untouched =  1\n", encoding="utf-8")
    if setup.endswith(".bat"):
        command = ["cmd.exe", "/c", str(project / setup)]
    else:
        command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(project / setup),
        ]
    # The environment intentionally has no pip: setup must fail without claiming success.
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, timeout=45)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "Setup completed" not in result.stdout
    assert sentinel.read_text(encoding="utf-8") == "preserve existing environment"
    assert source.read_text(encoding="utf-8") == "untouched =  1\n"
