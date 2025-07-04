# -*- coding: utf-8 -*-

from __future__ import annotations

from importlib.util import find_spec

import numpy as np
import pint

from qe_tools import CONSTANTS, ELEMENTS

_has_ase = bool(find_spec('ase'))
if not _has_ase:
    raise ImportError('ASE should be properly installed to use the ASE converter.')
else:
    from ase.atoms import Atoms


def get_output_ase(self):
    """Convert the parsed data to ASE objects."""

    ureg = pint.UnitRegistry()

    converted_outputs = {}

    xml_dict = self.raw_data.get('xml')

    try:
        cell = np.array([v for v in xml_dict['output']['atomic_structure']['cell'].values()]) * CONSTANTS.bohr_to_ang
        symbols = [el['@name'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']]
        # This is to handle the case where symbols are not only
        # atom symbols (e.g., Ni1 and Ni2 in the case of an AFM computation).
        symbols_new = []
        for s in symbols:
            s_low = s.lower()
            s_elem = ''
            for e in ELEMENTS:
                e_low = e.lower()
                if e_low in s_low and len(e_low) > len(s_elem):
                    s_elem = e
            if s_elem == '':
                s_elem = s
            symbols_new.append(s_elem)
        symbols = symbols_new

        positions = (
            np.array([el['$'] for el in xml_dict['output']['atomic_structure']['atomic_positions']['atom']])
            * CONSTANTS.bohr_to_ang
        )

        if _has_ase:
            converted_outputs['ase_structure'] = Atoms(
                cell=cell,
                positions=positions,
                symbols=symbols,
                pbc=True,
            )
    except KeyError:
        pass

    try:
        converted_outputs['energy'] = xml_dict['output']['total_energy']['etot'] * CONSTANTS.ry_to_ev * ureg.eV
    except KeyError:
        pass

    try:
        converted_outputs['forces'] = (
            np.array(xml_dict['output']['forces']['$']).reshape(xml_dict['output']['forces']['@dims'])
            * 2
            * CONSTANTS.ry_to_ev
            / CONSTANTS.bohr_to_ang
            * ureg.eV
            / ureg.angstrom
        )
    except KeyError:
        pass

    return converted_outputs
