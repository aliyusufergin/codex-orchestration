# Validation and review evidence

## Repair Validation

```text
Repair report: spawn-audit.py invalid-input exit status

Changed files:
- /tmp/codex-issue14-74o2zfxo/repair/spawn-audit.py
- /tmp/codex-issue14-74o2zfxo/repair/test_spawn_audit.py

Regression command (before repair)
Command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p test_spawn_audit.py -v
Exit status: 1
Output:
test_malformed_json_emits_error_and_exits_one (test_spawn_audit.SpawnAuditCliTests.test_malformed_json_emits_error_and_exits_one) ... FAIL

======================================================================
FAIL: test_malformed_json_emits_error_and_exits_one (test_spawn_audit.SpawnAuditCliTests.test_malformed_json_emits_error_and_exits_one)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/codex-issue14-74o2zfxo/repair/test_spawn_audit.py", line 22, in test_malformed_json_emits_error_and_exits_one
    self.assertEqual(result.returncode, 1, result)
AssertionError: 0 != 1 : CompletedProcess(returncode=0, stdout='{"error": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"}\\n', stderr='')

----------------------------------------------------------------------
Ran 1 test in 0.049s

FAILED (failures=1)

Regression command (after repair)
Command: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p test_spawn_audit.py -v
Exit status: 0
Output:
test_malformed_json_emits_error_and_exits_one (test_spawn_audit.SpawnAuditCliTests.test_malformed_json_emits_error_and_exits_one) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.053s

OK

Malformed CLI direct run (before repair)
Input: {malformed\\n
Stdout: {"error": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"}
Stderr: (empty)
Exit status: 0

Malformed CLI direct run (after repair)
Input: {malformed\\n
Stdout: {"error": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"}
Stderr: (empty)
Exit status: 1

Result: malformed JSON emits parseable JSON with a nonempty error and exits 1.
```

## Fresh Review

```text
Fresh review: /root/review_invalid_input
Base: df423f138d7d1ebfea6b5ad0f9d585e5363593c2
Candidate: a6ab201af56819302f82404eaf3bd53210e43540
Requested: gpt-5.6-terra / high, fork_turns none; normal Consequence floor.
Findings: none (no blocking or non-blocking defects found).
Whole base...candidate diff inspected. Error response preserved and invalid JSON/validation error handler exits 1. Subprocess regression checks public CLI return code and parseable JSON with nonempty error.
Reviewer validation:
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s . -p test_spawn_audit.py -v: exit 0, 1 test passed.
Independent direct CLI malformed JSON check: exit 1, parseable JSON error, empty stderr.
git diff --check df423f138d7d1ebfea6b5ad0f9d585e5363593c2...a6ab201af56819302f82404eaf3bd53210e43540: exit 0.
Reviewer before AND after observations: git rev-parse HEAD = a6ab201af56819302f82404eaf3bd53210e43540; git status --porcelain=v1 --untracked-files=all empty; git diff empty; git diff --cached empty.
Before/after repair evidence inspected: same regression failed with CLI status 0 before source repair, passed afterward; direct CLI status 0 -> 1 and same parseable error.
Residual evidence gap: regression specifically covers malformed JSON syntax; no separate structurally valid JSON rejection test. Shared changed exception handler; non-blocking for stated criteria.
```

