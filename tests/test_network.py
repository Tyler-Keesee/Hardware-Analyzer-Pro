import psutil
import pytest

from src.core.network import Network


@pytest.mark.parametrize("error", [PermissionError("restricted"), psutil.AccessDenied()])
def test_restricted_network_does_not_prevent_monitoring(monkeypatch, tmp_path, error):
    def denied():
        raise error

    monkeypatch.setattr(psutil, "net_if_addrs", denied)
    monkeypatch.setattr(Network, "test_internet_connection", lambda self: {"connected": False})
    network = Network(log_dir=str(tmp_path))
    try:
        summary = network.get_network_summary()
        assert summary["interfaces"] == []
        assert "interfaces" in summary["errors"]
        assert "io_stats" in summary
        assert "timestamp" in summary
    finally:
        network.cleanup()
