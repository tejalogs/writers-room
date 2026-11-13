import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from lint import DEFAULT_BANNED, lint, load_banned, sentences  # noqa: E402

BANNED = load_banned(DEFAULT_BANNED)


def checks(findings, level=None):
    return {f.check for f in findings if level is None or f.level == level}


GOOD_BLOG = """---
title: Why a strong CV gets no interview callbacks
meta_description: A strong CV with no interview callbacks is usually strong for the wrong role. Here is how to tell, and the one change that fixes it fast.
primary_keyword: interview callbacks
---

# Why a strong CV gets no interview callbacks

**Answer:** a strong CV that gets no interview callbacks is usually strong for the wrong role. It describes the job you had. Recruiters are hiring for the job you want.

Her spreadsheet had 212 rows. Column F said "no reply" 198 times. She had rewritten the CV four times.

## Key takeaways
- The CV was never the problem.

## Why does a good CV get rejected?
It is aimed at the wrong role. That is the short answer. The long one takes a story about a woman who wrote "results-driven" eleven times and meant it every time, because nobody had ever shown her what the hiring manager actually read first.

## What should you change first?
Pick one role. Then rewrite the top third for it. Nothing else matters until that is done, and most people skip it entirely.

## FAQ
Is it the ATS? Rarely.
"""


class SentenceTests(unittest.TestCase):
    def test_splits_on_terminal_punctuation(self) -> None:
        self.assertEqual(len(sentences("One two three. Four five six! Seven eight?")), 3)


class SharedChecks(unittest.TestCase):
    def test_banned_phrase_is_error(self) -> None:
        f = lint("In today's fast-paced world, jobs are hard. Very hard indeed.", "podcast", BANNED, {})
        self.assertIn("banned-phrase", checks(f, "ERROR"))

    def test_throat_clearing_is_error(self) -> None:
        f = lint("Welcome to the show where we talk jobs. It is good.", "podcast", BANNED, {})
        self.assertIn("throat-clearing", checks(f, "ERROR"))

    def test_unclosed_loop_is_error(self) -> None:
        f = lint("She paused. [LOOP: secret] There was one thing. Then nothing.", "podcast", BANNED, {})
        self.assertIn("open-loop", checks(f, "ERROR"))

    def test_closed_loop_passes(self) -> None:
        text = "She paused. [LOOP: secret] One thing. Later. [CLOSE: secret] It was the form."
        self.assertNotIn("open-loop", checks(lint(text, "podcast", BANNED, {})))

    def test_needs_marker_reported(self) -> None:
        f = lint("Stat here. [NEEDS SOURCE: callback rate] More text follows.", "podcast", BANNED, {})
        self.assertIn("needs-marker", checks(f, "INFO"))

    def test_any_needs_marker_reported(self) -> None:
        f = lint("Clicks rose. [NEEDS METRIC: before/after CTR] Then [NEEDS LINK: case study].",
                 "podcast", BANNED, {})
        self.assertEqual(sum(1 for x in f if x.check == "needs-marker"), 2)

    def test_brand_rules(self) -> None:
        brand = {
            "brand_name": "Acme Learning",
            "wrong_spellings": ["Acme Learnings"],
            "banned_terms": [{"pattern": r"\bguaranteed? jobs?\b", "reason": "no job guarantees"}],
        }
        f = lint("Acme Learnings offers a guaranteed job. Really.", "podcast", BANNED, brand)
        self.assertIn("brand-name", checks(f, "ERROR"))
        self.assertIn("brand-compliance", checks(f, "ERROR"))

    def test_monotone_rhythm_warns(self) -> None:
        text = " ".join(["This sentence has exactly seven words here."] * 12)
        self.assertIn("monotone-rhythm", checks(lint(text, "podcast", BANNED, {})))


