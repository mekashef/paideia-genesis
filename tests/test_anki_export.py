import unittest
import tempfile
import shutil
import zipfile
from pathlib import Path
from src.anki.generator import AnkiManager

class TestAnkiExport(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.test_wiki_dir = Path(tempfile.mkdtemp())
        from src.wiki.schema import init_wiki_structure
        from src.wiki.course_importer import CourseImporter
        init_wiki_structure(self.test_wiki_dir)
        importer = CourseImporter(wiki_dir=self.test_wiki_dir)
        importer.import_mit_ocw_course()
        self.manager = AnkiManager(export_dir=self.test_dir, wiki_dir=self.test_wiki_dir)
        self.manager.recompile_from_wiki()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        shutil.rmtree(self.test_wiki_dir, ignore_errors=True)

    def test_staged_cards_initialization(self):
        cards = self.manager.get_staged_cards()
        self.assertTrue(len(cards) >= 1)
        self.assertTrue(any("{{c1::" in c.get("text", "") for c in cards))

    def test_add_card(self):
        new_card = {
            "type": "cloze",
            "text": "The landmark drug class to reduce mortality in HFrEF by blocking Angiotensin II is {{c1::ACE Inhibitors}}.",
            "pearl": "Monitor for cough and hyperkalemia.",
            "tags": ["Cardiology", "Pharmacology"]
        }
        added = self.manager.add_card(new_card)
        self.assertTrue(added["id"].startswith("card-"))
        cards = self.manager.get_staged_cards()
        self.assertEqual(cards[-1]["text"], new_card["text"])

    def test_generate_apkg_valid_zip(self):
        apkg_path = self.manager.generate_apkg(deck_name="Test::Medical_Deck")
        self.assertTrue(apkg_path.exists())
        self.assertTrue(apkg_path.stat().st_size > 0)
        
        # Verify it is a valid zip archive (Anki packages are zip files)
        self.assertTrue(zipfile.is_zipfile(apkg_path))
        with zipfile.ZipFile(apkg_path, 'r') as z:
            names = z.namelist()
            # Anki apkg files contain collection.anki2 or collection.anki21
            self.assertTrue(any("collection.anki" in n for n in names))

if __name__ == "__main__":
    unittest.main()
