# Introduction

!!! warning

    `qe-tools` is being redesigned significantly for the next major release (v3.0).
    The previous version did not have any documentation, this one corresponds to the "latest" state of the package on the `main` branch.

## 💾 Installation

To install the latest `main` branch

    git clone git@github.com:aiidateam/qe-tools.git
    pip install -e qe-tools

!!! warning

    The latest `main` will be very unstable until we get to a major release.
    Here be dragons! 🐉

To install latest stable release (v2.3.0) from the [PyPI](https://pypi.org/), simply use `pip`:

    pip install qe-tools

## 📋 Road map

The basic features we want to offer, in order of priority:

1. Output parsing.
2. Input file parsing / generation / validation.
3. Interfaces with other tools (AiiDA, `pymatgen`, ASE, ...).
4. Definitions and explanations of failure modes (i.e. exit codes/status).
5. (tbd) Error handling approaches.
