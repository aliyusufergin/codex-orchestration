# Issue #5: one delegated change through acceptance

Live native-subagent demo on 2026-09-14 using the rewritten
[orchestration skill](../../../plugins/codex-orchestration/skills/orchestration/SKILL.md).
The Parent read the skill and its references, supplied the contracts, made the
commits and accepted the candidate. This exercises the normal-Consequence path;
installation/invocation and fresh-session record matching were exercised in
issues #2 and #3. It does not claim a new plugin-installation smoke run.

The task repository was disposable:
`/tmp/codex-orchestration-issue5-9cjx4q0b`. The owning session directory remained
`/home/dev/projects/codex-orchestration`; shell commands used the disposable
repository as their working directory. The spawn audit therefore used the owning
session directory, not the task directory. No nested CLI or alternate inference
surface was used.

## Plan report shown before spawning

```text
PLAN REPORT
base commit: 0019dc24b955f66159de4c9ee1e69fd945052b30
branch: main
task directory: /tmp/codex-orchestration-issue5-9cjx4q0b
session directory: /home/dev/projects/codex-orchestration
run start: 2026-09-14T17:16:16Z
work:
  demo_change: trim greeting names; use "world" for blank names
    write scope: greeting.py, test_greeting.py in the task directory
    dependencies: none
    Consequence: normal; exercise the required review path
    requested settings: gpt-5.6-luna / medium; fork_turns: "none"
    selection reason: starting point
    validation: unittest plus Python compilation
review:
  demo_review: examine the committed candidate and return findings
    write scope: none
    dependencies: candidate commit and validation evidence
    Consequence: normal
    requested settings: gpt-5.6-terra / high; fork_turns: "none"
    selection reason: scrutiny floor
direct execution: none
```

The Parent seeded a Git repository on `main` with `greeting.py`, a unittest file
containing one named-greeting test, and `.gitignore` excluding `__pycache__/`.
The seed function returned `f"Hello, {name}!"`. The contract required surrounding
whitespace to be trimmed, empty or whitespace-only names to become `world`, and
existing named greetings and internal whitespace to remain unchanged.

## Pinned work and validation

The native `collaboration.spawn_agent` call specified:

```json
{
  "task_name": "demo_change",
  "model": "gpt-5.6-luna",
  "reasoning_effort": "medium",
  "fork_turns": "none"
}
```

The self-contained message supplied the objective above, the task directory,
write scope, completed dependency, agreed public `greet` test seam, exact
commands and expected outcomes. It forbade starting agents, Ultra, changes to
version-control state and edits to the main checkout. It required escalation of
any decision right to the Parent with options, evidence and work so far.
The host returned `/root/demo_change`.

The subagent returned these results, all from the task directory:

| Command | Result |
| --- | --- |
| `python3 -m unittest test_greeting.py -v`, before implementation | exit 1; three expected failures |
| Same command, after implementation | exit 0; five tests passed |
| `python3 -m py_compile greeting.py test_greeting.py` | exit 0 |

Its [candidate diff](candidate.patch) adds `name = name.strip() or "world"` and
four public-behaviour tests. The Parent inspected the diff and committed only
`greeting.py` and `test_greeting.py`, without re-running the subagent's checks:

```sh
git diff --check
git add greeting.py test_greeting.py
git -c user.name='Codex Demo' -c user.email=demo@example.invalid commit -m 'Normalize greeting names'
git rev-parse HEAD
```

All commands exited 0. The commit was
`336e4623e9ac4b4b42748797d262136eeb1b85f1`, on top of the recorded base.

## Review of the committed candidate

After the commit, the Parent made a second native spawn:

```json
{
  "task_name": "demo_review",
  "model": "gpt-5.6-terra",
  "reasoning_effort": "high",
  "fork_turns": "none"
}
```

The host returned `/root/demo_review`. This subagent did no work on the candidate.
Its contract supplied both SHAs, the comparison command, acceptance criteria,
validation evidence, write scope `none`, permission to re-run unittest and the
same spawn/version-control boundaries. It required findings with location,
evidence and a blocking mark, or `findings: none`, plus residual risk.
The writable sandbox was inherited; no enforced read-only isolation is claimed.

The review returned:

> findings: none.

It inspected the committed diff and both candidate files, and ran
`python3 -m unittest test_greeting.py -v`: exit 0, five tests passed. Its residual
risk was the declared string-input assumption. Before and after review,
`git rev-parse HEAD` returned the candidate SHA and `git status --porcelain`
returned no entries. The Parent independently checked the unchanged HEAD and
clean status, plus `git diff --quiet` and `git diff --cached --quiet` (exit 0).

## Acceptance report

```text
ACCEPTANCE REPORT
base commit: 0019dc24b955f66159de4c9ee1e69fd945052b30
candidate: 336e4623e9ac4b4b42748797d262136eeb1b85f1
candidate unchanged: same HEAD before/after review; index and working tree clean
validation: subagent reported 5 passing tests and successful compilation
integration check: not needed; one change
review: findings none; reviewer also ran all 5 tests successfully
open blocking / non-blocking findings: none / none
residual risk: input is assumed to be a string, as specified
spawn audit: both requested model/effort pairs confirmed; no unplanned subagents
Parent effort: unobservable within the demo's start-time window
labels: none
acceptance: accepted
```

The existing spawn audit command read live default session records with the plan's
start timestamp and owning session directory. It exited 0 with no record errors:

| Task | Requested | Realized | Status |
| --- | --- | --- | --- |
| `demo_change` | `gpt-5.6-luna` / medium | `gpt-5.6-luna` / medium | confirmed |
| `demo_review` | `gpt-5.6-terra` / high | `gpt-5.6-terra` / high | confirmed |

The Parent result was `unobservable`, with reason
`No unique Parent record with turns in this run`: the demo began within an
already-running Parent turn, and its timestamp window contained no Parent turn
record. `parent_ran_at_ultra` was null. This limitation was reported rather than
filled from requested settings. Full audit artifacts remain in `/tmp`; raw
session records and conversation content are not copied into this repository.
