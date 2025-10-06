"""
Helper module for managing the QuantumESPRESSO version.
"""

from __future__ import annotations

from functools import total_ordering

from packaging.version import Version

__all__ = ("parse_version",)


@total_ordering
class _LatestVersionImpl:
    """
    Implements a 'latest' version that compares as newer to any
    packaging.version._BaseVersion object.

    The object is implemented as a singleton, meaning it can only be
    instantiated once.
    """

    __instance_count = 0

    def __init__(self):
        super().__init__()
        if self.__instance_count > 0:
            raise TypeError("Cannot instantiate the singleton more than once.")
        # Needs to be set at type(self) explicitly, otherwise we just
        # create an instance attribute.
        type(self).__instance_count += 1  # noqa: SLF001

    def __gt__(self, other):
        if self is other:
            return False
        return True


_LATEST_VERSION = _LatestVersionImpl()


def parse_version(
    qe_version: str | _LatestVersionImpl | Version | None = None,
) -> _LatestVersionImpl | Version:
    """Parse the QE version string to a comparable object.

    Parses the QE version string into a packaging.version.Version
    object. If no version is given, a singleton object representing the
    latest version is returned instead.
    The function is idempotent, i.e. applying it to an already-parsed
    version returns the same object.

    Parameters
    ----------
    qe_version :
        A string representing the QuantumESPRESSO version. Must comply
        with the PEP440 versioning scheme. Valid versions are e.g.
        '6.5', '6.4.1', '6.4rc2'.
    """
    if isinstance(qe_version, (_LatestVersionImpl, Version)):
        return qe_version
    if qe_version is None:
        return _LATEST_VERSION
    return Version(qe_version)


def convert_qe_time_to_sec(timestr):
    """Given the walltime string of Quantum Espresso, converts it in a number of seconds (float)."""
    rest = timestr.strip()

    if "d" in rest:
        days, rest = rest.split("d")
    else:
        days = "0"

    if "h" in rest:
        hours, rest = rest.split("h")
    else:
        hours = "0"

    if "m" in rest:
        minutes, rest = rest.split("m")
    else:
        minutes = "0"

    if "s" in rest:
        seconds, rest = rest.split("s")
    else:
        seconds = "0."

    if rest.strip():
        raise ValueError(
            f"Something remained at the end of the string '{timestr}': '{rest}'"
        )

    return (
        float(seconds)
        + float(minutes) * 60.0
        + float(hours) * 3600.0
        + float(days) * 86400.0
    )
