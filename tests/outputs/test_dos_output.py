from pathlib import Path

import pytest

from qe_tools.outputs import DosOutput


@pytest.mark.parametrize(
    "spin_type",
    [
        "nospin",
        "collinear",
    ],
)
def test_default_xml(robust_data_regression_check, spin_type):
    """Test the default XML output of pw.x."""

    pw_directory = Path(__file__).parent / "fixtures" / "pw" / spin_type
    dos_directory = Path(__file__).parent / "fixtures" / "dos" / spin_type

    dos_out = DosOutput.from_files(
        dos=dos_directory / "prefix.dos",
        stdout=dos_directory / "dos.out",
        xml=pw_directory / "data-file-schema.xml",
    )

    robust_data_regression_check(
        {
            "full_dos": dos_out.get_output("full_dos"),
            "spin_type": dos_out.get_output("spin_type"),
        }
    )
