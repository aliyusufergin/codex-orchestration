# Spawn audit at acceptance

The Parent runs the audit after validation and the planned reviews finish,
before deciding Acceptance. The command supplies host evidence; the Parent
applies the consequences below and fills the [acceptance report](reports.md).

## Run the command

Use Python 3.10+ and the installed plugin's `scripts/spawn-audit.py`. Resolve
the path from this reference: `../../../scripts/spawn-audit.py`. From a repository
checkout, the invocation is:

```sh
python3 plugins/codex-orchestration/scripts/spawn-audit.py <<'JSON'
{
  "start_time": "<run start, ISO 8601 with timezone>",
  "cwd": "<absolute owning session directory>",
  "planned_subagents": [
    {
      "task_name": "<canonical task path returned by the spawn>",
      "requested_model": "<model from the plan>",
      "requested_effort": "<effort from the plan>"
    }
  ]
}
JSON
```

Replace the placeholders and include every subagent planned during the run:
execution, review, correction and replacement review. Keep the original requested
settings when realization differs. Reusing a subagent for a follow-up keeps one
plan entry; the audit examines all its owning turns. Give each new spawn a unique
task name and retain disqualified reviews in the input. With no planned spawns,
use an empty array and still run the command to surface unplanned subagents.
The plan report supplies this input; no orchestration state file is required.

The [command interface](../../../scripts/spawn-audit.md) defines optional
`records_root` and `parent_thread_id`, exact output fields, matching and exit
statuses. Use the default host record location first; sandbox reads succeeded
in the runtime smoke. Missing access or a changed record format is reported as
`unobservable`, without assuming access requires escalation. If Python or the
command cannot run, state the failed invocation and reason as unobservable audit
coverage. Correct invalid JSON or input fields and rerun: exit 1 is an input
error, whereas exit 0 includes confirmed, mismatch and unobservable outcomes.

## Apply the evidence

Use the [capability snapshot](capability-snapshot.md), with live host metadata
taking precedence, to compare model strength and effort separately. Compare
each readable owning turn, including follow-ups; a null summary field can mean
settings varied, so inspect `evidence`. A stronger model does not compensate for
effort below the floor. Preserve the command's status even when strength cannot
be ordered: report that comparison as unknown, never invent a model equivalence
or treat a known difference as confirmed.

For reviews, use the effective requirement recorded in the plan, including any
stronger user minimum or explicit floor exception. Preserve the original floor
and the `by user preference` label for an exception. A runtime mismatch itself
does not authorise lowering a floor.

| Evidence | Consequence at acceptance |
| --- | --- |
| `confirmed` | Report requested and realized settings with sources. A review counts only if it also meets the plan's review requirements; confirmation alone is not a floor check. |
| A review has a realized model or effort below its effective floor on any owning turn | Disqualify that review and run a new planned, pinned, fresh-context review meeting the requirement before acceptance. |
| Execution ran weaker than requested | Report the weaker dimension and evidence; retain the work without redoing execution for this mismatch. Validation, required review and blocking-finding rules still apply. |
| Any subagent ran stronger than requested in model or effort | Report a `cost anomaly` with the requested and realized settings. This is routing drift, without a pricing or cost receipt. |
| `unobservable` settings or incomplete evidence | State the missing identity, fields or records plainly, alongside any readable evidence. Never claim confirmation; uncertainty alone does not block acceptance. A proven below-floor review remains disqualified even if other evidence is missing. |
| Unplanned subagents | List identities, settings and sources. Their output never counts as Review, even if their settings meet a floor. |
| `host_sessions` classified as `host_approval` | Report separately as host approval infrastructure; their output never counts as Review. |
| `parent_ran_at_ultra` is true | Add the label `Parent ran at Ultra` and cite the relevant turns. Continue the run and leave the Parent's settings untouched. |
| `parent_ran_at_ultra` is null | State Parent Ultra use as unobservable. False is appropriate only when the command supplies complete readable evidence with no Ultra turn. |

Apply every relevant row: stronger model plus weaker effort is both a cost
anomaly and weaker execution, or a disqualified review if effort is below its
floor. A review weaker than requested but still meeting its effective requirement
may count; report the mismatch. At high Consequence, also compare realized
review models with all realized execution models for that piece. A known collision
violates the required model difference and needs a replacement review.

For each disqualified review, show the reason and replacement task in the report.
Revise the plan, spawn the replacement against the same base and current candidate,
then rerun the audit with both entries before acceptance. A below-floor reviewer
is replaced by a fresh subagent, not continued as its own replacement. If routing
keeps realizing below the requirement, reassess the route or environment; acceptance
waits for a qualifying replacement. Unobservable replacement settings alone do
not block acceptance. Retain findings from disqualified reviews for disposition
under the normal blocking-finding rules; replacing a review does not erase them.
Finally confirm the reviewed candidate is unchanged as required by the skill.

## Preserve the runtime-smoke limits

The command already handles these findings from issue #3. Supply accurate input
and report its gaps rather than reconstructing identity from task names:

- Use the owning session directory for `cwd`; a shell tool's `workdir` does not
  relocate the session. Match Parent id, canonical task path, directory and run
  start together; names can recur in historical runs.
- Owning `session_meta.id` identifies a subagent; `session_id` may equal the
  Parent id. Embedded metadata and inherited history do not replace the first
  owning metadata or prove a fresh pinned spawn's settings.
- A null agent path may belong to a host guardian. Keep the command's separate
  host-approval classification and its unplanned work-subagent entries.
- Report `record_errors` and unresolved Parent identity. An empty unplanned
  list with incomplete discovery is not evidence that no unplanned spawns exist.
- Show every returned Parent turn with its timestamp, effort and source. Only
  turns at or after the recorded run start are returned; a run begun mid-turn
  may have no Parent turn in that window. With no work subagents, Parent effort
  is unobservable, including a run with only host approval sessions. Do not
  infer it from requested subagent settings or backdate the run to fill the gap.

The [runtime smoke and disposable-session completion](https://github.com/aliyusufergin/codex-orchestration/issues/3)
record the evidence and limits. These source records demonstrate this host's
behavior, not a guarantee that another host exposes the same record format.
