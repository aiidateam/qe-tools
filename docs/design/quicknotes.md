# Quick notes

A place to write down quick notes on the design decisions made for the `qe-tools` package.

## Main goal

The main goal of this package should be to develop *easy to use* tools to deal with Quantum ESPRESSO that *just work*.

* **Easy to use**: Tools should be easy to find, intuitive and require as few steps as possible to get the desired outcome.
* **Just work**: Tools should be robust and clever, working as the user intends with a variety of input options without having to understand their functionality in too much detail.

The basic features we want to offer, in order of priority:

1. Output parsing.
2. Input file parsing / generation / validation.
3. Interfaces with other tools (AiiDA, `pymatgen`, ASE, ...).
4. Definitions and explanations of failure modes.

## Parsing

![](img/class_structure.png)

### One output object for each calculation

Although QE can provide the output of a calculation distributed over various files, it would be useful to gather all of these into a single "output" object from which the user can access all data they are interested in.

Question: would it instead not be useful to have one object that has both inputs and outputs? Reasons could be:

1. The user might want to just load both input/output from the directory in one fell swoop, since they might want to work with the output of the calculation differently depending on the input.
2. Some parsing functionality might be easier to implement if the inputs are known.
   I think it may even be necessary for some outputs to know e.g. what the number of k-points are. Some of the inputs are also in the XML output though...

### One output file, one parser

Even though the user might want to obtain all outputs from a single object, it still is sensible to have a separate parser tool for each output file.
The output class can then rely on these nicely separated parsers to combine all outputs into one based on preference.

## One input per code

Typically, each executable in the Quantum ESPRESSO suite will have a single input file.
Technical exceptions are restart files such as the charge density, but those are full (sometimes binary system-specific) files that don't require a Python object to represent.
The input class should allow for several use cases:

1. Generate a Quantum ESPRESSO input file from various Python types.
2. Parse an existing input file into various Python types.

## ASE/`pymatgen`/AiiDA/... support

Most users will want to provide e.g. the input structure or output data in the flavour of their choosing.
We should provide tools for converting:

1. The flavored Python types (`Structure`, `Atoms`, ...) into the Quantum ESPRESSO input file.
2. The Quantum ESPRESSO raw parsed output into the flavour's Python type.
