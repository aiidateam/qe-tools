# -*- coding: utf-8 -*-
"""
Tests for the version parsing helper.
"""

import pytest

from qe_tools.utils._qe_version import parse_version, _LatestVersionImpl

VERSION_INPUT_SORTED = ['2.3', '6.4.1', '6.4.2a1', '6.4.2', None]


def test_sorting():
    """
    Check that the parsed versions compare/sort in the correct way.
    """
    versions_parsed = [parse_version(inp) for inp in VERSION_INPUT_SORTED]
    assert sorted(versions_parsed) == versions_parsed


@pytest.mark.parametrize('input_', VERSION_INPUT_SORTED)
def test_idempotent(input_):
    """
    Check that the parsing function is idempotent (returns the same
    object when given an already-parsed object).
    """
    parsed = parse_version(input_)
    parsed_twice = parse_version(parsed)
    assert parsed is parsed_twice


@pytest.mark.parametrize('input_', VERSION_INPUT_SORTED)
def test_equal(input_):
    """
    Test that two objects created from the same input compare equal.
    """
    parsed1 = parse_version(input_)
    parsed2 = parse_version(input_)
    assert parsed1 == parsed2
    # These tests are needed to check that the 'latest' version has
    # a consistent ordering.
    assert not parsed1 < parsed2
    assert not parsed1 > parsed2
    assert parsed1 <= parsed2
    assert parsed1 >= parsed2


def test_singleton():
    """
    Check that the '_LatestVersionImpl' singleton check works.
    """
    with pytest.raises(TypeError):
        _LatestVersionImpl()
