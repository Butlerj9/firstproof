# Shared Tooling Bundle (Research Mode)
Generated: 2026-02-12 12:52:25 -08:00
Root: D:\firstproof



======================================================================
SOURCE: tools/README.md
======================================================================

# Scout API Helper

`tools/scout_api.py` is a small OpenAI-compatible CLI for scout-model calls.

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



======================================================================
SOURCE: tools/scout_api.py
======================================================================

#!/usr/bin/env python3
"""
Minimal OpenAI-compatible API helper for scout models.

Supports:
- Moonshot/Kimi via https://api.moonshot.cn/v1
- Groq/Qwen via https://api.groq.com/openai/v1
- Any custom OpenAI-compatible host

Examples:
  python tools/scout_api.py --provider groq --test
  python tools/scout_api.py --provider moonshot --test
  python tools/scout_api.py --provider groq --model qwen/qwen3-32b --prompt "Say hello"
  python tools/scout_api.py --provider openai_compat --base-url https://example/v1 \
      --api-key-env MY_KEY --model my-model --prompt "ping"
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import textwrap
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - fallback path
    requests = None  # type: ignore

# Avoid UnicodeEncodeError on Windows code pages when model output contains non-ASCII.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


DEFAULT_ENV_FILES = [
    pathlib.Path(r"d:/Projects/loopforge-new/POC9/.env"),
    pathlib.Path(r"d:/Projects/loopforge-new/M0/.env"),
    pathlib.Path(".env"),
]

PROVIDERS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "default_model": "qwen/qwen3-32b",
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "api_key_env": "FIREWORKS_API_KEY",
        "default_model": "accounts/fireworks/models/qwen3-235b-a22b-instruct-2507",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.ai/v1",
        "api_key_env": "MOONSHOT_API_KEY",
        "default_model": "moonshot-v1-8k",
    },
    "openai_compat": {
        "base_url": "",
        "api_key_env": "OPENAI_API_KEY",
        "default_model": "",
    },
}


def mask_secret(value: str) -> str:
    if not value:
        return "<empty>"
    return f"<set len={len(value)}>"


def parse_env_line(line: str) -> Optional[Tuple[str, str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip().strip("'").strip('"')
    if not key:
        return None
    return key, value


def load_env_files(paths: Iterable[pathlib.Path]) -> List[pathlib.Path]:
    loaded: List[pathlib.Path] = []
    for path in paths:
        if not path.exists():
            continue
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            parsed = parse_env_line(raw)
            if not parsed:
                continue
            key, value = parsed
            # Keep existing shell env variables authoritative.
            if key not in os.environ:
                os.environ[key] = value
        loaded.append(path)
    return loaded


def build_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def http_json(
    method: str,
    url: str,
    headers: Dict[str, str],
    payload: Optional[Dict[str, Any]],
    timeout: int,
) -> Tuple[int, Dict[str, Any], str]:
    if requests is not None:
        try:
            if method.upper() == "GET":
                resp = requests.get(url, headers=headers, timeout=timeout)
            else:
                resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            status = int(resp.status_code)
            text = resp.text or ""
            try:
                parsed = resp.json() if text else {}
            except ValueError:
                parsed = {}
            return status, parsed, text
        except Exception as exc:
            return 0, {}, str(exc)

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url=url, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            status = int(resp.getcode())
            parsed = json.loads(text) if text else {}
            return status, parsed, text
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        parsed: Dict[str, Any]
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {}
        return int(exc.code), parsed, body


def extract_message_text(choice_message: Any) -> str:
    if not isinstance(choice_message, dict):
        return str(choice_message)
    content = choice_message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        if parts:
            return "\n".join(parts)
    return ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenAI-compatible scout API helper (Moonshot/Groq/custom)."
    )
    parser.add_argument(
        "--provider",
        choices=sorted(PROVIDERS.keys()),
        default="groq",
        help="Provider profile to use.",
    )
    parser.add_argument(
        "--env-file",
        action="append",
        default=[],
        help="Optional .env file path (can be repeated).",
    )
    parser.add_argument(
        "--base-url",
        default="",
        help="Override base URL (required for openai_compat unless profile default exists).",
    )
    parser.add_argument(
        "--api-key-env",
        default="",
        help="Environment variable name for API key override.",
    )
    parser.add_argument("--model", default="", help="Model name.")
    parser.add_argument("--system", default="", help="Optional system prompt.")
    parser.add_argument("--prompt", default="", help="User prompt text.")
    parser.add_argument("--prompt-file", default="", help="Path to prompt file.")
    parser.add_argument("--max-tokens", type=int, default=128, help="max_tokens value.")
    parser.add_argument("--temperature", type=float, default=0.2, help="temperature value.")
    parser.add_argument("--reasoning-effort", default="", help="Optional reasoning_effort value.")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds.")
    parser.add_argument("--list-models", action="store_true", help="Call GET /models.")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run a short chat connectivity test prompt.",
    )
    parser.add_argument(
        "--raw-json",
        action="store_true",
        help="Print full JSON payload response.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolved settings and exit without API call.",
    )
    return parser.parse_args()


def resolve_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        prompt_path = pathlib.Path(args.prompt_file)
        return prompt_path.read_text(encoding="utf-8")
    if args.prompt:
        return args.prompt
    if args.test:
        return "Reply with exactly: OK"
    raise ValueError("No prompt provided. Use --prompt, --prompt-file, or --test.")


def main() -> int:
    args = parse_args()

    user_env_files = [pathlib.Path(p) for p in args.env_file]
    env_candidates = user_env_files + DEFAULT_ENV_FILES
    loaded_env_files = load_env_files(env_candidates)

    profile = PROVIDERS[args.provider]
    base_url = args.base_url or profile["base_url"]
    api_key_env = args.api_key_env or profile["api_key_env"]
    model = args.model or profile["default_model"]
    api_key = os.environ.get(api_key_env, "")

    if not base_url:
        print("ERROR: No base URL resolved. Set --base-url.", file=sys.stderr)
        return 2
    if not api_key:
        print(
            f"ERROR: API key not found in env var '{api_key_env}'.",
            file=sys.stderr,
        )
        if loaded_env_files:
            print(
                "Loaded .env files: " + ", ".join(str(p) for p in loaded_env_files),
                file=sys.stderr,
            )
        return 2
    if not model and not args.list_models:
        print("ERROR: No model resolved. Set --model.", file=sys.stderr)
        return 2

    print(f"Provider: {args.provider}")
    print(f"Base URL: {base_url}")
    print(f"API key env: {api_key_env} ({mask_secret(api_key)})")
    if model:
        print(f"Model: {model}")
    if loaded_env_files:
        print("Loaded .env files:")
        for env_file in loaded_env_files:
            print(f"  - {env_file}")

    if args.dry_run:
        print("Dry run complete.")
        return 0

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "firstproof-scout-helper/1.0",
    }

    if args.list_models:
        url = build_url(base_url, "/models")
        status, parsed, text = http_json("GET", url, headers, payload=None, timeout=args.timeout)
        print(f"HTTP {status} GET {url}")
        if args.raw_json:
            print(json.dumps(parsed, indent=2, ensure_ascii=True))
        else:
            if status == 200 and isinstance(parsed, dict):
                models = parsed.get("data", [])
                print(f"Model count: {len(models) if isinstance(models, list) else 'unknown'}")
                if isinstance(models, list):
                    for m in models[:20]:
                        if isinstance(m, dict):
                            print(f"  - {m.get('id')}")
            else:
                print(text[:1200])
        return 0 if status == 200 else 1

    try:
        prompt_text = resolve_prompt(args)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    messages: List[Dict[str, str]] = []
    if args.system:
        messages.append({"role": "system", "content": args.system})
    messages.append({"role": "user", "content": prompt_text})

    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
    }
    if args.reasoning_effort:
        payload["reasoning_effort"] = args.reasoning_effort

    url = build_url(base_url, "/chat/completions")
    start = time.time()
    status, parsed, text = http_json("POST", url, headers, payload=payload, timeout=args.timeout)
    elapsed = time.time() - start
    print(f"HTTP {status} POST {url} ({elapsed:.2f}s)")

    if args.raw_json:
        if parsed:
            print(json.dumps(parsed, indent=2, ensure_ascii=True))
        else:
            print(text[:4000])
        return 0 if status == 200 else 1

    if status != 200:
        print("Request failed.")
        print(text[:2000])
        return 1

    choices = parsed.get("choices", [])
    if not choices:
        print("No choices returned.")
        print(json.dumps(parsed, indent=2, ensure_ascii=True)[:2000])
        return 1

    first_choice = choices[0] if isinstance(choices, list) else {}
    message = first_choice.get("message", {}) if isinstance(first_choice, dict) else {}
    content = extract_message_text(message)
    if args.test:
        print("Test response:")
    else:
        print("Response:")
    print(textwrap.shorten(content.replace("\r", " ").replace("\n", " ").strip(), width=1200, placeholder=" ..."))

    # Optional reasoning field visibility.
    reasoning = ""
    if isinstance(message, dict):
        raw_reasoning = message.get("reasoning")
        if isinstance(raw_reasoning, str):
            reasoning = raw_reasoning.strip()
    if reasoning:
        print("Reasoning (truncated):")
        print(textwrap.shorten(reasoning.replace("\r", " ").replace("\n", " ").strip(), width=800, placeholder=" ..."))

    usage = parsed.get("usage")
    if usage is not None:
        print("Usage:")
        print(json.dumps(usage, ensure_ascii=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())



======================================================================
SOURCE: tools/scout_stream.py
======================================================================

#!/usr/bin/env python
"""
Streaming caller for Fireworks Kimi K2.5 model.
Fireworks requires stream=true for max_tokens > 4096 on thinking models.
Parses SSE (Server-Sent Events) streaming response. Stdlib only.
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.request


