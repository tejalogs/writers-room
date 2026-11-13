import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "writers-room" / "scripts"))

from anonymize import anonymize, discover_names  # noqa: E402


class PatternTests(unittest.TestCase):
    def test_email_removed(self) -> None:
        out = anonymize("Mail me at priya.s+jobs@gmail.com please").text
        self.assertNotIn("gmail", out)
        self.assertIn("[EMAIL]", out)

    def test_uk_and_intl_phone_removed(self) -> None:
        out = anonymize("Call 07700 900123 or +91 98765 43210 tomorrow").text
        self.assertNotIn("900123", out)
        self.assertNotIn("43210", out)

    def test_url_removed(self) -> None:
        out = anonymize("My profile is https://linkedin.com/in/someone ok").text
        self.assertIn("[URL]", out)

    def test_uk_postcode_removed(self) -> None:
        self.assertIn("[POSTCODE]", anonymize("I live near SW1A 1AA now").text)

    def test_dob_removed(self) -> None:
        self.assertIn("[DOB]", anonymize("Born 04/07/1996 in winter").text)

    def test_plain_numbers_survive(self) -> None:
        out = anonymize("I applied to 212 jobs in 2025 and got 3 replies").text
        self.assertIn("212", out)
        self.assertIn("2025", out)


class NameTests(unittest.TestCase):
    def test_passed_names_and_parts_removed(self) -> None:
        out = anonymize("Priya Sharma said Priya was tired", names=("Priya Sharma",)).text
        self.assertNotIn("Priya", out)
        self.assertNotIn("Sharma", out)

    def test_same_name_gets_same_tag(self) -> None:
        out = anonymize("Rahul called. Later rahul emailed.", names=("Rahul",)).text
        self.assertEqual(out.count("[NAME_1]"), 2)

    def test_intro_name_discovered(self) -> None:
        self.assertIn("Arjun", discover_names("Hi, my name is Arjun, I need help"))

    def test_named_speaker_label_discovered(self) -> None:
        self.assertIn("Meera", discover_names("Agent: Hello\nMeera: Hi there"))

    def test_generic_speakers_kept(self) -> None:
        self.assertEqual(discover_names("Agent: Hello\nUser: Hi"), ())

    def test_nationality_not_mistaken_for_name(self) -> None:
        out = anonymize("I'm Indian and this is Monday for me").text
        self.assertIn("Indian", out)
        self.assertIn("Monday", out)

    def test_orgs_removed(self) -> None:
        out = anonymize("I worked at Infosys for 3 years", orgs=("Infosys",)).text
        self.assertIn("[ORG_1]", out)


if __name__ == "__main__":
    unittest.main()
