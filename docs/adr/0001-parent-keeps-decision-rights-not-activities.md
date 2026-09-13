# The Parent keeps decision rights, not activities

Astra Advisor and codex-orchestrator both give the top-level Astra session a list of activities (verification, integration, decomposition) without separating the judgment from the work. We define the Parent's authority as six decision rights (Intent, Architecture, Plan, Scrutiny, Integration and Acceptance) that are never delegated, while any work that feeds them, including discovery, research, design proposals and running checks, can go to a subagent. Whether the Parent does some work itself is then a routing choice, not an exception to its authority.

## Considered Options

- Decision rights plus named activities the Parent always performs itself, such as re-running checks before review: rejected because it duplicates subagent validation and fills the Parent's context with logs.
- Astra Advisor's activity list unchanged: rejected because "delegate bounded work" cannot be stated without exceptions for verification and integration.
