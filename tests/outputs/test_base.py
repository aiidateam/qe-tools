from textwrap import dedent

import pytest
import yaml

from qe_tools.outputs.base import BaseOutput


class TestBaseOutput(BaseOutput):
    _output_spec_mapping = {"A": "a", "not-parsed": "e"}

    def from_dir(cls, _: str):
        pass


@pytest.fixture
def raw_outputs():
    """Simple `raw_outputs` for transparent testing."""
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
    assert result == TestBaseOutput(raw_outputs).get_output_from_spec(spec)


def test_list_outputs(raw_outputs):
    assert TestBaseOutput(raw_outputs).list_outputs() == ["A"]
    assert TestBaseOutput(raw_outputs).list_outputs(only_available=False) == [
        "A",
        "not-parsed",
    ]
