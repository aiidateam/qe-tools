# Units

Quantum ESPRESSO uses different units for the same quantity across input, stdout, and XML.
Instead, `qe-tools` exposes outputs on e.g. the `PwOutput` class in a single opinionated set of units, independent of what Quantum ESPRESSO writes to the XML or stdout.
Below you can find the units we chose for each quantity:

| Quantity              | Unit              |
| --------------------- | ----------------- |
| Energy                | `eV`              |
| Force                 | `eV/Å`            |
| Stress / pressure     | `GPa`             |
| Length                | `Å`               |
| Volume                | `Å³`              |
| Reciprocal length     | `1/Å`             |
| Density of states     | `1/eV`            |
| Magnetic moment       | `μ_B`             |
| Time                  | `s`               |

## Converting to different units

To convert outputs to different units, we rely on the [`pint` package](https://pint.readthedocs.io/en/stable/):

```python
fermi_energy = pw_out.get_output('fermi_energy', to='pint')
```

This will return a `pint` quantity with unit.
You can then convert the value to any unit you prefer:

```python
fermi_energy.to('Ry')
```
