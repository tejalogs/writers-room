# Ads Structure — text, image and video ads

An ad is the persuasion arc (`narrative.md` §10) compressed to a glance. It has one job: make the right person stop and take one next step. Everything in `principles.md` still applies; ads just have less room to get it wrong.

## Contents
1. Before writing: awareness, angle, offer
2. Platform anatomy and character limits
3. Ad patterns
4. Variants and testing
5. Policy and truth (read this before every health, finance, jobs or housing ad)

---

## 1. Before writing

1. **Awareness level** (Eugene Schwartz) decides the opening line:

   | Audience is... | Open with... | Example (budgeting app) |
   |---|---|---|
   | Unaware of the problem | The moment they'd recognise | "Declined. With £2,300 in savings." |
   | Problem-aware | The problem, named better than they can | "You know where your money goes. You just don't look." |
   | Solution-aware | Why this approach beats the one they're considering | "Spreadsheets track. They don't nudge." |
   | Product-aware | The offer, proof, or the objection that stopped them | "Free for 30 days. Cancel in two taps." |
   | Most aware | The offer and the CTA | "Your first month is on us. Start tonight." |

2. **The angle comes from the Contradiction Hunt** (`pipeline/03-angle.md`), never from the feature list. Run 3–5 angles, not one.
3. **One ad, one promise.** The landing page headline must match the ad's promise (message match); a mismatch wastes the click.
4. **The offer is concrete:** what they get, what it costs (time or money), what happens next.

## 2. Platform anatomy

Limits change: **check the platform's current specs before shipping.** These were the published limits at the time of writing.

| Platform | Parts | Limits / what shows |
|---|---|---|
| **Google Search (responsive search ads)** | Up to 15 headlines, 4 descriptions | Headlines ≤ 30 characters; descriptions ≤ 90. Each headline must make sense alone and in any combination |
| **Meta (Facebook / Instagram)** | Primary text, headline, description, CTA button | Only the first ~125 characters of primary text show before "more"; the headline is short (~27–40 characters show) |
| **LinkedIn** | Intro text, headline, CTA | ~150 characters of intro show before "see more"; keep headlines short (~70 characters) |
| **Video ads (any platform)** | See `video-structure.md` | Hook in the first 2–3 seconds; works with sound off |

**Google responsive search ad set (minimum):** 3 headlines with the keyword, 3 with the benefit or outcome, 2 with proof (real numbers, awards, reviews), 2 with the offer, 2 with a CTA, 1 that handles the main objection. Pin only when you must.

## 3. Ad patterns

| Pattern | Shape | Best for |
|---|---|---|
| **Recognition → turn** | A moment they've lived → the uncomfortable truth → the next step | Cold audiences |
| **Problem → agitate → solve** | Name the pain → show what it costs → the product | Problem-aware audiences. Don't over-agitate: no fear without a way out |
| **Before → after → bridge** | Their world now → their world with the outcome → how to get there | Outcome-led products. Before/after claims are restricted in health and finance (see §5) |
| **Proof-first** | A real number, review or result → what it means → CTA | Product-aware audiences; only with verified proof |
| **Objection-first** | The reason they haven't bought, said honestly → the answer | Retargeting |
| **Native / story** | Reads like a post, not an ad | Social feeds; still must be clearly an ad where the platform labels it |

**Line by line:**
- Line 1 does the hook alone; assume nothing else gets read.
- Sell the **outcome** (what changes for them), shown concretely, not features.
- One CTA, a verb plus an outcome ("See where your money went", not "Learn more" or "Submit").
- Specific beats clever. Clarity beats both.

## 4. Variants and testing

- Build a **variant matrix**: 3–5 angles × 2–3 hook types × formats. Change **one thing** per test so you learn something.
- Write 10+ hooks per angle; pick finalists with the pairwise judge (a large model or a human).
- Log each ad in the brand's `evals/performance-log.csv` with angle, device and hook type; judge on the business metric (leads, signups, sales), not clicks alone.

## 5. Policy and truth

Ads face legal and platform rules on top of the brand's own. **When in doubt, check the platform's current policy page.**

- **No personal-attribute assertions (Meta).** Don't imply you know the viewer's health, finances, ethnicity, religion, sexuality, criminal record or similar: avoid "Are you struggling with debt?", "Other diabetics like you...". Talk about the situation, not the viewer's attribute: "Debt can feel impossible to get on top of."
- **Health:** no cure, treatment or result claims without evidence the regulator accepts; no before/after body images where restricted; prescription and medical products often need certification.
- **Finance:** no guaranteed returns, no "get rich" framing, and representative examples and risk warnings where your regulator requires them (e.g. FCA in the UK). Credit, loans and crypto have special policies.
- **Jobs, housing and credit:** many platforms restrict targeting and wording to prevent discrimination; never imply who may or may not apply.
- **No fake urgency or scarcity** ("only 2 left!" when there aren't), no fake reviews, no invented testimonials, no actors presented as real customers.
- **Brand rules:** mirror every compliance rule as a `banned_terms` entry in `brand.json` so the linter catches it. Cover the implied versions too, not just the obvious word: "guarantee" is easy, but "you'll get interviews" makes the same promise. The template's `brand.json` shows a pattern for both.
