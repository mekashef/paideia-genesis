"""Course and Syllabus Importer Subsystem for Paideia Genesis.
Supports importing MIT OpenCourseWare courses, course syllabi, and lecture outlines into the Living Universal Wiki.
Covers Engineering, Computer Science, Research, Sciences, and Medicine.
"""
import re
import json
import datetime
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.config import WIKI_DIR, RAW_SOURCES_DIR
from src.wiki.indexer import WikiIndexer
from src.wiki.compiler import WikiCompiler
from src.wiki.schema import init_wiki_structure
from src.anki.generator import AnkiManager
from src.tutor.student_profile import StudentProfile
from src.llm.client import get_llm_client, BaseLLMClient
from src.wiki.hst121_curriculum import (
    HST121_CONCEPTS,
    HST121_DIFFERENTIALS,
    HST121_TRAPS,
    HST121_FLASHCARDS,
    HST121_CURRICULUM_TOPICS
)
from src.wiki.hst121_full_sessions_and_entities import (
    HST121_SESSIONS_WIKI,
    HST121_ENTITIES_WIKI
)
from src.wiki.eecs_curriculum import (
    EECS_SESSIONS,
    EECS_CONCEPTS,
    EECS_ENTITIES,
    EECS_DIFFERENTIALS,
    EECS_TRAPS,
    EECS_FLASHCARDS,
    EECS_CURRICULUM_TOPICS
)
from src.wiki.vision_curriculum import (
    VISION_CURRICULUM_TOPICS,
    VISION_SESSIONS,
    VISION_CONCEPTS,
    VISION_ENTITIES,
    VISION_DIFFERENTIALS,
    VISION_TRAPS,
    VISION_FLASHCARDS
)

DEFAULT_MIT_OCW_HST121_SESSIONS = [
    {"session": 1, "topic": "Overview of Embryology & Physiology", "instructors": "Dr. Jonathan N. Glickman"},
    {"session": 2, "topic": "Gastroduodenal Pathophysiology and Disorders; Pathology of Esophagus and Stomach", "instructors": "Dr. Helen Shields, Dr. Jonathan N. Glickman"},
    {"session": 3, "topic": "Mucosal Immunology of the GI Tract", "instructors": "Dr. Richard S. Blumberg"},
    {"session": 4, "topic": "Lipid Digestion, Absorption and Malabsorption", "instructors": "Dr. Martin C. Carey"},
    {"session": 5, "topic": "Minicases: Esophagus and Gastric Disorders", "instructors": "Faculty"},
    {"session": 6, "topic": "Intestinal Pathophysiology and Diarrheal Illness", "instructors": "Dr. Wayne I. Lencer"},
    {"session": 7, "topic": "Pathology of the Intestines (IBD, Ischemia, Polyps)", "instructors": "Drs. Carolyn C. Compton and Jonathan N. Glickman"},
    {"session": 8, "topic": "Clinic: Inflammatory Bowel Disease; Minicases: Malabsorption", "instructors": "Faculty"},
    {"session": 9, "topic": "Gastrointestinal Neoplasms (Adenoma-Carcinoma, HNPCC, FAP)", "instructors": "Dr. Jonathan N. Glickman"},
    {"session": 10, "topic": "Physiological Chemistry of GI Lipids", "instructors": "Dr. Martin C. Carey"},
    {"session": 11, "topic": "Physiology and Biochemistry of Pancreas; Acute & Chronic Pancreatitis", "instructors": "Faculty"},
    {"session": 12, "topic": "Pathology of Pancreas and Biliary Tract", "instructors": "Dr. Jonathan N. Glickman"},
    {"session": 13, "topic": "Biliary Secretion, Cholestasis and Gallstone Formation", "instructors": "Dr. Martin C. Carey"},
    {"session": 14, "topic": "Imaging of the GI Tract; Diagnostic & Therapeutic Endoscopy", "instructors": "Faculty"},
    {"session": 15, "topic": "Pathology of the Liver (Hepatitis, Steatohepatitis)", "instructors": "Dr. Jonathan N. Glickman"},
    {"session": 16, "topic": "Immunology of the Liver", "instructors": "Dr. Jack Wands"},
    {"session": 17, "topic": "Jaundice and Disorders of Bilirubin Metabolism; Drug-Induced Liver Disease", "instructors": "Dr. Raymond T. Chung"},
    {"session": 18, "topic": "Physiology and Biochemistry of the Liver", "instructors": "Faculty"},
    {"session": 19, "topic": "Clinic: Chronic Liver Disease and Liver Transplantation", "instructors": "Faculty"},
    {"session": 20, "topic": "Pathophysiological Consequences of Cirrhosis and Portal Hypertension", "instructors": "Faculty"}
]

