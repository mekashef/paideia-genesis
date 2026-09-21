"""Unit tests for HippoRAG associative spreading activation and multi-foci brain graph memory."""
import unittest
import shutil
import tempfile
from pathlib import Path
from src.wiki.graph_memory import AssociativeGraphMemory
from src.wiki.schema import init_wiki_structure


class TestHippoRAGActivation(unittest.TestCase):
    """Tests spreading activation, associative context discovery, and brain graph structure."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.wiki_dir = self.test_dir / "wiki"
        self.wiki_dir.mkdir(parents=True, exist_ok=True)
        init_wiki_structure(self.wiki_dir)

        # Create sample connected markdown notes
        concepts_dir = self.wiki_dir / "concepts"
        entities_dir = self.wiki_dir / "entities"

        (concepts_dir / "pathophysiology_of_cirrhosis.md").write_text(
            "# Pathophysiology of Cirrhosis\n\n"
            "Portal hypertension leads to [[ascites]] and [[spironolactone]] blockade.\n",
            encoding="utf-8"
        )

        (concepts_dir / "ascites.md").write_text(
            "# Ascites\n\n"
            "Peritoneal fluid accumulation. Linked to [[pathophysiology_of_cirrhosis]] and [[heart_failure]].\n",
            encoding="utf-8"
        )

        (concepts_dir / "heart_failure.md").write_text(
            "# Heart Failure\n\n"
            "Reduced cardiac output leads to venous congestion and [[spironolactone]] usage.\n",
            encoding="utf-8"
        )

        (entities_dir / "spironolactone.md").write_text(
            "# Spironolactone\n\n"
            "Aldosterone antagonist used in [[pathophysiology_of_cirrhosis]] and [[heart_failure]].\n",
            encoding="utf-8"
        )

        self.memory = AssociativeGraphMemory(wiki_dir=self.wiki_dir)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_graph_nodes_and_edges_populated(self):
        """Graph memory should index markdown files and link them via wikilinks."""
        brain_graph = self.memory.get_brain_graph()
        self.assertIn("nodes", brain_graph)
        self.assertIn("links", brain_graph)
        self.assertGreaterEqual(len(brain_graph["nodes"]), 3)
        self.assertGreaterEqual(len(brain_graph["links"]), 2)

    def test_spreading_activation_scores(self):
        """Spreading activation should assign highest associative activation to connected concepts."""
        ranks = self.memory.spreading_activation(seed_slugs=["pathophysiology_of_cirrhosis"])
        self.assertIn("pathophysiology_of_cirrhosis", ranks)
        self.assertIn("ascites", ranks)
        # Directly linked nodes should have positive activation
        self.assertGreater(ranks.get("ascites", 0.0), 0.0)

    def test_get_associative_context(self):
        """Retrieves top associative concepts ranked by spreading activation."""
        context = self.memory.get_associative_context(seed_slugs=["pathophysiology_of_cirrhosis"], top_k=3)
        self.assertIsInstance(context, list)
        self.assertGreater(len(context), 0)
        top_slugs = [item["slug"] for item in context]
        # Connected concepts should be retrieved
        self.assertTrue(any(s in top_slugs for s in ["ascites", "spironolactone", "heart_failure"]))

    def test_nonexistent_concept_handling(self):
        """Querying nonexistent concept should gracefully return fallback distribution without crashing."""
        context = self.memory.get_associative_context(seed_slugs=["completely_unknown_condition"], top_k=2)
        self.assertIsInstance(context, list)


if __name__ == "__main__":
    unittest.main()
