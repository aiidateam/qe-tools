# -*- coding: utf-8 -*-

__all__ = ('get_parameters_from_cell',)

from typing import Dict, Iterable, Optional

import numpy as np
import scipy.linalg as la

from .. import CONSTANTS
from ..parsers._input_base import _get_cell_from_parameters

CellT = Iterable[Iterable[float]]
ParametersT = Dict[str, float]


def get_parameters_from_cell(
    *,
    ibrav: int,
    cell: CellT,
    tolerance: float = 1e-4,
    using_celldm: bool = False,
    qe_version: Optional[str] = None,
) -> ParametersT:
    """
    Get the cell parameters from a given `ibrav` and cell. Only the
    parameters necessary for the given ibrav are returned.

    The cell must already conform to the QuantumESPRESSO convention
    for the given ``ibrav`` value. This is checked by the code; the
    strictness of the check can be controlled with the ``tolerance``
    argument.

    Note that only non-zero `ibrav` are accepted.

    Parameters
    ----------
    ibrav :
        Bravais-lattice index, as defined by QuantumESPRESSO.
    cell :
        The lattice vectors, in units of Angstrom.
    tolerance :
        Absolute tolerance on each entry of the cell, when checking if
        the parameters are consistent with the given input cell.
    using_celldm :
        Determines the format of the parameters. By default, they are
        given as ``A``, ``B``, ``C``, ``cosAB``, ``cosAC``, ``cosBC``.
        If the flag is ``True``, the ``celldm(1-6)`` format is used
        instead.
        Note that the keys in the returned dictionary are always in
        lowercase.
    qe_version :
        Defines which version of QuantumESPRESSO is used. This is
        necessary in cases where different use different
        definitions.
        If no version is specified, it will default to the latest
        implemented version.
        The string must comply with the PEP440 versioning scheme.
        Valid version strings are e.g. '6.5', '6.4.1', '6.4rc2'.

    Raises
    ------
    ValueError :
        If an invalid `ibrav` is passed, or the cell reconstructed
        from the parameters does not match the input cell.
    """

    parameters = _get_parameters_from_cell_bare(ibrav=ibrav, cell=cell)

    _check_parameters(
        ibrav=ibrav,
        cell=cell,
        parameters=parameters,
        tolerance=tolerance,
        qe_version=qe_version,
    )

    if using_celldm:
        parameters = _convert_to_celldm(parameters, ibrav=ibrav)
    return parameters


