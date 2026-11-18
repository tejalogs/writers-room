"""Shared text helpers for the Writers' Room scripts (standard library only)."""
from __future__ import annotations

import re
from dataclasses import dataclass

MARKER_RE = re.compile(r"\[(?:LOOP|CLOSE|REHOOK|PAUSE|EMPHASIS|SLOW|MUSIC|SFX|"
                       r"COLD OPEN|IDENT|PROMISE)[^\]]*\]", re.I)
NEEDS_RE = re.compile(r"\[NEEDS [A-Z]+[^\]]*\]")
SPEAKER_RE = re.compile(r"^\s*(?:HOST(?: [A-Z])?|GUEST|[A-Z]{2,}):\s*", re.M)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


@dataclass(frozen=True)
class Finding:
    level: str  # ERROR | WARN | INFO
    check: str
    message: str
    line: int | None = None


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
            meta = {**meta, key.strip(): value.strip().strip('"').strip("'")}
    return meta, text[end + 4:].lstrip("\n")


def strip_markers(text: str) -> str:
    return MARKER_RE.sub("", text)


def prose_lines(body: str) -> list[str]:
    """Lines that are prose (not headings, code fences, tables or block quotes)."""
    out, in_code = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith(("#", "|", ">")):
            continue
        out.append(line)
    return out


def clean_prose(body: str, keep_needs: bool = False) -> str:
    text = "\n".join(prose_lines(HTML_COMMENT_RE.sub("", body)))
    text = SPEAKER_RE.sub("", text)
    text = strip_markers(text)
    if not keep_needs:
        text = NEEDS_RE.sub("", text)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text.replace("- ", " ")).strip()
    parts = re.split(r"(?<=[.!?])[\"'”’)]*\s+(?=[\"'“‘(\[]*[A-Z0-9])", flat)
    return [p.strip() for p in parts if len(p.split()) >= 2]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9'’-]+", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1
