"""Unit and integration tests for Anthropic Contextual Retrieval in Paideia Genesis.
Tests chunking, situational context prefix generation, Contextual BM25 (FTS5),
Contextual Embeddings, Reciprocal Rank Fusion (RRF), Reranking, and API endpoints.
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

from src.wiki.indexer import WikiIndexer, chunk_markdown
from src.llm.client import get_llm_client, MockUniversalLLMClient
from src.api.server import app

class TestContextualRetrieval(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.concepts_dir = self.test_dir / "concepts"
        self.concepts_dir.mkdir(parents=True)
        self.llm = MockUniversalLLMClient()
        self.indexer = WikiIndexer(wiki_dir=self.test_dir, llm_client=self.llm)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_chunk_markdown_splitting(self):
        """Verifies markdown content is split into structured semantic chunks by header."""
        sample_md = """---
title: Raft Distributed Consensus Protocol
domain: Computer Science
system: Distributed Systems
---

# Raft Distributed Consensus Protocol

> **Core Summary**: Decomposed consensus algorithm structuring safety into leader election and log replication.

## Leader Election
In Raft, leader election is initiated when a follower's randomized heartbeat timeout expires without receiving heartbeats from a leader.
A candidate increments its current term, votes for itself, and sends RequestVote RPCs to all peers.

## Log Replication
Once a leader is elected, it begins serving client requests.
The leader appends entries to its local write-ahead log and issues AppendEntries RPCs to propagate entries to followers.
A log entry is considered committed once it has been replicated across a majority quorum of $F + 1$ nodes.

## Split-Brain Safety Trap
If network partition isolates the leader with a minority of nodes, the majority partition will elect a new leader.
The minority leader cannot commit new log entries because it cannot achieve a quorum.
"""
        chunks = chunk_markdown(sample_md, doc_title="Raft Distributed Consensus Protocol")
        self.assertGreaterEqual(len(chunks), 3)
        section_titles = [c["section_title"] for c in chunks]
        self.assertTrue(any("Leader Election" in t for t in section_titles))
        self.assertTrue(any("Log Replication" in t for t in section_titles))
        self.assertTrue(any("Split-Brain" in t for t in section_titles))

    def test_contextual_prefix_generation(self):
        """Verifies situational context prefix situates a chunk within the parent document."""
        whole_doc = """# Acute Decompensated Heart Failure (ADHF)
ADHF is a clinical syndrome characterized by impaired forward cardiac output and high venous filling pressures.
## Diuretic Management
Loop diuretics like intravenous furosemide are the first-line pharmacotherapy for fluid overload in ADHF."""
        chunk = "Loop diuretics like intravenous furosemide are the first-line pharmacotherapy for fluid overload in ADHF."

        prefix = self.llm.generate_contextual_prefix(whole_doc, chunk)
        self.assertIsInstance(prefix, str)
        self.assertGreater(len(prefix), 10)
        self.assertTrue("Acute Decompensated Heart Failure" in prefix or "chunk" in prefix)

    def test_contextual_indexing_and_bm25(self):
        """Verifies chunks are indexed into SQLite FTS5 with situational context."""
        doc_path = self.concepts_dir / "adhf-management.md"
        doc_path.write_text("""---
title: Acute Decompensated Heart Failure
tags: [cardiology, hemodynamics]
---
# Acute Decompensated Heart Failure

## Pathophysiology
Impaired ventricular systolic ejection causes retrograde pulmonary venous congestion.

## Pharmacotherapy
Intravenous furosemide is the cornerstone of decongestion therapy.
Beta-blockers must not be acutely initiated during active decompensation.
""", encoding="utf-8")

        self.indexer.index_file(doc_path)

        # Contextual search should match on exact keyword in chunk
        results = self.indexer.contextual_search("ventricular systolic ejection", limit=5)
        self.assertGreaterEqual(len(results), 1)
        top = results[0]
        self.assertEqual(top["title"], "Acute Decompensated Heart Failure")
        self.assertIn("context_summary", top)
        self.assertIn("section_title", top)
        self.assertIn("match_snippet", top)

    def test_hybrid_rrf_and_reranking(self):
        """Verifies hybrid Reciprocal Rank Fusion and cross-encoder reranking."""
        doc1 = self.concepts_dir / "raft.md"
        doc1.write_text("""---
title: Raft Protocol
---
# Raft Protocol
## Randomized Election Timeouts
Followers wait between 150ms and 300ms before becoming candidates to prevent split votes.
""", encoding="utf-8")

        doc2 = self.concepts_dir / "paxos.md"
        doc2.write_text("""---
title: Paxos Protocol
---
# Paxos Protocol
## Two Phase Commit
Phase 1 prepare and phase 2 accept ensure single-decree consensus across distributed nodes.
""", encoding="utf-8")

        self.indexer.index_file(doc1)
        self.indexer.index_file(doc2)

        results = self.indexer.contextual_search("randomized election timeouts candidates", limit=5, use_rerank=True)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Raft Protocol")
        self.assertIn("rrf_score", results[0])
        self.assertIn("rerank_score", results[0])
        self.assertGreater(results[0]["rrf_score"], 0.0)

    def test_api_contextual_search_endpoints(self):
        """Verifies FastAPI endpoints /api/wiki/search and /api/wiki/contextual_search."""
        client = TestClient(app)

        # 1. Standard search with contextual mode
        resp1 = client.get("/api/wiki/search?q=heart&mode=contextual")
        self.assertEqual(resp1.status_code, 200)
        data1 = resp1.json()
        self.assertEqual(data1["mode"], "contextual")
        self.assertIn("results", data1)

        # 2. Dedicated contextual search endpoint
        resp2 = client.get("/api/wiki/contextual_search?q=consensus&rerank=true")
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertEqual(data2["mode"], "contextual_retrieval")
        self.assertIn("results", data2)

if __name__ == "__main__":
    unittest.main()
