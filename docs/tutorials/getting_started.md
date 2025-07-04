# Getting started

## Parsing `pw.x` outputs

Say we have just run a `pw.x` calculation in the `qe_dir` directory:

```
from qe_tools.outputs.pw import PwOutput

pw_out = PwOutput.from_dir("qe_dir")
pw_out.outputs
```

## Parsing a single output file

If you only want to parse the `stdout` of the `pw.x` calculation, you can load the parser class directly:

```
from qe_tools.outputs.parsers.pw import PwStdoutParser
pw_out = PwStdoutParser.from_file('qe_dir/pw.out')
```

## Parsing an already existing input file

Currently the input class `PwInputFile` only supports parsing an already existing input file:

```
from qe_tools.inputs.pw import PwInputFile
from pathlib import Path

pw_input = PwInputFile(Path('qe_dir/pw.in').read_text())
```

This will also only really parse the structure and k-points.
