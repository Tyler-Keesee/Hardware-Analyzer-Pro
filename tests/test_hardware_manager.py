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
