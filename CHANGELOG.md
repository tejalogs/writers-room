# Changelog

## Unreleased

Hooks were the weakest part in user tests. With no real story to hand, models opened with "Imagine you're walking…" or "I opened my laptop, coffee in hand…": scenes built from props that tell the reader nothing.

### Added
- **Hook checker** (`scripts/hooks_check.py`), run on the opening in every linter mode:
  - `dead-hook` (ERROR): "imagine / picture this" openings, made-up "you" scenes, stock moves such as "we've all been there" and "in a world where".
  - `stock-scene` (WARN): scenes built from coffee, laptops, alarms and screens with no number, name or quote; routine openings ("I opened…").
  - `vague-hook` (WARN): no anchor plus vague words.
  - `placeholder-hook` (WARN): an anchor that's still a `[NEEDS SOURCE]` marker.
- **`--mode hooks`** lints the stage-3 list of ten hooks, one per bullet.
- **`evals/hook-gate.md`:** six questions per finalist (anchor, swap, truth, change, gap, payoff), dead patterns with the fix for each, and what to do when every hook fails.

### Changed
- **Every hook now carries an anchor** (a number, name, exact quote or the claim the piece proves) and a source tag. A table maps your material to the hook types it can support. Cold opens are allowed only from a real moment with a detail only that story has.
- The phrase list moved out of `hooks.md` and into the linter and the gate, so writing instructions stay positive.
- The lite path and the angle stage both lint hooks before picking.

Tested with two fresh agents (one with story material, one with none). Neither produced an "imagine" or stock-prop hook. The linter scored the story hooks 100/100 and caught the one planted dead hook. 96 tests.

## v0.3.0 — 2026-11-18

From a fresh-eyes review of the repo and a scan of 13 related projects (Vale, proselint, slopless, STORM, humanizer, avoid-ai-writing, voiceprint, WritingBench and others).

### Added
- **Checkpoints:** the agent stops after the angle (you pick) and after the outline (you approve). "Autopilot" skips the pauses and records each choice in `review.md`.
- **Hand-off message:** every run ends with which file to open, the ship status, what's blocking and one next step.
- **Per-stage loading:** `SKILL.md` now lists exactly which files each stage loads, instead of loading all the craft files up front.
- **Lite path** (`pipeline/LITE.md` and `craft/lite.md`): four stages and a one-page cheat sheet for 4–8B local models. The small model writes, code checks, and a larger model or the user chooses.
- **Research stage** (`pipeline/02b-research.md`): reader and sceptic perspectives, a claims table with source, date and confidence for every fact, and an unused-material check. Also **no-story mode** for explainers, how-tos, comparisons and data posts.
- **Linter v2:**
  - `--mode ad` (Google, Meta and LinkedIn character limits, headline count, duplicates) and `--mode social` (per-platform post limits, the "see more" cut, hashtags, lazy closing questions).
  - New checks: unsourced statistics, repeated sentence openers, UK/US spelling consistency, watch words clustering in a 150-word window.
  - A score out of 100 with `--fail-under` for CI; `<!-- wr-ignore -->` and `<!-- wr-ignore-line -->` comments for deliberate exceptions; a `lang` setting that switches off the English-only checks.
  - Split into small modules (`wr_text.py`, `checks_v2.py`, `formats.py`).
- **`preserve.py`:** checks that polishing didn't drop a real quote, a `[NEEDS …]` marker or a link.
- 26 new tests (78 in total).

### Changed
- README, banner and plugin descriptions rewritten without marketing filler. Gone: "actually finish", "world-class", the emoji feature grid, "ship it".
- The brand template says nine questions, matching its nine sections.

## v0.2.2 — 2026-11-13

From an end-to-end audit (fresh agents running the portfolio, no-material and video-ad scenarios):

### Fixed
- **Anonymiser privacy gaps:** bare-domain URLs (`linkedin.com/in/someone`) were not removed; a first name alone ("Meera") got a different tag from the full name ("Meera Rao"), so one person read as two.
- **Linter:** `[NEEDS …]` markers no longer count toward sentence length.
- **Draft stage:** don't narrate missing material to the reader; voice samples supply rhythm, never facts; fixed-length formats write variants instead of over-length drafts.
- **Product facts:** the mine stage now collects what the product actually does, with `[NEEDS PRODUCT]` for unknowns, so ads never describe screens or results nobody confirmed.
- **Judging fallback:** with no second model, show the user the top options instead of self-judging silently.
- Video: persistent supers and legal lines don't count toward on-screen text limits; loop markers are stripped from final A/V tables.
- Hooks: "at least 5 types" now reads "or as many as the material honestly supports (minimum 3)".
- Brand template: an implied-promise rule ("you'll get…") alongside "guarantee".
- Docs: contents for `masters.md`, `watch-words.txt` kept out of drafting, the illustrative label on the principles example, and the "nobody tells you" frequency claim removed from an "after" example.

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
