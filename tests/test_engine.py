from cctracker.engine import CCEngine, meets
from cctracker.models import ExerciseType
from cctracker.progressions import Movement, Standard

from .test_record import make_workout

engine = CCEngine()


def plan(workout):
    return [(e.exercise_type, e.step, e.expected_reps) for e in workout.exercises]


def worksets(workout):
    return [e.expected_reps for e in workout.worksets()]


def test_meets():
    assert meets([20, 20], Standard(2, 20))
    assert meets([25, 20, 3], Standard(2, 20))
    assert not meets([20, 19], Standard(2, 20))
    assert not meets([], Standard(1, 1))


def test_brand_new_starts_at_step_one_beginner(record):
    workout = engine.next_workout(Movement.pushups, record)
    assert workout.step == 1
    assert plan(workout) == [
        (ExerciseType.warmup, 1, 5),
        (ExerciseType.warmup, 1, 5),
        (ExerciseType.workset, 1, 10),
    ]


def test_warmups_match_the_books_example(record):
    # Book: working close pushups (step 6) -> 20 incline pushups, then 15 kneeling pushups.
    record.set_start_step(Movement.pushups, 6)
    workout = engine.next_workout(Movement.pushups, record)
    assert plan(workout) == [
        (ExerciseType.warmup, 2, 20),
        (ExerciseType.warmup, 3, 15),
        (ExerciseType.workset, 6, 5),
    ]


def test_warmups_use_steps_easy_enough_for_high_reps(record):
    # Close pullups can't be done for 20 reps; drop back to vertical/horizontal pulls.
    record.set_start_step(Movement.pullups, 10)
    workout = engine.next_workout(Movement.pullups, record)
    assert [(e.step, e.expected_reps) for e in workout.exercises[:2]] == [(1, 20), (2, 15)]


def test_one_work_set_until_ten_reps_then_two(record):
    # Full pushups: beginner 1x5 met, working toward intermediate 2x10.
    record.record_workout(make_workout(Movement.pushups, 5, 7))
    workout = engine.next_workout(Movement.pushups, record)
    assert workout.step == 5
    assert worksets(workout) == [8]
    assert "intermediate" in workout.note

    record.record_workout(make_workout(Movement.pushups, 5, 10))
    assert worksets(engine.next_workout(Movement.pushups, record)) == [10, 10]

    record.record_workout(make_workout(Movement.pushups, 5, 10, 9))
    assert worksets(engine.next_workout(Movement.pushups, record)) == [10, 10]

    record.record_workout(make_workout(Movement.pushups, 5, 10, 10))
    workout = engine.next_workout(Movement.pushups, record)
    assert worksets(workout) == [11, 11]
    assert "progression" in workout.note


def test_two_sets_sooner_when_intermediate_reps_are_below_ten(record):
    # Full pullups: intermediate is 2x8, so a second set comes in at 8 reps.
    record.record_workout(make_workout(Movement.pullups, 5, 8))
    assert worksets(engine.next_workout(Movement.pullups, record)) == [8, 8]


def test_third_set_only_when_progression_needs_it(record):
    # Kneeling pushups: progression is 3x30.
    record.record_workout(make_workout(Movement.pushups, 3, 15, 15))
    assert worksets(engine.next_workout(Movement.pushups, record)) == [16, 16, 15]


def test_missing_the_beginner_standard_suggests_going_back(record):
    record.record_workout(make_workout(Movement.squats, 5, 3))
    workout = engine.next_workout(Movement.squats, record)
    assert worksets(workout) == [4]
    assert "going back to step 4" in workout.note


def test_targets_are_capped_at_the_goal(record):
    record.record_workout(make_workout(Movement.pushups, 5, 30))
    assert worksets(engine.next_workout(Movement.pushups, record)) == [10, 10]


def test_progression_standard_moves_you_up_a_step(record):
    record.record_workout(make_workout(Movement.pushups, 5, 20, 20))
    workout = engine.next_workout(Movement.pushups, record)
    assert workout.step == 6
    assert worksets(workout) == [5]
    assert "step 6" in workout.note


def test_master_step_stays_at_ten(record):
    record.record_workout(make_workout(Movement.pullups, 10, 6, 6))
    workout = engine.next_workout(Movement.pullups, record)
    assert workout.step == 10
    assert "elite standard met" in workout.note
    assert worksets(workout) == [6, 6]


def test_timed_holds_progress_in_seconds(record):
    record.record_workout(make_workout(Movement.handstand_pushups, 1, 40))
    workout = engine.next_workout(Movement.handstand_pushups, record)
    assert worksets(workout) == [45]


def test_start_step_ignores_old_history_at_that_step(record):
    record.record_workout(make_workout(Movement.squats, 5, 9, 9))
    record.set_start_step(Movement.squats, 5)
    workout = engine.next_workout(Movement.squats, record)
    assert worksets(workout) == [5]
