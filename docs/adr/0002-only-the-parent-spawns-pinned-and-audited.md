# Only the Parent spawns, every spawn is pinned, and acceptance audits the spawns

Codex subagents inherit the spawner's model and reasoning effort unless both are set together with `fork_turns: "none"`, and the host's own tool guidance tells the model not to set them unless the user, AGENTS.md or a skill asks. The spawn result does not report the settings a subagent actually ran with, and the Ultra effort adds automatic task delegation. Local rollouts showed unpinned workflow spawns running as `gpt-6-astra/high`.

So only the Parent starts subagents, always through native `spawn_agent` with an explicit model, reasoning effort and fresh context. Subagents never spawn; a workflow step that wants parallel agents is lifted to the Parent. At acceptance, a spawn audit reads the subagents' rollouts to compare requested and realized settings and to surface subagents that were not in the plan. Through the parent thread id each subagent records, it also reads the Parent's reasoning effort on every turn, and the acceptance report is labelled when the Parent ran at Ultra. When pinned spawning is unavailable, the Parent stops once and asks the user.

## Considered Options

- Let subagents spawn from pinned slots allocated in their contract (codex-orchestrator): rejected for nested budgets and agents the Parent cannot see.
- Pin only the Parent's direct spawns (Astra Advisor's current gap): rejected because inheritance is a silent fallback.
- Report requested settings only: rejected because one read at acceptance confirms settings and also enforces the spawn rule.
- Refuse to orchestrate while the Parent runs at Ultra: rejected because the Parent's effort is not cheaply observable before the first spawn, so refusal would add a fragile check to every run, while the audit already surfaces unplanned subagents and their output never counts as review.

## Consequences

The spawn audit depends on Codex's undocumented rollout format; when it cannot read it, the result is an explicit `unobservable`, never a failure. A run with no subagents has no Parent effort record. App and cloud thread tools are not delegation surfaces.
