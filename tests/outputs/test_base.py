from textwrap import dedent

import pytest
import yaml

# Note: we use and import the PwOutput class here, because we can't instantiate the
# abstract base class BaseOutput. But we are testing the methods of that class here.
from qe_tools.outputs.pw import PwOutput


@pytest.fixture
def raw_outputs():
    return yaml.safe_load(
        dedent(
            """
            a: 1
            b:
                c: 3
                d: 4
            """
        )
    )


@pytest.mark.parametrize(
    ("spec", "result"),
    [
        ("a", 1),
        ("b.c", 3),
        ("b", {"c": 3, "d": 4}),
    ],
)
def test_get_output_from_spec(raw_outputs, spec, result):
    assert result == PwOutput(raw_outputs).get_output_from_spec(spec)
