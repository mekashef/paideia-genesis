"""Main entrypoint for Paideia Genesis Living Medical Teacher & LLM-Wiki."""
import sys
import uvicorn
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.config import HOST, PORT, WIKI_DIR, DEMO_DATA_DIR
from src.wiki.schema import init_wiki_structure
from src.wiki.compiler import WikiCompiler
from src.wiki.indexer import WikiIndexer
from src.api.server import app

def main():
    print("=" * 70)
    print("  Paideia Genesis - Living Medical Teacher & Compounding LLM-Wiki")
    print("  Inspired by Andrej Karpathy's LLM-Wiki & Socratic Medical Tutoring")
    print("=" * 70)
    
    # 1. Initialize directory structure and schema
    print("[1/3] Initializing Karpathy-style Medical Wiki schema...")
    init_wiki_structure()

    # 2. Check if initial curricula should be pre-compiled
    concepts_dir = WIKI_DIR / "concepts"
    if not any(concepts_dir.glob("*.md")):
        print("[2/3] Seeding starter medical curricula (Cardiology & MIT HST.121)...")
        demo_lecture = DEMO_DATA_DIR / "Cardiology_Block_Lecture_4_Heart_Failure_and_Diuretics.md"
        if demo_lecture.exists():
            compiler = WikiCompiler()
            compiler.ingest_source(
                filename="Cardiology_Lecture_4_ADHF_and_Diuretics.md",
                content=demo_lecture.read_text(encoding="utf-8"),
                source_type="lecture"
            )
            print("      ✓ Cardiology Block compiled into concepts, entities, and differentials.")

        from src.wiki.course_importer import CourseImporter
        from src.anki.generator import AnkiManager

        importer = CourseImporter()
        importer.import_mit_ocw_course()
        print("      ✓ MIT HST.121 Gastroenterology & Hepatology curriculum compiled.")

        anki_mgr = AnkiManager()
        anki_mgr.recompile_from_wiki()
        print("      ✓ 117-card spaced-repetition master deck synthesized.")
    else:
        print("[2/3] Existing Medical Wiki found. Reindexing with SQLite FTS5...")
        indexer = WikiIndexer()
        indexer.reindex_all()


    # 3. Start server
    print(f"[3/3] Starting Paideia Genesis Web Server on http://{HOST}:{PORT}...")
    print(f"      Dashboard: http://localhost:{PORT}")
    print("=" * 70)

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    main()
