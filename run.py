"""Main entrypoint for Paideia Genesis Living Medical Teacher & LLM-Wiki."""
import sys
import uvicorn
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.config import HOST, PORT, WIKI_DIR, RAW_SOURCES_DIR, DEMO_DATA_DIR, AUTO_SEED_DEMO_DATA
from src.wiki.schema import init_wiki_structure
from src.wiki.compiler import WikiCompiler
from src.wiki.indexer import WikiIndexer
from src.api.server import app

def main():
    print("=" * 70)
    print("  Paideia Genesis - Universal Living Education Assistant & Compounding LLM-Wiki")
    print("  Personalized Socratic AI Tutor & Knowledge Engine for All Disciplines")
    print("=" * 70)
    
    # Check for CLI flags
    clean_requested = "--clean" in sys.argv
    seed_requested = "--seed" in sys.argv or AUTO_SEED_DEMO_DATA

    # 1. Initialize directory structure and schema
    print("[1/3] Initializing Karpathy-style Universal Wiki schema...")
    init_wiki_structure()

    if clean_requested:
        print("      [CLEAN] Purging existing wiki content for a clean research workspace...")
        for subdir in ["concepts", "course_sessions", "differentials", "entities", "exam_traps"]:
            target = WIKI_DIR / subdir
            if target.exists():
                for f in target.glob("*.md"):
                    try:
                        f.unlink()
                    except Exception:
                        pass
        for subdir in ["lectures", "exam_logs"]:
            target = RAW_SOURCES_DIR / subdir
            if target.exists():
                for f in target.glob("*"):
                    try:
                        f.unlink()
                    except Exception:
                        pass
        from src.anki.generator import AnkiManager
        anki_mgr = AnkiManager()
        if anki_mgr.cards_file.exists():
            anki_mgr.cards_file.write_text("[]", encoding="utf-8")
        init_wiki_structure()
        print("      ✓ Wiki purged to clean slate.")

    # 2. Check if initial curricula should be pre-compiled
    concepts_dir = WIKI_DIR / "concepts"
    has_content = any(concepts_dir.glob("*.md"))

    if seed_requested and not has_content:
        print("[2/3] Seeding starter curricula (MIT 6.033 Distributed Systems & HST.121)...")
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
        importer.import_engineering_course()
        print("      ✓ MIT 6.033 Distributed Systems & Networking curriculum compiled.")

        anki_mgr = AnkiManager()
        anki_mgr.recompile_from_wiki()
        print("      ✓ Spaced-repetition universal master deck synthesized.")
    else:
        if has_content:
            print("[2/3] Existing Wiki found. Reindexing with SQLite FTS5...")
        else:
            print("[2/3] Pristine research workspace ready. (Use --seed to load starter curricula)")
        indexer = WikiIndexer()
        indexer.reindex_all()

    # 3. Start server
    print(f"[3/3] Starting Paideia Genesis Web Server on http://{HOST}:{PORT}...")
    print(f"      Dashboard: http://localhost:{PORT}")
    print("=" * 70)

    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    main()
