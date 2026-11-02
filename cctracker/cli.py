import argparse
import getpass
import os
import sys

from .engine import CCEngine
from .progressions import PROGRESSIONS, Movement, get_step
from .record import DEFAULT_DATA_DIR, Record

ALIASES = {"hspu": Movement.handstand_pushups, "legs": Movement.leg_raises}


def movement_arg(text):
    key = text.lower().replace("-", "_")
    if key in ALIASES:
        return ALIASES[key]
    try:
        return Movement(key)
    except ValueError:
        choices = ", ".join(m.value for m in Movement)
        raise argparse.ArgumentTypeError(f"unknown movement '{text}' (choose from {choices}, hspu)")


def cmd_steps(args, record, out, ask):
    movements = [args.movement] if args.movement else list(Movement)
    for movement in movements:
        print(f"\n{movement.label}", file=out)
        print(f"  {'#':>2}  {'Step':<30} {'Beginner':>9} {'Intermed.':>9} {'Progress.':>9}", file=out)
        for step in PROGRESSIONS[movement]:
            suffix = " (sec)" if step.timed else " (each side)" if step.per_side else ""
            print(f"  {step.number:>2}  {step.name:<30} {str(step.beginner):>9} "
                  f"{str(step.intermediate):>9} {str(step.progression):>9}{suffix}", file=out)


def cmd_status(args, record, out, ask):
    print(f"{record.name}'s progress", file=out)
    for movement in Movement:
        step = get_step(movement, record.current_step(movement))
        last = record.last_workout(movement)
        last_text = f"last trained {last.date}" if last else "not started"
        print(f"  {movement.label:<18} step {step.number:>2}  {step.name:<30} {last_text}", file=out)


def cmd_start(args, record, out, ask):
    record.set_start_step(args.movement, args.step)
    record.save()
    print(f"{get_step(args.movement, args.step)} - your next workout will start here.", file=out)


def cmd_next(args, record, out, ask):
    print(CCEngine().next_workout(args.movement, record).full_workout(), file=out, end="")


def cmd_log(args, record, out, ask):
    workout = CCEngine().next_workout(args.movement, record)
    print(workout.full_workout(), file=out)
    print("Enter reps (or seconds) for each set. Enter = hit the target, q = stop here.\n", file=out)
    while (exercise := workout.next_step()) is not None:
        step = get_step(args.movement, exercise.step)
        prompt = (f"{exercise.exercise_type.value} - {step.name}, "
                  f"target {exercise.expected_reps} {step.unit}: ")
        answer = _ask_reps(ask, prompt, out)
        if answer == "q":
            break
        exercise.reps_done(exercise.expected_reps if answer is None else answer)

    if ask("\nSave this workout? [Y/n] ").strip().lower() in ("", "y", "yes"):
        if record.record_workout(workout):
            record.save()
            print(f"Saved to {record.path}", file=out)
        else:
            print("No work sets with reps were done - nothing to save.", file=out)
    else:
        print("Not saved.", file=out)


def _ask_reps(ask, prompt, out):
    while True:
        answer = ask(prompt).strip().lower()
        if answer in ("", "q"):
            return None if answer == "" else "q"
        if answer.isdigit():
            return int(answer)
        print("Please enter a whole number, Enter, or q.", file=out)


def cmd_history(args, record, out, ask):
    movements = [args.movement] if args.movement else list(Movement)
    for movement in movements:
        workouts = record.history(movement)
        if not workouts:
            continue
        print(f"\n{movement.label}", file=out)
        for workout in workouts[-args.limit:]:
            reps = ", ".join(str(e.actual_reps) for e in workout.exercises)
            print(f"  {workout.date}  step {workout.step:>2} {get_step(movement, workout.step).name:<30} "
                  f"{reps}", file=out)


def build_parser():
    parser = argparse.ArgumentParser(prog="cctracker", description="Track Convict Conditioning workouts.")
    parser.add_argument("-u", "--user", default=os.environ.get("CCTRACKER_USER") or getpass.getuser(),
                        help="whose record to use (default: $CCTRACKER_USER or your login name)")
    parser.add_argument("--data-dir", default=DEFAULT_DATA_DIR,
                        help="where records are stored (default: $CCTRACKER_HOME or ~/.cctracker)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("steps", help="show the ten-step progression tables")
    p.add_argument("movement", nargs="?", type=movement_arg)
    p.set_defaults(func=cmd_steps)

    p = sub.add_parser("status", help="show your current step for each movement")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("start", help="set the step you're starting from")
    p.add_argument("movement", type=movement_arg)
    p.add_argument("step", type=int, choices=range(1, 11), metavar="step (1-10)")
    p.set_defaults(func=cmd_start)

    p = sub.add_parser("next", help="print your next workout")
    p.add_argument("movement", type=movement_arg)
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("log", help="step through your next workout and record it")
    p.add_argument("movement", type=movement_arg)
    p.set_defaults(func=cmd_log)

    p = sub.add_parser("history", help="show past workouts")
    p.add_argument("movement", nargs="?", type=movement_arg)
    p.add_argument("-n", "--limit", type=int, default=10, help="workouts per movement (default 10)")
    p.set_defaults(func=cmd_history)
    return parser


def main(argv=None, out=sys.stdout, ask=input):
    args = build_parser().parse_args(argv)
    record = Record(args.user, args.data_dir)
    try:
        args.func(args, record, out, ask)
    except (KeyboardInterrupt, EOFError):
        print("\nStopped - nothing saved.", file=out)
        return 1
    return 0
