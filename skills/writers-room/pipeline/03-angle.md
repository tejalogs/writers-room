# Stage 3 — Angle

**Input:** `01-brief.md`, `02-material.md`, `craft/hooks.md`, brand `evals/what-works.md` if present.
**Output:** `03-angle.md`

The angle is the most important decision in the piece. A great angle with average sentences beats a weak angle with beautiful ones.

## Do

0. **Start from human behaviour, never from the product.** Write 3–5 "why do people...?" questions about the audience's behaviour ("Why do people keep applying to jobs when nobody replies?"). The product or brand doesn't appear at this step at all.

0b. **Run the Contradiction Hunt** on the strongest question. Fill all five lines from the material (story bank wording where possible):

   | | |
   |---|---|
   | What they **believe** | "I'm preparing for interviews." |
   | What they **do** | Watch interview videos. |
   | What they **expect** | To feel confident. |
   | What they **experience** | They freeze on an unfamiliar question. |
   | The **uncomfortable truth** connecting the gap | Watching a skill isn't the same as practising it. |

   The uncomfortable truth is usually your spine. If you can't fill the "experience" line from real material, you don't have the piece yet: mark `[NEEDS STORY]`.

1. Write **5 different angles**. Each is: a spine sentence (≤ 20 words) + the belief it overturns + the story that proves it. Make them genuinely different (different enemy, different story, different promise), not rewordings.
   Angle generators to try:
   - **The contradiction:** the uncomfortable truth from step 0b, stated flatly.
   - **The collision:** connect the problem to an unrelated situation that shares its shape ("job hunting is like dating: you keep sending messages, nobody replies, and you start changing your photo instead of asking who you're messaging"). Test it: the parallel must hold for at least three points, or it's a gimmick.
   - **Invert the advice:** what common advice is wrong here?
   - **The hidden cost:** what is the reader's current behaviour quietly costing them?
   - **The wrong question:** what are they asking that they shouldn't be?
   - **The insider view:** what does the other side (hiring manager, buyer, expert) see that they don't?
   - **The pattern:** what did we see across many stories that no single person would notice?
1b. **Pick the storytelling device** that best carries the winning idea, not the default "explain it" mode:

   | Device | What it is | Truth guardrail |
   |---|---|---|
   | **Parallel paths** | Two people with similar starts make different choices; outcomes diverge | Both must be real, or the piece says plainly it's a hypothetical |
   | **Behind the scenes** | What the other side sees (a recruiter's screen, a buyer's checklist) | Based on sourced or first-hand knowledge, never guessed |
   | **Visual metaphor** | The abstract problem as a physical thing (career confusion as a maze) | Keep it consistent; drop it if it needs explaining |
   | **Confession** | Someone admits a mistake or a realisation | Real person, real words (story bank or author's own) |
   | **Satire / exaggeration** | Real behaviour pushed to absurdity to make a truth memorable | Obviously exaggerated; never presented as fact |
   | **Unexpected revelation** | Start with one explanation, reveal a different one | The reveal must be true and supported |

   Record the device in the output. The same idea told through a different device is a different piece; try two devices if the first feels flat.

2. Run the **competitor swap test** on each. Delete any a competitor could publish.
3. Pick the winner with `evals/pairwise-judge.md` (criterion: "Which would make a busy, sceptical person stop and need to know more, *and* can our material actually prove it?").
4. Write 10 hooks for the winning angle, using at least 5 hook types, or as many types as the material honestly supports (minimum 3; see `craft/hooks.md` rule 6). Run the pairwise tournament. Keep the top 2.
5. Write the **payoff line**: the sentence near the end that pays off the hook's promise.

## ⏸ Checkpoint

Unless the user said "autopilot", **stop here**. Show them the spine, the top 2–3 angles (one line each, with the story or fact behind it) and the top 2 hooks, and ask which to take. Don't outline until they answer.

## Output format

```markdown
## Behaviour questions
## Contradiction Hunt (believe / do / expect / experience / truth)
## Angles considered
1. Spine: ... | Overturns: ... | Proof: <story id> | Swap test: pass/fail
...
## Winner + why + device
## Hooks (10) → top 2
## Payoff line
```
