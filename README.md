# CCTracker

A command-line tracker for *Convict Conditioning* (Paul Wade) workouts.
It knows the Big Six ten-step progressions, works out what your next session should be from your
history, walks you through it set by set, and records what you actually did.

## Install

Requires Python 3.10+, no dependencies.

```sh
pip install -e .           # or: uv pip install -e .
cctracker --help           # or, without installing: python -m cctracker --help
```

## Usage

```sh
cctracker steps pushups        # the ten-step table with beginner / intermediate / progression standards
cctracker start pushups 5      # already past step 1? jump straight to your step
cctracker next pushups         # print today's workout without saving anything
cctracker log pushups          # step through it, enter your reps, and save
cctracker status               # current step for all six movements
cctracker history pullups      # past sessions
```

Movements: `pushups`, `squats`, `pullups`, `leg-raises`, `bridges`, `handstand-pushups` (or `hspu`).

During `log`, press Enter to record the target, type the number you actually did, or `q` to finish
early. Only work sets with at least one rep are saved; warm-ups aren't recorded.

Records are JSON files in `~/.cctracker/<user>.json`. Change the user with `--user` or
`$CCTRACKER_USER`, and the directory with `--data-dir` or `$CCTRACKER_HOME`.

## How the next workout is chosen

Following the book's *Warming Up* and *Making Progress* advice:

1. **Warm-up**: 20 reps, then 15 reps, of earlier steps easy enough that you could do about 40 and
   30 reps of them (e.g. close pushups -> incline pushups, then kneeling pushups).
2. **Work sets**: aim for the next standard you haven't met at your current step, beating last
   session by one rep per set (five seconds for timed holds), capped at that standard. You do one
   work set until you can reach ten reps, then two; a third only if the progression standard needs it.
3. **Progression**: when your last session met the progression standard, you move up to the next step
   and start again at its beginner standard. Step 10, the Master Step, has an elite standard instead.

The tables live in [`cctracker/progressions.py`](cctracker/progressions.py).

## Development

```sh
uv venv && uv pip install -e '.[test]'
.venv/bin/pytest
```
