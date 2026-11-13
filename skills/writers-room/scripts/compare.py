#!/usr/bin/env python3
"""Compare lint results for two sets of outputs (e.g. without vs with the skill).

Usage:
    python3 compare.py --a baseline/ --b with-skill/ --mode blog [--brand brand.json]

Each directory holds one final .md per scenario, named <scenario-id>.md. Prints a
Markdown table of errors, warnings and the most common checks per side. This
measures mechanical quality only; judge writing quality with evals/pairwise-judge.md
(a large model or a human).
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint import DEFAULT_BANNED, DEFAULT_WATCH, Finding, lint, load_banned, load_brand  # noqa: E402


@dataclass(frozen=True)
class Summary:
    files: int
    errors: int
    warnings: int
    needs_markers: int
    top_checks: tuple[tuple[str, int], ...]


def summarise(findings_by_file: dict[str, list[Finding]]) -> Summary:
    all_findings = [f for fs in findings_by_file.values() for f in fs]
    counted = Counter(f.check for f in all_findings if f.level in ("ERROR", "WARN"))
    return Summary(
        files=len(findings_by_file),
        errors=sum(1 for f in all_findings if f.level == "ERROR"),
        warnings=sum(1 for f in all_findings if f.level == "WARN"),
        needs_markers=sum(1 for f in all_findings if f.check == "needs-marker"),
        top_checks=tuple(counted.most_common(5)),
    )


def lint_dir(folder: Path, mode: str, brand: dict) -> dict[str, list[Finding]]:
    banned = load_banned(DEFAULT_BANNED) + tuple(p.lower() for p in brand.get("extra_banned_phrases", []))
    watch = load_banned(DEFAULT_WATCH)
    results: dict[str, list[Finding]] = {}
    for path in sorted(folder.glob("*.md")):
        results = {**results, path.stem: lint(path.read_text(encoding="utf-8"), mode, banned, brand, watch)}
    return results


def render(a: Summary, b: Summary, label_a: str, label_b: str) -> str:
    def top(s: Summary) -> str:
        return ", ".join(f"{c} ({n})" for c, n in s.top_checks) or "none"

    rows = [
        f"| | {label_a} | {label_b} |",
        "|---|---|---|",
        f"| Files | {a.files} | {b.files} |",
        f"| Errors | {a.errors} | {b.errors} |",
        f"| Warnings | {a.warnings} | {b.warnings} |",
        f"| [NEEDS] markers (honest gaps) | {a.needs_markers} | {b.needs_markers} |",
        f"| Most common issues | {top(a)} | {top(b)} |",
    ]
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare lint results for two output folders")
    parser.add_argument("--a", type=Path, required=True, help="e.g. baseline outputs")
    parser.add_argument("--b", type=Path, required=True, help="e.g. with-skill outputs")
    parser.add_argument("--mode", choices=("blog", "podcast", "video"), required=True)
    parser.add_argument("--brand", type=Path, default=None)
    parser.add_argument("--label-a", default="Baseline")
    parser.add_argument("--label-b", default="With skill")
    args = parser.parse_args(argv)
    for folder in (args.a, args.b):
        if not folder.is_dir():
            print(f"Not a directory: {folder}", file=sys.stderr)
            return 2
    brand = load_brand(args.brand)
    a = summarise(lint_dir(args.a, args.mode, brand))
    b = summarise(lint_dir(args.b, args.mode, brand))
    print(render(a, b, args.label_a, args.label_b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
