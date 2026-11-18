"""Linter v2 checks: repetition, unsourced stats, spelling consistency, watch-word clusters,
inline ignores and the 0–100 score. Rule ideas borrowed from Vale, proselint, slopless and
avoid-ai-writing."""
from __future__ import annotations

import re
from typing import Iterable

from wr_text import Finding, line_of, sentences, words

WATCH_WINDOW = 150
WATCH_CLUSTER_MIN = 3

STAT_RE = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|per ?cent\b)|\b\d+ (?:in|out of) (?:every )?\d+\b", re.I)
SOURCE_CUE_RE = re.compile(
    r"according to|\bsource\b|\bstudy\b|\bsurvey|\breport\b|research (?:by|from)|data from|"
    r"\bfound\b|we (?:surveyed|measured|counted|asked|analysed|analyzed)|our (?:own )?data|"
    r"\(\d{4}\)|\b(?:19|20)\d{2}\b|https?://|\[NEEDS", re.I)

# Exact word forms, so "organism" or "realistic" never match.
SPELLING_PAIRS: tuple[tuple[frozenset[str], frozenset[str]], ...] = tuple(
    (frozenset(uk.split()), frozenset(us.split())) for uk, us in (
        ("colour colours coloured colourful", "color colors colored colorful"),
        ("favour favours favourite favourites favoured", "favor favors favorite favorites favored"),
        ("behaviour behaviours behavioural", "behavior behaviors behavioral"),
        ("organise organised organising organisation organisations",
         "organize organized organizing organization organizations"),
        ("realise realised realising", "realize realized realizing"),
        ("recognise recognised recognising", "recognize recognized recognizing"),
        ("analyse analysed analysing", "analyze analyzed analyzing"),
        ("optimise optimised optimising optimisation", "optimize optimized optimizing optimization"),
        ("prioritise prioritised prioritising", "prioritize prioritized prioritizing"),
        ("centre centres", "center centers"),
        ("labour", "labor"),
        ("defence", "defense"),
        ("cancelled cancelling", "canceled canceling"),
        ("travelled travelling traveller", "traveled traveling traveler"),
    ))

IGNORE_FILE_RE = re.compile(r"<!--\s*wr-ignore:\s*([\w,\s-]+?)\s*-->")
IGNORE_LINE_RE = re.compile(r"<!--\s*wr-ignore-line:\s*([\w,\s-]+?)\s*-->")


def check_repeated_openers(prose: str) -> list[Finding]:
    """Three or more sentences in a row starting with the same word."""
    firsts = [(words(s)[0].lower() if words(s) else "", s) for s in sentences(prose)]
    found, run = [], 1
    for i in range(1, len(firsts)):
        same = firsts[i][0] and firsts[i][0] == firsts[i - 1][0]
        run = run + 1 if same else 1
        if run == 3:
            found.append(Finding("WARN", "repeated-opener",
                                 f'3+ sentences in a row start with "{firsts[i][0]}": {firsts[i][1][:60]}'))
    return found[:3]


def check_unsourced_stats(prose_with_needs: str) -> list[Finding]:
    """A percentage or 'X in Y' figure with no source cue in the same sentence."""
    found = []
    for sent in sentences(prose_with_needs):
        if STAT_RE.search(sent) and not SOURCE_CUE_RE.search(sent):
            found.append(Finding("WARN", "unsourced-stat",
                                 f"Statistic with no source in the sentence: {sent[:80]}"))
    return found[:5]


def check_spelling(prose: str, spelling: str | None) -> list[Finding]:
    toks = {w.lower() for w in words(prose)}
    uk_used = sorted(t for uk, _ in SPELLING_PAIRS for t in uk & toks)
    us_used = sorted(t for _, us in SPELLING_PAIRS for t in us & toks)
    wanted = (spelling or "").upper()
    if wanted == "UK" and us_used:
        return [Finding("WARN", "spelling", f"US spellings in a UK piece: {', '.join(us_used[:6])}")]
    if wanted == "US" and uk_used:
        return [Finding("WARN", "spelling", f"UK spellings in a US piece: {', '.join(uk_used[:6])}")]
    if not wanted and uk_used and us_used:
        return [Finding("WARN", "spelling",
                        f"Mixed UK ({', '.join(uk_used[:3])}) and US ({', '.join(us_used[:3])}) spelling")]
    return []


def check_watch_clusters(prose: str, watch: Iterable[str]) -> list[Finding]:
    """Watch words that are fine alone but cluster inside one ~150-word window."""
    watch_set = frozenset(watch)
    toks = [w.lower() for w in words(prose)]
    hits = [i for i, t in enumerate(toks) if t in watch_set]
    for start in range(len(hits)):
        window = [i for i in hits[start:] if i - hits[start] < WATCH_WINDOW]
        if len(window) >= WATCH_CLUSTER_MIN:
            listed = ", ".join(toks[i] for i in window[:5])
            return [Finding("WARN", "watch-cluster",
                            f"{len(window)} watch words within {WATCH_WINDOW} words ({listed}); rewrite that passage")]
    return []


def parse_ignores(raw: str) -> tuple[frozenset[str], dict[int, frozenset[str]]]:
    def ids(group: str) -> frozenset[str]:
        return frozenset(i.strip() for i in group.split(",") if i.strip())

    file_level = frozenset().union(*(ids(m.group(1)) for m in IGNORE_FILE_RE.finditer(raw)))
    by_line: dict[int, frozenset[str]] = {}
    for m in IGNORE_LINE_RE.finditer(raw):
        line = line_of(raw, m.start())
        by_line = {**by_line, line: by_line.get(line, frozenset()) | ids(m.group(1))}
    return file_level, by_line


def apply_ignores(findings: list[Finding], raw: str) -> list[Finding]:
    file_level, by_line = parse_ignores(raw)

    def ignored(f: Finding) -> bool:
        if f.check in file_level:
            return True
        return f.line is not None and f.check in by_line.get(f.line, frozenset())

    return [f for f in findings if not ignored(f)]


def score(findings: Iterable[Finding]) -> int:
    """0–100: each ERROR costs 10, each WARN costs 3, notes are free."""
    items = list(findings)
    errors = sum(1 for f in items if f.level == "ERROR")
    warns = sum(1 for f in items if f.level == "WARN")
    return max(0, 100 - 10 * errors - 3 * warns)
