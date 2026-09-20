import unittest
import tempfile
import shutil
from pathlib import Path
from src.tutor.socratic_engine import SocraticTeacher
from src.llm.client import MockMedicalLLMClient

class TestSocraticEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.mock_llm = MockMedicalLLMClient()
        self.teacher = SocraticTeacher(llm_client=self.mock_llm, wiki_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_vignette(self):
        vignette = self.teacher.generate_adaptive_vignette()
        self.assertIn("stem", vignette)
        self.assertIn("options", vignette)
        self.assertEqual(len(vignette["options"]), 4)
        self.assertIn("correct_option", vignette)

    def test_evaluate_response_wrong_answer_trap_recorded(self):
        vignette = self.teacher.generate_adaptive_vignette()
        # Option A is incorrect in our sample vignette
        evaluation = self.teacher.evaluate_response(
            vignette=vignette,
            selected_option_id="A",
            student_reasoning="I thought beta blockers were standard for heart failure."
        )
        self.assertFalse(evaluation["is_correct"])
        self.assertIn("socratic_critique", evaluation)
        self.assertIn("anki_card_candidate", evaluation)

        # Verify trap file was compiled into wiki/exam_traps/
        traps_dir = self.test_dir / "exam_traps"
        trap_files = list(traps_dir.glob("*.md"))
        self.assertTrue(len(trap_files) >= 1)

if __name__ == "__main__":
    unittest.main()
