"""Pin the projwfc PDOS column-decoding conventions."""

from __future__ import annotations

import numpy as np

from qe_tools.outputs.parsers.projwfc import PdosAtmWfcParser, PdosTotParser


def test_pdos_atm_wfc_unpolarised_p():
    """Spin-unpolarised `l=1` (p) PDOS file: 1 ldos col + 3 m cols."""
    content = (
        "# E (eV)   ldos(E)   pdos(E)    pdos(E)    pdos(E)\n"
        " -1.000   0.300   0.100   0.100   0.100\n"
        "  0.000   0.600   0.200   0.200   0.200\n"
        "  1.000   0.900   0.300   0.300   0.300\n"
    )
    parsed = PdosAtmWfcParser.parse(content)

    np.testing.assert_array_equal(parsed["energies"], [-1.0, 0.0, 1.0])
    np.testing.assert_array_equal(parsed["ldos"], [0.3, 0.6, 0.9])
    np.testing.assert_array_equal(
        parsed["pdos_m"],
        [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2], [0.3, 0.3, 0.3]],
    )


def test_pdos_atm_wfc_spin_polarised_reshape_axes():
    """Spin-polarised `l=1` PDOS: pin the (n_e, spin, m) axis order.

    QE writes the columns as `up_m1, dw_m1, up_m2, dw_m2, up_m3, dw_m3`.
    We expect `pdos_m[:, spin, m]` with `spin=0` for up, `spin=1` for down.
    """
    # ldos_up, ldos_dw, then 6 m-columns interleaved per spin
    content = (
        "# E (eV)  ldosup(E)  ldosdw(E)  "
        "pdosup(E) pdosdw(E) pdosup(E) pdosdw(E) pdosup(E) pdosdw(E)\n"
        # Pick distinct values for each (spin, m) so axis order is unambiguous.
        "0.0  9.0  8.0  10  20  30  40  50  60\n"
    )
    parsed = PdosAtmWfcParser.parse(content)

    np.testing.assert_array_equal(parsed["ldos"], [[9.0, 8.0]])
    assert parsed["pdos_m"].shape == (1, 2, 3)
    # Spin-up (axis 1 = 0) follows the up_m1, up_m2, up_m3 columns.
    np.testing.assert_array_equal(parsed["pdos_m"][0, 0, :], [10, 30, 50])
    # Spin-down (axis 1 = 1) follows the dw_m1, dw_m2, dw_m3 columns.
    np.testing.assert_array_equal(parsed["pdos_m"][0, 1, :], [20, 40, 60])


def test_pdos_tot_spin_polarised():
    """`pdos_tot` with spin-polarised columns: dosup, dosdw, pdosup, pdosdw."""
    content = (
        "# E (eV)  dosup(E)  dosdw(E)  pdosup(E)  pdosdw(E)\n"
        " -1.0  1.0  2.0  10.0  20.0\n"
        "  0.0  3.0  4.0  30.0  40.0\n"
    )
    parsed = PdosTotParser.parse(content)

    np.testing.assert_array_equal(parsed["energies"], [-1.0, 0.0])
    np.testing.assert_array_equal(parsed["dos_total"], [[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_array_equal(parsed["pdos_total"], [[10.0, 20.0], [30.0, 40.0]])
