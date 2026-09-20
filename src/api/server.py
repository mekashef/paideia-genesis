"""FastAPI Server exposing the Living Medical Teacher API and serving the Web Dashboard."""
import os
import re
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from src.config import WIKI_DIR, RAW_SOURCES_DIR, ANKI_EXPORT_DIR, LLM_PROVIDER
from src.wiki.schema import init_wiki_structure
from src.wiki.indexer import WikiIndexer, parse_markdown_file
from src.wiki.compiler import WikiCompiler
from src.wiki.graph_memory import AssociativeGraphMemory
from src.wiki.knowledge_puller import KnowledgePuller
from src.tutor.student_profile import StudentProfile
from src.tutor.socratic_engine import SocraticTeacher
from src.anki.generator import AnkiManager
from src.wiki.course_importer import CourseImporter

app = FastAPI(
    title="Paideia Genesis - Living Medical Teacher & LLM-Wiki",
    description="Adaptive Medical Learning System combining Karpathy's LLM-Wiki, HippoRAG, and Socratic tutoring.",
    version="0.2.0"
)

# Initialize engines
init_wiki_structure()
indexer = WikiIndexer()
compiler = WikiCompiler()
student_profile = StudentProfile()
teacher = SocraticTeacher()
anki_manager = AnkiManager()
graph_memory = AssociativeGraphMemory()
knowledge_puller = KnowledgePuller()
course_importer = CourseImporter()

# Ensure static directory exists
STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

class AnswerSubmission(BaseModel):
    vignette: Dict[str, Any]
    selected_option_id: str
    student_reasoning: Optional[str] = ""

class IngestTextRequest(BaseModel):
    filename: str
    content: str
    source_type: Optional[str] = "lecture"

class UpdatePageRequest(BaseModel):
    path: str
    content: str

class QuickCaptureRequest(BaseModel):
    note: str
    topic_hint: Optional[str] = "General"
    tags: Optional[List[str]] = []

class PullExternalRequest(BaseModel):
    query: str

class ImportCourseRequest(BaseModel):
    url: Optional[str] = "https://ocw.mit.edu/courses/hst-121-gastroenterology-fall-2005/pages/lecture-notes/"

class CardReviewRequest(BaseModel):
    card_id: str
    rating: int


@app.get("/api/status")
def get_status():
    all_pages = list(WIKI_DIR.rglob("*.md"))
    schedule = student_profile.get_schedule()
    staged = anki_manager.get_staged_cards()
    return {
        "status": "online",
        "llm_provider": LLM_PROVIDER,
        "total_wiki_pages": len(all_pages),
        "days_to_exam": schedule.get("days_remaining", 0),
        "target_exam": schedule.get("target_exam", "Medical Board"),
        "staged_flashcards": len(staged)
    }

@app.get("/api/wiki/tree")
def get_wiki_tree(course: Optional[str] = None):
    categories = ["course_sessions", "concepts", "entities", "differentials", "exam_traps", "student_profile"]
    tree: Dict[str, Any] = {}
    
    course_filter = (course or "all").lower().strip()

    for cat in categories:
        folder = WIKI_DIR / cat
        items = []
        if folder.exists():
            for f in sorted(folder.glob("*.md")):
                parsed = parse_markdown_file(f)
                sys_tag = parsed.get("system") or ""
                src_tag = parsed.get("source") or ""
                raw_tags = parsed.get("tags") or ""

                # Determine course association
                title_lower = parsed["title"].lower()
                stem_lower = f.stem.lower()

                is_hst121 = (
                    "hst.121" in src_tag.lower()
                    or "hst.121" in raw_tags.lower()
                    or "gastroenterology" in sys_tag.lower()
                    or "hepatology" in sys_tag.lower()
                    or "gi" in raw_tags.lower()
                    or cat == "course_sessions"
                    or stem_lower == "spironolactone"
                )
                is_cardio = (
                    "cardio" in raw_tags.lower()
                    or "renal" in raw_tags.lower()
                    or "cardio" in sys_tag.lower()
                    or "renal" in sys_tag.lower()
                    or "cardio" in title_lower
                    or "heart" in stem_lower
                    or "diuretic" in stem_lower
                    or "carvedilol" in stem_lower
                    or "furosemide" in stem_lower
                    or stem_lower == "spironolactone"
                )

                item_course = "HST.121" if is_hst121 and not is_cardio else ("Cardiopulmonary" if is_cardio and not is_hst121 else ("Both" if is_hst121 and is_cardio else "Core"))

                if course_filter in ["hst121", "hst-121", "gastroenterology"] and not is_hst121:
                    continue
                if course_filter in ["cardio", "cardiopulmonary", "renal"] and not is_cardio:
                    continue

                items.append({
                    "slug": f.stem,
                    "title": parsed["title"],
                    "rel_path": str(f.relative_to(WIKI_DIR)),
                    "tags": raw_tags,
                    "system": sys_tag,
                    "source": src_tag,
                    "course": item_course
                })
        tree[cat] = items
    return tree

