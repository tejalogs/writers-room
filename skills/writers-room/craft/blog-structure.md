# Blog Structure — for the scanner, the reader and the answer engine

A blog is read three ways at once:
1. **The scanner** skims headings and bold text in 10 seconds and decides whether to stay.
2. **The reader** reads every word if the scanner was convinced.
3. **The answer engine** (Google, AI Overviews, ChatGPT, Perplexity, Gemini) lifts self-contained chunks to quote.

Every structural choice must serve all three.

## Pick the post type first

| Type | Search intent | Spine | Length |
|---|---|---|---|
| **Answer post** | "why / how / what is" query | One question, answered surprisingly well | 1,200–1,800 |
| **Playbook** | "how to" with steps | A method with named steps | 1,500–2,500 |
| **Point of view** | No query; shareable | A contrarian belief, proven | 1,000–1,600 |
| **Story post** | Trust / brand | One real journey, with the lesson | 1,200–2,000 |
| **Comparison** | "X vs Y", "best X for" | An honest verdict, with criteria | 1,500–2,500 |
| **Data post** | Citations, links | Original numbers, interpreted | 1,000–2,000 |

## The default anatomy

```markdown
---
title: <= 60 chars, primary keyword near the front, specific promise
meta_description: 120–160 chars; answer + reason to click
slug: short-keyword-slug
primary_keyword: ...
secondary_keywords: [...]
author: <real person from brand pack>
updated: YYYY-MM-DD
---

# Title (one H1 only)

*Dek: one line that sharpens the promise.*

**Answer block:** 40–60 words that answer the title's question directly and completely, in plain language. This is the chunk answer engines quote.

Hook line + opening story (100–200 words). Real moment from the story bank.

## Key takeaways
- 3–5 bullets, each a complete claim (not a teaser)

## <Question the reader actually asks>?
First 1–2 sentences: the direct answer. **Key sentence in bold.**
Then depth: why, an example, a detail, data with source.
End on a forward pull (see bridges-and-loops.md).

## <Next question>?
...

## <The original section>
Something only this brand can say: its own data, story bank pattern, named framework. This is the information gain. Without it, the post doesn't ship.

## What to do next / The method
Concrete steps. Numbered if order matters.

## FAQ
4–6 real questions (from People Also Ask, forums, sales and support calls), each answered in 2–4 sentences that stand alone.

## <Closing question, e.g. "What should you do before your next X?">
Callback to the opening story + one action + soft CTA from the brand pack. Give the close its own H2: without one, it reads as part of the last FAQ answer.
```

## Section rules

1. **H2s as real questions** where the post type allows. Use the words searchers and customers actually use (mine them from calls, People Also Ask, Reddit), not clever labels. Clever goes in the body.
2. **Answer first, then earn it.** Each H2 opens with the direct answer, so the section works if lifted alone.
3. **Each section is self-contained:** name the subject again instead of "this" or "it" at the start of a section. An answer engine may quote section 4 without sections 1–3.
4. **Paragraphs:** 1–4 sentences. One idea each.
5. **Bold one key sentence per section**, the one a scanner should read if nothing else.
6. **Lists when the content is list-shaped; tables for comparisons.** Never turn an argument into bullets.
7. **Every claim with a number has a source and a date**, or it comes from the brand's own data and says so.
8. **The brand appears in the body at most twice before the closing CTA**, and only where it's genuinely the answer.

## What separates great blogs from SEO filler

- **Information gain:** at least one thing the top 10 results don't say. If everything in the post exists on page one already, it has no reason to rank and no reason to be cited.
- **A real human in it:** a story, a quote, a named author with real experience.
- **A point of view:** answer posts still take a position. "It depends" is never the whole answer: say what it depends on and what you'd do.
