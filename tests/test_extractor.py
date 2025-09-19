import json
from pathlib import Path

import pytest

from qe_tools.extractors import extract


@pytest.mark.parametrize("parser", ["pw", "cp"])
def test_input_dict_extraction(parser: str):
    datadir = Path(__file__).resolve().parent / "data"
    filepath = datadir / f"{parser}.in"
    refpath = datadir / "extractor_ref" / f"{parser}.json"
    assert extract(filepath.as_posix(), parser) == json.loads(refpath.read_text())
