# Lint rules (apply by hand if you can't run `lint.py`)

**ERROR = must fix. WARN = fix or justify in the critique.**

## Both formats
- ERROR: any phrase from `craft/banned-phrases.txt` or the brand's `extra_banned_phrases`.
- ERROR: any brand `banned_terms` match; any brand-name misspelling.
- ERROR: opening with throat-clearing ("Welcome to", "In this episode/article", "Today we", "Have you ever", "In today's", "Let's dive", greetings).
- ERROR: a `[LOOP: id]` with no matching `[CLOSE: id]` after it.
- WARN: first sentence over 15 words (podcast) / 20 words (blog).
- WARN: sentence lengths barely vary (standard deviation under ~4.5 words).
- WARN: more than 8 hedge words (very, really, just, actually, basically, quite, simply) per 1,000 words.
- INFO: more than one em dash per 200 words (an older-model tell; newer models use fewer).
- WARN: fewer than one number or quotation per 300 words.
- WARN: words from `craft/watch-words.txt` above ~2 per 1,000 words, or any one repeated.
- WARN, structural tells (density matters more than any single word):
  - "It's not X, it's Y" / "not just X, but Y" more than once per piece (or 1 per 1,000 words)
  - "rather than" more than 2 per 1,000 words
  - "serves as / stands as / acts as / boasts" more than once per piece
  - trailing ", highlighting / underscoring / reflecting / showcasing..." clauses more than once per piece
  - any vague attribution: "experts say", "studies show", "research suggests" with no named source
  - any unbacked frequency claim: "most people", "almost nobody", "everyone knows", "the vast majority"
  - a final paragraph opening with a tidy moral ("Ultimately", "In the end", "The future is...")

Fix flagged sentences by rewriting toward a specific detail (number, name, source, the person's words), never by swapping in a synonym.
- INFO: list every `[NEEDS STORY/SOURCE]` marker.

## Podcast
- ERROR: any sentence over 25 words.
- WARN: average sentence over 17 words.
- ERROR: a script over 600 words with no `[REHOOK]` markers. WARN: any stretch over ~260 words without one.
- WARN: more than 2 bold spans or list items (listeners can't see formatting).
- Note: the 25-word cap and ~260-word re-hook spacing are craft rules of thumb, not measured thresholds.

## Video (`--mode video`, A/V table)
- ERROR: no A/V table (`| 0:00–0:02 | Visual | Audio | On-screen text |` rows).
- ERROR: a row with no visual, or an end time not after its start time.
- WARN: the first shot doesn't start at 0:00 or runs past 0:03 (late hook).
- WARN: on-screen text over 8 words in one row.
- WARN: voice-over faster than 2.7 words per second (text after `VO:` in the Audio column).
- WARN: a gap or overlap between consecutive timecodes.
- The shared language checks (banned phrases, brand rules, watch words, structural tells) run on the voice-over and on-screen text.

## Blog
- ERROR: no frontmatter; title missing or over 60 characters; meta description outside 120–160 characters; no primary keyword.
- ERROR: not exactly one H1.
- WARN: fewer than 3 H2s; under 30% of content H2s phrased as questions; no FAQ; no Key takeaways.
- WARN: a question H2 whose first sentence runs over 30 words (answer first).
- WARN: primary keyword not in the first 100 words, or not in the title/H1.
- WARN: sentences over 35 words.
