"""Hace importables los ejemplos de las subcarpetas Estructurales/ y Comportamiento/."""
import sys
from pathlib import Path

_BASE = Path(__file__).parent
for _sub in ("Estructurales", "Comportamiento"):
    sys.path.insert(0, str(_BASE / _sub))
