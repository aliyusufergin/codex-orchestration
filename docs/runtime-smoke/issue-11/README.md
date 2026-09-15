# Issue #11: Composing with workflows through touchpoints

Live native-subagent demo on 2026-09-15, audited from `13:27:45Z`, in the owning
session directory `/home/dev/projects/codex-orchestration`. Disposable code ran
in `/tmp/codex-issue11-demo-F0mYML`; a shell working-directory override does not
relocate the session records. This is a controlled composition demo for
[issue #11](https://github.com/aliyusufergin/codex-orchestration/issues/11), using
the [workflow touchpoints reference](../../../plugins/codex-orchestration/skills/orchestration/references/workflows.md).

## Sources and resolved contracts

The Parent read the locally installed `.agents/skills/implement/SKILL.md`,
`.agents/skills/tdd/SKILL.md` (including `tests.md` and `mocking.md`), and
`.agents/skills/code-review/SKILL.md`. These are installed workflow sources,
not bundled plugin workflows. The TDD source SHA-256 was
`cb01f66bebfaa25fa1f88e6b7e769cd9fd9f35b1120b8563749820738814c927`;
the code-review source SHA-256 was
`47f4e52c21694def9c7c11cbfbf891ca35eac7a93e395797515be3c8a409ae50`.

The user-invoked implement flow shaped the Parent's plan. The TDD discipline
source traveled in the implementation contract. The Parent lifted the
code-review workflow's two parallel axes into its own pinned spawns; neither
review subagent executed that workflow's spawning or aggregation steps.

| Touchpoint | Concrete answer sent in contracts |
| --- | --- |
| Test seam / user question | Use the public spawn-audit CLI's JSON stdin/stdout and exit status, already agreed in parent issue #1's Testing Decisions, seam 1. Invoke raw invalid JSON `{`; expect a JSON error and exit 1. The optional proposed arithmetic seam was unused. |
| Agent starts / work split | One TDD slice; after completion and a Parent commit, separate Standards and Spec axes. Each subagent executes only its assigned piece and never starts agents. |
| Own checking / Acceptance | TDD checks return Validation evidence. The Parent commissions separate Review and retains Acceptance. |
| Fixed point / version control | `never commit` and no staging or other version-control changes. Review contracts supply literal base and candidate SHAs and the comparison below. The Parent makes both commits. |

Before the first spawn the Parent reported the tasks, scopes, dependencies and
settings. The host exposed four slots including the Parent. Task names below
have canonical prefix `/root/issue11_`; every spawn explicitly supplied
`fork_turns: "none"`, `model` and `reasoning_effort`.

| Task | Write scope in disposable directory | Dependencies | Requested model / effort |
| --- | --- | --- | --- |
| `tdd` | `spawn-audit.py`, `test_spawn_audit_demo.py` | none | `gpt-5.6-luna` / `medium` |
| `standards` | `none` | completed TDD Validation and candidate commit | `gpt-5.6-terra` / `high` |
| `spec` | `none` | completed TDD Validation and candidate commit | `gpt-5.6-terra` / `high` |

Execution used the starting point. The two reviews used the normal-Consequence
floor: workflow composition errors can cause later agents to bypass the
Parent's decisions. Both review contexts were fresh and had done no work on
the candidate. They ran concurrently. There were no preference exceptions.
No integration check was needed for the demo's single implementation slice.

## Test-first evidence and candidate

The Parent copied the existing spawn-audit command into the disposable
repository and deliberately changed the invalid-input handler to return `0`.
This seeded fault exercises an existing agreed seam; it is not a production
bug claim. The production command was unchanged.

- Disposable base: `f4669064a0cb5202a10da806de389be025316440`.
- Disposable candidate: `c9a17825f3a33525b456e1c3fbb582343c72de48`.
- Parent repository base for the documentation work: `c867a889c490c06c86bb7dc6e23567a998389f1e`.

The subagent read its TDD sources, added one subprocess test first and returned:

| Stage | Command in the disposable directory | Exit and result |
| --- | --- | --- |
| Red, before implementation | `python3 -m unittest -v test_spawn_audit_demo.py` | 1; expected exit 1, got 0 (`1 != 0`) |
| Green, after changing the handler to return 1 | same command | 0; one test passed |
| Syntax validation | `python3 -m py_compile spawn-audit.py test_spawn_audit_demo.py` | 0 |

The Parent read the changes and evidence, then committed the candidate on the
disposable repository's current branch. Both review contracts received:

```sh
git diff f4669064a0cb5202a10da806de389be025316440...c9a17825f3a33525b456e1c3fbb582343c72de48
```

The exact test and repair are retained in [candidate.patch](candidate.patch).
There is no configured typechecker in this Python standard-library project;
syntax validation is reported as such.

## Review axes, side by side

| Standards | Spec |
| --- | --- |
| Findings: none. The test uses the public process interface, no mocks, and independent expected values. No documented-standard breaches or baseline smells found. | Findings: none. The correction returns exit 1 on invalid JSON; the subprocess test uses raw `{` and checks JSON error output. No missing behavior, scope creep or incorrect implementation found. |
| Evidence: examined the committed diff and supplied Validation; HEAD and tracked status unchanged before/after. | Evidence: reran the focused test and syntax validation, and checked whitespace; all passed. HEAD and tracked status unchanged before/after. |
| Limit: relied on the supplied test/compile evidence. | Limit: did not independently reproduce the supplied Red run against the already-fixed candidate. |

Each axis returned separately; the Parent preserved both findings lists and
accepted the disposable candidate with zero blocking or non-blocking findings.
The Parent also confirmed `HEAD` still matched the candidate, with clean index
and tracked working tree. This demo review is separate from the later review of
the repository's documentation candidate.

## Spawn audit

After both demo reviews finished, the Parent ran
`python3 plugins/codex-orchestration/scripts/spawn-audit.py` with JSON stdin:

```json
{
  "start_time": "2026-09-15T13:27:45Z",
  "cwd": "/home/dev/projects/codex-orchestration",
  "planned_subagents": [
    {"task_name": "/root/issue11_tdd", "requested_model": "gpt-5.6-luna", "requested_effort": "medium"},
    {"task_name": "/root/issue11_standards", "requested_model": "gpt-5.6-terra", "requested_effort": "high"},
    {"task_name": "/root/issue11_spec", "requested_model": "gpt-5.6-terra", "requested_effort": "high"}
  ]
}
```

The command exited 0; its complete metadata-only output is retained in
[spawn-audit.json](spawn-audit.json).

| Task | Realized model / effort | Audit status | Effect |
| --- | --- | --- | --- |
| `tdd` | `gpt-5.6-luna` / `medium` | confirmed | Validation retained |
| `standards` | `gpt-5.6-terra` / `high` | confirmed | Meets normal floor; Review counts |
| `spec` | `gpt-5.6-terra` / `high` | confirmed | Meets normal floor; Review counts |

All three Parent calls were pinned, all realized settings matched, and the
audit found no unplanned subagents, host approval sessions or record errors.
No unpinned spawns were observed. Parent effort and whether it ran at Ultra
are `unobservable`: the audit found no unique Parent record with owning turns
inside this run's time window. Requested settings are not used to fill that gap.

This artifact covers the completed disposable demo, before these two review
sessions were continued to inspect the repository implementation. The final
conversation audit includes their later turns as well.

## Coverage limits

This demonstrates a test-first workflow in one subagent and two Parent-spawned
review axes, with literal touchpoint answers, a committed candidate and a live
spawn audit. It does not exercise missing workflow sources, unresolved user
questions, new touchpoints discovered mid-execution or review corrections.
It is not an installation or full-release smoke test. The disposable code is
not shipped in the plugin; no automated tests of instruction prose were added.
