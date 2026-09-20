"""Anki Flashcard Generator and AnkiConnect Bridge using genanki and SM-2 Spaced Repetition."""
import re
import json
import random
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
import genanki
from src.config import ANKI_EXPORT_DIR, ANKI_CONNECT_URL, WIKI_DIR
from src.anki.compiler import WikiFlashcardCompiler, atomize_card

CARDS_STORAGE_FILE = ANKI_EXPORT_DIR / "staged_cards.json"

# Genanki custom CSS styling for medical flashcards
MED_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 19px;
    text-align: left;
    color: #1f2937;
    background-color: #f9fafb;
    padding: 24px;
    line-height: 1.6;
    border-radius: 12px;
}
.cloze {
    font-weight: bold;
    color: #2563eb;
    background-color: #dbeafe;
    padding: 2px 6px;
    border-radius: 4px;
}
.pearl-box {
    margin-top: 18px;
    padding: 12px 16px;
    background: #ecfdf5;
    border-left: 4px solid #10b981;
    color: #065f46;
    border-radius: 0 8px 8px 0;
    font-size: 16px;
}
.tag-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    color: #4b5563;
    background: #e5e7eb;
    padding: 2px 8px;
    border-radius: 9999px;
    margin-bottom: 12px;
}
"""

CLOZE_MODEL = genanki.Model(
    987234123,
    'Paideia Genesis Cloze Model',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Cloze Card',
            'qfmt': '<span class="tag-badge">{{Tags}}</span><div>{{cloze:Text}}</div>',
            'afmt': '<span class="tag-badge">{{Tags}}</span><div>{{cloze:Text}}</div><hr id="answer"><div class="pearl-box"><strong>Clinical Pearl:</strong> {{Extra}}</div>',
        },
    ],
    css=MED_CSS
)

QA_MODEL = genanki.Model(
    876123456,
    'Paideia Genesis QA Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Pearl'},
        {'name': 'Tags'},
    ],
    templates=[
        {
            'name': 'Forward Card',
            'qfmt': '<span class="tag-badge">{{Tags}}</span><div style="font-weight: 600;">{{Question}}</div>',
            'afmt': '<span class="tag-badge">{{Tags}}</span><div style="font-weight: 600;">{{Question}}</div><hr id="answer"><div>{{Answer}}</div><div class="pearl-box"><strong>Board Pearl:</strong> {{Pearl}}</div>',
        },
    ],
    css=MED_CSS
)

class AnkiManager:
    def __init__(self, export_dir: Path = ANKI_EXPORT_DIR, wiki_dir: Path = WIKI_DIR):
        self.export_dir = export_dir
        self.wiki_dir = wiki_dir
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.cards_file = self.export_dir / "staged_cards.json"
        self._init_storage()

    def _init_storage(self):
        """Initializes storage and compiles comprehensive wiki cards if empty or small."""
        if not self.cards_file.exists():
            self.recompile_from_wiki()
        else:
            try:
                cards = json.loads(self.cards_file.read_text(encoding="utf-8"))
                if len(cards) < 30:
                    self.recompile_from_wiki()
            except Exception:
                self.recompile_from_wiki()

    def recompile_from_wiki(self, atomic: bool = False) -> Dict[str, Any]:
        """Compiles cards across all wiki files, merging with existing review histories."""
        existing = []
        if self.cards_file.exists():
            try:
                existing = json.loads(self.cards_file.read_text(encoding="utf-8"))
            except Exception:
                existing = []

        compiler = WikiFlashcardCompiler(self.wiki_dir)
        compiled_cards = compiler.compile_all(existing_cards=existing, atomic_cards=atomic)
        self.cards_file.write_text(json.dumps(compiled_cards, indent=2), encoding="utf-8")
        return {
            "success": True,
            "total_cards": len(compiled_cards),
            "added": max(0, len(compiled_cards) - len(existing))
        }

    def get_staged_cards(self) -> List[Dict[str, Any]]:
        if not self.cards_file.exists():
            return []
        try:
            return json.loads(self.cards_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def get_filtered_cards(
        self,
        course: Optional[str] = None,
        system: Optional[str] = None,
        card_type: Optional[str] = None,
        mastery: Optional[str] = None,
        search: Optional[str] = None,
        cloze_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """Filters cards based on course, organ system, card type, mastery, search keyword, and cloze derivation mode."""
        all_cards = self.get_staged_cards()
        today_str = datetime.date.today().isoformat()

        # Handle Cloze Derivation Mode (Atomic 1-by-1 vs Combined Multi-Cloze)
        if cloze_mode == "atomic":
            derived_pool = []
            for c in all_cards:
                derived_pool.extend(atomize_card(c))
            all_cards = derived_pool
        elif cloze_mode == "combined":
            # Filter out derived child cards if present in storage, preserving base multi-cloze format
            all_cards = [c for c in all_cards if "parent_id" not in c]

        # Compute global stats
        stats = {
            "total": len(all_cards),
            "due": sum(1 for c in all_cards if c.get("due_date", today_str) <= today_str or c.get("mastery") == "unreviewed"),
            "unreviewed": sum(1 for c in all_cards if c.get("mastery") == "unreviewed"),
            "struggling": sum(1 for c in all_cards if c.get("mastery") == "struggling"),
            "learning": sum(1 for c in all_cards if c.get("mastery") == "learning"),
            "mastered": sum(1 for c in all_cards if c.get("mastery") == "mastered"),
            "by_system": {},
            "by_course": {
                "HST.121": 0,
                "Cardiopulmonary": 0,
                "Both": 0
            }
        }
        for c in all_cards:
            sys = c.get("system") or "Other"
            stats["by_system"][sys] = stats["by_system"].get(sys, 0) + 1
            crs = c.get("course") or "HST.121"
            stats["by_course"][crs] = stats["by_course"].get(crs, 0) + 1

        stats["mastery_percentage"] = round((stats["mastered"] / max(1, stats["total"])) * 100, 1)

        # Filtering
        filtered = all_cards

        # Course filter
        if course and course.lower() != "all":
            clow = course.lower().strip()
            if clow in ["hst121", "hst-121", "gi", "liver"]:
                filtered = [c for c in filtered if c.get("course") in ["HST.121", "Both"]]
            elif clow in ["cardio", "cardiopulmonary", "renal"]:
                filtered = [c for c in filtered if c.get("course") in ["Cardiopulmonary", "Both"]]

        # System filter
        if system and system.lower() != "all":
            slow = system.lower().strip()
            filtered = [c for c in filtered if slow in (c.get("system") or "").lower()]

        # Card Type filter
        if card_type and card_type.lower() != "all":
            tlow = card_type.lower().strip()
            filtered = [c for c in filtered if tlow == (c.get("type") or "").lower()]

        # Mastery filter
        if mastery and mastery.lower() != "all":
            mlow = mastery.lower().strip()
            if mlow == "due":
                filtered = [c for c in filtered if c.get("due_date", today_str) <= today_str or c.get("mastery") == "unreviewed"]
            else:
                filtered = [c for c in filtered if (c.get("mastery") or "unreviewed").lower() == mlow]

        # Text search
        if search and search.strip():
            q = search.strip().lower()
            def match_card(c: Dict[str, Any]) -> bool:
                fields = [
                    c.get("text", ""),
                    c.get("front", ""),
                    c.get("back", ""),
                    c.get("pearl", ""),
                    c.get("system", ""),
                    c.get("source", ""),
                    c.get("target_unknown", ""),
                    " ".join(c.get("tags", []))
                ]
                return any(q in f.lower() for f in fields)
            filtered = [c for c in filtered if match_card(c)]

        return {
            "cards": filtered,
            "filtered_count": len(filtered),
            "stats": stats
        }

    def record_review(self, card_id: str, rating: int) -> Optional[Dict[str, Any]]:
        """Updates spaced repetition state of a card using the SM-2 algorithm.
        Supports both base Anki cards and derived atomic single-unknown cards.
        Rating:
          1: Again (< 10 min / Struggling)
          2: Hard (1 day / Difficult)
          3: Good (3-4 days / Retained)
          4: Easy (7+ days / Mastered)
        """
        cards = self.get_staged_cards()
        target_card = None
        target_idx = -1

        for idx, c in enumerate(cards):
            if c.get("id") == card_id:
                target_card = c
                target_idx = idx
                break

        # Check if card_id is a derived atomic child card (e.g. card-002-c1)
        parent_card = None
        parent_idx = -1
        if not target_card and "-c" in card_id:
            parent_id = card_id.rsplit("-c", 1)[0]
            for idx, c in enumerate(cards):
                if c.get("id") == parent_id:
                    parent_card = c
                    parent_idx = idx
                    atomic_children = atomize_card(c)
                    for child in atomic_children:
                        if child.get("id") == card_id:
                            target_card = child
                            break
                    break

        if not target_card:
            return None

        today = datetime.date.today()
        repetitions = target_card.get("repetitions", 0)
        interval = min(36500, max(1, target_card.get("interval", 1)))
        ease_factor = target_card.get("ease_factor", 2.5)

        # SuperMemo-2 (SM-2) algorithm
        # Map rating 1..4 to quality scale 1..5
        q_map = {1: 1, 2: 2, 3: 4, 4: 5}
        quality = q_map.get(rating, 3)

        if rating < 3:
            # Failed recall
            repetitions = 0
            interval = 1
            mastery = "struggling"
        else:
            # Successful recall
            if repetitions == 0:
                interval = 1
            elif repetitions == 1:
                interval = 3 if rating == 3 else 5
            else:
                interval = min(36500, int(round(interval * ease_factor)))

            repetitions += 1
            # Adjust ease factor
            ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))

            if interval >= 7 or repetitions >= 3:
                mastery = "mastered"
            else:
                mastery = "learning"

        next_due = (today + datetime.timedelta(days=interval)).isoformat()

        target_card["repetitions"] = repetitions
        target_card["interval"] = interval
        target_card["ease_factor"] = round(ease_factor, 2)
        target_card["due_date"] = next_due
        target_card["last_reviewed"] = today.isoformat()
        target_card["mastery"] = mastery

        if target_idx >= 0:
            cards[target_idx] = target_card
        elif parent_card is not None and parent_idx >= 0:
            # Store atomic child review state in parent card's atomic_states dictionary
            parent_card.setdefault("atomic_states", {})[card_id] = {
                "repetitions": repetitions,
                "interval": interval,
                "ease_factor": round(ease_factor, 2),
                "due_date": next_due,
                "last_reviewed": today.isoformat(),
                "mastery": mastery
            }
            parent_card["last_reviewed"] = today.isoformat()
            cards[parent_idx] = parent_card

        self.cards_file.write_text(json.dumps(cards, indent=2), encoding="utf-8")
        return target_card

    def grade_student_recall(self, card_id: str, student_answer: str) -> Optional[Dict[str, Any]]:
        """Evaluates student's free-text active recall with Jev System 1 and updates SM-2.
        Supports both base Anki cards and derived atomic single-unknown cards.
        """
        cards = self.get_staged_cards()
        target_card = None
        for c in cards:
            if c.get("id") == card_id:
                target_card = c
                break

        if not target_card and "-c" in card_id:
            parent_id = card_id.rsplit("-c", 1)[0]
            for c in cards:
                if c.get("id") == parent_id:
                    atomic_children = atomize_card(c)
                    for child in atomic_children:
                        if child.get("id") == card_id:
                            target_card = child
                            break
                    break

        if not target_card:
            return None

        from src.llm.jev_client import jev_client
        grade_result = jev_client.grade_free_text_recall(target_card, student_answer)
        sm2_rating = grade_result["sm2_rating"]

        # Update card repetition via SM-2
        updated_card = self.record_review(card_id, sm2_rating)

        return {
            "card": updated_card,
            "grading": grade_result
        }

    def add_card(self, card_data: Dict[str, Any]) -> Dict[str, Any]:
        """Adds or deduplicates a single flashcard."""
        cards = self.get_staged_cards()
        new_text = (card_data.get("text") or card_data.get("front") or "").strip()
        if new_text:
            for existing in cards:
                existing_text = (existing.get("text") or existing.get("front") or "").strip()
                if existing_text == new_text:
                    return existing

        if not card_data.get("id"):
            card_data["id"] = f"card-{len(cards)+1:03d}"
        if "repetitions" not in card_data:
            card_data["repetitions"] = 0
            card_data["interval"] = 1
            card_data["ease_factor"] = 2.5
            card_data["due_date"] = datetime.date.today().isoformat()
            card_data["last_reviewed"] = None
            card_data["mastery"] = "unreviewed"

        cards.append(card_data)
        self.cards_file.write_text(json.dumps(cards, indent=2), encoding="utf-8")
        return card_data

    def generate_apkg(
        self,
        course: Optional[str] = None,
        system: Optional[str] = None,
        deck_name: Optional[str] = None,
        atomic: bool = False
    ) -> Path:
        """Compiles staged cards into a downloadable Anki .apkg file, supporting course filtering and atomic derivation."""
        filtered_result = self.get_filtered_cards(course=course, system=system, cloze_mode="atomic" if atomic else None)
        cards = filtered_result["cards"]

        if not deck_name:
            suffix = "_SingleUnknown" if atomic else ""
            if course and course.lower() in ["hst121", "hst-121"]:
                deck_name = f"PaideiaGenesis::MIT_HST121_Gastroenterology{suffix}"
            elif course and course.lower() in ["cardio", "cardiopulmonary"]:
                deck_name = f"PaideiaGenesis::Cardiopulmonary_Renal{suffix}"
            else:
                deck_name = f"PaideiaGenesis::Master_Medical_HighYield{suffix}"

        deck_id = random.randrange(1 << 30, 1 << 31)
        deck = genanki.Deck(deck_id, deck_name)

        for card in cards:
            raw_tags = card.get("tags", ["PaideiaGenesis"])
            tags = [re.sub(r'[^\w\-]', '_', str(t)).strip('_') for t in raw_tags if str(t).strip()]
            if card.get("system"):
                tags.append(re.sub(r'[^\w\-]', '_', card["system"]).strip('_'))
            if card.get("course"):
                tags.append(re.sub(r'[^\w\-]', '_', card["course"]).strip('_'))
            tags_str = " ".join(tags)

            def sanitize_field(val: str) -> str:
                if not val:
                    return ""
                # Replace naked < and > before digits (e.g. < 50, > 125) with HTML entities
                s = re.sub(r'<(\s*\d)', r'&lt;\1', str(val))
                s = re.sub(r'>(\s*\d)', r'&gt;\1', s)
                return s

            if card.get("type") in ["cloze", "differential", "trap"] or "{{c1::" in card.get("text", ""):
                note = genanki.Note(
                    model=CLOZE_MODEL,
                    fields=[sanitize_field(card.get("text", card.get("front", ""))), sanitize_field(card.get("pearl", card.get("back", ""))), tags_str],
                    tags=tags
                )
                deck.add_note(note)
            else:
                note = genanki.Note(
                    model=QA_MODEL,
                    fields=[sanitize_field(card.get("front", "")), sanitize_field(card.get("back", "")), sanitize_field(card.get("pearl", "")), tags_str],
                    tags=tags
                )
                deck.add_note(note)

        clean_filename = re.sub(r'[^\w\-]', '_', deck_name).strip('_') + ".apkg"
        out_file = self.export_dir / clean_filename
        package = genanki.Package(deck)
        package.write_to_file(str(out_file))
        return out_file

    def sync_to_ankiconnect(self) -> Dict[str, Any]:
        """Attempts to sync staged cards to a running Anki instance via AnkiConnect (localhost:8765)."""
        try:
            test_resp = requests.post(ANKI_CONNECT_URL, json={"action": "version", "version": 6}, timeout=2)
            if test_resp.status_code != 200:
                return {"success": False, "message": "AnkiConnect returned unexpected response"}

            cards = self.get_staged_cards()
            deck_name = "PaideiaGenesis::Medical_Master_HighYield"

            requests.post(ANKI_CONNECT_URL, json={"action": "createDeck", "version": 6, "params": {"deck": deck_name}}, timeout=2)

            notes_payload = []
            for c in cards:
                notes_payload.append({
                    "deckName": deck_name,
                    "modelName": "Cloze",
                    "fields": {
                        "Text": c.get("text", c.get("front", "")),
                        "Extra": c.get("pearl", c.get("back", ""))
                    },
                    "tags": c.get("tags", ["PaideiaGenesis"])
                })

            resp = requests.post(ANKI_CONNECT_URL, json={"action": "addNotes", "version": 6, "params": {"notes": notes_payload}}, timeout=5)
            data = resp.json()
            return {"success": True, "synced_count": len(cards), "data": data}
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "AnkiConnect is not currently running. Start Anki Desktop with AnkiConnect addon to enable 1-click sync, or download the .apkg file directly."
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
