"""Generic file-parsing base class."""

from __future__ import annotations

import abc
from io import TextIOBase
from pathlib import Path
from typing import TextIO


class BaseOutputFileParser(abc.ABC):
    """
    Abstract class for parsing a single output file.
    A computation with multiple output files should therefore define multiple parsers.
    """

    @staticmethod
    @abc.abstractmethod
    def parse(content: str):
        """Parse the file content and return a dictionary of parsed data."""

    @classmethod
    def parse_from_file(cls, file: str | Path | TextIO):
        """
        Helper function to generate a BaseOutputFileParser object
        from a file instead of its string.
        """
        if isinstance(file, (str, Path)):
            with Path(file).open("r") as handle:
                content = handle.read()
        elif isinstance(file, TextIOBase):
            content = file.read()
        else:
            raise TypeError(f"Unsupported type: {type(file)}")

        return cls.parse(content)
