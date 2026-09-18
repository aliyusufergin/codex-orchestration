# Release smoke checklist

Run this against the release candidate in a disposable repository. This checks
live behavior; the package verifier remains the automated check. Use the
[skill](../plugins/codex-orchestration/skills/orchestration/SKILL.md),
[report reference](../plugins/codex-orchestration/skills/orchestration/references/reports.md)
and [spawn audit reference](../plugins/codex-orchestration/skills/orchestration/references/spawn-audit.md)
as the expected behavior, rather than maintaining copies of their rules here.

For each checkbox, retain an observation and mark **pass**, **fail** or
**unobservable**, with evidence. An attempt with missing evidence is not a
confirmed release pass. File every failure as a new GitHub issue, linking its
reproduction and evidence, and link those issues from the run report.

## 1. Install and prepare

- [ ] Record the plugin source commit, manifest version, Codex version, Python
  version and date. Run `sh plugins/codex-orchestration/scripts/verify.sh` in the
  source checkout and retain its exit status.
- [ ] Follow the [README installation instructions](../README.md#install). For
  an unpublished candidate, use the local-marketplace procedure under
  [Local development](../README.md#local-development) and record that choice.
  Retain the marketplace registration and installation results; check the
  installed skill and references match the source being tested.
- [ ] Create a temporary Git repository with a clean initial commit and a small,
  testable repair task. Keep run evidence outside it so evidence files do not
  affect its candidate or clean-tree checks.
- [ ] Start a **fresh Codex session rooted in that repository**, using the
  installed plugin. Record its owning session directory and thread identity.
  A shell tool's `workdir` override in an existing session is not equivalent.
  All delegation inside the test uses the host's native spawn tool.

A reproducible task uses the existing public spawn-audit command seam: copy
`plugins/codex-orchestration/scripts/spawn-audit.py` from the source checkout into
the temporary repository, change only its invalid-input handler's exit status
from `1` to `0`, and commit that seeded fault. Ask for its repair and a subprocess
regression test that supplies malformed JSON, checks the JSON error and expects
exit `1`. This is a deliberately seeded test fault, not a plugin bug.

## 2. Check invocation and planning

- [ ] In a separate fresh control session with the plugin installed, request a
  simple task without naming orchestration. Record whether the orchestration
  skill loaded; then end the control session. Use a separate repository so this
  control does not dirty the smoke task's starting tree.
- [ ] In the smoke session, explicitly invoke
  `$codex-orchestration:orchestration` with the repair task. Retain the invocation
  and evidence that the installed skill was loaded. Request a delegated repair
  and a normal-Consequence review so both execution and review are exercised.
- [ ] Check the plan report against the report reference. Record the report's
  position before the first spawn, the base SHA and branch, starting status,
  task contracts, scopes, dependencies, requested settings and routing reasons.

## 3. Observe execution, candidate and review

- [ ] Retain each native spawn's arguments and returned canonical task path.
  Check its explicit settings and context against the skill's pinned-spawn
  requirements; include any later correction or replacement spawns.
- [ ] Confirm `python3` and session-record reads work inside the ordinary
  workspace-write sandbox. Match real subagents using task path, Parent identity,
  session directory and time; retain ambiguity or access errors as evidence.
- [ ] Retain Validation commands, exit statuses and results. For the seeded
  fault, preserve the failing regression test before repair and passing result
  after repair. Record whether an integration check was needed and its result.
- [ ] Observe the Parent commit on the original branch before review starts.
  Save the base SHA, candidate SHA, candidate diff and review contract's literal
  comparison. Confirm the diff contains the complete repair and test.
- [ ] Retain the review's findings and evidence. Capture `git rev-parse HEAD`,
  `git status --porcelain=v1`, `git diff` and `git diff --cached` immediately
  before and after review and at Acceptance. Check the same candidate, unchanged
  tracked contents and index, and inspect new untracked files. Describe the
  observed state without claiming the reviewer had a read-only sandbox.

## 4. Audit and accept

- [ ] Run the installed [spawn-audit command](../plugins/codex-orchestration/scripts/spawn-audit.md)
  against **live records**. Retain its JSON input, stdout and exit status. Supply
  the owning session's actual directory and start time, and its Parent thread id
  when collecting from another session. Fixture output is not live evidence.
- [ ] Compare every planned subagent's requested and realized model and effort;
  retain the source locations and confirm that eligible reviews meet the planned
  Scrutiny. Include unplanned subagents, host approval sessions, record errors,
  Parent efforts per turn and the Ultra result. If settings are unobservable,
  record the gap without turning it into a confirmed pinning result.
  Check that the Parent turn open at the recorded start is included even if it
  began earlier and ended later; retain its start/end metadata alongside its
  contexts. Keep the original run start for subagent matching. If start/end
  records cannot establish that turn, retain the unobservable boundary reason
  and any readable in-run turns.
- [ ] Check the acceptance report against its reference, including candidate
  identity, Validation, review findings, integration check or reason it was
  unnecessary, audit outcomes and applicable labels. Account for every failure
  or unobservable result before stating the release outcome.

## 5. Retain and publish

- [ ] Save a Markdown run report with the checklist results, environment,
  source/base/candidate SHAs, invocation, plan and acceptance reports, Validation
  and review evidence, and links to failure issues. Retain the disposable
  candidate as a patch and the audit as JSON so `/tmp` cleanup does not erase the
  result. Publish only relevant metadata, never raw private session transcripts.
  Rebuild record projections field by field and check their keys before committing:
  retain only `timestamp`, `type`, `payload` on each line; `session_meta` payloads
  may contain `id`, `timestamp`, `cwd`, `thread_source`, `parent_thread_id`,
  `agent_path`, `source`; `turn_context` payloads may contain `turn_id`,
  `root_turn_id`, `cwd`, `model`, `effort`, `sandbox_policy`; `task_started`,
  `task_complete`, `turn_aborted` event payloads retain only `type`, `turn_id`.
- [ ] Record the completed run on the release ticket, linking the committed
  evidence and every newly filed failure. State coverage limits explicitly.

This is one representative clean-tree release path. The
[runtime smoke records](runtime-smoke/issue-13.md) link the dirty-tree scenarios;
the [unavailable-spawning scenarios](runtime-smoke/issue-12.md) cover the other
startup branch. Run additional scenarios when the release changes those paths.
For a completed example with a filed audit gap, see the
[issue #14 run](runtime-smoke/issue-14/README.md).
