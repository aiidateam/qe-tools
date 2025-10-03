[![Templated from python-copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mbercx/python-copier/refs/heads/main/docs/img/badge.json)](https://github.com/mbercx/python-copier)

# `qe-tools`

Python tools for working with [Quantum ESPRESSO](https://www.quantum-espresso.org/).

>[!WARNING]
> The `qe-tools` is being redesigned significantly for the next major release (v3.0).
> Expect the API on `main` to be _very_ unstable until the alpha release, and even then there could be breaking changes.

## 📋 Road map

The basic features we want to offer, in order of priority:

1. Output parsing.
2. Input file parsing / generation / validation.
3. Interfaces with other tools (AiiDA, `pymatgen`, ASE, ...).
4. Definitions and explanations of failure modes (i.e. exit codes/status).
5. (tbd) Error handling approaches.
