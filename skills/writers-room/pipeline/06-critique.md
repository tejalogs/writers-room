# Stage 6 — Critique panel

**Input:** `05-draft.md` (lint-clean), `01-brief.md`, `evals/critic-panel.md`.
**Output:** `06-critique.md`

Run each critic in `evals/critic-panel.md` **as a separate pass**, following its "Rules for every critic": quote the sentence, name the failed question, propose a specific fix. Each pass reads the draft as that one critic only, cares about nothing else, and is harsh. If possible, use a different (and large) model from the one that drafted.

For each critic, output:

```markdown
## <Critic name> — <score 1–5>
- "<exact quoted sentence>" → fails: <which checklist question> → fix: <specific change>
- (3–7 items, worst first)
```

Then a **fix list**: every item scored as must-fix (anything from a critic scoring below 4, any truth or compliance issue) or nice-to-have.

## Gate

If any critic scores below 3, the problem is structural: go back to stage 4 (outline) or stage 3 (angle), not stage 7. Polishing won't save a weak spine.
