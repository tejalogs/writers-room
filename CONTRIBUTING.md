# Contributing

Thanks for helping make AI-assisted writing less generic.

## The bar for changes

- **Craft changes** (`skills/writers-room/craft/`, `pipeline/`): explain *why* in the PR. Link to evidence (a study, a benchmark, a master's book) or show a before/after that proves the change helps. Opinions without examples are hard to review.
- **Never add invented examples presented as real.** Teaching examples must be labelled as illustrative.
- **No copyrighted passages.** Describe techniques in your own words; don't paste other writers' sentences.
- **Linter changes** (`scripts/lint.py`): add a test in `tests/`, keep the standard library only, and prefer WARN over ERROR for anything stylistic.
- **Banned and watch lists:** single words go in `watch-words.txt` (WARN by density), stable multi-word phrases in `banned-phrases.txt`. Note the date you reviewed them.

## Run the checks

```bash
python3 -m unittest discover -s tests -v
```

## Prove it works

If your change affects writing quality, run the scenarios in `skills/writers-room/evals/RUNNING.md` before and after, and paste the `compare.py` table plus your pairwise results in the PR.
