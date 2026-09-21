"""Tests for Anki Atomic / Single-Unknown Flashcard Derivation & Spaced Repetition."""
import unittest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

from src.anki.compiler import WikiFlashcardCompiler, atomize_card
from src.anki.generator import AnkiManager
from src.api.server import app

class TestAnkiAtomicCards(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.temp_dir / "wiki"
        self.export_dir = self.temp_dir / "export"
        self.wiki_dir.mkdir(parents=True)
        self.export_dir.mkdir(parents=True)
        self.manager = AnkiManager(export_dir=self.export_dir, wiki_dir=self.wiki_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_atomize_single_cloze_card(self):
        card = {
            "id": "test-001",
            "text": "The microscopic hallmark of Crohn is {{c1::granulomas}}.",
            "pearl": "Noncaseating granulomas are pathognomonic.",
            "tags": ["GI"]
        }
        atomic = atomize_card(card)
        self.assertEqual(len(atomic), 1)
        self.assertTrue(atomic[0]["is_atomic"])
        self.assertEqual(atomic[0]["target_unknown"], "granulomas")
        self.assertEqual(atomic[0]["text"], card["text"])

    def test_atomize_multi_cloze_card_minimum_information_principle(self):
        card = {
            "id": "test-002",
            "text": "Gross endoscopic examination showing {{c1::skip lesions::morphology}} indicates {{c2::Crohn's disease}}, whereas continuous rectosigmoid involvement indicates {{c3::Ulcerative Colitis}}.",
            "pearl": "Crohn vs UC contrast",
            "tags": ["GI", "Differentials"]
        }
        atomic = atomize_card(card)
        self.assertEqual(len(atomic), 3)

        # Child 1 tests skip lesions; c2 and c3 are plain text
        c1 = atomic[0]
        self.assertEqual(c1["id"], "test-002-c1")
        self.assertEqual(c1["parent_id"], "test-002")
        self.assertEqual(c1["cloze_index"], 1)
        self.assertEqual(c1["total_clozes"], 3)
        self.assertEqual(c1["target_unknown"], "skip lesions")
        self.assertIn("{{c1::skip lesions::morphology}}", c1["text"])
        self.assertNotIn("{{c2::", c1["text"])
        self.assertIn("indicates Crohn's disease, whereas continuous", c1["text"])
        self.assertIn("indicates Ulcerative Colitis.", c1["text"])
        self.assertIn("Atomic", c1["tags"])
        self.assertIn("Single-Unknown", c1["tags"])

        # Child 2 tests Crohn's disease; c1 and c3 are plain text
        c2 = atomic[1]
        self.assertEqual(c2["id"], "test-002-c2")
        self.assertEqual(c2["cloze_index"], 2)
        self.assertEqual(c2["target_unknown"], "Crohn's disease")
        self.assertIn("{{c1::Crohn's disease}}", c2["text"])
        self.assertIn("showing skip lesions indicates", c2["text"])
        self.assertNotIn("::morphology}}", c2["text"])  # hint stripped on revealed context

        # Child 3 tests Ulcerative Colitis
        c3 = atomic[2]
        self.assertEqual(c3["id"], "test-002-c3")
        self.assertEqual(c3["target_unknown"], "Ulcerative Colitis")
        self.assertIn("{{c1::Ulcerative Colitis}}", c3["text"])

    def test_atomize_qa_card_unchanged(self):
        card = {
            "id": "qa-001",
            "front": "What is the formula for stool osmotic gap?",
            "back": "290 - 2 * (Na + K)",
            "pearl": "Normal < 50 mOsm/kg indicates secretory diarrhea",
            "tags": ["Physiology"]
        }
        atomic = atomize_card(card)
        self.assertEqual(len(atomic), 1)
        self.assertTrue(atomic[0]["is_atomic"])
        self.assertEqual(atomic[0]["front"], card["front"])

    def test_switch_back_and_forth_between_atomic_and_combined(self):
        # Base card in storage
        base_card = {
            "id": "card-base",
            "text": "In IBD, smoking {{c1::worsens}} Crohn's disease, but is {{c2::protective}} in UC.",
            "pearl": "Former smokers often flare with UC",
            "tags": ["HST121"]
        }
        self.manager.add_card(base_card)

        # 1. Query in Combined Mode
        res_combined = self.manager.get_filtered_cards(cloze_mode="combined")
        self.assertEqual(res_combined["filtered_count"], 1)
        self.assertEqual(res_combined["cards"][0]["id"], "card-base")

        # 2. Query in Atomic Mode (derived on-the-fly)
        res_atomic = self.manager.get_filtered_cards(cloze_mode="atomic")
        self.assertEqual(res_atomic["filtered_count"], 2)
        self.assertEqual(res_atomic["cards"][0]["id"], "card-base-c1")
        self.assertEqual(res_atomic["cards"][1]["id"], "card-base-c2")

        # 3. Query back in Combined Mode (storage intact)
        res_back = self.manager.get_filtered_cards(cloze_mode="combined")
        self.assertEqual(res_back["filtered_count"], 1)
        self.assertEqual(res_back["cards"][0]["id"], "card-base")

    def test_atomic_child_review_persists_independently(self):
        base_card = {
            "id": "card-persist",
            "text": "Triad of {{c1::fever}}, {{c2::RUQ pain}}, and {{c3::jaundice}} is Charcot triad.",
            "pearl": "Ascending cholangitis",
            "tags": ["HST121"]
        }
        self.manager.add_card(base_card)

        # Review child 1 on first presentation (rating 4 -> repetitions=1, interval=1, mastery=learning)
        updated_c1 = self.manager.record_review("card-persist-c1", 4)
        self.assertIsNotNone(updated_c1)
        self.assertEqual(updated_c1["repetitions"], 1)
        self.assertEqual(updated_c1["interval"], 1)
        self.assertEqual(updated_c1["mastery"], "learning")

        # Second successful review for child 1 (rating 4 -> repetitions=2, interval=5)
        updated_c1_again = self.manager.record_review("card-persist-c1", 4)
        self.assertEqual(updated_c1_again["repetitions"], 2)
        self.assertEqual(updated_c1_again["interval"], 5)

        # Review child 2 as Again (Struggling, rating 1)
        updated_c2 = self.manager.record_review("card-persist-c2", 1)
        self.assertIsNotNone(updated_c2)
        self.assertEqual(updated_c2["mastery"], "struggling")
        self.assertEqual(updated_c2["interval"], 1)

        # Fetch in atomic mode and verify child cards have distinct review states
        cards = self.manager.get_filtered_cards(cloze_mode="atomic")["cards"]
        c1 = next(c for c in cards if c["id"] == "card-persist-c1")
        c2 = next(c for c in cards if c["id"] == "card-persist-c2")
        c3 = next(c for c in cards if c["id"] == "card-persist-c3")

        self.assertEqual(c1["mastery"], "learning")
        self.assertEqual(c1["interval"], 5)
        self.assertEqual(c2["mastery"], "struggling")
        self.assertEqual(c2["interval"], 1)
        self.assertEqual(c3["mastery"], "unreviewed")

    def test_apkg_generation_both_modes(self):
        base_card = {
            "id": "card-export",
            "text": "Primary sclerosing cholangitis causes {{c1::beading}} of ducts and is associated with {{c2::Ulcerative Colitis}}.",
            "pearl": "PSC has p-ANCA positivity",
            "tags": ["HST121"]
        }
        self.manager.add_card(base_card)

        # Generate combined deck
        apkg_comb = self.manager.generate_apkg(deck_name="Combined_Test", atomic=False)
        self.assertTrue(apkg_comb.exists())
        self.assertTrue(apkg_comb.stat().st_size > 500)

        # Generate single-unknown atomic deck
        apkg_atom = self.manager.generate_apkg(deck_name="Atomic_Test", atomic=True)
        self.assertTrue(apkg_atom.exists())
        self.assertTrue(apkg_atom.stat().st_size > 500)

class TestAnkiApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from src.wiki.schema import init_wiki_structure
        from src.wiki.course_importer import CourseImporter
        from src.anki.generator import AnkiManager
        init_wiki_structure()
        importer = CourseImporter()
        importer.import_mit_ocw_course()
        anki_mgr = AnkiManager()
        anki_mgr.recompile_from_wiki()

    @classmethod
    def tearDownClass(cls):
        client = TestClient(app)
        client.post("/api/wiki/reset", json={"confirm": True})

    def setUp(self):
        self.client = TestClient(app)

    def test_api_cards_cloze_modes(self):
        # Fetch atomic
        resp_atomic = self.client.get("/api/anki/cards?cloze_mode=atomic")
        self.assertEqual(resp_atomic.status_code, 200)
        data_atom = resp_atomic.json()
        self.assertIn("cards", data_atom)
        self.assertGreater(data_atom["stats"]["total"], 100)

        # Fetch combined
        resp_comb = self.client.get("/api/anki/cards?cloze_mode=combined")
        self.assertEqual(resp_comb.status_code, 200)
        data_comb = resp_comb.json()
        self.assertIn("cards", data_comb)

        # Total atomic cards should be >= total combined cards
        self.assertGreaterEqual(data_atom["stats"]["total"], data_comb["stats"]["total"])

    def test_api_export_atomic(self):
        resp = self.client.get("/api/anki/export?atomic=true")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["content-type"], "application/octet-stream")
        self.assertGreater(len(resp.content), 500)

if __name__ == "__main__":
    unittest.main()
