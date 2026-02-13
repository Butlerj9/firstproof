# Scout API Helper

`tools/scout_api.py` is a small OpenAI-compatible CLI for scout-model calls.

## Package archives

- `tools/gpt-pro-final/` — GPT-pro prompt packages, lane packets, and transcripts.
- `tools/claude-research-final/` — Claude Research prompt packages, lane packets, and transcripts.

It supports:
- `groq` (default key env: `GROQ_API_KEY`)
- `moonshot` (default key env: `MOONSHOT_API_KEY`)
- `fireworks` (default key env: `FIREWORKS_API_KEY`)
- `openai_compat` (custom base URL + key env)

It auto-loads `.env` values from:
1. `d:/Projects/loopforge-new/POC9/.env`
2. `d:/Projects/loopforge-new/M0/.env`
3. local `.env` in current working directory

## Quick checks

```bash
python tools/scout_api.py --provider groq --test
python tools/scout_api.py --provider moonshot --test
python tools/scout_api.py --provider groq --list-models
python tools/scout_api.py --provider moonshot --list-models
python tools/scout_api.py --provider fireworks --list-models
```

## Basic usage

```bash
python tools/scout_api.py --provider groq --model qwen/qwen3-32b --prompt "Find a counterexample candidate."
python tools/scout_api.py --provider moonshot --model kimi-k2.5 --prompt "Re-derive identity X from first principles."
python tools/scout_api.py --provider fireworks --model accounts/fireworks/models/kimi-k2-instruct-0905 --prompt "Test prompt"
```

## Custom provider (OpenAI-compatible)

```bash
python tools/scout_api.py \
  --provider openai_compat \
  --base-url https://your-host.example/v1 \
  --api-key-env YOUR_API_KEY_ENV \
  --model your/model-name \
  --prompt "Test prompt"
```

## Notes

- Use `--prompt-file` for long prompts.
- Use `--raw-json` for full response payloads.
- Use `--dry-run` to validate key/base/model resolution without an API call.

## Recommended use cases

- Stuck on a narrow technical point: ask a scout for an independent derivation, then verify locally.
- Adversarial stress testing: query 2-3 models with the same lemma and compare failure modes.
- Model triage before heavy use: run `model_capability_probe.py` and pick the best performer for that task type.

Use sparingly:

- Keep scouts as secondary checks, not primary proof generators.
- For llm-only tracks, avoid web-searching foundational lemmas; rely on local reasoning + controlled experiments.

## Tooling provenance

For a per-problem index of which tool produced discovery vs validation signals, see `RESULTS.md` §8 (Tooling provenance index). Each problem's `audit.md` contains an `## Escalation Ledger` with per-event tool/model/script attribution, and each `transcript.md` has an `## Escalation Events` block mapping events to concrete commands and outputs.

Cross-reference with `CONTAMINATION.md` for any external-source ingestion events.

## Capability probe

`tools/model_capability_probe.py` runs deterministic exact-answer checks across multiple providers.

Example:

```bash
python tools/model_capability_probe.py \
  --model-spec fireworks:accounts/fireworks/models/kimi-k2-instruct-0905 \
  --model-spec groq:openai/gpt-oss-120b \
  --model-spec fireworks:accounts/fireworks/models/deepseek-v3p2 \
  --output tools/model_probe_results.json
```

Notes:
- Defaults: `max_tokens=512`, `timeout=90`, `delay=0.5s`.
- Results include per-question predictions and a scoreboard.
