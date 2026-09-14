# Issue #4: spawn audit against real records

On 2026-09-14, the new command read the host's default session records for the
recent [issue #3 disposable-session run](issue-3/disposable-session/README.md).
No fixture root was supplied. The input used that run's actual session directory,
the Parent's creation timestamp, its explicit thread id, and a two-task plan:
`smoke_a` and `smoke_b`, each requesting `gpt-5.6-luna/low`.

```sh
python3 plugins/codex-orchestration/scripts/spawn-audit.py < /tmp/issue4-real-input.json
```

The input and complete report are temporary local artifacts because they contain
real session identifiers and paths. Only this summary is committed:

| Evidence | Result |
| --- | --- |
| `smoke_a` | confirmed, Luna/low on both initial and follow-up turns |
| `smoke_b` | confirmed, Luna/low on one turn |
| Unplanned subagents relative to the two-task input | `/root/standards_review`, `/root/spec_review` |
| Host session | guardian classified as `host_approval`, model `codex-auto-review` |
| Parent efforts | medium, medium |
| Parent ran at Ultra | false |
| Record errors | none |
| Exit status | 0 |

The two Review subagents appear as unplanned because this input deliberately
contains only the smoke probes. This agrees with the direct session records
reported in issue #3. The command recovered the Parent through its recorded
identity and retained both of its recorded turns. No conversation content was
emitted. This is a read-only smoke check of existing real records; it makes no
new model calls.
