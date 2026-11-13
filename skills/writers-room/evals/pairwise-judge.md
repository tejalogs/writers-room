# Pairwise Judge — picking winners reliably

Models are inconsistent at scoring things out of 10, but better at "A or B?". Use this for hooks, angles, titles and any choice between options.

**Who may judge:** a large model (frontier class) or a human. In LitBench (2,480 human-labelled pairs), large models agreed with human readers ~70–73% of the time; 7–8B models only ~58–60%, close to chance. If you are a small model, generate the options and stop: don't run this bracket yourself.

**No second model available?** If you drafted the options and nobody else can judge, don't quietly judge yourself. Show the user your top 2–3 options with a one-line case for each and let them pick. If they'd rather you pick, say in `review.md` that the choice was self-judged.

**Verdict first, short reason after.** In the same study, asking the judge to reason at length before its verdict *lowered* accuracy. Keep the one-line format below.

## Prompt (use verbatim, one pair per call)

```
You are judging two options for the same piece.
Criterion: <one criterion, e.g. "Which first line makes a busy, sceptical <audience> need to read the second line?">
Context: <spine sentence + audience in one line>

Option A: <text>
Option B: <text>

Judge on the criterion only. Ignore length and polish.
Answer with exactly: "WINNER: A" or "WINNER: B" on the first line, then one sentence of reason. Do not write anything before the verdict.
```

## Procedure

1. **Knockout bracket:** pair options randomly; winners advance. 10 options → 4 rounds.
2. **Swap order:** judge each pair twice, A/B then B/A. If the verdict flips, it's a tie: keep both for the next round. Position bias is systematic and gets *stronger* the closer two options are in quality, so never skip the swap on close calls.
3. **Final two:** judge on a second criterion too (e.g. "Which can our material actually pay off?"). If they split, the user picks.
4. Record the bracket in the stage file so humans can see why something won.

## Criteria library

- Hook: "...makes a busy, sceptical <audience> need the second line?"
- Angle: "...would make a busy, sceptical person stop *and* can our material prove it?"
- Title: "...would you click from a search results page, and does it promise exactly what the post delivers?"
- Close: "...leaves the reader with a changed belief and a clear action?"