def _get_parameters_from_cell_bare(  # pylint: disable=too-many-branches
    *, ibrav: int, cell: CellT
) -> ParametersT:
    """
    Implementation of the conversion from cell to parameters, without
    checks. This function always returns the parameters in the
    A, B, C, cosAB, cosAC, cosBC form.
    """
    # pylint: disable=invalid-name
    v1, v2, v3 = [np.array(v) for v in cell]

    A, B, C = ('a', 'b', 'c')
    cosAB, cosAC, cosBC = ('cosab', 'cosac', 'cosbc')

    if ibrav == 1:
        parameters = {A: la.norm(v1)}
    elif ibrav == 2:
        parameters = {A: np.sqrt(2) * la.norm(v1)}
    elif ibrav in [-3, 3]:
        parameters = {A: 2 * la.norm(v1) / np.sqrt(3)}
    elif ibrav == 4:
        parameters = {A: la.norm(v1), C: la.norm(v3)}
    elif ibrav in [5, -5]:
        parameters = {A: la.norm(v1)}
        parameters[cosAB] = np.dot(v1, v2) / parameters[A] ** 2
    elif ibrav == 6:
        parameters = {A: la.norm(v1), C: la.norm(v3)}
    elif ibrav == 7:
        parameters = {A: np.sqrt(2) * la.norm(v1[:2]), C: 2 * v1[-1]}
    elif ibrav == 8:
        parameters = {A: la.norm(v1), B: la.norm(v2), C: la.norm(v3)}
    elif ibrav in [9, -9]:
        parameters = {A: 2 * abs(v1[0]), B: 2 * abs(v1[1]), C: la.norm(v3)}
    elif ibrav == 91:
        parameters = {A: la.norm(v1), B: la.norm(v2 + v3), C: la.norm(v3 - v2)}
    elif ibrav == 10:
        parameters = {A: 2 * v1[0], B: 2 * v2[1], C: 2 * v1[2]}
    elif ibrav == 11:
        parameters = {A: 2 * v1[0], B: 2 * v1[1], C: 2 * v1[2]}
    elif ibrav == 12:
        parameters = {A: la.norm(v1), B: la.norm(v2), C: la.norm(v3)}
        parameters[cosAB] = np.dot(v1, v2) / (parameters[A] * parameters[B])
    elif ibrav == -12:
        parameters = {A: la.norm(v1), B: la.norm(v2), C: la.norm(v3)}
        parameters[cosAC] = np.dot(v1, v3) / (parameters[A] * parameters[C])
    elif ibrav == 13:
        parameters = {A: 2 * v1[0], B: la.norm(v2), C: 2 * v3[2]}
        parameters[cosAB] = 2 * np.dot(v1, v2) / (parameters[A] * parameters[B])
    elif ibrav == -13:
        parameters = {A: 2 * abs(v1[0]), B: 2 * abs(v1[1]), C: la.norm(v3)}
        parameters[cosAC] = v3[0] / la.norm(v3)
    elif ibrav == 14:
        parameters = {A: la.norm(v1), B: la.norm(v2), C: la.norm(v3)}
        parameters[cosAB] = np.dot(v1, v2) / (parameters[A] * parameters[B])
        parameters[cosAC] = np.dot(v1, v3) / (parameters[A] * parameters[C])
        parameters[cosBC] = np.dot(v2, v3) / (parameters[B] * parameters[C])
    else:
        raise ValueError(f"The given 'ibrav' value '{ibrav}' is not understood.")
    return parameters


def _check_parameters(
    *,
    ibrav: int,
    parameters: ParametersT,
    cell: CellT,
    tolerance: float,
    qe_version: Optional[str] = None,
) -> None:
    """
    Check that the parameters describe the given cell.
    """
    system_dict = {'ibrav': ibrav, **parameters}
    cell_reconstructed = _get_cell_from_parameters(
        cell_parameters=None,  # this is only used for ibrav=0
        system_dict=system_dict,
        alat=parameters['a'],
        using_celldm=False,
        qe_version=qe_version,
    )
    if not np.allclose(cell_reconstructed, cell, rtol=0, atol=tolerance):
        raise ValueError(
            f'The cell {cell_reconstructed} constructed with ibrav={ibrav}, parameters={parameters} does not match '
            f'the input cell{cell}.'
        )


def _convert_to_celldm(parameters: ParametersT, ibrav: int) -> ParametersT:
    """
    Convert parameters from A, B, C, cosAB, cosAC, cosBC to celldm(1-6).

    The `ibrav` input is needed because the conversion is not the same
    for all `ibrav` values.
    """
    alat = parameters.pop('a')

    res_parameters = {'celldm(1)': alat / CONSTANTS.bohr_to_ang}

    for in_key, out_key in [('b', 'celldm(2)'), ('c', 'celldm(3)')]:
        if in_key in parameters:
            res_parameters[out_key] = parameters.pop(in_key) / alat

    # See subroutine abc2celldm in QE latgen.f90
    if ibrav in (0, 14):
        res_parameters['celldm(4)'] = parameters.pop('cosbc')
        res_parameters['celldm(5)'] = parameters.pop('cosac')
        res_parameters['celldm(6)'] = parameters.pop('cosab')
    elif ibrav in (-12, -13):
        res_parameters['celldm(5)'] = parameters.pop('cosac')
    elif ibrav in (-5, 5, 12, 13):
        res_parameters['celldm(4)'] = parameters.pop('cosab')

    # Make sure all input parameters were used.
    assert not parameters, f'Parameters {parameters.keys()} not used.'

    return res_parameters
