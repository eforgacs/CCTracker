import sys
sys.path.append("..") # Adds higher directory to python modules path.

import WorkoutEngine as we
import unittest

class TestWorkout(unittest.TestCase):

    def test_final_step(self):
        # Empty workout
        workout = we.Workout(we.WorkoutType.pushups)
        self.assertTrue(workout.did_final_step())

        # Workout with 1 exercise
        exercise = we.Exercise(we.ExerciseType.warmup, 25, 1.2)
        workout.add_exercise(exercise)
        self.assertFalse(workout.did_final_step())

    def test_next_step_good(self):
        # Empty workout
        workout = we.Workout(we.WorkoutType.pushups)
        exercise = workout.next_step()
        self.assertEqual(exercise, None)

        # Workout with 1 exercise
        workout = we.Workout(we.WorkoutType.pushups)
        exercise = we.Exercise(we.ExerciseType.workset, 10, 3.1)
        workout.add_exercise(exercise)
        
        next_exercise = workout.next_step()
        self.assertEqual(next_exercise.get_expected_reps(), 10)

        bad_exercise = workout.next_step()
        self.assertEqual(bad_exercise, None)

        # Workout with 2 exercises
        workout = we.Workout(we.WorkoutType.pullups)
        exercise = we.Exercise(we.ExerciseType.workset, 10, 3.1)
        workout.add_exercise(exercise)
        exercise = we.Exercise(we.ExerciseType.workset, 10, 3.1)
        workout.add_exercise(exercise)
        
        next_exercise = workout.next_step()
        self.assertEqual(next_exercise.get_expected_reps(), 10)
        next_exercise = workout.next_step()
        self.assertEqual(next_exercise.get_expected_reps(), 10)

        bad_exercise = workout.next_step()
        self.assertEqual(bad_exercise, None)

    def test_multiple_exercises_final_step(self):
        # Workout with 2 exercises, assert final steps
        workout = we.Workout(we.WorkoutType.pushups)
        exercise = we.Exercise(we.ExerciseType.warmup, 10, 3.1)
        workout.add_exercise(exercise)
        exercise = we.Exercise(we.ExerciseType.workset, 8, 4.1)
        workout.add_exercise(exercise)
        
        next_exercise = workout.next_step()
        self.assertFalse(workout.did_final_step())

        next_exercise = workout.next_step()
        self.assertTrue(workout.did_final_step())
        
    def test_print_workout(self):
        # empty workout
        workout = we.Workout(we.WorkoutType.pushups)
        self.assertEqual(workout.full_workout(), "WORKOUT TYPE:WorkoutType.pushups\n\n")

        exercise = we.Exercise(we.ExerciseType.proposed, 33, 6.1)
        workout.add_exercise(exercise)
        lines = []
        lines.append("WORKOUT TYPE:WorkoutType.pushups\n\n")
        lines.append("EXERCISE TYPE:ExerciseType.proposed\n\n")
        lines.append("EXERCISE:6.1\n")
        lines.append("REPS:33\n\n")
        full_workout = ""
        for line in lines:
            full_workout += line
        self.assertEqual(workout.full_workout(), full_workout)

    def test_get_exercises(self):
        workout = we.Workout(we.WorkoutType.pushups)

        # test empty workout
        self.assertEqual(len(workout.get_exercises()), 0)

        # test workout w/ 1 exercise
        exercise = we.Exercise(we.ExerciseType.warmup, 10, 3.2)
        workout.add_exercise(exercise)
        exercises = workout.get_exercises()
        self.assertEqual(len(exercises), 1)

        workout.add_exercise(exercise)
        exercises = workout.get_exercises()
        self.assertEqual(len(exercises), 2)
 
    def test_get_type(self):
        workout_types = []
        workout_types.append(we.WorkoutType.bridges)
        workout_types.append(we.WorkoutType.handstand_pushups)
        workout_types.append(we.WorkoutType.leg_raises)
        workout_types.append(we.WorkoutType.pullups)
        workout_types.append(we.WorkoutType.pushups)
        workout_types.append(we.WorkoutType.squats)

        for workout_type in workout_types:
            workout = we.Workout(workout_type)
            self.assertEqual(workout_type, workout.get_type())

suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkout)
unittest.TextTestRunner(verbosity=2).run(suite)

