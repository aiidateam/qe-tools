# Inputs: Desired usage

## Producing a `pw.x` input file

A user might want to generate a Quantum ESPRESSO input file from other Python types, e.g.:

```
PwInput(
    structure=
    parameters=
    kpoints=
    magmom=
    ...
)
```

It will definitely be challenging to define a complete API that doesn't get overly big or convoluted.

Another approach for constructing a class that defines the inputs of a Quantum ESPRESSO calculation can be found in:

[https://github.com/elinscott/qe_input_prototype](https://github.com/elinscott/qe_input_prototype)

This defines the inputs files as `pydantic` models, and allows you to complete the namelists with tab-completion, also offers validation features based on the Quantum ESPRESSO files that define the inputs.
However, at first glance it requires a lot of Quantum ESPRESSO knowledge to populate the inputs.
We could use these classes under the hood, having a wrapper class that knows how to convert commonly used formats from ASE, `pymatgen`, etc into the corresponding namelists.

One challenge here will always be that Quantum ESPRESSO expects properties etc to be defined in terms of the _kinds_, whereas most other structure classes have a site-based approach.
This in combination with the 3-character limit for the kind names means that we'll typically have to use threshold to combine sites into one kind even if they don't have exactly the same value for all properties.
Otherwise we would create too many kinds for

## Parsing an existing `pw.x` input file

It would also be nice to be able to directly parse from a file, e.g.:

```
PwInput.from_file('path/to/file')
```

These features are already present in the package, but seem to be a bit limited.
Moreover, I would not call the class `PwInputFile`, but rather `PwInput`, to be in line with `PwOutput`, _and_ the fact that it doesn't just represent the file.
