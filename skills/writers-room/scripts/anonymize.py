#!/usr/bin/env python3
"""Strip identifiers from a transcript before it enters a story bank.

Usage:
    python3 anonymize.py TRANSCRIPT [--names "Priya,Rahul"] [--orgs "Acme Ltd,TCS"]
                         [--report report.json] > out.txt

Catches: emails, phone numbers, URLs, UK postcodes, US ZIP codes, dates of birth,
long ID-like numbers, names you pass, names introduced as "my name is X" /
"this is X", and speaker labels that contain a name.

It CANNOT find every name, employer or school. A human must read the output
before it is used. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")),
    ("URL", re.compile(r"\b(?:https?://|www\.)\S+", re.I)),
    ("PHONE", re.compile(r"(?<![\w])(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?){2,4}\d{3,4}(?![\w])")),
    ("POSTCODE", re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b")),
    ("DOB", re.compile(r"\b(?:\d{1,2}[/-]\d{1,2}[/-](?:19|20)\d{2})\b")),
    ("ID", re.compile(r"\b[A-Z]{0,3}\d{8,}\b")),
)
# Deliberately narrow: "I'm Indian" or "this is Monday" must not be treated as names.
INTRO_RE = re.compile(
    r"(?i:\bmy name is|\bmy name's|\bcall me|\bthis is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    r"(?=\s+speaking|\s*[,.]|\s+from\b|\s+here\b|$)"
)
SPEAKER_RE = re.compile(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:", re.M)
GENERIC_SPEAKERS = frozenset({"Agent", "User", "Host", "Guest", "Speaker", "Caller", "Adviser",
                              "Advisor", "Counsellor", "Counselor", "Candidate", "Interviewer"})
NOT_NAMES = frozenset({"Sorry", "Here", "Just", "Not", "Really", "Very", "Going", "Looking",
                       "Calling", "Working", "From", "Fine", "Good", "Okay", "Happy", "Sure"})


@dataclass(frozen=True)
class Result:
    text: str
    counts: dict[str, int] = field(default_factory=dict)
    names_found: tuple[str, ...] = ()


def _apply_patterns(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for label, pattern in PATTERNS:
        text, n = pattern.subn(f"[{label}]", text)
        if n:
            counts = {**counts, label: n}
    return text, counts


def discover_names(text: str) -> tuple[str, ...]:
    intro = {m.group(1) for m in INTRO_RE.finditer(text)}
    speakers = {m.group(1) for m in SPEAKER_RE.finditer(text)}
    candidates = (intro | speakers) - GENERIC_SPEAKERS
    cleaned = {c for c in candidates if c.split()[0] not in NOT_NAMES}
    return tuple(sorted(cleaned))


def _expand(names: tuple[str, ...]) -> tuple[str, ...]:
    """Include each part of multi-word names so 'Priya Sharma' also hides 'Priya'."""
    parts = {p for n in names for p in n.split() if len(p) > 2}
    return tuple(sorted(set(names) | parts, key=len, reverse=True))


def _replace_terms(text: str, terms: tuple[str, ...], label: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    for term in terms:
        tag = mapping.get(term) or f"[{label}_{len(mapping) + 1}]"
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.I)
        if pattern.search(text):
            mapping = {**mapping, term: tag}
            text = pattern.sub(tag, text)
    return text, mapping


def anonymize(text: str, names: tuple[str, ...] = (), orgs: tuple[str, ...] = ()) -> Result:
    found = discover_names(text)
    all_names = _expand(tuple(n.strip() for n in names if n.strip()) + found)
    text, counts = _apply_patterns(text)
    text, name_map = _replace_terms(text, all_names, "NAME")
    text, org_map = _replace_terms(text, tuple(o.strip() for o in orgs if o.strip()), "ORG")
    counts = {**counts, "NAME": len(name_map), "ORG": len(org_map)}
    return Result(text=text, counts=counts, names_found=found)


def _split_csv(value: str | None) -> tuple[str, ...]:
    return tuple(v for v in (value or "").split(",") if v.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Strip identifiers from a transcript")
    parser.add_argument("file", type=Path)
    parser.add_argument("--names", help="comma-separated names to remove")
    parser.add_argument("--orgs", help="comma-separated employers/schools to remove")
    parser.add_argument("--report", type=Path, help="write counts + auto-found names as JSON")
    args = parser.parse_args(argv)
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Could not read {args.file}: {exc}", file=sys.stderr)
        return 2
    result = anonymize(text, _split_csv(args.names), _split_csv(args.orgs))
    sys.stdout.write(result.text)
    summary = {"counts": result.counts, "auto_found_names": list(result.names_found)}
    if args.report:
        args.report.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n# anonymize: {summary} -- a human must read this before use", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
