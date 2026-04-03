from textwrap import dedent
from glom import Spec

import pytest
import yaml

from qe_tools.outputs.base import BaseOutput, output_mapping


@output_mapping
class _TestMapping:
    A: float = Spec("a")
    not_parsed: str = Spec("e")


class TestBaseOutput(BaseOutput[_TestMapping]):
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
        "not_parsed",
    ]


def test_outputs_unavailable_raises(raw_outputs):
    outputs = TestBaseOutput(raw_outputs).outputs
    with pytest.raises(AttributeError, match="not_parsed.*not available"):
        outputs.not_parsed


def test_outputs_frozen(raw_outputs):
    outputs = TestBaseOutput(raw_outputs).outputs
    with pytest.raises(AttributeError):
        outputs.A = 999


def test_get_output_dict(raw_outputs):
    assert TestBaseOutput(raw_outputs).get_output_dict() == {"A": 1}
    assert TestBaseOutput(raw_outputs).get_output_dict(
        [
            "A",
        ]
    ) == {"A": 1}
    with pytest.raises(KeyError):
        TestBaseOutput(raw_outputs).get_output_dict(
            [
                "B",
            ]
        )
