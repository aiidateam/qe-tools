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

## Parsing `pw.x` outputs

Say we have just run a `pw.x` calculation in the `qe_dir` directory:

```python
from qe_tools.outputs import PwOutput

qe_dir = '/Users/mbercx/project/qetools/data/qe_dir'

pw_out = PwOutput.from_dir(qe_dir)
pw_out.outputs
```

## Parsing a single output file

If you only want to parse the `stdout` of the `pw.x` calculation, you can use the `from_files` method:

```python
from qe_tools.outputs import PwOutput

pw_out = PwOutput.from_files(stdout='/Users/mbercx/project/qetools/data/qe_dir/pw.out')
pw_out.outputs
```

## Parsing an already existing input file

Currently the input class `PwInputFile` only supports parsing an already existing input file:
```python
from qe_tools.inputs.pw import PwInputFile
from pathlib import Path

pw_input = PwInputFile((Path(qe_dir) / 'pw.in').read_text())
pw_input.as_dict()
```


This will also only really parse the structure and k-points.



