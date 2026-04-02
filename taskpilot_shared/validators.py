from __future__ import annotations
import re
from datetime import datetime


EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email))


def validate_due_date(date_str: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized date format: {date_str!r}")


def validate_priority(priority: str) -> str:
    allowed = {"low", "medium", "critical"}
    if priority not in allowed:
        raise ValueError(f"Invalid priority {priority!r}. Must be one of {allowed}")
    return priority


def batch_validate_priorities(priorities: list[str]) -> dict[str, bool]:
    if not priorities:
        return {
            "valid_count": 0,
            "invalid_count": 0,
            "pass_rate": 0.0,
        }
    results = {}
    for p in priorities:
        try:
            validate_priority(p)
            results[p] = True
        except ValueError:
            results[p] = False
    summary = {
        "valid_count": sum(results.values()),
        "invalid_count": len(results) - sum(results.values()),
        "pass_rate": sum(results.values()) / len(priorities),
    }
    return summary
