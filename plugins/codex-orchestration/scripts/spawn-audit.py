#!/usr/bin/env python3
"""Read Codex rollout evidence; stdin and stdout are single JSON objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
import sys


def timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timestamp must include a timezone")
    return result


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def record(line: str) -> dict:
    row = json.loads(line)
    if not isinstance(row, dict) or not nonempty(row.get("type")):
        raise ValueError("Record must be an object with a type")
    if row["type"] in ("session_meta", "turn_context") and not isinstance(row.get("payload"), dict):
        raise ValueError("Record payload must be an object")
    return row


def validate_request(request) -> dict:
    if not isinstance(request, dict):
        raise ValueError("Input must be a JSON object")
    timestamp(request.get("start_time"))
    for key in ("cwd", "records_root"):
        if key == "records_root" and key not in request:
            continue
        value = request.get(key)
        if not nonempty(value) or "\0" in value or not Path(value).is_absolute():
            raise ValueError(f"{key} must be an absolute path")
    if "parent_thread_id" in request and not nonempty(request["parent_thread_id"]):
        raise ValueError("parent_thread_id must be a non-empty string")
    tasks = request.get("planned_subagents")
    if not isinstance(tasks, list):
        raise ValueError("planned_subagents must be an array")
    names = set()
    for task in tasks:
        if not isinstance(task, dict) or not all(nonempty(task.get(key)) for key in (
                "task_name", "requested_model", "requested_effort")):
            raise ValueError("Each planned subagent needs task_name, requested_model and requested_effort strings")
        if not re.fullmatch(r"(?:/root/)?[a-z0-9_]+", task["task_name"]):
            raise ValueError("task_name must be a direct task name or /root/<task_name>")
        task["task_name"] = task["task_name"].removeprefix("/root/")
        if task["task_name"] in names:
            raise ValueError("Planned task names must be unique")
        names.add(task["task_name"])
    return request


@dataclass
class Session:
    path: Path
    meta: dict

    def is_guardian(self) -> bool:
        source = self.meta.get("source")
        subagent = source.get("subagent") if isinstance(source, dict) else None
        return self.meta.get("thread_source") == "guardian_review" or (
            isinstance(subagent, dict) and subagent.get("other") == "guardian")

    def turns(self, start: datetime) -> tuple[list[dict], list[dict]]:
        start = max(start, timestamp(self.meta["timestamp"]))
        result = []
        errors = []
        line_number = 0
        try:
            with self.path.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    row = record(line)
                    if line_number > 1 and row["type"] == "session_meta":
                        raise ValueError("Embedded session metadata: subsequent turns may be inherited history")
                    if row["type"] != "turn_context":
                        continue
                    if timestamp(row.get("timestamp")) < start:
                        continue
                    payload = row["payload"]
                    if not all(nonempty(payload.get(key)) for key in ("model", "effort", "turn_id")):
                        raise ValueError("Turn lacks model, effort or turn id")
                    result.append({
                        "path": str(self.path), "line": line_number,
                        "thread_id": self.meta["id"], "timestamp": row["timestamp"],
                        "turn_id": payload["turn_id"],
                        "model": payload["model"], "effort": payload["effort"],
                    })
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append({"path": str(self.path), "line": line_number, "reason": str(exc)})
        return result, errors

    def parent_turns(self, start: datetime) -> tuple[list[dict], list[dict], str | None]:
        """Include the Parent turn already open at start, without widening child matching."""
        turns, errors = self.turns(timestamp(self.meta["timestamp"]))
        starts = {}
        ends = {}
        line_number = 0
        try:
            with self.path.open(encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    row = record(line)
                    if line_number > 1 and row["type"] == "session_meta":
                        break
                    payload = row.get("payload")
                    if row["type"] != "event_msg" or not isinstance(payload, dict):
                        continue
                    kind = payload.get("type")
                    if kind not in ("task_started", "task_complete", "turn_aborted"):
                        continue
                    when = timestamp(row.get("timestamp"))
                    if not nonempty(payload.get("turn_id")):
                        raise ValueError("Turn boundary lacks turn id")
                    if when <= start:
                        (starts if kind == "task_started" else ends)[payload["turn_id"]] = when
        except (OSError, UnicodeError, ValueError) as exc:
            error = {"path": str(self.path), "line": line_number, "reason": str(exc)}
            if error not in errors:
                errors.append(error)
        latest_start = max(starts.values()) if starts else None
        start_turn = max(starts, key=starts.get) if starts else None
        reason = None
        if start_turn in ends:
            start_turn = None
        # Contexts cannot reorder known starts, but an unidentified turn at the
        # boundary prevents a complete claim about Parent coverage.
        if any(turn["turn_id"] not in starts and turn["turn_id"] not in ends
               and timestamp(turn["timestamp"]) <= start
               and (latest_start is None or timestamp(turn["timestamp"]) >= latest_start)
               for turn in turns):
            reason = "Cannot establish the Parent turn open at run start"
        selected = [turn for turn in turns
                    if timestamp(turn["timestamp"]) >= start or turn["turn_id"] == start_turn]
        if start_turn is not None and not any(turn["turn_id"] == start_turn for turn in selected):
            reason = "No readable context for the Parent turn open at run start"
        return selected, errors, reason


def settings_report(turns: list[dict], errors: list[dict]) -> dict:
    models = {turn["model"] for turn in turns}
    efforts = {turn["effort"] for turn in turns}
    observable = bool(turns) and not errors
    return {
        "status": "observable" if observable else "unobservable",
        "reason": None if observable else (errors[0]["reason"] if errors else "No recorded turns in this run"),
        "realized_model": next(iter(models)) if len(models) == 1 else None,
        "realized_effort": next(iter(efforts)) if len(efforts) == 1 else None,
        "evidence": turns,
    }


def audit(request: dict) -> dict:
    start = timestamp(request["start_time"])
    root = Path(request.get("records_root", Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "sessions"))
    sessions = []
    errors = []
    if not root.is_dir():
        errors.append({"path": str(root), "reason": "Session records directory is missing or unreadable"})

    def walk_error(exc: OSError) -> None:
        errors.append({"path": str(exc.filename), "reason": str(exc)})

    for directory, dirs, files in os.walk(root, onerror=walk_error):
        dirs.sort()
        for filename in sorted(files):
            if not filename.endswith(".jsonl"):
                continue
            path = Path(directory) / filename
            try:
                with path.open(encoding="utf-8") as stream:
                    row = record(stream.readline())
                if row["type"] != "session_meta":
                    raise ValueError("First record is not owning session metadata")
                meta = row["payload"]
                if not all(nonempty(meta.get(key)) for key in ("id", "cwd")):
                    raise ValueError("Session metadata lacks id or cwd")
                for key in ("parent_thread_id", "agent_path"):
                    if meta.get(key) is not None and not nonempty(meta[key]):
                        raise ValueError(f"Session metadata {key} must be a string or null")
                if meta.get("thread_source") in ("subagent", "guardian_review") and not meta.get("parent_thread_id"):
                    raise ValueError("Subagent session metadata lacks parent_thread_id")
                timestamp(meta.get("timestamp"))
                sessions.append(Session(path, meta))
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append({"path": str(path), "line": 1, "reason": str(exc)})

    parent_id = request.get("parent_thread_id", os.environ.get("CODEX_THREAD_ID"))
    if not parent_id:
        planned_paths = {"/root/" + task["task_name"] for task in request["planned_subagents"]}
        parent_ids = {session.meta["parent_thread_id"] for session in sessions
                      if session.meta.get("parent_thread_id")
                      and session.meta.get("cwd") == request["cwd"]
                      and timestamp(session.meta["timestamp"]) >= start
                      and (not planned_paths or session.meta.get("agent_path") in planned_paths)}
        parent_id = next(iter(parent_ids)) if len(parent_ids) == 1 else None
    children = [session for session in sessions
                if parent_id and session.meta.get("parent_thread_id") == parent_id
                and timestamp(session.meta["timestamp"]) >= start]
    planned = []
    matched_paths = set()
    for task in request["planned_subagents"]:
        matches = [session for session in children
                   if session.meta.get("agent_path") == "/root/" + task["task_name"]
                   and not session.is_guardian()
                   and session.meta.get("cwd") == request["cwd"]]
        if len(matches) != 1:
            planned.append({**task, "status": "unobservable",
                            "reason": "No unique matching session record",
                            "realized_model": None, "realized_effort": None, "evidence": []})
            continue
        matched_paths.add(matches[0].path)
        turns, turn_errors = matches[0].turns(start)
        errors.extend(turn_errors)
        mismatch = any(turn["model"] != task["requested_model"]
                       or turn["effort"] != task["requested_effort"] for turn in turns)
        summary = settings_report(turns, turn_errors)
        if mismatch:
            summary["status"] = "mismatch"
        elif summary["status"] == "observable":
            summary["status"] = "confirmed"
        planned.append({**task, **summary})
    unplanned = []
    host_sessions = []
    for session in children:
        if session.path in matched_paths:
            continue
        turns, turn_errors = session.turns(start)
        errors.extend(turn_errors)
        item = {"thread_id": session.meta["id"], "agent_path": session.meta.get("agent_path"),
                "cwd": session.meta["cwd"], "path": str(session.path),
                "classification": "host_approval" if session.is_guardian() else "work_subagent",
                **settings_report(turns, turn_errors)}
        (host_sessions if session.is_guardian() else unplanned).append(item)
    parents = [session for session in sessions if session.meta["id"] == parent_id]
    has_work_subagents = any(not session.is_guardian() for session in children)
    parent_turns, parent_errors, parent_reason = parents[0].parent_turns(start) if len(parents) == 1 and has_work_subagents else ([], [], None)
    errors.extend(parent_errors)
    parent_report = {"thread_id": parent_id, "turns": parent_turns,
                     "status": "observable" if parent_turns and not parent_errors and not parent_reason else "unobservable"}
    if parent_report["status"] == "unobservable":
        if not has_work_subagents:
            parent_reason = "No work subagents found"
        elif len(parents) != 1:
            parent_reason = "No unique Parent session record"
        elif parent_errors:
            parent_reason = parent_errors[0]["reason"]
        elif not parent_reason:
            parent_reason = "No readable Parent turn in the run"
        parent_report["reason"] = parent_reason
    ultra = any(turn["effort"] == "ultra" for turn in parent_turns)
    return {"planned_subagents": planned, "unplanned_subagents": unplanned, "host_sessions": host_sessions,
            "record_errors": errors, "parent": parent_report,
            "parent_ran_at_ultra": True if ultra else (False if parent_report["status"] == "observable" else None)}


def main() -> int:
    try:
        request = validate_request(json.load(sys.stdin))
    except (ValueError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1
    print(json.dumps(audit(request), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
