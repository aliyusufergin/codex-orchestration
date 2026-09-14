# Spawn audit fixture provenance

`session-records/` copies the four sanitized JSONL seeds from issue #3's
[disposable-session records](../../../../docs/runtime-smoke/issue-3/disposable-session/README.md)
and `historical_review_spec.jsonl` from its
[earlier records](../../../../docs/runtime-smoke/issue-3/README.md).
The copied seeds are unchanged. They contain owning metadata and turn contexts,
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
