import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from hooks_check import check_hook, check_hook_list, parse_hook_list  # noqa: E402
from lint import DEFAULT_BANNED, lint, load_banned  # noqa: E402

BANNED = load_banned(DEFAULT_BANNED)


def ids(findings):
    return {f.check for f in findings}


class DeadHookTests(unittest.TestCase):
    def test_imagine_is_dead(self) -> None:
        self.assertIn("dead-hook", ids(check_hook("Imagine you're walking into your dream job interview.")))

    def test_picture_this_is_dead(self) -> None:
        self.assertIn("dead-hook", ids(check_hook("Picture this: a Monday morning and an empty inbox.")))

    def test_second_person_scene_is_dead(self) -> None:
        self.assertIn("dead-hook", ids(check_hook("You're sitting at your desk, staring at the screen.")))

    def test_coffee_laptop_scene_is_stock(self) -> None:
        found = ids(check_hook("I opened my laptop. The coffee cup was still warm and I felt ready."))
        self.assertIn("stock-scene", found)

    def test_we_have_all_been_there_is_dead(self) -> None:
        self.assertIn("dead-hook", ids(check_hook("We've all been there. The job hunt is hard.")))


class LiveHookTests(unittest.TestCase):
    def test_anchored_scene_passes(self) -> None:
        self.assertEqual(check_hook("At 11:40 on a Sunday night she clicked submit for the 212th time."), [])

    def test_specific_number_passes(self) -> None:
        self.assertEqual(check_hook("212 applications. 198 marked \"no reply\"."), [])

    def test_contrarian_claim_passes(self) -> None:
        self.assertEqual(check_hook("Applying to more jobs is making you less hireable."), [])

    def test_quote_passes(self) -> None:
        self.assertEqual(check_hook("\"I don't need a better CV. I need someone to tell me the truth.\""), [])

    def test_stock_prop_with_anchor_passes(self) -> None:
        self.assertNotIn("stock-scene", ids(check_hook("The card was declined at 6:14 am, coffee in one hand.")))

    def test_vague_unanchored_hook_warns(self) -> None:
        self.assertIn("vague-hook", ids(check_hook("Sometimes life feels like a struggle you can't win.")))


class HookListTests(unittest.TestCase):
    LIST = ("1. Imagine waking up to a dream offer.\n"
            "2. 212 applications. 198 \"no reply\". (S-T001)\n"
            "3. Applying to more jobs is making you less hireable.\n")

    def test_parses_and_strips_source_tags(self) -> None:
        hooks = parse_hook_list(self.LIST)
        self.assertEqual(len(hooks), 3)
        self.assertFalse(hooks[1].endswith("(S-T001)"))

    def test_only_dead_hook_flagged(self) -> None:
        found = check_hook_list(self.LIST)
        self.assertEqual([f.message.split()[1] for f in found if f.check == "dead-hook"], ["1"])

    def test_placeholder_anchor_warns(self) -> None:
        found = check_hook_list("- [NEEDS SOURCE: X%] of remote workers say they are burned out. (claim 1)\n")
        self.assertIn("placeholder-hook", ids(found))

    def test_hooks_mode_in_linter(self) -> None:
        self.assertIn("dead-hook", ids(lint(self.LIST, "hooks", BANNED, {})))


class HookInLongFormTests(unittest.TestCase):
    def test_blog_opening_checked(self) -> None:
        self.assertIn("dead-hook", ids(lint("Imagine you are job hunting. It is hard work today.", "podcast", BANNED, {})))

    def test_social_first_line_checked(self) -> None:
        text = "---\nplatform: linkedin\n---\nPicture this: a quiet office. Nobody replies."
        self.assertIn("dead-hook", ids(lint(text, "social", BANNED, {})))

    def test_video_first_shot_checked(self) -> None:
        text = ("| Time | Visual | Audio | Text |\n|---|---|---|---|\n"
                "| 0:00–0:02 | CU: a coffee cup on a desk | VO: Imagine your perfect morning. | – |\n")
        self.assertIn("dead-hook", ids(lint(text, "video", BANNED, {})))


if __name__ == "__main__":
    unittest.main()
