from src.core.hardware_manager import HardwareManager


def test_hardware_manager_initialization():
    """Test basic initialization of HardwareManager."""
    manager = HardwareManager()
    assert manager is not None


def test_get_cpu_usage():
    """Test CPU usage retrieval."""
    manager = HardwareManager()
    usage = manager.get_cpu_usage()
    assert isinstance(usage, float)
    assert 0 <= usage <= 100


def test_get_ram_usage():
    """Test RAM usage retrieval."""
    manager = HardwareManager()
    usage = manager.get_ram_usage()
    assert isinstance(usage, float)
    assert 0 <= usage <= 100


def test_get_gpu_usage():
    """Test GPU usage retrieval."""
    manager = HardwareManager()
    usage = manager.get_gpu_usage()
    assert isinstance(usage, float)
    assert 0 <= usage <= 100


def test_missing_storage_measurements_are_not_reported_as_healthy(hardware_manager):
    for drives in ([], [{"device": "restricted", "error": "Permission denied"}]):
        status = hardware_manager._get_aggregate_storage_status(drives)
        assert status["message"] == "Storage Unavailable"
