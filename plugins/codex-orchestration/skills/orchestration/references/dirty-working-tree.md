# Starting from a dirty working tree

## Ask once before spawning

At run startup, inspect `git status --porcelain=v1 --untracked-files=all` from
the repository root. Staged changes, unstaged changes and untracked files all
make the tree dirty. Record the starting status alongside the base commit.
Before any subagent starts or task edits begin, ask once per run:

> The working tree contains uncommitted changes: <brief status summary>.
> Set these changes aside for this run, or run without commits?

Reuse an explicit choice already supplied for this run. Otherwise keep the
choice pending until the user answers; silence selects neither option. Retain
the answer in the plan and resolve later workflow commit and review touchpoints
from it. The spawning-availability choice is separate: a Parent-only run uses
the same dirty-tree choice and candidate procedure.

## Set changes aside

The Parent saves the identified starting changes in a recoverable stash,
including untracked files (`git stash push --include-untracked` with a unique
run description). Record its exact object ID and original status in the
conversation. Inspect the saved tracked and untracked contents and confirm the
index and working tree are clean before starting work. If saving fails or leaves
user changes, pause affected work and resolve that condition; do not stage them
into a candidate. A stash does not save dirty submodule contents: preserve those
separately and verify recovery before continuing.

Use the normal committed-candidate lifecycle, staging only the run's changes.
Keep the saved changes aside through every candidate, correction and review.
After the unchanged-candidate Acceptance check, restore the exact saved stash
with `git stash apply --index <saved-object-id>`. Inspect the result against the
starting status, including untracked contents and staging. Keep the stash as a
recovery copy and report its ID and restoration result. If restoration conflicts,
preserve the saved copy and conflict state, report the paths and obtain the
user's direction for conflicts involving their work. Restored user changes are
outside the accepted candidate and must never enter a later candidate commit.

## Run without commits

This choice replaces candidate and correction commits for the entire run,
including workflow commit steps and Parent-only execution. Keep the original
branch and base commit; leave the user's index intact. Neither the Parent nor
any subagent commits, stages, stashes or switches branches in this path.

Before task edits, capture the starting contents as review evidence. Preserve
user changes, identify them separately from the task's changes, and settle any
overlap requiring a user decision before writing. Include the starting evidence
in every review contract so existing user changes are not attributed to the run.
The candidate represents the complete dirty result relative to the base,
including those starting changes; its hash must not cover only the task's paths.

### Capture and identify a candidate

After Validation and any integration check, wait for all writers to finish.
Capture a complete, reproducible evidence bundle outside the working tree.
Use this same recipe for the starting evidence, every candidate and every
unchanged-candidate check:

1. Record the literal base SHA and the current branch and HEAD. Require HEAD to
   equal the base and the branch to equal the starting branch.
2. Capture `git -c core.quotePath=true diff --binary --full-index --no-ext-diff
   --no-textconv --no-renames --ignore-submodules=none <base-commit> --` from the
   repository root, with fixed diff configuration for the run. This is the full
   tracked diff, including staged and unstaged changes in the final contents.
   Also capture the same command with `--cached` to cover the index; a staged
   change cancelled by an unstaged edit must still affect the hash.
3. Enumerate untracked paths with `git ls-files --others --exclude-standard -z`.
   Retain initially untracked paths even if later ignore rules hide them, and
   include any ignored task outputs required for Acceptance. In bytewise path
   order, capture each repository-relative path, its file type and executable
   bit, and its exact bytes (the link target for a symlink). Represent deletions
   explicitly for retained paths. Include binary files and unusual filenames.
4. Compute SHA-256 over the base SHA, both diff byte strings and the ordered
   untracked records, encoding each field as its decimal byte length, a newline,
   then the raw bytes. Record the field order and capture commands with the
   evidence. Record `sha256:<digest>` as the candidate identifier. Timestamps and
   evidence-directory paths are not hash inputs.

Repeat the capture to confirm it is stable before review. Stop on capture errors,
unreadable files or contents the recipe cannot represent, such as dirty nested
repositories or submodules; obtain complete evidence before proceeding. An
incomplete bundle cannot identify a candidate. Keep bundles unchanged and outside
the scanned tree so evidence does not alter its own hash. They are review
artifacts, not orchestration state files.

### Review, corrections and Acceptance

Supply reviewers the literal base SHA, candidate hash, starting evidence, full
tracked diff and untracked records/content explicitly, either inline or as exact
artifact paths accessible to the fresh context. Include the capture recipe and
Validation evidence. Replace commit-based workflow comparisons in the contract;
`git diff <base>...HEAD` cannot show this candidate. Reviewers check the live hash,
HEAD and branch before and after review and return both observations. They leave
all candidate contents, including untracked files and the index, unchanged.

Corrections produce a new captured candidate and hash, retaining earlier bundles.
The [correction loop](corrections.md) still selects follow-up versus whole-candidate
review. A follow-up receives its previously reviewed bundle and hash, the new
bundle and hash, and an explicit content diff between those snapshots, including
untracked changes and index changes. A new whole-candidate review receives the
full new bundle relative to the original base. Record hashes wherever contracts
and correction history ordinarily name candidate SHAs.

Immediately before Acceptance, recapture the live candidate with the same recipe
and compare its hash with the reviewed hash. Confirm branch and HEAD still match
the start and that the index matches the starting evidence. Any mismatch blocks
Acceptance: resolve unexpected movement, capture and validate the new candidate,
and obtain the reviews required by Scrutiny. Apply the hash check even when review
was permissibly skipped or the Parent performed the checks in a Parent-only run.
The [acceptance report](reports.md) carries the hash, evidence paths, before/after
observations and `ran without commits` label, plus any other applicable labels.
