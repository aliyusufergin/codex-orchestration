---
name: orchestration
description: "Delegate bounded work with pinned native subagents, then review and accept a committed candidate."
---

# Codex Orchestration

The user invokes this execution layer alongside their workflow. The top-level
session is the **Parent** and keeps six decision rights:

- **Intent**: the user's desired outcome, acceptance criteria, preferences and questions.
- **Architecture**: interfaces, schemas, trust boundaries and cross-ownership decisions.
- **Plan**: splitting work, routing it, assigning write scopes and ordering dependencies.
- **Scrutiny**: how hard the work is checked.
- **Integration**: resolving conflicts between subagents' outputs.
- **Acceptance**: deciding that the work is done and its evidence sufficient.

Subagents may provide evidence and proposals for these decisions. **Bounded work**
leaves no decision right open, has acceptance criteria the subagent can check,
names a write scope and fits in one fresh context. Delegate bounded work by
default, including work on the Parent's critical path. **Direct execution** is
allowed only when briefing and checking a subagent would cost more than the work;
record that reason in the plan report. When host capacity is full, wait for a slot.

Only the Parent makes **pinned spawns**. This skill explicitly authorises and
requires setting `model`, `reasoning_effort` and `fork_turns: "none"` together on
every native `collaboration.spawn_agent` call. Subagents never start agents,
never use Ultra and never change version-control state. Use contracts rather
than native agent roles. A spawn request records requested settings, not proof
of realized settings. Keep the Parent's model and effort as the user selected.

## From plan to acceptance

1. **Plan.** Record the run's start time, session working directory, current branch
   and `git rev-parse HEAD` as the **base commit**. For a clean starting tree,
   settle Intent and Architecture and identify one piece of bounded work.
   Before every plan report, read the
   [capability snapshot](references/capability-snapshot.md). Live host metadata
   overrides its capabilities and defaults. Routing starts at the cheapest model
   at its default effort: a stronger model needs a one-line capability reason,
   and a higher effort needs a one-line depth reason. **Difficulty** selects
   model and effort; **Consequence**, the cost of an undetected error, selects
   Scrutiny. Apply the Scrutiny and preferences rules below, then show the
   [plan report](references/reports.md) before the first spawn.
2. **Contract and spawn.** Read [contracts](references/contracts.md) and supply all
   fields, including resolved workflow touchpoints, write scope and validation
   commands. Make the planned pinned spawn with a self-contained contract.
   Dependent work starts after its dependency finishes; overlapping write scopes
   run serially.
3. **Validation.** Read the subagent's changes and returned commands and results.
   An **integration check** is needed only when more than one change was combined;
   it can be delegated. If evidence is insufficient, contract the missing check
   to a subagent. The Parent judges sufficiency without re-running checks by default.
4. **Candidate.** The Parent commits the integrated change on the current branch
   and records `git rev-parse HEAD` as the **candidate**. Stage only the run's
   changes. Review begins only after this commit exists.
5. **Review.** Run each review required by the plan's Scrutiny, or record the
   permitted skip and its reason. Send each review contract to a fresh-context
   subagent that did no work on the candidate. Apply the selected floor and
   any explicit user preference; explain stronger selections.
   Give it the base commit, candidate commit and validation evidence. It examines
   `git diff <base-commit>...<candidate-commit>` and returns findings; it changes
   no tracked files. This is a contract constraint, not a claim of sandbox isolation.
6. **Acceptance.** Read the candidate's diff, evidence and review findings.
   Acceptance is blocked while any blocking finding is open. A correction is
   bounded work and makes a new candidate subject to the plan's Scrutiny; direct execution
   uses the same cost exception. Before accepting, confirm `git rev-parse HEAD`
   still equals the reviewed candidate and that the index and working tree have
   no changes to the candidate. Movement or edits invalidate that review for
   acceptance. Show the [acceptance report](references/reports.md) for the
   unchanged candidate, retaining each review's findings separately. For a
   permitted review skip, check the committed candidate and its tracked status
   at acceptance and report the skip instead of claiming a reviewed candidate.

## Scrutiny and preferences

For each piece of work, record its Consequence, the corresponding snapshot floor
and the resulting review requirement in the plan report:

| Consequence | Review requirement |
| --- | --- |
| low | May skip review with a one-line reason, repeated in the acceptance report. If reviewed, meet both the model and effort floor. |
| normal | Review is required at or above both parts of its floor. |
| high | Review is required at or above both parts of its floor, on a different model from the one that did the work. The Parent may add a second independent review. |

For high Consequence, compare the reviewer model with every model that did work
on the piece, including direct execution and corrections. Each additional review
uses a separate fresh-context subagent that did no work on the candidate and
meets the same floor and model-difference rule. Record whether a second review
was run, and preserve its findings separately. A reviewer model or effort above
the applicable floor needs a one-line reason.

Treat routing and checking preferences from the request and applicable AGENTS.md
as Intent. Before selecting settings, translate them into model exclusions,
minimum review settings or explicit exceptions. Start execution routing at the
cheapest eligible model at its default effort; keep capability and depth reasons
for stronger selections. For review, select eligible settings that satisfy both
the Consequence floor and any stronger requested minimum. A request to always
review at the strongest floor requires review for every piece, including low
Consequence, using the strongest model floor and the highest effort floor in
the snapshot. Compare model and effort separately: a stronger model never
compensates for effort below the applicable minimum.

A model exclusion alone permits neither a weaker review nor a skipped review.
If no available settings satisfy the preferences, floor and model-difference
rule together, return the conflict and options to the user before dependent work.
Only an explicit preference to lower a floor or remove a review authorises that
exception. Preserve the original Consequence and floor, record the changed
requirement in the plan, and label each such exception `by user preference` in
the acceptance report with the preference and the review actually run or skipped.
When a high-Consequence review still runs, its model must differ from the
execution models even if the user lowered its floor. A label by itself does not
grant an exception.