class StructuralTellChecks(unittest.TestCase):
    def test_repeated_not_x_but_y_warns(self) -> None:
        text = ("It's not just a tool, but a partner. The team agreed. "
                "This is not only about speed, but about trust. We moved on.")
        self.assertIn("not-x-but-y", checks(lint(text, "blog", BANNED, {}), "WARN"))

    def test_single_contrast_allowed(self) -> None:
        text = "It's not just a tool, but a partner. The team agreed. We moved on."
        self.assertNotIn("not-x-but-y", checks(lint(text, "blog", BANNED, {})))

    def test_copula_avoidance_warns(self) -> None:
        text = "The office serves as a hub. The CV stands as a record. It is fine."
        self.assertIn("copula-avoidance", checks(lint(text, "blog", BANNED, {}), "WARN"))

    def test_vague_attribution_warns(self) -> None:
        text = "Studies show that interviews matter. She called back on Friday."
        self.assertIn("vague-attribution", checks(lint(text, "blog", BANNED, {}), "WARN"))

    def test_unbacked_frequency_warns(self) -> None:
        text = "Most people never ask for feedback. She did, on a Tuesday."
        self.assertIn("unbacked-frequency", checks(lint(text, "blog", BANNED, {}), "WARN"))

    def test_repeated_watch_word_warns(self) -> None:
        text = "A robust plan. A robust team. She called on Friday."
        f = lint(text, "blog", BANNED, {}, watch=("robust",))
        self.assertIn("watch-words", checks(f, "WARN"))

    def test_single_watch_word_in_long_text_passes(self) -> None:
        text = "A robust plan. " + "She called again on Friday morning. " * 100
        f = lint(text, "blog", BANNED, {}, watch=("robust",))
        self.assertNotIn("watch-words", checks(f))

    def test_tidy_ending_warns(self) -> None:
        text = "She called on Friday.\n\nUltimately, success comes to those who prepare well."
        self.assertIn("tidy-ending", checks(lint(text, "blog", BANNED, {}), "WARN"))

    def test_em_dash_is_only_info(self) -> None:
        text = "She waited — then called — then waited — again. It rang."
        self.assertNotIn("em-dashes", checks(lint(text, "blog", BANNED, {}), "WARN"))


class PodcastChecks(unittest.TestCase):
    def test_markdown_in_script_warns(self) -> None:
        text = "HOST: Three things.\n- **One** idea\n- **Two** ideas\n- Three ideas\nHOST: Done now."
        self.assertIn("podcast-markdown", checks(lint(text, "podcast", BANNED, {}), "WARN"))

    def test_long_sentence_is_error_for_audio(self) -> None:
        long = "word " * 30
        text = ("Short one. " * 8) + long.strip() + "."
        self.assertIn("long-sentence", checks(lint(text, "podcast", BANNED, {}), "ERROR"))

    def test_missing_rehooks_is_error(self) -> None:
        text = "She clicked submit again. " * 160
        self.assertIn("rehook", checks(lint(text, "podcast", BANNED, {}), "ERROR"))


class BlogChecks(unittest.TestCase):
    def test_good_blog_has_no_errors(self) -> None:
        errors = [f for f in lint(GOOD_BLOG, "blog", BANNED, {}) if f.level == "ERROR"]
        self.assertEqual(errors, [], errors)

    def test_missing_frontmatter_is_error(self) -> None:
        f = lint("# Title\n\nSome text here. More text.", "blog", BANNED, {})
        self.assertIn("frontmatter", checks(f, "ERROR"))

    def test_two_h1_is_error(self) -> None:
        f = lint(GOOD_BLOG + "\n# Another H1\n", "blog", BANNED, {})
        self.assertIn("h1", checks(f, "ERROR"))

    def test_short_meta_description_is_error(self) -> None:
        text = GOOD_BLOG.replace(GOOD_BLOG.split("meta_description: ")[1].split("\n")[0], "Too short.")
        self.assertIn("meta-description", checks(lint(text, "blog", BANNED, {}), "ERROR"))


if __name__ == "__main__":
    unittest.main()
