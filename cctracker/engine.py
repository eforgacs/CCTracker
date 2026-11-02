"""Decides what your next session for a movement should look like.

The rules follow the book's "Making Progress" and "Warming Up" advice:
  * Warm up with a 20-rep set and then a 15-rep set of earlier, easier steps:
    ones you could do about 40 and 30 reps of.
  * Work toward the next standard at your current step, trying to beat last
    session by one rep per set (five seconds for timed holds).
  * Stick to one work set until you can do ten reps (or the intermediate
    standard's reps, if lower), then two; add a third only when the
    progression standard calls for it.
  * Once last session met the progression standard, move up a step and
    start again at its beginner standard.
"""

from math import ceil

from .models import Exercise, ExerciseType, Workout
from .progressions import STEPS_PER_MOVEMENT, get_step

REP_INCREMENT = 1
SECONDS_INCREMENT = 5
SINGLE_SET_UNTIL = 10
# (reps you could manage on the warm-up step, reps to actually do)
WARMUPS = ((40, 20), (30, 15))


def level_names(step_number):
    last = "elite" if step_number == STEPS_PER_MOVEMENT else "progression"
    return ("beginner", "intermediate", last)


def meets(reps_done, standard):
    """True if at least `standard.sets` sets reached `standard.reps`."""
    return sum(1 for reps in reps_done if reps >= standard.reps) >= standard.sets


class CCEngine:
    def next_workout(self, movement, record):
        step_number = record.current_step(movement)
        last = record.last_workout(movement)
        last_reps = []
        if last is not None and last.step == step_number and movement not in record.start_steps:
            last_reps = [e.actual_reps for e in last.worksets()]

        step = get_step(movement, step_number)
        note = ""
        if last_reps and meets(last_reps, step.progression):
            if step_number < STEPS_PER_MOVEMENT:
                step_number += 1
                step = get_step(movement, step_number)
                last_reps = []
                note = f"Progression standard met - welcome to step {step_number}!"
            else:
                note = "Master Step elite standard met. See the book's Going Beyond section for what's next."

        names = level_names(step_number)
        level, goal = next(((name, s) for name, s in zip(names, step.standards)
                            if not meets(last_reps, s)), (names[-1], step.progression))
        if not note:
            if not last_reps:
                note = f"New step: aim for the beginner standard ({goal})."
            elif goal is step.beginner:
                note = (f"Beginner standard ({goal}) not met yet. The book suggests going back to "
                        f"step {max(1, step_number - 1)} until you're ready.")
            else:
                note = f"Working toward the {level} standard ({goal})."

        workout = Workout(movement=movement, step=step_number, note=note)
        for warmup in self._warmups(movement, step_number):
            workout.add_exercise(warmup)
        for target in self._targets(step, goal, last_reps):
            workout.add_exercise(Exercise(ExerciseType.workset, step_number, target))
        return workout

    def _warmups(self, movement, step_number):
        warmups = []
        for capacity, reps in WARMUPS:
            easier = [n for n in range(1, step_number)
                      if get_step(movement, n).progression.reps >= capacity]
            if easier:
                warmups.append(Exercise(ExerciseType.warmup, easier[-1], reps))
            else:
                # Nothing easier to draw on: warm up lightly with the current step.
                step = get_step(movement, step_number)
                warmups.append(Exercise(ExerciseType.warmup, step_number, ceil(step.beginner.reps / 2)))
        return warmups

    def _targets(self, step, goal, last_reps):
        """One target per set: last time's reps plus a bit, capped at the goal."""
        if not last_reps:
            return [goal.reps] * goal.sets
        sets = goal.sets
        if goal is step.intermediate and max(last_reps) < min(SINGLE_SET_UNTIL, goal.reps):
            sets = 1
        increment = SECONDS_INCREMENT if step.timed else REP_INCREMENT
        targets = []
        for i in range(sets):
            # A newly added set aims to match the last one rather than beat it.
            previous = last_reps[i] + increment if i < len(last_reps) else last_reps[-1]
            targets.append(max(1, min(goal.reps, previous)))
        return targets
