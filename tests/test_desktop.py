"""Exercise the real Qt window, its report actions, and the process entry point."""

import csv
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

from src.main import HardwareAnalyzerApp
from src.core.network import Network

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def qt_app():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def window(qt_app, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        Network,
        "test_internet_connection",
        lambda self: {"connected": False, "external_ip": None, "error": "Test offline mode"},
    )
    monkeypatch.setattr(
        QMessageBox,
        "critical",
        lambda parent, title, message: pytest.fail(f"Unexpected dialog: {title}: {message}"),
    )
    root_logger = logging.getLogger()
    original_handlers = set(root_logger.handlers)
    widget = HardwareAnalyzerApp()
    yield widget
    widget.close()
    qt_app.processEvents()
    for handler in root_logger.handlers[:]:
        if handler not in original_handlers:
            root_logger.removeHandler(handler)
            handler.close()


def test_window_refresh_graphs_and_themes(window, qt_app):
    assert [window.tab_widget.tabText(i) for i in range(4)] == [
        "Hardware",
        "Network",
        "Monitoring",
        "Settings",
    ]
    window.show()
    window.refresh_all()
    assert "CPU INFORMATION" in window.hardware_text.toPlainText()
    assert "Error generating" not in window.hardware_text.toPlainText()
    assert json.loads(window.network_text.toPlainText())["connectivity"]["connected"] is False
    assert hasattr(window, "canvas")
    assert len(window.cpu_line.get_ydata()) > 0
    for index in range(4):
        window.tab_widget.setCurrentIndex(index)
        qt_app.processEvents()
        assert not window.grab().isNull()
    window.change_theme("Dark")
    assert window.current_theme == "Dark"
    window.change_theme("Light")
    assert window.current_theme == "Light"
    window.close()
    assert not window.refresh_timer.isActive()
    assert not window.network_timer.isActive()
    assert not window.graph_timer.isActive()


@pytest.mark.parametrize("kind,extension", [("JSON", "json"), ("CSV", "csv"), ("PDF", "pdf")])
def test_toolbar_exports_use_real_dialog_api(window, monkeypatch, tmp_path, kind, extension):
    destination = tmp_path / f"report.{extension}"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *a: (str(destination), ""))
    monkeypatch.setattr(QMessageBox, "exec", lambda self: int(QMessageBox.StandardButton.Ok))
    window.handle_export(f"Export {kind}")
    assert destination.stat().st_size > 100
    if extension == "json":
        data = json.loads(destination.read_text(encoding="utf-8"))
        assert "cpu" in data["hardware"]
        assert "network" in data
    elif extension == "csv":
        with destination.open(encoding="utf-8", newline="") as report:
            rows = list(csv.reader(report))
        assert ["Section", "Field", "Value"] == rows[0]
        assert any(row[0] == "cpu" and row[1] == "name" for row in rows)
        assert any(row[0] == "gpu" for row in rows)
    else:
        assert destination.read_bytes().startswith(b"%PDF-")


def test_entry_point_opens_real_window_from_another_directory(tmp_path):
    project = tmp_path / "project with spaces"
    project.mkdir()
    shutil.copy2(ROOT / "run.py", project / "run.py")
    shutil.copytree(
        ROOT / "src", project / "src", ignore=shutil.ignore_patterns("__pycache__", "logs")
    )
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", PYTHONUTF8="1")
    result = subprocess.run(
        [sys.executable, str(project / "run.py"), "--smoke-test"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Desktop smoke test passed" in result.stdout


def test_missing_qt_explains_the_project_environment(monkeypatch, capsys):
    import builtins
    import run

    original_import = builtins.__import__

    def without_qt(name, *args, **kwargs):
        if name.startswith("PyQt6"):
            raise ModuleNotFoundError("No module named 'PyQt6'")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(sys, "argv", ["run.py"])
    monkeypatch.setattr(builtins, "__import__", without_qt)
    assert run.main() == 1
    output = capsys.readouterr().out
    assert sys.executable in output
    assert "setup.bat" in output
    assert "launch.bat" in output
