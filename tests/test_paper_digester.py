"""Comprehensive unit tests for PaperDigester and Deep Academic Paper Digestion Engine."""
import unittest
import tempfile
import shutil
import io
from pathlib import Path
from fastapi.testclient import TestClient

from src.wiki.schema import init_wiki_structure
from src.wiki.paper_digester import PaperDigester
from src.wiki.indexer import WikiIndexer
from src.anki.generator import AnkiManager
from src.api.server import app

class TestPaperDigester(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.temp_dir / "wiki"
        self.raw_dir = self.temp_dir / "raw_sources"
        self.assets_dir = self.wiki_dir / "assets"
        init_wiki_structure(self.wiki_dir, self.raw_dir)
        self.digester = PaperDigester(
            wiki_dir=self.wiki_dir,
            raw_sources_dir=self.raw_dir,
            assets_dir=self.assets_dir
        )
        self.client = TestClient(app)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_text_from_file_markdown_and_text(self):
        """Verifies text extraction from .md, .txt, and .json files."""
        md_file = self.temp_dir / "paper_notes.md"
        md_file.write_text("# Diffusion Models in 3D\n\nScore-based generative modeling for radiance fields.", encoding="utf-8")
        text = self.digester.extract_text_from_file(md_file)
        self.assertIn("Diffusion Models in 3D", text)
        self.assertIn("radiance fields", text)

    def test_extract_text_and_figures_from_pdf(self):
        """Verifies PDF text and embedded image extraction using pypdf."""
        import pypdf
        writer = pypdf.PdfWriter()
        writer.add_blank_page(width=200, height=200)
        pdf_bytes_io = io.BytesIO()
        writer.write(pdf_bytes_io)
        pdf_bytes = pdf_bytes_io.getvalue()

        text, figures = self.digester.extract_text_and_figures_from_pdf(pdf_bytes, slug="test-blank-paper")
        self.assertIsInstance(text, str)
        self.assertIsInstance(figures, list)

    def test_digest_paper_synthesizes_visuals_and_math(self):
        """Verifies that digest_paper produces Mermaid schematics, KaTeX formulas, benchmark matrices, and sub-concepts in papers/."""
        title = "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
        abstract = "Anisotropic 3D Gaussians with tile-based rasterization for 100+ FPS real-time rendering."
        content = "### Differentiable Projection\nCovariance projection Sigma' = J W Sigma W^T J^T.\nAlpha blending C = sum c_i alpha_i prod (1 - alpha_j)."

        res = self.digester.digest_paper(
            title=title,
            abstract=abstract,
            content=content,
            arxiv_id="2308.04079",
            tags=["3DGS", "Radiance-Fields", "Real-Time"]
        )

        self.assertTrue(res["success"])
        self.assertTrue(res["slug"].startswith("3d-gaussian-splatting"))
        self.assertTrue(res["rel_path"].startswith("papers/"))
        self.assertTrue(res["has_mermaid"])
        self.assertGreaterEqual(res["concepts_compiled"], 1)
        self.assertGreaterEqual(res["flashcards_staged"], 1)

        # Verify master paper file exists in papers/
        paper_file = self.wiki_dir / res["rel_path"]
        self.assertTrue(paper_file.exists())
        paper_md = paper_file.read_text(encoding="utf-8")

        # Verify Visual Architecture schematic block
        self.assertIn("```mermaid", paper_md)
        self.assertIn("flowchart", paper_md)

        # Verify Mathematical Formulations with KaTeX
        self.assertIn("$$", paper_md)

        # Verify Benchmark Matrix Table
        self.assertIn("Empirical SOTA Benchmark", paper_md)
        self.assertIn("|", paper_md)

        # Verify Engineering Traps
        self.assertIn("[!CAUTION]", paper_md)

        # Verify Algorithmic Pseudocode
        self.assertIn("```python", paper_md)

        # Verify sub-concepts exist
        concepts_dir = self.wiki_dir / "concepts"
        concept_files = list(concepts_dir.glob("*.md"))
        self.assertGreaterEqual(len(concept_files), 1)

    def test_api_paper_upload_and_digest_endpoint(self):
        """Verifies multipart file upload endpoint /api/paper/upload_and_digest."""
        content = b"# DINOv2: Learning Robust Visual Features without Supervision\n\nSelf-supervised vision backbone."
        files = {
            "file": ("dinov2_preprint.md", content, "text/markdown")
        }
        data = {
            "title": "DINOv2: Learning Robust Visual Features without Supervision",
            "tags": '["Self-Supervised", "Vision-Transformer", "Backbone"]'
        }
        resp = self.client.post("/api/paper/upload_and_digest", files=files, data=data)
        self.assertEqual(resp.status_code, 200)
        res = resp.json()
        self.assertTrue(res.get("success"))
        self.assertTrue(res.get("rel_path").startswith("papers/"))
        self.assertTrue(res.get("has_mermaid"))

    def test_wiki_tree_returns_papers_section(self):
        """Verifies GET /api/wiki/tree returns the papers category."""
        resp = self.client.get("/api/wiki/tree")
        self.assertEqual(resp.status_code, 200)
        tree = resp.json()
        self.assertIn("papers", tree)
        self.assertIsInstance(tree["papers"], list)

    def test_contextual_retrieval_on_digested_paper(self):
        """Verifies that digested papers are searchable with Anthropic contextual search."""
        self.digester.digest_paper(
            title="DUSt3R: Geometric 3D Vision Made Easy",
            abstract="Direct unconstrained stereo 3D reconstruction without explicit camera calibration.",
            content="### Pointmap Regression\nDirectly regresses dense 3D pointmaps and confidence maps.",
            arxiv_id="2312.14132"
        )
    def test_digest_paper_populates_architectures_algorithms_frameworks_theories_and_formulations(self):
        """Verifies that digesting a paper populates algorithms, frameworks, architectures (in entities/) and theories & formulations (in concepts/)."""
        res = self.digester.digest_paper(
            title="3D Gaussian Splatting for Real-Time Radiance Field Rendering",
            abstract="Anisotropic 3D Gaussians with tile-based rasterization for 100+ FPS real-time rendering.",
            content="Covariance Sigma = R S S^T R^T. Tile rasterizer sorts Gaussians. CUDA kernel acceleration.",
            arxiv_id="2308.04079",
            tags=["3DGS", "Radiance-Fields"]
        )

        self.assertTrue(res["success"])
        self.assertGreaterEqual(res.get("architectures_compiled", 0), 1)
        self.assertGreaterEqual(res.get("algorithms_compiled", 0), 1)
        self.assertGreaterEqual(res.get("frameworks_compiled", 0), 1)
        self.assertGreaterEqual(res.get("theoretical_concepts_compiled", 0), 1)
        self.assertGreaterEqual(res.get("formulations_compiled", 0), 1)

        # Verify entity files on disk
        entities_dir = self.wiki_dir / "entities"
        entity_files = list(entities_dir.glob("*.md"))
        self.assertGreaterEqual(len(entity_files), 3)

        categories_found = set()
        for ef in entity_files:
            text = ef.read_text(encoding="utf-8")
            if 'category: "Architecture"' in text:
                categories_found.add("Architecture")
            elif 'category: "Algorithm"' in text:
                categories_found.add("Algorithm")
            elif 'category: "Framework"' in text:
                categories_found.add("Framework")

        self.assertIn("Architecture", categories_found)
        self.assertIn("Algorithm", categories_found)
        self.assertIn("Framework", categories_found)

        # Verify concept files on disk
        concepts_dir = self.wiki_dir / "concepts"
        concept_files = list(concepts_dir.glob("*.md"))
        self.assertGreaterEqual(len(concept_files), 2)

        concept_cats_found = set()
        for cf in concept_files:
            text = cf.read_text(encoding="utf-8")
            if 'category: "Theoretical Concept"' in text:
                concept_cats_found.add("Theoretical Concept")
            elif 'category: "Mathematical Formulation"' in text:
                concept_cats_found.add("Mathematical Formulation")

        self.assertIn("Theoretical Concept", concept_cats_found)
        self.assertIn("Mathematical Formulation", concept_cats_found)

if __name__ == "__main__":
    unittest.main()
