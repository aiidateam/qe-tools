#!/usr/bin/env python
from __future__ import print_function
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)

import io
import os
import unittest
import json

from qe_tools import PwInputFile, CpInputFile
from qe_tools.utils.exceptions import InputValidationError

# Folder with input file examples
data_folder = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
# Folder with parsing comparison
reference_folder = os.path.join(data_folder, 'ref')

class CustomTestCase(unittest.TestCase):
    """
    Extension of the unittest TestCase to support also deep almost-equal
    comparisons of dicts
    )
    """

    def assertNestedAlmostEqual(self, expected, actual, *args, **kwargs):
        """
        Check that dict have almost equal content, for float content.
        Works recursively for dicts, tuples, lists, ... Use
        :py:meth:`unittest.TestCase.assertEqual` except for numbers, where
        :py:meth:`unittest.TestCase.assertAlmostEqual` is used.
        Additional parameters are passed only to AlmostEqual
        """
        import numpy
        is_root = not '__trace' in kwargs
        trace = kwargs.pop('__trace', 'ROOT')
        try:
            if isinstance(expected, (int, float, complex)):
                self.assertAlmostEqual(expected, actual, *args, **kwargs)
            elif isinstance(expected, (list, tuple, numpy.ndarray)):
                self.assertEqual(len(expected), len(actual))
                for index in range(len(expected)):
                    v1, v2 = expected[index], actual[index]
                    self.assertNestedAlmostEqual(v1, v2,
                                          __trace=repr(index), *args, **kwargs)
            elif isinstance(expected, dict):
                self.assertEqual(set(expected), set(actual))
                for key in expected:
                    self.assertNestedAlmostEqual(expected[key], actual[key],
                                        __trace=repr(key), *args, **kwargs)
            else:
                self.assertEqual(expected, actual)
        except AssertionError as exc:
            exc.__dict__.setdefault('traces', []).append(trace)
            if is_root:
                trace = ' -> '.join(reversed(exc.traces))
                exc = AssertionError("%s\nTRACE: %s" % (str(exc), trace))
            raise exc

    def assertNestedAlmostEqualOnlyKeysInFirst(self, expected, actual, *args, **kwargs):
        """
        Check that dict have almost equal content, for float content.

        Check only keys in first dictionary (i.e. if it contains less keys,
        only those are checked).
        Works recursively for dicts, tuples, lists, ... Use
        :py:meth:`unittest.TestCase.assertEqual` except for numbers, where
        :py:meth:`unittest.TestCase.assertAlmostEqual` is used.
        Additional parameters are passed only to AlmostEqual
        """
        import numpy
        is_root = not '__trace' in kwargs
        trace = kwargs.pop('__trace', 'ROOT')
        try:
            if isinstance(expected, (int, float, complex)):
                self.assertAlmostEqual(expected, actual, *args, **kwargs)
            elif isinstance(expected, (list, tuple, numpy.ndarray)):
                self.assertEqual(len(expected), len(actual))
                for index in range(len(expected)):
                    v1, v2 = expected[index], actual[index]
                    self.assertNestedAlmostEqual(v1, v2,
                                          __trace=repr(index), *args, **kwargs)
            elif isinstance(expected, dict):
                self.assertEqual(set(expected), set(actual).intersection(set(expected)))
                for key in expected:
                    self.assertNestedAlmostEqualOnlyKeysInFirst(expected[key], actual[key],
                                        __trace=repr(key), *args, **kwargs)
            else:
                self.assertEqual(expected, actual)
        except AssertionError as exc:
            exc.__dict__.setdefault('traces', []).append(trace)
            if is_root:
                trace = ' -> '.join(reversed(exc.traces))
                exc = AssertionError("%s\nTRACE: %s" % (str(exc), trace))
            raise exc


