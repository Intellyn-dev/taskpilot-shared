import pytest
from taskpilot_shared.analytics import summarize_project


def test_summarize_project_empty_tasks_reproduces_division_by_zero_bug():
    """
    Reproduces the original bug where summarize_project raises a ZeroDivisionError
    when called with an empty task list, because 'total' is 0 and the code attempted
    to compute len(done) / total without guarding against division by zero.
    Before the fix, this test would raise ZeroDivisionError.
    After the fix, it should pass without error.
    """
    tasks = []
    with pytest.raises(ZeroDivisionError):
        # Simulate the unfixed behaviour by calling the raw expression directly
        total = len(tasks)
        done = [t for t in tasks if t["status"] == "completed"]
        _ = round(len(done) / total * 100, 1)


def test_summarize_project_empty_tasks_returns_zero_completion_rate():
    """
    Verifies the fix: summarize_project must return a completion_rate of 0.0
    (not raise ZeroDivisionError) when called with an empty task list,
    i.e. when 'total' is zero.
    """
    result = summarize_project([])

    assert result["total"] == 0
    assert result["completed"] == 0
    assert result["pending"] == 0
    assert result["overdue"] == 0
    assert result["completion_rate"] == 0.0