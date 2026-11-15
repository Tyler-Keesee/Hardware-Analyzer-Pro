import sys
import os
import logging
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


def setup_directories():
    """Create all required directories."""
    dirs = [
        "logs",
        "src/logs",
        "src/core/logs",
        "src/static",
        "src/templates",
        "reports",
        "results",
        "metrics",
    ]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)


def setup_logging():
    """Initialize logging configuration."""
    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Setup file handler
    file_handler = logging.FileHandler("logs/hardware_analyzer.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def print_log_locations():
    """Print locations of log files."""
    base_dir = os.getcwd()
    log_files = {
        "Main Log": os.path.join(base_dir, "logs", "hardware_analyzer.log"),
        "CPU Log": os.path.join(base_dir, "logs", "cpu_manager.log"),
        "GPU Log": os.path.join(base_dir, "logs", "gpu_manager.log"),
        "RAM Log": os.path.join(base_dir, "logs", "ram_manager.log"),
        "Network Log": os.path.join(base_dir, "logs", "network_manager.log"),
        "Storage Log": os.path.join(base_dir, "logs", "storage_manager.log"),
    }

    print("\nLog File Locations:")
    print("=" * 50)
    for name, path in log_files.items():
        print(f"{name}: {path}")
    print("=" * 50 + "\n")


def copy_default_theme():
    """Create default theme file if it doesn't exist."""
    theme_dir = Path("src/static")
    theme_file = theme_dir / "style.qss"

    if not theme_file.exists():
        default_theme = """
/* Default theme */
QMainWindow {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

QWidget {
    background-color: #1E1E1E;
    color: #FFFFFF;
}

QPushButton {
    background-color: #0066cc;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #0052a3;
}

QTabWidget::pane {
    border: 1px solid #333333;
    background-color: #252526;
}

QTabBar::tab {
    background-color: #2D2D2D;
    color: #FFFFFF;
    padding: 8px 20px;
    border: none;
}

QTabBar::tab:selected {
    background-color: #007ACC;
}
"""
        theme_file.write_text(default_theme)


def optimize_qt_settings():
    """Configure Qt for optimal performance."""
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_LOGGING_RULES"] = "*.debug=false;qt.qpa.*=false"


def main():
    """Main application entry point with performance optimizations."""
    parser = argparse.ArgumentParser(description="Hardware Analyzer Pro")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Open, render, refresh, and close the real desktop window for verification.",
    )
    args = parser.parse_args()
    try:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        from PyQt6.QtCore import Qt, QTimer

        os.chdir(ROOT_DIR)
        # Setup environment
        setup_directories()
        setup_logging()
        print_log_locations()
        copy_default_theme()

        # Set DPI attributes before creating QApplication
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Set environment hints before initializing Qt.
        optimize_qt_settings()
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        if args.smoke_test:

            def fail_on_dialog(parent, title, message, *unused):
                raise RuntimeError(f"{title}: {message}")

            QMessageBox.critical = fail_on_dialog

        # Import and create main window
        from src.main import HardwareAnalyzerApp

        window = HardwareAnalyzerApp()
        window.show()

        if args.smoke_test:

            def verify_window():
                try:
                    if window.tab_widget.count() != 4:
                        raise RuntimeError("Expected all four desktop tabs")
                    window.refresh_all()
                    text = window.hardware_text.toPlainText()
                    if not text or "Error generating" in text:
                        raise RuntimeError("Hardware view was not populated")
                    if not hasattr(window, "canvas"):
                        raise RuntimeError("Performance graph canvas was not created")
                    for index in range(window.tab_widget.count()):
                        window.tab_widget.setCurrentIndex(index)
                        app.processEvents()
                        if window.grab().isNull():
                            raise RuntimeError("Desktop tab failed to render")
                    print(
                        "Desktop smoke test passed: four tabs, hardware refresh, graphs, rendering."
                    )
                    window.close()
                    app.exit(0)
                except Exception:
                    logging.exception("Desktop smoke test failed")
                    window.close()
                    app.exit(1)

            QTimer.singleShot(0, verify_window)

        return app.exec()

    except ImportError as e:
        print(f"Error: {e}")
        print(f"Python in use: {sys.executable}")
        print("Windows: run setup.bat, then launch.bat from the project folder.")
        print("Existing installation: .\\venv\\Scripts\\python.exe .\\run.py")
        print("Linux/macOS: .venv/bin/python -m pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        logging.exception("Application failed to start")
        return 1


if __name__ == "__main__":
    sys.exit(main())
