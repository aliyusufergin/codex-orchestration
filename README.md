# Codex Orchestration

A user-invoked Codex plugin for delegating bounded work to pinned native
subagents, reviewing a candidate, and accepting it with evidence.

It adds an execution layer to the workflows you already use, such as test-first
development or code review. The Parent is your top-level session: it makes the
decisions while subagents contribute bounded changes or evidence. A plan report
explains the proposed work; an acceptance report identifies the result and the
evidence behind it.

The [orchestration skill](plugins/codex-orchestration/skills/orchestration/SKILL.md)
is the source of execution rules. The [glossary](CONTEXT.md) explains the terms.

## Install

In a Codex host with plugin support:

```sh
codex plugin marketplace add aliyusufergin/codex-orchestration --ref main
codex plugin add codex-orchestration@codex-orchestration
```

Start a fresh session at your chosen model and supported effort, and invoke:

```text
Use $codex-orchestration:orchestration to plan, build, verify, and review this work.
```

Invoke it alongside your chosen workflow or a concrete task. Installation alone
does not opt subsequent tasks into orchestration.

Use a host with native subagents and explicit model and effort controls, plus
Python 3.10+ for the spawn audit. The audit reads local Codex session records;
its evidence can be unavailable on a different host or after a record-format
change. See the [audit documentation](plugins/codex-orchestration/scripts/spawn-audit.md)
for its evidence and limitations.

## Choosing the Parent's reasoning effort

Lower effort can reduce the time spent reasoning in the Parent; higher effort
gives it more room to think through ambiguous intent, architecture and conflicting
evidence, at a possible cost in latency and reasoning tokens. The useful balance
depends on your task. This project does not recommend a particular level.

Avoid running the Parent at **Ultra**. In the host examined for this project,
Ultra includes automatic task delegation, which can introduce subagents outside
the explicit plan. The rationale and runtime evidence are in
[ADR 0002](docs/adr/0002-only-the-parent-spawns-pinned-and-audited.md).

## Design decisions

The ADRs explain the choices and alternatives:

- [Parent decision rights](docs/adr/0001-parent-keeps-decision-rights-not-activities.md)
- [Pinned spawns and the spawn audit](docs/adr/0002-only-the-parent-spawns-pinned-and-audited.md)
- [Composition with user-invoked workflows](docs/adr/0003-user-invoked-execution-layer-over-workflows.md)
- [Routing and scrutiny](docs/adr/0004-routing-starts-cheap-and-only-the-scrutiny-floor-binds.md)
- [Delegation and its cost](docs/adr/0005-bounded-work-is-delegated-by-default.md)
- [Contracts instead of roles](docs/adr/0006-contracts-carry-properties-not-roles.md)
- [Base commits, candidates and review](docs/adr/0007-candidates-are-parent-commits-before-review.md)

## Update

```sh
codex plugin marketplace upgrade codex-orchestration
codex plugin add codex-orchestration@codex-orchestration
```

Start a new session after updating so it picks up the installed skill.

## Local development

Install this checkout as the marketplace to try changes before publication:

```sh
codex plugin marketplace add /absolute/path/to/codex-orchestration
codex plugin add codex-orchestration@codex-orchestration
```

Run the same package checks used by CI (Python 3.10+ required):

```sh
sh plugins/codex-orchestration/scripts/verify.sh
```

The verifier checks the manifest, marketplace, local Markdown links, license and
attribution, explicit invocation metadata, absence of static role files, and
the capability snapshot as the single source of model names within the skill.
It also runs the JSON command tests for the
[spawn audit](plugins/codex-orchestration/scripts/spawn-audit.md), which compares
planned subagents with the host's session records and reports Parent effort.

Before a release, follow the [release smoke checklist](docs/release-smoke-checklist.md)
in a disposable repository and retain the observed results. Package checks alone
do not establish live host behavior.

## Attribution

Forked from [Astra Advisor](https://github.com/DannyMac180/astra-advisor) by Daniel
McAteer, importing its Git history through `c72d328` (v0.2.0).
**codex-orchestrator** (`8f559d6`, v0.4.0 unreleased) is a design reference for this
fork; its code was not imported. Despite the similar names, **Codex Orchestration**
(this repository and the `codex-orchestration` plugin) and **codex-orchestrator**
are different projects. Astra Advisor is the upstream fork source; this plugin
develops its own design through the ADRs above.

Distributed under the [MIT license](LICENSE), retaining Daniel McAteer's copyright
notice.
