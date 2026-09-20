import unittest
import tempfile
import shutil
from pathlib import Path
from src.wiki.indexer import WikiIndexer, parse_markdown_file

class TestWikiIndexer(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.concepts_dir = self.test_dir / "concepts"
        self.concepts_dir.mkdir(parents=True)

        # Create sample markdown file
        self.sample_file = self.concepts_dir / "heart-failure.md"
        self.sample_file.write_text(
            "---\n"
            "title: Congestive Heart Failure\n"
            "tags: [cardiology, pathophysiology]\n"
            "---\n"
            "# Congestive Heart Failure\n\n"
            "Heart failure involves impaired ventricular ejection and pulmonary edema. "
            "Treatment includes [[loop-diuretics]] and [[ace-inhibitors]].\n",
            encoding="utf-8"
        )
        self.indexer = WikiIndexer(wiki_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_parse_markdown_file(self):
        sample = self.concepts_dir / "ibd.md"
        sample.write_text(
            "---\n"
            "title: Inflammatory Bowel Disease\n"
            "system: Gastroenterology\n"
            "source: MIT HST.121 Gastroenterology\n"
            "tags: [Gastroenterology, Immunology]\n"
            "---\n"
            "# Inflammatory Bowel Disease\n\n"
            "Covers Crohn disease and [[ulcerative-colitis]].\n",
            encoding="utf-8"
        )
        parsed = parse_markdown_file(sample)
        self.assertEqual(parsed["title"], "Inflammatory Bowel Disease")
        self.assertEqual(parsed["system"], "Gastroenterology")
        self.assertEqual(parsed["source"], "MIT HST.121 Gastroenterology")
        self.assertIn("Gastroenterology", parsed["tags"])
        self.assertIn("system", parsed["frontmatter"])
        self.assertEqual(len(parsed["links"]), 1)
        self.assertEqual(parsed["links"][0][0], "ulcerative-colitis")

    def test_indexing_and_search(self):
        self.indexer.index_file(self.sample_file)
        results = self.indexer.search("ventricular ejection")
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["title"], "Congestive Heart Failure")

    def test_graph_extraction(self):
        self.indexer.index_file(self.sample_file)
        graph = self.indexer.get_graph()
        self.assertTrue(any(n["id"] == "heart-failure" for n in graph["nodes"]))
        self.assertTrue(any(l["source"] == "heart-failure" and l["target"] == "loop-diuretics" for l in graph["links"]))

if __name__ == "__main__":
    unittest.main()
