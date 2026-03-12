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
def test_default_xml(data_regression, xml_format):
    """Test the default XML output of pw.x."""

    name = f"default_xml_{xml_format}"

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / name

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "base_outputs": pw_out.get_output_dict(),
            "raw_outputs": pw_out.raw_outputs,
        }
    )


@pytest.mark.parametrize(
    "fixture_directory",
    [
        "failed_no_xml",
    ],
)
def test_failed(data_regression, fixture_directory):
    """Test failed calculations of pw.x."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / fixture_directory

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "base_outputs": pw_out.get_output_dict(),
            "raw_outputs": pw_out.raw_outputs,
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
