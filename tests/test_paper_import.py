"""Unit tests for Research Paper Ingestion and Synthesis."""
import unittest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

from src.wiki.schema import init_wiki_structure
from src.wiki.course_importer import CourseImporter
from src.api.server import app

class TestPaperImport(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.temp_dir / "wiki"
        self.db_path = self.temp_dir / "index.db"
        init_wiki_structure(self.wiki_dir)
        self.importer = CourseImporter(wiki_dir=self.wiki_dir)
        self.client = TestClient(app)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_paper_import_custom_paper(self):
        """Verifies import_paper compiles a new paper, creates flashcard, and writes concept file."""
        title = "LoRA: Low-Rank Adaptation of Large Language Models"
        abstract = "Freezes pre-trained model weights and injects trainable rank decomposition matrices into layers."
        arxiv_id = "2106.09685"
        tags = ["Deep Learning", "Parameter-Efficient Fine-Tuning", "LoRA"]
        content = "### Mathematical Formulation\n$$W = W_0 + \\Delta W = W_0 + B \\cdot A$$\nwhere $B \\in \\mathbb{R}^{d \\times r}$ and $A \\in \\mathbb{R}^{r \\times k}$ with $r \\ll \\min(d, k)$."

        res = self.importer.import_paper(
            title=title,
            abstract=abstract,
            content=content,
            arxiv_id=arxiv_id,
            tags=tags
        )

        self.assertTrue(res["success"])
        self.assertIn("lora", res["slug"])
        self.assertTrue(res["card_staged"])

        concept_path = self.wiki_dir / res["rel_path"]
        self.assertTrue(concept_path.exists())
        text = concept_path.read_text(encoding="utf-8")
        self.assertIn("2106.09685", text)
        self.assertIn("LoRA: Low-Rank Adaptation", text)
        self.assertIn("Parameter-Efficient Fine-Tuning", text)

    def test_api_import_paper_endpoint(self):
        """Verifies POST /api/wiki/import_paper endpoint."""
        payload = {
            "title": "Segment Anything (SAM)",
            "abstract": "A foundation model for promptable image segmentation with zero-shot generalization.",
            "arxiv_id": "2304.02643",
            "tags": ["Segmentation", "Foundation Models", "Vision"],
            "content": "### Architecture\nHeavy ViT image encoder with lightweight prompt encoder and two-way transformer decoder."
        }
        resp = self.client.post("/api/wiki/import_paper", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        self.assertIn("segment-anything", data.get("slug"))

if __name__ == "__main__":
    unittest.main()
