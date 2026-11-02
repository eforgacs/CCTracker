import pytest

from cctracker.record import Record


@pytest.fixture
def record(tmp_path):
    return Record("tester", tmp_path)
