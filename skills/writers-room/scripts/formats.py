"""Ad and social linter modes: platform character limits and first-line visibility.

Limits change: they mirror craft/ads-structure.md and craft/social-structure.md at the time
of writing. Check each platform's current specs before shipping.
"""
from __future__ import annotations

import re

from wr_text import Finding, line_of

# (heading pattern, max characters, level, what is limited)
AD_SECTION_LIMITS: tuple[tuple[re.Pattern[str], int, str, str], ...] = (
    (re.compile(r"google.*headline", re.I), 30, "ERROR", "item"),
    (re.compile(r"google.*description", re.I), 90, "ERROR", "item"),
    (re.compile(r"(?:meta|facebook|instagram).*headline", re.I), 40, "WARN", "item"),
    (re.compile(r"linkedin.*headline", re.I), 70, "WARN", "item"),
    (re.compile(r"(?:meta|facebook|instagram).*primary", re.I), 125, "WARN", "first-line"),
    (re.compile(r"linkedin.*intro", re.I), 150, "WARN", "first-line"),
)

SOCIAL_LIMITS = {
    # platform: (first-line visible chars, max chars per post or None)
    "linkedin": (140, 3000),
    "x": (280, 280),
    "threads": (500, 500),
    "instagram": (125, 2200),
    "youtube": (150, 5000),
}
LAZY_CTA_RE = re.compile(r"(?:thoughts\?|what do you think\?|agree\?)\s*$", re.I)
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")


def _sections(body: str) -> list[tuple[str, int, str]]:
    """Split on H2 headings: (heading, line number, section text)."""
    matches = list(re.finditer(r"^##\s+(.+)$", body, re.M))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((m.group(1).strip(), line_of(body, m.start()), body[m.end():end]))
    return out


def _items(section: str) -> list[str]:
    bullets = re.findall(r"^\s*(?:[-*]|\d+[.)])\s+(.+?)\s*$", section, re.M)
    if bullets:
        return bullets
    return [p.strip() for p in re.split(r"\n\s*\n", section) if p.strip()]


def _first_line(text: str) -> str:
    return text.strip().splitlines()[0].strip() if text.strip() else ""


def check_ad(body: str) -> list[Finding]:
    found: list[Finding] = []
    matched = False
    for heading, line, text in _sections(body):
        for pattern, limit, level, kind in AD_SECTION_LIMITS:
            if not pattern.search(heading):
                continue
            matched = True
            items = _items(text)
            for item in items:
                target = item if kind == "item" else _first_line(item)
                if len(target) > limit:
                    what = "characters" if kind == "item" else "characters before the 'more' cut"
                    found.append(Finding(level, "ad-limit",
                                         f'{heading}: "{target[:50]}…" is {len(target)} {what} (max {limit})', line))
            if re.search(r"google.*headline", heading, re.I):
                if len(items) < 8:
                    found.append(Finding("WARN", "ad-variants",
                                         f"{heading}: only {len(items)} headlines; aim for 8–15 distinct ones", line))
                dupes = {i.lower() for i in items if [x.lower() for x in items].count(i.lower()) > 1}
                if dupes:
                    found.append(Finding("WARN", "ad-duplicates", f"{heading}: duplicate headlines", line))
    if not matched:
        found.append(Finding("WARN", "ad-sections",
                             "No recognised ad sections. Use H2s like '## Google headlines', "
                             "'## Google descriptions', '## Meta primary text', '## LinkedIn intro'"))
    return found


def ad_copy(body: str) -> str:
    return "\n\n".join(item for _, _, text in _sections(body) for item in _items(text))


def check_social(meta: dict[str, str], body: str) -> list[Finding]:
    platform = meta.get("platform", "linkedin").lower()
    found: list[Finding] = []
    if platform not in SOCIAL_LIMITS:
        return [Finding("WARN", "platform", f'Unknown platform "{platform}"; use one of {", ".join(SOCIAL_LIMITS)}')]
    if "platform" not in meta:
        found.append(Finding("INFO", "platform", "No platform in frontmatter; assuming linkedin"))
    visible, max_chars = SOCIAL_LIMITS[platform]
    posts = [p.strip() for p in re.split(r"^\s*---\s*$", body, flags=re.M) if p.strip()]
    for n, post in enumerate(posts, start=1):
        label = f"post {n}" if len(posts) > 1 else "post"
        first = _first_line(post)
        if n == 1 and len(first) > visible:
            found.append(Finding("WARN", "first-line-cut",
                                 f"First line is {len(first)} characters; only ~{visible} show before the cut"))
        if max_chars and len(post) > max_chars:
            found.append(Finding("ERROR", "post-length",
                                 f"{label} is {len(post)} characters (max {max_chars} on {platform})"))
    all_text = "\n".join(posts)
    tags = HASHTAG_RE.findall(all_text)
    if len(tags) > 3:
        found.append(Finding("WARN", "hashtags", f"{len(tags)} hashtags; use 0–3"))
    if posts and LAZY_CTA_RE.search(posts[-1]):
        found.append(Finding("WARN", "lazy-cta", 'Ends on a generic "Thoughts?"; ask a specific question'))
    return found


def social_copy(body: str) -> str:
    return re.sub(r"^\s*---\s*$", "\n", body, flags=re.M)
