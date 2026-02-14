#!/usr/bin/env python3
"""
Lightweight lint for final-form consistency in PXX/answer.md files.

This checker flags potential status contradictions, especially:
- Top-level Submitted status with unresolved/open language in body
- Mixed status markers that suggest stale merged content

It is intentionally conservative: findings are warnings for manual review.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Iterable


STATUS_LINE_RE = re.compile(r"^\*\*Status\*\*:\s*(.+)\s*$", re.IGNORECASE)

OPEN_PATTERNS = [
    re.compile(r"\bremains open\b", re.IGNORECASE),
    re.compile(r"\bif direction remains open\b", re.IGNORECASE),
    re.compile(r"\bunresolved\b", re.IGNORECASE),
    re.compile(r"\bnot formally proved\b", re.IGNORECASE),
    re.compile(r"\bBLOCKED_WITH_FRONTIER\b", re.IGNORECASE),
    re.compile(r"\b🟡\s*Candidate\b", re.IGNORECASE),
    re.compile(r"\b📊\s*Conjecture\b", re.IGNORECASE),
]

SUPPRESSED_CONTEXT_PATTERNS = [
    re.compile(r"\bhistorical note\b", re.IGNORECASE),
    re.compile(r"\bsuperseded\b", re.IGNORECASE),
    re.compile(r"\bchronological\b", re.IGNORECASE),
    re.compile(r"\barchive\b", re.IGNORECASE),
    re.compile(r"\b0\s+unresolved\b", re.IGNORECASE),
    re.compile(r"\bno\s+unresolved\b", re.IGNORECASE),
]


@dataclass
class Finding:
    path: pathlib.Path
    line_no: int
    message: str
    line: str


def is_submitted_status(status_text: str) -> bool:
    normalized = status_text.lower()
    return "submitted" in normalized or "✅" in status_text


def status_line(lines: list[str]) -> tuple[int, str] | None:
    for i, line in enumerate(lines, start=1):
        m = STATUS_LINE_RE.match(line.strip())
        if m:
            return i, m.group(1).strip()
    return None


def suppressed_by_context(line: str) -> bool:
    return any(p.search(line) for p in SUPPRESSED_CONTEXT_PATTERNS)


def scan_file(path: pathlib.Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    status_info = status_line(lines)
    if status_info is None:
        findings.append(
            Finding(path, 1, "Missing top-level **Status** line", lines[0] if lines else "")
        )
        return findings

    status_ln, status_val = status_info
    submitted = is_submitted_status(status_val)

    # Flag multiple status lines: common source of stale merged state.
    extra_status_lines = []
    for i, line in enumerate(lines, start=1):
        if i == status_ln:
            continue
        if STATUS_LINE_RE.match(line.strip()):
            extra_status_lines.append((i, line))
    for i, line in extra_status_lines:
        findings.append(
            Finding(path, i, "Additional **Status** line found (possible stale section)", line)
        )

    if submitted:
        for i, line in enumerate(lines, start=1):
            if i == status_ln:
                continue
            if suppressed_by_context(line):
                continue
            if any(p.search(line) for p in OPEN_PATTERNS):
                findings.append(
                    Finding(
                        path,
                        i,
                        "Submitted status with unresolved/open language",
                        line,
                    )
                )
    return findings


def discover_paths(input_paths: Iterable[str]) -> list[pathlib.Path]:
    resolved: list[pathlib.Path] = []
    for raw in input_paths:
        p = pathlib.Path(raw)
        if any(ch in raw for ch in "*?[]"):
            resolved.extend(sorted(pathlib.Path(".").glob(raw)))
        elif p.is_dir():
            resolved.extend(sorted(p.glob("answer.md")))
        elif p.is_file():
            resolved.append(p)
    # Stable dedup
    out: list[pathlib.Path] = []
    seen: set[pathlib.Path] = set()
    for p in resolved:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Check final-form consistency in answer.md files.")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["P*/answer.md"],
        help="Paths, directories, or globs to scan (default: P*/answer.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero if any finding is emitted.",
    )
    args = parser.parse_args()

    targets = discover_paths(args.paths)
    if not targets:
        print("No files matched.")
        return 1

    all_findings: list[Finding] = []
    for path in targets:
        all_findings.extend(scan_file(path))

    if not all_findings:
        print(f"OK: scanned {len(targets)} files, no findings.")
        return 0

    print(f"Findings: {len(all_findings)} across {len(targets)} files")
    for f in all_findings:
        print(f"- {f.path}:{f.line_no}: {f.message}")
        print(f"  {f.line.strip()}")

    if args.strict:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
