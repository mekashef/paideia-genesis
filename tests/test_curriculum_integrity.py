"""Unit tests for curriculum data integrity across MIT HST.121 and Cardiopulmonary blocks."""
import unittest
from src.wiki.hst121_full_sessions_and_entities import (
    HST121_SESSIONS_WIKI,
    HST121_ENTITIES_WIKI
)
from src.wiki.hst121_curriculum import (
    HST121_CONCEPTS,
    HST121_DIFFERENTIALS,
    HST121_TRAPS,
    HST121_CURRICULUM_TOPICS
)


class TestCurriculumIntegrity(unittest.TestCase):
    """Verifies that medical curriculum data sets are complete, structurally valid, and linked."""

    def test_hst121_sessions_count_and_structure(self):
        """Ensures all 20 MIT HST.121 lecture sessions are populated with complete clinical metadata."""
        self.assertEqual(len(HST121_SESSIONS_WIKI), 20, "MIT HST.121 must contain exactly 20 lecture sessions")

        seen_session_nums = set()
        for session in HST121_SESSIONS_WIKI:
            s_num = session.get("session_num")
            self.assertIsNotNone(s_num)
            self.assertNotIn(s_num, seen_session_nums, f"Duplicate session number: {s_num}")
            seen_session_nums.add(s_num)

            self.assertTrue(session.get("slug"), f"Session {s_num} missing slug")
            self.assertTrue(session.get("title"), f"Session {s_num} missing title")
            self.assertTrue(session.get("summary"), f"Session {s_num} missing summary")
            self.assertTrue(session.get("content"), f"Session {s_num} missing content")
            self.assertIn("### Session Objectives", session["content"])

    def test_hst121_entities_count_and_fields(self):
        """Ensures all 28 pharmacological, anatomical, and pathological entities are complete."""
        self.assertGreaterEqual(len(HST121_ENTITIES_WIKI), 28, "MIT HST.121 must contain at least 28 high-yield entities")

        for entity in HST121_ENTITIES_WIKI:
            title = entity.get("title")
            self.assertTrue(title, "Entity missing title")
            self.assertTrue(entity.get("slug"), f"Entity '{title}' missing slug")
            self.assertTrue(entity.get("summary"), f"Entity '{title}' missing summary")
            self.assertTrue(entity.get("content"), f"Entity '{title}' missing content")
            self.assertTrue(
                "### " in entity["content"],
                f"Entity '{title}' content does not contain a markdown section header."
            )
            self.assertTrue(
                "Related:" in entity["content"],
                f"Entity '{title}' content missing related wikilinks."
            )

    def test_comparative_differentials_integrity(self):
        """Ensures comparative differentials have tables and discriminant features."""
        self.assertGreaterEqual(len(HST121_DIFFERENTIALS), 6, "Must contain at least 6 comparative differential tables")

        for diff in HST121_DIFFERENTIALS:
            self.assertTrue(diff.get("slug"), "Differential missing slug")
            self.assertTrue(diff.get("title"), f"Differential {diff.get('slug')} missing title")
            self.assertTrue(diff.get("content"), f"Differential {diff.get('slug')} missing content")
            self.assertIn("|", diff["content"], f"Differential {diff.get('slug')} must contain markdown table syntax")

    def test_exam_traps_integrity(self):
        """Ensures board exam traps highlight high-yield clinical fallacies and pearls."""
        self.assertGreaterEqual(len(HST121_TRAPS), 3, "Must contain at least 3 high-yield exam traps")

        for trap in HST121_TRAPS:
            self.assertTrue(trap.get("slug"), "Exam trap missing slug")
            self.assertTrue(trap.get("title"), f"Exam trap {trap.get('slug')} missing title")
            self.assertTrue(trap.get("content"), f"Exam trap {trap.get('slug')} missing content")
            self.assertIn("Pearl", trap["content"], f"Exam trap {trap.get('slug')} must contain clinical pearls")

    def test_curriculum_topics_coverage(self):
        """Verifies overall curriculum syllabus topics."""
        self.assertGreaterEqual(len(HST121_CURRICULUM_TOPICS), 5)
        self.assertGreaterEqual(len(HST121_CONCEPTS), 19)


if __name__ == "__main__":
    unittest.main()
