import io

from cctracker.cli import main
from cctracker.progressions import Movement
from cctracker.record import Record


def run(tmp_path, *argv, answers=()):
    out = io.StringIO()
    answers = iter(answers)
    code = main(["--user", "ed", "--data-dir", str(tmp_path), *argv], out=out, ask=lambda _: next(answers))
    return code, out.getvalue()


def test_steps_table(tmp_path):
    code, out = run(tmp_path, "steps", "hspu")
    assert code == 0
    assert "One-arm handstand pushups" in out
    assert "Wall pushups" not in out


def test_next_does_not_save(tmp_path):
    code, out = run(tmp_path, "next", "leg-raises")
    assert "Knee tucks" in out
    assert not (tmp_path / "ed.json").exists()


def test_log_records_reps_and_advances(tmp_path):
    run(tmp_path, "start", "pushups", "5")
    # two warmups (Enter = hit target), one workset, then save
    code, out = run(tmp_path, "log", "pushups", answers=["", "", "7", "y"])
    assert code == 0, out
    assert "Saved" in out
    last = Record("ed", tmp_path).last_workout(Movement.pushups)
    assert [e.actual_reps for e in last.exercises] == [7]

    _, out = run(tmp_path, "next", "pushups")
    assert "Full pushups                   8 reps" in out


def test_log_can_stop_early_and_decline_saving(tmp_path):
    _, out = run(tmp_path, "log", "squats", answers=["abc", "q", "n"])
    assert "whole number" in out
    assert "Not saved" in out
    assert not (tmp_path / "ed.json").exists()


def test_status_and_history(tmp_path):
    run(tmp_path, "log", "bridges", answers=["", "", "", "y"])
    _, out = run(tmp_path, "status")
    assert "Short bridges" in out and "last trained" in out
    _, out = run(tmp_path, "history")
    assert "Bridges" in out and "Pushups" not in out
