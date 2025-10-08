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
    ],
)
def test_default_xml(data_regression, xml_format):
    """Test the default XML output of pw.x."""

    name = f"default_xml_{xml_format}"

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / name

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "outputs": pw_out.raw_outputs,
            "structure": pw_out.get_output("structure"),
            "fermi_energy": pw_out.get_output("fermi_energy"),
        }
    )


def test_ase_outputs(robust_data_regression_check):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    robust_data_regression_check(
        {"structure": pw_out.get_output("structure", to="ase").todict()}
    )


def test_pymatgen_outputs(robust_data_regression_check):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    robust_data_regression_check(
        {
            "structure": pw_out.get_output("structure", to="pymatgen").as_dict(),
        },
    )
