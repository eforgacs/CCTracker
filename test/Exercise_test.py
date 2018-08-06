import sys
sys.path.append("..") # Adds higher directory to python modules path.

import WorkoutEngine as we
import unittest


class TestExercise(unittest.TestCase):

    def test_name_good(self):
        exercise = we.Exercise(we.ExerciseType.proposed, 10, "3.1.0.1")
        self.assertEqual(exercise.get_code(), "3.1.0.1")

    def test_expected_reps_good(self):
        exercise = we.Exercise(we.ExerciseType.proposed, 1, "3.1.0.1")
        self.assertEqual(exercise.get_expected_reps(), 1)
        exercise = we.Exercise(we.ExerciseType.proposed, 10, "3.1.0.1")
        self.assertEqual(exercise.get_expected_reps(), 10)
        exercise = we.Exercise(we.ExerciseType.proposed, 20, "3.1.0.1")
        self.assertEqual(exercise.get_expected_reps(), 20)
        exercise = we.Exercise(we.ExerciseType.proposed, 100, "3.1.0.1")
        self.assertEqual(exercise.get_expected_reps(), 100)

    def test_type(self):        
        exercise = we.Exercise(we.ExerciseType.proposed, 10, "3.1.0.1")
        self.assertEqual(exercise.get_type(), we.ExerciseType.proposed)
        exercise = we.Exercise(we.ExerciseType.warmup, 10, "3.1.0.1")
        self.assertEqual(exercise.get_type(), we.ExerciseType.warmup)
        exercise = we.Exercise(we.ExerciseType.workset, 10, "3.1.0.1")
        self.assertEqual(exercise.get_type(), we.ExerciseType.workset)

    def test_reps_done(self):
        exercise = we.Exercise(we.ExerciseType.workset, 10, "3.1.0.1")
        self.assertEqual(exercise.get_actual_reps(), 0)
        exercise.reps_done(5)
        self.assertEqual(exercise.get_actual_reps(), 5)
        exercise.reps_done(10)
        self.assertEqual(exercise.get_actual_reps(), 10)
        exercise.reps_done(11)
        self.assertEqual(exercise.get_actual_reps(), 11)

    def test_expected_reps(self):
        exercise = we.Exercise(we.ExerciseType.workset, 10, "3.1.0.1")
        self.assertEqual(exercise.get_expected_reps(), 10)      

suite = unittest.TestLoader().loadTestsFromTestCase(TestExercise)
unittest.TextTestRunner(verbosity=2).run(suite)
