# Outputs: Desired usage

## One class to rule both input/output

If you want to parse all the inputs and outputs from a `pw.x` run in the `pw_run` directory:

```
from qe_tools.parsers import PwParser

parser = PwParser.from_dir('pw_run')
```

Then you can obtain the outputs as

```
parser.outputs['structure']
```

similarly, the inputs can then be obtained from the `inputs` attribute:

```
parser.inputs['structure']
```

(Maybe this should not be a "parser", but a "calculation". E.g. `PwCalc` that has `inputs` and `outputs`.)
