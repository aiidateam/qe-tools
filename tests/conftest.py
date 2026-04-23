"""Project-wide pytest fixtures & hooks.

Load the `dough.testing` plugin explicitly so `json_serializer` and
`robust_data_regression_check` are available to the test suite.
"""

pytest_plugins = ["dough.testing.plugin"]
