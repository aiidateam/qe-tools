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


# --- SubMapping (nested output namespaces) ----------------------------------


@output_mapping
class _NestedMapping:
    c: int = Spec("b.c")
    d: int = Spec("b.d")
    missing: int = Spec("b.nope")


@output_mapping
class _ParentMapping:
    A: float = Spec("a")
    nested: _NestedMapping


class _ParentOutput(BaseOutput[_ParentMapping]):
    @classmethod
    def from_dir(cls, _: str):
        pass


def test_submapping_output_access(raw_outputs):
    """Resolved outputs on a sub-namespace are accessible via attribute."""
    outputs = _ParentOutput(raw_outputs).outputs
    assert outputs.nested.c == 3
    assert outputs.nested.d == 4


def test_submapping_missing_output_raises(raw_outputs):
    outputs = _ParentOutput(raw_outputs).outputs
    with pytest.raises(AttributeError, match="missing.*not available"):
        outputs.nested.missing


def test_submapping_list_outputs_top_level_only(raw_outputs):
    """`list_outputs` yields top-level field names only — sub-namespaces as a single entry."""
    pw_out = _ParentOutput(raw_outputs)
    # Both modes return the same result here: sub-namespaces are *always* listed
    # (even if every output is missing), and there are no unresolvable top-level
    # outputs in `_ParentMapping` for `only_available=True` to filter out.
    assert pw_out.list_outputs() == ["A", "nested"]
    assert pw_out.list_outputs(only_available=False) == ["A", "nested"]


def test_submapping_get_output_namespace_returns_dict(raw_outputs):
    """`get_output(<sub-namespace>)` returns a partial dict of available outputs."""
    pw_out = _ParentOutput(raw_outputs)
    assert pw_out.get_output("nested") == {"c": 3, "d": 4}
    # Users index the dict directly.
    assert pw_out.get_output("nested")["c"] == 3


def test_submapping_get_output_dict_shape(raw_outputs):
    """`get_output_dict()` is flat at the top level; sub-namespaces are nested dicts."""
    assert _ParentOutput(raw_outputs).get_output_dict() == {
        "A": 1,
        "nested": {"c": 3, "d": 4},
    }


def test_validation_rejects_non_spec_top_level_default():
    """Top-level field defaults that aren't `Spec`/`SubMapping` raise in `__init__`."""

    @output_mapping
    class _BadParent:
        bad: int = 42  # type: ignore[assignment]

    class _BadOutput(BaseOutput[_BadParent]):
        @classmethod
        def from_dir(cls, _: str):
            pass

    with pytest.raises(TypeError, match="_BadParent.bad"):
        _BadOutput(raw_outputs={})


def test_decorator_rejects_bare_annotation_non_output_mapping():
    """Bare annotation whose type isn't `@output_mapping`-decorated is rejected at decoration time."""
    with pytest.raises(TypeError, match="bad.*@output_mapping class"):

        @output_mapping
        class _BadBare:
            bad: int
