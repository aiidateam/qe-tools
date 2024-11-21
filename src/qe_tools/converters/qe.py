# -*- coding: utf-8 -*-
"""Tools for converting Quantum ESPRESSO outputs to Python data types."""


def convert_qe_time_to_sec(timestr):
    """Given the walltime string of Quantum Espresso, converts it in a number of seconds (float)."""
    rest = timestr.strip()

    if 'd' in rest:
        days, rest = rest.split('d')
    else:
        days = '0'

    if 'h' in rest:
        hours, rest = rest.split('h')
    else:
        hours = '0'

    if 'm' in rest:
        minutes, rest = rest.split('m')
    else:
        minutes = '0'

    if 's' in rest:
        seconds, rest = rest.split('s')
    else:
        seconds = '0.'

    if rest.strip():
        raise ValueError(f"Something remained at the end of the string '{timestr}': '{rest}'")

    num_seconds = float(seconds) + float(minutes) * 60.0 + float(hours) * 3600.0 + float(days) * 86400.0

    return num_seconds
