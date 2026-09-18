# Spawn audit fixture provenance

`session-records/` copies the four sanitized JSONL seeds from issue #3's
[disposable-session records](../../../../docs/runtime-smoke/issue-3/disposable-session/README.md)
and `historical_review_spec.jsonl` from its
[earlier records](../../../../docs/runtime-smoke/issue-3/README.md).
Issue #4 built its fixtures from these issue #3 samples alone. The copied seeds
are unchanged. They contain owning metadata and turn contexts,
never conversations or credentials.

The command tests copy these seeds to a temporary records root. Individual tests
derive mismatches, inherited Parent settings, extra or missing sessions, duplicate
names, malformed records, and additional Parent turns by changing the relevant
fields. These variations are synthetic cases, not claims about the smoke run.
The guardian variation follows issue #3's observed `guardian_review`, null
`agent_path`, and `source.subagent.other = "guardian"` shape.

The historical embedded Parent metadata is deliberately preserved. Its inherited
contexts must never confirm a subagent. `session_id` is shared in the seeds;
only the first `session_meta.id` identifies the owning session. Matching also
uses Parent id, canonical task path, session cwd, and creation time. The older
records must not be confused with current tasks even when paths are reused.

Issue #15 adds `issue-14/`, a second seed projected from the live
[issue #14 release smoke](../../../../docs/runtime-smoke/issue-14/README.md).
The source is `~/.codex/sessions/2026/09/16/`: Parent
`01a0a851-0923-7893-8c0c-dcb4a2863055`, repair
`01a0a852-6386-77f3-a2e3-e4ecc66fd84a`, and review
`01a0a854-e1e3-7dd3-8d2a-fe65842408db`. Each projection has four lines:
owning metadata, `task_started`, `turn_context`, and `task_complete`.
These are rebuilt field by field using the release checklist's allowlist, with
no copied live lines. Their keys are checked before committing. They also
regenerate #14's retained projections, adding the boundary events needed for
the [before/after replay](../../../../docs/runtime-smoke/issue-15/README.md).

Tests derive open start turns, Ultra, later spawning turns, compaction contexts,
completed/aborted historical turns and unestablished boundaries from this seed.
Derived cases are synthetic; the unchanged seed retains the original timestamps,
identities, directories and settings.
