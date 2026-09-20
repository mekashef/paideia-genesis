"""LLM-Wiki schema definition and directory structure manager for medical domain.
Adapted from Andrej Karpathy's LLM-Wiki specification.
"""
from pathlib import Path
from typing import Optional
from src.config import RAW_SOURCES_DIR, WIKI_DIR, ANKI_EXPORT_DIR

SCHEMA_CONTENT = """# Medical LLM-Wiki Schema

This wiki is an evolving, compounding knowledge base designed to accompany a medical student through their preclinical, clinical, and board examination years.

## Layer Hierarchy
1. **Raw Sources (`raw_sources/`)**: Immutable original documents (lecture slides, syllabi, question bank logs). The LLM reads from here but never alters original files.
2. **The Medical Wiki (`wiki/`)**: Curated markdown files maintained by the LLM:
   - `index.md`: Category-organized master index of all concepts, drugs, diseases, and syntheses.
   - `log.md`: Chronological journal of all ingests, study drills, error diagnostics, and updates.
   - `concepts/`: Deep physiological mechanisms, biochemical pathways, and pathophysiologies.
   - `entities/`: High-yield drugs, microbes, anatomic structures, and diagnostic tests.
   - `differentials/`: Side-by-side comparative analyses and clinical decision algorithms.
   - `exam_traps/`: High-yield board traps, common student misunderstandings, and look-alike pitfalls.
   - `student_profile/`: Student diagnostic model (mastery scores, misconceptions, upcoming deadlines).

## Cross-Linking Conventions
- Use standard wikilink syntax: `[[concept-slug]]` or `[[concept-slug|Display Text]]`.
- Every page begins with YAML frontmatter:
  ```yaml
  ---
  title: Acute Decompensated Heart Failure
  system: Cardiovascular
  high_yield_rating: 5/5
  tags: [cardiology, pharmacology, board-trap]
  last_updated: 2026-09-18
  ---
  ```
- Every concept page includes a "Board Exam Traps & Common Errors" section.
"""

INDEX_INITIAL_TEMPLATE = """# Medical Master Index

Welcome to your living Medical Wiki. As lectures and exam results are ingested, this index dynamically updates.

## High-Yield Concepts
- *No concepts compiled yet.*

## Pharmacologic Agents & Entities
- *No entities registered yet.*

## Differentials & Syntheses
- *No comparative syntheses yet.*

## Board Traps & Misconceptions
- *No traps recorded yet.*
"""

LOG_INITIAL_TEMPLATE = """# Medical Learning Log

Append-only chronological record of all knowledge acquisitions, quiz drills, and wiki lint passes.

## [2026-09-18] system_init | Medical LLM-Wiki initialized with Karpathy schema
"""

def init_wiki_structure(
    wiki_dir: Optional[Path] = None,
    raw_sources_dir: Optional[Path] = None,
    anki_export_dir: Optional[Path] = None
):
    """Create all required directories and base index/log files if not present."""
    target_wiki_dir = wiki_dir or WIKI_DIR
    target_raw_dir = raw_sources_dir or RAW_SOURCES_DIR
    target_anki_dir = anki_export_dir or ANKI_EXPORT_DIR

    target_raw_dir.mkdir(parents=True, exist_ok=True)
    (target_raw_dir / "lectures").mkdir(parents=True, exist_ok=True)
    (target_raw_dir / "syllabus").mkdir(parents=True, exist_ok=True)
    (target_raw_dir / "exam_logs").mkdir(parents=True, exist_ok=True)

    target_wiki_dir.mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "course_sessions").mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "concepts").mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "entities").mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "differentials").mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "exam_traps").mkdir(parents=True, exist_ok=True)
    (target_wiki_dir / "student_profile").mkdir(parents=True, exist_ok=True)
    target_anki_dir.mkdir(parents=True, exist_ok=True)

    schema_file = target_wiki_dir / "SCHEMA.md"
    if not schema_file.exists():
        schema_file.write_text(SCHEMA_CONTENT, encoding="utf-8")

    index_file = target_wiki_dir / "index.md"
    if not index_file.exists():
        index_file.write_text(INDEX_INITIAL_TEMPLATE, encoding="utf-8")

    log_file = target_wiki_dir / "log.md"
    if not log_file.exists():
        log_file.write_text(LOG_INITIAL_TEMPLATE, encoding="utf-8")
