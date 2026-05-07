from pathlib import Path

import pytest

from qe_tools.outputs.pw import PwOutput


@pytest.mark.parametrize(
    "xml_format",
    [
        "211101",
        "220603",
        "230310",
        "240411",
        "250521",
    ],
)
def test_default_xml(data_regression, fingerprint_heavy, xml_format):
    """Test the default XML output of pw.x."""

    name = f"default_xml_{xml_format}"

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / name

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "base_outputs": fingerprint_heavy(pw_out.get_output_dict()),
            "raw_outputs": pw_out.raw_outputs,
        }
    )


@pytest.mark.parametrize(
    "fixture_directory",
    [
        "collinear",
    ],
)
def test_success_base(data_regression, fingerprint_heavy, fixture_directory):
    """Test the base outputs of successful pw.x calculations."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / fixture_directory

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "base_outputs": fingerprint_heavy(pw_out.get_output_dict()),
        }
    )


@pytest.mark.parametrize(
    "fixture_directory",
    [
        "failed_no_xml",
    ],
)
def test_failed(data_regression, to_jsonable, fixture_directory):
    """Test failed calculations of pw.x."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / fixture_directory

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "base_outputs": to_jsonable(pw_out.get_output_dict()),
            "raw_outputs": pw_out.raw_outputs,
        }
    )


def test_total_energy_nscf_clobber():
    """Test that `total_energy` falls back to stdout when an nscf XML clobbered the scf one.

    QE writes `<etot>0.0</etot>` for `nscf` and `bands` runs (see PW/src/non_scf.f90).
    In the common `scf → nscf` workflow at a shared `prefix`, the nscf run overwrites
    the scf XML on disk, so the only reliable source of the SCF total energy is the
    `!  total energy = ...` line in the scf stdout.
    """
    from qe_tools import CONSTANTS

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "nscf_etot_clobber"

    pw_out = PwOutput.from_dir(pw_directory)

    # Sanity check: the fixture really is an nscf XML with the bogus etot.
    assert (
        pw_out.raw_outputs["xml"]["input"]["control_variables"]["calculation"] == "nscf"
    )
    assert pw_out.raw_outputs["xml"]["output"]["total_energy"]["etot"] == 0.0

    # Despite that, `total_energy` should resolve via the stdout fallback.
    assert pw_out.get_output("total_energy") == pytest.approx(
        -75.53725762 * CONSTANTS.ry_to_ev
    )


def test_insulator_homo(robust_data_regression_check):
    """Test stdout-derived `highest_occupied_level` from an insulator SCF."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "insulator_homo"

    pw_out = PwOutput.from_dir(pw_directory)

    robust_data_regression_check(
        {
            "highest_occupied_level": pw_out.get_output("highest_occupied_level"),
        }
    )


def test_tot_magnetization(data_regression):
    """Test the output of a spin-polarized pw.x calculation with tot_magnetization."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "tot_magnetization"

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "fermi_energy_up": pw_out.get_output("fermi_energy_up"),
            "fermi_energy_down": pw_out.get_output("fermi_energy_down"),
            "number_of_bands": pw_out.get_output("number_of_bands"),
        }
    )


def test_ase_outputs(robust_data_regression_check):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    robust_data_regression_check(
        {
            "structure": pw_out.get_output("structure", to="ase").todict(),
            "fermi_energy": pw_out.get_output("fermi_energy", to="ase"),
        },
    )


def test_pymatgen_outputs(robust_data_regression_check):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    robust_data_regression_check(
        {
            "structure": pw_out.get_output("structure", to="pymatgen").as_dict(),
            "fermi_energy": pw_out.get_output("fermi_energy", to="ase"),
        },
    )
