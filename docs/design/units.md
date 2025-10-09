# Units

We make the decision to have a single opinionated set of units.
This means that even for the base outputs the units **do not** correspond to the Quantum ESPRESSO outputs.
The main reason for this is _consistency_:

1. Quantum ESPRESSO is not consistent in its usage of units for in- and outputs.
    There are even discrepancies between output files (stdout and XML).

    !!! note

        This is not an accusation: scientific development in FORTRAN while trying to stay backwards-compatible is challenging, and science often gets in the way of taking the time for good design.
        Here we have the privilege of starting from the ground up in a much simpler context.

2. We want to have a SSOT for units that we can make very clear and accessible to the user.
   When they get an energy, it's going to be in eV, not Ha.
   If users desire to work in different units, we can look into using `pint`, see:

   https://github.com/aiidateam/qe-tools/issues/106
