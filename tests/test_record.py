from cctracker.models import Exercise, ExerciseType, Workout
from cctracker.progressions import Movement
from cctracker.record import Record


def make_workout(movement, step, *reps, warmup_reps=None):
    workout = Workout(movement, step, date="2026-01-01")
    if warmup_reps is not None:
        workout.add_exercise(Exercise(ExerciseType.warmup, max(1, step - 1), 10, warmup_reps))
    for r in reps:
        workout.add_exercise(Exercise(ExerciseType.workset, step, 10, r))
    return workout


def test_new_record_is_empty_and_not_written(record):
    assert not record.path.exists()
    for movement in Movement:
        assert record.last_workout(movement) is None
        assert record.current_step(movement) == 1


def test_existing_record_is_loaded_not_overwritten(tmp_path):
    record = Record("ed", tmp_path)
    record.record_workout(make_workout(Movement.pushups, 5, 6, 4))
    record.save()

    reloaded = Record("ed", tmp_path)
    last = reloaded.last_workout(Movement.pushups)
    assert isinstance(last, Workout)
    assert [e.actual_reps for e in last.exercises] == [6, 4]
    assert reloaded.current_step(Movement.pushups) == 5


def test_only_worksets_with_reps_are_recorded(record):
    assert not record.record_workout(make_workout(Movement.pushups, 3, warmup_reps=10))
    assert not record.record_workout(make_workout(Movement.pushups, 3, 0, 0))
    assert record.last_workout(Movement.pushups) is None

    assert record.record_workout(make_workout(Movement.pushups, 3, 0, 5, warmup_reps=10))
    assert [e.actual_reps for e in record.last_workout(Movement.pushups).exercises] == [5]


def test_last_workout_is_per_movement(record):
    record.record_workout(make_workout(Movement.pushups, 3, 3, 10))
    record.record_workout(make_workout(Movement.pullups, 2, 2, 2))
    assert record.last_workout(Movement.pushups).step == 3
    assert record.last_workout(Movement.pullups).step == 2
    assert record.last_workout(Movement.squats) is None


def test_start_step_applies_until_next_workout(tmp_path):
    record = Record("ed", tmp_path)
    record.record_workout(make_workout(Movement.squats, 2, 5))
    record.set_start_step(Movement.squats, 6)
    record.save()

    record = Record("ed", tmp_path)
    assert record.current_step(Movement.squats) == 6
    record.record_workout(make_workout(Movement.squats, 6, 5))
    assert record.current_step(Movement.squats) == 6
    assert Movement.squats not in record.start_steps
