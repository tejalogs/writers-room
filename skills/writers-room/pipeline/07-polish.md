# Stage 7 — Polish

**Input:** `05-draft.md`, `06-critique.md`, `craft/word-craft.md` (now, not before).
**Output:** `final.md`

## Do, in this order

1. **Apply every must-fix** from the critique.
1b. **Word-craft pass:** run the swap drill from `craft/word-craft.md`, then the linter. Fix each flagged sentence with the revise loop (SKILL.md, step 3): rewrite toward a specific detail, never a synonym.
2. **Cut 15–20%.** Look first for: sentences that restate the previous one, throat-clearing openers, adjectives doing a number's job, examples that repeat a point already proven, hedges ("quite", "very", "really", "just", "actually").
3. **Line edit for rhythm.** Read each paragraph aloud. Vary sentence length. End paragraphs on the strongest word.
4. **Sharpen the quote-test line.** Find the one line someone would repeat. Make it shorter and give it its own paragraph.
5. **Check the callback.** The close returns to the opening image, now seen differently.
6. **Run the linter again.** Zero errors.
7. Blogs, social posts, ads and video A/V tables: strip loop markers. Podcasts: keep all markers (production script).
8. Write a separate `review.md` for the user (never put notes inside `final.md`: anything above the frontmatter breaks the blog lint and publishing). List every remaining `[NEEDS ...]` item (and remove those markers from the body of a blog `final.md`), every story id used, every claim that needs a fact check, and the ship status (which critics are below 4 and what would lift them).

9. Run `scripts/preserve.py 05-draft.md final.md --review review.md` and resolve anything it reports as lost.
10. **Hand-off message** (SKILL.md, step 4): what you made and where, the ship status, what's blocking, and one next step.

## Gate

All seven tests in `craft/principles.md` pass. Write one line per test in `06-critique.md` under "Final checks".
