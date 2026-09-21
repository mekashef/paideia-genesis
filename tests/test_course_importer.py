import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from src.config import WIKI_DIR, RAW_SOURCES_DIR
from src.wiki.course_importer import CourseImporter
from src.api.server import app

class TestCourseImporter(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        client = TestClient(app)
        client.post("/api/wiki/reset", json={"confirm": True})

    def setUp(self):
        self.importer = CourseImporter()
        self.client = TestClient(app)

    def test_fetch_metadata(self):
        meta = self.importer.fetch_course_metadata("https://ocw.mit.edu/courses/hst-121-gastroenterology-fall-2005/pages/lecture-notes/")
        self.assertIn("HST.121", meta["course_code"])
        self.assertEqual(len(meta["sessions"]), 20)
        self.assertEqual(meta["sessions"][0]["session"], 1)

    def test_import_hst121_execution(self):
        res = self.importer.import_hst121_course()
        self.assertTrue(res["success"])
        self.assertEqual(res["sessions_imported"], 20)
        self.assertGreaterEqual(res["concepts_compiled"], 19)
        self.assertGreaterEqual(res["differentials_compiled"], 6)
        self.assertGreaterEqual(res["traps_compiled"], 3)
        self.assertEqual(res["session_pages_compiled"], 20)
        self.assertGreaterEqual(res["entities_compiled"], 28)

        # Check core concept files exist across all 20 lectures
        pud_file = WIKI_DIR / "concepts" / "peptic-ulcer-disease-and-h-pylori.md"
        cirrhosis_file = WIKI_DIR / "concepts" / "pathophysiology-of-cirrhosis.md"
        embryo_file = WIKI_DIR / "concepts" / "gi-embryology-and-malrotation.md"
        hepatitis_file = WIKI_DIR / "concepts" / "viral-hepatitis-and-serology.md"
        polyps_file = WIKI_DIR / "concepts" / "colorectal-neoplasms-and-polyps.md"
        metabolic_file = WIKI_DIR / "concepts" / "metabolic-liver-diseases.md"

        diff_file = WIKI_DIR / "differentials" / "crohns-vs-ulcerative-colitis.md"
        diarrhea_diff = WIKI_DIR / "differentials" / "secretory-vs-osmotic-diarrhea.md"
        trap_file = WIKI_DIR / "exam_traps" / "gi-board-traps.md"
        hbv_trap = WIKI_DIR / "exam_traps" / "hepatitis-b-serology-traps.md"

        # Check lecture session files
        ses1_file = WIKI_DIR / "course_sessions" / "session-01-overview-of-embryology-and-physiology.md"
        ses20_file = WIKI_DIR / "course_sessions" / "session-20-pathophysiological-consequences-of-cirrhosis.md"

        # Check entity files
        spiro_file = WIKI_DIR / "entities" / "spironolactone.md"
        omep_file = WIKI_DIR / "entities" / "omeprazole-ppi.md"
        cftr_file = WIKI_DIR / "entities" / "cftr.md"
        ugt1a1_file = WIKI_DIR / "entities" / "ugt1a1.md"

        self.assertTrue(pud_file.exists())
        self.assertTrue(cirrhosis_file.exists())
        self.assertTrue(embryo_file.exists())
        self.assertTrue(hepatitis_file.exists())
        self.assertTrue(polyps_file.exists())
        self.assertTrue(metabolic_file.exists())

        self.assertTrue(diff_file.exists())
        self.assertTrue(diarrhea_diff.exists())
        self.assertTrue(trap_file.exists())
        self.assertTrue(hbv_trap.exists())

        self.assertTrue(ses1_file.exists())
        self.assertTrue(ses20_file.exists())
        self.assertTrue(spiro_file.exists())
        self.assertTrue(omep_file.exists())
        self.assertTrue(cftr_file.exists())
        self.assertTrue(ugt1a1_file.exists())

        # Check cross-system associative links
        cirrhosis_text = cirrhosis_file.read_text(encoding="utf-8")
        self.assertIn("[[acute-decompensated-heart-failure]]", cirrhosis_text)
        self.assertIn("[[renin-angiotensin-aldosterone-system]]", cirrhosis_text)

        # Check raw manifest was saved
        manifest = RAW_SOURCES_DIR / "syllabus" / "MIT_HST121_Gastroenterology_Curriculum.json"
        self.assertTrue(manifest.exists())

    def test_course_import_api_endpoints(self):
        resp1 = self.client.post("/api/course/import_hst121")
        self.assertEqual(resp1.status_code, 200)
        data1 = resp1.json()
        self.assertTrue(data1["success"])
        self.assertEqual(data1["sessions_imported"], 20)

        resp2 = self.client.post("/api/course/import_url", json={
            "url": "https://ocw.mit.edu/courses/hst-121-gastroenterology-fall-2005/pages/lecture-notes/"
        })
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertTrue(data2["success"])

        # Check tree endpoint includes new concepts
        tree_resp = self.client.get("/api/wiki/tree")
        self.assertEqual(tree_resp.status_code, 200)
        tree_data = tree_resp.json()
        concept_slugs = [item["slug"] for item in tree_data.get("concepts", [])]
        self.assertIn("peptic-ulcer-disease-and-h-pylori", concept_slugs)
        self.assertIn("pathophysiology-of-cirrhosis", concept_slugs)

        # Check brain graph has nodes for new concepts
        graph_resp = self.client.get("/api/wiki/brain_graph")
        self.assertEqual(graph_resp.status_code, 200)
        graph_data = graph_resp.json()
        node_ids = [n["id"] for n in graph_data.get("nodes", [])]
        self.assertIn("peptic-ulcer-disease-and-h-pylori", node_ids)
        self.assertIn("pathophysiology-of-cirrhosis", node_ids)
