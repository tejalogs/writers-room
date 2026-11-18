# Hook gate — checking hooks after they're written

Use this **after** generating hooks (stage 3, or L2 in the lite path), never as a prompt while writing them: a list of phrases to avoid primes the very phrases it lists. Generate from `craft/hooks.md` (anchors and types), then check here.

## 1. Run the linter

```bash
python3 <skill-dir>/scripts/lint.py hooks.md --mode hooks
```
One hook per bullet, each with its source tag. Drop every hook marked `dead-hook`. Rewrite or drop every `stock-scene` and `vague-hook`.

## 2. Ask six questions of each finalist

1. **Anchor:** does it contain a number, name, exact quote or specific claim from *our* material? Can you point to the story id or claim number?
2. **Swap test:** could this line open a different article on a different topic? If yes, it's generic.
3. **Truth:** did this happen, or is it a scene we built? Check every word of the hook against its source: a hook may compress the story but never add to it. "She replied to the 40th" is in the story; "she stopped archiving them" and "not one was a reply" are not. Hooks built from no material fail, however good they sound. So do absolutes the material can't back ("the only…", "most likely…").
4. **Change:** does it start at the moment something changes, rather than at the routine before it?
5. **Gap:** does it make the reader need the next line? Read only the hook, then ask "so what?". If there's no pull, it fails.
6. **Payoff:** does the piece deliver what the hook promises? Name the line where it pays off.

**Choosing the winner.** Show the user the top 2–3 surviving hooks at the stage 3 checkpoint. On autopilot, pick with `evals/pairwise-judge.md` if a second model is available; otherwise pick yourself and say so in `review.md`. If the linter can't run, apply `scripts/LINT-RULES.md` (Hooks section) by hand and note that it was a hand check.

## 3. Dead patterns, with what to do instead

These show up when a model writes hooks without material. Each one has a fix that comes from the material.

| Dead pattern | Why it fails | What to do instead |
|---|---|---|
| "Imagine you're walking into your dream interview…" | Asks the reader to build the scene; nothing real is on the page | Start with a real moment: "Her interview lasted 11 minutes. She found out why three weeks later." |
| "I opened my laptop. The coffee was still warm…" | Routine plus props found in thousands of openings; nothing has happened yet | Start at the change: "The rejection email arrived at 6:14. It was four lines long." |
| "You're sitting at your desk, staring at the screen…" | A generic "you" scene; the reader knows it's invented | Name the reader's real situation with an anchor: "You've sent 40 applications this month. How many got a reply?" |
| "We've all been there." / "Let's be honest…" | Claims a shared feeling instead of earning it | Show one person's real version of it, with their words |
| "In a world where…" / "Did you know…?" | Trailer and quiz openings; the reader has seen thousands | State the fact flatly: "41 of 300 had never been told why they were rejected." |
| "Sometimes life feels like a struggle…" | Vague words, no subject, no anchor | Make the claim the piece will prove: "Applying to more jobs is making you less hireable." |

(Illustrative examples. In real pieces, every number and moment must come from the story bank or the research table.)

## 4. If every hook fails

That usually means the material is thin, not the writing. Go back to stage 2 or 2b: find one real moment, one surprising number or one sharp quote. A strong contrarian claim from the spine is the fallback that needs no story.
