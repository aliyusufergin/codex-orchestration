# Reports

Show these short blocks in the user's conversation. Replace placeholders with
evidence or an explicit `not run`, `not needed` or `unobservable` and its reason.

## Plan report

Show before the first spawn; show revisions when the plan changes. This report
holds the plan, without a separate orchestration state file.

```text
PLAN REPORT
base commit: <SHA>
branch / working directory: <branch> / <absolute session directory>
run start: <ISO 8601 timestamp with timezone>
work:
  <task name>: <contract objective and acceptance criteria>
    write scope: <none or paths>
    dependencies: <none or task names>
    Consequence: <low | normal | high, with reason>
    requested settings: <model> / <effort>; fork_turns: "none"
    selection reason: <starting point, or capability/depth reason for departing>
    validation: <commands and expected outcomes>
review:
  <task name>: <candidate examination and findings to return>
    write scope: none
    dependencies: <candidate commit and validation evidence>
    Consequence: <level>
    requested settings: <model> / <effort>; fork_turns: "none"
    selection reason: <scrutiny floor, or reason for stronger selection>
direct execution: <none, or work and why delegation costs more>
```

## Acceptance report

```text
ACCEPTANCE REPORT
base commit: <SHA>
candidate: <SHA>
candidate unchanged: <HEAD before/after review, index and working-tree evidence>
validation: <commands, exit statuses and results; who ran them>
integration check: <evidence, or not needed because only one change was made>
reviews: <one entry per review/axis, with findings and residual risk>
open blocking findings: <must be none for acceptance>
open non-blocking findings: <locations and evidence, or none>
spawn audit:
  <task>: requested <model/effort>; realized <model/effort or unobservable>;
          <confirmed | mismatch | unobservable>; <source or reason>
  unplanned subagents: <evidence, or unobservable with reason>
  Parent efforts: <per-turn evidence, or unobservable with reason>
labels: <applicable labels and reasons, or none>
acceptance: <Parent's decision and evidence supporting it>
```

The [spawn audit command](../../../scripts/spawn-audit.md) provides settings
evidence; its input uses the session directory, even when the task's files live
elsewhere. Requested settings alone never fill the realized column.

Reserve labels for applicable run conditions: `Parent-only run` with
`no independent review`, `review skipped at low Consequence` with its reason,
`by user preference`, `Parent ran at Ultra`, and `ran without commits`.
These labels report a condition; they do not authorise an exception by themselves.
