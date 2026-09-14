# Issue #3: runtime smoke evidence

Run: 2026-09-14, Codex CLI 0.154.0, multi-agent v2, workspace-write,
network disabled. Source: [issue #3](https://github.com/aliyusufergin/codex-orchestration/issues/3)
and its [parent specification](https://github.com/aliyusufergin/codex-orchestration/issues/1).
Base commit: `260c7468628dce1a51442cdddb1debac7d024c98`.

## Result and limits

The host records are readable in the default sandbox. Two fresh-context pinned
spawns realized `gpt-5.6-luna/low`; a follow-up retained both settings. The Parent
was found through the subagent's `parent_thread_id`, and its one recorded turn
at collection time ran `gpt-6-astra/medium`. No Ultra turn was present.

**The disposable-session prerequisite remains incomplete.** A disposable Git
repository was initialized with `mktemp -d /tmp/codex-issue3-smoke-XXXXXX` followed
by `git init -q <returned-directory>`. All three probe subagents ran their shell
commands there, but native spawning inherits the current session directory and
has no working-directory argument. Both `session_meta.cwd` and `turn_context.cwd`
remained the current project. This is evidence from a real workspace-write
session, not proof of a session launched in a disposable repository. A fresh
user-launched session in that repository must repeat the smoke test before that
prerequisite can be marked complete. No nested Codex CLI or alternative inference
surface was used.

Luna was selected as the cheapest model identified by the specification's routing
baseline. The live model cache fetched at `2026-09-14T06:56:46.101455662Z` lists
`low` as its lowest supported effort and `medium` as its default. It has no pricing
field, so current relative price was not independently verified.

## Requested and realized settings

The native calls specified `fork_turns: "none"`, `model: "gpt-5.6-luna"`, and
`reasoning_effort: "low"`. Task names were `smoke_a` and `smoke_b`.
A third identically pinned spawn, `review_spec`, deliberately reused a historical
canonical path. It was a collision probe, not the implementation's Spec review.

| Canonical agent path | Creation time (UTC) | Realized model / effort | Result |
| --- | --- | --- | --- |
| `/root/smoke_a` | 2026-09-14T06:57:11.212Z | gpt-5.6-luna / low, both turns | confirmed |
| `/root/smoke_b` | 2026-09-14T06:57:20.810Z | gpt-5.6-luna / low | confirmed |
| `/root/review_spec` | 2026-09-14T06:58:02.627Z | gpt-5.6-luna / low | confirmed |

The spawn responses contained only canonical task names, not realized settings.
Each initial probe used the shell tool's `workdir` set to the disposable repository:

```sh
python3 -c 'import os,sys; print("cwd",os.getcwd()); print("python",sys.version.split()[0]); print("thread",os.environ.get("CODEX_THREAD_ID"))'
```

Redacted output for the first two spawns:

```text
cwd /tmp/disposable-repo
python 3.14.4
thread smoke_a

cwd /tmp/disposable-repo
python 3.14.4
thread smoke_b
```

The native `followup_task` targeted `/root/smoke_a` without any model or effort
arguments. It ran this command in the same disposable directory:

```sh
python3 -c 'import os; print("followup_cwd",os.getcwd()); print("thread",os.environ.get("CODEX_THREAD_ID"))'
```

```text
followup_cwd /tmp/disposable-repo
thread smoke_a
```

The host added a second distinct `turn_context` at
`2026-09-14T06:57:42.406Z`, still `gpt-5.6-luna/low`, to the same subagent file.
The earlier context is at `2026-09-14T06:57:14.136Z`.

## Exact sandbox read and matching probe

The following command was run without escalation. It reads only session metadata
and turn contexts; no conversation text is printed. `CODEX_THREAD_ID` selects this
Parent's children, then the child's recorded parent id locates the Parent record.
The JSON result below is unchanged except for the explanatory aliases in the
separate fixture files.

```sh
python3 - <<'PY'
import json, os
from pathlib import Path

root = Path('/home/dev/.codex/sessions')
start = '2026-09-14T06:57:03'
cwd = '/home/dev/projects/codex-orchestration'
current = os.environ['CODEX_THREAD_ID']
index = []
for path in root.rglob('*.jsonl'):
    with path.open() as stream:
        first = json.loads(next(stream))
    if first.get('type') == 'session_meta':
        index.append((path, first['payload']))

def turns(path):
    result = []
    for line in path.open():
        row = json.loads(line)
        if row.get('type') == 'turn_context':
            p = row['payload']
            result.append({'model': p.get('model'), 'effort': p.get('effort')})
    return result

for task in ('smoke_a', 'smoke_b', 'review_spec'):
    canonical = '/root/' + task
    same_name = [(p, m) for p, m in index if m.get('agent_path') == canonical]
    matches = [(p, m) for p, m in same_name
               if m.get('parent_thread_id') == current
               and m.get('cwd') == cwd and m.get('timestamp', '') >= start]
    print(json.dumps({'task': task, 'same_path_records': len(same_name),
                      'matches': len(matches),
                      'turns': turns(matches[0][0]) if len(matches) == 1 else []}))
    if task == 'smoke_a' and len(matches) == 1:
        parent_id = matches[0][1]['parent_thread_id']
        parents = [(p, m) for p, m in index if m.get('id') == parent_id]
        print(json.dumps({'parent_matches': len(parents),
                          'turns': turns(parents[0][0]) if len(parents) == 1 else []}))
PY
```

```jsonl
{"task": "smoke_a", "same_path_records": 1, "matches": 1, "turns": [{"model": "gpt-5.6-luna", "effort": "low"}, {"model": "gpt-5.6-luna", "effort": "low"}]}
{"parent_matches": 1, "turns": [{"model": "gpt-6-astra", "effort": "medium"}]}
{"task": "smoke_b", "same_path_records": 1, "matches": 1, "turns": [{"model": "gpt-5.6-luna", "effort": "low"}]}
{"task": "review_spec", "same_path_records": 2, "matches": 1, "turns": [{"model": "gpt-5.6-luna", "effort": "low"}]}
```

## Collision evidence and fixture format

[records/review_spec.jsonl](records/review_spec.jsonl) and
[records/historical_review_spec.jsonl](records/historical_review_spec.jsonl)
both record `/root/review_spec`. The historical record was created on September
12 under another Parent and another working directory. The complete tuple of
parent id, canonical path, session directory and creation time selects exactly
one current record. This is a real cross-session/cross-directory collision, not
a fabricated fixture. It does not exercise two simultaneous Parents in the same
directory, nor duplicate task names under the same Parent.

The other samples are [parent](records/parent.jsonl),
[smoke_a](records/smoke_a.jsonl), and [smoke_b](records/smoke_b.jsonl).
They retain only `session_meta` and `turn_context` projections. IDs and paths are
stable aliases across files; timestamps, model/effort, JSON types and retained
field nesting are preserved. Instructions, conversation, tool content, git
metadata, nicknames, and unrelated fields are omitted. These are minimal fixture
seeds, not full host rollouts. The historical file contains an embedded Parent
`session_meta` and inherited turn contexts; it must not be treated as evidence of
a fresh pinned spawn.

## Consequences for the spawn audit

- Read access, Python availability, fresh pinned settings, per-turn effort, and
  follow-up retention are confirmed in this host, not guaranteed across hosts.
- Refuted: a shell command's `workdir` changes the session's recorded directory.
  Match against the session directory; do not substitute a tool's workdir.
- Refuted: `session_id` uniquely identifies a subagent. It equals the Parent id
  in these samples; use the owning `session_meta.id` and `parent_thread_id`.
- Refuted: every `session_meta` inside a rollout describes its owning session.
  The historical sample embeds a Parent record after its own metadata. Preserve
  ownership and inherited-history boundaries rather than selecting the last
  metadata row or attributing every context blindly to the subagent.
- Task name alone is ambiguous across real sessions. Use the full matching tuple,
  and return `unobservable` when identity remains ambiguous or records are absent.
- The Parent lookup and effort read work through its child's parent id. A run
  with no children and Parent effort changes across multiple turns were not
  exercised here; do not infer them from this single Parent turn.
- No requested/realized mismatch was observed. The native spawn response alone
  still supplies no evidence of realization.

## Validation

This ticket adds evidence and fixture seeds, not the future spawn audit command.
The parent specification's live smoke seam applies; there is no new automated
behavior or typechecking target. JSON parsing and a strict field allowlist check
validate the fixture projections. The repository's complete existing suite is
`sh plugins/codex-orchestration/scripts/verify.sh`.
