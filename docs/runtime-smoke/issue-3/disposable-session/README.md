# Issue #3: disposable-session completion

Fresh run on 2026-09-14, Codex CLI 0.154.0, native multi-agent v2.
This supplements [the historical run](../README.md) and its
[published evidence](https://github.com/aliyusufergin/codex-orchestration/issues/3#issuecomment-5660256452).
The review base remains `260c7468628dce1a51442cdddb1debac7d024c98`;
the preceding evidence candidate was `ac32e9ef91e018b687c09f3df4a24f61cc3521cc`.

## Result

The disposable-session prerequisite is now confirmed: the Parent's owning
`session_meta.cwd` and all current probe `turn_context.cwd` values equal the
session's disposable repository. The shell `pwd` independently returned that
same directory. Public samples alias it as `/tmp/disposable-repo`.
All recorded current turns use `workspace-write` with network disabled.
The record read below required no escalation; GitHub network operations and
writes to the original checkout use the host's separate approval mechanism.

Both probes used native `spawn_agent` with `fork_turns: "none"`,
`model: "gpt-5.6-luna"`, `reasoning_effort: "low"`, and task names
`smoke_a` and `smoke_b`. Write scope: none; no subagent spawning or git changes.
They ran without shell working-directory overrides:

```sh
python3 -c 'import os,sys; print("cwd",os.getcwd()); print("python",sys.version.split()[0])'
```

Each returned (directory redacted):

```text
cwd /tmp/disposable-repo
python 3.14.4
```

Native `followup_task` targeted `/root/smoke_a` with no model/effort arguments:

```sh
python3 -c 'import os; print("followup_cwd",os.getcwd())'
```

```text
followup_cwd /tmp/disposable-repo
```

| Probe | Requested | Realized | Result |
| --- | --- | --- | --- |
| smoke_a, initial and follow-up | gpt-5.6-luna / low | gpt-5.6-luna / low on both distinct turns | confirmed |
| smoke_b | gpt-5.6-luna / low | gpt-5.6-luna / low | confirmed |
| Parent, through smoke_a's parent_thread_id | not changed by this task | gpt-6-astra / medium on its one recorded turn | readable; no Ultra observed |

## Cheapest available model and lowest host effort

Checked 2026-09-14 against the five models exposed by this session's native
spawn tool. Standard short-context text input/output USD per million tokens:

| Model | Input | Output |
| --- | ---: | ---: |
| gpt-5.6-luna | 0.20 | 1.20 |
| gpt-5.6-terra | 2 | 12 |
| gpt-5.6-sol | 4 | 20 |
| gpt-5.5 | 5 | 30 |
| gpt-6-astra | 10 | 50 |

Sources opened during this run: [OpenAI model catalog](https://developers.openai.com/api/docs/models),
[Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna), and
[GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5).
Luna is therefore cheapest in this available set under the parent specification's
API-equivalent relative-price proxy. This is not a subscription charge or total
run-cost claim, nor a claim about all models in OpenAI's catalog.

The local host cache `/home/dev/.codex/models_cache.json`, fetched at
`2026-09-14T07:41:57.297934333Z`, lists Luna efforts
`low, medium, high, xhigh, max`, default `medium`, and no price field.
The native spawn tool agrees. Although the API page also lists `none`, that is
not exposed by this host; `low` is its lowest supported effort. This resolves
the earlier price-evidence gap without substituting API effort availability
for native host availability.

## Exact sandbox read and redacted output

The command below was executed from the disposable session with default sandbox
permissions. It selects owning metadata from the first record, matches parent
id + canonical path + cwd + creation time, and follows the child's parent id
back to the Parent. It reads only metadata/turn projections into its output.
The temporary script is a one-off evidence collector, not the future spawn audit
command. The initial collection hit a TypeError sorting a null canonical path;
the corrected command retains that host record explicitly instead of dropping it.

```sh
python3 - <<'PY'
import json, os
from pathlib import Path
root = Path('/home/dev/.codex/sessions')
current = os.environ['CODEX_THREAD_ID']
cwd = os.getcwd()
index = []
for path in root.rglob('*.jsonl'):
    with path.open() as stream:
        row = json.loads(next(stream))
    if row.get('type') == 'session_meta':
        index.append((path, row['payload']))
parent = [(p,m) for p,m in index if m.get('id') == current]
assert len(parent) == 1
start = parent[0][1]['timestamp']
selected = {'parent': parent[0]}
summary = []
for task in ('smoke_a', 'smoke_b'):
    same = [(p,m) for p,m in index if m.get('agent_path') == '/root/'+task]
    matches = [(p,m) for p,m in same if m.get('parent_thread_id') == current
               and m.get('cwd') == cwd and m.get('timestamp','') >= start]
    assert len(matches) == 1
    selected[task] = matches[0]
    historical = [(p,m) for p,m in same if m.get('parent_thread_id') != current and m.get('cwd') != cwd]
    assert historical
    if task == 'smoke_a':
        selected['historical_smoke_a'] = max(historical,key=lambda x:x[1]['timestamp'])
        linked = [(p,m) for p,m in index if m.get('id') == matches[0][1]['parent_thread_id']]
        assert linked == parent
    summary.append({'task':task,'same_path_records':len(same),'matches':len(matches)})
aliases = {m['id']:name for name,(p,m) in selected.items()}
aliases[selected['historical_smoke_a'][1]['parent_thread_id']] = 'historical-parent'
turns = {}
def alias(v):
    if v not in aliases: aliases[v] = 'turn-'+str(len(aliases))
    return aliases[v]
for name,(path,meta) in selected.items():
    projected=[]; turns[name]=[]; owning=True
    for line in path.open():
        row=json.loads(line); kind=row.get('type'); p=row.get('payload',{})
        if kind not in ('session_meta','turn_context'): continue
        if kind == 'session_meta':
            if projected: owning=False
            q={k:p[k] for k in ('session_id','id','parent_thread_id','timestamp','cwd','cli_version','thread_source','agent_path','multi_agent_version') if k in p}
            for k in ('session_id','id','parent_thread_id'):
                if k in q: q[k]=alias(q[k])
        else:
            assert owning, 'Inherited history needs separate handling'
            q={k:p[k] for k in ('turn_id','root_turn_id','cwd','model','effort','sandbox_policy') if k in p}
            for k in ('turn_id','root_turn_id'):
                if k in q:q[k]=alias(q[k])
            if 'sandbox_policy' in q:
                q['sandbox_policy']={k:v for k,v in q['sandbox_policy'].items() if k in ('type','network_access','exclude_tmpdir_env_var','exclude_slash_tmp')}
            turns[name].append({'timestamp':row['timestamp'],'model':p.get('model'),'effort':p.get('effort'),'cwd_matches':p.get('cwd')==cwd,'sandbox_policy':q.get('sandbox_policy')})
        if 'cwd' in q:q['cwd']='/tmp/disposable-repo' if q['cwd']==cwd else '/workspace/historical-repo'
        projected.append({'timestamp':row['timestamp'],'type':kind,'payload':q})
    Path('/tmp/issue3-fresh/records/'+name+'.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in projected))
children=[{'agent_path':m.get('agent_path'),'thread_source':m.get('thread_source')} for _,m in index if m.get('parent_thread_id')==current]
result={'parent_matches_through_child':1,'parent_session_cwd_matches':parent[0][1]['cwd']==cwd,'start':start,'matching':summary,'turns':turns,'all_direct_subagents':children}
Path('/tmp/issue3-fresh/probe-output.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
PY
```

```json
{
  "parent_matches_through_child": 1,
  "parent_session_cwd_matches": true,
  "start": "2026-09-14T07:36:02.270Z",
  "matching": [
    {
      "task": "smoke_a",
      "same_path_records": 2,
      "matches": 1
    },
    {
      "task": "smoke_b",
      "same_path_records": 2,
      "matches": 1
    }
  ],
  "turns": {
    "parent": [
      {
        "timestamp": "2026-09-14T07:43:17.597Z",
        "model": "gpt-6-astra",
        "effort": "medium",
        "cwd_matches": true,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      }
    ],
    "smoke_a": [
      {
        "timestamp": "2026-09-14T07:44:24.484Z",
        "model": "gpt-5.6-luna",
        "effort": "low",
        "cwd_matches": true,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      },
      {
        "timestamp": "2026-09-14T07:44:45.191Z",
        "model": "gpt-5.6-luna",
        "effort": "low",
        "cwd_matches": true,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      }
    ],
    "historical_smoke_a": [
      {
        "timestamp": "2026-09-14T06:57:14.136Z",
        "model": "gpt-5.6-luna",
        "effort": "low",
        "cwd_matches": false,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      },
      {
        "timestamp": "2026-09-14T06:57:42.406Z",
        "model": "gpt-5.6-luna",
        "effort": "low",
        "cwd_matches": false,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      }
    ],
    "smoke_b": [
      {
        "timestamp": "2026-09-14T07:44:30.078Z",
        "model": "gpt-5.6-luna",
        "effort": "low",
        "cwd_matches": true,
        "sandbox_policy": {
          "type": "workspace-write",
          "network_access": false,
          "exclude_tmpdir_env_var": false,
          "exclude_slash_tmp": false
        }
      }
    ]
  },
  "all_direct_subagents": [
    {
      "agent_path": "/root/smoke_b",
      "thread_source": "subagent"
    },
    {
      "agent_path": "/root/smoke_a",
      "thread_source": "subagent"
    },
    {
      "agent_path": null,
      "thread_source": "guardian_review"
    }
  ]
}
```

## Fixtures and design consequences

The four files in [records](records/) retain only `session_meta` and
`turn_context` projections. Identifiers use consistent aliases across files;
timestamps, retained JSON types and nesting remain unchanged. No conversation,
instructions, credentials, personal identifiers or raw rollouts are included.
`source` is omitted from these minimal seeds; the earlier seeds retain its shape.

Both task names have two historical/current records, but each complete matching
tuple selects exactly one current record. `historical_smoke_a.jsonl` is a real
record from the earlier Parent in another directory, not a fabricated collision.
It contains both original and follow-up turns. This tests cross-session and
cross-directory reuse, not simultaneous Parents in the same directory.

The earlier refutations remain applicable: shell `workdir` does not relocate a
session; `session_id` is not a unique subagent id; embedded metadata must not
replace owning metadata. Current fresh-context seeds have no inherited metadata;
the collector explicitly refuses to attribute contexts after a second metadata
record. The historical run retains the inherited-history counterexample.

Newly refuted: every record with this `parent_thread_id` necessarily has a
canonical agent path. The host created a `guardian_review` record with null path
and `source.subagent.other = "guardian"`. It is surfaced as host approval
infrastructure, not counted as a planned work subagent or used as independent
review. A future audit must retain and classify such records rather than crash
or silently omit them. No unplanned work subagent was present at collection.

Record access, Python availability, exact realized settings, unambiguous matching,
Parent effort readability and follow-up retention are confirmed for this host.
Missing records or unresolved identity still require `unobservable`; this run
does not establish no-child Parent lookup or multi-turn Parent effort changes.

## Verification and review scope

No runtime implementation or prose tests are added. Validation checks JSON and
strict projection fields; the full repository verifier is
`sh plugins/codex-orchestration/scripts/verify.sh`. Candidate SHA, validation
results, independent Standards/Spec review findings, final spawn audit and
publication readback are recorded in the completion comment on issue #3.
