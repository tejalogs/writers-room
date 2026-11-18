import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from checks_v2 import score  # noqa: E402
from lint import DEFAULT_BANNED, lint, load_banned, main  # noqa: E402
from wr_text import Finding  # noqa: E402

BANNED = load_banned(DEFAULT_BANNED)


def checks(findings, level=None):
    return {f.check for f in findings if level is None or f.level == level}


class NewRuleTests(unittest.TestCase):
    def test_repeated_opener(self) -> None:
        text = "She called. She waited. She called again. Nobody answered."
        self.assertIn("repeated-opener", checks(lint(text, "podcast", BANNED, {})))

    def test_unsourced_stat_flagged(self) -> None:
        text = "Most hiring is broken. About 75% of CVs are never read by a person."
        self.assertIn("unsourced-stat", checks(lint(text, "podcast", BANNED, {})))

    def test_sourced_stat_passes(self) -> None:
        text = "According to a 2024 survey by Acme, 41% of graduates got no feedback."
        self.assertNotIn("unsourced-stat", checks(lint(text, "podcast", BANNED, {})))

    def test_needs_marker_counts_as_source(self) -> None:
        text = "About 75% of CVs are never read [NEEDS SOURCE: CV read rate]."
        self.assertNotIn("unsourced-stat", checks(lint(text, "podcast", BANNED, {})))

    def test_spelling_against_brand(self) -> None:
        f = lint("We organized the colour chart today. It looked fine.", "podcast", BANNED, {"spelling": "UK"})
        self.assertIn("spelling", checks(f))

    def test_mixed_spelling_without_brand(self) -> None:
        f = lint("The colour was nice. We analyzed it later.", "podcast", BANNED, {})
        self.assertIn("spelling", checks(f))

    def test_organism_is_not_a_spelling_variant(self) -> None:
        f = lint("The organism grew. Realistic plans work.", "podcast", BANNED, {"spelling": "US"})
        self.assertNotIn("spelling", checks(f))

    def test_watch_cluster(self) -> None:
        text = "A robust and seamless way to elevate your team. Then we went home early."
        f = lint(text, "podcast", BANNED, {}, watch=("robust", "seamless", "elevate"))
        self.assertIn("watch-cluster", checks(f))


class IgnoreAndScoreTests(unittest.TestCase):
    def test_file_level_ignore(self) -> None:
        text = "<!-- wr-ignore: repeated-opener -->\nShe called. She waited. She called again. Nobody came."
        self.assertNotIn("repeated-opener", checks(lint(text, "podcast", BANNED, {})))

    def test_line_level_ignore(self) -> None:
        text = "Fine opening line here.\nIn conclusion, it ends. <!-- wr-ignore-line: banned-phrase -->"
        self.assertNotIn("banned-phrase", checks(lint(text, "podcast", BANNED, {})))

    def test_score(self) -> None:
        findings = [Finding("ERROR", "a", "x"), Finding("WARN", "b", "y"), Finding("INFO", "c", "z")]
        self.assertEqual(score(findings), 87)

    def test_non_english_skips_english_rules(self) -> None:
        f = lint("In conclusion, es muy bueno. Vale.", "podcast", BANNED, {"lang": "es"})
        self.assertNotIn("banned-phrase", checks(f))
        self.assertIn("lang", checks(f, "INFO"))


class AdModeTests(unittest.TestCase):
    AD = ("## Google headlines\n- Find the money you missed\n- Budgeting that nudges you before payday arrives\n\n"
          "## Google descriptions\n- See every subscription in one place and cancel the ones you forgot.\n\n"
          "## Meta primary text\nDeclined at the pump with £2,300 in savings.\n\nShe knew where it went.\n")

    def test_google_headline_over_30_is_error(self) -> None:
        self.assertIn("ad-limit", checks(lint(self.AD, "ad", BANNED, {}), "ERROR"))

    def test_too_few_headlines_warns(self) -> None:
        self.assertIn("ad-variants", checks(lint(self.AD, "ad", BANNED, {}), "WARN"))

    def test_missing_sections_warns(self) -> None:
        self.assertIn("ad-sections", checks(lint("Just some ad copy here. Buy now.", "ad", BANNED, {})))


class SocialModeTests(unittest.TestCase):
    def test_x_post_over_280_is_error(self) -> None:
        text = "---\nplatform: x\n---\n" + ("word " * 70)
        self.assertIn("post-length", checks(lint(text, "social", BANNED, {}), "ERROR"))

    def test_long_first_line_and_hashtags_and_lazy_cta(self) -> None:
        first = "This first line goes on and on far past the point where LinkedIn cuts it off with a see more link, " \
                "which means nobody reads the rest of it at all."
        text = f"---\nplatform: linkedin\n---\n{first}\n\nSecond line. #a #b #c #d\n\nThoughts?"
        found = checks(lint(text, "social", BANNED, {}))
        self.assertTrue({"first-line-cut", "hashtags", "lazy-cta"} <= found, found)

    def test_social_throat_clearing(self) -> None:
        text = "---\nplatform: linkedin\n---\nWelcome to my post about hiring. It matters."
        self.assertIn("throat-clearing", checks(lint(text, "social", BANNED, {}), "ERROR"))


class CliTests(unittest.TestCase):
    def test_fail_under(self) -> None:
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
            fh.write("She called. She waited. She called again. Nobody answered.")
            path = fh.name
        self.assertEqual(main([path, "--mode", "podcast", "--fail-under", "100"]), 1)
        self.assertEqual(main([path, "--mode", "podcast", "--fail-under", "50"]), 0)


if __name__ == "__main__":
    unittest.main()
