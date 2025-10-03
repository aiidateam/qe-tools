# Developer Guide

## Quick start

Thanks for contributing! 🙏
Below you can find an overview of the commands to get you up and running quickly.

First clone the repository from GitHub

    git clone <GITHUB-REPO>

and install the package locally in **editable** mode (`-e`):

    cd qe-tools
    pip install -e .

!!! note
    We support various tools for developers.
    Select your preferred one from the tabs below.
    If you don't know `uv` or Hatch, stick with the default for now.

=== "Default"

    The "default" approach to developing is to install the development extras in your current environment:

        pip install -e .[pre-commit,tests,docs]

    🔧 **Pre-commit**

    To make sure your changes adhere to our formatting/linting preferences, install the pre-commit hooks:

        pre-commit install

    They will then run on every `git commit`.
    You can also run them on e.g. all files using:

        pre-commit run -a

    Drop the `-a` option in case you only want to run on staged files.

    🧪 **Tests**

    You can run all tests in the `tests` directory with `pytest`:

        pytest

    Or select the test module:

        pytest tests/parsers/test_pw.py

    See the [`pytest` documentation](https://docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run) for more information.

    📚 **Documentation**

    We use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) as our documentation framework.
    Start the documentation server with:

        mkdocs serve

    and open the documentation in your browser via the link shown.
    Every time you save a file, the corresponding documentation page is updated automatically!

=== "uv"

    `uv` is a Python package and project manager.
    See [the documentation](https://docs.astral.sh/uv/getting-started/installation/) on how to install `uv`.

    🔧 **Pre-commit**

    To make sure your changes adhere to our formatting/linting preferences, install the pre-commit hooks:

        uvx pre-commit install

    They will then run on every `git commit`.
    You can also run them on e.g. all files using:

        uvx pre-commit run -a

    Drop the `-a` option in case you only want to run on staged files.

    !!! note
        Here we use the [`uvx` command](https://docs.astral.sh/uv/guides/tools/#running-tools) to run the `pre-commit` tool without installing it.
        Alternatively you can also install [`pre-commit` as a tool](https://docs.astral.sh/uv/guides/tools/#installing-tools) and omit `uvx`.

    🧪 **Tests**

    You can run all tests in the `tests` directory with `pytest`:

        uv run pytest

    Or select the test module:

        uv run pytest tests/parsers/test_pw.py

    See the [`pytest` documentation](https://docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run) for more information.

    📚 **Documentation**

    We use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) as our documentation framework.
    Start the documentation server with:

        mkdocs serve

    and open the documentation in your browser via the link shown.
    Every time you save a file, the corresponding documentation page is updated automatically!

=== "Hatch"

    You can use [Hatch](https://hatch.pypa.io/1.9/install/) to run development tools in isolated environments.
    To see a table of the available environments and their scripts, run:

        hatch env show

    🔧 **Pre-commit**

    To make sure your changes adhere to our formatting/linting preferences, install the pre-commit hooks:

        hatch run pre-commit:install

    They will then run on every `git commit`.
    You can also run them on e.g. all files using:

        hatch run pre-commit:run -a

    Drop the `-a` option in case you only want to run on staged files.

    🧪 **Tests**

    You can run all tests in the `tests` directory using:

        hatch test

    Or select the test module:

        hatch test tests/parsers/test_pw.py

    You can also run the tests for a specific Python version with the `-py` option:

        hatch test -py 3.11

    Or all supported Python `versions` with `--all`:

        hatch test --all

    See the [Hatch documentation](https://hatch.pypa.io/1.12/tutorials/testing/overview/) for more information.

    📚 **Documentation**

    We use [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) as our documentation framework.
    Start the documentation server with:

        hatch run docs:serve

    and open the documentation in your browser via the link shown.
    Every time you save a file, the corresponding documentation page is updated automatically!


## Pre-commit rules

From the extensive [Ruff ruleset](https://docs.astral.sh/ruff/rules/), we ignore the following globally:

| Code      | Rule                                                                                                                      | Rationale / Note                                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `TRY003`  | [raise-vanilla-args](https://docs.astral.sh/ruff/rules/raise-vanilla-args/)                                               | Formatting warning/exception messages beforehand makes the code less readable, for a minor benefit in readability of the exception. |
| `EM101`   | [raw-string-in-exception](https://docs.astral.sh/ruff/rules/raw-string-in-exception/)                                     | Same as `TRY003`                                                                                                                    |
| `EM102`   | [f-string-in-exception](https://docs.astral.sh/ruff/rules/f-string-in-exception/)                                         | Same as `TRY003`                                                                                                                    |
| `PLR2004` | [magic-value-comparison](https://docs.astral.sh/ruff/rules/magic-value-comparison/)                                       | We have a lot of “magic values” to compare with in scientific code; naming them all would reduce readability for little benefit.    |
| `FBT002`  | [boolean-default-value-positional-argument](https://docs.astral.sh/ruff/rules/boolean-default-value-positional-argument/) | We understand the concept, but adhering to this rule is not a small change in syntax; disable for now.                              |
| `TID252`  | [relative-imports](https://docs.astral.sh/ruff/rules/relative-imports/)                                                   | We don’t mind relative imports; as long as you don’t go up a level, they’re more readable (less verbose).                           |

And the following rules for the files in the `tests` directory:

| Code      | Rule                                                                                                                      | Rationale / Note                                                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `INP001`  | [implicit-namespace-package](https://docs.astral.sh/ruff/rules/implicit-namespace-package/)                               | When tests are not part of the package, there is no need for `__init__.py` files.                                                   |
| `S101`    | [assert](https://docs.astral.sh/ruff/rules/assert/)                                                                       | Asserts should not be used in production environments, but are fine for tests.                                                      |
