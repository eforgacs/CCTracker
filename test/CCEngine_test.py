import sys
sys.path.append("..") # Adds higher directory to python modules path.

import WorkoutEngine as we
import unittest


class TestExercise(unittest.TestCase):
    def test_level_good(self):
        pass

suite = unittest.TestLoader().loadTestsFromTestCase(TestExercise)
unittest.TextTestRunner(verbosity=2).run(suite)

