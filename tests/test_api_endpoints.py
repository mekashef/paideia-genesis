import unittest
from fastapi.testclient import TestClient
from src.api.server import app

class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from src.wiki.schema import init_wiki_structure
        from src.wiki.course_importer import CourseImporter
        from src.wiki.compiler import WikiCompiler
        from src.anki.generator import AnkiManager
        from src.config import BASE_DIR, WIKI_DIR

        init_wiki_structure()
        demo_lecture = BASE_DIR / "demo_data" / "Cardiology_Block_Lecture_4_Heart_Failure_and_Diuretics.md"
        if demo_lecture.exists() and not (WIKI_DIR / "concepts" / "acute-decompensated-heart-failure.md").exists():
            compiler = WikiCompiler()
            compiler.ingest_source(
                filename="Cardiology_Block_Lecture_4_Heart_Failure_and_Diuretics.md",
                content=demo_lecture.read_text(encoding="utf-8"),
                source_type="lecture"
            )
        sessions_dir = WIKI_DIR / "course_sessions"
        if not (sessions_dir / "session-20-pathophysiological-consequences-of-cirrhosis.md").exists():
            importer = CourseImporter()
            importer.import_mit_ocw_course()

            anki_mgr = AnkiManager()
            anki_mgr.recompile_from_wiki()

    @classmethod
    def tearDownClass(cls):
        client = TestClient(app)
        client.post("/api/wiki/reset", json={"confirm": True})

    def setUp(self):
        self.client = TestClient(app)

    def test_status_endpoint(self):
        resp = self.client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "online")
        self.assertIn("days_to_exam", data)
        self.assertIn("total_wiki_pages", data)

    def test_curriculum_endpoint(self):
        resp = self.client.get("/api/curriculum")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("current_block", data)
        self.assertIn("target_exam", data)

    def test_student_profile_endpoint(self):
        resp = self.client.get("/api/student/profile")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("readiness_score", data)
        self.assertIn("mastery", data)

    def test_vignette_and_evaluation(self):
        # 1. Generate vignette
        vignette_resp = self.client.post("/api/tutor/generate_vignette")
        self.assertEqual(vignette_resp.status_code, 200)
        vignette = vignette_resp.json()
        self.assertIn("stem", vignette)

        # 2. Submit evaluation
        eval_resp = self.client.post("/api/tutor/evaluate", json={
            "vignette": vignette,
            "selected_option_id": "B",
            "student_reasoning": "Furosemide relieves pulmonary congestion, avoid beta blockers."
        })
        self.assertEqual(eval_resp.status_code, 200)
        eval_data = eval_resp.json()
        self.assertTrue(eval_data["is_correct"])

    def test_anki_cards_and_export(self):
        # 1. Get all cards with stats
        cards_resp = self.client.get("/api/anki/cards")
        self.assertEqual(cards_resp.status_code, 200)
        data = cards_resp.json()
        cards = data.get("cards", [])
        self.assertGreaterEqual(len(cards), 80)
        self.assertIn("stats", data)
        self.assertGreaterEqual(data["stats"]["total"], 80)

        # 2. Test course filtering
        hst_resp = self.client.get("/api/anki/cards?course=hst121")
        self.assertEqual(hst_resp.status_code, 200)
        hst_cards = hst_resp.json().get("cards", [])
        self.assertGreater(len(hst_cards), 0)
        for c in hst_cards:
            self.assertIn(c.get("course"), ["HST.121", "Both"])

        # 3. Test system filtering
        hep_resp = self.client.get("/api/anki/cards?system=Hepatology")
        self.assertEqual(hep_resp.status_code, 200)
        hep_cards = hep_resp.json().get("cards", [])
        self.assertGreater(len(hep_cards), 0)
        for c in hep_cards:
            self.assertIn("hepat", c.get("system", "").lower())

        # 4. Test review submission (SM-2 rating)
        first_card_id = cards[0]["id"]
        review_resp = self.client.post("/api/anki/cards/review", json={
            "card_id": first_card_id,
            "rating": 3
        })
        self.assertEqual(review_resp.status_code, 200)
        review_data = review_resp.json()
        self.assertTrue(review_data["success"])
        self.assertEqual(review_data["card"]["id"], first_card_id)
        self.assertIn(review_data["card"]["mastery"], ["learning", "mastered"])


        # 5. Test recompilation
        recomp_resp = self.client.post("/api/anki/compile_from_wiki")
        self.assertEqual(recomp_resp.status_code, 200)
        self.assertTrue(recomp_resp.json()["success"])

        # 6. Export deck (master and filtered)
        export_resp = self.client.get("/api/anki/export?course=hst121")
        self.assertEqual(export_resp.status_code, 200)
        self.assertEqual(export_resp.headers["content-type"], "application/octet-stream")
        self.assertTrue(len(export_resp.content) > 0)


    def test_brain_graph_and_associative_recall(self):
        # 1. Brain graph default
        graph_resp = self.client.get("/api/wiki/brain_graph")
        self.assertEqual(graph_resp.status_code, 200)
        data = graph_resp.json()
        self.assertIn("nodes", data)
        self.assertIn("links", data)
        node_ids = {n["id"] for n in data["nodes"]}
        self.assertNotIn("index", node_ids)
        self.assertNotIn("SCHEMA", node_ids)

        # 2. Mechanisms layer
        mech_resp = self.client.get("/api/wiki/brain_graph?layer=mechanisms")
        self.assertEqual(mech_resp.status_code, 200)
        mech_data = mech_resp.json()
        categories = {n.get("category") for n in mech_data["nodes"]}
        self.assertNotIn("session", categories)

        # 3. Course filter HST.121
        hst_resp = self.client.get("/api/wiki/brain_graph?course=hst121")
        self.assertEqual(hst_resp.status_code, 200)
        hst_data = hst_resp.json()
        self.assertTrue(len(hst_data["nodes"]) > 0)
        for n in hst_data["nodes"]:
            self.assertIn(n.get("course"), ["HST.121", "Both"])

        # 4. Cardio filter
        cardio_resp = self.client.get("/api/wiki/brain_graph?course=cardio")
        self.assertEqual(cardio_resp.status_code, 200)
        cardio_data = cardio_resp.json()
        for n in cardio_data["nodes"]:
            self.assertIn(n.get("course"), ["Cardiopulmonary", "Both"])


        # Associative recall
        assoc_resp = self.client.get("/api/wiki/associative_recall?slug=acute-decompensated-heart-failure")
        self.assertEqual(assoc_resp.status_code, 200)
        assoc_data = assoc_resp.json()
        self.assertIn("associative_concepts", assoc_data)

    def test_page_update_live_editor(self):
        update_resp = self.client.put("/api/wiki/page", json={
            "path": "concepts/test-edit.md",
            "content": "# Test Edit\nLive in-place editing works perfectly."
        })
        self.assertEqual(update_resp.status_code, 200)
        self.assertTrue(update_resp.json()["success"])

    def test_quick_capture_endpoint(self):
        qc_resp = self.client.post("/api/wiki/quick_capture", json={
            "topic_hint": "Sulfa Allergy in Diuretics",
            "note": "Ethacrynic acid does not contain a sulfa moiety and is safe in sulfa-allergic patients."
        })
        self.assertEqual(qc_resp.status_code, 200)
        self.assertTrue(qc_resp.json()["success"])

    def test_pull_external_endpoint(self):
        pull_resp = self.client.post("/api/wiki/pull_external", json={
            "query": "Empagliflozin SGLT2 inhibitor"
        })
        self.assertEqual(pull_resp.status_code, 200)
        self.assertTrue(pull_resp.json()["success"])
        self.assertIn("title", pull_resp.json())

    def test_wiki_tree_course_filtering(self):
        # 1. All courses
        tree_all = self.client.get("/api/wiki/tree").json()
        self.assertIn("course_sessions", tree_all)
        self.assertIn("concepts", tree_all)
        self.assertTrue(len(tree_all["course_sessions"]) >= 20)

        # 2. HST.121 Filter
        tree_hst = self.client.get("/api/wiki/tree?course=hst121").json()
        self.assertEqual(len(tree_hst["course_sessions"]), 20)
        self.assertTrue(len(tree_hst["concepts"]) >= 15)
        for item in tree_hst["concepts"]:
            self.assertIn(item["course"], ["HST.121", "Both"])

        # 3. Cardio Filter
        tree_cardio = self.client.get("/api/wiki/tree?course=cardio").json()
        self.assertEqual(len(tree_cardio["course_sessions"]), 0)
        self.assertTrue(len(tree_cardio["concepts"]) >= 3)
        for item in tree_cardio["concepts"]:
            self.assertIn(item["course"], ["Cardiopulmonary", "Both"])

if __name__ == "__main__":
    unittest.main()
