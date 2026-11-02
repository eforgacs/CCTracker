import pytest

from cctracker.models import Exercise, ExerciseType, Workout
from cctracker.progressions import Movement


def test_reps_done():
    exercise = Exercise(ExerciseType.workset, 3, 10)
    assert exercise.actual_reps == 0
    exercise.reps_done(11)
    assert exercise.actual_reps == 11
    with pytest.raises(ValueError):
        exercise.reps_done(-1)


def test_stepping_through_a_workout():
    workout = Workout(Movement.pullups, 2)
    assert workout.did_final_step()
    assert workout.next_step() is None

    workout.add_exercise(Exercise(ExerciseType.warmup, 1, 20))
    workout.add_exercise(Exercise(ExerciseType.workset, 2, 10))
    assert not workout.did_final_step()
    assert workout.next_step().exercise_type is ExerciseType.warmup
    assert workout.next_step().expected_reps == 10
    assert workout.did_final_step()
    assert workout.next_step() is None


def test_worksets_and_round_trip():
    workout = Workout(Movement.squats, 4, date="2026-01-01")
    workout.add_exercise(Exercise(ExerciseType.warmup, 3, 15, 15))
    workout.add_exercise(Exercise(ExerciseType.workset, 4, 8, 9))
    assert [e.step for e in workout.worksets()] == [4]
    assert Workout.from_dict(Movement.squats, workout.as_dict()) == workout


def test_full_workout_lists_every_set():
    workout = Workout(Movement.pushups, 7, note="hello")
    workout.add_exercise(Exercise(ExerciseType.workset, 7, 5))
    text = workout.full_workout()
    assert "Uneven pushups" in text
    assert "5 reps each side" in text
    assert "hello" in text
