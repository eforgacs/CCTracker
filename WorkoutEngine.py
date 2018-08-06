'''start program
load account
	app reads history
	program determines next workout
		option printout
			all paths reported
			program ends
		option interactive
			path is followed dynamically
			?request to save workout
			program ends
class Menu (defer)
class Account

TypeOfWorkout
	invalid
	pushups
	pullups
	squats
	leg_raises

CCEngine
	Workout nextWorkout(TypeOfWorkout, Record)

Record
	__init__(,name)
	Workout lastWorkout(TypeOfWorkout)
	recordWorkout(Workout)

Workout
	(all paths - flow chart)
        print_full_workout
	did_last_step() returns T/F
	Exercise next_step(reps=0)
	?? work_done ??
Exercise
        __init__(self, ExerciseType, Reps, Level)
        get_level()
        get_reps()
        get_type()
        

	'''


from enum import Enum
from copy import deepcopy
from time import gmtime, strftime

import json, os        

class ExerciseType(Enum):
    warmup = 1
    workset = 2
    proposed = 3

class Exercise:
    def __init__(self, exercise_type, expected_reps, exercise_code):
        self.exercise_type = exercise_type
        self.expected_reps = expected_reps
        self.code = exercise_code
        self.actual_reps = 0

    def get_code(self):
        return self.code

    def reps_done(self, reps):
        self.actual_reps = reps
    
    def get_expected_reps(self):
        return self.expected_reps

    def get_actual_reps(self):
        return self.actual_reps
    
    def get_type(self):
        return self.exercise_type

    def as_dict(self):
        the_dict = dict()
        the_dict["code"] = self.code
        the_dict["expected_reps"] = self.expected_reps
        the_dict["actual_reps"] = self.actual_reps

class WorkoutType(Enum):
    pushups = 1
    leg_raises = 2
    pullups = 3
    squats = 4
    bridges = 5
    handstand_pushups = 6
       
class Workout(json.JSONEncoder):
    def __init__(self, workout_type):
        self.workout_type = workout_type
        self.exercises = []
        self.step = 0
#        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        
    def add_exercise(self, exercise):
        self.exercises.append(deepcopy(exercise))
        
    def did_final_step(self):
        number_of_steps = len(self.exercises)        
        return number_of_steps == self.step

    # returns None if index out of bounds
    def next_step(self):
        self.step = self.step + 1
        if (len(self.exercises) < self.step):
            return None
        return self.exercises[self.step - 1]

    def full_workout(self):
        
        full_workout = ""
        full_workout += "WORKOUT TYPE:" + str(self.get_type()) + "\n\n"
        for exercise in self.exercises:
            full_workout += "EXERCISE TYPE:" + str(exercise.get_type()) + "\n"
            full_workout += "\n"
            full_workout += "EXERCISE:" + str(exercise.get_code()) + "\n"
            full_workout += "REPS:" + str(exercise.get_expected_reps()) + "\n"
            full_workout += "\n"
        return full_workout

    # used by ccTracker and record
    def get_exercises(self):
        return self.exercises
    
    def get_type(self):
        return self.workout_type

#    def get_time(self):
#        return self.time
    
#    def set_time(self):
#        self.time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def as_dict(self):
        the_dict = dict()
#        the_dict[time] = self.time
        the_dict["exercises"] = []
        for exercise in self.exercises:
            the_dict["exercises"].append(exercise.as_dict())

class Record():
    def __init__(self, name):
        self.name = name
        new_record = {}
        emptyWorkouts = []
        
        new_record["pushups"] = []
        new_record["leg_raises"] = []
        new_record["pullups"] = []
        new_record["squats"] = []
        new_record["bridges"] = []
        new_record["handstand_pushups"] = []

        with open(name, 'w') as outfile:
            json.dump(new_record, outfile)
        outfile.close()

        record_file = open(name, 'r')
        self.workout_history = json.load(record_file)
        #print(self.workout_history)

    def last_workout(self, workout_type):
        ''' returns None if no viable workout '''
        #print(self.workout_history)
        workout_list = self.workout_history[workout_type.name]
        if not workout_list:
            return None
        return workout_list[-1]

    def get_workout_history(self):
        return self.workout_history
    
    def record_workout(self, workout):
        ''' only record worksets with a minimum of 1 rep completed '''
        expected_exercise_type = ExerciseType.workset
        exercises = workout.get_exercises()
        workout_type = workout.get_type()
        temp_workout = Workout(workout_type)
        # add viable exercise to temp_workout
        for exercise in exercises:
            if expected_exercise_type == exercise.get_type():
                if exercise.get_actual_reps() > 0:
                    temp_workout.add_exercise(exercise)
        if len(temp_workout.get_exercises()) > 0:
            workout_list = self.workout_history[workout_type.name]
            workout_list.append(temp_workout)   
        
    def record(self):
        #print ("^^^^")
        #print (self.as_dict())
        #print ("^^^^")
        with open(self.name, 'w') as outfile:
            json.dump(self.as_dict(), outfile)
        outfile.close()

    def as_dict(self):
        the_dict = dict()
        workout_keys = self.workout_history.keys()
        #print(workout_keys)
        for workout_key in workout_keys:
            the_dict[workout_key] = []
            the_workouts = self.workout_history[workout_key]
            for the_workout in the_workouts:
                the_dict[workout_key].append(the_workout.as_dict())
        return the_dict
        #print(json.dump(the_dict))
        

class CCEngine():
    def next_workout(self, workout_type, record):
        record.last_workout(workout_type)
        print("GETTING NEXT WORKOUT...", workout_type)

def to_json(obj):
    json_str = ""
    if isinstance(obj, Record):
        json_str += "{"
        is_first = True
        history = obj.get_workout_history()
        for workout_list in history:
            if not is_first:
                json_str += ","
            else:
                is_first = False
            json_str += '"'
            json_str += Workout
                
