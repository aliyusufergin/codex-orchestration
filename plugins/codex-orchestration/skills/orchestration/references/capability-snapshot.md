# Capability snapshot — 2026-09-14

Read before every plan report. Live host metadata overrides this dated snapshot.
Supported efforts and defaults below come from Codex CLI 0.154.0's model cache,
fetched on 2026-09-14, and the native spawn schema. They are Codex settings;
API defaults can differ. An unavailable model or effort cannot be selected.

| Model | Supported efforts | Default effort | Relative input / output price |
| --- | --- | --- | --- |
| `gpt-5.6-luna` | low, medium, high, xhigh, max | medium | 1× / 1× |
| `gpt-5.6-terra` | low, medium, high, xhigh, max, ultra | medium | 10× / 10× |
| `gpt-5.6-sol` | low, medium, high, xhigh, max, ultra | low | 20× / 16.67× |
| `gpt-6-astra` | low, medium, high, xhigh, max, ultra | low | 50× / 41.67× |
| `gpt-5.5` | low, medium, high, xhigh | medium | 25× / 25× |

The starting point is `gpt-5.6-luna` / `medium`. Ultra is listed where the host
supports it, but is excluded for subagents by the skill's spawn rule.

Relative prices are an API-equivalent routing proxy, not a cost receipt or a
subscription-savings claim. They divide standard uncached input/output rates
for prompts up to 272K tokens by Luna's $0.20/$1.20 per million tokens.
The official model pages, read on the snapshot date, give the underlying rates:
[Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) $0.20/$1.20,
[Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) $2/$12,
[Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) $4/$20,
[Astra](https://developers.openai.com/api/docs/models/gpt-6-astra) $10/$50, and
[GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5) $5/$30.
Sol's prices are promotional, available at least through 2026-11-21.

## Parent model note

If the host identifies the Parent's model as other than GPT-6 Astra
(`gpt-6-astra`), note that once per run and continue normally, keeping its
selected model and reasoning effort. Unknown model identity requires no guess
or confirmation gate.

## Scrutiny floor

These are policy floors from the project specification, not claims from pricing.
Model and effort each have to meet their floor. For review, the ordered model
strength is Luna < Terra < Sol < Astra, and effort is
low < medium < high < xhigh < max. GPT-5.5 is a supported execution option;
this snapshot does not establish its equivalence to a review floor.

| Consequence | Minimum reviewer model | Minimum reviewer effort |
| --- | --- | --- |
| low | `gpt-5.6-luna` | max |
| normal | `gpt-5.6-terra` | high |
| high | `gpt-5.6-sol` | high |
