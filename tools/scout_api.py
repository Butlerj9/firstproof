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
