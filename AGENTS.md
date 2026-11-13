# Writers' Room — instructions for any coding agent

When the user asks you to write, outline, rewrite or critique a **podcast script, blog post, article, essay, social post, ad, landing page or video script**, use the Writers' Room skill in `skills/writers-room/`:

1. Read `skills/writers-room/SKILL.md` and follow it exactly. It tells you which craft files to read and which pipeline stages to run.
2. Load the brand pack from `.writers-room/` in the user's project, or the path the user gives. If none exists, offer to create one from `skills/writers-room/brand-template/`.
3. Never invent stories, quotes, statistics, results or people. Mark gaps `[NEEDS STORY: ...]` / `[NEEDS SOURCE: ...]`. When the piece is about the user (portfolio, About page, personal post), interview them with `pipeline/00-interview.md`: up to three open questions per round, never with example answers.
4. Run `python3 skills/writers-room/scripts/lint.py <file> --mode blog|podcast|video` after drafting and after polishing. If you can't run commands, apply `skills/writers-room/scripts/LINT-RULES.md` by hand.
5. Save every stage to `writers-room-output/<slug>/` so the user can review the angle and outline before the draft.

Antigravity users: you can also add a workflow at `.agent/workflows/write.md` that says "Follow AGENTS.md for the user's writing request."