class CourseImporter:
    def __init__(self, llm_client: Optional[BaseLLMClient] = None, wiki_dir: Path = WIKI_DIR):
        self.wiki_dir = wiki_dir
        self.llm = llm_client or get_llm_client()
        self.indexer = WikiIndexer(wiki_dir)
        self.anki_manager = AnkiManager(wiki_dir=wiki_dir)
        self.student_profile = StudentProfile(wiki_dir / "student_profile")
        init_wiki_structure(self.wiki_dir)

    def fetch_course_metadata(self, url: str) -> Dict[str, Any]:
        """Fetches and parses course structure from an external URL like MIT OCW."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "PaideiaGenesisCourseImporter/0.3"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode("utf-8", errors="replace")

            # Extract course title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            title = title_match.group(1).split('|')[0].strip() if title_match else "Course Curriculum"

            # Check if this is an engineering course
            is_eecs = "6.033" in url or "computer" in title.lower() or "systems" in title.lower() or "distributed" in title.lower()

            # Extract table rows
            rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
            sessions = []
            for r in rows:
                clean = re.sub(r'<[^>]+>', ' ', r)
                clean = re.sub(r'\s+', ' ', clean).strip()
                match = re.match(r'^(\d+)\s+(.*?)(?:Dr\.|Prof\.|Faculty|$)', clean)
                if match:
                    ses_num = int(match.group(1))
                    topic_text = match.group(2).strip()
                    sessions.append({
                        "session": ses_num,
                        "topic": topic_text,
                        "instructors": "MIT Faculty"
                    })

            if not sessions:
                sessions = EECS_SESSIONS if is_eecs else DEFAULT_MIT_OCW_HST121_SESSIONS

            course_code = "MIT 6.033" if is_eecs else "HST.121"
            institution = "Massachusetts Institute of Technology (MIT OpenCourseWare)"

            return {
                "url": url,
                "course_code": course_code,
                "title": title or ("MIT 6.033: Computer System Design" if is_eecs else "HST.121: Gastroenterology"),
                "institution": institution,
                "domain": "Computer Science" if is_eecs else "Medicine",
                "sessions": sessions
            }
        except Exception:
            # Fallback based on URL hint
            if "6.033" in url or "computer" in url.lower():
                return {
                    "url": url,
                    "course_code": "MIT 6.033",
                    "title": "MIT 6.033: Computer System Design & Distributed Systems",
                    "institution": "MIT Department of EECS (MIT OpenCourseWare)",
                    "domain": "Computer Science",
                    "sessions": [{"session": s["session_num"], "topic": s["title"], "instructors": s["instructors"]} for s in EECS_SESSIONS]
                }
            return {
                "url": url,
                "course_code": "HST.121",
                "title": "HST.121: Gastroenterology",
                "institution": "Harvard-MIT Division of Health Sciences and Technology (MIT OpenCourseWare)",
                "domain": "Medicine",
                "sessions": DEFAULT_MIT_OCW_HST121_SESSIONS
            }

    def import_hst121_course(self, url: Optional[str] = None) -> Dict[str, Any]:
        """Full automated ingestion and compilation of MIT HST.121 Gastroenterology."""
        course_url = url or "https://ocw.mit.edu/courses/hst-121-gastroenterology-fall-2005/pages/lecture-notes/"
        meta = self.fetch_course_metadata(course_url)

        # 1. Save immutable raw course manifest
        raw_manifest_path = RAW_SOURCES_DIR / "syllabus" / "MIT_HST121_Gastroenterology_Curriculum.json"
        raw_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        raw_manifest_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        # 2. Compile lecture session pages (20 sessions)
        compiled_sessions = self._compile_gi_sessions()

        # 3. Compile high-yield concept pages
        compiled_concepts = self._compile_gi_concepts()

        # 4. Compile medical entities (drugs, enzymes, microbes, biomarkers)
        compiled_entities = self._compile_gi_entities()

        # 5. Compile comparative differentials
        compiled_diffs = self._compile_gi_differentials()

        # 6. Compile high-yield GI board exam traps
        compiled_traps = self._compile_gi_traps()

        # 7. Update index.md
        self._refresh_master_index()

        # 8. Append to log.md
        today = datetime.date.today().isoformat()
        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(
                f"\n## [{today}] course_import | Imported `{meta['course_code']}: {meta['title']}` "
                f"({len(compiled_sessions)} lectures, {len(compiled_concepts)} concepts, {len(compiled_entities)} entities, {len(compiled_diffs)} differentials)\n"
            )

        # 9. Update Student Profile & Curriculum
        self._update_curriculum_for_gi(meta)

        # 10. Stage high-yield GI flashcards into Anki
        self._stage_gi_flashcards()

        return {
            "success": True,
            "course": meta["title"],
            "sessions_imported": len(meta["sessions"]),
            "session_pages_compiled": len(compiled_sessions),
            "concepts_compiled": len(compiled_concepts),
            "entities_compiled": len(compiled_entities),
            "differentials_compiled": len(compiled_diffs),
            "traps_compiled": len(compiled_traps),
            "anki_cards_staged": len(HST121_FLASHCARDS)
        }

    # Alias for curriculum bootstrap
    import_mit_ocw_course = import_hst121_course

    def import_engineering_course(self, url: Optional[str] = None) -> Dict[str, Any]:
        """Full automated ingestion and compilation of MIT 6.033 Distributed Systems & Networking."""
        course_url = url or "https://ocw.mit.edu/courses/6-033-computer-system-design-spring-2009/"
        meta = {
            "url": course_url,
            "course_code": "MIT 6.033",
            "title": "MIT 6.033: Computer System Design & Distributed Systems",
            "institution": "Massachusetts Institute of Technology (EECS)",
            "domain": "Computer Science",
            "sessions": [{"session": s["session_num"], "topic": s["title"], "instructors": s["instructors"]} for s in EECS_SESSIONS]
        }

        raw_manifest_path = RAW_SOURCES_DIR / "syllabus" / "MIT_6_033_Distributed_Systems_Curriculum.json"
        raw_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        raw_manifest_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        compiled_sessions = self._compile_eecs_sessions()
        compiled_concepts = self._compile_eecs_concepts()
        compiled_entities = self._compile_eecs_entities()
        compiled_diffs = self._compile_eecs_differentials()
        compiled_traps = self._compile_eecs_traps()

        self._refresh_master_index()

        today = datetime.date.today().isoformat()
        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(
                f"\n## [{today}] course_import | Imported `{meta['course_code']}: {meta['title']}` "
                f"({len(compiled_sessions)} lectures, {len(compiled_concepts)} concepts, {len(compiled_entities)} entities, {len(compiled_diffs)} differentials)\n"
            )

        self._update_curriculum_for_eecs(meta)
        self._stage_eecs_flashcards()

        return {
            "success": True,
            "course": meta["title"],
            "domain": meta.get("domain", "Computer Science"),
            "sessions_imported": len(meta["sessions"]),
            "session_pages_compiled": len(compiled_sessions),
            "concepts_compiled": len(compiled_concepts),
            "entities_compiled": len(compiled_entities),
            "differentials_compiled": len(compiled_diffs),
            "traps_compiled": len(compiled_traps),
            "anki_cards_staged": len(EECS_FLASHCARDS)
        }

    def import_curriculum_manifest(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Generic importer for arbitrary course syllabi, research roadmaps, or subject manifests."""
        title = manifest.get("title", "Custom Curriculum")
        code = manifest.get("course_code", "CUSTOM")
        domain = manifest.get("domain", "General")
        today = datetime.date.today().isoformat()

        # 1. Save raw source manifest
        slug_code = re.sub(r'[^\w\-]', '_', code.lower()).strip('_')
        raw_manifest_path = RAW_SOURCES_DIR / "syllabus" / f"{slug_code}_Curriculum.json"
        raw_manifest_path.parent.mkdir(parents=True, exist_ok=True)
        raw_manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        # 2. Compile sessions
        compiled_sessions = []
        sessions_dir = self.wiki_dir / "course_sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        for s in manifest.get("sessions", []):
            s_num = s.get("session", len(compiled_sessions) + 1)
            topic = s.get("topic", f"Session {s_num}")
            slug = s.get("slug") or re.sub(r'[^\w\-]', '-', f"session-{s_num:02d}-{topic}".lower()).strip('-')[:50]
            instructors = s.get("instructors", "Faculty / Lead Researcher")
            summary = s.get("summary", f"Core lecture and reading module for {topic}.")
            body = s.get("content", f"### Objectives\n- Understand {topic} in {domain}.\n\n### Key Principles\nFoundational principles and applications.")

            page_file = sessions_dir / f"{slug}.md"
            page_content = f"""---
title: {topic}
session: {s_num}
instructors: {instructors}
domain: {domain}
course: {code}
source: {title}
last_compiled: {today}
---

# {topic}

**Instructors / Sources**: {instructors}  
**Curriculum**: {title} ({code})

> **Module Summary**: {summary}

{body}

---
*Curriculum module compiled into Paideia Genesis*
"""
            page_file.write_text(page_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            compiled_sessions.append(slug)

        # 3. Compile custom concepts if present
        compiled_concepts = []
        concepts_dir = self.wiki_dir / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        for c in manifest.get("concepts", []):
            slug = c.get("slug") or re.sub(r'[^\w\-]', '-', c.get("title", "concept").lower()).strip('-')
            page_file = concepts_dir / f"{slug}.md"
            tags_str = ", ".join(c.get("tags", [domain, code]))
            page_content = f"""---
title: {c.get('title')}
domain: {domain}
system: {c.get('field', domain)}
course: {code}
tags: [{tags_str}]
source: {title}
last_compiled: {today}
---

# {c.get('title')}

> **Core Summary**: {c.get('summary', '')}

{c.get('content', '')}

---
*Compiled from: `{title}`*
"""
            page_file.write_text(page_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            compiled_concepts.append(slug)

        # 4. Refresh index & log
        self._refresh_master_index()
        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(
                f"\n## [{today}] custom_import | Imported `{code}: {title}` "
                f"({len(compiled_sessions)} sessions, {len(compiled_concepts)} concepts)\n"
            )

        # 5. Update learner schedule
        topics_list = manifest.get("topics") or [{"name": s.get("topic", f"Session {i+1}"), "priority": "HIGH"} for i, s in enumerate(manifest.get("sessions", []))]
        schedule = {
            "current_block": f"{code}: {title}",
            "target_exam": manifest.get("target_exam", f"{code} Mastery Milestone"),
            "exam_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            "topics": topics_list
        }
        self.student_profile.update_schedule(schedule)

        return {
            "success": True,
            "course": title,
            "sessions_imported": len(manifest.get("sessions", [])),
            "session_pages_compiled": len(compiled_sessions),
            "concepts_compiled": len(compiled_concepts)
        }

    # -------------------------------------------------------------------------
    # Engineering Curriculum Helpers
    # -------------------------------------------------------------------------

    def _compile_eecs_sessions(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        sessions_dir = self.wiki_dir / "course_sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        for s in EECS_SESSIONS:
            page_file = sessions_dir / f"{s['slug']}.md"
            content = f"""---
title: {s['title']}
session: {s['session_num']}
instructors: {s['instructors']}
domain: Computer Science
field: Distributed Systems
course: MIT 6.033
source: MIT 6.033 Computer System Design
last_compiled: {today}
---

# {s['title']}

**Instructors**: {s['instructors']}  
**Curriculum**: MIT Department of Electrical Engineering & Computer Science (6.033)

> **Lecture Summary**: {s['summary']}

{s['content']}

---
*Official lecture notes synthesis from MIT OpenCourseWare 6.033*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(s["slug"])
        return created

    def _compile_eecs_concepts(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        concepts_dir = self.wiki_dir / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        for c in EECS_CONCEPTS:
            page_file = concepts_dir / f"{c['slug']}.md"
            tags_str = ", ".join(c["tags"])
            content = f"""---
title: {c['title']}
domain: {c['domain']}
system: {c['field']}
course: {c['course']}
tags: [{tags_str}]
source: MIT 6.033 Distributed Systems
last_compiled: {today}
---

# {c['title']}

> **Core Summary**: {c['summary']}

{c['content']}

---
*Compiled from MIT 6.033 Computer System Design Lecture Notes*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(c["slug"])
        return created

    def _compile_eecs_entities(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        entities_dir = self.wiki_dir / "entities"
        entities_dir.mkdir(parents=True, exist_ok=True)
        for e in EECS_ENTITIES:
            page_file = entities_dir / f"{e['slug']}.md"
            content = f"""---
title: {e['title']}
domain: {e['domain']}
category: {e['category']}
course: {e['course']}
source: MIT 6.033 Distributed Systems
last_compiled: {today}
---

# {e['title']}

> **Quick Summary**: {e['summary']}

{e['content']}

---
*Entity compiled from MIT 6.033 Technical Knowledge Base*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(e["slug"])
        return created

    def _compile_eecs_differentials(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        diff_dir = self.wiki_dir / "differentials"
        diff_dir.mkdir(parents=True, exist_ok=True)
        for d in EECS_DIFFERENTIALS:
            page_file = diff_dir / f"{d['slug']}.md"
            content = f"""---
title: {d['title']}
domain: Computer Science
field: Distributed Systems
course: MIT 6.033
source: MIT 6.033 Comparative Syntheses
last_compiled: {today}
---

{d['content']}

---
*Compiled from MIT 6.033 Comparative Architectural Syntheses*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(d["slug"])
        return created

    def _compile_eecs_traps(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        traps_dir = self.wiki_dir / "exam_traps"
        traps_dir.mkdir(parents=True, exist_ok=True)
        for t in EECS_TRAPS:
            trap_file = traps_dir / f"{t['slug']}.md"
            tags_str = ", ".join(t["tags"])
            content = f"""---
title: {t['title']}
domain: {t.get('domain', 'Computer Science')}
tags: [{tags_str}]
course: MIT 6.033
last_compiled: {today}
---

{t['content']}

---
*Compiled from MIT 6.033 System Design Traps & Anti-Patterns*
"""
            trap_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(trap_file)
            created.append(t["slug"])
        return created

    def _update_curriculum_for_eecs(self, meta: Dict[str, Any]):
        mastery = self.student_profile.get_mastery()
        if "Distributed Systems" not in mastery:
            mastery["Distributed Systems"] = 55.0
        if "Storage Engines" not in mastery:
            mastery["Storage Engines"] = 50.0
        if "Computer Architecture" not in mastery:
            mastery["Computer Architecture"] = 60.0
        if "Systems Programming" not in mastery:
            mastery["Systems Programming"] = 58.0

        self.student_profile.knowledge_file.write_text(json.dumps(mastery, indent=2), encoding="utf-8")

        schedule = {
            "current_block": "MIT 6.033 Computer System Design & Distributed Systems",
            "target_exam": "MIT 6.033 Final Design Exam & Technical Milestone",
            "exam_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            "topics": EECS_CURRICULUM_TOPICS
        }
        self.student_profile.update_schedule(schedule)

    def _stage_eecs_flashcards(self):
        for card in EECS_FLASHCARDS:
            self.anki_manager.add_card(card)

    # -------------------------------------------------------------------------
    # Medical Curriculum Helpers (Preserved for 100% Backward Compatibility)
    # -------------------------------------------------------------------------

    def _compile_gi_sessions(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        sessions_dir = self.wiki_dir / "course_sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        for s in HST121_SESSIONS_WIKI:
            page_file = sessions_dir / f"{s['slug']}.md"
            content = f"""---
title: {s['title']}
session: {s['session_num']}
instructors: {s['instructors']}
source: MIT HST.121 Gastroenterology
course: HST.121
domain: Medicine
system: Gastroenterology
last_compiled: {today}
---

# {s['title']}

**Instructors**: {s['instructors']}  
**Curriculum**: Harvard-MIT Division of Health Sciences and Technology (HST.121)

> **Lecture Summary**: {s['summary']}

{s['content']}

---
*Official lecture notes synthesis from MIT OpenCourseWare HST.121*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(s["slug"])
        return created

    def _compile_gi_entities(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        entities_dir = self.wiki_dir / "entities"
        entities_dir.mkdir(parents=True, exist_ok=True)
        for e in HST121_ENTITIES_WIKI:
            page_file = entities_dir / f"{e['slug']}.md"
            content = f"""---
title: {e['title']}
category: {e['category']}
source: MIT HST.121 Gastroenterology
course: HST.121
domain: Medicine
last_compiled: {today}
---

# {e['title']}

> **Quick Pearl**: {e['summary']}

{e['content']}

---
*Entity compiled from MIT HST.121 Gastroenterology Knowledge Base*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(e["slug"])
        return created

    def _compile_gi_concepts(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        for c in HST121_CONCEPTS:
            page_file = self.wiki_dir / "concepts" / f"{c['slug']}.md"
            tags_str = ", ".join(c["tags"])
            content = f"""---
title: {c['title']}
system: {c['system']}
domain: Medicine
course: HST.121
tags: [{tags_str}]
source: MIT HST.121 Gastroenterology
last_compiled: {today}
---

# {c['title']}

> **High-Yield Summary**: {c['summary']}

{c['content']}

---
*Compiled from MIT HST.121 Gastroenterology Lecture Notes*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(c["slug"])

        return created

    def _compile_gi_differentials(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        for d in HST121_DIFFERENTIALS:
            page_file = self.wiki_dir / "differentials" / f"{d['slug']}.md"
            content = f"""---
title: {d['title']}
source: MIT HST.121 Gastroenterology
course: HST.121
domain: Medicine
last_compiled: {today}
---

{d['content']}

---
*Compiled from MIT HST.121 Comparative Syntheses*
"""
            page_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(page_file)
            created.append(d["slug"])

        return created

    def _compile_gi_traps(self) -> List[str]:
        created = []
        today = datetime.date.today().isoformat()
        for t in HST121_TRAPS:
            trap_file = self.wiki_dir / "exam_traps" / f"{t['slug']}.md"
            content = f"""---
title: {t['title']}
tags: [board-trap, gastroenterology, USMLE, HST.121]
course: HST.121
domain: Medicine
last_compiled: {today}
---

{t['content']}

---
*Compiled from MIT HST.121 Board Examination Traps*
"""
            trap_file.write_text(content, encoding="utf-8")
            self.indexer.index_file(trap_file)
            created.append(t["slug"])
        return created

    def _refresh_master_index(self):
        compiler = WikiCompiler(self.llm, self.wiki_dir)
        compiler._update_index()

    def _update_curriculum_for_gi(self, meta: Dict[str, Any]):
        mastery = self.student_profile.get_mastery()
        if "Gastroenterology" not in mastery:
            mastery["Gastroenterology"] = 52.0
        if "Hepatology" not in mastery:
            mastery["Hepatology"] = 48.0

        self.student_profile.knowledge_file.write_text(json.dumps(mastery, indent=2), encoding="utf-8")

        schedule = {
            "current_block": "HST.121 Gastroenterology (Harvard-MIT Health Sciences & Technology)",
            "target_exam": "HST.121 Final Examination & USMLE GI Block",
            "exam_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            "topics": HST121_CURRICULUM_TOPICS
        }
        self.student_profile.update_schedule(schedule)

    def _stage_gi_flashcards(self):
        for card in HST121_FLASHCARDS:
            self.anki_manager.add_card(card)

    def import_vision_curriculum(self) -> Dict[str, Any]:
        """Compiles Deep Learning & Computer Vision Foundations curriculum into the living wiki."""
        today = datetime.date.today().isoformat()
        
        # 1. Compile sessions
        sessions_created = []
        for s in VISION_SESSIONS:
            page_file = self.wiki_dir / "course_sessions" / f"{s['slug']}.md"
            file_content = f"""---
title: {s['title']}
system: Deep Learning & Computer Vision
domain: Computer Science & AI
course: 3D-Vision
source: ArXiv Deep Learning & Computer Vision Foundation Papers
last_compiled: {today}
---

# {s['title']}

**Instructors / Authors**: {s['instructors']}  
**Curriculum**: Deep Learning & 3D Computer Vision Research Track

> **Paper Essence**: {s['summary']}

{s['content']}

---
*Compiled from Deep Learning & 3D Vision Foundations*
"""
            page_file.write_text(file_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            sessions_created.append(s["slug"])

        # 2. Compile concepts
        concepts_created = []
        for c in VISION_CONCEPTS:
            page_file = self.wiki_dir / "concepts" / f"{c['slug']}.md"
            tags_str = ", ".join(c.get("tags", []))
            file_content = f"""---
title: {c['title']}
system: {c['system']}
domain: {c['domain']}
course: 3D-Vision
tags: [{tags_str}]
source: ArXiv Deep Learning & Computer Vision Foundation Papers
last_compiled: {today}
---

# {c['title']}

> **Core Summary**: {c['summary']}

{c['content']}

---
*Compiled from Deep Learning & 3D Vision Foundations*
"""
            page_file.write_text(file_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            concepts_created.append(c["slug"])

        # 3. Compile entities
        entities_created = []
        for e in VISION_ENTITIES:
            page_file = self.wiki_dir / "entities" / f"{e['slug']}.md"
            file_content = f"""---
title: {e['title']}
category: {e['category']}
domain: Computer Science & AI
course: 3D-Vision
source: ArXiv Deep Learning & Computer Vision Foundation Papers
last_compiled: {today}
---

# {e['title']}

> **Entity Classification**: `{e['category']}`

### High-Yield Architectural Notes
{e['high_yield_notes']}

---
*Compiled from Deep Learning & 3D Vision Foundations*
"""
            page_file.write_text(file_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            entities_created.append(e["slug"])

        # 4. Compile differentials
        diffs_created = []
        for d in VISION_DIFFERENTIALS:
            page_file = self.wiki_dir / "differentials" / f"{d['slug']}.md"
            file_content = f"""---
title: {d['title']}
domain: Computer Science & AI
course: 3D-Vision
source: ArXiv Deep Learning & Computer Vision Foundation Papers
last_compiled: {today}
---

# {d['title']}

> **Architectural Trade-offs**: {d['summary']}

{d['content']}

---
*Compiled from Deep Learning & 3D Vision Foundations*
"""
            page_file.write_text(file_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            diffs_created.append(d["slug"])

        # 5. Compile traps
        traps_created = []
        for t in VISION_TRAPS:
            page_file = self.wiki_dir / "exam_traps" / f"{t['slug']}.md"
            file_content = f"""---
title: {t['title']}
tags: [pitfall, deep-learning, computer-vision, failure-mode]
domain: Computer Science & AI
course: 3D-Vision
source: ArXiv Deep Learning & Computer Vision Foundation Papers
last_compiled: {today}
---

# {t['title']}

> [!CAUTION]
> **Research & Implementation Pitfall**:
> {t['summary']}

{t['content']}

---
*Compiled from Deep Learning & 3D Vision Foundations*
"""
            page_file.write_text(file_content, encoding="utf-8")
            self.indexer.index_file(page_file)
            traps_created.append(t["slug"])

        # 6. Stage flashcards
        for card in VISION_FLASHCARDS:
            self.anki_manager.add_card(card)

        # 7. Update curriculum & log
        self._update_curriculum_for_vision()
        self._refresh_master_index()

        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(f"\n## [{today}] curriculum_import | Compiled Deep Learning & Computer Vision Foundations\n")

        return {
            "success": True,
            "course": "Deep Learning & Computer Vision Foundations",
            "domain": "Computer Science & AI",
            "sessions_imported": len(sessions_created),
            "session_pages_compiled": len(sessions_created),
            "concepts_compiled": len(concepts_created),
            "entities_compiled": len(entities_created),
            "differentials_compiled": len(diffs_created),
            "traps_compiled": len(traps_created),
            "anki_cards_staged": len(VISION_FLASHCARDS)
        }

    def _update_curriculum_for_vision(self):
        mastery = self.student_profile.get_mastery()
        for k, v in [
            ("Vision Transformers & Attention", 75.0),
            ("3D Computer Vision & NeRF", 68.0),
            ("3D Gaussian Splatting", 70.0),
            ("Self-Supervised & Foundation Models (DINOv2)", 74.0),
            ("Generative Diffusion Models", 66.0),
            ("Visual SLAM & Spatial AI", 62.0)
        ]:
            if k not in mastery:
                mastery[k] = v

        self.student_profile.knowledge_file.write_text(json.dumps(mastery, indent=2), encoding="utf-8")

        schedule = {
            "current_block": "Deep Learning & 3D Computer Vision Research Track",
            "target_exam": "Deep Learning & Computer Vision Research Qualifying Milestone",
            "exam_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
            "topics": VISION_CURRICULUM_TOPICS
        }
        self.student_profile.update_schedule(schedule)

    def import_paper(
        self,
        title: str,
        abstract: str = "",
        content: str = "",
        arxiv_id: str = "",
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Synthesizes a research preprint or published paper into the Karpathy 5-layer wiki."""
        today = datetime.date.today().isoformat()
        clean_slug = re.sub(r'[^\w\-]', '-', title.lower()).strip('-')[:50]
        paper_tags = tags or ["Deep-Learning", "Computer-Vision", "Research-Paper"]
        
        # Save raw source into lectures/papers
        raw_dir = RAW_SOURCES_DIR / "papers"
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_file = raw_dir / f"{clean_slug}.md"
        raw_file.write_text(f"# {title}\n\nArXiv: {arxiv_id}\n\n## Abstract\n{abstract}\n\n## Content\n{content}", encoding="utf-8")

        # Compile concepts into wiki
        concepts_dir = self.wiki_dir / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        page_file = concepts_dir / f"{clean_slug}.md"
        tags_str = ", ".join(paper_tags)
        
        summary_text = abstract.strip() if abstract.strip() else f"Research paper on {title}."
        body_text = content.strip() if content.strip() else f"### Abstract\n{summary_text}\n\n### Key Theoretical Foundations\nFoundational principles and empirical benchmarks of {title}."
        
        file_content = f"""---
title: {title}
domain: Computer Science & AI
system: Deep Learning & Computer Vision
tags: [{tags_str}]
source: {arxiv_id or title}
last_compiled: {today}
---

# {title}

> **Core Summary**: {summary_text[:300]}

{body_text}

---
*Compiled from research paper preprint: `{title}` ({arxiv_id})*
"""
        page_file.write_text(file_content, encoding="utf-8")
        self.indexer.index_file(page_file)

        # Stage candidate active recall card
        self.anki_manager.add_card({
            "type": "cloze",
            "text": f"Paper Concept ({title}): {{c1::{summary_text[:120]}...}}",
            "pearl": f"Source: {title} ({arxiv_id})",
            "tags": paper_tags + [clean_slug],
            "source": f"paper: {clean_slug}"
        })

        self._refresh_master_index()

        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(f"\n## [{today}] paper_import | Compiled paper `{title}` ({clean_slug})\n")

        return {
            "success": True,
            "title": title,
            "slug": clean_slug,
            "rel_path": f"concepts/{clean_slug}.md",
            "card_staged": True
        }
