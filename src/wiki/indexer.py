"""SQLite FTS5 full-text search and wikilink graph indexer for the Medical Wiki."""
import re
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.config import DB_PATH, WIKI_DIR

WIKILINK_PATTERN = re.compile(r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def get_db_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_indexer_db(db_path: Path = DB_PATH):
    """Initializes the SQLite database with FTS5 virtual table and links table."""
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # FTS5 full-text table
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

    conn.commit()
    conn.close()

def parse_markdown_file(file_path: Path) -> Dict[str, Any]:
    """Extracts frontmatter metadata, title, and body from a markdown file."""
    content = file_path.read_text(encoding="utf-8", errors="replace")
    title = file_path.stem.replace("-", " ").title()
    tags = ""
    system = ""
    source = ""
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
        "frontmatter": frontmatter,
        "body": body,
        "raw": content,
        "links": links
    }

class WikiIndexer:
    def __init__(self, wiki_dir: Path = WIKI_DIR, db_path: Optional[Path] = None):
        self.wiki_dir = wiki_dir
        if db_path:
            self.db_path = db_path
        elif self.wiki_dir != WIKI_DIR:
            self.db_path = self.wiki_dir / "index.db"
        else:
            self.db_path = DB_PATH
        init_indexer_db(self.db_path)

    def index_file(self, file_path: Path):
        """Indexes a single markdown file."""
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

        conn.commit()
        conn.close()

    def reindex_all(self):
        """Scans the wiki folder and reindexes all markdown files, clearing deleted ones."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wiki_fts")
        cursor.execute("DELETE FROM wiki_meta")
        cursor.execute("DELETE FROM wiki_links")
        conn.commit()
        conn.close()

        for md_file in self.wiki_dir.rglob("*.md"):
            self.index_file(md_file)

    def search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """Performs full-text search against the medical wiki using SQLite FTS5."""
        if not query.strip():
            return []
            
        # Clean query for FTS5 (escape special chars)
        clean_q = re.sub(r'[^\w\s]', ' ', query).strip()
        if not clean_q:
            return []
            
        # Format query words with wildcards for prefix matching
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
            # Fallback simple LIKE query if FTS syntax error
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
