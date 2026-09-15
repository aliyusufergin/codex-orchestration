# Contracts

Before each spawn, fill these fields with concrete values. A fresh context must
be able to do the work from this contract and its named sources alone.

| Field | Contents |
| --- | --- |
| Objective | Desired behaviour and acceptance criteria the subagent can check. |
| Context | Working directory, source/spec paths, decisions already made and relevant evidence. |
| Write scope | `none`, or specific paths the subagent may change. |
| Dependencies | Named work that must have finished, and the outputs to consume; `none` when independent. |
| Workflow | Discipline skills to read and use, or `none`; resolve their touchpoints before spawning. Include agreed test seams, answers to user questions, the base commit for review workflows and who handles any split or review. |
| Validation | Exact commands, their working directory and expected outcomes; include required typechecking and tests where the project provides them. |
| Return | Changes and paths, each validation command with its exit status and result, unresolved concerns and any question requiring a decision right. |
| Boundaries | Never start agents, use Ultra or change version-control state (including staging, committing, switching branches or creating worktrees). Leave changes within the write scope for the Parent. |
| Escalation | Make local choices within the agreed Architecture and write scope. Stop at the first decision right encountered; return the question, options, evidence and work so far to the Parent. Route every user question through the Parent. Resume only under the Parent's updated contract. |

Before supplying the Workflow field, follow [workflows](workflows.md) to read
the applicable source and resolve every touchpoint into concrete contract answers.

## Findings-only contract

For research or exploration returning only findings, use write scope `none`.
Name the question to investigate, source boundaries and evidence required by
Validation. Return findings with source locations, uncertainty and any escalation;
the Parent makes the decision they inform. Resolve workflow review touchpoints
as findings-only work under the skill's findings-only branch. An independent
check commissioned by the Parent uses this same contract form.

## Review contract

Use the same fields with write scope `none`.

For a run without commits, apply the
[dirty-tree review procedure](dirty-working-tree.md#review-corrections-and-acceptance)
instead of the SHA comparisons and tracked-status checks below. Supply its
candidate hash, explicit diff and untracked evidence, and capture recipe.

Include:

- The exact base and candidate SHAs. For a review of the whole candidate, use
  `git diff <base-commit>...<candidate-commit>` as the comparison command;
  for a follow-up review, use the comparison specified below.
- The originating acceptance criteria, relevant standards, and the validation
  commands and results returned for this candidate.
- The review's Consequence and selected Scrutiny, plus confirmation that this
  subagent did no work on the candidate. Include the snapshot floor, effective
  requirement after preferences, and the reason for any stronger selection.
  At high Consequence, name the execution models and show that this review uses
  a different model; identify whether this is the first or second review.
- The checks it may run. It may inspect and re-run checks but changes no tracked
  files and implements no corrections. Check the candidate SHA and tracked status
  before and after review and return both observations.
- Findings, each with a location (file and line, or the relevant artifact),
  evidence explaining the problem, and an explicit **blocking** or
  **non-blocking** mark. Return `findings: none` if none were found. Always state
  residual risk or evidence gaps. Return findings, not a single acceptance verdict.

The Parent owns Acceptance. Keep separate review axes as separate findings lists.

For a follow-up review, retain these boundaries and supply the comparison and
reviewer-specific findings required by the [correction loop](corrections.md).
Return the disposition of each supplied blocking finding with evidence, plus any
new findings in the reviewed change. A disputed finding's new review also returns
whether it upholds or overturns that finding and why.

## Correction contract

Use the common contract fields, including validation, boundaries and escalation.
For a run without commits, substitute candidate hashes and evidence bundles for
candidate SHAs and apply the [dirty-tree procedure](dirty-working-tree.md) when
creating the corrected candidate; the original base remains a commit SHA.
Include:

- The original work's objective and acceptance criteria, the current candidate
  SHA and the run's base SHA, plus the implementation subagent's canonical task path
  (or the Parent for direct execution).
- The blocking findings to resolve, each tied to its reviewer, reviewed candidate,
  location and evidence. Define the observable outcome that resolves each finding.
- The correction's write scope and dependencies, and any changes to the original
  contract or workflow touchpoints decided by the Parent.
- Any prior correction attempts and review results for these findings, and the
  reassessment that changes this attempt's contract, model or plan.
- The correction's model and effort, routing reasons and Consequence under the
  plan. State whether this is a follow-up, replacement or direct execution.
- Validation commands that check the corrected behaviour and relevant regressions.
  Return the changes and command results, mapping each finding to its correction
  evidence or explaining why it remains unresolved. The Parent makes the new
  candidate commit and arranges the review under the [correction loop](corrections.md).
