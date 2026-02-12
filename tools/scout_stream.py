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
