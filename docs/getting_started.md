---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: .jupytext-sync-ipynb//ipynb,md
    main_language: python
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.3
---

# Getting started

!!! warning

    `qe-tools` is being redesigned significantly for the next major release (v3.0).
    The API below can break as we improve it. Here be dragons! 🐉

## Parsing outputs

Say you have just run a `pw.x` calculation in the `qe_dir/` directory.
You can parse the outputs from this directory using:

```python
from qe_tools.outputs import PwOutput

pw_out = PwOutput.from_dir('qe_dir/')
```

You can then obtain e.g. the Fermi energy using:

```python
pw_out.get_output('fermi_energy')
```

### Converting to other units

By default, `qe-tools` returns energies in eV. You can obtain a [`pint`](https://pint.readthedocs.io/en/stable/) quantity with unit attached using the `to` input (requires the `pint` extra: `pip install qe-tools[pint]`):

```python
fermi_energy = pw_out.get_output('fermi_energy', to='pint')
fermi_energy
```

and can then convert the value to any unit you prefer:

```python
fermi_energy.to('Ry')
```

See the [units section](units.md) for more information on the list of units we return quantities in by default.

### Tab completion

Alternatively, you can also find the **available** outputs in the `outputs` namespace:

```python
pw_out.outputs.fermi_energy
```

Since these are attributes, you can obtain them via tab completion, and if you're working in an IDE with static analysis you'll see the type of the output and a docstring. Give it a try!


!!! warning

    The `outputs` namespace is designed for interactive access.
    If an output is not available, accessing it raises `AttributeError`.
    Tab completion in an IPython kernel (e.g. in Jupyter) only shows available outputs — but static analysis tools like Pylance will show all declared outputs regardless.

### Converting to other libraries

Another output you're likely interested in is the structure:

```python
pw_out.get_output('structure')
```

But you might want the structure in the flavor of your favorite Python package.
You can also do this using the `to` argument:

```python
pw_out.get_output('structure', to='ase')
```

### Getting all outputs

To obtain a list of all available outputs:

```python
pw_out.list_outputs()
```

!!! note

    By default, the `list_outputs` method will only return the list of available outputs, i.e. that can be parsed from the output files.
    To see all **supported** outputs, run:

    ```python
    pw_out.list_outputs(only_available=False)
    ```



```python
pw_out.get_output_dict()
```

<!-- #region -->


### Parsing a single output file

If you want to parse the contents of a single output file of the `pw.x` calculation, you can use the `from_files` method:
<!-- #endregion -->

```python
from qe_tools.outputs import PwOutput

pw_out = PwOutput.from_files(stdout='qe_dir/pw.out')
```

!!! warning "Important"

    For the `pw.x` calculation, we retrieve most of the final outputs from the XML file.
    Parsing _only_ from the `stdout` file will lead to limited results.

### Other codes

We don't only provide output parsing for `pw.x`!
Below you can find and example where we plot the DOS output of a `dos.x` calculation:

```python
from qe_tools.outputs import DosOutput

dos_out = DosOutput.from_dir('dos_dir')
```

```python
import matplotlib.pyplot as plt

plt.plot(dos_out.outputs.energy, dos_out.outputs.dos)
```

!!! info "That's it for now!"

    `qe-tools` is a work in progress, and we welcome feedback!
    Feel free to [open an issue if you have comments or feature requests](https://github.com/aiidateam/qe-tools/issues/new).
