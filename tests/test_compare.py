import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from compare import lint_dir, render, summarise  # noqa: E402


class CompareTests(unittest.TestCase):
    def test_counts_errors_and_needs_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "a.md").write_text("Welcome to the show. In conclusion, it ends.", encoding="utf-8")
            (folder / "b.md").write_text("She called. [NEEDS SOURCE: rate] It rang twice.", encoding="utf-8")
            summary = summarise(lint_dir(folder, "podcast", {}))
        self.assertEqual(summary.files, 2)
        self.assertGreaterEqual(summary.errors, 2)
        self.assertEqual(summary.needs_markers, 1)

    def test_render_has_both_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            summary = summarise(lint_dir(Path(tmp), "blog", {}))
        table = render(summary, summary, "Base", "Skill")
        self.assertIn("| | Base | Skill |", table)


if __name__ == "__main__":
    unittest.main()
