"""The Big Six ten-step progressions from Convict Conditioning (Paul Wade).

Each step has three standards, written as (sets, reps):
  beginner     -> where you start when you first reach the step
  intermediate -> halfway there
  progression  -> hit this and you've earned the next step

For timed holds (the first three handstand pushup steps) "reps" are seconds.
Unilateral movements (uneven, one-arm, one-leg...) are per side.

Names and numbers are checked against the book's Training Goals for each step.
On step 10 (the Master Step) the book calls the last standard the "elite" standard.
"""

from dataclasses import dataclass
from enum import Enum


class Movement(Enum):
    pushups = "pushups"
    squats = "squats"
    pullups = "pullups"
    leg_raises = "leg_raises"
    bridges = "bridges"
    handstand_pushups = "handstand_pushups"

    @property
    def label(self):
        return self.value.replace("_", " ").title()


@dataclass(frozen=True)
class Standard:
    sets: int
    reps: int

    def __str__(self):
        return f"{self.sets} x {self.reps}"


@dataclass(frozen=True)
class Step:
    movement: Movement
    number: int
    name: str
    beginner: Standard
    intermediate: Standard
    progression: Standard
    timed: bool = False
    per_side: bool = False

    @property
    def standards(self):
        return (self.beginner, self.intermediate, self.progression)

    @property
    def unit(self):
        return "sec" if self.timed else "reps"

    def __str__(self):
        return f"{self.movement.label} step {self.number}: {self.name}"


def _steps(movement, rows):
    steps = []
    for number, (name, beginner, intermediate, progression, *flags) in enumerate(rows, start=1):
        steps.append(Step(
            movement=movement,
            number=number,
            name=name,
            beginner=Standard(*beginner),
            intermediate=Standard(*intermediate),
            progression=Standard(*progression),
            timed="timed" in flags,
            per_side="per_side" in flags,
        ))
    return tuple(steps)


PROGRESSIONS = {
    Movement.pushups: _steps(Movement.pushups, [
        ("Wall pushups", (1, 10), (2, 25), (3, 50)),
        ("Incline pushups", (1, 10), (2, 20), (3, 40)),
        ("Kneeling pushups", (1, 10), (2, 15), (3, 30)),
        ("Half pushups", (1, 8), (2, 12), (2, 25)),
        ("Full pushups", (1, 5), (2, 10), (2, 20)),
        ("Close pushups", (1, 5), (2, 10), (2, 20)),
        ("Uneven pushups", (1, 5), (2, 10), (2, 20), "per_side"),
        ("1/2 one-arm pushups", (1, 5), (2, 10), (2, 20), "per_side"),
        ("Lever pushups", (1, 5), (2, 10), (2, 20), "per_side"),
        ("One-arm pushups", (1, 5), (2, 10), (1, 100), "per_side"),
    ]),
    Movement.squats: _steps(Movement.squats, [
        ("Shoulderstand squats", (1, 10), (2, 25), (3, 50)),
        ("Jackknife squats", (1, 10), (2, 20), (3, 40)),
        ("Supported squats", (1, 10), (2, 15), (3, 30)),
        ("Half squats", (1, 8), (2, 35), (2, 50)),
        ("Full squats", (1, 5), (2, 10), (2, 30)),
        ("Close squats", (1, 5), (2, 10), (2, 20)),
        ("Uneven squats", (1, 5), (2, 10), (2, 20), "per_side"),
        ("1/2 one-leg squats", (1, 5), (2, 10), (2, 20), "per_side"),
        ("Assisted one-leg squats", (1, 5), (2, 10), (2, 20), "per_side"),
        ("One-leg squats", (1, 5), (2, 10), (2, 50), "per_side"),
    ]),
    Movement.pullups: _steps(Movement.pullups, [
        ("Vertical pulls", (1, 10), (2, 20), (3, 40)),
        ("Horizontal pulls", (1, 10), (2, 20), (3, 30)),
        ("Jackknife pulls", (1, 10), (2, 15), (3, 20)),
        ("Half pullups", (1, 8), (2, 11), (2, 15)),
        ("Full pullups", (1, 5), (2, 8), (2, 10)),
        ("Close pullups", (1, 5), (2, 8), (2, 10)),
        ("Uneven pullups", (1, 5), (2, 7), (2, 9), "per_side"),
        ("1/2 one-arm pullups", (1, 4), (2, 6), (2, 8), "per_side"),
        ("Assisted one-arm pullups", (1, 3), (2, 5), (2, 7), "per_side"),
        ("One-arm pullups", (1, 1), (2, 3), (2, 6), "per_side"),
    ]),
    Movement.leg_raises: _steps(Movement.leg_raises, [
        ("Knee tucks", (1, 10), (2, 25), (3, 40)),
        ("Flat knee raises", (1, 10), (2, 20), (3, 35)),
        ("Flat bent leg raises", (1, 10), (2, 15), (3, 30)),
        ("Flat frog raises", (1, 8), (2, 15), (3, 25)),
        ("Flat straight leg raises", (1, 5), (2, 10), (2, 20)),
        ("Hanging knee raises", (1, 5), (2, 10), (2, 15)),
        ("Hanging bent leg raises", (1, 5), (2, 10), (2, 15)),
        ("Hanging frog raises", (1, 5), (2, 10), (2, 15)),
        ("Partial straight leg raises", (1, 5), (2, 10), (2, 15)),
        ("Hanging straight leg raises", (1, 5), (2, 10), (2, 30)),
    ]),
    Movement.bridges: _steps(Movement.bridges, [
        ("Short bridges", (1, 10), (2, 25), (3, 50)),
        ("Straight bridges", (1, 10), (2, 20), (3, 40)),
        ("Angled bridges", (1, 8), (2, 15), (3, 30)),
        ("Head bridges", (1, 8), (2, 15), (2, 25)),
        ("Half bridges", (1, 8), (2, 15), (2, 20)),
        ("Full bridges", (1, 6), (2, 10), (2, 15)),
        ("Wall walking bridges (down)", (1, 3), (2, 6), (2, 10)),
        ("Wall walking bridges (up)", (1, 2), (2, 4), (2, 8)),
        ("Closing bridges", (1, 1), (2, 3), (2, 6)),
        # The book gives the elite standard as 2 sets of 10-30.
        ("Stand-to-stand bridges", (1, 1), (2, 3), (2, 10)),
    ]),
    Movement.handstand_pushups: _steps(Movement.handstand_pushups, [
        ("Wall headstands", (1, 30), (1, 60), (1, 120), "timed"),
        ("Crow stands", (1, 10), (1, 30), (1, 60), "timed"),
        ("Wall handstands", (1, 30), (1, 60), (1, 120), "timed"),
        ("Half handstand pushups", (1, 5), (2, 10), (2, 20)),
        ("Handstand pushups", (1, 5), (2, 10), (2, 15)),
        ("Close handstand pushups", (1, 5), (2, 9), (2, 12)),
        ("Uneven handstand pushups", (1, 5), (2, 8), (2, 10), "per_side"),
        ("1/2 one-arm handstand pushups", (1, 4), (2, 6), (2, 8), "per_side"),
        ("Lever handstand pushups", (1, 3), (2, 4), (2, 6), "per_side"),
        ("One-arm handstand pushups", (1, 1), (2, 2), (1, 5), "per_side"),
    ]),
}

STEPS_PER_MOVEMENT = 10


def get_step(movement, number):
    if not 1 <= number <= STEPS_PER_MOVEMENT:
        raise ValueError(f"step must be between 1 and {STEPS_PER_MOVEMENT}, got {number}")
    return PROGRESSIONS[movement][number - 1]
