# -*- coding: utf-8 -*-

import json
import pathlib

import numpy as np
import pytest
from pytest_cases import parametrize, parametrize_with_cases

from qe_tools.converters import get_parameters_from_cell

CASES_DATA_DIR = pathlib.Path(__file__).resolve().parent / 'data' / 'ref'


@parametrize(path=CASES_DATA_DIR.iterdir())
def case_structure_generator(path):
    """Create test cases from reference data files."""
    with open(str(path), 'r', encoding='utf-8') as in_f:
        case_data = json.load(in_f)
    system_dict = case_data['namelists']['SYSTEM']
    ibrav = system_dict['ibrav']
    ins = {'ibrav': ibrav, 'cell': case_data['cell']}

    if '-' in path.name:
        _, qe_version_with_suffix = path.name.split('-')
        qe_version, _ = qe_version_with_suffix.rsplit('.', 1)
    else:
        qe_version = None

    ins = {'ibrav': ibrav, 'cell': case_data['cell'], 'qe_version': qe_version}

    if ibrav == 0:
        return ins, None, ValueError

    outs = {}
    for key in (['a', 'b', 'c', 'cosab', 'cosac', 'cosbc'] + ['celldm({})'.format(i) for i in range(1, 7)]):
        if key in system_dict:
            outs[key] = system_dict[key]

    return ins, outs, None


def case_ibrav_zero():
    return {'cell': np.eye(3), 'ibrav': 0}, None, ValueError


def case_wrong_cell():
    return {'cell': np.eye(3), 'ibrav': 3}, None, ValueError


@parametrize_with_cases("inputs, expected_output, expected_error", cases='.')
def test_parameters_from_cell(inputs, expected_output, expected_error):
    """
    Test the `get_parameters_from_cell` behavior matches the expected
    output or error defined in the test cases.
    """
    if expected_error is not None:
        with pytest.raises(expected_error):
            get_parameters_from_cell(**inputs)
    else:
        if 'celldm(1)' in expected_output:
            inputs.setdefault('using_celldm', True)
        actual_output = get_parameters_from_cell(**inputs)
        assert actual_output.keys() == expected_output.keys()
        for key in expected_output:
            assert np.isclose(expected_output[key], actual_output[key])
