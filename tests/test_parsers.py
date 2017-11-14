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
        with open(fname) as f:
            in_fobj = ParserClass(f)
        with open(fname) as f:
            content = f.read()
            in_string = ParserClass(content)

        # TODO: check they are the same
        # TODO: check the following

        #print(pwin.atomic_positions)
        #print(pwin.atomic_species)
        #print(pwin.cell_parameters)
        #print(pwin.k_points)
        #print(pwin.namelists)


    def test_example_ibrav0(self):
        self.singletest(label='example_ibrav0')


if __name__ == "__main__":
    unittest.main()
