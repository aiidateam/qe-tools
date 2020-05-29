# -*- coding: utf-8 -*-

import json
import pathlib

import numpy as np
import pytest
from pytest_cases import cases_data, case_name, cases_generator, CaseData, THIS_MODULE

from qe_tools.generators.cell_conversion import get_parameters_from_cell

CASES_DATA_DIR = pathlib.Path(__file__).resolve().parent / 'data' / 'ref'


@cases_generator("case {path.name}", path=CASES_DATA_DIR.iterdir())
def case_structure_generator(path) -> CaseData:
    with open(str(path), 'r') as in_f:
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

    outs = dict()
    for key in (['a', 'b', 'c', 'cosab', 'cosac', 'cosbc'] +
                ['celldm({})'.format(i) for i in range(1, 7)]):
        if key in system_dict:
            outs[key] = system_dict[key]

    return ins, outs, None


@case_name("case ibrav=0")
def case_ibrav_zero() -> CaseData:
    return {'cell': np.eye(3), 'ibrav': 0}, None, ValueError


@case_name("case wrong cell")
def case_wrong_cell() -> CaseData:
    return {'cell': np.eye(3), 'ibrav': 3}, None, ValueError


@cases_data(module=THIS_MODULE)
def test_parameters_from_cell(case_data):
    inputs, expected_output, expected_error = case_data.get()
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
