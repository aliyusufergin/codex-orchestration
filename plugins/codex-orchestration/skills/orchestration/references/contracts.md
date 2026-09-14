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
| Escalation | Stop at the first decision right encountered; return the question, options, evidence and work so far. The Parent decides how to continue. |

Read an applicable workflow's own instructions before supplying the contract.
Its user questions, agent starts, acceptance decisions, version-control changes
and work splitting are touchpoints for the Parent to resolve. A workflow's
review inside the subagent counts as validation.

## Review contract

Use the same fields with write scope `none`. Include:

- The exact base and candidate SHAs, and
  `git diff <base-commit>...<candidate-commit>` as the comparison command.
- The originating acceptance criteria, relevant standards, and the validation
  commands and results returned for this candidate.
- The review's Consequence and selected Scrutiny, plus confirmation that this
  subagent did no work on the candidate.
- The checks it may run. It may inspect and re-run checks but changes no tracked
  files and implements no corrections. Check the candidate SHA and tracked status
  before and after review and return both observations.
- Findings, each with a location (file and line, or the relevant artifact),
  evidence explaining the problem, and an explicit **blocking** or
  **non-blocking** mark. Return `findings: none` if none were found. Always state
  residual risk or evidence gaps. Return findings, not a single acceptance verdict.

The Parent owns Acceptance. Keep separate review axes as separate findings lists.
