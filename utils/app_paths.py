from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent


def resource_path(*parts: str) -> Path:
    return project_root().joinpath(*parts)


def writable_data_dir() -> Path:
    destino = Path.home() / "Documents" / "StatPro"
    destino.mkdir(parents=True, exist_ok=True)
    return destino