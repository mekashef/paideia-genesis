"""Unit tests for WikiCompiler text extraction, ingestion, and compilation workflows."""
import unittest
import shutil
import tempfile
from pathlib import Path
from src.wiki.compiler import WikiCompiler
from src.llm.client import MockMedicalLLMClient


class TestWikiCompilerExtended(unittest.TestCase):
    """Tests file ingestion, text extraction, and markdown compilation."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.test_dir / "wiki"
        self.mock_llm = MockMedicalLLMClient()
        self.compiler = WikiCompiler(llm_client=self.mock_llm, wiki_dir=self.wiki_dir)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_extract_text_from_plain_markdown(self):
        """Plain markdown and text files should be read cleanly."""
        sample_file = self.test_dir / "lecture_test.md"
        sample_file.write_text("# Cardiology Block\n\nHeart failure pathophysiology.", encoding="utf-8")

        extracted = self.compiler.extract_text_from_file(sample_file)
        self.assertIn("Cardiology Block", extracted)
        self.assertIn("Heart failure pathophysiology", extracted)

    def test_ingest_source_with_mock_llm(self):
        """Ingesting a source file compiles concepts and differentials into the wiki structure."""
        lecture_content = (
            "# Acute Decompensated Heart Failure\n\n"
            "Diuretic therapy with Furosemide inhibits NKCC2 in the thick ascending limb."
        )
        result = self.compiler.ingest_source(
            filename="Test_Heart_Failure.md",
            content=lecture_content,
            source_type="lecture"
        )
        self.assertIn("pages", result)
        self.assertGreaterEqual(len(result["pages"]), 1)
        self.assertGreaterEqual(result["pages_created"], 1)

    def test_special_characters_handling_in_extraction(self):
        """Compiler must not crash when extracting text with Unicode and mathematical symbols."""
        sample_file = self.test_dir / "math_notes.md"
        sample_file.write_text(
            "ΔOsm = 290 - 2 × ([Na⁺] + [K⁺])\nα₁-adrenergic & β₂-receptors.",
            encoding="utf-8"
        )
        extracted = self.compiler.extract_text_from_file(sample_file)
        self.assertIn("ΔOsm", extracted)
        self.assertIn("β₂-receptors", extracted)


if __name__ == "__main__":
    unittest.main()
