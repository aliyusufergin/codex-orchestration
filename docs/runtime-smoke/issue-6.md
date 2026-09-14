# Issue #6: Scrutiny and preferences

Live native-subagent demo on 2026-09-14, with a disposable task repository at
`/tmp/codex-issue6-demo-u0bT36` and owning session directory
`/home/dev/projects/codex-orchestration`. This exercises the updated
[skill](../../plugins/codex-orchestration/skills/orchestration/SKILL.md) and
[report fields](../../plugins/codex-orchestration/skills/orchestration/references/reports.md).
It is a controlled documentation scenario, not a production release or a fresh
plugin-installation test. Scenario preferences below are test inputs, not new
preferences attributed to the user for this implementation session.

## Low Consequence: live skip

The Parent seeded `README.md` containing `# Demo` and `release.md` containing
`# Release`, a blank line, and `Publish the candidate.`. Seed commit:
`17a012f520f8bf1f9d12c215d692dc715e7ef6e1`, branch `main`.

Before changing the heading, the Parent announced low Consequence and a review
skip because the effect is cosmetic. Direct execution costs less than briefing
and checking a subagent for this one-line edit. The Parent changed the heading
to `# Scrutiny demo`, ran `git diff --check` (exit 0), inspected the diff, and
committed only `README.md`.

```text
ACCEPTANCE REPORT
base commit: 17a012f520f8bf1f9d12c215d692dc715e7ef6e1
candidate: f279e9ac0f9a32d796670412980e5ea15f87c681
candidate unchanged: HEAD equals candidate; git status --porcelain empty
validation: heading inspected; git diff --check exit 0
integration check: not needed; one change
reviews: not run
review skips: low Consequence; heading change is cosmetic
second reviews: not applicable
preferences: none
open blocking / non-blocking findings: none / none
spawn audit: no subagents; Parent effort unobservable for this demo
labels: review skipped at low Consequence — heading change is cosmetic
acceptance: accepted; no review claimed
```

## High Consequence: live review with a model exclusion

Plan shown before the first spawn, start `2026-09-14T18:15:01Z`:

```text
PLAN REPORT
base commit: f279e9ac0f9a32d796670412980e5ea15f87c681
branch / task directory: main / /tmp/codex-issue6-demo-u0bT36
session directory: /home/dev/projects/codex-orchestration
work: issue6_demo_work — require validation and review before publishing
  write scope: release.md
  dependencies: none
  Consequence: high; simulated release gate
  review requirement: required; floor gpt-5.6-sol/high; different execution model
  requested settings: gpt-5.6-luna/medium; fork_turns: "none"
  selection reason: starting point
  validation: inspect exact instruction; git diff --check
review: issue6_demo_review — inspect committed diff and return findings
  write scope: none
  dependencies: candidate and validation evidence
  Consequence: high
  requested settings: gpt-6-astra/high; fork_turns: "none"
  selection reason: scenario preference excludes the model at the floor
  independence: no work on candidate; different from gpt-5.6-luna
  second review: not planned
preferences: "do not use Sol"; execution unchanged, review moves above floor
direct execution: none
```

Native `collaboration.spawn_agent` returned `/root/issue6_demo_work` with the
planned explicit model, effort and fresh-context arguments. Its contract allowed
only `release.md`, prescribed the exact sentence
`Publish the candidate only after validation and review both pass.`, and forbade
spawning and version-control mutations. It returned exact diff inspection and
`git diff --check`, both exit 0. The Parent inspected the one-line diff and
committed it as `2b78d52c7903a50be5263b6b8628532efc829b91`.

The next pinned spawn returned `/root/issue6_demo_review` at the planned settings.
Its contract supplied both SHAs, the exact requirement, execution model and
validation evidence, with write scope `none`. It inspected the committed diff
and ran `git diff --check <base>...<candidate>`; both exited 0. It returned no
findings. Its before/after HEAD checks matched the candidate and tracked status
was clean. The Parent also confirmed HEAD, empty `git status --porcelain` and
successful `git diff --quiet` / `git diff --cached --quiet` at acceptance.

```text
ACCEPTANCE REPORT
base commit: f279e9ac0f9a32d796670412980e5ea15f87c681
candidate: 2b78d52c7903a50be5263b6b8628532efc829b91
candidate unchanged: matching HEAD before/after review; index and tree clean
validation: execution subagent inspected exact sentence; diff check exit 0
integration check: not needed; one change
reviews: issue6_demo_review; findings none; committed diff check exit 0
review skips: none
second reviews: not run; Parent chose one review for this bounded scenario
preferences: "do not use Sol"; actual review gpt-6-astra/high, above floor
open blocking / non-blocking findings: none / none
residual risk: documentation does not enforce the release gate at runtime
spawn audit: both requested settings confirmed; no unplanned subagents or errors
Parent efforts: unobservable; no Parent turns within the demo window
labels: none; preference strengthens review and needs no exception label
acceptance: accepted for the documentation scenario
```

The [spawn audit](../../plugins/codex-orchestration/scripts/spawn-audit.md) read
live default session records using the reported start time, owning session
directory, and two planned task names/settings; exit 0. Realized settings:

| Task | Requested and realized | Status | Owning record evidence |
| --- | --- | --- | --- |
| issue6_demo_work | `gpt-5.6-luna/medium` | confirmed | Thread `01a0a121-c25f-7a32-b37c-277ebaa800c0`, line 8, `2026-09-14T18:15:42.894Z` |
| issue6_demo_review | `gpt-6-astra/high` | confirmed | Thread `01a0a122-f1cb-7ec0-abdd-b6f594db3fdd`, line 8, `2026-09-14T18:16:58.870Z` |

Parent evidence was `unobservable` with reason `No unique Parent record with
turns in this run`, because the demo began during an existing turn.
`parent_ran_at_ultra` was null. Raw conversation records are not copied here.

## Additional preference cases

These are worked policy cases against the dated snapshot, not additional live
spawns. Model and effort minima are compared separately.

| Intent | Consequence | Result |
| --- | --- | --- |
| No preference | normal | Required review at `gpt-5.6-terra/high`. |
| AGENTS.md: "always review at the strongest floor" | low | Required review at `gpt-5.6-sol/max`; reason: requested strongest model and effort floors. No skip. |
| Request: "review at Luna/medium even if below the floor" | normal | Preserve the normal `gpt-5.6-terra/high` floor in the plan; run requested weaker review; report `by user preference`. |
| Request: "skip review for this change" | normal | Preserve normal Consequence and its required floor; explicitly remove the review; report `by user preference`. |
| Request excludes both models eligible for high review | high | Return conflict/options before dependent work; an exclusion alone does not lower the floor. |
| Execution used the strongest eligible reviewer model and all alternatives are excluded | high | Return model-difference conflict/options; fresh context alone does not satisfy the rule. |

The acceptance fields for the explicit skip case are:

```text
reviews: not run
review skips: normal Consequence; required review removed by explicit request
preferences: "skip review for this change"; review skipped by user preference
labels: by user preference — normal-Consequence review removed
```

The weaker-review case retains the original floor and states the actual result:

```text
preferences: normal floor gpt-5.6-terra/high; requested gpt-5.6-luna/medium
labels: by user preference — model and effort floors lowered
```

For a second high-Consequence review, the plan must add a separate fresh-context
subagent meeting the same floor and execution-model exclusion; acceptance keeps
its findings separate. This demo chooses not to add one and records that choice.
