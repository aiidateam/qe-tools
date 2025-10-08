# Scope

The main goal of this package should be to develop *easy to use* tools to deal with Quantum ESPRESSO that *just work*.

* **Easy to use**: Discoverable, consistent and intuitive APIs with minimal setup and one obvious way to do common tasks.
* **Just work**: Sensible defaults, robust input handling (paths, strings, file-like objects), predictable behavior, and clear, actionable errors.

We want to target both conventional Quantum ESPRESSO users that run calculations manually, but also offer an API that other tools can use to interface with Quantum ESPRESSO more easily.

## Quantum ESPRESSO versions

Providing and maintaining support for _all_ Quantum ESPRESSO versions is not sustainable.
Hence, starting from `qe-tools==3.0`, we implement the following support conventions:

* Provide support for the five latest minor versions of Quantum ESPRESSO.
* Older versions are supported up to a maximum of four years.

In line with these conventions, we aim to support Quantum ESPRESSO v7.0 and above for the release of `qe-tools` v3.0.

## Road map

The basic features we want to offer, in order of priority:

1. Output parsing, see [current design](outputs.md).
1. Interoperability with other tools ([AiiDA](https://aiida.net/), [`pymatgen`](https://pymatgen.org/), [ASE](https://ase-lib.org/), [MaRDA extractors](https://github.com/marda-alliance/metadata_extractors), ...).
1. Input file parsing / generation / validation.
1. Definitions and explanations of failure modes.
1. (tbd) Error handling approaches.

## What this package will _not_ do

* **Runnings calculations/workflows**: plenty of other tools out there for this.
  Instead, this package aims to make it easier for these tools to integrate with Quantum ESPRESSO.
* **Go beyond Quantum ESPRESSO**: The focus on the tools is entirely Quantum ESPRESSO.
  At no point will we attempt to generalize the package to e.g. other plane-wave codes.
