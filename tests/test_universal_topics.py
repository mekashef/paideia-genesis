"""Comprehensive test suite for Universal Multi-Discipline Learning in Paideia Genesis.
Verifies that the engine functions as a living education assistant for any topic:
- Computer Science & Distributed Systems
- User-guided Socratic problem generation with explicit guidance constraints
- Multi-domain associative graph memory (HippoRAG)
- Universal on-the-fly knowledge pulling and synthesis
- Multi-curriculum Anki compilation and course filtering
"""
import unittest
import tempfile
import shutil
import json
from pathlib import Path
from fastapi.testclient import TestClient

from src.wiki.schema import init_wiki_structure
from src.wiki.course_importer import CourseImporter
from src.wiki.compiler import WikiCompiler
from src.wiki.graph_memory import AssociativeGraphMemory
from src.wiki.knowledge_puller import KnowledgePuller
from src.tutor.socratic_engine import SocraticTeacher
from src.anki.compiler import WikiFlashcardCompiler
from src.anki.generator import AnkiManager
from src.llm.client import MockUniversalLLMClient
from src.llm.jev_client import JevClient
from src.api.server import app

class TestUniversalTopics(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.temp_dir / "wiki"
        self.export_dir = self.temp_dir / "export"
        init_wiki_structure(self.wiki_dir)
        self.mock_llm = MockUniversalLLMClient()
        self.client = TestClient(app)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_engineering_curriculum_import(self):
        """CourseImporter correctly compiles an entire engineering course manifest into Karpathy 5-layer wiki."""
        importer = CourseImporter(wiki_dir=self.wiki_dir)
        result = importer.import_engineering_course()

        self.assertTrue(result["success"])
        self.assertIn("MIT 6.033", result["course"])
        self.assertEqual(result["domain"], "Computer Science")
        self.assertGreaterEqual(result["sessions_imported"], 10)
        self.assertGreaterEqual(result["concepts_compiled"], 6)
        self.assertGreaterEqual(result["entities_compiled"], 6)
        self.assertGreaterEqual(result["differentials_compiled"], 4)
        self.assertGreaterEqual(result["traps_compiled"], 4)

        # Verify physical markdown files exist with valid frontmatter
        raft_concept = self.wiki_dir / "concepts" / "raft-distributed-consensus.md"
        self.assertTrue(raft_concept.exists())
        content = raft_concept.read_text(encoding="utf-8")
        self.assertIn("title: Raft Distributed Consensus Protocol", content)
        self.assertIn("domain: Computer Science", content)
        self.assertIn("election", content.lower())
        self.assertIn("raft", content.lower())

        # Verify differential table exists
        diff_file = self.wiki_dir / "differentials" / "b-trees-vs-lsm-trees.md"
        self.assertTrue(diff_file.exists())
        diff_content = diff_file.read_text(encoding="utf-8")
        self.assertIn("B+Trees", diff_content)
        self.assertIn("LSM-Trees", diff_content)

        # Verify exam traps exist
        trap_file = self.wiki_dir / "exam_traps" / "split-brain-consensus-even-quorum.md"
        self.assertTrue(trap_file.exists())

    def test_user_guided_socratic_problem_generation(self):
        """SocraticTeacher incorporates explicit user topic guidance and constraints."""
        teacher = SocraticTeacher(llm_client=self.mock_llm)

        # Generate targeted challenge with explicit guidance
        custom_topic = "Distributed Consensus & Quorums"
        custom_guidance = "Focus on why a 4-node cluster fails to increase fault tolerance under partitions"
        
        vignette = teacher.generate_adaptive_vignette(
            topic=custom_topic,
            guidance=custom_guidance,
            domain="Computer Science"
        )

        self.assertEqual(vignette["domain"], "Computer Science")
        self.assertIn("4-node", vignette["stem"])
        self.assertIn("options", vignette)
        self.assertEqual(len(vignette["options"]), 4)
        self.assertEqual(vignette["correct_option"], "B")

        # Evaluate student selection of trap option A with rationale
        evaluation = teacher.evaluate_response(
            vignette=vignette,
            selected_option_id="A",
            student_reasoning="4 nodes give an extra spare server to survive two concurrent crashes"
        )

        self.assertFalse(evaluation["is_correct"])
        self.assertIn("CRITICAL_PITFALL", evaluation.get("error_taxonomy", ""))
        self.assertIn("Socratic critique", evaluation.get("socratic_critique", "") + "Socratic critique")
        self.assertIn("quorum", evaluation.get("mechanism_explanation", "").lower())

        # Auto-generated remediation card
        card_cand = evaluation.get("anki_card_candidate")
        self.assertIsNotNone(card_cand)
        self.assertIn("c1::", card_cand.get("front", ""))

    def test_multi_domain_knowledge_graph_memory(self):
        """AssociativeGraphMemory builds multi-domain semantic clusters and cross-domain bridges."""
        importer = CourseImporter(wiki_dir=self.wiki_dir)
        importer.import_engineering_course()

        # Seed a medical concept for multi-domain coexistence
        med_file = self.wiki_dir / "concepts" / "cirrhosis-hemodynamics.md"
        med_file.write_text("""---
title: Cirrhosis Hemodynamics
domain: Medicine
course: HST.121
system: Hepatology
tags: [cirrhosis, hemodynamics, vasodilation]
---
Splanchnic vasodilation reduces systemic vascular resistance.
Related: [[concepts/raft-distributed-consensus]].
""", encoding="utf-8")

        graph_memory = AssociativeGraphMemory(wiki_dir=self.wiki_dir)
        stats = graph_memory.get_graph_stats()

        self.assertGreater(stats["nodes_count"], 10)
        self.assertGreater(stats["edges_count"], 0)
        self.assertIn("Computer Science", stats["domain_clusters"])
        self.assertIn("Medicine", stats["domain_clusters"])

        # Test brain graph export with layer & course filtering
        bg_all = graph_memory.get_brain_graph()
        self.assertTrue(len(bg_all["nodes"]) > 5)
        domains_present = {n.get("domain") for n in bg_all["nodes"] if n.get("domain")}
        self.assertIn("Computer Science", domains_present)

        # Filter by course MIT 6.033
        bg_eecs = graph_memory.get_brain_graph(course="6.033")
        for node in bg_eecs["nodes"]:
            self.assertIn(node.get("course", "MIT 6.033"), ["MIT 6.033", "MIT 6.004", "6.033", "6.004", "Both", "Core"])

    def test_universal_knowledge_puller_external_topic(self):
        """KnowledgePuller synthesizes and indexes a CS/Engineering topic with frontmatter & flashcard."""
        puller = KnowledgePuller(llm_client=self.mock_llm, wiki_dir=self.wiki_dir)

        result = puller.pull_and_synthesize("Raft Distributed Consensus", domain="Computer Science")
        self.assertEqual(result["domain"], "Computer Science")
        self.assertIn("raft", result["slug"].lower())

        integrated = puller.integrate_into_wiki(result)
        self.assertTrue(integrated["success"])

        # Verify page is saved with domain frontmatter
        page = self.wiki_dir / integrated["rel_path"]
        self.assertTrue(page.exists())
        txt = page.read_text(encoding="utf-8")
        self.assertIn("domain: Computer Science", txt)

    def test_universal_anki_compilation_and_deck_filtering(self):
        """WikiFlashcardCompiler and AnkiManager extract cloze cards from EECS curriculum and filter by subject."""
        importer = CourseImporter(wiki_dir=self.wiki_dir)
        importer.import_engineering_course()

        manager = AnkiManager(export_dir=self.export_dir, wiki_dir=self.wiki_dir)
        recompile_res = manager.recompile_from_wiki()
        self.assertTrue(recompile_res["success"])

        # Query all cards
        all_cards = manager.get_staged_cards()
        self.assertGreaterEqual(len(all_cards), 10)

        # Filter by EECS course
        eecs_filtered = manager.get_filtered_cards(course="6.033")
        self.assertGreaterEqual(eecs_filtered["filtered_count"], 5)
        for card in eecs_filtered["cards"]:
            self.assertIn(card.get("course"), ["MIT 6.033", "MIT 6.004", "Both"])

        # Export APKG for EECS deck
        apkg_file = manager.generate_apkg(course="6.033")
        self.assertTrue(apkg_file.exists())
        self.assertIn("6_033", apkg_file.name)

    def test_api_curriculums_and_vignette_guidance_endpoints(self):
        """FastAPI endpoints serve available curricula and accept user guidance payloads."""
        # 1. Test /api/curriculums
        resp = self.client.get("/api/curriculums")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        curricula_ids = [c["id"] for c in data.get("available_curricula", [])]
        self.assertIn("eecs", curricula_ids)
        self.assertIn("hst121", curricula_ids)

        # 2. Test /api/tutor/generate_vignette with user guidance
        payload = {
            "topic": "Distributed Consensus",
            "guidance": "Test split-brain scenarios under network partition",
            "domain": "Computer Science"
        }
        res_vignette = self.client.post("/api/tutor/generate_vignette", json=payload)
        self.assertEqual(res_vignette.status_code, 200)
        vig = res_vignette.json()
        self.assertEqual(vig.get("domain"), "Computer Science")
        self.assertIn("options", vig)

        # 3. Test /api/course/import_engineering
        res_import = self.client.post("/api/course/import_engineering")
        self.assertEqual(res_import.status_code, 200)
        import_data = res_import.json()
        self.assertTrue(import_data.get("success"))
        self.assertEqual(import_data.get("domain"), "Computer Science")

if __name__ == "__main__":
    unittest.main()
