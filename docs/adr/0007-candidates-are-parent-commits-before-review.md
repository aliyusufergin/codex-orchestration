# Candidates are commits the Parent makes before review

Neither fork base commits: codex-orchestrator tracks an uncommitted working-tree revision, and Astra Advisor says nothing about version control. Matt Pocock's code-review diffs `<fixed-point>...HEAD`, which never sees uncommitted changes, and every subagent shares one working directory. So the Parent records a base commit when a run starts, commits the integrated change on the current branch before review, and treats that commit as the candidate. Each correction is a new commit, every review compares against the base commit, and acceptance checks that the candidate's SHA did not move during review. Subagents never change version-control state. If the working tree already holds uncommitted user changes when the run starts, the Parent asks once whether to set them aside first or to run without commits, tracking the candidate by a diff hash. Squashing the run's commits is left to the user's flow.

## Considered Options

- An uncommitted candidate identified by a diff hash, committed only after acceptance: rejected as the default because review workflows that diff commits would need special instructions in every contract; kept as the fallback for a dirty starting tree.
- A dedicated work branch per run: rejected because switching branches in a shared working directory is risky while the user has uncommitted changes.