def load_api_key(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("FIREWORKS_API_KEY="):
                value = line.split("=", 1)[1].strip().strip("'\"")
                return value
    raise ValueError(f"FIREWORKS_API_KEY not found in {env_path}")


def stream_chat(api_key, prompt_text, timeout=420, max_tokens=16384):
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = json.dumps({
        "model": "accounts/fireworks/models/kimi-k2p5",
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "stream": True,
        "messages": [{"role": "user", "content": prompt_text}]
    }).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "text/event-stream",
    }
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    ctx = ssl.create_default_context()
    content_parts = []
    finish_reason = None
    usage = None

    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        print(f"  HTTP {resp.status}")
        buf = ""
        while True:
            chunk = resp.read(4096)
            if not chunk:
                break
            buf += chunk.decode("utf-8", errors="replace")
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line or line == "data: [DONE]":
                    continue
                if line.startswith("data: "):
                    try:
                        d = json.loads(line[6:])
                        ch = d.get("choices", [{}])[0]
                        c = ch.get("delta", {}).get("content")
                        if c:
                            content_parts.append(c)
                        fr = ch.get("finish_reason")
                        if fr:
                            finish_reason = fr
                        if d.get("usage"):
                            usage = d["usage"]
                    except (json.JSONDecodeError, IndexError):
                        pass
        # drain remainder
        for line in buf.strip().split("\n"):
            line = line.strip()
            if not line or line == "data: [DONE]":
                continue
            if line.startswith("data: "):
                try:
                    d = json.loads(line[6:])
                    ch = d.get("choices", [{}])[0]
                    c = ch.get("delta", {}).get("content")
                    if c:
                        content_parts.append(c)
                    fr = ch.get("finish_reason")
                    if fr:
                        finish_reason = fr
                    if d.get("usage"):
                        usage = d["usage"]
                except (json.JSONDecodeError, IndexError):
                    pass
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        print(f"  HTTP ERROR {e.code}: {body}")
        return {"content": None, "finish_reason": None, "usage": None, "error": body}
    except Exception as e:
        print(f"  Exception: {e}")
        return {"content": None, "finish_reason": None, "usage": None, "error": str(e)}

    return {"content": "".join(content_parts), "finish_reason": finish_reason, "usage": usage}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prompt-file", required=True)
    p.add_argument("--output-file", required=True)
    p.add_argument("--env-file", default=r"d:\Projects\loopforge-new\POC9\.env")
    p.add_argument("--timeout", type=int, default=420)
    p.add_argument("--max-tokens", type=int, default=16384)
    args = p.parse_args()

    api_key = load_api_key(args.env_file)
    print(f"Key loaded ({len(api_key)} chars)")

    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()
    print(f"Prompt: {len(prompt)} chars from {args.prompt_file}")

    t0 = time.time()
    r = stream_chat(api_key, prompt, timeout=args.timeout, max_tokens=args.max_tokens)
    print(f"  Elapsed: {time.time()-t0:.1f}s, finish_reason: {r['finish_reason']}")
    if r.get("usage"):
        print(f"  usage: {json.dumps(r['usage'])}")

    if r["content"]:
        print(f"  Content: {len(r['content'])} chars")
        with open(args.output_file, "w", encoding="utf-8") as f:
            f.write(r["content"])
        try:
            parsed = json.loads(r["content"])
            ok = "approaches" in parsed
            print(f"  Valid JSON: YES, has approaches: {ok}")
            if ok:
                print(f"  Approaches: {len(parsed['approaches'])}")
        except json.JSONDecodeError:
            s, e = r["content"].find("{"), r["content"].rfind("}")
            if s >= 0 and e > s:
                try:
                    parsed = json.loads(r["content"][s:e+1])
                    ok = "approaches" in parsed
                    print(f"  Extracted JSON, approaches: {ok}")
                    if ok:
                        with open(args.output_file, "w", encoding="utf-8") as f:
                            f.write(r["content"][s:e+1])
                except json.JSONDecodeError:
                    print("  No valid JSON found")
            else:
                print("  No JSON structure found")
        if r["finish_reason"] == "length":
            print(f"  TRUNCATED at {len(r['content'])} chars")
    else:
        print(f"  No content. Error: {r.get('error','unknown')}")
    sys.exit(0 if r["content"] else 1)


