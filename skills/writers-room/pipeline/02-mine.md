# Stage 2 — Mine the material

**Input:** `01-brief.md`, the brand's `story-bank/stories/` (status `approved` only), sources supplied in the brief.
**Output:** `02-material.md`

## Do

1. Search the story bank by tags matching the audience segment, belief and topic. Pull **3–8 candidate stories**.
2. For each, copy: story id, the best verbatim line, the concrete detail, the belief, the turning point.
3. Pull **real questions** from the stories (customer words) for H2s and FAQ.
4. List facts and numbers with their sources. Anything without a source goes under "Unverified: do not use as fact".
5. Blogs, if you can browse: skim the top 5 results for the primary keyword. Write two lists: **"Everyone says"** (table stakes) and **"Nobody says"** (our information gain).
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

## Unverified (do not state as fact)
- ...

## Everyone says / Nobody says (blogs)
- ...
```
