# Codex Orchestration

A fork of Astra Advisor for Codex. A Parent session keeps every decision right and hands bounded work to subagents started with an explicit model and reasoning effort, composing with existing workflows instead of defining its own.

## Language

### Sessions

**Parent**:
The top-level session that holds the decision rights and is the only session that starts subagents.
_Avoid_: Astra (as a role name), orchestrator, root agent

**Subagent**:
An agent session started by the Parent to carry out one piece of work.
_Avoid_: delegate, child agent, descendant, worker, explorer, tester (as role names)

**Pinned spawn**:
Starting a subagent with its model, its reasoning effort and a fresh context all stated explicitly.
_Avoid_: dispatch, delegation call

**Requested settings**:
The model and reasoning effort named in a pinned spawn.

**Realized settings**:
The model and reasoning effort a session actually ran with, as recorded by the host.
_Avoid_: observed settings, actual settings, runtime pin

**Spawn audit**:
The acceptance-time read of the host's session records that compares every subagent's requested and realized settings, surfaces subagents that were not in the plan, and records the Parent's reasoning effort on each turn. Each subagent comes out confirmed, mismatch or unobservable.
_Avoid_: settings check, routing proof

**Parent-only run**:
A run in which pinned spawning is unavailable and the user chose to let the Parent do the work itself; its acceptance is labelled as having no independent review.
_Avoid_: fallback, solo mode

### Decision rights

**Decision right**:
A decision only the Parent may make. Subagents may supply evidence or proposals for it, never the decision itself. There are six: Intent, Architecture, Plan, Scrutiny, Integration and Acceptance.
_Avoid_: Astra-owned work, parent responsibilities

**Intent**:
What the user wants, including the acceptance criteria, any preferences about how the work is routed or checked, and every question put to the user.

**Architecture**:
Interfaces, schemas, trust boundaries and anything that crosses an ownership boundary.

**Plan**:
How work is split, which model and effort each piece gets, who owns what, and in what order it runs.

**Scrutiny**:
How hard a piece of work is checked before acceptance.
_Avoid_: review risk, review level

**Integration**:
Resolving conflicts between the outputs of different subagents.

**Acceptance**:
The Parent's decision that work is done, including the judgment that its evidence is sufficient.
_Avoid_: parent verification (for the judgment), final approval

### Delegation

**Bounded work**:
Work that leaves no decision right open, has acceptance criteria the subagent can check, names a write scope, and fits in one fresh context.
_Avoid_: AFK work, independent task

**Contract**:
The written statement of a piece of bounded work that the Parent hands to a subagent.
_Avoid_: brief, handoff, task message

**Write scope**:
The part of the working directory a subagent may change under its contract.
_Avoid_: allowed paths, file ownership

**Escalation**:
A subagent stopping at the first decision right it meets inside its work and returning the question, the options, its evidence and its work so far to the Parent.
_Avoid_: blocker, contract breach, assumption

**Direct execution**:
The Parent carrying out a piece of bounded work itself, which it does only when briefing and checking a subagent would cost more than the work.
_Avoid_: local work, doing it inline

**Delegation cost**:
What handing a piece of work to a subagent costs beyond the subagent's own work: briefing it, transferring context, checking its result, and the Parent context the exchange consumes.
_Avoid_: handoff cost, handoff tax, coordination overhead

### Routing

**Difficulty**:
How hard a piece of work is to get right on the first attempt, made up of the capability it needs and the reasoning depth it needs.
_Avoid_: risk, complexity, capability class

**Consequence**:
The cost of an error in a piece of work that goes undetected, rated low, normal or high.
_Avoid_: risk, risk tier, severity

**Capability snapshot**:
The dated table of models with their supported reasoning efforts, default effort and relative price. Live host metadata overrides it.
_Avoid_: model table, lanes, routing table

**Starting point**:
The cheapest model in the capability snapshot at its default reasoning effort, where routing a piece of work begins.
_Avoid_: default lane, baseline

**Scrutiny floor**:
The weakest reviewer model and reasoning effort allowed at a Consequence level.
_Avoid_: review baseline, review lane

### Verification

**Validation**:
A subagent running the checks named in its contract and returning the commands and their results as evidence.
_Avoid_: worker testing, self-review

**Integration check**:
A full check of the integrated result, needed only when more than one change has been combined.
_Avoid_: parent verification

**Review**:
A fresh-context subagent's examination of a candidate's diff and evidence, which may re-run checks but never changes the candidate. Its strength is set by Scrutiny.
_Avoid_: code review (names a workflow), independent review

**Base commit**:
The commit the Parent records when a run starts, against which every review of the run compares its candidate.
_Avoid_: starting revision

