[![Templated from python-copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mbercx/python-copier/refs/heads/main/docs/img/badge.json)](https://github.com/mbercx/python-copier)

# `qe-tools`

Python tools for working with [Quantum ESPRESSO](https://www.quantum-espresso.org/).

>[!WARNING]
> The `qe-tools` package is being redesigned significantly for the next major release (v3.0).
> Expect the API on `main` to be _very_ unstable until the alpha release, and even then there could be breaking changes.

## 📋 Road map

The basic features we want to offer, in order of priority:

1. Output parsing: see [current design](https://qe-tools.readthedocs.io/en/latest/design/outputs/).
1. Interoperability with other tools ([AiiDA](https://aiida.net/), [`pymatgen`](https://pymatgen.org/), [ASE](https://ase-lib.org/), [MaRDA extractors](https://github.com/marda-alliance/metadata_extractors), ...).
1. Input file parsing / generation / validation.
1. Definitions and explanations of failure modes.
1. (tbd) Error handling approaches.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and environment isolation. By default, `uv sync` will install the `dev` dependency group, which includes all scientific extras (`ase`, `pymatgen`), testing tools, and documentation builders.

### Quick Start
- **Set up/refresh dev environment (Latest Python version):**
    ```bash
    uv sync
    ```
- **Set up/refresh dev environment (Strict Python 3.13):**
    ```bash
    uv sync --python 3.13
    ```
- **Run the full test suite:**
    ```bash
    uv run pytest tests
    ```
- **Run linting/pre-commit on all files:**
    ```bash
    uv run pre-commit run --all-files
    ```

### Documentation
Documentation scripts in `pyproject.toml` are minimized to favor direct `uv` execution, ensuring a consistent environment without legacy overhead.

- **Build documentation:** ```bash
    uv run mkdocs build --clean --strict
    ```
- **Local Preview:** To serve the documentation locally for development:
    ```bash
    uv run mkdocs serve --dev-addr localhost:8000
    ```
- **Manual Deployment:**
    While deployment is primarily handled via CI/CD pipelines, you can manually deploy to GitHub Pages using:
    ```bash
    uv run mkdocs gh-deploy --force
    ```