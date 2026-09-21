import unittest
import tempfile
import shutil
from pathlib import Path
from src.wiki.knowledge_puller import KnowledgePuller
from src.llm.client import MockMedicalLLMClient

class TestKnowledgePuller(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.concepts_dir = self.test_dir / "concepts"
        self.concepts_dir.mkdir(parents=True)
        self.mock_llm = MockMedicalLLMClient()
        self.puller = KnowledgePuller(llm_client=self.mock_llm, wiki_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_pull_and_synthesize(self):
        result = self.puller.pull_and_synthesize("SGLT2 inhibitors in heart failure")
        self.assertIn("slug", result)
        self.assertIn("title", result)
        self.assertIn("summary", result)
        self.assertIn("candidate_card", result)

    def test_integrate_into_wiki(self):
        synthesized = self.puller.pull_and_synthesize("SGLT2 inhibitors")
        res = self.puller.integrate_into_wiki(synthesized)
        self.assertTrue(res["success"])
        page_path = self.test_dir / res["rel_path"]
        self.assertTrue(page_path.exists())
        content = page_path.read_text(encoding="utf-8")
        self.assertIn("SGLT2", content)
        self.assertIn("High-Yield Summary", content)

if __name__ == "__main__":
    unittest.main()
