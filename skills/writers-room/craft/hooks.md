# Hooks — earning the next ten seconds

A hook is a **promise plus a gap**. It promises something the audience wants and opens a gap they need closed. The gap must be specific to this piece: if the hook would work on any piece about the topic, it fails the competitor swap test.

## Every hook carries an anchor

An **anchor** is one concrete thing **taken from your material** (the story bank, the stage-2b claims table, the brand pack) that only this piece has. If it isn't in the material, it isn't an anchor: it's an invention, however specific it sounds. With no material, your only anchors are the spine's claim and a sharp question.
- a **number** from the story bank or the research table ("212 applications", "41 of 300");
- a **name, place or object** from a real story ("Column F", "the 6:14 bus");
- someone's **exact words** ("'It felt like begging. I sent it anyway.'");
- a **specific claim** the piece will prove ("Applying to more jobs is making you less hireable").

Write the anchor's source after each hook: `(S-T001)`, `(claim 3)`, `(spine)`. If you can't name a source, the hook isn't ready.

- `(spine)` is valid only for a contrarian claim, a named enemy or a question that the piece itself will argue and prove. It never covers a number, a fact or a "most…" claim; those need a story id or a claims-table row.
- A hook whose anchor is still a `[NEEDS SOURCE]` placeholder can be listed, but it can't be a finalist until the source is found.

Atmosphere is not an anchor. Morning light, a coffee cup, a laptop opening and a deep breath appear in thousands of openings, so they tell the reader nothing about this one.

## Pick the type from your material

| What you have | Strongest hook types |
|---|---|
| A real moment (story bank or interview) | Cold open (1), overheard line (4), confession (7, only the author's own) |
| A surprising number or fact (research table) | Specific number (3), contrarian claim (2) |
| A belief you overturn, but no story yet | Contrarian claim (2), named enemy (8), implicating question (6) |
| Two real people with different outcomes | Two-people contrast (5) |

## The eight hook types

Each has a mechanism (why it works), a use case and a failure mode. Examples are illustrative patterns; in real pieces, the details must come from the story bank or a cited source. The examples below come from one domain (careers); `examples.md` §3.1 shows all eight types in SaaS, health, finance and travel.

### 1. Cold open in the scene
Start in the middle of a real moment, at the point of highest tension.
> "At 11:40 on a Sunday night she clicked submit for the 212th time, then opened a new tab and typed: *what is wrong with me.*"
- **Mechanism:** a story in progress triggers the need to know what happens next.
- **Use only when:** you have a real moment from the story bank or an interview. Cite it. Best default for podcasts when you have one.
- **The detail test:** the scene needs at least one detail only that story has (the 212th time, the search typed into a new tab). If every detail in your scene could appear in someone else's story (coffee, a laptop, the alarm), it isn't a scene yet. Use a different hook type.
- **Never build a scene the material doesn't contain**, including "you" scenes the reader is asked to picture. Starting with the moment itself is always stronger than asking the reader to imagine one.

### 2. The contrarian claim
State the opposite of what the audience believes, flatly, without hedging.
> "Applying to more jobs is making you less hireable."
- **Mechanism:** contradiction creates cognitive dissonance; they keep going to resolve it.
- **Use when:** the spine overturns a common belief. Best default for blogs and short-form.
- **Fails when:** it's contrarian for show and the piece can't prove it. The payoff must earn the claim.

### 3. The specific number
A precise, surprising figure, ideally your own data.
> "Of 300 candidates we spoke to last quarter, 41 had never been told why they were rejected. Not once."
- **Mechanism:** precision signals truth; surprise demands explanation.
- **Fails when:** the number is a recycled internet stat ("recruiters look for 6 seconds") or unsourced. Recycled stats are anti-hooks: the audience has heard them.

### 4. The overheard line
Open with a verbatim quote from a real person.
> "'I don't need a better CV. I need someone to tell me the truth.'"
- **Mechanism:** a human voice is instantly intimate; the audience wonders who said it and why.
- **Use when:** the story bank has a line that's sharp, raw, and stands alone.

### 5. The two-people contrast
Two people, same starting point, different outcomes; withhold the reason.
> "Same degree. Same city. Same target role. One had four interviews in a month. The other had none in six. The difference wasn't the CV."
- **Mechanism:** the audience starts guessing; guessing is engagement.

### 6. The implicating question
A question that makes the audience examine themselves, not a rhetorical one.
> "When did someone last tell you, specifically, why you didn't get the job?"
- **Fails when:** it's answerable with "no" and a shrug ("Have you ever wondered...?"). Banned.

### 7. The confession / stakes
The narrator admits a mistake or a risk.
> "I told a candidate to stop applying for a month. She was furious. I wasn't sure I was right."
- **Mechanism:** vulnerability builds trust; unresolved stakes create suspense.

### 8. The named enemy
Name a belief, habit or system as the antagonist.
> "There's a piece of advice that has wasted more job seekers' time than any other: 'it's a numbers game.'"
- **Mechanism:** a shared enemy aligns the audience with you.

## Hook rules

1. **First line:** 15 words or fewer for audio, 20 for text.
2. **Lead with the anchor.** Put the number, the name, the quote or the claim in the first five words if you can. Context comes after, if at all.
3. **Start at the change.** Open on the moment something shifted (the rejection, the number, the realisation), not on the routine before it.
4. **Pay it off.** Every hook's promise must be explicitly paid off. Write down the payoff line before you write the hook.
5. **The brand never appears in the hook.**
6. **Tournament every time:** write 10 hooks using at least 5 different types (or as many as the material supports), each tagged with its anchor's source. Run `lint.py hooks.md --mode hooks`, drop every hook it flags, then pick the winner with `evals/pairwise-judge.md`. Never ship your first hook.
7. **Skip types your material can't support.** No second person in the story bank means no two-people contrast; no author experience on record means no confession. Fill the 10 with more of the types you *can* support, and note which you skipped and why.

After the tournament, run the finalists through `evals/hook-gate.md`.

## The hook stack (longer pieces)

A single line isn't enough for a 15-minute episode or a 2,000-word post. Stack:

1. **Hook** (line 1): one of the eight types.
2. **Twist** (lines 2–3): complicate it. "And the worst part? She was doing everything the advice told her to."
3. **Promise** (lines 3–5): what the audience will walk away with, stated concretely. "By the end of this you'll know the three signals that tell you whether to keep applying or stop."
4. **First open loop:** a question the piece will answer later, not now. See `bridges-and-loops.md`.

## Blog hooks vs answer engines

AEO wants the direct answer in the first paragraph; craft wants tension. **Resolve it by making the answer the hook.** A surprising, direct answer is a contrarian hook:
> "**Why does a strong CV get no callbacks?** Usually because it's strong for the wrong role. Most CVs we review are optimised for the job the person *had*, not the one they want."

The answer is complete enough for an AI to quote, and surprising enough that a human keeps reading.
