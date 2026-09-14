# Spawn audit command

Run with Python 3.10+; no third-party packages are needed:

```sh
python3 plugins/codex-orchestration/scripts/spawn-audit.py < run.json
```

Input is one JSON object:

```json
{
  "start_time": "2026-09-14T07:43:00Z",
  "cwd": "/tmp/disposable-repo",
  "planned_subagents": [
    {
      "task_name": "smoke_a",
      "requested_model": "gpt-5.6-luna",
      "requested_effort": "low"
    }
  ]
}
```

`start_time` is an ISO 8601 timestamp with a timezone. `cwd` is the absolute
session directory, not a shell tool's working-directory override. Task names
are unique direct task names (`smoke_a`) or canonical paths (`/root/smoke_a`).
Requested model and effort are nonempty strings compared exactly with the host;
the command does not impose a dated model catalog. An empty plan is valid.

Two optional fields control record lookup:

- `records_root`: absolute directory containing JSONL rollouts, searched
  recursively. Defaults to `$CODEX_HOME/sessions`, or `~/.codex/sessions` when
  `CODEX_HOME` is unset. Tests supply a temporary fixture root.
- `parent_thread_id`: identifies the Parent explicitly. Otherwise the command
  uses `CODEX_THREAD_ID`; outside a host session, it follows matching subagent
  records to a unique Parent. If several Parents match, identity is unobservable.
  Supply this field when auditing another run or testing from a live session.

Output is one JSON object. `planned_subagents` preserves input order and contains
requested settings, `realized_model`, `realized_effort`, `status`, and `evidence`.
Each evidence entry cites the file path, line, owning thread id, turn id,
timestamp, model, and effort. A realized field is `null` when there are no readable
turns or that setting changes across turns; evidence retains each readable turn.

- `confirmed`: every readable owning turn matches, with no unreadable remainder.
- `mismatch`: at least one owning turn differs, including a follow-up turn or an
  unpinned spawn that inherited the Parent's settings. A mismatch remains proven
  even if later evidence is unreadable; consult `record_errors` for those gaps.
- `unobservable`: identity is missing or ambiguous, or complete owning settings
  cannot be read. `reason` explains why. The command never fills in missing
  realized settings from the plan or Parent.

`unplanned_subagents` lists other direct subagents under the same Parent created
at or after the start, including those with a different session directory or
an unknown task path. `host_sessions` retains guardian records separately with
`classification: "host_approval"`; these do not count as work subagents or Review.
Both lists include realized settings and evidence, with an observable/unobservable
status. Duplicate matches to a planned name make that planned entry unobservable.

`parent` contains its thread id, observable/unobservable status, and `turns`, each
with model, effort and source evidence. Only turns at or after the run's start
are included. `parent_ran_at_ultra` is `true` if any readable owning Parent turn
ran at Ultra, `false` when complete readable Parent evidence contains no Ultra,
and `null` when unknown. In accordance with ADR 0002, a run with no subagents has
no Parent effort record. An empty plan still reports any unplanned subagents.

`record_errors` describes missing, unreadable, or malformed files and directories.
An empty unplanned list is not proof that no unplanned subagents exist when
discovery has errors or Parent identity is unresolved. Only first-record owning
metadata is indexed. A second metadata record ends trustworthy attribution:
subsequent inherited contexts are not used. The command reads the live files
without locking them; an unfinished line is unobservable and can be retried.
Only metadata and turn evidence are emitted, never conversation content.

All audit outcomes exit **0**, including mismatch and unobservable. Invalid JSON
or invalid input fields return a JSON `error` and exit **1**. Record access and
format problems are audit outcomes, not invalid input.

Run the command tests directly with:

```sh
python3 -m unittest discover -s plugins/codex-orchestration/tests -p test_spawn_audit.py
```

The repository's `verify.sh` runs these tests as well as package checks, and the
existing GitHub Actions workflow invokes that same verifier.