if __name__ == "__main__":
    main()



======================================================================
SOURCE: tools/model_capability_probe.py
======================================================================

#!/usr/bin/env python3
"""
Cross-provider capability probe for scout models.

Runs a small deterministic question set with exact answers and reports
per-model accuracy.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


DEFAULT_ENV_FILES = [
    pathlib.Path(r"d:/Projects/loopforge-new/POC9/.env"),
    pathlib.Path(r"d:/Projects/loopforge-new/M0/.env"),
    pathlib.Path(".env"),
]

PROVIDERS: Dict[str, Dict[str, str]] = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.ai/v1",
        "api_key_env": "MOONSHOT_API_KEY",
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "api_key_env": "FIREWORKS_API_KEY",
    },
}


@dataclass
class ModelSpec:
    provider: str
    model: str


DEFAULT_MODELS: List[ModelSpec] = [
    ModelSpec("groq", "qwen/qwen3-32b"),
    ModelSpec("groq", "openai/gpt-oss-120b"),
    ModelSpec("moonshot", "kimi-k2.5"),
    ModelSpec("moonshot", "kimi-k2-thinking"),
    ModelSpec("fireworks", "accounts/fireworks/models/qwen3-235b-a22b-instruct-2507"),
    ModelSpec("fireworks", "accounts/fireworks/models/deepseek-v3p2"),
    ModelSpec("fireworks", "accounts/fireworks/models/deepseek-r1-0528"),
    ModelSpec("fireworks", "accounts/fireworks/models/kimi-k2p5"),
]


QUESTIONS: List[Tuple[str, str, str]] = [
    ("Q1", "Compute 987*123.", "121401"),
    ("Q2", "Find the smallest positive n with n≡2 (mod 3), n≡3 (mod 5), n≡2 (mod 7).", "23"),
    ("Q3", "Compute det([[1,2,3],[0,1,4],[5,6,0]]).", "1"),
    ("Q4", "Compute S = sum_{k=1}^{20} k*2^k.", "39845890"),
    ("Q5", "How many derangements are there of 8 elements?", "14833"),
    ("Q6", "How many tilings of a 2x10 board by 2x1 dominoes?", "89"),
    ("Q7", "How many subsets of {1,...,10} contain no two consecutive integers?", "144"),
    ("Q8", "Compute 7^222 mod 13.", "12"),
    ("Q9", "If x+y=7 and xy=10, compute x^3+y^3.", "133"),
    ("Q10", "What is C(10,4)?", "210"),
    ("Q11", "How many onto functions from a 5-element set to a 3-element set?", "150"),
    ("Q12", "How many spanning trees does K_6 have?", "1296"),
]


def parse_env_line(line: str) -> Optional[Tuple[str, str]]:
    s = line.strip()
    if not s or s.startswith("#") or "=" not in s:
        return None
    k, v = s.split("=", 1)
    k = k.strip()
    v = v.strip().strip('"').strip("'")
    if not k:
        return None
    return k, v


def load_env(paths: List[pathlib.Path]) -> None:
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            parsed = parse_env_line(line)
            if not parsed:
                continue
            k, v = parsed
            if k not in os.environ:
                os.environ[k] = v


def extract_content(payload: Dict[str, Any]) -> str:
    choices = payload.get("choices", [])
    if not isinstance(choices, list) or not choices:
        return ""
    msg = choices[0].get("message", {})
    if not isinstance(msg, dict):
        return ""
    # Some providers emit a dedicated reasoning field; keep it as fallback.
    for reasoning_key in ("reasoning_content", "reasoning"):
        rv = msg.get(reasoning_key)
        if isinstance(rv, str) and rv.strip():
            reasoning_text = rv.strip()
            break
    else:
        reasoning_text = ""

    content = msg.get("content", "")
    if isinstance(content, str):
        if content.strip():
            return content
        return reasoning_text
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            if isinstance(item, dict):
                for key in ("text", "content", "reasoning_content"):
                    text = item.get(key)
                    if isinstance(text, str) and text.strip():
                        parts.append(text)
        joined = "\n".join(parts)
        if joined.strip():
            return joined
        return reasoning_text
    return ""


def normalize_answer(text: str) -> str:
    s = text.strip()
    # If JSON, prefer "answer" key.
    try:
        obj = json.loads(s)
        if isinstance(obj, dict) and "answer" in obj:
            s = str(obj["answer"]).strip()
    except Exception:
        # Handle JSON embedded in text/code fences.
        mjson = re.search(r"\{[\s\S]*\}", s)
        if mjson:
            try:
                obj = json.loads(mjson.group(0))
                if isinstance(obj, dict) and "answer" in obj:
                    s = str(obj["answer"]).strip()
            except Exception:
                pass
    # Prefer an explicit "answer: ..." pattern.
    mans = re.search(r'"?answer"?\s*[:=]\s*"?([^"\n\r}]+)"?', s, flags=re.IGNORECASE)
    if mans:
        s = mans.group(1).strip()
    else:
        # Reasoning-heavy models often write "the answer is X" in plain text.
        mphrases = re.findall(
            r"(?i)\b(?:final\s+)?answer(?:\s+is)?\s*[:=]?\s*([-+]?\d+(?:/\d+)?)",
            s,
        )
        if mphrases:
            s = mphrases[-1].strip()

    # Accept last signed integer/fraction-like token if extra text appears.
    tokens = re.findall(r"[-+]?\d+(?:/\d+)?", s)
    if tokens:
        s = tokens[-1]

    s = s.replace(",", "").strip()
    if re.fullmatch(r"[-+]?\d+", s):
        try:
            s = str(int(s))
        except Exception:
            pass
    return s


def call_model(
    provider: str,
    model: str,
    question: str,
    max_tokens: int,
    timeout: int,
) -> Tuple[bool, str, str, float]:
    cfg = PROVIDERS[provider]
    base_url = cfg["base_url"].rstrip("/")
    key = os.environ.get(cfg["api_key_env"], "")
    if not key:
        return False, "", f"missing {cfg['api_key_env']}", 0.0

    prompt = (
        "You are being scored for exact correctness.\n"
        'Return ONLY valid compact JSON with exactly one field named "answer".\n'
        "No markdown, no explanation.\n\n"
        f"Question: {question}"
    )
    body: Dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "firstproof-model-probe/1.0",
    }
    url = f"{base_url}/chat/completions"
    attempt = 0
    max_attempts = 3
    while attempt < max_attempts:
        attempt += 1
        start = time.time()
        try:
            resp = requests.post(url, headers=headers, json=body, timeout=timeout)
            elapsed = time.time() - start
            if resp.status_code == 200:
                data = resp.json()
                raw = extract_content(data)
                if not raw:
                    return False, "", "empty content", elapsed
                return True, raw, "", elapsed
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < max_attempts:
                time.sleep(2 ** attempt)
                continue
            return False, "", f"http {resp.status_code}: {resp.text[:200]}", elapsed
        except Exception as exc:
            if attempt < max_attempts:
                time.sleep(2 ** attempt)
                continue
            return False, "", str(exc), 0.0
    return False, "", "unreachable", 0.0


def run_probe(
    models: List[ModelSpec],
    max_tokens: int,
    timeout: int,
    delay_s: float,
) -> Dict[str, Any]:
    results: Dict[str, Any] = {
        "timestamp": int(time.time()),
        "questions": [{"id": qid, "question": q, "expected": a} for qid, q, a in QUESTIONS],
        "models": [],
    }

    for spec in models:
        model_key = f"{spec.provider}:{spec.model}"
        row: Dict[str, Any] = {
            "model_key": model_key,
            "provider": spec.provider,
            "model": spec.model,
            "score": 0,
            "total": len(QUESTIONS),
            "items": [],
        }
        for qid, question, expected in QUESTIONS:
            ok, raw, err, elapsed = call_model(
                spec.provider,
                spec.model,
                question,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            item: Dict[str, Any] = {
                "id": qid,
                "expected": expected,
                "ok": ok,
                "latency_s": round(elapsed, 3),
            }
            if not ok:
                item["error"] = err
            else:
                pred = normalize_answer(raw)
                item["predicted"] = pred
                item["correct"] = pred == expected
                if item["correct"]:
                    row["score"] += 1
            row["items"].append(item)
            if delay_s > 0:
                time.sleep(delay_s)
        results["models"].append(row)

    results["models"].sort(key=lambda m: m["score"], reverse=True)
    return results


def parse_model_specs(raw_specs: List[str]) -> List[ModelSpec]:
    specs: List[ModelSpec] = []
    for raw in raw_specs:
        if ":" not in raw:
            raise ValueError(f"Bad --model-spec '{raw}'. Expected provider:model")
        provider, model = raw.split(":", 1)
        provider = provider.strip()
        model = model.strip()
        if provider not in PROVIDERS:
            raise ValueError(f"Unknown provider '{provider}'.")
        if not model:
            raise ValueError(f"Bad --model-spec '{raw}' (empty model).")
        specs.append(ModelSpec(provider=provider, model=model))
    return specs


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-model exact-answer capability probe.")
    parser.add_argument(
        "--model-spec",
        action="append",
        default=[],
        help="Override model list. Format: provider:model (repeatable).",
    )
    parser.add_argument("--max-tokens", type=int, default=512, help="Per-call max_tokens.")
    parser.add_argument("--timeout", type=int, default=90, help="Per-call timeout seconds.")
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between calls in seconds (helps avoid rate limits).",
    )
    parser.add_argument(
        "--output",
        default="tools/model_probe_results.json",
        help="Output JSON path.",
    )
    args = parser.parse_args()

    load_env(DEFAULT_ENV_FILES)
    models = parse_model_specs(args.model_spec) if args.model_spec else DEFAULT_MODELS

    print("Running probe for models:")
    for m in models:
        print(f"  - {m.provider}:{m.model}")

    results = run_probe(
        models=models,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
        delay_s=args.delay,
    )

    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\nScoreboard:")
    for row in results["models"]:
        print(f"  {row['score']:>2}/{row['total']}  {row['model_key']}")
    print(f"\nSaved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

