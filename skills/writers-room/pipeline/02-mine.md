# Stage 2 — Mine the material

**Input:** `01-brief.md`, the brand's `story-bank/stories/` (status `approved` only), sources supplied in the brief.
**Output:** `02-material.md`

## Do

1. Search the story bank by tags matching the audience segment, belief and topic. Pull **3–8 candidate stories**.
2. For each, copy: story id, the best verbatim line, the concrete detail, the belief, the turning point.
3. Pull **real questions** from the stories (customer words) for H2s and FAQ.
4. **Product facts (when the piece promotes a product or offer).** Collect what the product actually does and what the customer sees: the screens or steps, what they get at the end, how long it takes, the price, who it's for. Take them from the brand pack or ask the user with open questions. Anything unknown becomes `[NEEDS PRODUCT: what's missing]`. Never describe a screen, result or feature you haven't been told about.
5. List facts and numbers already supplied (brand proof, user sources) with their sources. Anything without a source goes under "Unverified: do not use as fact". Fresh research happens in stage 2b (`02b-research.md`).
6. If the story bank has nothing usable:
   - if the user lived the story (personal or portfolio pieces, their own projects), go back and run `00-interview.md`;
   - otherwise write `[NEEDS STORY: <the kind of moment needed>]` and tell the user what to look for in their calls or records.

   Never fill the gap with invention, a "composite" character, or sample answers for the user to pick from.

## Output format

```markdown
## Stories
- <id>: "<verbatim line>" — detail: ... — belief: ... — turn: ...

## Real questions (customer words)
- ...

## Facts (with source + date)
- ...

## Product facts
- ...

## Unverified (do not state as fact)
- ...
```