class PwTest(CustomTestCase):
    def singletest(self, label, parser='pw'):
        """
        Run a single test.

        :param label: used to generate the filename (<label>.in)
        :param parser: used to define the parser to use. Possible values:
            ``pw``, ``cp``.
        """
        fname = os.path.join(data_folder, '{}.in'.format(label))
        if not os.path.isfile(fname):
            raise ValueError("File {} not found".format(fname))
        if parser == 'pw':
            ParserClass = PwInputFile
        elif parser == 'cp':
            ParserClass = CpInputFile
        else:
            raise ValueError("Invalid valude for 'parser': '{}'".format(parser))

        in_fname = ParserClass(fname)
        structure = in_fname.get_structure_from_qeinput()

        # Check opening as file-object
        with open(fname) as f:
            in_fobj = ParserClass(f)
        self.assertNestedAlmostEqual(in_fname.atomic_positions, in_fobj.atomic_positions)
        self.assertNestedAlmostEqual(in_fname.atomic_species, in_fobj.atomic_species)
        self.assertNestedAlmostEqual(in_fname.cell_parameters, in_fobj.cell_parameters)
        self.assertNestedAlmostEqual(in_fname.k_points, in_fobj.k_points)
        self.assertNestedAlmostEqual(in_fname.namelists, in_fobj.namelists)
        self.assertNestedAlmostEqual(structure,
            in_fobj.get_structure_from_qeinput())

        # Check opening from string with file content
        # Open in binary mode so I get also '\r\n' from Windows and I check
        # that the parser properly copes with them
        with open(fname, 'rb') as f:
            # I decode for python3, internally I want a string not bytes
            # I assume it's UTF-8
            content = f.read().decode('utf-8')
            in_string = ParserClass(content)
        self.assertNestedAlmostEqual(in_string.atomic_positions, in_fobj.atomic_positions)
        self.assertNestedAlmostEqual(in_string.atomic_species, in_fobj.atomic_species)
        self.assertNestedAlmostEqual(in_string.cell_parameters, in_fobj.cell_parameters)
        self.assertNestedAlmostEqual(in_string.k_points, in_fobj.k_points)
        self.assertNestedAlmostEqual(in_string.namelists, in_fobj.namelists)
        self.assertNestedAlmostEqual(in_string.get_structure_from_qeinput(),
            in_fobj.get_structure_from_qeinput())

        result = {
            # Raw, from input
            "atomic_positions": in_fname.atomic_positions,
            # Raw, from input
            "atomic_species": in_fname.atomic_species,
            # Raw, from input can be None
            "cell_parameters": in_fname.cell_parameters,
            "namelists": in_fname.namelists,
            # Parsed, always angstrom and Cartesian
            "positions_angstrom": structure['positions'],
            # Parsed, always a 3x3 matrix
            "cell": structure['cell'],
        }
        if parser != 'cp':
            result["k_points"] = in_fname.k_points

        ref_fname = os.path.join(reference_folder, '{}.json'.format(label))
        try:
            with open(ref_fname) as f:
                ref = json.load(f)
        except Exception:
            print("What I parsed (to be used in a test reference):")
            print_test_comparison(label=label, parser=parser, write=False)
            raise

        # Check only things in the first dictionary (that therefore must be the
        # test json). In this way I can remove things from the test json
        # if I don't want to test them.
        self.assertNestedAlmostEqualOnlyKeysInFirst(ref, result)

    ############################################################################
    ## Here start the tests
    ############################################################################
    def test_example_ibrav0(self):
        self.singletest(label='example_ibrav0')

    def test_example_ibrav0_uppercaseunits(self):
        self.singletest(label='example_ibrav0_uppercaseunits')

    def test_example_ibrav0_multiplespecies(self):
        self.singletest(label='example_ibrav0_multiplespecies')

    def test_example_ibrav0_alat(self):
        self.singletest(label='example_ibrav0_alat')

    def test_example_ibrav0_crystal(self):
        self.singletest(label='example_ibrav0_crystal')

    def test_example_ibrav0_bohr(self):
        self.singletest(label='example_ibrav0_bohr')

    def test_example_ibrav0_nounits_cp(self):
        # Deprecated behavior
        with self.assertRaises(InputValidationError):
            self.singletest(label='example_ibrav0_nounits_cp', parser='cp')

    def test_example_ibrav0_nounits_pw(self):
        # Deprecated behavior
        with self.assertRaises(InputValidationError):
            self.singletest(label='example_ibrav0_nounits_pw', parser='pw')

    def test_example_ibrav0_ifpos(self):
        self.singletest(label='example_ibrav0_ifpos')

    def test_example_mixture_windows_linux_newlines(self):
        self.singletest(label='example_mixture_windows_linux_newlines')

    def test_lattice_ibrav0_cell_parameters(self):
        self.singletest(label='lattice_ibrav0_cell_parameters')

    def test_lattice_ibrav0_cell_parameters_a(self):
        self.singletest(label='lattice_ibrav0_cell_parameters_a')

    def test_lattice_ibrav0_cell_parameters_ang(self):
        self.singletest(label='lattice_ibrav0_cell_parameters_ang')

    def test_lattice_ibrav0_cell_parameters_celldm(self):
        self.singletest(label='lattice_ibrav0_cell_parameters_celldm')

    def test_lattice_ibrav1(self):
        self.singletest(label='lattice_ibrav1')

    def test_lattice_ibrav1_kauto(self):
        self.singletest(label='lattice_ibrav1_kauto')

    def test_lattice_ibrav10(self):
        self.singletest(label='lattice_ibrav10')

    def test_lattice_ibrav11(self):
        self.singletest(label='lattice_ibrav11')

    def test_lattice_ibrav12(self):
        self.singletest(label='lattice_ibrav12')

    def test_lattice_ibrav13(self):
        self.singletest(label='lattice_ibrav13')

    def test_lattice_ibrav14(self):
        self.singletest(label='lattice_ibrav14')

    def test_lattice_ibrav2(self):
        self.singletest(label='lattice_ibrav2')

    def test_lattice_ibrav3(self):
        self.singletest(label='lattice_ibrav3')

    def test_lattice_ibrav4(self):
        self.singletest(label='lattice_ibrav4')

    def test_lattice_ibrav5(self):
        self.singletest(label='lattice_ibrav5')

    def test_lattice_ibrav6(self):
        self.singletest(label='lattice_ibrav6')

    def test_lattice_ibrav7(self):
        self.singletest(label='lattice_ibrav7')

    def test_lattice_ibrav8(self):
        self.singletest(label='lattice_ibrav8')

    def test_lattice_ibrav9(self):
        self.singletest(label='lattice_ibrav9')

    # The following is for negative ibravs

    def test_lattice_ibrav_12(self):
        self.singletest(label='lattice_ibrav_12')

    def test_lattice_ibrav_3(self):
        self.singletest(label='lattice_ibrav_3')

    def test_lattice_ibrav_5(self):
        self.singletest(label='lattice_ibrav_5')

    def test_no_newline_exponential_time(self):
        """
        This tries to avoid a regression of #15 
        (too slow parsing of specific output)
        """
        import timeout_decorator
        # Should not run in more than 2 seconds 
        # (it should be actually much faster!)
        @timeout_decorator.timeout(2)
        def mytest():
            self.singletest(label='no_newline_exponential_time')
        
        # Run the test
        mytest()

    ##Wyckoff position input (crystal_sg) not supported by this parser
    #def test_lattice_wyckoff_sio2(self):
    #   self.singletest(label='lattice_wyckoff_sio2')


