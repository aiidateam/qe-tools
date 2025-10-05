# Scope

The main goal of this package should be to develop *easy to use* tools to deal with Quantum ESPRESSO that *just work*.

* **Easy to use**: Discoverable, consistent and intuitive APIs with minimal setup and one obvious way to do common tasks.
* **Just work**: Sensible defaults, robust input handling (paths, strings, file-like objects), predictable behavior, and clear, actionable errors.

We want to target both conventional Quantum ESPRESSO users that run calculations manually, but also offer an API that other tools can use to interface with Quantum ESPRESSO more easily.

## Road map

The basic features we want to offer, in order of priority:

1. Output parsing.
2. Input file parsing / generation / validation.
3. Interoperability with other tools ([AiiDA](https://aiida.net/), [`pymatgen`](https://pymatgen.org/), [ASE](https://ase-lib.org/), [MaRDA extractors](https://github.com/marda-alliance/metadata_extractors), ...).
4. Definitions and explanations of failure modes.
5. (tbd) Error handling approaches.

## What this package will _not_ do

* **Runnings calculations/workflows**: plenty of other tools out there for this.
  Instead, this package aims to make it easier for these tools to integrate with Quantum ESPRESSO.
* **Go beyond Quantum ESPRESSO**: The focus on the tools is entirely Quantum ESPRESSO.
  At no point will we attempt to generalize the package to e.g. other plane-wave codes.
