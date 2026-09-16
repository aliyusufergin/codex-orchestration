# Reports from the smoke session

These are retained observations, not plugin instructions. The smoke Parent accepted
the disposable repair. Its claim that the smoke passed is qualified by the
release report: Parent effort coverage was unobservable and is tracked in issue #15.

## Plan report

```text
PLAN REPORT
base commit: df423f138d7d1ebfea6b5ad0f9d585e5363593c2
branch / working directory: smoke / /tmp/codex-issue14-74o2zfxo/repair
run start: 2026-09-16T03:45:02Z
starting tree: clean
saved changes / starting evidence: starting-observations.json; no saved changes needed
native capability: model, reasoning_effort and fork_turns none supported together
Parent model note: host identifies GPT-6; exact variant not independently asserted; settings unchanged
host capacity: 4 total slots; Parent active, 3 available
work:
  repair_invalid_input: Fix invalid-input exit status and add stdlib subprocess CLI regression proving malformed JSON emits JSON error and exits 1; demonstrate failure before repair and pass after.
    write scope: repair/spawn-audit.py, repair/test_spawn_audit.py; evidence/repair-* and evidence/validation-*
    dependencies: none
    Consequence: normal, explicitly requested
    review requirement: required; snapshot and effective floor gpt-5.6-terra / high; no model difference required
    requested settings: gpt-5.6-luna / medium; fork_turns: none
    selection reason: cheapest eligible model at default effort; bounded one-branch repair
    validation: python3 -m unittest discover -s . -p test_spawn_audit.py -v; fail before repair, pass afterward; no typechecker configured
integration check: not needed because only one bounded change is planned
review:
  review_invalid_input: examine complete base...candidate diff and evidence; return located blocking/non-blocking findings and residual risk
    write scope: none
    dependencies: repair_invalid_input validation and Parent candidate commit
    Consequence: normal
    requested settings: gpt-5.6-terra / high; fork_turns: none
    selection reason: exact normal-Consequence scrutiny floor
    independence: fresh context; no candidate work
    second review: not planned
preferences: CLI seam settled; native pinned spawn only; commit current branch; no push; writes only disposable repo and designated evidence; no optional questions
workflow touchpoints: Parent owns split, commit, Review, Acceptance and questions; worker validates public CLI and never starts agents or changes VCS state
 direct execution: no implementation; Parent performs reserved orchestration and evidence collection
```

## Acceptance report

```text
ACCEPTANCE REPORT
base commit: df423f138d7d1ebfea6b5ad0f9d585e5363593c2
candidate: a6ab201af56819302f82404eaf3bd53210e43540
candidate unchanged: before-review-observations.json, after-review-observations.json and acceptance-observations.json each show identical candidate HEAD, smoke branch, clean index/tree/untracked status, empty unstaged/cached diffs, and complete base...candidate diff.
user changes: none; starting tree clean, starting-observations.json retained.
validation: repair agent ran PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p test_spawn_audit.py -v; exit 1 before repair (assertion 0 != 1), exit 0 after (1 test passed). Direct malformed JSON CLI emitted JSON error in both cases; exit 0 before, exit 1 after. Full retained validation results: repair-report.txt. Fresh reviewer independently reran regression (exit 0), direct CLI check (exit 1, JSON error), and git diff --check base...candidate (exit 0). No typechecker configured.
integration check: not needed; one bounded repair including regression.
reviews: /root/review_invalid_input; findings none; complete findings retained separately in review-invalid-input.txt. Residual gap: separate structurally valid but invalid request coverage absent; shared handler and outside requested malformed-syntax regression scope.
review skips: none
second reviews: not run; normal Consequence requires one.
correction history: none
preferences: normal Consequence; pinned native repair Luna/medium and fresh review Terra/high; exact normal review floor met; public CLI seam; committed on current branch, no push; no optional questions or floor exceptions. Repository and designated evidence writes only. Initial VCS write denied by read-only sandbox; authorized escalation succeeded.
open blocking findings: none
open non-blocking findings: none; residual coverage limit noted above.
spawn audit:
  command: python3 /home/dev/.codex/plugins/cache/codex-orchestration/codex-orchestration/0.2.0/scripts/spawn-audit.py < /tmp/codex-issue14-74o2zfxo/evidence/spawn-audit-input.json
  run start: 2026-09-16T03:45:02Z
  session directory: /tmp/codex-issue14-74o2zfxo/repair
  exit status: 0; default host records used for this live Parent session.
  repair_invalid_input: requested gpt-5.6-luna/medium; realized gpt-5.6-luna/medium; confirmed. Source: spawn-audit-output.json planned_subagents[0].evidence (owning rollout line 8, 2026-09-16T03:46:10.357Z). Effect: none.
  review_invalid_input: requested gpt-5.6-terra/high; realized gpt-5.6-terra/high; confirmed. Source: spawn-audit-output.json planned_subagents[1].evidence (owning rollout line 8, 2026-09-16T03:48:52.331Z). Effect: review counts; meets both normal floor dimensions.
  unplanned subagents: none found
  host approval sessions: none found by audit
  record errors: none
  Parent efforts: unobservable; no Parent turns in audit window; audit reports No unique Parent record with turns in this run. Run started mid-turn; do not infer or backdate.
  Parent ran at Ultra: unobservable (audit null)
labels: none
acceptance: ACCEPTED. Required red/green CLI regression, minimal repair, committed unchanged candidate, fresh review without findings, and confirmed native pinned execution/review satisfy the release smoke criteria. Evidence retained in /tmp/codex-issue14-74o2zfxo/evidence.
```

