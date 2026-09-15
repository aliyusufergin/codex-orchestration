# Reports

Show these short blocks in the user's conversation. Replace placeholders with
evidence or an explicit `not run`, `not needed` or `unobservable` and its reason.

## Plan report

For a [Parent-only run](without-pinned-spawning.md), apply that procedure's
plan-report adjustments before filling this block.

Show before the first spawn; show revisions when the plan changes. This report
holds the plan, without a separate orchestration state file.
For a permitted skip, put the reason in the work's review requirement and omit
that review's spawn entry. Each planned second review gets its own entry.

```text
PLAN REPORT
base commit: <SHA>
branch / working directory: <branch> / <absolute session directory>
run start: <ISO 8601 timestamp with timezone>
host capacity: <reported slot limit, live occupancy and available slots>
work:
  <task name>: <contract objective and acceptance criteria>
    write scope: <none or paths>
    dependencies: <none or task names>
    Consequence: <low | normal | high, with reason>
    review requirement: <required or skipped with reason; snapshot model/effort floor;
                         effective requirement after preferences; model difference if high>
    requested settings: <model> / <effort>; fork_turns: "none"
    selection reason: <starting point, or capability/depth reason for departing>
    validation: <commands and expected outcomes>
  <repeat for every planned contract>
integration check:
  <task name, or not needed because only one change is planned>:
    executor: <Parent or planned subagent with model/effort and selection reason>
    write scope: <none or paths>
    dependencies: <all tasks whose changes are combined>
    validation: <commands, combined scope and expected outcomes>
review:
  <task name>: <candidate examination and findings to return>
    write scope: none
    dependencies: <candidate commit and validation evidence>
    Consequence: <level>
    requested settings: <model> / <effort>; fork_turns: "none"
    selection reason: <scrutiny floor, or reason for stronger selection>
    independence: <no work on candidate; if high, compare with execution models>
    second review: <separate task entry, or not planned>
preferences: <request/AGENTS.md preferences and routing/checking effects, or none>
direct execution: <none, or work and why delegation costs more>
```

## Acceptance report

For a [Parent-only run](without-pinned-spawning.md), distinguish the Parent's
checks from independent reviews and apply that reference's required labels.

For findings-only work, report the findings and the Parent decision they inform;
mark candidate and review fields `not needed: findings-only` when the whole run
has no changes. In mixed runs, list those tasks separately from candidate reviews.
Record any independent findings check and its evidence without counting it as a
candidate review. Include all findings-only subagents in the spawn audit.

```text
ACCEPTANCE REPORT
base commit: <SHA>
candidate: <SHA>
candidate unchanged: <HEAD before/after review, index and working-tree evidence>
validation: <commands, exit statuses and results; who ran them>
integration check: <evidence, or not needed because only one change was made>
reviews: <one entry per review/axis, with findings and residual risk>
review skips: <work, Consequence and one-line reason, or none>
second reviews: <per high-Consequence piece: review entry, or not run>
correction history: <none, or chronological entries below>
  <findings and originating reviewer/axis>:
    candidate: <reviewed SHA -> corrected SHA; unchanged for a dispute-only review>
    contract / routing: <correction objective, task path, model/effort;
                         follow-up, replacement or direct execution and reason>
    reassessment: <surviving finding or plan/contract challenge, evidence and changed
                   contract/model/plan; capability-gap reason if stronger; or none>
    validation: <commands, exit statuses and results, or reference to evidence above>
    review: <task path, compared SHAs, follow-up or whole candidate, findings and
             disposition per blocking finding; dispute evidence and outcome if any>
preferences: <applied preferences and actual routing/checking;
              label each relaxed floor or removed review "by user preference">
open blocking findings: <must be none for acceptance>
open non-blocking findings: <locations and evidence, or none>
spawn audit:
  command: <invocation, run start and session directory; exit status>
  <task>: requested <model/effort>; realized <model/effort or unobservable>;
          <confirmed | mismatch | unobservable>; <source or reason>
          effect: <review counts / disqualified and replacement task;
                   weaker execution retained; cost anomaly; or none>
  unplanned subagents: <identities, realized settings and sources;
                       none found, or discovery unobservable with reason>
  host approval sessions: <separately classified evidence, or none found>
  record errors: <paths/reasons and limits on coverage, or none>
  Parent efforts: <each turn's timestamp, effort and source;
                   retain readable turns alongside any unobservable remainder>
  Parent ran at Ultra: <true | false | unobservable, from audit evidence>
labels: <applicable labels and reasons, or none>
acceptance: <Parent's decision and evidence supporting it>
```

Apply the [spawn audit](spawn-audit.md) reference before filling this block.
Keep every planned subagent, including disqualified and replacement reviews.
For settings that change across turns, list each turn with its source instead
of collapsing the evidence into one model/effort pair. Requested settings alone
never fill the realized column. Summarize evidence without copying conversation
content from the host records.

Reserve labels for applicable run conditions: `Parent-only run` with
`no independent review`, `review skipped at low Consequence` with its reason,
`by user preference`, `Parent ran at Ultra`, and `ran without commits`.
These labels report a condition; they do not authorise an exception by themselves.
