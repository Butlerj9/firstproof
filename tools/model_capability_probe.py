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
