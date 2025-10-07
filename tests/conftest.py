import pytest

from numpy import ndarray


@pytest.fixture()
def robust_data_regression_check(data_regression, json_serializer):
    def factory(input):
        return data_regression.check(json_serializer(input))

    return factory


@pytest.fixture()
def json_serializer():
    """Fixture for making dictionaries JSON serializable in a robust manner for testing.

    Supported conversions:

        * numpy.ndarray; converted into list with `.tolist()`.
        * float/int: convert into float rounded to 5 digits.
    """

    def factory(item):
        if isinstance(item, (str, bool)):
            return item
        if isinstance(item, (list, tuple)):
            return [factory(el) for el in item]
        if isinstance(item, dict):
            return {k: factory(v) for k, v in item.items()}
        if isinstance(item, (float, int)):
            return round(float(item), 5)
        if isinstance(item, ndarray):
            return factory(item.tolist())
        raise TypeError(f"Type: '{type(item)}' not supported!")

    return factory
