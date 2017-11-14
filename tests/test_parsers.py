from __future__ import print_function
import os
import unittest

from qe_tools import PwInputFile, CpInputFile

data_folder = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')

class PwTest(unittest.TestCase):
    def test_example_ibrav0(self):
        pwin = PwInputFile(os.path.join(data_folder, 'example-ibrav0.in'))
        #print(pwin.atomic_positions)
        #print(pwin.atomic_species)
        #print(pwin.cell_parameters)
        #print(pwin.k_points)
        #print(pwin.namelists)


if __name__ == "__main__":
    unittest.main()
