# Issue #14: installed-plugin release smoke

Completed on 2026-09-16 using the [release checklist](../../release-smoke-checklist.md).
The disposable repair passed Validation and fresh Review, both pinned spawns
realized their requested settings, and the candidate remained unchanged.
**The release result has an audit gap**, filed as
[issue #15](https://github.com/aliyusufergin/codex-orchestration/issues/15): the
audit omitted the Parent turn already active at the recorded run start.
This qualifies the smoke Parent's own “smoke passed” completion message.

## Environment and installation

- Plugin source: `f24bcdc43697b729e1c6b7f1de1eb2c495e91ec5`, version `0.2.0`.
  The #14 changes are documentation and evidence; plugin files were unchanged.
- Codex CLI: `0.154.0`; Python: `3.14.4`.
- Installed from the checkout's local marketplace, the README's unpublished
  candidate path. Registration returned marketplace `codex-orchestration`, root
  `/home/dev/projects/codex-orchestration`, `alreadyAdded: false`.
- Installation returned `codex-orchestration@codex-orchestration`, version
  `0.2.0`, cache `/home/dev/.codex/plugins/cache/codex-orchestration/codex-orchestration/0.2.0`.
  All 22 source package files matched the installed files byte for byte.
- Fresh owning session directory: `/tmp/codex-issue14-74o2zfxo/repair`.
  Evidence was written to the sibling `evidence` directory, outside Git.
- Parent thread: `01a0a851-0923-7893-8c0c-dcb4a2863055`.
  Its recorded sandbox was `workspace-write`, network disabled, with the
  evidence directory additionally writable. Local record reads needed no
  escalation. Git writes used an approved escalation after the sandbox denied
  `.git/index.lock`; the commit then succeeded.

The outer implementation session launched fresh `codex exec` sessions as the
system under test, each with its own actual working root. Delegation **inside**
the smoke used native `spawn_agent`; the CLI was not a replacement delegation
surface for the plugin. The smoke used the existing Parent model and effort
configuration. This records the tested settings without recommending them.

## Checklist results

Each row corresponds to a checkbox in the release checklist, in order.

| Section / check | Result and evidence |
| --- | --- |
| 1 / Versions and package check | Pass. Versions above; source verifier passed all package checks and 22 tests, exit 0. No configured typechecker. |
| 1 / Installation | Pass via local marketplace; registration, cache identity and byte comparison above. Git marketplace download was not tested. |
| 1 / Disposable task | Pass. Copied the source audit command, seeded only its invalid-input return status as 0, committed it, and began with a clean tree. |
| 1 / Fresh session | Pass. Owning Parent and both subagent records have the disposable cwd; see the retained record projections below. |
| 2 / Non-invoked control | Pass. Separate clean repository and fresh thread `01a0a850-7f3a-70c2-8158-e9f4728520cb`; prompt “Read hello.txt and report its contents. Do not change any files.” The only command was `cat hello.txt`; response was `release control`. No orchestration skill read or spawn appeared. CLI exited 0. |
| 2 / Explicit invocation | Pass. [Exact prompt](invocation.txt); first command read the installed namespaced skill. CLI exited 0. |
| 2 / Plan | Pass. Plan report preceded the first native spawn and recorded base, clean starting state, scopes, dependencies, Consequence, settings, reasons and review requirement; see [reports](reports.md). |
| 3 / Pinned calls | Pass. Both [native spawn calls](spawn-calls.json) explicitly supplied model, effort and `fork_turns: none`; [returned task paths](spawn-requests.json) match the plan. |
| 3 / Runtime assumptions | Pass. Python and ordinary sandbox record reads worked; live matching uniquely identified both tasks by Parent, path, cwd and time. |
| 3 / Validation | Pass. Regression exited 1 before repair (`0 != 1`) and 0 after repair (one test passed). Direct malformed-input result changed from exit 0 to exit 1, preserving the JSON error. [Validation evidence](validation.md). Integration check unnecessary for one change. |
| 3 / Candidate | Pass. Parent committed the complete repair and test on `smoke` before spawning review; comparison and [patch](candidate.patch) below. |
| 3 / Reviewer preservation | Pass. Fresh reviewer reported no findings and independently reran the regression. HEAD, branch, index, working files and untracked status were unchanged before/after review and at Acceptance; [state observations](candidate-state.json). No sandbox isolation claim is made. |
| 4 / Live audit command | Pass. Installed command read live host records; [input](spawn-audit-input.json), [output](spawn-audit-output.json), exit 0, empty stderr. |
| 4 / Audit coverage | Partial: both subagent settings confirmed; the audit reported no unplanned subagents, host approval records or record errors. Parent effort and Ultra result unobservable, filed as [#15](https://github.com/aliyusufergin/codex-orchestration/issues/15). A host guardian session did run during this run, but it was created 24 s before the recorded start, so the audit did not report it; filed as [#16](https://github.com/aliyusufergin/codex-orchestration/issues/16). |
| 4 / Acceptance report | Pass for the disposable repair. [Retained report](reports.md) includes candidate, evidence, review, integration-check reason, audit gap and labels (`none`). Its release-pass claim is qualified above. |
| 5 / Retention | Pass. Reports, invocation, Validation, Review, patch, state observations, spawn calls, audit and metadata projections are retained here. Private raw transcripts are excluded. |
| 5 / Publication | Results and failure issue are recorded on [#14](https://github.com/aliyusufergin/codex-orchestration/issues/14). |

## Base, candidate and review

- Base: `df423f138d7d1ebfea6b5ad0f9d585e5363593c2`.
- Candidate: `a6ab201af56819302f82404eaf3bd53210e43540`.
- Branch: `smoke` throughout.
- Review comparison:

  ```sh
  git diff df423f138d7d1ebfea6b5ad0f9d585e5363593c2...a6ab201af56819302f82404eaf3bd53210e43540
  ```

The [candidate patch](candidate.patch) contains the one-line repair and a
28-line standard-library subprocess regression. It is disposable smoke code,
not a change to the shipped audit command. There were no corrections, review
skips or user preference exceptions. The review noted that separately testing
structurally valid but invalid request data was outside this malformed-JSON
task's coverage.

## Spawn audit and retained records

| Task | Requested | Realized | Result |
| --- | --- | --- | --- |
| `/root/repair_invalid_input` | `gpt-5.6-luna` / `medium` | `gpt-5.6-luna` / `medium` | Confirmed |
| `/root/review_invalid_input` | `gpt-5.6-terra` / `high` | `gpt-5.6-terra` / `high` | Confirmed; meets normal Scrutiny floor |

The installed audit ran with the original plan start `2026-09-16T03:45:02Z`.
Its [unaltered output](spawn-audit-output.json) cites the live record files and
line numbers. The following minimal projections retain only owning metadata
and turn settings, including the sandbox policy; they exclude conversation and
instructions. Their line numbers differ from the live records:

- [Parent](records/parent.jsonl)
- [Repair subagent](records/repair_invalid_input.jsonl)
- [Review subagent](records/review_invalid_input.jsonl)

The Parent projection shows a readable `gpt-6-astra` / `high` turn beginning at
`03:44:43.375Z`, before the plan's recorded start. The audit filtered it out.
This direct observation explains [#15](https://github.com/aliyusufergin/codex-orchestration/issues/15);
it does **not** replace the audit's `unobservable` / `null` results or backdate
the smoke run. The metadata projections reproduce that gap by supplying their
absolute directory as `records_root` with the retained input; they are evidence
from this live run, not a substitute for performing it.

## Coverage limits

This run exercised installation from a local marketplace, invocation, a clean
single-change candidate, native execution and review, and live auditing. It did
not exercise Git marketplace fetching, dirty starts, corrections, unavailable
spawning, high Consequence or every workflow combination. Host-specific behavior
and undocumented record formats require a new live run for another release.
The expected failing regression was deliberately seeded; the only plugin
failure found in this run is the Parent audit coverage gap filed as #15.
