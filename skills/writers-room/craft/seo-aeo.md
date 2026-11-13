# SEO and AEO — being found and being quoted

**SEO** gets the page ranked in search results. **AEO** (answer engine optimisation) gets the page's sentences quoted inside AI answers: Google AI Overviews, ChatGPT, Perplexity, Gemini, Claude. Good craft serves both; this file covers what craft alone misses.

## 1. Before writing: intent and questions

1. **Primary keyword + intent.** Decide what the searcher wants: an answer, a method, a comparison or a decision. The post type follows intent (see `blog-structure.md`). Wrong intent = no ranking, however good the writing.
2. **Question mining.** Collect 10–20 real questions about the topic from: People Also Ask, related searches, Reddit and forums, AI assistant follow-up suggestions, and above all **the brand's own sales and support calls** (the story bank). Customer-call questions are gold: competitors don't have them.
3. **Gap check.** Read the top 5 results (if you can browse). List what they all say (table stakes: cover briefly) and what none say (your information gain: cover deeply).

## 2. On the page

| Element | Rule |
|---|---|
| Title | ≤ 60 characters. Primary keyword near the front. A specific promise, not a label. |
| Meta description | 120–160 characters. The answer + a reason to click. |
| Slug | 3–6 words, keyword, no dates or stop words. |
| H1 | Exactly one. Matches the title's intent. |
| First 100 words | Contain the primary keyword naturally, and the answer block. |
| H2s | Real questions in searchers' words, or clear topic labels. Secondary keywords where natural. |
| Internal links | 2–4 to the brand's relevant pages (from the brand pack), with descriptive anchor text. Never "click here". |
| External links | 1–3 to primary sources for any statistic. |
| Author | A real named person with relevant experience, plus a bio line. |
| Updated date | Visible. Refresh posts with new data at least yearly. |

Never stuff keywords. If a sentence reads worse because of a keyword, take the keyword out.

## 3. Writing to be quoted (AEO)

AI engines retrieve **chunks** (a paragraph or section), not whole pages. They prefer chunks that are clear, specific, self-contained and attributable.

1. **Answer block** at the top: 40–60 words, complete on its own.
2. **Definitions as "X is Y" sentences:** "Role clarity is the ability to name the specific role you're targeting and explain why you fit it."
3. **Self-contained sections:** restate the subject; no "as mentioned above".
4. **Attributable claims:** "According to <brand>'s analysis of 300 consultations in 2026, ..." beats "studies show". Brand-attributed original data is the single strongest citation magnet.
5. **Named frameworks:** a named, numbered method ("the three-signal test") is easy to quote and attribute.
6. **Concrete numbers with dates and sources.**
7. **Consensus + addition:** agree with what's true in the common answer, then add what only you know. Engines favour content that is both consistent with trusted sources and adds something.
8. **FAQ section** with questions phrased the way people ask assistants (full sentences, conversational).

## 4. Structured data (stage 8 output)

- `Article` (or `BlogPosting`) with author, datePublished, dateModified, publisher.
- `FAQPage` for the FAQ block. Google shows FAQ rich results only for limited site types now, but the markup still helps machines parse question/answer pairs.
- `BreadcrumbList` if the site uses breadcrumbs.
- Podcasts: `PodcastEpisode` with the transcript linked.

Output JSON-LD in `package.md`; never invent fields (e.g. ratings) the page doesn't show.

## 5. After publishing (feeds the learning loop)

- Request indexing; add the post to the sitemap and, if the brand has one, `llms.txt`.
- At 14 and 60 days, log in the brand pack's `evals/performance-log.csv`: impressions, clicks, average position, AI citations observed (ask the major assistants the target questions and note who gets cited).
