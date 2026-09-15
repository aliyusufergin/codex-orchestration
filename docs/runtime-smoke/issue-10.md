# Issue #10: Parallel work with write scopes and dependencies

Live native-subagent demo on 2026-09-15 in the implementation session at
`/home/dev/projects/codex-orchestration`, with disposable outputs in
`/tmp/codex-issue10-demo-7btGK3`. The demo exercises the
[parallel work instructions](../../plugins/codex-orchestration/skills/orchestration/references/parallel-work.md)
and [plan report](../../plugins/codex-orchestration/skills/orchestration/references/reports.md).
It is a controlled scheduling scenario, not a full orchestration or installation
test. Subagents used fresh contexts and inherited session settings; no pinned
spawn or realized-settings claim is made.

## Plan and contracts

The Parent showed the three pieces, their scopes and dependencies before the
first spawn. The host reported four concurrency slots including the Parent.
All paths below are relative to the disposable directory, and all task names
have canonical prefix `/root/issue10_`.

| Task | Objective | Write scope | Dependencies |
| --- | --- | --- | --- |
| `piece_a` | Create left value 2, stage `initial` | `left.json` | none |
| `piece_b` | Create right value 3 | `right.json` | none |
| `piece_c` | Double left to 4, stage `complete` | `left.json` | `piece_a` |
| `integration` | Check both complete outputs and total 7 | `none` | `piece_a`, `piece_b`, `piece_c` |

Each change contract supplied exact JSON content, a JSON validation command,
the relevant instructions and boundaries: only the named file could change,
no subagent starts or version-control changes, and decision rights returned to
the Parent. C received A's successful completion time, output and validation
evidence before it started. The integration contract supplied the expected
combined objects and required a read-only assertion check.

## Observed ordering

The Parent started A and B without waiting for either result. A native
`collaboration.list_agents` response showed both sessions `running` alongside
the Parent. Their scopes were disjoint. The timestamps below are the subagents'
reported command times, not host spawn timestamps or proof of simultaneous file
writes.

| Task | Reported start (UTC) | Reported finish (UTC) | Validation |
| --- | --- | --- | --- |
| `piece_a` | 11:08:32 | 11:08:43 | `python3 -m json.tool /tmp/codex-issue10-demo-7btGK3/left.json`, exit 0 |
| `piece_b` | 11:08:46 | 11:08:56 | `python3 -m json.tool /tmp/codex-issue10-demo-7btGK3/right.json`, exit 0 |
| `piece_c` | 11:09:19 | 11:09:31 | `python3 -m json.tool /tmp/codex-issue10-demo-7btGK3/left.json`, exit 0 |

C was spawned only after the Parent received A's completion and passing
validation. A and C share `left.json` and ran serially. The integration subagent
was spawned after all three change contracts returned successful validation.

## Plan change

The initial conversation plan assigned the integration check to the Parent.
During the run, the Parent showed an interim update assigning it to a fresh
subagent, with write scope `none` and dependencies on A, B and C. This let the
Parent document the demo while the subagent checked the combined result.

## Integration evidence

`/root/issue10_integration` reported start and finish at `11:10:17Z`, after C's
completion. It ran the following check, which exited 0:

```sh
python3 - <<'PY'
import json
from pathlib import Path

root = Path('/tmp/codex-issue10-demo-7btGK3')
left = json.loads((root / 'left.json').read_text())
right = json.loads((root / 'right.json').read_text())
assert left == {'name': 'left', 'value': 4, 'stage': 'complete'}, left
assert right == {'name': 'right', 'value': 3}, right
assert left['value'] + right['value'] == 7
print('PASS: left.json and right.json match exact expected objects; combined value total = 7')
PY
```

Output: `PASS: left.json and right.json match exact expected objects; combined value total = 7`.
The check reported no concerns or writes. This evidence was returned before the
implementation candidate was committed for the code-review workflow. The demo
files remain disposable; the review examines the committed instructions and
this evidence record, not a separately committed demo application.

## Coverage limits

This scenario demonstrates concurrently active independent sessions, a dependent
update that serializes a shared write scope, and the integration-check ordering.
It does not independently isolate the overlap rule from dependency ordering,
exhaust host capacity, exercise a capacity rejection, or test dependency failure,
cycles, ambiguous scopes or integration failure. Those branches are instructions
reviewed against the issue; this demo is not evidence that they ran. Per the
parent spec's testing decisions, no automated tests of rule prose were added.
