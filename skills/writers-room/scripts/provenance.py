#!/usr/bin/env python3
"""Check that every number and quote in a finished piece comes from the material.

Usage:
    python3 provenance.py FINAL --material 02-material.md 02b-research.md <brand-dir> [...]

Material can be files or folders (all .md/.txt/.csv/.json inside are read): the stage-2
material, the stage-2b claims table, the brand pack (BRAND.md proof, story bank).

Flags:
  unsourced-number  a number, percentage or duration not found anywhere in the material
  unsourced-quote   a quotation (12+ characters) not found verbatim in the material

Exit code 1 if anything is unsourced. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from wr_text import NEEDS_RE, split_frontmatter

NUMBER_RE = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?:\s?%|\s?per ?cent)?")
QUOTE_RE = re.compile(r"[\"“]([^\"”\n]{12,}?)[\"”]")
LIST_MARKER_RE = re.compile(r"^(\s*(?:#+\s*)?(?:[-*]\s+)?)\d+[.)]\s", re.M)
MATERIAL_SUFFIXES = (".md", ".txt", ".csv", ".json")


@dataclass(frozen=True)
class Unsourced:
    kind: str
    item: str
    context: str


def _norm_number(raw: str) -> str:
    return re.sub(r"[,\s]|per ?cent", "", raw.lower()).replace("%", "")


def _norm_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("’", "'").replace("‘", "'")).strip().lower()


def read_material(paths: list[Path]) -> str:
    chunks = []
    for path in paths:
        files = sorted(p for p in path.rglob("*") if p.suffix in MATERIAL_SUFFIXES) if path.is_dir() else [path]
        for f in files:
            try:
                chunks.append(f.read_text(encoding="utf-8"))
            except OSError as exc:
                raise SystemExit(f"Could not read material {f}: {exc}") from exc
    return "\n".join(chunks)


def _piece_text(final: str) -> str:
    _, body = split_frontmatter(final)
    body = NEEDS_RE.sub("", body)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"https?://\S+", "", body)
    return LIST_MARKER_RE.sub(r"\1", body)


def _context(text: str, start: int) -> str:
    return re.sub(r"\s+", " ", text[max(0, start - 40): start + 50]).strip()


def find_unsourced(final: str, material: str) -> tuple[Unsourced, ...]:
    piece = _piece_text(final)
    known_numbers = {_norm_number(m.group(0)) for m in NUMBER_RE.finditer(material)}
    material_norm = _norm_text(material)
    numbers, seen = [], set()
    for m in NUMBER_RE.finditer(piece):
        value = _norm_number(m.group(0))
        if value in known_numbers or value in seen:
            continue
        seen.add(value)
        numbers.append(Unsourced("unsourced-number", m.group(0).strip(), _context(piece, m.start())))
    quotes = [Unsourced("unsourced-quote", q, q[:80]) for q in dict.fromkeys(QUOTE_RE.findall(piece))
              if _norm_text(q) not in material_norm]
    return tuple(numbers) + tuple(quotes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check every number and quote traces to the material")
    parser.add_argument("final", type=Path)
    parser.add_argument("--material", type=Path, nargs="+", required=True,
                        help="material files or folders (02-material.md, 02b-research.md, brand pack)")
    args = parser.parse_args(argv)
    try:
        final = args.final.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Could not read {args.final}: {exc}", file=sys.stderr)
        return 2
    missing = find_unsourced(final, read_material(args.material))
    if not missing:
        print("provenance: every number and quote traces to the material")
        return 0
    print(f"provenance: {len(missing)} item(s) don't trace to the material:")
    for m in missing:
        print(f"  {m.kind:<16} {m.item[:40]:<12} …{m.context}…")
    print("Add each to the claims table with a source, mark it [NEEDS SOURCE], or cut it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
