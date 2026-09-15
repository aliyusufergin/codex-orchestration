# Issue #8: Escalations and findings-only work

Live native-subagent demo on 2026-09-15 in the implementation session at
`/home/dev/projects/codex-orchestration`, using disposable output directory
`/tmp/codex-issue8-demo-YOOzUL`. This tests the
[escalation and findings-only instructions](../../plugins/codex-orchestration/skills/orchestration/SKILL.md)
and [contracts](../../plugins/codex-orchestration/skills/orchestration/references/contracts.md).
It is a controlled behavior scenario, not a full orchestration or installation
test. Spawns inherited the implementation session's settings; this demo makes
no pinned-spawn or realized-settings claim.

## Architecture fork and continuation

The Parent spawned `/root/issue8_demo` with fresh context and write scope limited
to the disposable `export-example.json`. The contract deliberately left two
export interfaces plausible: a bare array or an object with an `items` array.
It required stopping at the first decision right, returning question, options,
evidence and work so far, and resuming only under an updated contract. It also
included an unresolved audience question for the Parent, with a scenario answer
fixture held by the Parent. Formatting choices stayed with the subagent.

The subagent returned an Architecture escalation with both JSON shape options,
evidence that no consumer interface was established, and `No files written;
validation not run`. It separately identified the audience question as Intent
for the Parent and did not contact the user. Its context marker was
`copper-otter-82`.

The Parent showed the escalation in an interim conversation message, chose the
object envelope, and relayed the fixture answer `internal`. The audience answer
was simulated user input, not a preference supplied by the real user. This
exercises routing to the Parent without making the user answer a disposable
product question; an actual user-response round trip was not tested.

Using `collaboration.followup_task` on `/root/issue8_demo`, the Parent updated
the contract with the selected schema, audience and exact example content,
retaining its write scope and boundaries. The same subagent resumed and returned
the original marker, chose two-space indentation and a trailing newline locally,
and produced:

```json
{
  "audience": "internal",
  "items": [
    {
      "id": "example-1"
    }
  ]
}
```

Validation returned by the subagent:
`python3 -m json.tool /tmp/codex-issue8-demo-YOOzUL/export-example.json`, exit 0.
The Parent inspected the resulting file. The returned canonical task path and
matching marker demonstrate continuation in the same context. Replanning to a
replacement subagent is documented but was not exercised in this demo.

## Findings-only work

In parallel, the Parent commissioned `/root/issue8_research`, write scope `none`,
to identify who owns Architecture and whether research can supply evidence.
The contract required source locations and uncertainty, no file writes or
version-control mutations, and escalation only to the Parent.

It returned findings citing ADR 0001 line 3 and the findings-only contract:
the Parent owns Architecture; research can supply evidence; the Parent makes
the informed decision. It reported no uncertainty and no escalation. Those
findings fed the Parent's decision to retain that authority boundary in the
implementation. No candidate or review was commissioned for the research result.

The Parent did not commission an independent check of these findings: the
question was directly answered by the named local sources. The optional
independent check is documented as a Scrutiny decision using a fresh-context
findings-only contract; it does not trigger another review chain. The required
code review of this issue's committed documentation is separate from review of
the research result.
