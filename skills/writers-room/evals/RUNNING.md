# Running the evals — does the skill actually make writing better?

Anthropic's skill guidance: build evaluations first, compare against a run **without** the skill, and test on more than one model size. There's no built-in runner, so this is a short manual protocol.

## Setup

- Scenarios: `evals/scenarios.json` (7 scenarios with checkable expected behaviours: blog, podcast, no material, social post, no brand pack, video ad, landing page).
- Fixture brand pack: `evals/fixtures/brand/` (a fictional brand with two approved test stories).

## Protocol

1. **Baseline:** in a fresh session *without* the skill installed, give the model each scenario's `prompt` (paste the fixture `BRAND.md` and stories into the chat). Save each final piece as `runs/<model>/baseline/<scenario-id>.md`.
2. **With skill:** in a fresh session *with* the skill, run each prompt. Save `final.md` as `runs/<model>/skill/<scenario-id>.md`.
3. **Expected behaviours:** for each scenario, tick each `expected_behaviors` item pass/fail for both runs. Record in `runs/<model>/results.md`.
4. **Mechanical comparison:**
   ```bash
   python3 scripts/compare.py --a runs/<model>/baseline --b runs/<model>/skill --mode blog --brand evals/fixtures/brand/brand.json
   ```
5. **Quality comparison:** for each scenario, judge baseline vs skill with `evals/pairwise-judge.md` (criterion: "Which would a busy, sceptical reader finish and forward?"), order-swapped. Use a large model or a human, never a small model.
6. **Repeat on at least two model sizes** (e.g. a small and a frontier model).

## What "better" means

The skill passes when, on every model tested:
- expected-behaviour pass rate is higher with the skill;
- lint errors are lower;
- the skill version wins the majority of order-swapped pairwise judgements;
- the `no-material` scenario has **zero** invented people, quotes or numbers.

Re-run after any change to `craft/` or `pipeline/`. Keep `runs/` out of the published repo.
