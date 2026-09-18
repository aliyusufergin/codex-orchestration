"""Rebuild metadata projections, or check retained projections against the allowlist."""

import json
from pathlib import Path
import sys


FIELDS = {
    "session_meta": {"id", "timestamp", "cwd", "thread_source", "parent_thread_id", "agent_path", "source"},
    "turn_context": {"turn_id", "root_turn_id", "cwd", "model", "effort", "sandbox_policy"},
    "event_msg": {"type", "turn_id"},
}
EVENTS = {"task_started", "task_complete", "turn_aborted"}


def check(path):
    for line in path.read_text().splitlines():
        row = json.loads(line)
        assert set(row) == {"timestamp", "type", "payload"}, path
        assert row["type"] in FIELDS, path
        assert set(row["payload"]) <= FIELDS[row["type"]], path
        if row["type"] == "event_msg":
            assert row["payload"]["type"] in EVENTS, path


if sys.argv[1] == "--check":
    for name in sys.argv[2:]:
        check(Path(name))
    print(f"Allowlist passed: {len(sys.argv) - 2} projections")
else:
    source, destination = map(Path, sys.argv[1:])
    rows = []
    for line in source.read_text().splitlines():
        row = json.loads(line)
        kind = row["type"]
        if kind not in FIELDS:
            continue
        if kind == "event_msg" and row["payload"].get("type") not in EVENTS:
            continue
        # Build new objects; never retain a whole live row or payload.
        rows.append({"timestamp": row["timestamp"], "type": kind,
                     "payload": {key: row["payload"][key] for key in sorted(FIELDS[kind])
                                 if key in row["payload"]}})
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(json.dumps(row) + "\n" for row in rows))
    check(destination)
