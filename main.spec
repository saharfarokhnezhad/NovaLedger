# -*- mode: python ; coding: utf-8 -*-

from glob import glob
from PyInstaller.utils.hooks import collect_all

# -----------------------------
# Files
# -----------------------------

datas = []

# همه فایل‌های KV
for kv in glob("*.kv"):
    datas.append((kv, "."))

# دیتابیس
datas.append(("expense.db", "."))

# پوشه‌ها
datas.append(("assets", "assets"))
datas.append(("database", "database"))

# -----------------------------
# KivyMD
# -----------------------------

binaries = []
hiddenimports = []

tmp = collect_all("kivymd")
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

hiddenimports += [
    "kivymd.icon_definitions.md_icons",
]

# -----------------------------
# Analysis
# -----------------------------

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# -----------------------------
# EXE
# -----------------------------

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NovaLedger",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="logo.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="NovaLedger",
)