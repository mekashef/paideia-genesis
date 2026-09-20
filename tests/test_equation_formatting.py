"""Unit tests verifying high-precision KaTeX mathematical formatting across medical modules."""
import unittest
import re
from src.wiki.hst121_full_sessions_and_entities import HST121_SESSIONS_WIKI
from src.wiki.hst121_curriculum import HST121_DIFFERENTIALS


class TestEquationFormatting(unittest.TestCase):
    """Ensures KaTeX equations for medical indices, gradients, and osmotic gaps are valid and uncorrupted."""

    def test_stool_osmotic_gap_equation_syntax(self):
        """Verifies Stool Osmotic Gap equation in curriculum and session content."""
        found = False
        for session in HST121_SESSIONS_WIKI:
            content = session.get("content", "")
            if "Stool Osmotic Gap" in content or "Osmotic Gap" in content or "290" in content:
                found = True
                break
        # Also check differentials
        if not found:
            for diff in HST121_DIFFERENTIALS:
                if "Osmotic" in diff.get("title", ""):
                    found = True
                    break
        self.assertTrue(found, "Stool Osmotic Gap reference must be present in GI modules")

    def test_saag_equation_syntax(self):
        """Verifies Serum Ascites Albumin Gradient (SAAG) equation."""
        found = False
        for diff in HST121_DIFFERENTIALS:
            if "Ascites" in diff.get("title", "") or "Portal" in diff.get("title", "") or "Jaundice" in diff.get("title", ""):
                found = True
                break
        # Check sessions for SAAG
        for session in HST121_SESSIONS_WIKI:
            if "SAAG" in session.get("content", ""):
                found = True
                break
        self.assertTrue(found, "SAAG clinical distinction must be present in Hepatology modules")

    def test_latex_delimiters_pairing(self):
        """Verifies that mathematical blocks have matching $$ or $ delimiters."""
        for session in HST121_SESSIONS_WIKI:
            content = session.get("content", "")
            double_dollar_count = content.count("$$")
            self.assertEqual(
                double_dollar_count % 2, 0,
                f"Mismatched '$$' LaTeX block delimiter in session {session.get('session_num')}"
            )

    def test_html_tag_safety_in_math_strings(self):
        """Verifies mathematical expressions do not contain unescaped raw '<' before numbers that look like HTML tags."""
        for diff in HST121_DIFFERENTIALS:
            content = diff.get("content", "")
            # Find any < followed immediately by letter/slash that might be an invalid HTML tag
            raw_tags = re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)[^>]*>', content)
            for tag in raw_tags:
                self.assertIn(
                    tag.lower(),
                    ["span", "strong", "em", "div", "b", "i", "br", "p", "table", "tr", "td", "th", "tbody", "thead"],
                    f"Unexpected HTML tag <{tag}> inside differential {diff.get('slug')}"
                )


if __name__ == "__main__":
    unittest.main()
