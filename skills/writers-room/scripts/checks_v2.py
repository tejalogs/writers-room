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

SELF_RESEARCH_RE = re.compile(
    r"\bour (?:research|data|analytics|product|growth|editorial) team (?:ran|found|analy[sz]ed|tested|studied|collected)|"
    r"\bwe (?:ran|conducted|collected|fed|tested|surveyed|analy[sz]ed|studied|benchmarked) (?:a |an |the |every |our |\d)|"
    r"\bour (?:study|survey|experiment|analysis|research|audit|autopsy|benchmark|report) "
    r"(?:found|finds|shows|showed|revealed|reveals|proves)", re.I)
# A branded "study": "the 7-Day Curriculum Autopsy", "The Hiring Experiment".
NAMED_STUDY_RE = re.compile(
    r"\b[Tt]he (?:\d+-(?:[Dd]ay|[Ww]eek|[Mm]onth) )?(?:[A-Z][\w-]* ){1,3}"
    r"(?:Autopsy|Experiment|Study|Survey|Audit|Benchmark|Challenge|Report)\b")
SIGNPOST_RE = re.compile(
    r"(?:^|[.!?]\s+)(?:here is (?:why|what|how)|here'?s (?:why|what|how)|you will (?:see|learn|discover|find out)|"
    r"you'll (?:see|learn|discover|find out)|in this (?:post|article|guide|piece)|let'?s (?:look|explore|break down|dive)|"
    r"below,? (?:we|you)|we'?ll (?:cover|explore|look at|walk through))\b", re.I | re.M)
LABEL_BULLET_RE = re.compile(r"^\s*[-*]\s+(?:\*\*)?[A-Z][^:\n]{1,45}:(?:\*\*)?\s+\S")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F600-\U0001F64F☀-⛿✀-➿⭐⬆➡]")

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


def check_self_research(prose: str) -> list[Finding]:
    """The brand claiming to have run a study, survey or experiment."""
    hits = [m.group(0) for m in SELF_RESEARCH_RE.finditer(prose)] + \
           [m.group(0) for m in NAMED_STUDY_RE.finditer(prose)]
    return [Finding("WARN", "self-research",
                    f'"{h}": a study the brand ran must be in the claims table with its method; otherwise cut it')
            for h in dict.fromkeys(hits)][:3]


def check_signposting(prose: str) -> list[Finding]:
    """Narrating the piece's own structure instead of delivering it."""
    hits = [re.sub(r"\s+", " ", m.group(0)).strip(" .!?") for m in SIGNPOST_RE.finditer(prose)]
    if not hits:
        return []
    return [Finding("WARN", "signposting",
                    f'Narrates its own structure ({"; ".join(h[:30] for h in hits[:3])}): just deliver the content')]


def check_label_lists(body: str) -> list[Finding]:
    """Two or more bullet lists where most items are 'Label: explanation' (templated structure)."""
    lists, current = [], []
    for line in body.splitlines():
        if re.match(r"^\s*[-*]\s+", line):
            current.append(line)
        elif current:
            lists, current = lists + [current], []
    if current:
        lists = lists + [current]
    templated = [lst for lst in lists if len(lst) >= 3 and sum(bool(LABEL_BULLET_RE.match(i)) for i in lst) >= 3]
    if len(templated) >= 2:
        return [Finding("WARN", "label-lists",
                        f"{len(templated)} bullet lists built as 'Label: explanation'; the repeated template reads "
                        "as machine-made. Turn at least one into prose or a table")]
    return []


def check_emoji(prose: str) -> list[Finding]:
    found = EMOJI_RE.findall(prose)
    if found:
        return [Finding("WARN", "emoji", f"Emoji in the copy ({''.join(found[:5])}); cut them from blogs and landing pages")]
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
