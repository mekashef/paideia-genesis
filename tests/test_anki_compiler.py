import unittest
import tempfile
import shutil
from pathlib import Path
from src.config import WIKI_DIR
from src.anki.compiler import WikiFlashcardCompiler
from src.anki.generator import AnkiManager

class TestAnkiCompilerAndManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.manager = AnkiManager(export_dir=self.test_dir, wiki_dir=WIKI_DIR)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compile_all_cards(self):
        compiler = WikiFlashcardCompiler(WIKI_DIR)
        cards = compiler.compile_all()
        # Ensure we compiled comprehensive cards spanning wiki
        self.assertGreaterEqual(len(cards), 80)

        # Check essential fields on every card
        for card in cards:
            self.assertIn("id", card)
            self.assertIn("type", card)
            self.assertTrue(card.get("text") or card.get("front"))
            self.assertIn("pearl", card)
            self.assertIn("tags", card)
            self.assertIn("source", card)
            self.assertIn("system", card)
            self.assertIn("course", card)
            self.assertIn("mastery", card)

    def test_differentials_and_traps_compiled(self):
        compiler = WikiFlashcardCompiler(WIKI_DIR)
        cards = compiler.compile_all()
        types = {c.get("type") for c in cards}
        self.assertIn("differential", types)
        self.assertIn("trap", types)

        # Check specific high-yield clinical cards exist
        texts = " ".join((c.get("text", "") + " " + c.get("pearl", "")) for c in cards).lower()
        self.assertIn("crohn's disease", texts)
        self.assertIn("ulcerative colitis", texts)
        self.assertIn("lactulose", texts)
        self.assertIn("hepatitis b", texts)
        self.assertIn("stool osmotic gap", texts)


    def test_sm2_spaced_repetition_logic(self):
        # 1. Review with rating 1 (Again / Failed)
        res1 = self.manager.record_review("card-001", 1)
        self.assertIsNotNone(res1)
        self.assertEqual(res1["repetitions"], 0)
        self.assertEqual(res1["interval"], 1)
        self.assertEqual(res1["mastery"], "struggling")

        # 2. Review with rating 3 (Good)
        res2 = self.manager.record_review("card-001", 3)
        self.assertEqual(res2["repetitions"], 1)
        self.assertEqual(res2["interval"], 1)
        self.assertEqual(res2["mastery"], "learning")

        # 3. Multiple reviews with rating 4 (Easy) leading to mastered
        res3 = self.manager.record_review("card-001", 4)
        res4 = self.manager.record_review("card-001", 4)
        self.assertGreaterEqual(res4["interval"], 7)
        self.assertEqual(res4["mastery"], "mastered")

    def test_filtered_cards_and_search(self):
        # Course filter
        hst_res = self.manager.get_filtered_cards(course="hst121")
        self.assertGreater(hst_res["filtered_count"], 0)
        for c in hst_res["cards"]:
            self.assertIn(c.get("course"), ["HST.121", "Both"])

        # System filter
        hep_res = self.manager.get_filtered_cards(system="Hepatology")
        self.assertGreater(hep_res["filtered_count"], 0)
        for c in hep_res["cards"]:
            self.assertIn("hepat", c.get("system", "").lower())

        # Search filter
        search_res = self.manager.get_filtered_cards(search="Lactulose")
        self.assertGreaterEqual(search_res["filtered_count"], 1)
        self.assertIn("lactulose", search_res["cards"][0]["text"].lower())

    def test_apkg_export(self):
        apkg_path = self.manager.generate_apkg(course="hst121")
        self.assertTrue(apkg_path.exists())
        self.assertGreater(apkg_path.stat().st_size, 1000)

if __name__ == "__main__":
    unittest.main()
