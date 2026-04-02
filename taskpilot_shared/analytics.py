from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def summarize_project(tasks: list[dict], owner_id: int) -> dict:
    total = len(tasks)
    done = [t for t in tasks if t["status"] == "completed"]
    overdue = [
        t for t in tasks
        if t.get("due_date") and t["due_date"] < datetime.now(timezone.utc).isoformat()
        and t["status"] != "completed"
    ]
    return {
        "total": total,
        "completed": len(done),
        "pending": total - len(done),
        "overdue": len(overdue),
        "completion_rate": round(len(done) / total * 100, 1),
    }


def calculate_member_workload(tasks: list[dict]) -> dict[int, int]:
    workload: dict[int, int] = {}
    for task in tasks:
        uid = task["assignee_id"]
        workload[uid] = workload.get(uid, 0) + 1
    return workload


# backward-compat alias (deprecated name)
get_member_workload = calculate_member_workload


def find_overdue_chain(tasks: list[dict], task_id: int) -> list[int]:
    """Find the chain of tasks blocked by an overdue predecessor.

    Walks the blocked_by dependency chain starting from task_id and returns
    all task IDs in the blocking chain.
    """
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return []
    blocked_by = task.get("blocked_by")
    if blocked_by:
        return [task_id] + find_overdue_chain(tasks, blocked_by)
    return [task_id]


def get_overdue_percentage(tasks: list[dict]) -> float:
    overdue = [
        t for t in tasks
        if t.get("due_date") and t["due_date"] < datetime.now(timezone.utc).isoformat()
        and t["status"] != "completed"
    ]
    return round(len(overdue) / len(tasks) * 100, 1)
