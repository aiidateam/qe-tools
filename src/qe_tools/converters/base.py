import typing

from glom import glom


class BaseConverter:
    @classmethod
    def get_conversion_mapping(cls) -> dict[str, typing.Any]:
        """Return the conversion mapping for this converter.

        Subclasses override this to build their mapping lazily. Imports from optional
        dependencies belong inside this method so that simply importing the converter
        class does not pull them in.
        """
        raise NotImplementedError

    @classmethod
    def convert(cls, output: str, base_output: dict):
        output_converter, output_spec = cls.get_conversion_mapping()[output]

        arguments = glom(base_output, output_spec)

        if isinstance(arguments, dict):
            return output_converter(**arguments)
        if isinstance(arguments, list):
            return output_converter(*arguments)
        else:
            return output_converter(arguments)
