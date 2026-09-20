"""Unit tests for TypeSafe AI Jev 'System One' integration in Paideia Genesis."""
import unittest
from fastapi.testclient import TestClient

from src.config import TYPESAFE_API_KEY, ENABLE_JEV_SYSTEM_ONE
from src.llm.jev_client import JevClient, MockJevEngine, jev_client
from src.tutor.socratic_engine import SocraticTeacher
from src.anki.generator import AnkiManager
from src.api.server import app


class TestJevSystemOne(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.jev = JevClient()
        self.anki = AnkiManager()
        self.teacher = SocraticTeacher()

    def test_mock_engine_primitives(self):
        """Mock engine correctly implements Choice, Score, and Noul primitives."""
        questions = {
            "error_taxonomy": {
                "type": "choice",
                "instructions": "Classify error",
                "criteria": {"CLINICAL_CONTRAINDICATION": "Contraindicated drug", "MECHANISM_GAP": "Mechanism gap"}
            },
            "recall_quality": {
                "type": "score",
                "instructions": "Rate recall",
                "criteria": ["Level 0", "Level 1", "Level 2", "Level 3", "Level 4"]
            },
            "board_trap_triggered": {
                "type": "noul",
                "instructions": "Did student trigger board trap?"
            }
        }
        state = {
            "student_reasoning": "Administered carvedilol acutely in decompensated heart failure",
            "student_answer": "Inhibits NKCC2 in thick ascending limb"
        }

        answers = MockJevEngine.evaluate(state, questions)
        self.assertIn("error_taxonomy", answers)
        self.assertEqual(answers["error_taxonomy"]["type"], "choice")
        self.assertEqual(answers["error_taxonomy"]["choice"], "CLINICAL_CONTRAINDICATION")
        self.assertGreater(answers["error_taxonomy"]["confidence"], 0.8)

        self.assertIn("recall_quality", answers)
        self.assertEqual(answers["recall_quality"]["type"], "score")
        self.assertEqual(answers["recall_quality"]["score"], 4)

        self.assertIn("board_trap_triggered", answers)
        self.assertEqual(answers["board_trap_triggered"]["type"], "noul")
        self.assertGreater(answers["board_trap_triggered"]["noul"], 0.8)

    def test_vignette_diagnostic_triage(self):
        """Jev diagnostic triage classifies contraindicated medication and flags board trap."""
        vignette = {
            "vignette_id": "test-adhf-01",
            "stem": "68-year-old male presents with acute pulmonary edema and severe orthopnea...",
            "correct_option": "B",
            "topic": "Cardiovascular Pharmacology"
        }

        res = self.jev.diagnose_vignette_reasoning(
            vignette=vignette,
            selected_option="A",
            student_reasoning="Give carvedilol immediately to reduce chronic mortality"
        )
        self.assertTrue(res.success)
        self.assertTrue(res.system_one_active)
        self.assertGreater(res.latency_ms, 0)
        self.assertLess(res.latency_ms, 3000)  # Responsive latency guarantee over live internet network

        tax = res.answers.get("error_taxonomy", {})
        self.assertEqual(tax.get("choice"), "CLINICAL_CONTRAINDICATION")
        self.assertGreater(tax.get("confidence", 0), 0.9)

        trap = res.answers.get("board_trap_triggered", {})
        self.assertGreater(trap.get("noul", 0), 0.8)

    def test_active_recall_auto_grading_levels(self):
        """Jev correctly maps student recall accuracy to SM-2 spaced repetition levels."""
        card = {
            "front": "What is the molecular mechanism of Furosemide?",
            "pearl": "Inhibits the apical Na+/K+/2Cl- cotransporter (NKCC2) in the thick ascending limb of Henle."
        }

        # 1. Perfect recall -> Easy (Level 4 / Rating 4)
        good_res = self.jev.grade_free_text_recall(
            card=card,
            student_answer="Inhibits the NKCC2 symporter in the thick ascending limb abolishing the medullary osmotic gradient."
        )
        self.assertEqual(good_res["sm2_rating"], 4)
        self.assertEqual(good_res["rubric_level"], 4)
        self.assertIn("Easy", good_res["feedback_label"])

        # 2. Blank / failed recall -> Again (Level 0 / Rating 1)
        bad_res = self.jev.grade_free_text_recall(
            card=card,
            student_answer=""
        )
        self.assertEqual(bad_res["sm2_rating"], 1)
        self.assertEqual(bad_res["rubric_level"], 0)
        self.assertIn("Again", bad_res["feedback_label"])

    def test_document_classification_routing(self):
        """Jev routes medical text to appropriate organ block and yields Step-1 relevance score."""
        res = self.jev.classify_medical_document(
            title="Splanchnic Hemodynamics in Cirrhosis and Portal Hypertension",
            text="Cirrhosis produces increased intrahepatic resistance and hyperdynamic circulation. Beta-blockers reduce portal inflow."
        )
        self.assertEqual(res["organ_system"], "Hepatology")
        self.assertGreaterEqual(res["yield_score"], 2)

    def test_socratic_evaluate_includes_jev_telemetry(self):
        """SocraticTeacher.evaluate_response executes Jev System 1 and includes telemetry."""
        vignette = {
            "vignette_id": "test-vignette-telemetry",
            "stem": "Patient in acute pulmonary congestion...",
            "options": [{"id": "A", "text": "Carvedilol"}, {"id": "B", "text": "Furosemide"}],
            "correct_option": "B",
            "topic": "Cardiovascular"
        }
        res = self.teacher.evaluate_response(vignette, "A", "Start carvedilol for mortality benefit")
        self.assertIn("jev_system_one", res)
        jev_meta = res["jev_system_one"]
        self.assertTrue(jev_meta["active"])
        self.assertIn("latency_ms", jev_meta)
        self.assertEqual(jev_meta["error_taxonomy"], "CLINICAL_CONTRAINDICATION")
        self.assertTrue(jev_meta["board_trap_triggered"])

    def test_api_status_reports_system_one(self):
        """GET /api/status exposes Jev System One capability."""
        resp = self.client.get("/api/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("system_one", data)
        self.assertEqual(data["system_one"]["model"], "jev")
        self.assertTrue(data["system_one"]["enabled"])

    def test_api_grade_recall_endpoint(self):
        """POST /api/anki/cards/grade_recall auto-grades recall and updates SM-2 schedule."""
        cards = self.anki.get_staged_cards()
        self.assertGreater(len(cards), 0)
        card = cards[0]
        card_id = card["id"]

        # Supply accurate recall matching card's actual medical content
        matching_answer = card.get("pearl") or "Noncaseating granulomas and transmural inflammation in Crohn's disease"

        resp = self.client.post("/api/anki/cards/grade_recall", json={
            "card_id": card_id,
            "student_answer": matching_answer
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertIn("grading", data)
        self.assertIn("sm2_rating", data["grading"])
        self.assertIn("card", data)
        self.assertEqual(data["card"]["id"], card_id)
        self.assertGreaterEqual(data["card"]["repetitions"], 1)


if __name__ == "__main__":
    unittest.main()
