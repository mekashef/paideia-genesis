"""SQLite FTS5 full-text search, contextual retrieval, and wikilink graph indexer for Paideia Genesis."""
import re
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import DB_PATH, WIKI_DIR
from src.llm.client import get_llm_client, BaseLLMClient

WIKILINK_PATTERN = re.compile(r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def get_db_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_indexer_db(db_path: Path = DB_PATH):
    """Initializes the SQLite database with document FTS5, contextual chunk FTS5, and links table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # Document-level FTS5 full-text table
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS wiki_fts USING fts5(
        rel_path UNINDEXED,
        category,
        title,
        tags,
        content,
        tokenize = 'porter unicode61'
    );
    """)
    
    # Metadata table for quick metadata checks and modified timestamps
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_meta (
        rel_path TEXT PRIMARY KEY,
        category TEXT,
        title TEXT,
        tags TEXT,
        mtime REAL
    );
    """)

    # Links table for graph view
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_links (
        source_slug TEXT,
        target_slug TEXT,
        link_text TEXT,
        PRIMARY KEY (source_slug, target_slug)
    );
    """)

    # Anthropic Contextual Retrieval: Chunk storage table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_chunks (
        chunk_id TEXT PRIMARY KEY,
        rel_path TEXT,
        chunk_index INTEGER,
        section_title TEXT,
        original_content TEXT,
        context_summary TEXT,
        contextualized_text TEXT,
        embedding_json TEXT
    );
    """)

    # Anthropic Contextual Retrieval: Contextual BM25 FTS5 index
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS wiki_chunks_fts USING fts5(
        chunk_id UNINDEXED,
        rel_path UNINDEXED,
        section_title,
        context_summary,
        contextualized_text,
        tokenize = 'porter unicode61'
    );
    """)

    conn.commit()
    conn.close()

def parse_markdown_file(file_path: Path) -> Dict[str, Any]:
    """Extracts frontmatter metadata, title, and body from a markdown file."""
    content = file_path.read_text(encoding="utf-8", errors="replace")
    title = file_path.stem.replace("-", " ").title()
    tags = ""
    system = ""
    source = ""
    domain = ""
    course = ""
    category = ""
    entity_type = ""
    frontmatter: Dict[str, Any] = {}
    body = content

    fm_match = FRONTMATTER_PATTERN.match(content)
    if fm_match:
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        for line in fm_text.splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip('"\'')
                frontmatter[k] = v
                if k == "title":
                    title = v
                elif k == "tags":
                    tags = v
                elif k == "system":
                    system = v
                elif k == "source":
                    source = v
                elif k == "domain":
                    domain = v
                elif k == "course":
                    course = v
                elif k == "category":
                    category = v
                elif k == "entity_type":
                    entity_type = v

    # Extract first H1 if title was not in frontmatter
    if not fm_match:
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break

    # Extract wikilinks
    links = []
    for match in WIKILINK_PATTERN.finditer(body):
        target = match.group(1).strip()
        display = match.group(2).strip() if match.group(2) else target
        links.append((target, display))

    return {
        "title": title,
        "tags": tags,
        "system": system,
        "source": source,
        "domain": domain,
        "course": course,
        "category": category,
        "entity_type": entity_type,
        "frontmatter": frontmatter,
        "body": body,
        "raw": content,
        "links": links
    }

def chunk_markdown(content: str, doc_title: str = "") -> List[Dict[str, Any]]:
    """Splits markdown content into logical semantic chunks based on headers and paragraphs."""
    body = content
    fm_match = FRONTMATTER_PATTERN.match(content)
    if fm_match:
        body = content[fm_match.end():].strip()

    lines = body.splitlines()
    sections: List[Dict[str, Any]] = []
    current_title = doc_title or "Overview"
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                text_block = "\n".join(current_lines).strip()
                if text_block:
                    sections.append({"section_title": current_title, "content": text_block})
                current_lines = []
            current_title = line.lstrip("#").strip()
        else:
            current_lines.append(line)

    if current_lines:
        text_block = "\n".join(current_lines).strip()
        if text_block:
            sections.append({"section_title": current_title, "content": text_block})

    if not sections:
        clean_body = body.strip()
        if clean_body:
            sections = [{"section_title": doc_title or "Content", "content": clean_body}]

    final_chunks: List[Dict[str, Any]] = []
    for s in sections:
        text = s["content"]
        if len(text) > 1200:
            paragraphs = text.split("\n\n")
            curr_chunk = []
            curr_len = 0
            sub_idx = 1
            for p in paragraphs:
                p_str = p.strip()
                if not p_str:
                    continue
                if curr_len + len(p_str) > 1000 and curr_chunk:
                    final_chunks.append({
                        "section_title": f"{s['section_title']} (Part {sub_idx})",
                        "content": "\n\n".join(curr_chunk)
                    })
                    sub_idx += 1
                    curr_chunk = [p_str]
                    curr_len = len(p_str)
                else:
                    curr_chunk.append(p_str)
                    curr_len += len(p_str)
            if curr_chunk:
                final_chunks.append({
                    "section_title": f"{s['section_title']} (Part {sub_idx})" if sub_idx > 1 else s['section_title'],
                    "content": "\n\n".join(curr_chunk)
                })
        else:
            final_chunks.append(s)

    return final_chunks

