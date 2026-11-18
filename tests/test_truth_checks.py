import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from checks_v2 import check_emoji, check_label_lists, check_self_research, check_signposting  # noqa: E402


def ids(findings):
    return {f.check for f in findings}


class SelfResearchTests(unittest.TestCase):
    def test_our_team_ran(self) -> None:
        self.assertIn("self-research", ids(check_self_research("Our research team ran a test on every rubric.")))

    def test_we_collected(self) -> None:
        self.assertIn("self-research", ids(check_self_research("We collected the rubrics and fed them to agents.")))

    def test_named_autopsy(self) -> None:
        self.assertIn("self-research", ids(check_self_research("The results of the 7-Day Curriculum Autopsy were clear.")))

    def test_ordinary_we_passes(self) -> None:
        self.assertEqual(check_self_research("We think the CV was aimed at too many jobs."), [])


class StructureTests(unittest.TestCase):
    def test_signposting(self) -> None:
        text = "That grade is false comfort. Here is why your degree leaves you unprepared."
        self.assertIn("signposting", ids(check_signposting(text)))

    def test_no_signposting(self) -> None:
        self.assertEqual(check_signposting("The grade measured the wrong thing. Here, the fix is simple."), [])

    def test_two_label_lists_warn(self) -> None:
        body = ("- What college rewards: typing.\n- What companies need: wiring.\n- Why it hurts: speed.\n\n"
                "Some prose.\n\n"
                "- Curiosity: one.\n- Concern: two.\n- Motivation: three.\n")
        self.assertIn("label-lists", ids(check_label_lists(body)))

    def test_one_label_list_is_fine(self) -> None:
        body = "- Answer: yes.\n- Reason: speed.\n- Fix: rewrite.\n\nProse only after this."
        self.assertEqual(check_label_lists(body), [])

    def test_emoji(self) -> None:
        self.assertIn("emoji", ids(check_emoji("👉 Take the free diagnostic today.")))


if __name__ == "__main__":
    unittest.main()
