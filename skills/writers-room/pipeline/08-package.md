# Stage 8 — Package

**Input:** `final.md`, `01-brief.md`, the brand pack.
**Output:** `package.md`

## Blog

1. Final title (≤ 60 chars) + 2 alternates for testing.
2. Meta description (120–160 chars), slug.
3. JSON-LD: `BlogPosting` (author, dates, publisher from brand pack) + `FAQPage` from the FAQ section. No invented fields.
4. Internal links used, with anchor text.
5. **Repurposed cuts** (same truth, native to each format):
   - LinkedIn post (hook + 5–8 short paragraphs + question to close)
   - X thread (hook tweet + 5–7 tweets), or a single post
   - 3 short-video hooks (≤ 12 words each) with the beat each would cover
   - Email newsletter intro (≤ 120 words)
6. 3 target questions to check AI citations against in 14 days.

## Podcast

1. Episode title (≤ 60 chars) + 2 alternates.
2. Show notes: hook paragraph, 3 takeaway bullets, chapter list with estimated timestamps (150 wpm).
3. 3 clip moments: in-line, out-line, why it works standalone.
4. One quote-card line.
5. `PodcastEpisode` JSON-LD.
6. Blog spin-off: the H2 questions this episode answers.

## Video

1. Final A/V table + shot list (or AI-generation prompts per shot, with a character sheet).
2. Cut-downs: 15 s and 6 s versions, each with its own hook shot.
3. Aspect ratios needed (9:16, 4:5/1:1, 16:9) and what to reframe in each (text safe zones).
4. Thumbnail or cover frame, plus a first-frame text card.
5. Captions file (full VO transcript).

## Landing page

1. Final copy by section, with the CTA wording repeated consistently.
2. Title tag and meta description (if organic), `FAQPage` JSON-LD.
3. The 3 ads (or search queries) whose promise the headline must match.
4. One A/B test to run first (usually the headline).

## Learning-loop row

Add a pending row to the brand's `evals/performance-log.csv` with slug, format, angle type, storytelling device, hook type, publish date (blank until live). Leads, signups or sales and brand mentions are filled in later, from the brand's analytics. If the brand pack has no `evals/performance-log.csv` (or you can't write to it), put the row at the end of `package.md` and tell the user where to paste it.
