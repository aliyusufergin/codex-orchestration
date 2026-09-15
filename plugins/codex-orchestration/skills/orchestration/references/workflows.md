# Workflows

## Read the source and resolve touchpoints

Use this reference while planning a user-invoked flow and before handing any
workflow to a subagent. Read the installed workflow's own `SKILL.md` and the
instructions it requires, including skills reached by later steps. Resolve
paths from the installed skill, not from a presumed author or repository layout.
If required instructions are unavailable, obtain the source through the Parent
before starting dependent work.

User-invoked flow skills shape the Parent's plan: preserve their order,
dependencies and completion criteria. Model-invoked discipline skills travel in
the contract as concrete source paths to read and use. Keep their instructions
at the source; the fork ships neither workflow summaries nor per-workflow
adapters. Read the applicable source again when it changes or new work reaches
instructions not previously examined.

Find each step that asks the user, starts agents, reviews or accepts its own
work, changes version-control state, or splits work. Also check conditional and
referenced steps. Resolve every such **touchpoint** before the affected spawn:

| Touchpoint | Parent resolution | What reaches the subagent's contract |
| --- | --- | --- |
| Asking the user | Reuse answers and authorization already present in Intent. Ask the user only for a missing decision, keeping dependent work paused until the answer arrives. | The concrete answer and its scope, such as the agreed seams under test and expected examples. Further user questions return through Escalation. |
| Starting agents | Lift the requested pieces into the Parent's plan, each with its own contract, routing, scope and dependencies; start each through a pinned spawn. | The subagent's assigned piece, supplied inputs and where to return results. Never start agents; return any newly discovered spawn request to the Parent. |
| Reviewing or accepting its own work | Classify a workflow's checks and own review inside an executing subagent as Validation. Arrange separate Review when Scrutiny requires it; Acceptance stays with the Parent. | Which checks to perform, the evidence to return, and which review or acceptance steps the Parent handles. A self-review cannot satisfy required Review. |
| Changing version-control state | Have the Parent perform authorized operations at the appropriate plan step. Record the base commit at the start and make the candidate commit before Review, following the candidate lifecycle. | Literal base and candidate SHAs when needed, the exact comparison command, and `never commit` together with the contract's full version-control boundary. Any other requested operation returns to the Parent. |
| Splitting work | Decide the pieces, interfaces, ownership and ordering in the Parent's plan; apply the parallel-work rules to scopes, dependencies and host capacity. | Only the assigned bounded work and its named dependencies. Proposals to change the split return through Escalation. |

Write the answers into the [contract's Workflow field](contracts.md), alongside
the applicable source paths. A pointer to this reference or “touchpoints
resolved” is not an answer. Before spawning, check that a fresh context can
execute its assigned work without asking the user, choosing a split, starting
agents, changing version-control state or deciding Acceptance. If a touchpoint
cannot be resolved from existing Intent, settle it through the Parent first.
New touchpoints discovered during execution use the skill's Escalation procedure
and an updated contract before affected work resumes.

For a run without commits, resolve every version-control and review touchpoint
using the [dirty-tree procedure](dirty-working-tree.md): workflow commit steps
are omitted, candidate hashes replace candidate SHAs, and reviewers receive the
diff and untracked evidence explicitly. Include the concrete artifact paths and
capture recipe in each affected contract. This run-level choice also replaces
the committed-candidate and `HEAD` comparisons in the review steps below.

## Lift parallel review steps

When a workflow requests parallel agents, the Parent reads the requested axes
from that workflow and creates a separate contract and pinned spawn for each.
Use the [parallel-work rules](parallel-work.md) for eligibility and capacity.
For Review, each subagent receives the applicable axis instructions, standards
or spec sources, the same committed candidate and Validation evidence, and a
write scope of `none`. Apply the normal Review independence and Scrutiny rules
to each axis. Each subagent performs only its assigned axis; the workflow's
spawn and aggregation steps remain with the Parent.

Resolve a workflow's fixed-point question with the run's literal base commit
for a whole-candidate review. Supply the exact comparison from the
[review contract](contracts.md); the [correction loop](corrections.md) defines
the comparison for a Follow-up review. A workflow that compares against `HEAD`
must see the recorded candidate there, with no candidate edits during Review.

Report each axis side by side as its own findings list in the
[acceptance report](reports.md). Preserve its locations, evidence, blocking
marks and residual risk; do not merge findings into a single verdict or rank
one axis against another. Apply the spawn audit and resolve blocking findings
before the Parent decides Acceptance.
