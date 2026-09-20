import unittest
import tempfile
import shutil
from pathlib import Path
from src.tutor.student_profile import StudentProfile

class TestStudentProfile(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.profile = StudentProfile(profile_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_schedule_and_countdown(self):
        schedule = self.profile.get_schedule()
        self.assertIn("target_exam", schedule)
        self.assertIn("days_remaining", schedule)
        self.assertGreaterEqual(schedule["days_remaining"], 0)

    def test_record_attempt_success_and_penalty(self):
        initial_mastery = self.profile.get_mastery()
        cardio_initial = initial_mastery["Cardiovascular"]

        # Record correct attempt
        self.profile.record_attempt("Cardiovascular Pharmacology", is_correct=True)
        updated_mastery = self.profile.get_mastery()
        self.assertGreater(updated_mastery["Cardiovascular"], cardio_initial)

        # Record incorrect attempt
        self.profile.record_attempt(
            "Cardiovascular Pharmacology",
            is_correct=False,
            error_type="CLINICAL_CONTRAINDICATION",
            details="Gave beta blocker during acute decompensation"
        )
        post_fail_mastery = self.profile.get_mastery()
        self.assertLess(post_fail_mastery["Cardiovascular"], updated_mastery["Cardiovascular"])

        # Check misconception logged
        summary = self.profile.get_profile_summary()
        self.assertIn("CLINICAL_CONTRAINDICATION", summary["misconceptions_raw"])

if __name__ == "__main__":
    unittest.main()
