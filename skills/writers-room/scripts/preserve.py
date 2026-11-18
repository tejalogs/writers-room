#!/usr/bin/env python3
"""Check that polishing didn't silently drop real material.

Usage:
    python3 preserve.py DRAFT FINAL [--review review.md]

Reports quotes, [NEEDS …] markers and links that are in the draft but missing from the final.
A [NEEDS …] marker may instead be listed in review.md (the polish stage moves blog gaps there).
Exit code 1 if anything is missing. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

QUOTE_RE = re.compile(r"[\"“]([^\"”\n]{12,}?)[\"”]")
NEEDS_RE = re.compile(r"\[NEEDS ([A-Z]+)[^\]]*\]")
LINK_RE = re.compile(r"https?://[^\s)\]>\"']+")


@dataclass(frozen=True)
class Missing:
    kind: str
    item: str


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("‘", "'")).strip().lower()


def find_missing(draft: str, final: str, review: str = "") -> tuple[Missing, ...]:
    final_n, review_n = _norm(final), _norm(review)
    quotes = tuple(Missing("quote", q) for q in dict.fromkeys(QUOTE_RE.findall(draft))
                   if _norm(q) not in final_n)
    needs = tuple(Missing("needs-marker", m.group(0)) for m in NEEDS_RE.finditer(draft)
                  if _norm(m.group(0)) not in final_n and _norm(m.group(0)) not in review_n)
    links = tuple(Missing("link", url) for url in dict.fromkeys(LINK_RE.findall(draft)) if url not in final)
    return quotes + needs + links


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check polishing didn't drop real material")
    parser.add_argument("draft", type=Path)
    parser.add_argument("final", type=Path)
    parser.add_argument("--review", type=Path, default=None, help="review.md, where blog gaps may be listed")
    args = parser.parse_args(argv)
    try:
        draft = args.draft.read_text(encoding="utf-8")
        final = args.final.read_text(encoding="utf-8")
        review = args.review.read_text(encoding="utf-8") if args.review else ""
    except OSError as exc:
        print(f"Could not read file: {exc}", file=sys.stderr)
        return 2
    missing = find_missing(draft, final, review)
    if not missing:
        print("preserve: nothing lost (quotes, [NEEDS] markers and links all kept)")
        return 0
    print(f"preserve: {len(missing)} item(s) in the draft are missing from the final:")
    for m in missing:
        print(f"  {m.kind:<13} {m.item[:90]}")
    print("Restore them, or remove them on purpose and say why in review.md.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
