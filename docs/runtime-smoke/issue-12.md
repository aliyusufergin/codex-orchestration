# Issue #12: Runs without pinned spawning

Manual smoke scenarios for the
[startup check](../../plugins/codex-orchestration/skills/orchestration/SKILL.md)
and [Parent-only procedure](../../plugins/codex-orchestration/skills/orchestration/references/without-pinned-spawning.md).
These are expected results, not recorded live runs. This implementation session
exposes native spawning and cannot remove that tool or change its schema.
Run the unavailable-tool cases in a disposable Codex session configured by the
host; do not use a non-native inference workaround to simulate them.

Use a small file-change task with validation and a workflow requesting parallel
review axes. Record the conversation, tool calls, candidate and acceptance report.

| Host condition / user response | Expected behavior |
| --- | --- |
| Multi-agent disabled; no response yet | One question offers Parent-only execution or fixing the environment; dependent work stays paused. |
| Multi-agent disabled; choose Parent-only | Parent completes the task, validation, candidate and own checks; workflow review touchpoints cause no repeat question or spawn. Acceptance includes `Parent-only run` and `no independent review`. |
| Native spawn schema cannot set model or effort; choose Parent-only | Same completion path; no unpinned spawn or alternate delegation tool call. |
| Choose to fix the environment; it remains unavailable | Dependent work stays paused; no automatic Parent-only execution and no repeated question. |
| Restore native pinned spawning after choosing to fix it | Normal planned pinned spawns and candidate lifecycle resume. |
| Spawning becomes unavailable before required review; choose Parent-only | Parent finishes checks and resolves findings; unavailable replacement reviews do not loop. Audit retains prior subagents and acceptance carries both labels. |
| Native capacity is full, but pinning works | Existing capacity-wait procedure applies; no Parent-only question. |
| Parent model is identified as other than GPT-6 Astra, pinning works | One model note; normal orchestration continues across later turns with unchanged Parent settings. |
| Other Parent model and multi-agent disabled | Model note and availability question each occur once; the user's availability choice controls continuation. |

Inspect all cases for absence of app/cloud thread delegation, API inference,
nested inference CLIs and other non-native workarounds. Parent-only checks must
never be reported as independent review. No automated prose assertions are
added, following the parent specification's testing decisions.
