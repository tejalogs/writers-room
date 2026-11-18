import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from provenance import find_unsourced  # noqa: E402

MATERIAL = ('S-T001: "I\'ve got a spreadsheet with 212 rows." 198 marked no reply. '
            "Claims table: 41% of graduates got no feedback (Acme survey, 2024).")


def kinds(items):
    return [i.kind for i in items]


class ProvenanceTests(unittest.TestCase):
    def test_traced_numbers_and_quote_pass(self) -> None:
        final = 'She had 212 rows; 198 said no reply. "I\'ve got a spreadsheet with 212 rows." 41% got none.'
        self.assertEqual(find_unsourced(final, MATERIAL), ())

    def test_invented_numbers_flagged(self) -> None:
        final = "Your 3-week assignment took an AI 72 seconds, with 98% test coverage."
        flagged = {i.item for i in find_unsourced(final, MATERIAL)}
        self.assertTrue({"3", "72", "98%"} <= flagged, flagged)

    def test_invented_quote_flagged(self) -> None:
        final = 'Students asked: "Can an AI complete my entire semester assignment?"'
        self.assertEqual(kinds(find_unsourced(final, MATERIAL)), ["unsourced-quote"])

    def test_list_numbers_and_needs_markers_ignored(self) -> None:
        final = "### 1. The trap\n1. First step\n2. Second step\nRates rose [NEEDS SOURCE: 35% figure]."
        self.assertEqual(find_unsourced(final, MATERIAL), ())

    def test_frontmatter_and_urls_ignored(self) -> None:
        final = "---\nupdated: 2026-11-18\n---\nSee https://example.com/2026/77 for the quiz."
        self.assertEqual(find_unsourced(final, MATERIAL), ())

    def test_comma_numbers_match(self) -> None:
        self.assertEqual(find_unsourced("It cost 2,300 pounds.", "Proof: 2300 pounds saved"), ())


if __name__ == "__main__":
    unittest.main()