**Candidate**:
The commit, made by the Parent, that is reviewed and accepted; any change to it makes a new candidate.
_Avoid_: final patch, accumulated diff, working-tree revision

**Finding**:
A problem a review reports in a candidate, with its location, its evidence, and a mark saying whether it is blocking.
_Avoid_: verdict, issue, comment

**Correction**:
Bounded work that resolves blocking findings and so produces a new candidate.
_Avoid_: fix-first, rework

**Follow-up review**:
A review in which the reviewer that raised blocking findings checks only the change made since its review and whether those findings are resolved.
_Avoid_: re-review, delta review

### Reporting

**Plan report**:
The block the Parent shows before its first spawn, giving each piece of work's contract summary, write scope, dependencies, Consequence, model and effort, and any reason for leaving the starting point.
_Avoid_: route declaration, ASTRA ROUTE

**Acceptance report**:
The block the Parent shows at the end, giving the candidate, the validation, integration check and review results, open non-blocking findings, the spawn audit and any labels.
_Avoid_: completion receipt, cost receipt

### Composition

**Workflow**:
An installed skill, from any author, that governs how work is carried out, such as test-first development or code review.
_Avoid_: engineering process, methodology

**Touchpoint**:
A workflow step that would exercise a decision right or start an agent: asking the user, starting a subagent, reviewing or accepting its own work, changing version-control state, or splitting the work.
_Avoid_: collision point, conflict step, checkpoint

## Relationships

- The **Parent** holds all six **Decision rights**.
- **Difficulty** decides the model and effort for a piece of work: the capability it needs picks the model, the reasoning depth it needs picks the effort. **Consequence** decides its **Scrutiny**. Neither stands in for the other.
- Routing begins at the **Starting point** and moves to anything stronger only with a one-line reason; a **Review** never goes below the **Scrutiny floor** for its **Consequence**.
- Every **Subagent** starts from a **Pinned spawn** made by the **Parent**.
- A **Contract** describes one piece of **Bounded work** and names its **Write scope**.
- **Bounded work** goes to a **Subagent** unless it qualifies for **Direct execution**; a **Parent-only run** happens only when no **Pinned spawn** is possible.
- An **Escalation** hands a **Decision right** back to the **Parent**.
- Work passes through **Validation**, an **Integration check** when changes were combined, **Review**, and **Acceptance** of one **Candidate**.
- Only the **Parent** changes version-control state: each **Candidate** is a commit on top of the run's **Base commit**, and every **Review** compares against that **Base commit**.
- A **Review** goes to a **Subagent** that did no work on the **Candidate**.
- A blocking **Finding** keeps a **Candidate** from **Acceptance** until a **Correction** resolves it or a new **Review** overturns it.
- After a **Correction**, normal **Consequence** gets a **Follow-up review** and high **Consequence** gets a new **Review** of the whole **Candidate**.
- The **Parent** resolves a **Workflow**'s **Touchpoints** before handing work to a **Subagent**; a workflow's own review inside a subagent counts as **Validation**.
- The **Spawn audit** compares **Requested settings** with **Realized settings** and feeds the **Acceptance report**.

## Flagged ambiguities

- "Astra" named both the top-level role and a model. Resolved: the role is the **Parent**; Astra names a model only.
- "Risk" meant a general routing rationale in Astra Advisor and error-severity tiers in codex-orchestrator. Resolved: split into **Difficulty** and **Consequence**.
- "Verification" covered both judging whether evidence is sufficient and running checks, and "parent verification" named a separate stage in both fork bases. Resolved: running checks is **Validation** or an **Integration check**; the judgment belongs to **Acceptance**.
- "Handoff" names a portable session document in Matt Pocock's skills. Resolved: the cost of handing work to a subagent is **Delegation cost**, and the written handoff is a **Contract**.
- "Brief" names both a durable agent brief and a checkpoint summary in Matt Pocock's skills. Resolved: this context says **Contract**.
- "AFK" describes work a human need not steer, but here the Parent does the steering. Resolved: **Bounded work**.
- Worker, Explorer, Researcher, Tester and Reviewer were role names in codex-orchestrator. Resolved: there are no roles; a contract's write scope and what it asks the subagent to return say what the subagent does.
- "Mode" and "profile" named economy and balanced policy sets in codex-orchestrator. Resolved: there are no profiles; the user's routing and checking preferences are part of **Intent**.
- "Verdict" named a single ship, fix-first or rethink outcome in both fork bases. Resolved: a **Review** returns **Findings**, and **Acceptance** stays with the **Parent**.
- "Fixed point" is what Matt Pocock's code-review calls the commit a review compares against, and codex-orchestrator tracked uncommitted "revisions". Resolved: this context says **Base commit** and passes it as the fixed point to such workflows, and a **Candidate** is always a commit.
