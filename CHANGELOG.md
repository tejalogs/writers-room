# Changelog

## v0.1.0 — 2026-11-13

First public release.

### Formats
- **Podcast scripts:** solo, two-host and interview guides, written for the ear, with cold opens, open loops, re-hooks and delivery markers.
- **Blog posts:** six post types, structured for scanners, readers and AI answer engines (answer block, question H2s, FAQ, JSON-LD).
- **Social posts:** LinkedIn, X posts and threads, captions, YouTube and episode descriptions, short-video scripts.
- **One idea → all formats:** stage 8 repurposes any piece into native social cuts.

### Craft
- Principles with seven ship tests (competitor swap, second line, quote, stranger, turn, Monday, twelve-year-old).
- Eight hook types, the hook stack, and AEO-friendly "answer as hook".
- Bridges and open loops with a loop ledger; but/therefore; callbacks.
- Narrative craft (scenes, character, pacing, the persuasion arc, the ethics of true stories).
- Word craft: clichés, machine tells, zombie nouns, the swap drill.
- Techniques from McPhee, Ira Glass, Gladwell, Michael Lewis, Wolfe, Zinsser, Orwell, Pinker, Clark, Feynman, the Heath brothers, Housel, Sugarman, Schwartz and Ogilvy.
- Before/after example bank and model passages.

### Pipeline and evals
- Eight stages: brief → mine → angle (Contradiction Hunt, collisions, six storytelling devices) → outline → draft → critique → polish → package.
- Seven-critic panel where every finding quotes a sentence; a Truth Editor checks quotes, sources, frequency claims and invented thoughts.
- Pairwise judge with order-swapping; small models generate, larger models or humans judge.
- Five eval scenarios, a fictional fixture brand, and `compare.py` for with/without-skill comparisons.

### Tools (Python standard library only)
- `lint.py`: banned phrases, watch-word density, structural tells ("not X but Y", copula avoidance, trailing -ing clauses), vague attributions, unbacked frequency claims, tidy endings, rhythm, hooks, loops, re-hooks and blog SEO/AEO structure, plus brand compliance rules.
- `anonymize.py`: strips emails, phones, URLs, postcodes, IDs and names from transcripts before they enter a story bank.

### Brands
- Brand template with voice samples, compliance rules mirrored in `brand.json`, a private story bank and a performance log (including leads and signups).

### Known limitations
- Banned and watch lists and the linter heuristics are English-only.
- Teaching examples are drawn mostly from one domain (careers); more domains are planned.
- No published baseline eval results yet. Run `evals/RUNNING.md` on your own models.
- No dedicated ad, landing-page or video-ad format yet.
