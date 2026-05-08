from pathlib import Path

from qe_tools.outputs import BandsOutput


def test_bands_mgo(robust_data_regression_check):
    bands_directory = Path(__file__).parent / "fixtures" / "bands" / "mgo"

    bands = BandsOutput.from_dir(bands_directory)

    out = bands.get_output_dict()
    snapshot = {
        "number_of_kpoints": out["number_of_kpoints"],
        "number_of_bands": out["number_of_bands"],
        "k_points": out["k_points"],
        "eigenvalues": out["eigenvalues"],
        "k_path_distances": out["k_path_distances"],
        "high_symmetry_points": out["high_symmetry_points"],
        "high_symmetry_distances": out["high_symmetry_distances"],
        "is_high_symmetry": out["is_high_symmetry"].tolist(),
        "representations": out["representations"],
    }
    robust_data_regression_check(snapshot)


def test_bands_eigenvalues_gnu_fallback(robust_data_regression_check):
    """`eigenvalues` should resolve from the `.gnu` file when no `.dat` is provided.

    The `.dat` file is the canonical source for `eigenvalues`, but `BandsOutput` also
    exposes a `Coalesce` fallback to `.gnu` so that users who only have the gnuplot
    file can still read eigenvalues.
    """
    gnu_file = (
        Path(__file__).parent / "fixtures" / "bands" / "mgo" / "MgO-bands.dat.gnu"
    )

    bands = BandsOutput.from_files(gnu=gnu_file)

    out = bands.get_output_dict()
    snapshot = {
        "number_of_kpoints": out["number_of_kpoints"],
        "number_of_bands": out["number_of_bands"],
        "eigenvalues": out["eigenvalues"],
        "k_path_distances": out["k_path_distances"],
    }
    robust_data_regression_check(snapshot)
