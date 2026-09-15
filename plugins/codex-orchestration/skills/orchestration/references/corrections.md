# Blocking findings and corrections

Use this loop when a review returns blocking findings. Keep each finding tied to
its reviewer and reviewed candidate, preserving separate review axes. Acceptance
stays blocked until every blocking finding is resolved by a correction and its
required review, or overturned by a new review.

1. **Surface and classify.** Show blocking findings as interim messages with
   their locations and evidence. A finding that challenges the plan or contract
   returns the Parent to replanning: resolve the decision right and update the
   plan and contract before dependent work resumes. A disputed blocking finding
   goes to a new, fresh-context reviewer that did no work on the candidate;
   supply the finding, dispute evidence and whole candidate under the applicable
   Scrutiny. The Parent cannot dismiss the finding itself. Preserve the new
   review's evidence and whether it upholds or overturns the disputed finding.
2. **Contract the correction.** For findings requiring changes, fill the
   [correction contract](contracts.md#correction-contract). By default, send it
   through `collaboration.followup_task` to the canonical task path of the
   subagent that did the work, retaining its context. Choose a stronger model
   only when a finding reveals a capability gap, and record the gap and a
   one-line capability reason in the plan report. Apply the ordinary routing
   rules to effort. A replacement uses a pinned spawn and a self-contained
   contract; record why a replacement was needed. The Parent corrects directly
   only under the skill's direct-execution cost rule, with the reason recorded.
3. **Validate and commit.** Read the correction's changes and validation evidence,
   applying the normal validation and integration-check rules. The Parent commits
   every correction as a new candidate on the current branch, retaining the run's
   original base commit. Record the previous and new candidate SHAs.
4. **Review the new candidate.** Apply the plan's effective Scrutiny, including
   explicit user preferences, and use the [review contract](contracts.md#review-contract):

   - At normal Consequence, and at low Consequence when the work was reviewed,
     use `collaboration.followup_task` with each reviewer whose blocking findings
     are being corrected. Each follow-up review covers the change since that
     reviewer's reviewed candidate and its own blocking findings. Supply that
     SHA, the new candidate, `git diff <previously-reviewed-candidate>..<candidate-commit>`,
     and the correction's validation evidence. Retain the original base SHA as
     context; the follow-up comparison replaces the full-candidate comparison.
   - At high Consequence, use a new, fresh-context reviewer for the whole candidate:
     `git diff <base-commit>...<candidate-commit>`. Apply the floor and
     model-difference rule against every model that worked on it, including
     corrections. Apply this to each required review; keep their findings separate.
   - If a required follow-up reviewer is unavailable or no longer eligible under
     Scrutiny, revise the plan and use a new eligible reviewer on the whole candidate.
     Record the reason; a new context cannot stand in for the same reviewer's
     follow-up. Record any permitted review skip with its reason.

5. **Reassess surviving findings.** If a blocking finding survives a correction,
   reassess the contract, model or plan before another attempt. Record what the
   failed correction revealed and what will change in the next contract or plan;
   route disputes and plan challenges through step 1. Never repeat the same
   attempt or use an automatic stronger-model ladder. Corrections and reviews
   have no numeric budgets: continue until the blocking findings are resolved,
   or report the unresolved decision or external dependency preventing progress.
6. **Return to Acceptance.** Include all correction and review spawns in the
   spawn audit, retaining follow-up turns under their existing task paths.
   Show the [correction history](reports.md#acceptance-report), including disputes
   and reassessments, then apply the skill's unchanged-candidate acceptance check
   to the latest candidate and its required reviews.
