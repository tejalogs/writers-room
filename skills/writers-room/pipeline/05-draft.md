# Stage 5 — Draft

**Input:** `04-outline.md`, `02-material.md`, the format structure file, the brand's `BRAND.md` (including its voice samples), `craft/examples.md`.

**Not input:** `craft/word-craft.md` and `craft/banned-phrases.txt`. Don't load them here; listing words to avoid primes them. They're used in stage 7.
**Output:** `05-draft.md`

## Do

1. Draft **beat by beat**, following the outline exactly. Small models: draft one beat per call, giving the model the outline, the previous beat's last paragraph, and this beat's material.
2. Use the winning hook verbatim as the first line.
3. Quote story-bank lines **verbatim**. Don't polish a real person's words.
4. Keep loop markers in the draft: `[LOOP: id]`, `[CLOSE: id]`; podcasts also `[REHOOK]` and delivery markers.
5. Write in the brand voice: match the rhythm, sentence length and register of the voice samples in `BRAND.md` and the "after" examples in `craft/examples.md`. Borrow their moves, never their sentences or facts.
6. Leave `[NEEDS STORY: ...]` / `[NEEDS SOURCE: ...]` wherever material is missing. Never invent to fill. **Don't narrate the gap to the reader**: no "I don't have a story for this" or "I can't tell you the number" in the copy. Put the marker in and write the surrounding sentences as they'll read once the gap is filled. The gaps are for `review.md`, not for the audience.
6b. **Voice samples give you rhythm, never facts.** Don't lift claims, credentials or experiences from the samples in `BRAND.md` ("I hired for six years") into the piece unless the same fact appears in the brand's proof, the author bio or the story bank.
7. Aim 10–15% **over** target length: stage 7 cuts. Exception: fixed-length formats (video runtimes, ad character limits) never go over. Write 2–3 variants of the weakest beats or lines instead, so polish has options to choose from.

Then run the linter (see SKILL.md, step 3) and fix every ERROR with the revise loop before stage 6.

## Don't

- Don't open with context, definitions or greetings.
- Don't end any section on a summary.
- Don't mention the brand before the halfway point unless it's the direct answer to the question.
