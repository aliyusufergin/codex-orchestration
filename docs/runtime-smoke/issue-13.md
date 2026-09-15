# Issue #13: Starting from a dirty working tree

Smoke coverage for the
[dirty-tree procedure](../../plugins/codex-orchestration/skills/orchestration/references/dirty-working-tree.md).
The Git-mechanics results below were observed in a disposable repository. The
conversation scenarios are a manual checklist, not recorded live Codex runs.

## Observed Git mechanics

On 2026-09-15, a disposable repository contained `tracked.txt` with different
staged and unstaged user edits, plus an untracked `user notes.txt`.

- `git stash push --include-untracked` saved all three kinds of changes and left
  a clean tree. `git stash show --include-untracked --stat` included both files.
- A candidate modifying only `task.txt` was committed. Comparing it with the
  base listed only `task.txt`; user changes were outside the candidate.
- `git stash apply --index <saved-object-id>` restored `MM tracked.txt` and the
  untracked file. Reading the index, working file and untracked file confirmed
  their respective original contents. The stash was retained.
- Starting the no-commit probe from that restored dirty tree, an independent
  standard-library Python probe captured the documented length-prefixed fields:
  base, full binary diff, cached binary diff, then sorted untracked records
  (path, type, executable bit, bytes). It wrote no repository files or index.
  The starting hash differed after a task edit and a new untracked output.
  Two consecutive captures of the candidate produced the same hash:
  `790aebdd2b4e305dbaa475ad8c6e113c7c8d87d2ca2db035e53a710f3c7be32c`.
- Editing only the untracked output changed the hash to
  `82220ff524db82d1857a9221b8d3582ab86e0cd4ae64a558ddc5db23d4ceece9`.
  HEAD remained `9a23d19915e56966063ed897cb2efe59418e2855`, and the index retained
  only the user's staged edit. This exercises the data used by the Acceptance
  gate, not a live Parent's response to it.
- Restoring `tracked.txt`'s working contents to its base contents made its full
  diff empty while its cached diff still contained the staged user edit. The
  candidate recipe includes that cached diff so this state is represented.

The probe was temporary validation tooling, not a new installed helper or a test
of instruction wording. There is no configured typechecker for these Markdown
changes. Run the existing package verifier and spawn-audit suite as usual.

## Live conversation checklist

Use a disposable repository with staged, unstaged and untracked user changes,
then invoke orchestration with an implementation workflow. Record conversation,
tool calls, review contracts, evidence artifacts and the acceptance report.

| Scenario | Expected behavior |
| --- | --- |
| Dirty start, answer pending | One choice appears before task edits or any subagent; work waits for the answer. |
| Choice already explicit in the invocation | It is recorded and applied without repeating the question. |
| Choose set aside | User changes are recoverably saved; all candidates and corrections exclude them; restoration preserves staging and contents. |
| Saving fails or dirty submodule remains | Work pauses before spawning; remaining changes never enter a candidate. |
| Restoring conflicts with accepted work | Saved copy and conflict state remain; report names affected paths and requests direction; no commit includes restored work. |
| Choose without commits; workflow asks to commit and diff HEAD | No commit or staging occurs; every review axis receives the explicit full diff, untracked content, starting evidence and hash. |
| New binary file, executable change, symlink or unusual filename | Hash covers its path, type, executable bit and exact content; repeat captures are stable. |
| Staged change cancelled by working edit | Cached diff remains part of the candidate identity. |
| An initially untracked file becomes ignored | Its contents remain in the captured evidence and hash. |
| Tracked or untracked content changes during review | Recaptured hash differs; Acceptance waits for a new candidate and applicable review. |
| HEAD, branch or user's index changes unexpectedly | Acceptance pauses despite otherwise passing review. |
| Blocking findings cause a correction | A new hash and retained bundle replace a new commit; normal follow-up receives explicit changes since its reviewed snapshot; high Consequence gets full review. |
| Review skip or Parent-only run combined with no commits | Hash check still runs; report includes `ran without commits` and the other applicable labels. |
| Clean starting tree | No dirty-tree question; normal committed-candidate lifecycle. |

No automated prose assertions are added, following the parent specification's
testing decisions. These scenarios still require a live Codex smoke run before
release to establish that the instructions produce the expected conversation.
