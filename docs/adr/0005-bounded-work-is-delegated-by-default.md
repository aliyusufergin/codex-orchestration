# Bounded work is delegated by default

Codex's own spawn guidance tells the model to keep urgent blocking work and tightly coupled work local and to delegate only sidecar tasks that can run in parallel. Following it would make the Parent, the most expensive model in the session, the default implementer and fill its context with execution detail. We delegate every piece of bounded work, including work on the Parent's critical path. The Parent executes a piece itself only when briefing and checking a subagent would cost more than the work, and records why. When host capacity is full, work waits for a slot instead of moving to the Parent.

## Considered Options

- Weigh delegation against direct execution case by case: rejected because the Parent drifts back to executing work it could hand off.
- The host default of delegating only parallel sidecar work: rejected because it makes the Parent the implementer of everything on the critical path.
