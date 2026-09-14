# Codex Orchestration

A user-invoked Codex plugin for delegating bounded work to pinned native
subagents, reviewing a committed candidate, and accepting it with evidence.

The plan-to-acceptance path follows the
[glossary](CONTEXT.md) and [design decisions](docs/adr/0003-user-invoked-execution-layer-over-workflows.md)
for a single change at normal Consequence. Further execution paths are being
implemented in subsequent tickets.

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

The skill loads only when explicitly invoked. Its Codex UI metadata sets
`policy.allow_implicit_invocation: false`.

The Parent uses native subagents when the host exposes explicit model and reasoning
effort controls. Requested settings are distinguished from confirmed runtime
settings. See the [skill](plugins/codex-orchestration/skills/orchestration/SKILL.md)
for the execution sequence and its contract, capability and report references.

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

## Attribution

Forked from [Astra Advisor](https://github.com/DannyMac180/astra-advisor) by Daniel
McAteer, importing its Git history through `c72d328` (v0.2.0).
**codex-orchestrator** (`8f559d6`, v0.4.0 unreleased) is a design reference for this
fork; its code is not imported by this package change.

Distributed under the [MIT license](LICENSE), retaining Daniel McAteer's copyright
notice.
