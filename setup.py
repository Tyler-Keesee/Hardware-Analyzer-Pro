"""Package metadata; dependency installation belongs in setup.ps1 or pip."""

from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).resolve().parent


def read_requirements(filename):
    return [
        line.strip()
        for line in (ROOT / filename).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


setup(
    name="hardware_analyzer",
    version="1.0.0",
    description="Desktop hardware monitoring and analysis tool",
    author="Tyler Keesee",
    packages=find_packages(),
    py_modules=["run"],
    package_data={"src": ["static/*.qss", "static/*.js", "templates/*.html"]},
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "web": ["Flask>=2.2", "flask-cors>=4.0"],
    },
    entry_points={"console_scripts": ["hardware-analyzer=run:main"]},
    python_requires=">=3.10",
)
