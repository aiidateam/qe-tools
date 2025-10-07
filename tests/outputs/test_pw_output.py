"""Tests for the ``PwOutput``."""

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

    directory = Path(__file__).parent / "fixtures" / "pw" / name

    pw_out = PwOutput.from_dir(directory)

    data_regression.check(
        {
            "outputs": pw_out.raw_outputs,
        }
    )


def test_ase_outputs(data_regression, json_serializer):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "structure": json_serializer(
                pw_out.get_output("structure", fmt="ase").todict()
            ),
        }
    )


def test_pymatgen_outputs(data_regression):
    pw_directory = Path(__file__).parent / "fixtures" / "pw" / "default_xml_240411"

    pw_out = PwOutput.from_dir(pw_directory)

    data_regression.check(
        {
            "structure": pw_out.get_output("structure", fmt="pymatgen").as_dict(),
        }
    )
