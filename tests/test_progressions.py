import pytest

from cctracker.progressions import PROGRESSIONS, STEPS_PER_MOVEMENT, Movement, get_step


@pytest.mark.parametrize("movement", list(Movement))
def test_every_movement_has_ten_increasing_standards(movement):
    steps = PROGRESSIONS[movement]
    assert [s.number for s in steps] == list(range(1, STEPS_PER_MOVEMENT + 1))
    for step in steps:
        volumes = [s.sets * s.reps for s in step.standards]
        assert volumes == sorted(volumes), step


def test_get_step():
    assert get_step(Movement.pushups, 10).name == "One-arm pushups"
    assert get_step(Movement.handstand_pushups, 1).timed
    with pytest.raises(ValueError):
        get_step(Movement.pushups, 11)
