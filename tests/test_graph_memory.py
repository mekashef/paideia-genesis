import unittest
import tempfile
import shutil
from pathlib import Path
from src.wiki.graph_memory import AssociativeGraphMemory

class TestGraphMemory(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.concepts_dir = self.test_dir / "concepts"
        self.concepts_dir.mkdir(parents=True)

        # Create interlinked concepts
        (self.concepts_dir / "heart-failure.md").write_text(
            "---\ntitle: Heart Failure\n---\n# Heart Failure\nLinks to [[loop-diuretics]] and [[inotropes]].\n",
            encoding="utf-8"
        )
        (self.concepts_dir / "loop-diuretics.md").write_text(
            "---\ntitle: Loop Diuretics\n---\n# Loop Diuretics\nLinks to [[hypokalemia]] and [[heart-failure]].\n",
            encoding="utf-8"
        )
        (self.concepts_dir / "inotropes.md").write_text(
            "---\ntitle: Inotropic Agents\n---\n# Inotropic Agents\nLinks to [[cardiogenic-shock]].\n",
            encoding="utf-8"
        )
        (self.concepts_dir / "hypokalemia.md").write_text(
            "---\ntitle: Hypokalemia\n---\n# Hypokalemia\nElectrolyte disturbance.\n",
            encoding="utf-8"
        )
        (self.concepts_dir / "cardiogenic-shock.md").write_text(
            "---\ntitle: Cardiogenic Shock\n---\n# Cardiogenic Shock\nHemodynamic collapse.\n",
            encoding="utf-8"
        )

        self.memory = AssociativeGraphMemory(wiki_dir=self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_build_graph(self):
        adj, meta = self.memory.build_graph()
        self.assertIn("heart-failure", adj)
        self.assertIn("loop-diuretics", adj["heart-failure"])
        self.assertIn("inotropes", adj["heart-failure"])
        self.assertEqual(meta["heart-failure"]["title"], "Heart Failure")

    def test_spreading_activation_hipporag(self):
        # Spreading activation from heart-failure should activate loop-diuretics and multi-hop hypokalemia
        ranks = self.memory.spreading_activation(["heart-failure"])
        self.assertTrue(len(ranks) >= 4)
        # Directly linked nodes should have higher activation than unlinked
        self.assertGreater(ranks.get("loop-diuretics", 0), 0)
        self.assertGreater(ranks.get("inotropes", 0), 0)

    def test_associative_context_retrieval(self):
        context = self.memory.get_associative_context(["heart-failure"], top_k=3)
        self.assertTrue(len(context) >= 1)
        top_slugs = [c["slug"] for c in context]
        # Direct links should be ranked in top associations
        self.assertTrue("loop-diuretics" in top_slugs or "inotropes" in top_slugs)

    def test_brain_graph_enrichment(self):
        bg = self.memory.get_brain_graph()
        self.assertIn("nodes", bg)
        self.assertIn("links", bg)
        self.assertTrue(len(bg["nodes"]) >= 4)
        # Check node mastery is attached
        self.assertIn("mastery", bg["nodes"][0])
        self.assertIn("system", bg["nodes"][0])
        self.assertIn("entity_type", bg["nodes"][0])

    def test_admin_files_excluded_from_graph(self):
        # Create admin files that shouldn't appear in graph
        (self.test_dir / "index.md").write_text("# Master Index\n[[heart-failure]]\n[[loop-diuretics]]\n", encoding="utf-8")
        (self.test_dir / "SCHEMA.md").write_text("# Schema\n[[heart-failure]]\n", encoding="utf-8")
        (self.test_dir / "log.md").write_text("# Log\n[[heart-failure]]\n", encoding="utf-8")
        
        bg = self.memory.get_brain_graph()
        node_ids = {n["id"] for n in bg["nodes"]}
        self.assertNotIn("index", node_ids)
        self.assertNotIn("SCHEMA", node_ids)
        self.assertNotIn("log", node_ids)
        for link in bg["links"]:
            self.assertNotIn(link["source"], ["index", "SCHEMA", "log"])
            self.assertNotIn(link["target"], ["index", "SCHEMA", "log"])

    def test_course_and_layer_filters(self):
        # Add a session file
        sessions_dir = self.test_dir / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / "lec-01.md").write_text(
            "---\ntitle: Lec 01: Introduction\n---\n# Lecture 1\nLinks [[heart-failure]].\n",
            encoding="utf-8"
        )
        
        # Test layer=mechanisms filters out session
        bg_mech = self.memory.get_brain_graph(layer="mechanisms")
        node_cats = {n.get("category") for n in bg_mech["nodes"]}
        self.assertNotIn("session", node_cats)
        
        # Test layer=all includes session
        bg_all = self.memory.get_brain_graph(layer="all")
        node_ids = {n["id"] for n in bg_all["nodes"]}
        self.assertIn("lec-01", node_ids)

    def test_entity_metadata_takes_priority_over_name_guesses(self):
        entities = self.test_dir / "entities"
        entities.mkdir()
        (entities / "flow-model.md").write_text(
            "---\ntitle: Flow Model\ndomain: Physics\ncourse: PHY 101\n"
            "entity_type: protocol\n---\n# Flow Model\n",
            encoding="utf-8",
        )
        (entities / "uav-flow.md").write_text(
            "---\ntitle: UAV Flow\ndomain: Robotics\n---\n# UAV Flow\n",
            encoding="utf-8",
        )
        _, meta = self.memory.build_graph()
        self.assertEqual(meta["flow-model"]["entity_type"], "protocol")
        self.assertEqual(meta["flow-model"]["course"], "PHY 101")
        self.assertEqual(meta["uav-flow"]["entity_type"], "algorithm")
        models = self.memory.get_brain_graph(layer="models")
        self.assertNotIn("flow-model", {node["id"] for node in models["nodes"]})

if __name__ == "__main__":
    unittest.main()
