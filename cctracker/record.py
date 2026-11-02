import json
import os
from pathlib import Path

from .models import ExerciseType, Workout
from .progressions import Movement, get_step

DEFAULT_DATA_DIR = Path(os.environ.get("CCTRACKER_HOME", Path.home() / ".cctracker"))


class Record:
    """One person's training history, stored as a JSON file named after them.

    An existing file is loaded; a missing one starts an empty history. Nothing
    is written to disk until save() is called.
    """

    def __init__(self, name, data_dir=DEFAULT_DATA_DIR):
        self.name = name
        self.path = Path(data_dir) / f"{name}.json"
        self.start_steps = {}
        self.workouts = {movement: [] for movement in Movement}
        if self.path.exists():
            self._load()

    def _load(self):
        data = json.loads(self.path.read_text())
        self.start_steps = {Movement(m): step for m, step in data.get("start_steps", {}).items()}
        for movement_name, workouts in data.get("workouts", {}).items():
            movement = Movement(movement_name)
            self.workouts[movement] = [Workout.from_dict(movement, w) for w in workouts]

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(".json.tmp")
        tmp_path.write_text(json.dumps(self.as_dict(), indent=2) + "\n")
        tmp_path.replace(self.path)

    def as_dict(self):
        return {
            "name": self.name,
            "start_steps": {m.value: step for m, step in self.start_steps.items()},
            "workouts": {m.value: [w.as_dict() for w in ws] for m, ws in self.workouts.items()},
        }

    def set_start_step(self, movement, step):
        """Jump to a step (e.g. when you already train beyond step 1).

        Applies until the next workout is recorded for the movement.
        """
        get_step(movement, step)  # validates the range
        self.start_steps[movement] = step

    def last_workout(self, movement):
        """Returns the most recent workout for the movement, or None."""
        workouts = self.workouts[movement]
        return workouts[-1] if workouts else None

    def history(self, movement):
        return list(self.workouts[movement])

    def current_step(self, movement):
        """A pending start step wins, then the step last trained, then step 1."""
        if movement in self.start_steps:
            return self.start_steps[movement]
        last = self.last_workout(movement)
        return last.step if last else 1

    def record_workout(self, workout):
        """Keep only worksets with at least one rep done; skip the workout if none are left.

        Returns True if anything was recorded.
        """
        kept = [e for e in workout.exercises
                if e.exercise_type is ExerciseType.workset and e.actual_reps > 0]
        if not kept:
            return False
        self.workouts[workout.movement].append(
            Workout(movement=workout.movement, step=workout.step, exercises=kept, date=workout.date))
        self.start_steps.pop(workout.movement, None)
        return True
