# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Drinkingbird
Builds a single-file Windows executable

Usage:
    pyinstaller drinkingbird.spec
"""

import sys
from PyInstaller.utils.hooks import collect_all

# Collect all pynput data files and hidden imports
datas, binaries, hiddenimports = collect_all('pynput')

a = Analysis(
    ['drinkingbird.py'],
    pathex=[],
    binaries=binaries,
    datas=datas + [('README.md', '.')],
    hiddenimports=hiddenimports + [
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='drinkingbird',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add 'drinkingbird.ico' here if you create an icon file
)
