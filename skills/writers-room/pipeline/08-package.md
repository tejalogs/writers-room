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

## Learning-loop row

Add a pending row to the brand's `evals/performance-log.csv` with slug, format, angle type, storytelling device, hook type, publish date (blank until live). Leads, signups or sales and brand mentions are filled in later, from the brand's analytics.
