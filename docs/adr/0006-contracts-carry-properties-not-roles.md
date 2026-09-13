# Contracts carry properties, not roles

codex-orchestrator defines logical Explorer, Researcher, Worker, Tester and Reviewer roles with combination rules and a validator, and Codex offers native agent roles through `agent_type` whose role files can fix a model and reasoning effort that "cannot be changed". We use neither. A contract states a write scope (none, or specific paths) and what the subagent returns: changes with validation evidence, findings, or a review result. The one rule a role name used to carry stays as a sentence: a review goes to a subagent that did no work on the candidate. Task names may describe the work but carry no rules.

## Considered Options

- A single Reviewer role: rejected because the reviewer's constraints already fit in its contract and that one rule.
- codex-orchestrator's five logical roles: rejected because their combination exceptions and validation code repeat what contract fields already say.
- Codex native roles: rejected because role files can pin model and effort outside routing.
