# Issue #15: Parent boundary replay and release smoke

## Replay of issue #14

The [retained input](../issue-14/spawn-audit-input.json) keeps its original
`2026-09-16T03:45:02Z` start, cwd, Parent identity and planned settings. The
[replay input](replay-input.json) adds only `records_root`, pointing to #14's
regenerated metadata projections. Both commands exited 0 with empty stderr.

| Command | Parent | Ultra | Planned subagents |
| --- | --- | --- | --- |
| Before, source `d32f9c5` / plugin 0.2.0 | Unobservable; “No unique Parent record with turns in this run” | `null` | Both confirmed |
| After, plugin 0.2.1 | Observable, `gpt-6-astra` / `high` | `false` | Both confirmed |

The [before output](replay-before.json) and [after output](replay-after.json)
cite the same projections. The start turn's context is at line 3; its
`task_started` event is at line 2 and `task_complete` at line 4, after the run
start. Neither audit has record errors or unplanned subagents. This replay
reproduces #14; it is separate from live release validation.

## Projection privacy

[project-records.py](project-records.py) rebuilds each selected line field by
field using the issue's explicit allowlist. It retains metadata and turn
boundaries, excluding conversation, reasoning, instructions and tool output.
The #14 projections and new fixture seed were rebuilt from the three owning
records under `~/.codex/sessions/2026/09/16/`, identified in the
[fixture provenance](../../../plugins/codex-orchestration/tests/fixtures/README.md).
The original #3 seeds and #14 audit input/output are unchanged.

Before committing, run the allowlist check on every new or regenerated projection:

```sh
python3 docs/runtime-smoke/issue-15/project-records.py --check \
  docs/runtime-smoke/issue-14/records/*.jsonl \
  plugins/codex-orchestration/tests/fixtures/issue-14/*.jsonl
```
