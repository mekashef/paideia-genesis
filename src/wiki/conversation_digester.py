"""Conversation Capture & Discourse Topic Digestion Engine.

Transforms unstructured dialogues, advisor meetings, lab debates, and audio recordings
into Karpathy-style compounding wiki pages, concept mechanisms, and active recall cards.
"""
import io
import re
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import pypdf

from src.config import WIKI_DIR, RAW_SOURCES_DIR
from src.wiki.schema import init_wiki_structure
from src.wiki.indexer import WikiIndexer
from src.anki.generator import AnkiManager
from src.llm.client import get_llm_client, BaseLLMClient

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".webm", ".flac", ".aac"}
DOC_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown", ".json", ".csv"}

class ConversationDigester:
    def __init__(
        self,
        llm_client: Optional[BaseLLMClient] = None,
        wiki_dir: Path = WIKI_DIR,
        raw_sources_dir: Path = RAW_SOURCES_DIR
    ):
        self.wiki_dir = wiki_dir
        if raw_sources_dir == RAW_SOURCES_DIR and wiki_dir != WIKI_DIR:
            self.raw_sources_dir = wiki_dir.parent / "raw_sources"
        else:
            self.raw_sources_dir = raw_sources_dir
        self.llm = llm_client or get_llm_client()
        self.indexer = WikiIndexer(self.wiki_dir)
        self.anki_manager = AnkiManager(wiki_dir=self.wiki_dir)
        init_wiki_structure(self.wiki_dir, self.raw_sources_dir)

    def extract_text_from_document(self, file_data: Union[bytes, Path, str], filename: Optional[str] = None) -> str:
        """Extracts text from uploaded documents (PDF, Markdown, TXT) or audio."""
        if isinstance(file_data, (Path, str)):
            p = Path(file_data)
            if p.exists() and p.is_file():
                filename = filename or p.name
                file_bytes = p.read_bytes()
            else:
                file_bytes = str(file_data).encode("utf-8")
                filename = filename or "document.txt"
        else:
            file_bytes = file_data
            filename = filename or "document.txt"

        ext = Path(filename).suffix.lower()

        if ext == ".pdf":
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            pages = []
            for idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(f"--- Page {idx + 1} ---\n{text.strip()}")
            return "\n\n".join(pages)

        elif ext in AUDIO_EXTENSIONS:
            mime = "audio/webm" if ext == ".webm" else ("audio/mp4" if ext == ".m4a" else f"audio/{ext.lstrip('.')}")
            return self.llm.transcribe_audio(file_bytes, filename=filename, mime_type=mime)

        elif ext in [".txt", ".md", ".markdown", ".json", ".csv"]:
            try:
                return file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                return file_bytes.decode("latin-1", errors="replace")

        else:
            # Fallback raw string decode
            try:
                return file_bytes.decode("utf-8")
            except Exception:
                return file_bytes.decode("latin-1", errors="replace")

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "recording.wav", mime_type: str = "audio/wav") -> str:
        """Dispatches audio to LLM audio transcription gateway."""
        return self.llm.transcribe_audio(audio_bytes, filename=filename, mime_type=mime_type)

    def digest_conversation(
        self,
        title: str,
        content: Optional[str] = None,
        raw_text: Optional[str] = None,
        participants: Optional[Union[List[str], str]] = None,
        date: Optional[str] = None,
        tags: Optional[Union[List[str], str]] = None,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Decomposes a dialogue/meeting into structured insights, concepts, entities, and flashcards."""
        today = date or datetime.date.today().isoformat()
        clean_title = title.strip() or "Untitled Conversation"
        clean_slug = re.sub(r'[^\w\-]', '-', clean_title.lower()).strip('-')[:60]
        if not clean_slug:
            clean_slug = f"conversation-{today}"

        conv_content = content or raw_text or ""
        
        if isinstance(tags, list):
            conv_tags = tags
        elif isinstance(tags, str):
            conv_tags = [t.strip() for t in tags.split(",") if t.strip()]
        else:
            conv_tags = ["Discussion", "Meeting", "Research"]

        if isinstance(participants, list):
            conv_participants = participants
        elif isinstance(participants, str):
            conv_participants = [p.strip() for p in participants.split(",") if p.strip()]
        else:
            conv_participants = ["Collaborators"]

        inferred_domain = domain or "Computer Science & AI"

        # 1. Save immutable raw record
        raw_conv_dir = self.raw_sources_dir / "conversations"
        raw_conv_dir.mkdir(parents=True, exist_ok=True)
        raw_file = raw_conv_dir / f"{clean_slug}.md"
        raw_file.write_text(
            f"# {clean_title}\n\n**Date**: {today}\n**Participants**: {', '.join(conv_participants)}\n\n## Content\n{conv_content}",
            encoding="utf-8"
        )

        # 2. Prompt LLM to analyze discourse and extract knowledge
        prompt = f"""You are a master academic research analyst, cognitive scribe, and knowledge graph architect.
Analyze the following conversation / meeting notes and extract structured knowledge following Karpathy's LLM-Wiki architecture.
Target Technical Domain: {inferred_domain}
Conversation Title: {clean_title}
Participants: {', '.join(conv_participants)}
Date: {today}

Conversation Transcript / Notes:
{conv_content[:12000]}

Extract and return strictly valid JSON with this exact schema:
{{
  "title": "{clean_title}",
  "summary": "Executive summary of the discussion, core thesis, and technical decisions reached.",
  "insights": [
    "Insight 1 (key technical realization or novel perspective)",
    "Insight 2"
  ],
  "action_items": [
    "Action item 1 (follow-up experiment, paper to read, verification task)",
    "Action item 2"
  ],
  "concepts": [
    {{
      "slug": "kebab-case-concept-slug",
      "title": "Concept Title",
      "domain": "{inferred_domain}",
      "system": "Sub-domain or module name",
      "tags": ["tag1", "tag2"],
      "summary": "Crisp one-sentence summary of the theoretical mechanism or concept.",
      "content": "Deep mathematical/mechanistic explanation with explicit architectural principles and traps discussed in the meeting."
    }}
  ],
  "entities": [
    {{
      "slug": "entity-slug",
      "title": "Entity Name",
      "category": "Tool | Library | Algorithm | Model | Benchmark",
      "high_yield_notes": "Key technical notes on how this entity relates to the discussion."
    }}
  ],
  "differentials": [
    {{
      "slug": "comp-vs-comp",
      "title": "A vs B Comparison",
      "summary": "Discriminant comparison of trade-offs debated during the conversation.",
      "content": "| Feature | A | B |\\n|---|---|---|\\n| Trade-off | ... | ... |"
    }}
  ],
  "flashcards": [
    {{
      "front": "Cloze prompt testing a critical pearl from the conversation: e.g. In narrow baselines, 3DGS overfits as {{{{c1::planar floater artifacts}}}}.",
      "back": "Key reasoning from discussion."
    }}
  ]
}}"""

        try:
            digested = self.llm.generate_json(prompt)
        except Exception:
            # Fallback heuristic digest
            digested = {
                "title": clean_title,
                "summary": f"Discussion regarding {clean_title} covering core technical methodologies and next steps.",
                "insights": ["Discussion focused on theoretical formulation and practical implementation boundaries."],
                "action_items": ["Review discussed formulations and reproduce benchmark outcomes."],
                "concepts": [],
                "entities": [],
                "differentials": [],
                "flashcards": []
            }

        # 3. Create Master Conversation Document in wiki/conversations/
        conv_wiki_dir = self.wiki_dir / "conversations"
        conv_wiki_dir.mkdir(parents=True, exist_ok=True)
        conv_file = conv_wiki_dir / f"{clean_slug}.md"

        insights_md = "\n".join([f"- **Key Insight**: {ins}" for ins in digested.get("insights", [])])
        actions_md = "\n".join([f"- [ ] {act}" for act in digested.get("action_items", [])])
        
        related_links = []
        for c in digested.get("concepts", []):
            related_links.append(f"[[concepts/{c['slug']}|{c['title']}]]")
        for e in digested.get("entities", []):
            related_links.append(f"[[entities/{e['slug']}|{e['title']}]]")
        for d in digested.get("differentials", []):
            related_links.append(f"[[differentials/{d['slug']}|{d['title']}]]")
        links_str = ", ".join(related_links) if related_links else "None extracted"

        tags_str = ", ".join(conv_tags)
        participants_str = ", ".join(conv_participants)

        master_content = f"""---
title: "Conversation: {clean_title}"
domain: "{inferred_domain}"
system: "Discourse & Meetings"
course: "Conversations"
category: conversations
tags: [{tags_str}]
participants: [{participants_str}]
date: {today}
source: "Conversation Transcript"
last_compiled: {today}
---

# Conversation: {clean_title}

> **Executive Summary**: {digested.get("summary", "Technical discussion and conceptual consultation.")}

## Discussion Context & Metadata
- **Date**: `{today}`
- **Participants**: `{participants_str}`
- **Technical Domain**: `{inferred_domain}`
- **Compounded Synapses**: {links_str}

## Key Realizations & Strategic Insights
{insights_md or "- Detailed technical nuances recorded in transcript below."}

## Action Items & Research Follow-ups
{actions_md or "- [ ] Review discussion points and compound findings into concept pages."}

---

## Annotated Transcript & Notes
{conv_content}

---
*Captured and digested into Paideia Genesis Living Brain on {today}*
"""
        conv_file.write_text(master_content, encoding="utf-8")
        self.indexer.index_file(conv_file)

        # 4. Compound extracted concepts
        concepts_dir = self.wiki_dir / "concepts"
        concepts_dir.mkdir(parents=True, exist_ok=True)
        compiled_concepts = []
        for c in digested.get("concepts", []):
            c_slug = c.get("slug") or re.sub(r'[^\w\-]', '-', c.get("title", "concept").lower()).strip('-')
            c_file = concepts_dir / f"{c_slug}.md"
            c_tags = c.get("tags", []) + ["From-Conversation", clean_slug]
            c_content = f"""---
title: "{c.get('title', c_slug)}"
domain: "{c.get('domain', inferred_domain)}"
system: "{c.get('system', 'Deep Learning & AI')}"
course: "Deep Learning & Vision"
tags: [{', '.join(c_tags)}]
source: "Conversation: {clean_title}"
last_compiled: {today}
---

# {c.get('title', c_slug)}

> **Core Summary**: {c.get('summary', '')}

{c.get('content', '')}

---
*Derived from conversation: [[conversations/{clean_slug}|{clean_title}]]*
"""
            c_file.write_text(c_content, encoding="utf-8")
            self.indexer.index_file(c_file)
            compiled_concepts.append(c_slug)

        # 5. Compound extracted entities
        entities_dir = self.wiki_dir / "entities"
        entities_dir.mkdir(parents=True, exist_ok=True)
        compiled_entities = []
        for e in digested.get("entities", []):
            e_slug = e.get("slug") or re.sub(r'[^\w\-]', '-', e.get("title", "entity").lower()).strip('-')
            e_file = entities_dir / f"{e_slug}.md"
            e_content = f"""---
title: "{e.get('title', e_slug)}"
category: "{e.get('category', 'Tool')}"
domain: "{inferred_domain}"
source: "Conversation: {clean_title}"
last_compiled: {today}
---

# {e.get('title', e_slug)}

> **Entity Classification**: `{e.get('category', 'Technical Entity')}`

### Notes from Discussion
{e.get('high_yield_notes', '')}

---
*Mentioned in: [[conversations/{clean_slug}|{clean_title}]]*
"""
            e_file.write_text(e_content, encoding="utf-8")
            self.indexer.index_file(e_file)
            compiled_entities.append(e_slug)

        # 6. Compound extracted differentials
        diffs_dir = self.wiki_dir / "differentials"
        diffs_dir.mkdir(parents=True, exist_ok=True)
        compiled_differentials = []
        for d in digested.get("differentials", []):
            d_slug = d.get("slug") or re.sub(r'[^\w\-]', '-', d.get("title", "diff").lower()).strip('-')
            d_file = diffs_dir / f"{d_slug}.md"
            d_content = f"""---
title: "{d.get('title', d_slug)}"
domain: "{inferred_domain}"
source: "Conversation: {clean_title}"
last_compiled: {today}
---

# {d.get('title', d_slug)}

> **Comparative Summary**: {d.get('summary', '')}

{d.get('content', '')}

---
*Debated in: [[conversations/{clean_slug}|{clean_title}]]*
"""
            d_file.write_text(d_content, encoding="utf-8")
            self.indexer.index_file(d_file)
            compiled_differentials.append(d_slug)

        # 7. Stage active recall flashcards
        staged_cards = []
        for card in digested.get("flashcards", []):
            front = card.get("front", "").strip()
            if not front:
                continue
            card_obj = {
                "type": "cloze",
                "text": front,
                "pearl": card.get("back", f"Discussion pearl from {clean_title}"),
                "tags": conv_tags + [clean_slug, "ConversationPearl"],
                "source": f"Conversation: {clean_slug}"
            }
            self.anki_manager.add_card(card_obj)
            staged_cards.append(front[:40])

        # 8. Log journal entry
        with open(self.wiki_dir / "log.md", "a", encoding="utf-8") as f:
            f.write(
                f"\n## [{today}] conversation_digest | Digested `{clean_title}` "
                f"({len(compiled_concepts)} concepts, {len(compiled_entities)} entities, "
                f"{len(compiled_differentials)} diffs, {len(staged_cards)} cards)\n"
            )

        return {
            "success": True,
            "title": clean_title,
            "slug": clean_slug,
            "rel_path": f"conversations/{clean_slug}.md",
            "summary": digested.get("summary", ""),
            "insights_count": len(digested.get("insights", [])),
            "action_items_count": len(digested.get("action_items", [])),
            "concepts_compiled": len(compiled_concepts),
            "entities_compiled": len(compiled_entities),
            "differentials_compiled": len(compiled_differentials),
            "flashcards_staged": len(staged_cards),
            "staged_flashcards": len(staged_cards)
        }
