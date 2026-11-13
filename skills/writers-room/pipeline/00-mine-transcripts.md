# Stage 0 — Mine transcripts into stories (run when feeding the story bank)

**Input:** one anonymised transcript (output of `scripts/anonymize.py`, already read by a human).
**Output:** 0–5 story files in `<brand>/story-bank/stories/`, using `brand-template/story-bank/story-template.md`, each with `status: draft`.

## Do

1. **Re-check anonymisation first.** If you see any name, employer, school, email, phone, address or other identifier that survived, STOP and list it for the human. Do not write stories from that transcript until it's fixed.
2. Read the whole transcript. Look for **moments**, not summaries:
   - a line that is raw, specific or surprising (verbatim, under 40 words)
   - a belief the person holds about their situation ("I just need more applications")
   - a turning point (something they realised, or were told, that changed things)
   - a concrete detail (a number, a time, a ritual, an object: "the spreadsheet")
   - a question they asked that others will ask too (gold for FAQ and H2s)
3. A story file needs **at least** one verbatim line and one concrete detail. Skip anything that doesn't have both.
4. **Record only what was said.** Never infer outcomes ("she got the job") that the transcript doesn't state. Never infer ethnicity, origin or religion from anything except what the person said about themselves.
5. Tag each story so writers can find it: audience segment, emotion, belief, topic.

## Gate

- Every quote is verbatim from the transcript.
- No identifiers.
- `status: draft` until the human changes it to `approved`. Writers may only use `approved` stories.
