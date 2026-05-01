from pathlib import Path

from qe_tools.outputs import ProjwfcOutput


def test_projwfc_mgo(robust_data_regression_check):
    projwfc_directory = Path(__file__).parent / "fixtures" / "projwfc" / "mgo"

    proj = ProjwfcOutput.from_dir(projwfc_directory)

    out = proj.get_output_dict()
    snapshot = {
        "n_records": len(out["pdos"]),
        "records": out["pdos"],
        "pdos_total": out["pdos_total"],
    }
    robust_data_regression_check(snapshot)
