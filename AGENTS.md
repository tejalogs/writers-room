# Writers' Room — instructions for any coding agent

When the user asks you to write, outline, rewrite or critique a **podcast script, blog post, article, essay, social post, ad, landing page or video script**, use the Writers' Room skill in `skills/writers-room/`:

1. Read `skills/writers-room/SKILL.md` and follow it exactly. It tells you which craft files to read and which pipeline stages to run.
2. Load the brand pack from `.writers-room/` in the user's project, or the path the user gives. If none exists, offer to create one from `skills/writers-room/brand-template/`.
3. Never invent stories, quotes, statistics, results or people. Mark gaps `[NEEDS STORY: ...]` / `[NEEDS SOURCE: ...]`. When the piece is about the user (portfolio, About page, personal post), interview them with `pipeline/00-interview.md`: up to three open questions per round, never with example answers.
4. Run `python3 skills/writers-room/scripts/lint.py <file> --mode blog|podcast|video|ad|social` after drafting and after polishing, then `scripts/preserve.py` on the draft and the final. If you can't run commands, apply `skills/writers-room/scripts/LINT-RULES.md` by hand.
5. Save every stage to `writers-room-output/<slug>/`. Stop after the angle and after the outline for the user's choice, unless they said "autopilot". End by telling the user which file to open and what's still missing.
6. Small local models: follow `skills/writers-room/pipeline/LITE.md` instead of the full pipeline.

Antigravity users: you can also add a workflow at `.agent/workflows/write.md` that says "Follow AGENTS.md for the user's writing request."
