# Lite pipeline (small local models, or "quick" requests)

Four stages. One stage per call. Each stage lists **exactly** what to load; load nothing else.

The small model **writes**; code **checks**; a larger model or the user **chooses**.

---

## L1. Brief and material

**Load:** this file, `craft/lite.md`, the brand's `BRAND.md` §1–5, the story bank (approved stories only).

Write `brief.md`:
```markdown
Format: <blog | podcast | social | ad | landing | video>   Length: <words or seconds>
Reader: <one sentence>
Belief we overturn: "..."
Truth we land: "..."
Spine (≤ 20 words): ...
Material: <story ids and their best verbatim line> | <facts with source>
Missing: [NEEDS STORY/SOURCE: ...]
```

## L2. Hooks and plan

**Load:** this file, `craft/lite.md`, `brief.md`.

Write `plan.md`:
1. Five first lines, each a different type: real moment · surprising fact · contradiction · question about the reader · someone's exact words. Skip a type if the material can't support it. Each line carries an anchor and a source tag, e.g. `212 applications. 198 "no reply". (S-T001)`.
2. A plan of 4–7 beats, one line each: `<what happens> | <material> | but/so → next beat`.

Save the first lines as a bullet list in `hooks.md` and run `python3 <skill-dir>/scripts/lint.py hooks.md --mode hooks`. Replace any line it flags.

**Then stop.** The user (or a larger model) picks the first line and approves the plan.

## L3. Draft, one beat at a time

**Load per call:** this file, `craft/lite.md`, the approved plan, the voice samples from `BRAND.md`, and the previous beat's last paragraph.

Write one beat per call into `draft.md`. Quote stories word for word. Leave `[NEEDS …]` where material is missing, and don't mention the gap to the reader.

## L4. Check and fix

Run:
```bash
python3 <skill-dir>/scripts/lint.py draft.md --mode <mode> --brand <brand-dir>/brand.json
```
For each flagged sentence, call the model with only that sentence and its neighbours: *"Rewrite this so it says something specific: a number, a name, a source or someone's exact words. Don't just swap the flagged word."* Repeat at most 3 times. Save the result as `final.md`, then run `scripts/preserve.py draft.md final.md` and `scripts/provenance.py final.md --material brief.md <brand-dir>`. Cut or mark every number and quote that provenance flags; small models invent numbers more often than anything else.

Hand off: tell the user where `final.md` is, what's still `[NEEDS …]`, and that a larger model or a human should do the final read.
