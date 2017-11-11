import os
import unittest

from qe_tools import PwInputFile, CpInputFile

data_folder = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')

class PwTest(unittest.TestCase):
    def test_pw_ibrav0_angstrom_1(self):
        folder = os.path.join(data_folder, 'pw_ibrav0_angstrom_1')
        pwin = PwInputFile(os.path.join(folder, 'qe.in'))


if __name__ == "__main__":
    unittest.main()
