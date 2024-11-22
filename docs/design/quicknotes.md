# Quick notes

A place to write down quick notes on the design decisions made for the `qe-tools` package.

## Main goal

The main goal of this package should be to develop **easy to use** tools to deal with Quantum ESPRESSO that **just work**.

* **Easy to use**: Tools should be easy to find, intuitive and require as few steps as possible to get the desired outcome.
* **Just work**: Tools should be robust and clever, working as the user intends with a variety of input options without having to understand their functionality in too much detail.

## One input per code

Typically, each executable in the Quantum ESPRESSO suite will have a single input file.
Technical exceptions are restart files such as the charge density, but those are full (sometimes binary system-specific) files that don't require a Python object to represent.
The input class should allow for two use cases:

1. Generate a Quantum ESPRESSO input file from various Python types.
2. Parse an existing input file into various Python types.

## One output object for each calculation

Although QE can provide the output of a calculation distributed over various files, it would be useful to gather all of these into a single "output" object from which the user can access all data they are interested in.

Question: would it instead not be useful to have one object that has both inputs and outputs? Reasons could be:

1. The user might want to just load both input/output from the directory in one fell swoop, since they might want to work with the output of the calculation differently depending on the input.
2. Some parsing functionality might be easier to implement if the inputs are known. I think it may even be necessary for some outputs to know e.g. what the number of k-points are. Some of the inputs are also in the XML output though...

## One output file, one parser

Even though the user might want to obtain all outputs from a single object, it still is sensible to have a separate parser tool for each output file.
The output class can then rely on these nicely separated parsers to combine all outputs into one based on preference.

## ASE/`pymatgen`/AiiDA/... support

Most users will want to provide e.g. the input structure or output data in the flavour of their choosing.
We should provide tools for converting:

1. The flavored Python types (`Structure`, `Atoms`, ...) into the Quantum ESPRESSO input file.
2. The Quantum ESPRESSO raw parsed output into the flavour's Python type.

---

Notes from Guillaume:

I have changed the structure of the code to better reflect the distinction between input and output parsers.

For the outputs, I created objects such as PwOutput, that inherit from an abstract BaseOutput, that for now can be instantiated with a from_dir method (a from_files method could/should be added as well).

A user with a job that ran in a given directory could get the outputs easily using this classmethod. In these from_dir methods, specific XML and/or standard output Parsers would be used to get the results.

Each Parser would parse a single file, and the logic of parsing and extracting the outputs from the different codes would have to be implemented in each from_dir method.

For instance, a NebOutput.from_dir would parse the standard output of the global computation and probably the standard outputs and/or XML files for each image. The extracted outputs would be stored as a simple dictionary and these objects would not rely on any external package.

Then, in qe_tools.extractors, ASE and pymatgen objects could be constructed (e.g., ase.Atoms/pymatgen.Structure, band structures,...), allowing each to be optional dependencies.

This is only the base logic of the new structure and many things remain to be implemented.

The idea now is to see what breaks with this in `aiida-quantumespresso` and how the parsing could be moved from there to here. Then, more will be added depending on the needs.
