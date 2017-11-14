from __future__ import print_function
import os
import unittest

from qe_tools import PwInputFile, CpInputFile

data_folder = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')


class PwTest(unittest.TestCase):
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

        # Check opening as file-object
        with open(fname) as f:
            in_fobj = ParserClass(f)
        self.assertAlmostEqual(in_fname.atomic_positions, in_fobj.atomic_positions)
        self.assertAlmostEqual(in_fname.atomic_species, in_fobj.atomic_species)
        self.assertAlmostEqual(in_fname.cell_parameters, in_fobj.cell_parameters)
        self.assertAlmostEqual(in_fname.k_points, in_fobj.k_points)
        self.assertAlmostEqual(in_fname.namelists, in_fobj.namelists)

        # Check opening from string with file content
        with open(fname) as f:
            content = f.read()
            in_string = ParserClass(content)
        self.assertAlmostEqual(in_string.atomic_positions, in_fobj.atomic_positions)
        self.assertAlmostEqual(in_string.atomic_species, in_fobj.atomic_species)
        self.assertAlmostEqual(in_string.cell_parameters, in_fobj.cell_parameters)
        self.assertAlmostEqual(in_string.k_points, in_fobj.k_points)
        self.assertAlmostEqual(in_string.namelists, in_fobj.namelists)



    def test_example_ibrav0(self):
        self.singletest(label='example_ibrav0')


if __name__ == "__main__":
    unittest.main()
