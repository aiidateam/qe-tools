# -*- coding: utf-8 -*-
"""
Physical or mathematical constants.
Since every code has its own conversion units, this module defines what
QE understands as for an eV or other quantities.
Whenever possible, we try to use the constants defined in
:py:mod:aiida.common.constants:, but if some constants are slightly different
among different codes (e.g., different standard definition), we define
the constants in this file.
"""

from types import SimpleNamespace

__all__ = ('DEFAULT',)

DEFAULT = SimpleNamespace(
    ## These have been put here from the one of QE, taken directly from
    ## those in aiida.common.constants
    bohr_to_ang=0.52917720859,
    ang_to_m=1.0e-10,
    ry_to_ev=13.6056917253,
    ry_si=4.35974394 / 2.0 * 10 ** (-18),
    timeau_to_sec=2.418884326155573e-17,
    invcm_to_THz=0.0299792458,
    ## Values taken from https://gitlab.com/QEF/q-e/-/blob/develop/Modules/constants.f90
    ha_si=4.3597447222071e-18,  # J
    bohr_si=0.529177210903e-10,  # m
    # From the definition of Quantum ESPRESSO, conversion from atomic mass
    # units to Rydberg units:
    #  REAL(DP), PARAMETER :: AMU_SI           = 1.660538782E-27_DP  ! Kg
    #  REAL(DP), PARAMETER :: ELECTRONMASS_SI  = 9.10938215E-31_DP   ! Kg
    #  REAL(DP), PARAMETER :: AMU_AU           = AMU_SI / ELECTRONMASS_SI
    #  REAL(DP), PARAMETER :: AMU_RY           = AMU_AU / 2.0_DP
    amu_Ry=911.4442421323,
)

DEFAULT.hartree_to_ev = DEFAULT.ry_to_ev * 2.0
DEFAULT.bohr_si = DEFAULT.bohr_to_ang * DEFAULT.ang_to_m
DEFAULT.au_gpa = DEFAULT.ha_si / (DEFAULT.bohr_si**3.0) / 1.0e9
