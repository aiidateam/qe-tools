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
