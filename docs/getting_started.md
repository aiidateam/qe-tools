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
    The usage below is expected to break as we improve the API.

## Parsing outputs

Say you have just run a `pw.x` calculation in the `qe_dir` directory.
You can parse the outputs from this directory using:

```python
from qe_tools.outputs import PwOutput

pw_out = PwOutput.from_dir('qe_dir')
```

You can then obtain e.g. the Fermi energy from:

```python
pw_out.get_output('fermi_energy')
```

Another property you might be interested in is the structure:

```python
pw_out.get_output('structure')
```

But likely, you'll want the structure in the flavor of your favorite Python package.
You can also do this using the `to` input:

```python
pw_out.get_output('structure', to='ase')
```

You can list all available outputs:

```python
pw_out.list_outputs()
```

!!! note

    By default, the `list_outputs` method will only return the list of available outputs, i.e. that can be parsed from the output files.
    To see all **supported** outputs, run:

    ```python
    pw_out.list_outputs(only_available=False)
    ```

Alternatively, you can also find the **available** outputs in the `outputs` namespace:

```python
pw_out.outputs.fermi_energy
```

!!! warning

    The `outputs` namespace is designed for interactive access.
    If an output is not available, it will not be in the namespace.
    For programmatic access, use the `get_output` method.


Finally, you can obtain a dictionary of all **available** outputs in your preferred library:

```python
pw_out.get_output_dict(to='ase')
```


### Parsing a single output file

If you want to parse the contents of a single output file of the `pw.x` calculation, you can use the `from_files` method:

```python
from qe_tools.outputs import PwOutput

pw_out = PwOutput.from_files(xml='qe_dir/pwscf.xml')
```

!!! warning "Important"

    For the `pw.x` calculation, we retrieve most of the final outputs from the XML file.
    Parsing _only_ from the `stdout` file will lead to very limited results.


### Parsing other outputs

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


## Parsing an already existing input file

!!! warning

    The section below is a description of the "old" `qe-tools` approach, and so the features are still quite limited.
    Parsing and generating input files is further down [our road map](design/scope.md#road-map).

Currently the input class `PwInputFile` only supports parsing an already existing input file:

```python
from qe_tools.inputs.pw import PwInputFile
from pathlib import Path

pw_input = PwInputFile((Path('qe_dir') / 'pw.in').read_text())
pw_input.as_dict()
```

This will also only really parse the structure and k-points at the moment, so not very useful. 😅
