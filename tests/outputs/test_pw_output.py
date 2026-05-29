from pathlib import Path

import numpy as np
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
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "nscf_etot_clobber"

    pw_out = PwOutput.from_dir(pw_directory)

    # Sanity check: the fixture really is an nscf XML with the bogus etot.
    assert (
        pw_out.raw_outputs["xml"]["input"]["control_variables"]["calculation"] == "nscf"
    )
    assert pw_out.raw_outputs["xml"]["output"]["total_energy"]["etot"] == 0.0

    # Despite that, `total_energy` should resolve via the stdout fallback.
    assert pw_out.get_output("total_energy") == pytest.approx(-75.53725762)


def test_forces_stdout_xml_agree():
    """XML and stdout `forces` agree within stdout's printed precision.

    QE prints forces in `cartesian axes, Ry/au` to 8 decimal digits (~1e-8 Ry/bohr).
    `xml.output.forces` is in Hartree/bohr; multiplying the stdout values by 2
    (1 Ha = 2 Ry) puts both on the same scale.
    """
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_220603"

    pw_out = PwOutput.from_dir(pw_directory)
    xml_forces = pw_out.raw_outputs["xml"]["output"]["forces"]["$"]
    stdout_forces = np.array(pw_out.raw_outputs["stdout"]["forces"]).flatten()

    np.testing.assert_allclose(2 * np.asarray(xml_forces), stdout_forces, atol=1e-8)


def test_forces_stdout_fallback_without_xml():
    """`PwOutput.from_files(stdout=...)` exposes `forces` via the stdout fallback."""
    stdout_file = (
        Path(__file__).parent / "fixtures" / "pw" / "default_xml_220603" / "pw.out"
    )

    pw_out = PwOutput.from_files(stdout=stdout_file)

    assert "xml" not in pw_out.raw_outputs
    assert pw_out.get_output("forces") is not None
    assert len(pw_out.get_output("forces")) == 2


def test_cutoffs_stdout_xml_agree():
    """XML and stdout `ecutwfc` / `ecutrho` agree within stdout's printed precision.

    QE prints both cutoffs to 4 decimal digits (`30.0000 Ry`); XML stores them in
    Hartree. Multiplying the XML values by 2 (1 Ha = 2 Ry) puts both on the Ry scale.
    """
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_220603"

    pw_out = PwOutput.from_dir(pw_directory)
    xml = pw_out.raw_outputs["xml"]["input"]["basis"]
    stdout = pw_out.raw_outputs["stdout"]

    assert 2 * xml["ecutwfc"] == pytest.approx(stdout["ecutwfc_ry"], abs=1e-4)
    assert 2 * xml["ecutrho"] == pytest.approx(stdout["ecutrho_ry"], abs=1e-4)


def test_cutoffs_stdout_fallback_without_xml():
    """`PwOutput.from_files(stdout=...)` exposes the cutoffs via the stdout fallback."""
    stdout_file = (
        Path(__file__).parent / "fixtures" / "pw" / "default_xml_220603" / "pw.out"
    )

    pw_out = PwOutput.from_files(stdout=stdout_file)

    assert "xml" not in pw_out.raw_outputs
    assert pw_out.outputs.parameters.ecutwfc == pytest.approx(30.0)
    assert pw_out.outputs.parameters.ecutrho == pytest.approx(240.0)


def test_k_points_stdout_xml_agree():
    """Stdout-derived k-points agree with the XML values within stdout's printed precision.

    QE prints k-points in `cart. coord. in units 2pi/alat` to 7 digits and `alat` to
    5 digits, so cartesian coordinates in 1/Å can only match the XML at ~1e-3.
    """
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_211101"

    pw_out = PwOutput.from_dir(pw_directory)

    assert pw_out.get_output("k_points_weights") == pytest.approx(
        pw_out.raw_outputs["stdout"]["k_points_weights"]
    )
    np.testing.assert_allclose(
        pw_out.get_output("k_points_cartesian"),
        pw_out.raw_outputs["stdout"]["k_points_cartesian"],
        atol=1e-3,
    )


def test_k_points_stdout_fallback_without_xml():
    """`PwOutput.from_files(stdout=...)` exposes k-point outputs via the stdout fallback."""
    stdout_file = (
        Path(__file__).parent / "fixtures" / "pw" / "default_xml_211101" / "pw.out"
    )

    pw_out = PwOutput.from_files(stdout=stdout_file)

    assert "xml" not in pw_out.raw_outputs
    assert pw_out.get_output("number_of_k_points") == 2
    assert len(pw_out.get_output("k_points_weights")) == pw_out.get_output(
        "number_of_k_points"
    )
    assert len(pw_out.get_output("k_points_cartesian")) == pw_out.get_output(
        "number_of_k_points"
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
