from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from .progressions import Movement, get_step


class ExerciseType(Enum):
    warmup = "warmup"
    workset = "workset"


@dataclass
class Exercise:
    """A single set: which step, how many reps were asked for, how many were done."""
    exercise_type: ExerciseType
    step: int
    expected_reps: int
    actual_reps: int = 0

    def reps_done(self, reps):
        if reps < 0:
            raise ValueError("reps can't be negative")
        self.actual_reps = reps

    def as_dict(self):
        return {
            "type": self.exercise_type.value,
            "step": self.step,
            "expected_reps": self.expected_reps,
            "actual_reps": self.actual_reps,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            exercise_type=ExerciseType(data["type"]),
            step=data["step"],
            expected_reps=data["expected_reps"],
            actual_reps=data.get("actual_reps", 0),
        )


@dataclass
class Workout:
    movement: Movement
    step: int
    exercises: list = field(default_factory=list)
    date: str = field(default_factory=lambda: date.today().isoformat())
    # Engine commentary ("progression standard met..."); shown to the user, not saved.
    note: str = ""
    _position: int = field(default=0, repr=False, compare=False)

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def worksets(self):
        return [e for e in self.exercises if e.exercise_type is ExerciseType.workset]

    def did_final_step(self):
        return self._position >= len(self.exercises)

    def next_step(self):
        """Returns the next exercise, or None once the workout is finished."""
        if self.did_final_step():
            return None
        exercise = self.exercises[self._position]
        self._position += 1
        return exercise

    def full_workout(self):
        step = get_step(self.movement, self.step)
        lines = [f"{self.movement.label} - step {step.number}: {step.name}  ({self.date})"]
        if self.note:
            lines.append(self.note)
        lines.append("")
        for exercise in self.exercises:
            set_step = get_step(self.movement, exercise.step)
            amount = f"{exercise.expected_reps} {set_step.unit}"
            if set_step.per_side:
                amount += " each side"
            lines.append(f"  {exercise.exercise_type.value:<8} {set_step.name:<30} {amount}")
        return "\n".join(lines) + "\n"

    def as_dict(self):
        return {
            "date": self.date,
            "step": self.step,
            "exercises": [e.as_dict() for e in self.exercises],
        }

    @classmethod
    def from_dict(cls, movement, data):
        return cls(
            movement=movement,
            step=data["step"],
            exercises=[Exercise.from_dict(e) for e in data["exercises"]],
            date=data["date"],
        )
