"""Unit tests for the SuperMemo-2 (SM-2) spaced-repetition scheduling algorithm."""
import unittest
import json
import shutil
import tempfile
import datetime
from pathlib import Path
from src.anki.generator import AnkiManager


class TestSM2Algorithm(unittest.TestCase):
    """Tests the mathematical correctness and edge cases of the SM-2 algorithm in AnkiManager."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.cards_file = self.test_dir / "test_cards.json"
        self.anki_mgr = AnkiManager()
        # Override the cards storage file to our isolated temp file
        self.anki_mgr.cards_file = self.cards_file

        # Seed initial test card
        self.initial_card = {
            "id": "card-001",
            "front": "SAAG > 1.1 g/dL indicates {{c1::Portal Hypertension}}",
            "back": "Serum Ascites Albumin Gradient reflects transudative fluid from sinusoidal hypertension.",
            "pearl": "Cardiac ascites also has SAAG > 1.1, but ascites total protein > 2.5 g/dL.",
            "repetitions": 0,
            "interval": 1,
            "ease_factor": 2.5,
            "due_date": datetime.date.today().isoformat(),
            "last_reviewed": None,
            "mastery": "unreviewed",
            "tags": ["GI", "Hepatology", "HST121"],
            "course": "HST121",
            "system": "GI"
        }
        self.cards_file.write_text(json.dumps([self.initial_card], indent=2), encoding="utf-8")

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_failed_recall_rating_1_resets_progress(self):
        """Rating 1 ('Again') should reset repetitions to 0 and interval to 1 day."""
        card = self.initial_card
        card["repetitions"] = 3
        card["interval"] = 15
        card["ease_factor"] = 2.5
        self.cards_file.write_text(json.dumps([card], indent=2), encoding="utf-8")

        reviewed = self.anki_mgr.record_review("card-001", rating=1)
        self.assertIsNotNone(reviewed)
        self.assertEqual(reviewed["repetitions"], 0, "Repetitions must reset to 0 on rating 1")
        self.assertEqual(reviewed["interval"], 1, "Interval must reset to 1 day on rating 1")
        self.assertEqual(reviewed["mastery"], "struggling")

    def test_failed_recall_rating_2_resets_progress(self):
        """Rating 2 ('Hard') should also reset repetitions and interval when rating < 3."""
        card = self.initial_card
        card["repetitions"] = 2
        card["interval"] = 6
        self.cards_file.write_text(json.dumps([card], indent=2), encoding="utf-8")

        reviewed = self.anki_mgr.record_review("card-001", rating=2)
        self.assertIsNotNone(reviewed)
        self.assertEqual(reviewed["repetitions"], 0)
        self.assertEqual(reviewed["interval"], 1)
        self.assertEqual(reviewed["mastery"], "struggling")

    def test_successful_recall_progression(self):
        """Ratings 3 ('Good') and 4 ('Easy') should advance intervals and repetitions."""
        # First review with Good (3)
        r1 = self.anki_mgr.record_review("card-001", rating=3)
        self.assertEqual(r1["repetitions"], 1)
        self.assertEqual(r1["interval"], 1)
        self.assertEqual(r1["mastery"], "learning")

        # Second review with Good (3) -> interval becomes 3
        r2 = self.anki_mgr.record_review("card-001", rating=3)
        self.assertEqual(r2["repetitions"], 2)
        self.assertEqual(r2["interval"], 3)

        # Third review with Good (3) -> interval multiplies by ease factor
        r3 = self.anki_mgr.record_review("card-001", rating=3)
        self.assertEqual(r3["repetitions"], 3)
        self.assertGreater(r3["interval"], 3)
        self.assertEqual(r3["mastery"], "mastered", "Card should reach mastered state at rep 3")

    def test_ease_factor_minimum_floor(self):
        """Ease factor must never drop below 1.3 even after repeated low ratings."""
        for _ in range(10):
            self.anki_mgr.record_review("card-001", rating=3)

        cards = self.anki_mgr.get_staged_cards()
        self.assertGreaterEqual(cards[0]["ease_factor"], 1.3, "Ease factor must not fall below 1.3 floor")

    def test_card_deduplication(self):
        """Adding duplicate card text should not duplicate the card entry."""
        duplicate_data = {
            "front": "SAAG > 1.1 g/dL indicates {{c1::Portal Hypertension}}",
            "back": "Different back text",
            "pearl": "Different pearl"
        }
        res = self.anki_mgr.add_card(duplicate_data)
        cards = self.anki_mgr.get_staged_cards()
        self.assertEqual(len(cards), 1, "Duplicate card text must be deduplicated")

    def test_due_date_calculation(self):
        """Due date should properly reflect today + interval days."""
        reviewed = self.anki_mgr.record_review("card-001", rating=4)
        expected_due = (datetime.date.today() + datetime.timedelta(days=reviewed["interval"])).isoformat()
        self.assertEqual(reviewed["due_date"], expected_due)


if __name__ == "__main__":
    unittest.main()
