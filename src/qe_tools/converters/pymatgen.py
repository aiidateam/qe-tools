from __future__ import annotations

from importlib.util import find_spec

_has_pmg = bool(find_spec("pymatgen"))
if not _has_pmg:
    raise ImportError("pymatgen should be properly installed to use the pymatgen converter.")
