#!/usr/bin/env python3
"""Writers' Room linter: deterministic checks for blogs and podcast scripts.

Usage:
    python3 lint.py FILE --mode blog|podcast [--brand brand.json] [--json]

Exit code 1 if any ERROR is found. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_BANNED = SKILL_DIR / "craft" / "banned-phrases.txt"
DEFAULT_WATCH = SKILL_DIR / "craft" / "watch-words.txt"
WATCH_PER_K = 2.0

# Structural tells (EQ-Bench slop-score; Wikipedia "Signs of AI writing").
# (name, pattern, allowed per 1,000 words (minimum 1 per piece), advice)
STRUCTURAL_TELLS: tuple[tuple[str, re.Pattern[str], float, str], ...] = (
    ("not-x-but-y",
     re.compile(r"\b(?:not|isn't|wasn't|aren't)\s+(?:just|only|merely|simply|about)\s+[^.!?;]{1,60}?"
                r"(?:[,;]\s*but\b|[.!?]\s+(?:it's|it is|it was|this is)\b)", re.I),
     1.0, '"It\'s not X, it\'s Y" contrasts: once per piece at most'),
    ("rather-than", re.compile(r"\brather than\b", re.I), 2.0, '"rather than" contrasts piling up'),
    ("copula-avoidance",
     re.compile(r"\b(?:serves|served|stands|stood|acts|functions) as (?:a|an|the)\b|\bboasts\b", re.I),
     1.0, 'say "is"/"has" instead of "serves as"/"stands as"/"boasts"'),
    ("trailing-ing",
     re.compile(r",\s+(?:highlighting|underscoring|reflecting|showcasing|emphasi[sz]ing|demonstrating|"
                r"illustrating|signal(?:l)?ing|cementing|solidifying|marking|paving)\b", re.I),
     1.0, 'trailing ", highlighting..." clauses inflate significance; end the sentence or make it two'),
)
VAGUE_ATTRIBUTION = re.compile(
    r"\b(?:experts|studies|research|researchers|scientists|many people|some people|reports)\s+"
    r"(?:say|says|show|shows|suggest|suggests|agree|argue|believe|found|indicate|indicates)\b", re.I)
UNBACKED_FREQUENCY = re.compile(
    r"\b(?:most people|almost (?:nobody|no one|everyone)|everyone knows|nobody tells you"
    r"|no one talks about|the vast majority|nine times out of ten)\b", re.I)
TIDY_ENDING = re.compile(
    r"^\s*(?:ultimately|in the end|at its core|the takeaway|the bottom line|the future (?:of [^.]+ )?is"
    r"|as we move forward|moving forward|one thing is clear)\b", re.I)

THROAT_CLEARING = (
    "welcome to", "in this episode", "in this article", "in this post",
    "today we", "today i", "have you ever", "in today's", "let's dive",
    "hi everyone", "hello everyone", "hey everyone",
)
HEDGES = ("very", "really", "just", "actually", "basically", "quite", "simply")
MARKER_RE = re.compile(r"\[(?:LOOP|CLOSE|REHOOK|PAUSE|EMPHASIS|SLOW|MUSIC|SFX|"
                       r"COLD OPEN|IDENT|PROMISE|CLOSE)[^\]]*\]", re.I)
LOOP_RE = re.compile(r"\[LOOP:\s*([\w-]+)\s*\]", re.I)
CLOSE_RE = re.compile(r"\[CLOSE:\s*([\w-]+)\s*\]", re.I)
REHOOK_RE = re.compile(r"\[REHOOK\]", re.I)
NEEDS_RE = re.compile(r"\[NEEDS (?:STORY|SOURCE)[^\]]*\]", re.I)
SPEAKER_RE = re.compile(r"^\s*(?:HOST(?: [A-Z])?|GUEST|[A-Z]{2,}):\s*", re.M)

LIMITS = {
    "blog": {"max_sentence": 35, "first_line": 20, "min_words": 800},
    "podcast": {"max_sentence": 25, "first_line": 15, "min_words": 300},
}
REHOOK_MAX_GAP_WORDS = 260  # ~90-105 s at 150 wpm


@dataclass(frozen=True)
class Finding:
    level: str  # ERROR | WARN | INFO
    check: str
    message: str
    line: int | None = None


# ---------- text helpers ----------

def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta: dict[str, str] = {}
    for raw in text[3:end].strip().splitlines():
        if ":" in raw:
            key, value = raw.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, text[end + 4:].lstrip("\n")


def strip_markers(text: str) -> str:
    return MARKER_RE.sub("", text)


def prose_lines(body: str) -> list[str]:
    """Lines that are prose (not headings, code fences, frontmatter, tables)."""
    out, in_code = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith(("#", "|", ">")):
            continue
        out.append(line)
    return out


def clean_prose(body: str) -> str:
    text = "\n".join(prose_lines(body))
    text = SPEAKER_RE.sub("", text)
    text = strip_markers(text)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text.replace("- ", " ")).strip()
    parts = re.split(r"(?<=[.!?])[\"'”’)]*\s+(?=[\"'“‘(]*[A-Z0-9])", flat)
    return [p.strip() for p in parts if len(p.split()) >= 2]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9'’-]+", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def load_banned(path: Path) -> tuple[str, ...]:
    if not path.exists():
        return ()
    rows = (r.strip().lower() for r in path.read_text(encoding="utf-8").splitlines())
    return tuple(r for r in rows if r and not r.startswith("#"))


def load_brand(path: Path | None) -> dict:
    if path is None:
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Could not read brand file {path}: {exc}") from exc


# ---------- checks shared by both modes ----------

def check_banned(raw: str, phrases: Iterable[str]) -> list[Finding]:
    lower = raw.lower()
    found = []
    for phrase in phrases:
        idx = lower.find(phrase)
        if idx != -1:
            found.append(Finding("ERROR", "banned-phrase",
                                 f'"{phrase}" reads as generic/machine-written', line_of(raw, idx)))
    return found


def check_brand_terms(raw: str, brand: dict) -> list[Finding]:
    found = []
    for rule in brand.get("banned_terms", []):
        pattern = re.compile(rule["pattern"], re.I)
        for match in pattern.finditer(raw):
            found.append(Finding(rule.get("severity", "ERROR"), "brand-compliance",
                                 f'"{match.group(0)}": {rule.get("reason", "brand rule")}',
                                 line_of(raw, match.start())))
    name = brand.get("brand_name")
    for wrong in brand.get("wrong_spellings", []):
        for match in re.finditer(re.escape(wrong), raw):
            found.append(Finding("ERROR", "brand-name",
                                 f'"{wrong}" should be "{name}"', line_of(raw, match.start())))
    return found


def check_first_line(prose: str, mode: str) -> list[Finding]:
    sents = sentences(prose)
    if not sents:
        return [Finding("ERROR", "empty", "No prose found")]
    first = sents[0]
    found = []
    limit = LIMITS[mode]["first_line"]
    if len(words(first)) > limit:
        found.append(Finding("WARN", "hook-length",
                             f"First sentence is {len(words(first))} words (aim ≤ {limit}): {first[:80]}"))
    if first.lower().startswith(THROAT_CLEARING):
        found.append(Finding("ERROR", "throat-clearing", f"Opens with throat-clearing: {first[:80]}"))
    return found


def check_rhythm(prose: str, mode: str) -> list[Finding]:
    sents = sentences(prose)
    lengths = [len(words(s)) for s in sents]
    if len(lengths) < 8:
        return []
    found = []
    limit = LIMITS[mode]["max_sentence"]
    long_ones = [s for s, n in zip(sents, lengths) if n > limit]
    for s in long_ones[:5]:
        level = "ERROR" if mode == "podcast" else "WARN"
        found.append(Finding(level, "long-sentence", f"{len(words(s))} words (max {limit}): {s[:90]}..."))
    stdev = statistics.pstdev(lengths)
    if stdev < 4.5:
        found.append(Finding("WARN", "monotone-rhythm",
                             f"Sentence lengths barely vary (stdev {stdev:.1f}); mix short and long"))
    mean = statistics.mean(lengths)
    if mode == "podcast" and mean > 17:
        found.append(Finding("WARN", "ear-length", f"Average sentence {mean:.1f} words; aim 12–16 for audio"))
    return found


def check_hedges(prose: str) -> list[Finding]:
    toks = [w.lower() for w in words(prose)]
    if not toks:
        return []
    count = sum(1 for t in toks if t in HEDGES)
    per_k = count * 1000 / len(toks)
    if per_k > 8:
        return [Finding("WARN", "hedges", f"{count} hedge words ({per_k:.0f}/1000 words): cut very/really/just/actually")]
    return []


def check_dashes(prose: str) -> list[Finding]:
    # INFO only: em-dash overuse is an older-model tell; newer models use fewer.
    n_words = max(len(words(prose)), 1)
    dashes = prose.count("—")
    if dashes * 200 / n_words > 1:
        return [Finding("INFO", "em-dashes", f"{dashes} em dashes; consider fewer")]
    return []


def _allowed(per_k: float, n_words: int) -> float:
    return max(1.0, per_k * n_words / 1000)


def check_structural_tells(prose: str) -> list[Finding]:
    n_words = len(words(prose))
    found = []
    for name, pattern, per_k, advice in STRUCTURAL_TELLS:
        hits = [m.group(0) for m in pattern.finditer(prose)]
        if len(hits) > _allowed(per_k, n_words):
            sample = "; ".join(h[:50] for h in hits[:3])
            found.append(Finding("WARN", name, f"{len(hits)}x: {advice} (e.g. {sample})"))
    for match in VAGUE_ATTRIBUTION.finditer(prose):
        found.append(Finding("WARN", "vague-attribution",
                             f'"{match.group(0)}": name the source or cut the claim'))
    for match in UNBACKED_FREQUENCY.finditer(prose):
        found.append(Finding("WARN", "unbacked-frequency",
                             f'"{match.group(0)}" is a statistic in disguise: cite it, soften it or cut it'))
    return found


def check_tidy_ending(prose: str) -> list[Finding]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", prose) if len(words(p)) >= 5]
    if paras and TIDY_ENDING.match(paras[-1]):
        return [Finding("WARN", "tidy-ending",
                        f"Final paragraph opens with a tidy moral: {paras[-1][:60]}... End on a callback or image")]
    return []


def check_watch_words(prose: str, watch: Iterable[str]) -> list[Finding]:
    toks = [w.lower() for w in words(prose)]
    watch_set = frozenset(watch)
    if not toks or not watch_set:
        return []
    hits: dict[str, int] = {}
    for tok in toks:
        if tok in watch_set:
            hits = {**hits, tok: hits.get(tok, 0) + 1}
    total = sum(hits.values())
    repeated = sorted(w for w, n in hits.items() if n > 1)
    if total > _allowed(WATCH_PER_K, len(toks)) or repeated:
        listed = ", ".join(f"{w}×{n}" for w, n in sorted(hits.items()))
        return [Finding("WARN", "watch-words", f"{total} watch words ({listed}); rewrite toward specifics")]
    return []


def check_podcast_markdown(body: str) -> list[Finding]:
    bold = body.count("**") // 2
    bullets = len(re.findall(r"^\s*(?:[-*]|\d+\.)\s+", body, re.M))
    if bold + bullets > 2:
        return [Finding("WARN", "podcast-markdown",
                        f"{bold} bold spans and {bullets} list items; listeners can't see formatting, say it")]
    return []


def check_specificity(prose: str) -> list[Finding]:
    n_words = len(words(prose))
    if n_words < 300:
        return []
    numbers = len(re.findall(r"\b\d[\d,.:%]*\b", prose))
    quotes = len(re.findall(r"[\"“][^\"”]{8,}[\"”]", prose))
    per_300 = (numbers + quotes) * 300 / n_words
    if per_300 < 1:
        return [Finding("WARN", "specificity",
                        f"Only {numbers} numbers and {quotes} quotes in {n_words} words; add concrete detail")]
    return []


def check_needs(raw: str) -> list[Finding]:
    return [Finding("INFO", "needs-marker", m.group(0), line_of(raw, m.start()))
            for m in NEEDS_RE.finditer(raw)]


def check_loops(raw: str) -> list[Finding]:
    opened = [(m.group(1).lower(), m.start()) for m in LOOP_RE.finditer(raw)]
    closed = {m.group(1).lower(): m.start() for m in CLOSE_RE.finditer(raw)}
    found = []
    for loop_id, pos in opened:
        if loop_id not in closed:
            found.append(Finding("ERROR", "open-loop", f'Loop "{loop_id}" is never closed', line_of(raw, pos)))
        elif closed[loop_id] < pos:
            found.append(Finding("ERROR", "loop-order", f'Loop "{loop_id}" closes before it opens', line_of(raw, pos)))
    opened_ids = {i for i, _ in opened}
    for loop_id, pos in closed.items():
        if loop_id not in opened_ids:
            found.append(Finding("WARN", "orphan-close", f'CLOSE "{loop_id}" has no LOOP', line_of(raw, pos)))
    return found


# ---------- podcast-only ----------

def check_rehooks(body: str) -> list[Finding]:
    chunks = REHOOK_RE.split(body)
    gaps = [len(words(clean_prose(c))) for c in chunks]
    total = sum(gaps)
    if total < 600:
        return []
    if len(chunks) == 1:
        return [Finding("ERROR", "rehook", f"No [REHOOK] markers in {total} words; re-hook every ~225 words")]
    worst = max(gaps)
    if worst > REHOOK_MAX_GAP_WORDS:
        return [Finding("WARN", "rehook-gap",
                        f"Longest stretch without a re-hook is {worst} words (~{worst / 150:.1f} min)")]
    return []


# ---------- blog-only ----------

def check_blog_structure(meta: dict[str, str], body: str) -> list[Finding]:
    found = []
    h1 = re.findall(r"^#\s+(.+)$", body, re.M)
    h2 = re.findall(r"^##\s+(.+)$", body, re.M)
    if len(h1) != 1:
        found.append(Finding("ERROR", "h1", f"Found {len(h1)} H1 headings; need exactly 1"))
    if len(h2) < 3:
        found.append(Finding("WARN", "h2", f"Only {len(h2)} H2 sections"))
    content_h2 = [h for h in h2 if not re.search(r"takeaway|faq|frequently", h, re.I)]
    questions = [h for h in content_h2 if h.strip().endswith("?")]
    if content_h2 and len(questions) / len(content_h2) < 0.3:
        found.append(Finding("WARN", "h2-questions",
                             "Under 30% of H2s are questions; answer engines match question headings"))
    if not re.search(r"^##\s+.*(faq|frequently asked)", body, re.I | re.M):
        found.append(Finding("WARN", "faq", "No FAQ section"))
    if not re.search(r"^##\s+.*takeaway", body, re.I | re.M):
        found.append(Finding("WARN", "takeaways", "No Key takeaways section"))
    found.extend(check_answer_first(body))
    found.extend(check_meta(meta, body, h1[0] if h1 else ""))
    return found


def check_answer_first(body: str) -> list[Finding]:
    found = []
    for match in re.finditer(r"^##\s+(.+\?)\s*$", body, re.M):
        rest = body[match.end():].lstrip("\n")
        para = rest.split("\n\n", 1)[0]
        first = sentences(clean_prose(para))
        if first and len(words(first[0])) > 30:
            found.append(Finding("WARN", "answer-first",
                                 f'"{match.group(1)}": first sentence is {len(words(first[0]))} words; '
                                 "lead with a short direct answer", line_of(body, match.start())))
    return found


def check_meta(meta: dict[str, str], body: str, h1: str) -> list[Finding]:
    if not meta:
        return [Finding("ERROR", "frontmatter", "No frontmatter (title, meta_description, primary_keyword...)")]
    found = []
    title = meta.get("title", "")
    desc = meta.get("meta_description", "")
    kw = meta.get("primary_keyword", "").lower()
    if not title or len(title) > 60:
        found.append(Finding("ERROR", "title", f"Title missing or over 60 chars ({len(title)})"))
    if not 120 <= len(desc) <= 160:
        found.append(Finding("ERROR", "meta-description", f"Meta description is {len(desc)} chars; need 120–160"))
    if not kw:
        found.append(Finding("ERROR", "keyword", "No primary_keyword in frontmatter"))
        return found
    first_100 = " ".join(words(clean_prose(body))[:100]).lower()
    if kw not in first_100:
        found.append(Finding("WARN", "keyword-intro", f'Primary keyword "{kw}" not in first 100 words'))
    if kw not in (title + " " + h1).lower():
        found.append(Finding("WARN", "keyword-title", f'Primary keyword "{kw}" not in title or H1'))
    return found


# ---------- runner ----------

def lint(text: str, mode: str, banned: Iterable[str], brand: dict,
         watch: Iterable[str] = ()) -> list[Finding]:
    meta, body = split_frontmatter(text)
    prose = clean_prose(body)
    findings: list[Finding] = []
    findings += check_banned(body, banned)
    findings += check_brand_terms(body, brand)
    findings += check_first_line(prose, mode)
    findings += check_rhythm(prose, mode)
    findings += check_hedges(prose)
    findings += check_dashes(prose)
    findings += check_structural_tells(prose)
    findings += check_tidy_ending(prose)
    findings += check_watch_words(prose, watch)
    findings += check_specificity(prose)
    findings += check_loops(body)
    findings += check_needs(body)
    n_words = len(words(prose))
    if n_words < LIMITS[mode]["min_words"]:
        findings.append(Finding("WARN", "length", f"Only {n_words} words"))
    if mode == "podcast":
        findings += check_rehooks(body)
        findings += check_podcast_markdown(body)
    else:
        findings += check_blog_structure(meta, body)
    return findings


def format_report(findings: list[Finding], path: str) -> str:
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    rows = sorted(findings, key=lambda f: (order[f.level], f.line or 0))
    counts = {lvl: sum(1 for f in findings if f.level == lvl) for lvl in order}
    lines = [f"{path}: {counts['ERROR']} errors, {counts['WARN']} warnings, {counts['INFO']} notes"]
    for f in rows:
        where = f"L{f.line} " if f.line else ""
        lines.append(f"  {f.level:<5} {where}[{f.check}] {f.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--mode", choices=("blog", "podcast"), required=True)
    parser.add_argument("--brand", type=Path, default=None, help="brand.json from a brand pack")
    parser.add_argument("--banned", type=Path, default=DEFAULT_BANNED)
    parser.add_argument("--watch", type=Path, default=DEFAULT_WATCH)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Could not read {args.file}: {exc}", file=sys.stderr)
        return 2
    brand = load_brand(args.brand)
    banned = load_banned(args.banned) + tuple(p.lower() for p in brand.get("extra_banned_phrases", []))
    watch = load_banned(args.watch)  # same one-per-line format
    findings = lint(text, args.mode, banned, brand, watch)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        print(format_report(findings, str(args.file)))
    return 1 if any(f.level == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
