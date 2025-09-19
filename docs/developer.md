# Developer Guide

## Hatch

We use [Hatch](https://hatch.pypa.io/latest) to set up environments and scripts for most developer tasks.
To see a table of the available environmens and their scripts, run:

    hatch env show

### Documentation

The easiest way to work on the documentation is to start the server locally via:

    hatch run docs:serve

And go to the provided URL.
If you only want to build the documentation locally, there is also a script for that:

    hatch run docs:build

### Pre-commit

You can install the [pre-commit](https://pre-commit.com/) hooks with:

    hatch run precommit:install

Or run them via:

    hatch run precommit:install

From the extensive [Ruff ruleset](https://docs.astral.sh/ruff/rules/) that Hatch uses, we ignore the following:

| Code      | Rule                                                                                                                      | Rationale / Note                                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `TRY003`  | [raise-vanilla-args](https://docs.astral.sh/ruff/rules/raise-vanilla-args/)                                               | Formatting warning/exception messages beforehand makes the code less readable, for a minor benefit in readability of the exception. |
| `EM101`   | [raw-string-in-exception](https://docs.astral.sh/ruff/rules/raw-string-in-exception/)                                     | Same as `TRY003`                                                                                                                    |
| `EM102`   | [f-string-in-exception](https://docs.astral.sh/ruff/rules/f-string-in-exception/)                                         | Same as `TRY003`                                                                                                                    |
| `PLR2004` | [magic-value-comparison](https://docs.astral.sh/ruff/rules/magic-value-comparison/)                                       | We have a lot of “magic values” to compare with in scientific code; naming them all would reduce readability for little benefit.    |
| `FBT002`  | [boolean-default-value-positional-argument](https://docs.astral.sh/ruff/rules/boolean-default-value-positional-argument/) | We understand the concept, but adhering to this rule is not a small change in syntax; disable for now.                              |
| `TID252`  | [relative-imports](https://docs.astral.sh/ruff/rules/relative-imports/)                                                   | We don’t mind relative imports; as long as you don’t go up a level, they’re more readable (less verbose).                           |