class WikiIndexer:
    def __init__(self, wiki_dir: Path = WIKI_DIR, db_path: Optional[Path] = None, llm_client: Optional[BaseLLMClient] = None):
        self.wiki_dir = wiki_dir
        if db_path:
            self.db_path = db_path
        elif self.wiki_dir != WIKI_DIR:
            self.db_path = self.wiki_dir / "index.db"
        else:
            self.db_path = DB_PATH
        self.llm = llm_client or get_llm_client()
        init_indexer_db(self.db_path)

    def index_file(self, file_path: Path):
        """Indexes a single markdown file into document FTS and contextual chunks."""
        if not file_path.exists() or file_path.suffix != ".md":
            return
            
        rel_path = str(file_path.relative_to(self.wiki_dir))
        category = file_path.parent.name if file_path.parent != self.wiki_dir else "root"
        mtime = file_path.stat().st_mtime
        
        parsed = parse_markdown_file(file_path)
        source_slug = file_path.stem

        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # Delete existing entries
        cursor.execute("DELETE FROM wiki_fts WHERE rel_path = ?", (rel_path,))
        cursor.execute("DELETE FROM wiki_meta WHERE rel_path = ?", (rel_path,))
        cursor.execute("DELETE FROM wiki_links WHERE source_slug = ?", (source_slug,))
        cursor.execute("DELETE FROM wiki_chunks WHERE rel_path = ?", (rel_path,))
        cursor.execute("DELETE FROM wiki_chunks_fts WHERE rel_path = ?", (rel_path,))

        # Insert into FTS
        cursor.execute(
            "INSERT INTO wiki_fts (rel_path, category, title, tags, content) VALUES (?, ?, ?, ?, ?)",
            (rel_path, category, parsed["title"], parsed["tags"], parsed["body"])
        )

        # Insert into Meta
        cursor.execute(
            "INSERT INTO wiki_meta (rel_path, category, title, tags, mtime) VALUES (?, ?, ?, ?, ?)",
            (rel_path, category, parsed["title"], parsed["tags"], mtime)
        )

        # Insert links
        for target, display in parsed["links"]:
            target_slug = Path(target).stem
            cursor.execute(
                "INSERT OR IGNORE INTO wiki_links (source_slug, target_slug, link_text) VALUES (?, ?, ?)",
                (source_slug, target_slug, display)
            )

        # Anthropic Contextual Retrieval: Chunk & Situational Prepending
        if category != "student_profile" and file_path.name not in ["SCHEMA.md", "log.md", "index.md"]:
            chunks = chunk_markdown(parsed["raw"], doc_title=parsed["title"])
            for idx, c in enumerate(chunks):
                chunk_id = f"{rel_path}#chunk-{idx}"
                sec_title = c.get("section_title", parsed["title"])
                orig_content = c.get("content", "").strip()
                if not orig_content:
                    continue

                context_summary = self.llm.generate_contextual_prefix(parsed["raw"], orig_content)
                contextualized_text = f"Context: {context_summary}\nDocument: {parsed['title']}\nSection: {sec_title}\n\n{orig_content}"
                emb_vec = self.llm.embed_text(contextualized_text)
                emb_json = json.dumps(emb_vec)

                cursor.execute(
                    """INSERT INTO wiki_chunks
                       (chunk_id, rel_path, chunk_index, section_title, original_content, context_summary, contextualized_text, embedding_json)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (chunk_id, rel_path, idx, sec_title, orig_content, context_summary, contextualized_text, emb_json)
                )

                cursor.execute(
                    """INSERT INTO wiki_chunks_fts
                       (chunk_id, rel_path, section_title, context_summary, contextualized_text)
                       VALUES (?, ?, ?, ?, ?)""",
                    (chunk_id, rel_path, sec_title, context_summary, contextualized_text)
                )

        conn.commit()
        conn.close()

    def reindex_all(self):
        """Scans the wiki folder and reindexes all markdown files, clearing deleted ones."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wiki_fts")
        cursor.execute("DELETE FROM wiki_meta")
        cursor.execute("DELETE FROM wiki_links")
        cursor.execute("DELETE FROM wiki_chunks")
        cursor.execute("DELETE FROM wiki_chunks_fts")
        conn.commit()
        conn.close()

        for md_file in self.wiki_dir.rglob("*.md"):
            self.index_file(md_file)

    def contextual_search(self, query: str, limit: int = 15, use_rerank: bool = True) -> List[Dict[str, Any]]:
        """Anthropic Contextual Retrieval:
        1. Contextual BM25 via SQLite FTS5 over chunks with prepended situational context
        2. Contextual Dense Vector Embeddings
        3. Reciprocal Rank Fusion (RRF)
        4. Cross-Scorer Reranking to extract Top-K high-precision chunks
        """
        if not query.strip():
            return []

        clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
        if not clean_q:
            return []

        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()

        # 1. Contextual BM25 Search
        words = clean_q.split()
        fts_query = " AND ".join(f'"{w}"*' for w in words)
        bm25_matches: Dict[str, Dict[str, Any]] = {}

        try:
            cursor.execute("""
                SELECT chunk_id, rel_path, section_title, context_summary,
                       snippet(wiki_chunks_fts, 4, '<mark>', '</mark>', '...', 25) as match_snippet,
                       bm25(wiki_chunks_fts) as bm25_score
                FROM wiki_chunks_fts
                WHERE wiki_chunks_fts MATCH ?
                ORDER BY bm25_score ASC
                LIMIT 50
            """, (fts_query,))
            for rank_idx, row in enumerate(cursor.fetchall(), start=1):
                d = dict(row)
                d["bm25_rank"] = rank_idx
                bm25_matches[d["chunk_id"]] = d
        except Exception:
            try:
                cursor.execute("""
                    SELECT chunk_id, rel_path, section_title, context_summary,
                           substr(contextualized_text, 1, 150) as match_snippet,
                           0 as bm25_score
                    FROM wiki_chunks
                    WHERE contextualized_text LIKE ? OR section_title LIKE ?
                    LIMIT 30
                """, (f"%{clean_q}%", f"%{clean_q}%"))
                for rank_idx, row in enumerate(cursor.fetchall(), start=1):
                    d = dict(row)
                    d["bm25_rank"] = rank_idx
                    bm25_matches[d["chunk_id"]] = d
            except Exception:
                pass

        # 2. Contextual Vector Embedding Search
        cursor.execute("SELECT chunk_id, rel_path, section_title, original_content, context_summary, contextualized_text, embedding_json FROM wiki_chunks")
        all_chunks = [dict(row) for row in cursor.fetchall()]

        if not all_chunks:
            conn.close()
            return self._fallback_doc_search(query, limit)

        q_vec = self.llm.embed_text(query)
        scored_vecs = []
        for c in all_chunks:
            emb_str = c.get("embedding_json")
            if not emb_str:
                continue
            try:
                emb = json.loads(emb_str)
                sim = sum(a * b for a, b in zip(q_vec, emb))
                scored_vecs.append((sim, c))
            except Exception:
                continue

        scored_vecs.sort(key=lambda x: x[0], reverse=True)
        top_vecs: Dict[str, Dict[str, Any]] = {}
        for rank_idx, (sim, c) in enumerate(scored_vecs[:50], start=1):
            c_dict = dict(c)
            c_dict["vector_score"] = round(sim, 4)
            c_dict["vec_rank"] = rank_idx
            top_vecs[c_dict["chunk_id"]] = c_dict

        # 3. Reciprocal Rank Fusion (RRF)
        candidate_ids = set(bm25_matches.keys()) | set(top_vecs.keys())
        chunks_by_id = {c["chunk_id"]: c for c in all_chunks}

        fused_candidates = []
        for cid in candidate_ids:
            chunk_data = chunks_by_id.get(cid)
            if not chunk_data:
                continue
            bm25_info = bm25_matches.get(cid)
            vec_info = top_vecs.get(cid)

            rrf = 0.0
            if bm25_info:
                rrf += 1.0 / (60.0 + bm25_info["bm25_rank"])
            if vec_info:
                rrf += 1.0 / (60.0 + vec_info["vec_rank"])

            merged = dict(chunk_data)
            if bm25_info:
                merged["match_snippet"] = bm25_info.get("match_snippet")
                merged["bm25_rank"] = bm25_info["bm25_rank"]
            if vec_info:
                merged["vector_score"] = vec_info["vector_score"]
                merged["vec_rank"] = vec_info["vec_rank"]
            merged["rrf_score"] = rrf
            fused_candidates.append(merged)

        fused_candidates.sort(key=lambda x: x["rrf_score"], reverse=True)
        top_candidates = fused_candidates[:max(limit * 2, 20)]

        # 4. Cross-Encoder / Relevance Reranking
        if use_rerank and top_candidates:
            doc_texts = [c.get("contextualized_text", "") for c in top_candidates]
            rerank_scores = self.llm.rerank(query, doc_texts)
            for c, r_score in zip(top_candidates, rerank_scores):
                c["rerank_score"] = r_score
                c["final_score"] = (r_score * 0.7) + ((c["rrf_score"] * 30.0) * 0.3)
            top_candidates.sort(key=lambda x: x.get("final_score", 0), reverse=True)
        else:
            for c in top_candidates:
                c["rerank_score"] = c.get("vector_score", 0.0)
                c["final_score"] = c["rrf_score"]

        # Fetch metadata
        cursor.execute("SELECT rel_path, category, title, tags FROM wiki_meta")
        meta_by_path = {row["rel_path"]: dict(row) for row in cursor.fetchall()}
        conn.close()

        results = []
        for c in top_candidates[:limit]:
            meta = meta_by_path.get(c["rel_path"], {})
            snippet = c.get("match_snippet") or c.get("context_summary") or c.get("original_content", "")[:150]
            results.append({
                "chunk_id": c["chunk_id"],
                "rel_path": c["rel_path"],
                "title": meta.get("title", c["section_title"]),
                "category": meta.get("category", "concepts"),
                "tags": meta.get("tags", ""),
                "section_title": c["section_title"],
                "context_summary": c["context_summary"],
                "contextualized_text": c["contextualized_text"],
                "original_content": c["original_content"],
                "match_snippet": snippet,
                "rrf_score": round(c.get("rrf_score", 0.0), 5),
                "rerank_score": round(c.get("rerank_score", 0.0), 4),
                "rank": round(c.get("final_score", 0.0), 4)
            })

        return results

    def _fallback_doc_search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Document-level fallback search using SQLite FTS5."""
        clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
        if not clean_q:
            return []
        words = clean_q.split()
        fts_query = " AND ".join(f'"{w}"*' for w in words)
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT rel_path, category, title, tags,
                       snippet(wiki_fts, 4, '<mark>', '</mark>', '...', 25) as match_snippet,
                       bm25(wiki_fts) as rank
                FROM wiki_fts
                WHERE wiki_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit))
            results = [dict(row) for row in cursor.fetchall()]
        except Exception:
            cursor.execute("""
                SELECT rel_path, category, title, tags,
                       substr(content, 1, 150) as match_snippet,
                       0 as rank
                FROM wiki_fts
                WHERE title LIKE ? OR content LIKE ?
                LIMIT ?
            """, (f"%{clean_q}%", f"%{clean_q}%", limit))
            results = [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
        return results

    def search(self, query: str, limit: int = 15, mode: str = "contextual") -> List[Dict[str, Any]]:
        """Searches the wiki. If mode='contextual' (default), performs Anthropic Contextual Retrieval
        (Contextual BM25 + Vector Embeddings + RRF + Reranker), falling back to document FTS if needed."""
        if mode == "contextual":
            results = self.contextual_search(query, limit=limit, use_rerank=True)
            if results:
                return results

        return self._fallback_doc_search(query, limit=limit)

    def get_graph(self) -> Dict[str, Any]:
        """Returns nodes and links representing the cross-link graph of the wiki."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT rel_path, category, title FROM wiki_meta WHERE rel_path NOT IN ('index.md', 'SCHEMA.md', 'log.md') AND category != 'student_profile'")
        nodes = [{"id": Path(row["rel_path"]).stem, "title": row["title"], "category": row["category"], "path": row["rel_path"]} for row in cursor.fetchall()]
        
        cursor.execute("SELECT source_slug, target_slug, link_text FROM wiki_links WHERE source_slug NOT IN ('index', 'SCHEMA', 'log') AND target_slug NOT IN ('index', 'SCHEMA', 'log')")
        links = [{"source": row["source_slug"], "target": row["target_slug"], "label": row["link_text"]} for row in cursor.fetchall()]
        
        conn.close()
        return {"nodes": nodes, "links": links}
