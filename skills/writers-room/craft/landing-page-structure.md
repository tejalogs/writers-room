# Landing Page Structure — one page, one decision

A landing page exists for one decision: sign up, book, buy, download. Every section either moves the visitor toward that decision or answers a reason not to make it. Anything else is clutter.

## Contents
1. Before writing
2. The section order (the persuasion arc, as a page)
3. The hero, line by line
4. Features → outcomes
5. Proof
6. Objections and FAQ
7. Calls to action
8. Checks before shipping

---

## 1. Before writing

- **One goal per page.** One primary CTA. Navigation and other links compete with it; remove what you can.
- **Know where visitors come from.** Ad traffic needs **message match**: the headline repeats the ad's promise in the ad's words. Organic traffic needs the SEO basics from `seo-aeo.md` (title, meta description, one H1).
- **Know the awareness level** (`ads-structure.md` §1). Unaware visitors need recognition first; product-aware visitors need the offer and proof first. The section order below flexes accordingly.
- **Mine objections from real conversations:** sales calls, support tickets, reviews, the story bank. The objections people actually say are the FAQ.

## 2. The section order

| # | Section | Job | Persuasion arc step |
|---|---|---|---|
| 1 | **Hero** | Promise the outcome; show it's for them; one CTA | Hook + recognition |
| 2 | **The problem, in their words** | "That's me." A moment they've lived, not a list of pain points | Recognition |
| 3 | **The turn** | Why the usual fixes fail (the Contradiction Hunt's truth) | Tension + revelation |
| 4 | **How it works** | 3 steps, plainly, ideally with product visuals | Solution |
| 5 | **Outcomes** (not features) | What changes for them; see §4 | Solution |
| 6 | **Proof** | Real numbers, real reviews, real logos, real case stories | Credibility |
| 7 | **Objections / FAQ** | The 4–6 reasons people don't sign up, answered honestly | Removing friction |
| 8 | **Offer + final CTA** | What they get, what it costs, what happens next; repeat the hero promise | Action |

Product-aware traffic (retargeting, branded search): move proof and the offer up, and shorten sections 2–3.

## 3. The hero, line by line

- **Headline (≤ ~10 words):** the outcome, in the customer's words. Shown, not declared (see `examples.md` §3.3). Not the company name, not a slogan.
  - Declared: "Smart budgeting made easy" → Shown: "Find the money you didn't know you were spending"
- **Subheadline (1–2 sentences):** who it's for and how it works, concretely.
- **Primary CTA:** a verb plus the outcome ("Start my free month", "Book my assessment"). Add a friction-reducer underneath ("No card needed", "Cancel any time"), only if true.
- **Proof line:** one real, specific credibility signal (a rating with its count, a recognisable customer, a measured result). Leave it out rather than fake it.
- **Visual:** the product in use, or the outcome. Not abstract stock imagery.

## 4. Features → outcomes

For every feature, write the chain, and lead with the right-hand side:

| Feature (what it is) | So you can... (outcome) | Shown as (a moment) |
|---|---|---|
| Auto-categorised transactions | See where your money went without doing anything | "Open the app on payday: your month, already sorted." |
| Shared project page | Stop hunting for the latest version | "Every file, task and decision on one page." |

## 5. Proof

- **Only real proof:** verified numbers with dates, reviews from real customers (with permission), logos you're allowed to use, and case stories from the story bank.
- **Specific beats impressive:** "Rated 4.6 from 1,240 reviews" beats "Loved by thousands".
- **Put proof next to the claim it supports**, not only in a testimonial wall.
- No proof yet? Use honest substitutes: a clear guarantee you'll honour, a free trial, a transparent "how it works", a founder's note. Never fabricate.

## 6. Objections and FAQ

- Phrase questions the way customers ask them ("Can I cancel any time?", "Will this work if I'm self-employed?").
- Answer in 1–3 sentences, the direct answer first.
- Include the uncomfortable ones (price, time, "is this for me?"). An honest answer converts better than silence.
- Mark up with `FAQPage` JSON-LD if the page is meant to rank.

## 7. Calls to action

- Same primary CTA wording throughout the page; repeat it after sections 1, 5 and 8 on long pages.
- A secondary, lower-commitment CTA is fine for unaware traffic ("See how it works"), but visually quieter.
- Button copy completes the sentence "I want to...".

## 8. Checks before shipping

- **Five-second test:** show the hero for five seconds. Can someone say what it is, who it's for, and what to do next?
- **Message match:** does the headline repeat the ad's or search query's promise?
- **Proof audit:** is every number, review and logo real and permitted?
- **Mobile first:** the hero, CTA and proof fit the first phone screen.
- **Run the linter** on the copy (`--mode blog` checks clichés, watch words, structural tells, rhythm and brand rules; ignore its blog-only structure warnings).
- Every rule in `principles.md` still applies: true, specific, the visitor is the hero.
