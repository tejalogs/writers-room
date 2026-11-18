"""Hook checks: catch openings that carry no impact.

A dead hook either (a) opens with a stock move ("Imagine…", "Picture this…", "We've all been
there"), (b) builds a scene out of props every opening uses (coffee, laptop, alarm, rain) with
nothing specific, or (c) has no anchor at all: no number, name, quote or concrete claim.
"""
from __future__ import annotations

import re

from wr_text import Finding, sentences, words

DEAD_OPENER_RE = re.compile(
    r"^\W*(?:imagine|picture (?:this|yourself|it)|close your eyes|let'?s be honest|here'?s the thing|"
    r"we'?ve all been there|raise your hand|ever wondered|have you ever|let me tell you|"
    r"what if i told you|in a world where|it'?s no secret|you'?re not alone|let'?s talk about|"
    r"did you know|you know that feeling|there'?s a moment|think about it|we need to talk|"
    r"so,? here'?s|okay,? so|look,|listen,|story time)\b", re.I)

SECOND_PERSON_SCENE_RE = re.compile(
    r"^\W*(?:you'?re|you are) (?:sitting|standing|walking|lying|scrolling|staring|at your|in your|on your)|"
    r"^\W*it'?s \d{1,2}(?::\d{2})?\s?(?:am|pm)?[,.]? (?:and )?you\b", re.I)

FIRST_PERSON_ROUTINE_RE = re.compile(
    r"^\W*i (?:opened|woke|sat|walked|grabbed|poured|stared|looked|checked|logged)\b", re.I)

STOCK_PROPS = frozenset({
    "coffee", "latte", "mug", "cup", "laptop", "alarm", "sunrise", "sunlight", "sun", "rain", "raindrops",
    "window", "notifications", "notification", "scrolling", "scroll", "breath", "heart", "palms",
    "desk", "keyboard", "screen", "phone", "commute", "traffic", "morning", "monday",
})

ANCHOR_RE = re.compile(r"\d|[\"“”]|£|\$|€|₹")

# Words that make an unanchored hook mushy. A flat contrarian claim with none of these passes.
VAGUE_WORDS = frozenset({
    "feel", "feeling", "feelings", "struggle", "struggling", "overwhelmed", "everyone", "everybody",
    "sometimes", "life", "success", "dreams", "dream", "journey", "world", "things", "stuff",
    "amazing", "incredible", "truly", "really", "something", "somehow", "moment", "moments",
})


def _hook_text(text: str) -> str:
    """The first one or two sentences: what the reader sees before deciding."""
    sents = sentences(text)
    return " ".join(sents[:2]) if sents else text.strip()


def _has_anchor(hook: str) -> bool:
    if ANCHOR_RE.search(hook):
        return True
    # A capitalised word that isn't the first word of its sentence is likely a name, place or brand.
    pronouns = ("I", "I'm", "I've", "I'd", "I'll")
    return any(t[:1].isupper() and t not in pronouns
               for sent in (sentences(hook) or [hook]) for t in words(sent)[1:])


def check_hook(text: str, label: str = "Hook") -> list[Finding]:
    hook = _hook_text(text)
    first = sentences(hook)[0] if sentences(hook) else hook
    if not hook:
        return []
    found = []
    if DEAD_OPENER_RE.search(first):
        found.append(Finding("ERROR", "dead-hook",
                             f'{label} opens with a stock move: "{first[:70]}". Lead with the material itself.'))
    if SECOND_PERSON_SCENE_RE.search(first):
        found.append(Finding("ERROR", "dead-hook",
                             f'{label} puts the reader in a made-up scene: "{first[:70]}". Use a real moment or a fact.'))
    toks = {w.lower() for w in words(hook)}
    props = sorted(toks & STOCK_PROPS)
    anchored = _has_anchor(hook)
    if props and not anchored:
        found.append(Finding("WARN", "stock-scene",
                             f'{label} builds a scene from stock props ({", ".join(props[:4])}) with nothing '
                             "specific. A real scene needs a detail only this story has."))
    if FIRST_PERSON_ROUTINE_RE.search(first) and not anchored:
        found.append(Finding("WARN", "stock-scene",
                             f'{label} opens on a routine action ("{first[:50]}"). Start at the moment something changes.'))
    vague = sorted(toks & VAGUE_WORDS)
    if not anchored and vague and not found:
        found.append(Finding("WARN", "vague-hook",
                             f'{label} leans on vague words ({", ".join(vague[:3])}) with no anchor '
                             f'(number, name, quote or concrete claim): "{hook[:70]}"'))
    return found


def parse_hook_list(body: str) -> list[str]:
    """One hook per bullet or numbered line; falls back to one per non-empty line."""
    items = re.findall(r"^\s*(?:[-*]|\d+[.)])\s+(.+?)\s*$", body, re.M)
    if not items:
        items = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    # Drop trailing source tags like "(S-T001)" or "[claim 3]" from the text that gets judged.
    return [re.sub(r"\s*[\[(](?:S-[\w-]+|claim[^\])]*|source[^\])]*)[\])]\s*$", "", i, flags=re.I) for i in items]


def check_hook_list(body: str) -> list[Finding]:
    hooks = parse_hook_list(body)
    if not hooks:
        return [Finding("ERROR", "no-hooks", "No hooks found: write one per bullet")]
    found: list[Finding] = []
    for n, hook in enumerate(hooks, start=1):
        found.extend(check_hook(hook, label=f"Hook {n}"))
        if "[NEEDS" in hook:
            found.append(Finding("WARN", "placeholder-hook",
                                 f"Hook {n}'s anchor is a placeholder; it can't be a finalist until the source is found"))
        n_words = len(words(_hook_text(hook)))
        if n_words > 25:
            found.append(Finding("WARN", "hook-length", f"Hook {n} is {n_words} words; the line that hooks should be ≤ 20"))
    return found
