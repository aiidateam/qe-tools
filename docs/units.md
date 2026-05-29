# Units

Currently, `qe-tools` aims to report each output in the unit Quantum ESPRESSO uses, rather than imposing a single unit choice across the board.
This keeps the values you get out aligned with what most Quantum ESPRESSO users would expect.

The unit of each output is declared on each field (via a `Unit(...)` marker) and stated explicitly in the field's docstring.
The defaults per output class are:

| Output class       | Energy | Length  | Force     | Stress | Other            |
| ------------------ | ------ | ------- | --------- | ------ | ---------------- |
| `PwOutput`         | `Ry`   | `bohr`  | `Ry/bohr` | `kbar` | volume `bohr³`, k-points `1/bohr`, magnetization `μ_B`, time `s` |
| `DosOutput`        | `eV`   | —       | —         | —      | DOS `1/eV`       |
| `BandsOutput`      | `eV`   | —       | —         | —      | k-points in the units `bands.x` writes (typically `2π/alat`) |
| `ProjwfcOutput`    | `eV`   | —       | —         | —      | pDOS `1/eV`      |

A couple of fields in `PwOutput` come from sources QE prints in eV (e.g. `highest_occupied_level`, `lowest_unoccupied_level` from the stdout line `... (ev): ...`); those are exposed in eV, as written.
The docstring of every output field states its unit, so the source of truth is always the field itself.

Some outputs - like the total energy - are written in Ry in the stdout but in Ha in the XML.
Here we again choose the units most users will be familiar with: Ry.

!!! info "Switching to a single set of units"

    Originally, we had selected a single set of units (eV, eV/Å, ...) and wanted to enforce each output (and future input) was specified in these units.
    However, this turned out to cause a lot of friction with the QE ecosystem.
    We're looking into making the unit set configurable, so this consistent behavior can be recovered in the future.

## Converting to different units

To convert outputs to different units, we rely on the [`pint` package](https://pint.readthedocs.io/en/stable/).
It is an optional dependency; install it via the `pint` extra:

    pip install qe-tools[pint]

You can then request a `pint` quantity from any unit-annotated output:

```python
fermi_energy = pw_out.get_output('fermi_energy', to='pint')
```

This will return a `pint` quantity with unit attached.
You can then convert the value to any unit you prefer:

```python
fermi_energy.to('eV')
```
