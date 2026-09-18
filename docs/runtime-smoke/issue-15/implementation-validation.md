# Implementation validation

The agreed seam is the audit command's stdin JSON, stdout JSON and exit status,
as specified in #15. No typechecker is configured. Python compilation and the
package verifier passed.

TDD evidence:

- `test_parent_turn_open_at_start_is_reported_even_when_it_ends_later` failed
  against the original command: `unobservable != observable`. It passed after
  adding the Parent-only boundary path.
- `test_unestablished_start_turn_keeps_readable_later_turns_but_ultra_unknown`
  then failed: `observable != unobservable`. It passed after explicit boundary
  uncertainty handling. The old fixture test now expects unknown Ultra use
  where its historical turn lacks start/end records, as #15 requires.
- Standards review supplied a synthetic ordering counterexample. The new
  `test_start_turn_is_selected_by_start_event_not_context_order` failed:
  `unobservable != observable`. Selecting by host start events exclusively
  resolved it; repeated historical contexts cannot replace the latest start.

The CLI test file passed after each correction. Final source verification at
`c52fb32` ran `sh plugins/codex-orchestration/scripts/verify.sh`: package checks
passed, all 30 tests passed, exit 0. The original issue #3 seeds and the shared
`Session.turns()` helper are unchanged. The six regenerated #14/fixture
projections passed the explicit key allowlist before the implementation commit.

## Standards

Reviewed independently against base `d32f9c5`. The ordering concern was resolved
in `c52fb32` and the reviewer reran its CLI regression successfully. No blocking
findings remain. One non-blocking maintainability suggestion remains: the
Parent path repeats record traversal and error handling. Extraction was deferred
to preserve the shared helper's existing behavior in this focused correction.

## Spec

The separate Spec review found no implementation findings. It verified the CLI
suite, unchanged #3 seeds, all six projections against independent field-by-field
projection of the live originals, exact replay outputs, unchanged Plan step,
and absence of new output fields. Live release evidence is assessed separately
in the [run report](README.md).
