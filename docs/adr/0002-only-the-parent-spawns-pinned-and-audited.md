# Only the Parent spawns, every spawn is pinned, and acceptance audits the spawns

Codex subagents inherit the spawner's model and reasoning effort unless both are set together with `fork_turns: "none"`, and the host's own tool guidance tells the model not to set them unless the user, AGENTS.md or a skill asks. The spawn result does not report the settings a subagent actually ran with, and the Ultra effort adds automatic task delegation. Local rollouts showed unpinned workflow spawns running as `gpt-6-astra/high`.

So only the Parent starts subagents, always through native `spawn_agent` with an explicit model, reasoning effort and fresh context. Subagents never spawn; a workflow step that wants parallel agents is lifted to the Parent. At acceptance, a spawn audit reads the subagents' rollouts to compare requested and realized settings and to surface subagents that were not in the plan. Through the parent thread id each subagent records, it also reads the Parent's reasoning effort on every turn, and the acceptance report is labelled when the Parent ran at Ultra. The Parent turns of a run are the turn open at the recorded run start plus every later turn: the turn open at the start is the latest one the host records as started at or before it with no recorded end, and its contexts are collected by turn id. The recorded run start itself never moves, because the same value matches subagents. When pinned spawning is unavailable, the Parent stops once and asks the user.

## Considered Options

- Let subagents spawn from pinned slots allocated in their contract (codex-orchestrator): rejected for nested budgets and agents the Parent cannot see.
- Pin only the Parent's direct spawns (Astra Advisor's current gap): rejected because inheritance is a silent fallback.
- Report requested settings only: rejected because one read at acceptance confirms settings and also enforces the spawn rule.
- Refuse to orchestrate while the Parent runs at Ultra: rejected because the Parent's effort is not cheaply observable before the first spawn, so refusal would add a fragile check to every run, while the audit already surfaces unplanned subagents and their output never counts as review.
- Move the recorded run start back to the Parent's turn or session: rejected because the same value bounds subagent matching, so widening it reopens cross-session and cross-directory collisions.
- Add the last turn before the start only when no later turn was found: rejected because a run that plans in one turn and spawns in the next then reports no Ultra although the start turn ran at Ultra.
- Add the last turn before the start by time order alone: rejected because a start time supplied by hand between turns then counts a turn that had already ended.
- Record the active turn at startup from the Parent's own record: rejected because it adds a Plan-step read whose availability inside the running turn is unmeasured, while the same records prove the same fact at acceptance.
- Take the turn identity from the host: no such value has been observed; only the thread id is exposed.

## Consequences

The spawn audit depends on Codex's undocumented rollout format; when it cannot read it, the result is an explicit `unobservable`, never a failure. It reads the host's turn start and end records alongside its turn contexts: when a Parent turn at or before the run start exists and those records cannot establish whether it was still open, the Parent result is unobservable and Ultra stays null, while a readable Ultra turn still counts. A run with no subagents has no Parent effort record. App and cloud thread tools are not delegation surfaces.
