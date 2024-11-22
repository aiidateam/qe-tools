# -*- coding: utf-8 -*-
"""Base parser for the outputs of Quantum ESPRESSO."""

from __future__ import annotations

import abc


class BaseOutput(abc.ABC):
    """
    Abstract class for the outputs of Quantum ESPRESSO.
    """

    def __init__(self, outputs: dict | None = None):
        self.outputs = outputs

    @classmethod
    @abc.abstractmethod
    def from_dir(cls, directory: str):
        pass
