import pytest

from numpy import ndarray


@pytest.fixture()
def json_serializer():
    """Fixture for making dictionaries JSON serializable.

    Supported conversions:

        * numpy.ndarray; converted into list with `.tolist()`.
    """

    def factory(dictionary: dict):
        json_dict = {}

        for key, value in dictionary.items():
            if isinstance(value, dict):
                json_dict[key] = {k: factory(v) for k, v in value.items()}
            elif isinstance(value, ndarray):
                json_dict[key] = value.tolist()
            else:
                json_dict[key] = value

        return json_dict

    return factory