@app.get("/api/wiki/page")
def get_wiki_page(path: str):
    file_path = (WIKI_DIR / path).resolve()
    if not file_path.exists() or not str(file_path).startswith(str(WIKI_DIR.resolve())):
        raise HTTPException(status_code=404, detail="Page not found")
    parsed = parse_markdown_file(file_path)
    return {
        "rel_path": path,
        "title": parsed["title"],
        "content": parsed["raw"],
        "body": parsed["body"],
        "links": parsed["links"]
    }

@app.get("/api/wiki/search")
def search_wiki(q: str):
    results = indexer.search(q, limit=15)
    return {"query": q, "results": results}

@app.get("/api/wiki/graph")
def get_wiki_graph():
    return indexer.get_graph()

@app.get("/api/wiki/brain_graph")
def get_brain_graph(course: Optional[str] = None, layer: Optional[str] = None):
    return graph_memory.get_brain_graph(course=course, layer=layer)

@app.get("/api/wiki/associative_recall")
def get_associative_recall(slug: str, top_k: int = 5):
    return {"seed": slug, "associative_concepts": graph_memory.get_associative_context([slug], top_k=top_k)}

@app.put("/api/wiki/page")
def update_wiki_page(req: UpdatePageRequest):
    file_path = (WIKI_DIR / req.path).resolve()
    if not str(file_path).startswith(str(WIKI_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden path")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(req.content, encoding="utf-8")
    indexer.index_file(file_path)
    today = datetime.date.today().isoformat()
    with open(WIKI_DIR / "log.md", "a", encoding="utf-8") as f:
        f.write(f"\n## [{today}] user_edit | Modified `{req.path}` directly via web editor\n")
    return {"success": True, "path": req.path}

@app.post("/api/wiki/quick_capture")
def quick_capture(req: QuickCaptureRequest):
    today = datetime.date.today().isoformat()
    clean_topic = re.sub(r'[^\w\-]', '-', req.topic_hint.lower()).strip('-') or "quick-notes"
    slug = f"capture-{clean_topic}"
    page_file = WIKI_DIR / "concepts" / f"{slug}.md"
    tags_list = req.tags if req.tags else ["Quick-Capture", req.topic_hint]
    tags_str = ", ".join(tags_list)
    
    if page_file.exists():
        existing = page_file.read_text(encoding="utf-8")
        if req.note.strip() in existing:
            # Idempotent deduplication: identical note was already captured
            return {"success": True, "slug": slug, "rel_path": f"concepts/{slug}.md", "status": "already_exists"}
        
        # Compounding: append new note under dated section
        compounded = existing.rstrip() + f"\n\n### Additional Note ({today})\n> {req.note}\n"
        page_file.write_text(compounded, encoding="utf-8")
        indexer.index_file(page_file)
        with open(WIKI_DIR / "log.md", "a", encoding="utf-8") as f:
            f.write(f"\n## [{today}] quick_capture | Compounded note into `{slug}`\n")
    else:
        content = f"""---
title: Quick Capture: {req.topic_hint}
system: Clinical Notes
tags: [{tags_str}]
source: On-The-Fly Quick Capture
last_compiled: {today}
---

# Quick Capture: {req.topic_hint}

> **Captured Clinical Note / Board Pearl**:
> {req.note}

---
*Created on-the-fly by student in Paideia Genesis*
"""
        page_file.write_text(content, encoding="utf-8")
        indexer.index_file(page_file)
        with open(WIKI_DIR / "log.md", "a", encoding="utf-8") as f:
            f.write(f"\n## [{today}] quick_capture | Saved on-the-fly note `{slug}`\n")

    # Automatically stage flashcard candidate (AnkiManager deduplicates identical cards)
    anki_manager.add_card({
        "type": "cloze",
        "text": f"Quick Pearl ({req.topic_hint}): {req.note}",
        "pearl": f"Source: Quick Capture ({today})",
        "tags": ["PaideiaGenesis", "QuickCapture", clean_topic],
        "source": f"Quick capture: {slug}"
    })

    return {"success": True, "slug": slug, "rel_path": f"concepts/{slug}.md"}

@app.post("/api/wiki/pull_external")
def pull_external_knowledge(req: PullExternalRequest):
    synthesized = knowledge_puller.pull_and_synthesize(req.query)
    result = knowledge_puller.integrate_into_wiki(synthesized)
    return {
        "success": True,
        "title": synthesized.get("title", req.query),
        "slug": synthesized.get("slug"),
        "rel_path": result.get("rel_path"),
        "summary": synthesized.get("summary")
    }

@app.post("/api/wiki/ingest")
def ingest_text_source(req: IngestTextRequest):
    result = compiler.ingest_source(req.filename, req.content, req.source_type)
    return result

@app.post("/api/wiki/ingest_demo")
def ingest_demo_lecture():
    demo_file = Path(__file__).resolve().parent.parent.parent / "demo_data" / "Cardiology_Block_Lecture_4_Heart_Failure_and_Diuretics.md"
    if not demo_file.exists():
        raise HTTPException(status_code=404, detail="Demo lecture file not found")
    content = demo_file.read_text(encoding="utf-8")
    result = compiler.ingest_source("Cardiology_Lecture_4_ADHF_and_Diuretics.md", content, "lecture")
    return result

@app.post("/api/course/import_hst121")
def import_hst121():
    result = course_importer.import_hst121_course()
    return result

@app.post("/api/course/import_url")
def import_course_url(req: ImportCourseRequest):
    result = course_importer.import_hst121_course(req.url)
    return result

@app.get("/api/curriculum")
def get_curriculum():
    return student_profile.get_schedule()

@app.get("/api/student/profile")
def get_student_summary():
    return student_profile.get_profile_summary()

@app.post("/api/tutor/generate_vignette")
def generate_vignette():
    return teacher.generate_adaptive_vignette()

@app.post("/api/tutor/evaluate")
def evaluate_answer(sub: AnswerSubmission):
    result = teacher.evaluate_response(sub.vignette, sub.selected_option_id, sub.student_reasoning)
    # If card candidate was generated, automatically stage it into Anki manager
    card_cand = result.get("anki_card_candidate")
    if card_cand:
        anki_manager.add_card({
            "type": "cloze",
            "text": card_cand.get("front", ""),
            "pearl": card_cand.get("back", ""),
            "tags": ["PaideiaGenesis", "Board-Trap", sub.vignette.get("topic", "Cardiology")],
            "source": f"Diagnostic drill: {sub.vignette.get('vignette_id')}"
        })
    return result

@app.get("/api/anki/cards")
def get_staged_anki_cards(
    course: Optional[str] = None,
    system: Optional[str] = None,
    card_type: Optional[str] = None,
    mastery: Optional[str] = None,
    query: Optional[str] = None
):
    return anki_manager.get_filtered_cards(
        course=course,
        system=system,
        card_type=card_type,
        mastery=mastery,
        search=query
    )

@app.post("/api/anki/cards/review")
def review_anki_card(req: CardReviewRequest):
    updated_card = anki_manager.record_review(req.card_id, req.rating)
    if not updated_card:
        raise HTTPException(status_code=404, detail="Flashcard not found")

    # Sync mastery to student profile
    system_tag = updated_card.get("system", "Pharmacology")
    is_correct = (req.rating >= 3)
    student_profile.record_attempt(
        topic=system_tag,
        is_correct=is_correct,
        error_type="SPACED_REPETITION_SLIP" if not is_correct else None,
        details=f"Card drill: {updated_card.get('source', req.card_id)}"
    )

    stats = anki_manager.get_filtered_cards()["stats"]
    return {
        "success": True,
        "card": updated_card,
        "stats": stats
    }

@app.post("/api/anki/compile_from_wiki")
def compile_cards_from_wiki():
    result = anki_manager.recompile_from_wiki()
    result["stats"] = anki_manager.get_filtered_cards()["stats"]
    return result

@app.get("/api/anki/export")
def download_anki_deck(course: Optional[str] = None, system: Optional[str] = None):
    apkg_file = anki_manager.generate_apkg(course=course, system=system)
    return FileResponse(
        str(apkg_file),
        media_type="application/octet-stream",
        filename=apkg_file.name
    )

@app.post("/api/anki/sync_ankiconnect")
def sync_ankiconnect():
    return anki_manager.sync_to_ankiconnect()


# Mount static files
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
