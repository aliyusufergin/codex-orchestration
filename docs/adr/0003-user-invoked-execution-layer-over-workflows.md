# Orchestration is a user-invoked execution layer over workflows

Workflows such as test-first development or code review ask the user questions, start agents, review and accept their own work, commit, and split work, and neither fork base says how those steps meet orchestration. The orchestration skill is user-invoked, so it layers on top of whatever flow the user started instead of becoming a flow itself.

Workflows run unmodified as the how. Before handing work to a subagent, the Parent reads the workflow's own `SKILL.md`, resolves its touchpoints into the contract, and counts a workflow's review inside a subagent as validation rather than review. User-invoked flow skills shape the Parent's plan; model-invoked discipline skills go into contracts. The fork carries no per-workflow adapters and no summaries of any workflow.

## Considered Options

- Let the workflow win inside the subagent: rejected because its spawns, self-review and commits would bypass routing, scrutiny and integration.
- Ship adapters for known workflows: rejected because it couples the fork to specific authors and goes stale.
- Translate every workflow into contract steps: rejected because it re-implements the workflow and drifts from its source.
- Model-invoked orchestration, as in both fork bases: rejected because it can start delegation unasked and keeps its description in context every turn.
