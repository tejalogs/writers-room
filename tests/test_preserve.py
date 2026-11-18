import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from preserve import find_missing  # noqa: E402

DRAFT = ('She said: "It felt like begging. I sent it anyway." '
         "Rates rose [NEEDS SOURCE: callback rate]. See https://example.com/quiz for more.")


class PreserveTests(unittest.TestCase):
    def test_nothing_lost(self) -> None:
        self.assertEqual(find_missing(DRAFT, DRAFT), ())

    def test_dropped_quote_reported(self) -> None:
        final = DRAFT.replace("It felt like begging. I sent it anyway.", "It was hard.")
        self.assertEqual([m.kind for m in find_missing(DRAFT, final)], ["quote"])

    def test_altered_quote_reported(self) -> None:
        final = DRAFT.replace("I sent it anyway", "I sent it regardless")
        self.assertIn("quote", [m.kind for m in find_missing(DRAFT, final)])

    def test_needs_marker_moved_to_review_is_fine(self) -> None:
        final = DRAFT.replace(" [NEEDS SOURCE: callback rate]", "")
        self.assertEqual(find_missing(DRAFT, final, review="- [NEEDS SOURCE: callback rate]"), ())

    def test_needs_marker_dropped_everywhere_reported(self) -> None:
        final = DRAFT.replace(" [NEEDS SOURCE: callback rate]", "")
        self.assertEqual([m.kind for m in find_missing(DRAFT, final)], ["needs-marker"])

    def test_dropped_link_reported(self) -> None:
        final = DRAFT.replace(" See https://example.com/quiz for more.", "")
        self.assertEqual([m.kind for m in find_missing(DRAFT, final)], ["link"])

    def test_curly_quotes_match_straight(self) -> None:
        final = DRAFT.replace('"It felt like begging. I sent it anyway."', "“It felt like begging. I sent it anyway.”")
        self.assertEqual(find_missing(DRAFT, final), ())


if __name__ == "__main__":
    unittest.main()
