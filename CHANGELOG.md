# Changelog

## Unreleased

### Added
- **Ads** (`craft/ads-structure.md`): awareness levels, platform anatomy and limits (Google RSA, Meta, LinkedIn), ad patterns, variant matrices, and policy guardrails (personal attributes, health, finance, jobs, fake urgency).
- **Landing pages** (`craft/landing-page-structure.md`): the persuasion arc as a page, hero line by line, features → outcomes, real-proof rules, objections, CTAs and pre-ship checks.
- **Video, the filmmaker layer** (`craft/video-structure.md`): screen rules, shot vocabulary, storytelling devices turned into pictures, timed structures for 15/30/60 s, the A/V table format, on-screen text and VO pace, AI-video prompt briefs, and truth on screen.
- **Linter `--mode video`**: checks hook timing, missing visuals, on-screen text length, voice-over pace and timecode gaps, plus the shared language checks on VO and text. 9 new tests.
- **Examples across domains** (`craft/examples.md` §3): all eight hook types, generic → specific rewrites, declared → shown headlines and a Contradiction Hunt in SaaS, health, finance and travel.
- Critic panel: Director (video), Media Buyer (ads) and Conversion Editor (landing pages).
- Intake menu, brief and package stage cover ads, landing pages and video.

### Fixed
- README: `npx skills add` needs Node.js 22.20+ (skills CLI v1.8.1 fails on Node 20). Added a dependency-free one-line install via `git clone`, tested in Antigravity.

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
(The domain and format limitations are addressed in Unreleased.)
