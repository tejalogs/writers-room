# Changelog

## v0.2.1 — 2026-11-13

From the first real-world test (a portfolio post in Antigravity):

### Added
- **Interview stage** (`pipeline/00-interview.md`) for **personal mode**: when the piece is about the user (portfolio, About page, personal post, founder story, their own case study), the user is the story bank. Up to three open questions per round, follow-ups for scenes, numbers and exact words, a permission check before publishing numbers, approved story files, and a minimal personal brand pack.
- Eval scenario `personal-portfolio`.

### Fixed
- **No more example answers when asking the user for material.** A suggested anecdote the user accepts is still an invented story; `SKILL.md`, `AGENTS.md` and the mine stage now forbid it.
- A missing brand pack no longer means "neutral voice" for personal pieces; it triggers the interview.
- The linter reports any `[NEEDS …]` marker (e.g. `[NEEDS METRIC]`, `[NEEDS LINK]`), not just STORY and SOURCE.

## v0.2.0 — 2026-11-13

### Added
- **Ads** (`craft/ads-structure.md`): awareness levels, platform anatomy and limits (Google RSA, Meta, LinkedIn), ad patterns, variant matrices, and policy guardrails (personal attributes, health, finance, jobs, fake urgency).
- **Landing pages** (`craft/landing-page-structure.md`): the persuasion arc as a page, hero line by line, features → outcomes, real-proof rules, objections, CTAs and pre-ship checks.
- **Video, the filmmaker layer** (`craft/video-structure.md`): screen rules, shot vocabulary, storytelling devices turned into pictures, timed structures for 15/30/60 s, the A/V table format, on-screen text and VO pace, AI-video prompt briefs, and truth on screen.
- **Linter `--mode video`**: checks hook timing, missing visuals, on-screen text length, voice-over pace and timecode gaps, plus the shared language checks on VO and text. 9 new tests.
- **Examples across domains** (`craft/examples.md` §3): all eight hook types, generic → specific rewrites, declared → shown headlines and a Contradiction Hunt in SaaS, health, finance and travel.
- Critic panel: Director (video), Media Buyer (ads) and Conversion Editor (landing pages).
- Intake menu, brief and package stage cover ads, landing pages and video.

### Fixed
- Install no longer depends on Node.js: new `install.sh` (`curl … | bash`) installs into `.agents/skills/`, `~/.claude/skills/` (`--claude`) or any path, using git or curl + tar, and backs up existing installs. The skills CLI (`npx skills add`) needs Node.js 22.20+ (all versions since 1.5), which the README now says.

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
(The domain and format limitations are addressed in v0.2.0.)
