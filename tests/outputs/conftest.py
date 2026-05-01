"""Helpers shared by the `tests/outputs/` test suite.

`dough.testing._serialize` (exposed via the `robust_data_regression_check` fixture)
covers most cases, but it raises on `None` values. The existing `raw_outputs`
snapshots contain `null`s from optional QE XML fields, so for those we still need
a local helper. Use `robust_data_regression_check` everywhere else.
"""

from __future__ import annotations

import numpy as np
import pytest


def _to_jsonable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_jsonable(item) for item in obj]
    return obj


@pytest.fixture()
def to_jsonable():
    return _to_jsonable


_HEAVY_ARRAY_KEYS = ("eigenvalues", "occupations_kpoint")


def _fingerprint(arr: np.ndarray) -> dict:
    flat = arr.ravel()
    return {
        "shape": list(arr.shape),
        "sum": round(float(flat.sum()), 5),
        "first": round(float(flat[0]), 5),
        "last": round(float(flat[-1]), 5),
    }


@pytest.fixture()
def fingerprint_heavy():
    """Replace large numpy-array values in `get_output_dict()` with shape/sum fingerprints.

    Keeps default_xml regression snapshots small while still detecting Spec-resolution
    regressions per QE schema version.
    """

    def factory(out_dict: dict) -> dict:
        result = {}
        for key, value in out_dict.items():
            if key in _HEAVY_ARRAY_KEYS and isinstance(value, np.ndarray):
                result[key] = _fingerprint(value)
            else:
                result[key] = _to_jsonable(value)
        return result

    return factory
