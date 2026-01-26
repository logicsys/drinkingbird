#!/usr/bin/env python3
"""
Build script for creating a Windows executable of Drinkingbird.

This script automates the process of building a standalone Windows executable
using PyInstaller. The resulting binary can be distributed without requiring
Python to be installed on the target machine.

Usage:
    python build-windows.py [--clean] [--no-venv]

Requirements:
    - Python 3.7+
    - pip

The script will automatically install PyInstaller and other dependencies.
"""

import subprocess
import sys
import os
import shutil
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"{description}")
    print(f"{'='*50}")
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"\nERROR: {description} failed with exit code {result.returncode}")
        sys.exit(1)
    return result


def main():
    parser = argparse.ArgumentParser(description="Build Drinkingbird Windows executable")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts before building")
    parser.add_argument("--no-venv", action="store_true", help="Don't use a virtual environment")
    parser.add_argument("--spec", action="store_true", help="Use the .spec file for building")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    print("\n" + "=" * 60)
    print("  DRINKINGBIRD WINDOWS BUILD")
    print("=" * 60)

    # Clean if requested
    if args.clean:
        print("\nCleaning previous build artifacts...")
        for path in ["build", "dist", "__pycache__"]:
            if Path(path).exists():
                print(f"  Removing {path}/")
                shutil.rmtree(path)

    # Check Python version
    if sys.version_info < (3, 7):
        print("ERROR: Python 3.7 or higher is required")
        sys.exit(1)
    print(f"\nPython version: {sys.version}")

    # Setup virtual environment (Windows)
    venv_dir = script_dir / "venv-build"
    if not args.no_venv and sys.platform == "win32":
        if not venv_dir.exists():
            run_command(
                [sys.executable, "-m", "venv", str(venv_dir)],
                "Creating virtual environment"
            )

        # Use venv Python
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:
        python_exe = sys.executable
        pip_exe = "pip"

    # Install dependencies
    run_command(
        [str(pip_exe), "install", "--upgrade", "pip"],
        "Upgrading pip"
    )

    run_command(
        [str(pip_exe), "install", "pynput>=1.7.6", "pyinstaller"],
        "Installing build dependencies"
    )

    # Build with PyInstaller
    if args.spec and Path("drinkingbird.spec").exists():
        # Use spec file for more control
        run_command(
            [str(python_exe), "-m", "PyInstaller", "--clean", "--noconfirm", "drinkingbird.spec"],
            "Building executable with spec file"
        )
    else:
        # Direct build
        pyinstaller_args = [
            str(python_exe), "-m", "PyInstaller",
            "--onefile",
            "--name", "drinkingbird",
            "--console",
            "--clean",
            "--noconfirm",
        ]

        # Add hidden imports for pynput Windows backend
        if sys.platform == "win32":
            pyinstaller_args.extend([
                "--hidden-import", "pynput.keyboard._win32",
                "--hidden-import", "pynput.mouse._win32",
            ])

        # Include README if it exists
        if Path("README.md").exists():
            sep = ";" if sys.platform == "win32" else ":"
            pyinstaller_args.extend(["--add-data", f"README.md{sep}."])

        pyinstaller_args.append("drinkingbird.py")

        run_command(pyinstaller_args, "Building executable")

    # Verify output
    if sys.platform == "win32":
        exe_path = script_dir / "dist" / "drinkingbird.exe"
    else:
        exe_path = script_dir / "dist" / "drinkingbird"

    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print("\n" + "=" * 60)
        print("  BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable: {exe_path}")
        print(f"Size: {size_mb:.2f} MB")
        print("\nTo distribute:")
        print(f"  1. Copy '{exe_path.name}' to the target Windows machine")
        print("  2. Run from command prompt: drinkingbird.exe [options]")
        print("\nNo Python installation required on target machine.")
    else:
        print("\nERROR: Expected output file not found!")
        sys.exit(1)


if __name__ == "__main__":
    main()
