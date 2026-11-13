import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from lint import DEFAULT_BANNED, lint, load_banned, parse_shots  # noqa: E402

BANNED = load_banned(DEFAULT_BANNED)

HEADER = "| Time | Visual (shot) | Audio (VO / SFX / music) | On-screen text |\n|---|---|---|---|\n"
GOOD = HEADER + (
    "| 0:00–0:02 | ECU: card reader flashes DECLINED | SFX: two harsh beeps | Declined. With £2,300 in savings. |\n"
    "| 0:02–0:05 | CU: her face, then POV: banking app | VO: I knew exactly where my money went. | 11 subscriptions |\n"
    "| 0:05–0:08 | Match cut: list, nine rows struck through | VO: I just didn't like looking. | – |\n"
)


def checks(findings, level=None):
    return {f.check for f in findings if level is None or f.level == level}


class VideoLintTests(unittest.TestCase):
    def test_parses_rows(self) -> None:
        shots = parse_shots(GOOD)
        self.assertEqual(len(shots), 3)
        self.assertEqual((shots[1].start, shots[1].end), (2, 5))

    def test_good_script_has_no_errors_or_warnings(self) -> None:
        findings = [f for f in lint(GOOD, "video", BANNED, {}) if f.level in ("ERROR", "WARN")]
        self.assertEqual(findings, [], findings)

    def test_missing_table_is_error(self) -> None:
        self.assertIn("av-table", checks(lint("VO: hello there", "video", BANNED, {}), "ERROR"))

    def test_late_hook_warns(self) -> None:
        text = HEADER + "| 0:00–0:06 | Wide: a city skyline | VO: Welcome. | Brand |\n"
        self.assertIn("late-hook", checks(lint(text, "video", BANNED, {}), "WARN"))

    def test_missing_visual_is_error(self) -> None:
        text = HEADER + "| 0:00–0:02 | – | VO: Hi. | Hi |\n"
        self.assertIn("no-visual", checks(lint(text, "video", BANNED, {}), "ERROR"))

    def test_long_onscreen_text_warns(self) -> None:
        text = HEADER + "| 0:00–0:02 | CU: face | SFX: beep | This caption has far too many words to read in time |\n"
        self.assertIn("onscreen-text", checks(lint(text, "video", BANNED, {}), "WARN"))

    def test_fast_voiceover_warns(self) -> None:
        text = HEADER + "| 0:00–0:02 | CU: face | VO: one two three four five six seven eight nine ten | – |\n"
        self.assertIn("vo-pace", checks(lint(text, "video", BANNED, {}), "WARN"))

    def test_banned_phrase_in_voiceover_is_error(self) -> None:
        text = HEADER + "| 0:00–0:02 | CU: face | VO: Let's dive in. | – |\n"
        self.assertIn("banned-phrase", checks(lint(text, "video", BANNED, {}), "ERROR"))

    def test_timecode_gap_warns(self) -> None:
        text = HEADER + ("| 0:00–0:02 | CU: face | SFX: beep | – |\n"
                         "| 0:03–0:05 | ECU: hands | SFX: click | – |\n")
        self.assertIn("timecode-gap", checks(lint(text, "video", BANNED, {}), "WARN"))


if __name__ == "__main__":
    unittest.main()
