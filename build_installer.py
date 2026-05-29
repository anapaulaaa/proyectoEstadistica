from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def _data_args():
    args = []
    for nombre in ("datos", "assets"):
        carpeta = ROOT / nombre
        if carpeta.exists():
            args.extend(["--add-data", f"{carpeta}{os.pathsep}{nombre}"])
    return args


def _icon_args():
    if sys.platform == "darwin":
        icon = ROOT / "assets" / "app.icns"
    elif sys.platform.startswith("win"):
        icon = ROOT / "assets" / "app.ico"
    else:
        icon = None

    if icon is not None and icon.exists():
        return ["--icon", str(icon)]
    return []


def build(onefile: bool, clean: bool):
    try:
        import PyInstaller  # noqa: F401
    except Exception as error:
        raise SystemExit("PyInstaller no está instalado en este entorno.") from error

    salida = [
        sys.executable,
        "-m",
        "PyInstaller",
        "main.py",
        "--name",
        "StatPro",
        "--windowed",
        "--noconfirm",
        "--clean" if clean else "",
        "--onefile" if onefile else "--onedir",
        *(_icon_args()),
        *(_data_args()),
    ]

    salida = [elemento for elemento in salida if elemento]
    subprocess.run(salida, cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description="Construye el instalador de StatPro")
    parser.add_argument("--onefile", action="store_true", help="Genera un solo ejecutable por plataforma")
    parser.add_argument("--clean", action="store_true", help="Limpia la caché de build")
    args = parser.parse_args()
    build(onefile=args.onefile, clean=args.clean)


if __name__ == "__main__":
    main()