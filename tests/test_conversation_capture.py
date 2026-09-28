"""Unit tests for Conversation Capture and Discourse Digestion."""
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from src.wiki.schema import init_wiki_structure
from src.wiki.conversation_digester import ConversationDigester
from src.llm.client import MockUniversalLLMClient
from src.api.server import app

class TestConversationCapture(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.temp_dir / "wiki"
        self.raw_dir = self.temp_dir / "raw_sources"
        init_wiki_structure(self.wiki_dir)
        (self.raw_dir / "conversations").mkdir(parents=True, exist_ok=True)
        
        self.mock_llm = MockUniversalLLMClient()
        self.digester = ConversationDigester(wiki_dir=self.wiki_dir, raw_sources_dir=self.raw_dir, llm_client=self.mock_llm)
        self.client = TestClient(app)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_text_from_text_and_markdown(self):
        """Verifies text extraction from .txt and .md files."""
        txt_path = self.temp_dir / "notes.txt"
        txt_path.write_text("Discussion on Multi-Head Latent Attention in DeepSeek-V2.", encoding="utf-8")
        extracted_txt = self.digester.extract_text_from_document(txt_path)
        self.assertIn("Multi-Head Latent Attention", extracted_txt)

        md_path = self.temp_dir / "sync.md"
        md_path.write_text("# Meeting with Advisor\n\nDiscussed covariance scaling in 3DGS.", encoding="utf-8")
        extracted_md = self.digester.extract_text_from_document(md_path)
        self.assertIn("covariance scaling in 3DGS", extracted_md)

    def test_transcribe_audio_offline_fallback(self):
        """Verifies transcribe_audio falls back to deterministic mock text when offline."""
        dummy_audio = b"RIFF....WAVEfmt ...."
        transcription = self.digester.transcribe_audio(dummy_audio, filename="voice_memo.wav")
        self.assertIsInstance(transcription, str)
        self.assertGreater(len(transcription), 20)
        self.assertIn("Gaussian", transcription)

    def test_digest_conversation_end_to_end(self):
        """Verifies digestion creates master conversation page, compounded files, flashcards, and raw backup."""
        title = "Sync with Prof Sutton on 3DGS vs NeRF Losses"
        raw_text = (
            "Prof. Sutton: How does 3DGS handle unbounded background rendering compared to Instant-NGP?\n"
            "Self: 3DGS struggles when points diverge to infinity without skybox contraction or regularization.\n"
            "Prof. Sutton: You should introduce an SSIM loss and isotropic scaling penalty.\n"
            "Action items: Implement SSIM loss, test on Mip-NeRF 360 dataset."
        )
        participants = "Prof. Sutton, Researcher"
        domain = "Deep Learning & Computer Vision"
        tags = ["3DGS", "NeRF", "Loss Formulations", "Mentorship"]

        result = self.digester.digest_conversation(
            title=title,
            raw_text=raw_text,
            participants=participants,
            domain=domain,
            tags=tags
        )

        self.assertTrue(result["success"])
        self.assertIn("sync-with-prof-sutton", result["slug"])
        self.assertEqual(result["title"], title)
        self.assertGreaterEqual(result["staged_flashcards"], 1)

        # Check master conversation file in wiki/conversations/
        conv_file = self.wiki_dir / result["rel_path"]
        self.assertTrue(conv_file.exists())
        conv_content = conv_file.read_text(encoding="utf-8")
        self.assertIn("category: conversations", conv_content)
        self.assertIn("Prof. Sutton, Researcher", conv_content)
        self.assertIn("## Key Realizations & Strategic Insights", conv_content)
        self.assertIn("## Action Items & Research Follow-ups", conv_content)

        # Check compounded concept
        concept_files = list((self.wiki_dir / "concepts").glob("*.md"))
        self.assertGreater(len(concept_files), 0)

        # Check raw copy saved
        raw_files = list((self.wiki_dir.parent / "raw_sources" / "conversations").glob("*.md"))
        self.assertGreater(len(raw_files), 0)

    def test_api_conversation_digest_endpoint(self):
        """Verifies POST /api/conversation/digest JSON endpoint."""
        payload = {
            "title": "Lab Sync on Flow Matching",
            "raw_text": "Discussed optimal transport flow matching vs standard diffusion ODEs for image synthesis.",
            "participants": "Lab Group",
            "domain": "Deep Learning & Computer Vision",
            "tags": ["Flow Matching", "Diffusion", "Optimal Transport"]
        }
        resp = self.client.post("/api/conversation/digest", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        self.assertIn("lab-sync-on-flow-matching", data.get("slug"))
        self.assertIn("conversations/", data.get("rel_path"))

    def test_api_conversation_transcribe_endpoint(self):
        """Verifies POST /api/conversation/transcribe multipart upload."""
        fake_audio = io.BytesIO(b"MOCK_AUDIO_DATA_FOR_WHISPER_GEMINI")
        files = {"audio_file": ("test_memo.wav", fake_audio, "audio/wav")}
        resp = self.client.post("/api/conversation/transcribe", files=files)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        self.assertIn("text", data)
        self.assertGreater(data.get("word_count", 0), 0)

    def test_api_conversation_upload_and_digest_endpoint(self):
        """Verifies POST /api/conversation/upload_and_digest document upload."""
        doc_content = b"# Discussion on Diffusion Transformers (DiT)\n\nDiT replaces UNet backbone with standard vision transformer blocks."
        doc_file = io.BytesIO(doc_content)
        files = {"file": ("dit_meeting.md", doc_file, "text/markdown")}
        data = {
            "title": "Discussion on Diffusion Transformers",
            "participants": "Alex, Self",
            "domain": "Deep Learning & Computer Vision",
            "tags": json.dumps(["DiT", "Diffusion", "Transformers"])
        }
        resp = self.client.post("/api/conversation/upload_and_digest", files=files, data=data)
        self.assertEqual(resp.status_code, 200)
        res_json = resp.json()
        self.assertTrue(res_json.get("success"))
        self.assertIn("discussion-on-diffusion-transformers", res_json.get("slug"))

    def test_wiki_tree_contains_conversations(self):
        """Verifies GET /api/wiki/tree returns conversations category."""
        # First digest a conversation via API
        payload = {
            "title": "Tree Verification Sync",
            "raw_text": "Meeting notes checking sidebar categorization for discourse.",
            "participants": "Team",
            "domain": "Deep Learning & Computer Vision",
            "tags": ["TreeTest"]
        }
        digest_resp = self.client.post("/api/conversation/digest", json=payload)
        self.assertEqual(digest_resp.status_code, 200)

        # Query tree
        tree_resp = self.client.get("/api/wiki/tree?course=all")
        self.assertEqual(tree_resp.status_code, 200)
        tree = tree_resp.json()
        self.assertIn("conversations", tree)
        convs = tree["conversations"]
        self.assertIsInstance(convs, list)
        matching = [c for c in convs if "tree-verification-sync" in c.get("slug", "")]
        self.assertGreater(len(matching), 0)
        self.assertTrue(matching[0].get("is_conversation"))

if __name__ == "__main__":
    unittest.main()
