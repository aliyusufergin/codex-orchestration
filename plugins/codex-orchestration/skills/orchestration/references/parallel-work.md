# Parallel work

## Plan the contracts together

List all known pieces in the [plan report](reports.md), using their task names
in dependency fields. Resolve missing dependencies and cycles before spawning
affected work. Name the outputs each dependent contract consumes. Include an
integration check when the plan combines more than one change: its scope,
commands, expected results and prerequisite tasks, and whether the Parent or
a subagent runs it.

## Fill the available slots

All agents share the working directory and see edits immediately. Before each
spawn or follow-up, compare its write scope with every active contract's scope.
Directory scopes include their descendants; overlapping paths or patterns count
as overlap. Resolve ambiguous scopes to concrete paths before running them
together. Write scope `none` cannot collide with another writer, but a contract
that reads another task's output still needs a dependency if it requires that
output to be finished.

A task is eligible when every named dependency has finished with the required
outputs and validation evidence, and its write scope overlaps no active work.
A failed or escalated dependency remains unsatisfied until the Parent resolves
it; an early file appearing in the shared directory is not completion. Run
overlapping work serially, choosing in plan order when otherwise eligible.

Start eligible tasks concurrently up to the host's reported available slots.
Account for the Parent and other live sessions according to the host's slot
semantics; use no additional concurrency cap. When capacity is full, keep ready
work queued and wait for the host to make a slot available. A capacity rejection
is a wait condition, not a reason to move the work to direct execution. Recheck
dependencies and scopes as work finishes and fill newly available slots without
waiting for an entire batch to finish.

## Changes and integration

When the plan changes, show an interim message with the changed contracts,
write scopes, dependencies or ordering and the reason. Pause affected work and
resolve any new overlap before resuming it under updated contracts. Ordinary
task completion follows the existing plan; it does not require replanning.

Run the integration check only after all changes it checks have finished and
their validation evidence is available. Keep the checked result stable: wait
for active writers to that result, even when the check itself has write scope
`none`. Return the check's commands, exit statuses and results as evidence for
the candidate and review. The Parent retains the Integration decision right
when outputs conflict and commissions any corrections and renewed checks.
