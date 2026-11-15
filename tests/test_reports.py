"""Report failures that were not reached by the original four metric tests."""

import csv
from datetime import datetime, timedelta
import json


def test_pdf_with_embedded_performance_graph(hardware_manager, tmp_path):
    manager = hardware_manager
    now = datetime.now()
    manager.performance_history = [
        {"timestamp": now - timedelta(seconds=1), "metrics": {"cpu": {"usage": 5}}},
        {"timestamp": now, "metrics": {"cpu": {"usage": 15}}},
    ]
    destination = tmp_path / "performance.pdf"
    assert manager.export_performance_report(destination, "pdf")
    payload = destination.read_bytes()
    assert payload.startswith(b"%PDF-")
    assert b"/Subtype /Image" in payload
    assert not (tmp_path / "temp_graph.png").exists()


def test_manager_csv_preserves_nested_device_data(hardware_manager, tmp_path):
    destination = tmp_path / "hardware.csv"
    assert hardware_manager.export_performance_report(destination, "csv")
    with destination.open(encoding="utf-8", newline="") as report:
        rows = list(csv.DictReader(report))
    gpu_row = next(row for row in rows if row["Section"] == "gpu" and row["Field"] == "gpus")
    assert isinstance(json.loads(gpu_row["Value"]), list)


def test_html_escapes_hardware_strings(hardware_manager, monkeypatch, tmp_path):
    monkeypatch.setattr(
        hardware_manager, "get_hardware_summary", lambda: {"cpu": "<script>test</script>"}
    )
    destination = tmp_path / "report.html"
    assert hardware_manager.export_performance_report(destination, "html")
    payload = destination.read_text(encoding="utf-8")
    assert "<script>" not in payload
    assert "&lt;script&gt;" in payload


def test_unsupported_export_reports_failure(hardware_manager, tmp_path):
    destination = tmp_path / "report.unsupported"
    assert not hardware_manager.export_performance_report(destination, "unsupported")
    assert not destination.exists()
