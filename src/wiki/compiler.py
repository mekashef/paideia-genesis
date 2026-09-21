"""Karpathy-style Knowledge Compiler for the Universal Compounding LLM-Wiki."""
import re
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pypdf
from src.config import WIKI_DIR, RAW_SOURCES_DIR
from src.wiki.schema import init_wiki_structure
from src.wiki.indexer import WikiIndexer
from src.llm.client import get_llm_client, BaseLLMClient

class WikiCompiler:
    def __init__(self, llm_client: Optional[BaseLLMClient] = None, wiki_dir: Path = WIKI_DIR):
        self.wiki_dir = wiki_dir
        self.llm = llm_client or get_llm_client()
        self.indexer = WikiIndexer(wiki_dir)
        init_wiki_structure(self.wiki_dir)

    def extract_text_from_file(self, file_path: Path) -> str:
        """Extracts plain text from PDF or markdown/text files."""
        if file_path.suffix.lower() == ".pdf":
            reader = pypdf.PdfReader(str(file_path))
            text_parts = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                text_parts.append(f"--- Slide / Page {i+1} ---\n{page_text}")
            return "\n\n".join(text_parts)
        else:
            return file_path.read_text(encoding="utf-8", errors="replace")

    def ingest_source(
        self,
        filename: str,
        content: str,
        source_type: str = "lecture",
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Processes a raw source document and compiles it into the compounding LLM-Wiki."""
        # 1. Save raw immutable source
        target_dir = RAW_SOURCES_DIR / "lectures" if source_type == "lecture" else RAW_SOURCES_DIR / "exam_logs"
        target_dir.mkdir(parents=True, exist_ok=True)
        raw_path = target_dir / filename
        raw_path.write_text(content, encoding="utf-8")

        # 2. Prompt LLM to extract and compile structured knowledge
        domain_hint = domain or "auto-detected technical/scientific domain"
        prompt = f"""You are an elite academic curriculum compiler and knowledge graph architect.
Process the following raw course or research material into structured, cross-linked high-yield wiki pages following Karpathy's LLM-Wiki pattern.
Target Domain / Discipline: {domain_hint}

Source filename: {filename}
Source content:
{content[:8000]}

Extract and synthesize:
1. 'concepts': array of objects with keys: slug (kebab-case), title, system (or field/module), domain, tags (list), summary, content (markdown with deep mechanisms, theoretical foundations, architectural patterns, and explicit pitfalls/traps).
2. 'entities': array of key entities (tools, libraries, hardware, algorithms, theorems, equations, drugs, pathogens, components) with keys: slug, title, category, high_yield_notes.
3. 'differentials': array of comparative syntheses with keys: slug, title, summary, content (markdown tables and discriminant features).

Respond strictly with valid JSON conforming to this structure."""

        extraction = self.llm.generate_json(prompt, system_prompt="You are a universal knowledge graph compiler.")

        created_pages = []

        # 3. Write Concept pages
        concepts = extraction.get("concepts", [])
        for c in concepts:
            slug = c.get("slug", "unnamed-concept")
            page_file = self.wiki_dir / "concepts" / f"{slug}.md"
            tags_str = ", ".join(c.get("tags", []))
            page_content = f"""---
title: {c.get('title')}
domain: {c.get('domain', domain or 'General')}
system: {c.get('system', 'General')}
tags: [{tags_str}]
source: {filename}
last_compiled: {datetime.date.today().isoformat()}
---

# {c.get('title')}

> **Core Summary**: {c.get('summary', '')}

{c.get('content', '')}

---
*Compiled from raw source: `{filename}`*
"""
            page_file.write_text(page_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created_pages.append({"slug": slug, "title": c.get("title"), "category": "concepts"})

        # 4. Write Entity pages
        entities = extraction.get("entities", [])
        for e in entities:
            slug = e.get("slug", "unnamed-entity")
            page_file = self.wiki_dir / "entities" / f"{slug}.md"
            page_content = f"""---
title: {e.get('title')}
category: {e.get('category')}
domain: {domain or 'General'}
source: {filename}
last_compiled: {datetime.date.today().isoformat()}
---

# {e.get('title')} ({e.get('category')})

### Key Technical Notes & Insights
{e.get('high_yield_notes', '')}

---
*Compiled from raw source: `{filename}`*
"""
            page_file.write_text(page_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created_pages.append({"slug": slug, "title": e.get("title"), "category": "entities"})

        # 5. Write Differential pages
        differentials = extraction.get("differentials", [])
        for d in differentials:
            slug = d.get("slug", "unnamed-diff")
            page_file = self.wiki_dir / "differentials" / f"{slug}.md"
            page_content = f"""---
title: {d.get('title')}
domain: {domain or 'General'}
source: {filename}
last_compiled: {datetime.date.today().isoformat()}
---

# {d.get('title')}

{d.get('content', '')}

---
*Compiled from raw source: `{filename}`*
"""
            page_file.write_text(page_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created_pages.append({"slug": slug, "title": d.get("title"), "category": "differentials"})

        # 6. Update master index.md
        self._update_index()

        # 7. Append to log.md
        today = datetime.date.today().isoformat()
        log_entry = f"## [{today}] ingest | `{filename}` compiled into {len(created_pages)} wiki pages ({', '.join(p['slug'] for p in created_pages[:3])})\n"
        log_file = self.wiki_dir / "log.md"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{log_entry}")

        return {
            "source": filename,
            "pages_created": len(created_pages),
            "pages": created_pages
        }

    def _update_index(self):
        """Regenerates the catalog index.md with all current wiki pages."""
        sections = {
            "course_sessions": [],
            "concepts": [],
            "entities": [],
            "differentials": [],
            "exam_traps": []
        }

        for cat in sections.keys():
            folder = self.wiki_dir / cat
            if folder.exists():
                for md in sorted(folder.glob("*.md")):
                    title = md.stem.replace("-", " ").title()
                    lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
                    for line in lines:
                        if line.startswith("title:"):
                            title = line.split(":", 1)[1].strip().strip('"\'')
                            break
                        elif line.startswith("# "):
                            title = line[2:].strip()
                            break
                    rel_link = f"{cat}/{md.name}"
                    sections[cat].append(f"- [[{rel_link}|{title}]]")

        index_text = f"""# Universal Knowledge Master Index

*Last recompiled: {datetime.date.today().isoformat()}*

## Course & Reading Sessions
{chr(10).join(sections['course_sessions']) if sections['course_sessions'] else '- *No course sessions registered.*'}

## Core Concepts & Mechanisms
{chr(10).join(sections['concepts']) if sections['concepts'] else '- *No concepts compiled yet.*'}

## Entities, Components & Algorithms
{chr(10).join(sections['entities']) if sections['entities'] else '- *No entities registered yet.*'}

## Comparative Differentials & Trade-offs
{chr(10).join(sections['differentials']) if sections['differentials'] else '- *No comparative syntheses yet.*'}

## Traps, Anti-Patterns & Misconceptions
{chr(10).join(sections['exam_traps']) if sections['exam_traps'] else '- *No traps recorded yet.*'}
"""
        (self.wiki_dir / "index.md").write_text(index_text, encoding="utf-8")
        self.indexer.index_file(self.wiki_dir / "index.md")

    def lint_wiki(self) -> Dict[str, Any]:
        """Health-checks the wiki for orphan pages, missing cross-references, or broken links."""
        all_pages = set()
        outbound_links = {}
        inbound_links = {}

        for md in self.wiki_dir.rglob("*.md"):
            slug = md.stem
            all_pages.add(slug)
            content = md.read_text(encoding="utf-8", errors="replace")
            links = re.findall(r"\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]", content)
            outbound_links[slug] = [Path(l).stem for l in links]

        for source, targets in outbound_links.items():
            for target in targets:
                inbound_links.setdefault(target, []).append(source)

        orphans = [p for p in all_pages if p not in inbound_links and p not in ["index", "log", "SCHEMA"]]
        broken = []
        for source, targets in outbound_links.items():
            for target in targets:
                if target not in all_pages and target not in ["index", "log"]:
                    broken.append({"source": source, "broken_target": target})

        return {
            "total_pages": len(all_pages),
            "orphan_pages": orphans,
            "broken_links": broken,
            "status": "healthy" if not broken else "needs_attention"
        }
