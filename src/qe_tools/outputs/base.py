# -*- coding: utf-8 -*-
"""Base parser for the outputs of Quantum ESPRESSO."""

import abc


class BaseOutput(abc.ABC):
    """
    Abstract class for the outputs of Quantum ESPRESSO.
    """

    def __init__(self, outputs: dict | None = None, executable: str | None = None):
        self.outputs = outputs
        self.executable = executable

    @classmethod
    @abc.abstractmethod
    def from_dir(cls, directory: str):
        pass
