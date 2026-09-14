# Routing starts at the cheapest model and only the scrutiny floor binds

codex-orchestrator encodes capability lanes that fix a model and effort for each class of work and each review risk, and its lane table changed three times in five days; Astra Advisor leaves every choice to judgment. We keep one binding rule and one pattern. A review meets the scrutiny floor for its Consequence level unless an explicit user preference lowers it, because a weak review is the one routing error nothing downstream catches; at high Consequence a review that runs also uses a different model from the one that did the work, since a fresh context gives independence of context but not of errors. Everything else begins at the starting point, the cheapest model in the dated capability snapshot at its default reasoning effort, and moves to a stronger model or a higher effort only with a one-line reason: the capability the work needs picks the model, and the reasoning depth it needs picks the effort. Model names live only in the capability snapshot, which live host metadata overrides.

Issue #6 clarifies that routing and checking preferences in the request or AGENTS.md are Intent. An explicit preference may lower a floor or remove a review; the plan preserves the original Consequence and floor and the acceptance report labels the exception `by user preference`. Model exclusions alone grant neither exception. This preserves the user's control while making weakened checking visible.

## Considered Options

- Judgment only (Astra Advisor): rejected because nothing would stop cost pressure from weakening reviews or expose over-selection.
- A binding floor with no execution anchor: rejected because the largest price step, from the cheapest model to the next, would go unexamined.
- A non-binding start table keyed by kind of work: rejected because classifying work adds a judgment layer and a table that churns with model releases.
- Binding lanes (codex-orchestrator): rejected because lanes fuse model and effort, need a classification step and an override protocol, and change whenever the models do.