def print_test_comparison(label, parser='pw', write=False):
    """
    Prepare the json to compare the parsing results.

    :param label: used to generate the filename (<label>.in)
    :param parser: used to define the parser to use. Possible values:
        ``pw``, ``cp``.
    """
    fname = os.path.join(data_folder, '{}.in'.format(label))
    if not os.path.isfile(fname):
        raise ValueError("File {} not found".format(fname))
    if parser == 'pw':
        ParserClass = PwInputFile
    elif parser == 'cp':
        ParserClass = CpInputFile
    else:
        raise ValueError("Invalid valude for 'parser': '{}'".format(parser))

    parsed = ParserClass(fname)
    structure = parsed.get_structure_from_qeinput()

    result = {
        # Raw, from input
        "atomic_positions": parsed.atomic_positions,
        # Raw, from input
        "atomic_species": parsed.atomic_species,
        # Raw, from input can be None
        "cell_parameters": parsed.cell_parameters,
        "namelists": parsed.namelists,
        # Parsed, always angstrom and Cartesian
        "positions_angstrom": structure['positions'],
        # Parsed, always a 3x3 matrix
        "cell": structure['cell'],
    }

    if parser != 'cp':
        result["k_points"] = parsed.k_points

    if write:
        ref_fname = os.path.join(reference_folder, '{}.json'.format(label))
        with io.open(ref_fname, 'w', encoding="utf-8") as f:
            f.write(str(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False)))
            print("File '{}' written.".format(ref_fname))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))




if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == '--write-ref':
            try:
                label = sys.argv[2]
            except IndexError:
                print("Pass as filename (and optionally pw or cp to specify a parser, default: pw)", file=sys.stderr)
                sys.exit(1)
            try:
                parser = sys.argv[3]
            except IndexError:
                parser = 'pw'
            print_test_comparison(label, parser=parser, write=True)
        else:
            print("If you pass additional parameters, they must be --write-ref <label> [pw/cp]", file=sys.stderr)

    else:
        unittest.main()


