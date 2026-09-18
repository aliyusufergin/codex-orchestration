# Issue #15: Parent boundary replay and release smoke

Completed on 2026-09-18 against source commit
`c52fb326e04d7cc9069d5b0a2bc6a6d49a8e866c`, plugin **0.2.1**. The installed-plugin
smoke passed the repair, review and Parent audit checks. The Parent turn already
open at the recorded start is now observable, with Ultra `false`; both planned
subagents are confirmed. The pre-existing host-guardian coverage limit in
[#16](https://github.com/aliyusufergin/codex-orchestration/issues/16) remains out
of scope. No new release failures were found.

## Environment and installation

[Environment](environment.json): Codex CLI 0.154.0, Python 3.14.4. The
[source verifier](source-verify.txt) passed package checks and all 30 tests,
exit 0. No typechecker is configured. See
[implementation validation and code review](implementation-validation.md).

The README's local-marketplace commands registered this checkout and installed
`codex-orchestration@codex-orchestration` to
`/home/dev/.codex/plugins/cache/codex-orchestration/codex-orchestration/0.2.1`.
Both exited 0. After the review correction, installation was refreshed and all
25 source package files matched the installed files byte for byte, excluding
generated Python caches.

Fresh `codex exec --approve-for-me` sessions used separate actual roots under
`/tmp/codex-issue15-_t6lzls3/`: `control` and `repair`. The repair session additionally
allowed writes to the sibling `evidence` directory. Delegation within the smoke
used native `spawn_agent`. The recorded Parent sandbox was workspace-write;
Python and live-record reads succeeded there. Git commit required an approved
escalation because `.git` was mounted read-only. The outer session launched
Codex as the system under test, retaining the configured Parent model and effort.

## Release checklist observations

Each row follows the [release checklist](../../release-smoke-checklist.md).

| Check | Result and evidence |
| --- | --- |
| Versions and package checks | Pass; source commit, versions and exit statuses above. |
| Local installation | Pass; installation results and byte comparison above. Git marketplace fetching was not exercised. |
| Disposable task | Pass; source audit copied, only invalid-input exit 1 seeded as 0; clean committed base on `smoke`. Evidence stayed outside the repository. |
| Fresh owning session | Pass; Parent `01a0b501-1eb3-7921-b3ed-4247f5e3799b` and both subagents record the repair cwd in their [projections](records/parent.jsonl). |
| Non-invoked control | Pass; [control observation](control.json), fresh thread `01a0b501-6162-7920-ae38-5628c7331d6d`, only `cat hello.txt`, no orchestration load or spawn, exit 0. |
| Explicit invocation | Pass; [prompt](invocation.txt); [first completed command](skill-load.json) loaded the installed skill and references, exit 0. Smoke CLI exited 0. |
| Plan before spawning | Pass; [plan report](plan-report.txt) recorded start `14:52:39Z`, base, branch, clean state, contracts, scopes, dependencies, normal Consequence, settings and scrutiny before the first spawn at `14:53:45.405Z`. |
| Pinned calls | Pass; [native call metadata](spawn-calls.json) supplies explicit model, effort and `fork_turns: none`; [returned task paths](spawn-requests.json) match the plan. Contract text is represented by the plan; encrypted messages and raw transcripts are excluded. |
| Runtime assumptions | Pass; Python and ordinary sandbox reads worked; live evidence uniquely matched both tasks by Parent, path, cwd and creation time. |
| Validation | Pass; [red regression](repair-pre-fix.txt) failed with `0 != 1`; [green regression](validation-post-fix.txt) passed and direct CLI exit became 1 with JSON error and empty stderr. One change needed no integration check. |
| Candidate before review | Pass; Parent committed the full [repair and test](candidate.patch) before review. Base and candidate below. |
| Review and candidate preservation | Pass; fresh [review](review-invalid-input.txt) found no findings and independently reran the regression. [State observations](candidate-state.json) show the same HEAD, clean tracked/index/untracked state and empty diffs before/after review and at Acceptance. No read-only reviewer sandbox is claimed. |
| Live audit | Pass; installed command, [input](spawn-audit-input.json), [output](spawn-audit-output.json), [invocation and exit 0](spawn-audit-invocation.json); stderr empty. These are live results, not fixture results. |
| Audit coverage | Pass for #15; both pins confirmed, review meets normal floor, Parent observable at high, Ultra false, no record errors or unplanned subagents. Pre-start guardian exclusion remains #16. |
| Acceptance | Pass; [original acceptance report](acceptance-report.txt) identifies candidate, validation, review, integration-check reason, audit and labels (`none`). Original observation filenames in that report are consolidated into `candidate-state.json` here. |
| Retention | Pass; metadata projections, invocation, reports, audit JSON, validation, review, state and candidate patch retained here. Projection keys checked before committing. |
| Publication | Evidence committed locally for #15. This implementation request authorizes commits; no push or issue comment was performed. |

## Candidate and live Parent boundary

- Base: `06f58632b5ce58bf84d77c333dff04c99050a119`.
- Candidate: `0d0d377dc2fe05dbb567e8bc639899427f0c525d`, on `smoke` throughout.
- Review comparison: `git diff 06f58632b5ce58bf84d77c333dff04c99050a119...0d0d377dc2fe05dbb567e8bc639899427f0c525d`.
- Repair: `gpt-5.6-luna` / `medium`, confirmed.
- Review: `gpt-5.6-terra` / `high`, confirmed, meets normal Scrutiny floor.

The Parent [projection](records/parent.jsonl) records `task_started` at
`14:52:24.789Z`, its context at `14:52:26.543Z`, and `task_complete` at
`14:58:05.898Z`. The unchanged run start is `14:52:39Z`, inside that turn. The
live audit cites the original context at line 8 and reports `gpt-6-astra` / `high`;
the field-by-field projection has that same context at line 3. The
[repair](records/repair_invalid_input.jsonl) and
[review](records/review_invalid_input.jsonl) projections retain their matching
owning metadata and turn boundaries too.

Host guardian `01a0b501-1f3e-7033-aef7-364d662c68cd` was created at
`14:52:24.782Z`, before the run start, so the unchanged subagent window excludes
it and `host_sessions` is empty. This is the known #16 limit, not evidence that
no host approvals occurred. No backdating was used.

Coverage is one clean-tree release path: installation, explicit invocation,
delegated repair, normal-Consequence review, immutable candidate and live audit.
Dirty starts, corrections within the smoke, unavailable spawning, high
Consequence and other host formats were not exercised. The deliberately seeded
exit-status failure is the smoke task, not a shipped plugin defect.

## Replay of issue #14

The [retained input](../issue-14/spawn-audit-input.json) keeps its original
`2026-09-16T03:45:02Z` start, cwd, Parent identity and planned settings. The
[replay input](replay-input.json) adds only `records_root`, pointing to #14's
regenerated metadata projections. Both commands exited 0 with empty stderr.

| Command | Parent | Ultra | Planned subagents |
| --- | --- | --- | --- |
| Before, source `d32f9c5` / plugin 0.2.0 | Unobservable; “No unique Parent record with turns in this run” | `null` | Both confirmed |
| After, plugin 0.2.1 | Observable, `gpt-6-astra` / `high` | `false` | Both confirmed |

The [before output](replay-before.json) and [after output](replay-after.json)
cite the same projections. The start turn's context is at line 3; its
`task_started` event is at line 2 and `task_complete` at line 4, after the run
start. Neither audit has record errors or unplanned subagents. This replay
reproduces #14; it is separate from live release validation.

## Projection privacy

[project-records.py](project-records.py) rebuilds each selected line field by
field using the issue's explicit allowlist. It retains metadata and turn
boundaries, excluding conversation, reasoning, instructions and tool output.
The #14 projections and new fixture seed were rebuilt from the three owning
records under `~/.codex/sessions/2026/09/16/`, identified in the
[fixture provenance](../../../plugins/codex-orchestration/tests/fixtures/README.md).
The original #3 seeds and #14 audit input/output are unchanged.

Before committing, run the allowlist check on every new or regenerated projection:

```sh
python3 docs/runtime-smoke/issue-15/project-records.py --check \
  docs/runtime-smoke/issue-14/records/*.jsonl \
  docs/runtime-smoke/issue-15/records/*.jsonl \
  plugins/codex-orchestration/tests/fixtures/issue-14/*.jsonl
```
