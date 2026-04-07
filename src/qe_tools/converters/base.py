import typing

from glom import glom


class BaseConverter:
    conversion_mapping: typing.ClassVar[dict[str, typing.Any]]

    @classmethod
    def convert(cls, output: str, base_output: dict):
        output_converter, output_spec = cls.conversion_mapping[output]

        arguments = glom(base_output, output_spec)

        if isinstance(arguments, dict):
            return output_converter(**arguments)
        if isinstance(arguments, list):
            return output_converter(*arguments)
        else:
            return output_converter(arguments)
