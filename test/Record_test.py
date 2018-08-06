import sys
sys.path.append("..") # Adds higher directory to python modules path.

import WorkoutEngine as we
import unittest

import os.path


class TestExercise(unittest.TestCase):

    #record does not exist, new record will be created
    def test_new_record(self):
        if os.path.isfile("JohnDoe"):
            os.remove("JohnDoe")
        self.assertFalse(os.path.isfile("JohnDoe"))
        record = we.Record("JohnDoe")
        self.assertTrue(os.path.isfile("JohnDoe"))
        record_file = open("JohnDoe", 'r')
        record_line = record_file.readline()
        record_file.close()
        self.assertTrue('"squats": []' in record_line)
        self.assertTrue('"bridges": []' in record_line)
        self.assertTrue('"pushups": []' in record_line)
        self.assertTrue('"pullups": []' in record_line)
        self.assertTrue('"leg_raises": []' in record_line)
        self.assertTrue('"handstand_pushups": []' in record_line)
        if os.path.isfile("JohnDoe"):
            os.remove("JohnDoe")

    def test_preexisting_record(self):
        #bare, pre-existing record
        self.assertTrue(os.path.isfile("JaneDoe"))
        record = we.Record("JaneDoe")
        self.assertEqual(record.last_workout(we.WorkoutType.pushups), None)
        self.assertEqual(record.last_workout(we.WorkoutType.leg_raises), None)
        self.assertEqual(record.last_workout(we.WorkoutType.pullups), None)
        self.assertEqual(record.last_workout(we.WorkoutType.squats), None)
        self.assertEqual(record.last_workout(we.WorkoutType.bridges), None)
        self.assertEqual(record.last_workout(we.WorkoutType.handstand_pushups), None)

        #not bare, pre-existing record
        self.assertTrue(os.path.isfile("JaneDoe"))
        record = we.Record("JaneDoe")
        self.assertEqual(record.last_workout(we.WorkoutType.pushups), None)
        self.assertEqual(record.last_workout(we.WorkoutType.leg_raises), None)
        self.assertEqual(record.last_workout(we.WorkoutType.pullups), None)
        self.assertEqual(record.last_workout(we.WorkoutType.squats), None)
        self.assertEqual(record.last_workout(we.WorkoutType.bridges), None)
        self.assertEqual(record.last_workout(we.WorkoutType.handstand_pushups), None)
        
    def test_record_empty_record(self):
        #test record() by creating a record,
        #calling record(), then ensure file is correct
        if os.path.isfile("JackSprat"):
            os.remove("JackSprat")
        record = we.Record("JackSprat")
        record.record()
        self.assertTrue(os.path.isfile("JackSprat"))
        record_file = open("JackSprat", 'r')
        record_line = record_file.readline()
        record_file.close()
        self.assertTrue('"squats": []' in record_line)
        self.assertTrue('"bridges": []' in record_line)
        self.assertTrue('"pushups": []' in record_line)
        self.assertTrue('"pullups": []' in record_line)
        self.assertTrue('"leg_raises": []' in record_line)
        self.assertTrue('"handstand_pushups": []' in record_line)
        if os.path.isfile("JackSprat"):
            os.remove("JackSprat")

    def test_record_workout_bad(self):
        # no worksets
        exercises = []
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.3.0.2"))
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.4.0.2"))
        workout1 = we.Workout(we.WorkoutType.pushups)
        for exercise in exercises:
            workout1.add_exercise(exercise)
        record = we.Record("PussyFoot")
        record.record_workout(workout1)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        self.assertEqual(None, last_workout)
        last_workout = record.last_workout(we.WorkoutType.leg_raises)
        self.assertEqual(None, last_workout)
        last_workout = record.last_workout(we.WorkoutType.squats)
        self.assertEqual(None, last_workout)
        last_workout = record.last_workout(we.WorkoutType.pullups)
        self.assertEqual(None, last_workout)
        last_workout = record.last_workout(we.WorkoutType.bridges)
        self.assertEqual(None, last_workout)
        last_workout = record.last_workout(we.WorkoutType.handstand_pushups)
        self.assertEqual(None, last_workout)
        # no reps completed
        exercises = []
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.3.0.2"))
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.4.0.2"))
        exercises.append(we.Exercise(we.ExerciseType.workset, 5, "1.5.0.1"))
        workout1 = we.Workout(we.WorkoutType.pushups)
        for exercise in exercises:
            workout1.add_exercise(exercise)
        record = we.Record("SlimJim")
        record.record_workout(workout1)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        self.assertEqual(None, last_workout)
        files = ["SlimJim", "PussyFoot"]
        for file in files:
            if os.path.isfile(file):
                #os.remove(file)
                pass

    def test_record_workout(self):
        # 1 workset with 1 rep completed
        exercises = []
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.3.0.2"))
        exercises.append(we.Exercise(we.ExerciseType.warmup, 15, "1.4.0.2"))
        exercises.append(we.Exercise(we.ExerciseType.workset, 5, "1.5.0.1"))
        workout1 = we.Workout(we.WorkoutType.pushups)
        for exercise in exercises:
            exercise.reps_done(1)
            workout1.add_exercise(exercise)
        record = we.Record("SlimJim")
        record.record_workout(workout1)
        record.record()
        last_workout = record.last_workout(we.WorkoutType.pushups)
        self.assertTrue(not None == last_workout)
        self.assertEqual(1, len(last_workout.get_exercises()))
        
        # 2 worksets, 1 with reps completed & 1 without
        exercise1 = we.Exercise(we.ExerciseType.workset, 10, "1.5.0.2")
        exercise2 = we.Exercise(we.ExerciseType.workset, 20, "1.5.0.3")

        # exercise1 has no reps, exercise2 has no reps
        exercise1.reps_done(0)
        exercise2.reps_done(0)
        workout = we.Workout(we.WorkoutType.pushups)
        workout.add_exercise(exercise1)
        workout.add_exercise(exercise2)
        record = we.Record("N1N2")
        record.record_workout(workout)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        self.assertTrue(None == last_workout)

        # exercise1 has reps, exercise2 has no reps
        exercise1.reps_done(2)
        exercise2.reps_done(0)
        workout = we.Workout(we.WorkoutType.pushups)
        workout.add_exercise(exercise1)
        workout.add_exercise(exercise2)
        record = we.Record("H1N2")
        record.record_workout(workout)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        exercises = last_workout.get_exercises()
        self.assertEqual(1, len(exercises))
        self.assertEqual(2, exercises[0].get_actual_reps())
        

        # exercise1 has no reps, exercise2 has reps
        exercise1.reps_done(0)
        exercise2.reps_done(5)
        workout = we.Workout(we.WorkoutType.pushups)
        workout.add_exercise(exercise1)
        workout.add_exercise(exercise2)
        record = we.Record("N1H2")
        record.record_workout(workout)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        exercises = last_workout.get_exercises()
        self.assertEqual(1, len(exercises))
        self.assertEqual(5, exercises[0].get_actual_reps())

        # exercise1 has reps, exercise2 has reps
        exercise1.reps_done(3)
        exercise2.reps_done(10)
        workout = we.Workout(we.WorkoutType.pushups)
        workout.add_exercise(exercise1)
        workout.add_exercise(exercise2)
        record = we.Record("H1H2")
        record.record_workout(workout)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        exercises = last_workout.get_exercises()
        self.assertEqual(2, len(exercises))
        self.assertEqual(3, exercises[0].get_actual_reps())
        self.assertEqual(10, exercises[1].get_actual_reps())
        record.record()
                        


        # record has 2 different kinds of workouts, workout should only return last workout
        exercise1.reps_done(2)
        exercise2.reps_done(2)
        workout1 = we.Workout(we.WorkoutType.pullups)
        workout1.add_exercise(exercise1)
        workout1.add_exercise(exercise2)
        record.record_workout(workout1)
        last_workout = record.last_workout(we.WorkoutType.pushups)
        exercises = last_workout.get_exercises()
        self.assertEqual(2, len(exercises))
        self.assertEqual(3, exercises[0].get_actual_reps())
        self.assertEqual(10, exercises[1].get_actual_reps())
        record.record()
        files = ["SlimJim", "N1N2", "H1N2", "N1H2", "H1H2"]
        for file in files:
            if os.path.isfile(file):
                os.remove(file)
                pass

#    def __init__(self, name):
#        print("RECORD INITIALIZED")
#    def last_workout(self, workout_type):
#        print("LAST WORKOUT WAS:")
#    def record_workout(self, workout):
#        print("WORKOUT RECORDED")
#    def record(self):


suite = unittest.TestLoader().loadTestsFromTestCase(TestExercise)
unittest.TextTestRunner(verbosity=2).run(suite)
