# Lint rules (apply by hand if you can't run `lint.py`)

**ERROR = must fix. WARN = fix or justify in `review.md`. INFO = for your notes.**

`lint.py` prints a **score out of 100**: each ERROR costs 10 points and each WARN costs 3. Ship at 80 or above with zero errors. `--fail-under 80` makes the script exit with an error below that, which is useful in CI.

**Deliberate exceptions:** put `<!-- wr-ignore: check-id -->` anywhere in the file to silence a check for the whole file, or `<!-- wr-ignore-line: check-id -->` on a line to silence it there. Say why in `review.md`.

## Every mode
- ERROR: any phrase from `craft/banned-phrases.txt` or the brand's `extra_banned_phrases`.
- ERROR: any brand `banned_terms` match at ERROR severity; any brand-name misspelling.
- WARN: words from `craft/watch-words.txt` above ~2 per 1,000 words, any one repeated, or 3+ inside a 150-word window (`watch-cluster`).
- WARN: structural tells:
  - "It's not X, it's Y" / "not just X, but Y" more than once per piece (or 1 per 1,000 words)
  - "rather than" more than 2 per 1,000 words
  - "serves as / stands as / acts as / boasts" more than once per piece
  - trailing ", highlighting / underscoring / reflecting / showcasing…" clauses more than once per piece
  - vague attribution: "experts say", "studies show", "research suggests" with no named source
  - unbacked frequency: "most people", "almost nobody", "everyone knows", "the vast majority"
- WARN: a percentage or "X in Y" statistic with no source cue in the same sentence (`unsourced-stat`). A `[NEEDS SOURCE]` marker counts as a cue.
- WARN: three or more sentences in a row starting with the same word (`repeated-opener`).
- WARN: spelling that doesn't match the brand's `"spelling"` (UK/US), or a mix of both when none is set.
- WARN: more than 8 hedge words (very, really, just, actually, basically, quite, simply) per 1,000 words, for pieces over 150 words.
- INFO: every `[NEEDS …]` marker.
- If `brand.json` sets `"lang"` to anything other than `en`, the English-only checks above are skipped.

Fix flagged sentences by rewriting toward a specific detail (a number, a name, a source, the person's own words), never by swapping in a synonym.

## Hooks (every mode checks the opening; `--mode hooks` checks a bullet list)
- ERROR (`dead-hook`): the opening asks the reader to imagine or picture a scene, puts "you" in a made-up scene, or opens with a stock move ("We've all been there", "In a world where", "Did you know", "Let's be honest"…).
- WARN (`stock-scene`): the scene is built from props every opening uses (coffee, laptop, alarm, rain, morning, screen…) with no number, name or quote; or it opens on a routine action ("I opened…", "I woke…") with nothing specific.
- WARN (`vague-hook`): no anchor (number, name, quote or concrete claim) and vague words (feel, struggle, life, journey, something…).
- WARN (`hook-length`, hooks mode): a hook over 25 words.
- The fix is never a synonym: give the hook an anchor from the material. See `evals/hook-gate.md`.

## Blog and podcast (long form)
- ERROR: opening with throat-clearing ("Welcome to", "In this episode/article", "Today we", "Have you ever", "In today's", "Let's dive", greetings).
- ERROR: a `[LOOP: id]` with no matching `[CLOSE: id]` after it.
- WARN: first sentence over 15 words (podcast) / 20 words (blog).
- WARN: sentence lengths barely vary (standard deviation under ~4.5 words).
- WARN: fewer than one number or quotation per 300 words.
- WARN: a final paragraph opening with a tidy moral ("Ultimately", "In the end", "The future is…").
- INFO: more than one em dash per 200 words.

### Podcast
- ERROR: any sentence over 25 words.
- WARN: average sentence over 17 words.
- ERROR: a script over 600 words with no `[REHOOK]` markers. WARN: any stretch over ~260 words without one.
- WARN: more than 2 bold spans or list items (listeners can't see formatting).
- Note: the 25-word cap and ~260-word re-hook spacing are craft rules of thumb, not measured thresholds.

### Blog (also landing pages; ignore the blog-only structure warnings for those)
- ERROR: no frontmatter; title missing or over 60 characters; meta description outside 120–160 characters; no primary keyword.
- ERROR: not exactly one H1.
- WARN: fewer than 3 H2s; under 30% of content H2s phrased as questions; no FAQ; no Key takeaways.
- WARN: a question H2 whose first sentence runs over 30 words (answer first).
- WARN: primary keyword not in the first 100 words, or not in the title/H1.
- WARN: sentences over 35 words.

## Video (`--mode video`, A/V table)
- ERROR: no A/V table (`| 0:00–0:02 | Visual | Audio | On-screen text |` rows).
- ERROR: a row with no visual, or an end time not after its start time.
- WARN: the first shot doesn't start at 0:00 or runs past 0:03 (late hook).
- WARN: on-screen text over 8 words in one row.
- WARN: voice-over faster than 2.7 words per second (text after `VO:` in the Audio column).
- WARN: a gap or overlap between consecutive timecodes.

## Ad (`--mode ad`)
Write ads under H2 headings the linter recognises, one variant per bullet:
`## Google headlines`, `## Google descriptions`, `## Meta headlines`, `## Meta primary text`, `## LinkedIn headlines`, `## LinkedIn intro`.
- ERROR: a Google headline over 30 characters or a Google description over 90.
- WARN: a Meta headline over 40 or a LinkedIn headline over 70 characters.
- WARN: the first line of Meta primary text over 125 characters, or of a LinkedIn intro over 150 (it gets cut before "more").
- WARN: fewer than 8 Google headlines, or duplicates.
- WARN: no recognised sections.
- Limits change: check each platform's current specs before shipping.

## Social (`--mode social`)
Set `platform:` in frontmatter (`linkedin`, `x`, `threads`, `instagram`, `youtube`). Separate thread posts with a line containing only `---`.
- ERROR: a post over the platform maximum (X 280, Threads 500, Instagram 2,200, LinkedIn 3,000 characters).
- ERROR: throat-clearing in the first line.
- WARN: a first line longer than what shows before the cut (~140 LinkedIn, 125 Instagram, 150 YouTube).
- WARN: more than 3 hashtags; ending on a generic "Thoughts?".
