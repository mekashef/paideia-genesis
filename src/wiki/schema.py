"""LLM-Wiki schema definition and directory structure manager for universal multi-discipline knowledge.
Adapted from Andrej Karpathy's LLM-Wiki specification.
Supports engineering, computer science, research, undergraduate studies, school curricula, and medicine.
"""
from pathlib import Path
from typing import Optional
from src.config import RAW_SOURCES_DIR, WIKI_DIR, ANKI_EXPORT_DIR

SCHEMA_CONTENT = """# Universal LLM-Wiki Schema

This wiki is an evolving, compounding knowledge base designed to accompany a learner, engineer, or researcher through their coursework, technical mastery, and research milestones.

## Layer Hierarchy
1. **Raw Sources (`raw_sources/`)**: Immutable original documents (lecture slides, syllabi, papers, problem sets, textbook chapters). The LLM reads from here but never alters original files.
2. **The Compounding Wiki (`wiki/`)**: Curated markdown files maintained collaboratively by the learner and the LLM:
   - `index.md`: Category-organized master index of all concepts, entities, comparative differentials, and lecture sessions.
   - `log.md`: Chronological journal of all ingests, study drills, error diagnostics, and updates.
   - `course_sessions/`: Lectures, modules, chapters, reading seminars, research milestones.
   - `concepts/`: Deep mechanisms, theoretical foundations, architectural patterns, laws, and algorithms.
   - `entities/`: Tools, libraries, hardware, algorithms, theorems, equations, protocols, drugs, and components.
   - `differentials/`: Side-by-side comparative analyses, benchmark contrasts, trade-off studies, and decision trees.
   - `exam_traps/`: Anti-patterns, common misconceptions, edge cases, fallacies, and classic exam/interview traps.
   - `student_profile/`: Learner diagnostic profile (mastery scores, misconceptions, upcoming deadlines).

## Cross-Linking Conventions
- Use standard wikilink syntax: `[[concept-slug]]` or `[[concept-slug|Display Text]]`.
- Relative paths are supported: `[[concepts/raft-distributed-consensus|Raft Consensus]]`.
- Every page begins with YAML frontmatter:
  ```yaml
  ---
  title: Raft Distributed Consensus
  domain: Computer Science
  field: Distributed Systems
  course: MIT 6.033
  tags: [consensus, fault-tolerance, distributed-systems]
  last_updated: 2026-09-21
  ---
  ```
- Concept pages include a "Common Traps, Anti-Patterns & Misconceptions" section.
"""

INDEX_INITIAL_TEMPLATE = """# Universal Knowledge Master Index

Welcome to your living Compounding Wiki. As lectures, papers, and drill results are ingested, this index dynamically updates.

## Core Concepts & Mechanisms
- *No concepts compiled yet.*

## Key Entities, Algorithms & Components
- *No entities registered yet.*

## Comparative Differentials & Trade-offs
- *No comparative syntheses yet.*

## Common Traps, Anti-Patterns & Misconceptions
- *No traps recorded yet.*
"""

LOG_INITIAL_TEMPLATE = """# Universal Learning Log

Append-only chronological record of all knowledge acquisitions, quiz drills, and wiki lint passes.

## [2026-09-21] system_init | Universal LLM-Wiki initialized with Karpathy schema
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
