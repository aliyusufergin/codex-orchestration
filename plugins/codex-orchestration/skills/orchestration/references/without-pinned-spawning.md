# Runs without pinned spawning

Delegation uses native pinned spawns exclusively. App or cloud thread tools,
API calls, nested CLIs and other non-native inference workarounds never carry
delegation. Missing audit records alone do not mean spawning is unavailable;
use the [spawn audit](spawn-audit.md) rules for that uncertainty.

## Ask once

When native spawning is unavailable or cannot pin model, reasoning effort and
fresh context together, pause dependent work and ask the user once per run:

> Native pinned spawning is unavailable: <observed reason>. Choose a Parent-only
> run, which has no independent review, or fix the environment to enable native
> pinned spawning.

Keep the choice pending until the user answers. Silence grants neither option.
Retain the answer in the conversation and apply it to later workflow spawn and
review touchpoints; do not repeat the same question at each step.

If the user chooses to fix the environment, keep dependent work paused until
the host exposes working native pinned spawning. Resume the normal plan and
candidate lifecycle once that capability is available. Continued unavailability
leaves the choice pending under that decision, without repeated prompts or
automatic conversion to a Parent-only run.

## Complete a Parent-only run

The user's choice permits the Parent to execute all remaining work itself,
including workflow steps that normally request subagents. Revise the plan report
to record the observed limitation, the user's choice and the Parent as executor;
mark planned execution and review spawns as not run. This run-level exception
replaces delegation by default and required independent reviews, regardless of
Consequence; it does not need a per-piece delegation-cost justification.

Carry the requested workflow through validation, any needed integration check,
candidate creation and corrections, then Acceptance. When the user chose to run
without commits, use the [dirty-tree procedure](dirty-working-tree.md), including
its hash checks and label. The Parent examines the
candidate and evidence itself; those checks do not count as independent Review.
Keep the candidate unchanged at acceptance and resolve all blocking findings,
including any returned before spawning became unavailable.

Run the spawn audit with every subagent already planned or started; use an empty
list when there were none. Keep historical findings and audit outcomes visible.
For remaining reviews that cannot run, report the Parent-only exception instead
of entering a replacement-review spawn loop. Audit uncertainty remains subject
to the existing audit rules.

In the acceptance report, identify the work and reviews performed by the Parent,
the independent reviews not run and the audit's coverage limits. Always include
both labels `Parent-only run` and `no independent review`, even if some earlier
pieces received Review before the environment limitation. Any such earlier
reviews keep their own evidence; they do not establish independent review of
the completed candidate. The Parent's own checks cannot remove these labels.
