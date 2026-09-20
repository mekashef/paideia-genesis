"""Socratic Living Teacher Engine: Generates clinical drills, diagnoses reasoning errors, and updates the wiki."""
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import WIKI_DIR
from src.llm.client import get_llm_client, BaseLLMClient
from src.tutor.student_profile import StudentProfile
from src.wiki.indexer import WikiIndexer

class SocraticTeacher:
    def __init__(self, llm_client: Optional[BaseLLMClient] = None, wiki_dir: Path = WIKI_DIR):
        self.wiki_dir = wiki_dir
        self.llm = llm_client or get_llm_client()
        self.student_profile = StudentProfile(wiki_dir / "student_profile")
        self.indexer = WikiIndexer(wiki_dir)

    def generate_adaptive_vignette(self) -> Dict[str, Any]:
        """Generates a board-style clinical vignette prioritizing upcoming exam topics and weak areas."""
        schedule = self.student_profile.get_schedule()
        mastery = self.student_profile.get_mastery()
        
        # Identify weakest system
        weakest_system = min(mastery.items(), key=lambda x: x[1])[0]
        upcoming_topics = [t["name"] for t in schedule.get("topics", [])]
        
        # Search wiki for relevant context
        search_results = self.indexer.search(f"{weakest_system} {upcoming_topics[0]}", limit=3)
        wiki_snippets = "\n".join([f"- {r['title']}: {r['match_snippet']}" for r in search_results])

        prompt = f"""You are an expert Medical School Board Exam Tutor (USMLE Step 1 / Step 2 CK).
Generate a challenging clinical vignette tailored for this student.

Student Context:
- Upcoming Exam: {schedule.get('target_exam')} in {schedule.get('days_remaining')} days
- Weakest Organ System: {weakest_system} (Mastery: {mastery.get(weakest_system)}%)
- Priority Topics: {', '.join(upcoming_topics[:2])}
- Relevant Wiki Knowledge:
{wiki_snippets}

Requirements:
1. Create a realistic multi-step clinical vignette (patient age, acute presentation, vitals, physical exam, labs/imaging).
2. Ask a question testing pathophysiological mechanism or critical pharmacologic decision (with a classic board trap).
3. Provide 4 options (A, B, C, D).
4. Specify the correct option, complete rationale, and a high-yield learning pearl.

Respond strictly in JSON format with keys: vignette_id, topic, stem, options (array with id and text), correct_option, explanation, learning_pearl, high_yield_tags."""

        return self.llm.generate_json(prompt, system_prompt="You are a clinical medicine educator.")

    def evaluate_response(self, vignette: Dict[str, Any], selected_option_id: str, student_reasoning: str = "") -> Dict[str, Any]:
        """Evaluates student's choice and reasoning, provides Socratic diagnosis, updates wiki and profile."""
        correct_id = vignette.get("correct_option")
        is_correct = (selected_option_id.strip().upper() == correct_id.strip().upper())
        topic = vignette.get("topic", "Cardiovascular")

        prompt = f"""You are a Socratic Medical Educator.
Evaluate this student's response to a clinical vignette.

Vignette Stem:
{vignette.get('stem')}

Options:
{json.dumps(vignette.get('options', []))}

Correct Option: {correct_id}
Student Selected: {selected_option_id}
Student's Stated Reasoning: {student_reasoning if student_reasoning else "No reasoning provided."}

Task:
1. Determine if student was correct ({is_correct}).
2. If incorrect, classify error into one of: 'MECHANISM_GAP', 'DISCRIMINATOR_CONFUSION', 'CLINICAL_CONTRAINDICATION', 'READING_SLIP'.
3. Provide a Socratic critique (ask a targeted question that helps them discover why their choice was flawed, rather than just spoon-feeding the answer).
4. Provide the physiological mechanism explanation.
5. Provide a candidate high-yield Anki flashcard (cloze deletion format {{c1::...}}).

Respond strictly in JSON with keys: is_correct (bool), error_taxonomy, socratic_critique, mechanism_explanation, remediation_action, anki_card_candidate (with front and back)."""

        evaluation = self.llm.generate_json(prompt, system_prompt="You are a Socratic clinical educator.")
        evaluation["is_correct"] = is_correct

        # 1. Update Student Profile
        error_type = evaluation.get("error_taxonomy", "REASONING_GAP")
        details = evaluation.get("mechanism_explanation", "Student missed discriminator.")
        self.student_profile.record_attempt(topic, is_correct, error_type=error_type, details=details)

        # 2. If incorrect, compile to Medical Wiki exam_traps/
        if not is_correct:
            self._record_wiki_trap(vignette, selected_option_id, evaluation)

        return evaluation

    def _record_wiki_trap(self, vignette: Dict[str, Any], selected_id: str, evaluation: Dict[str, Any]):
        """Persists the student's missed concept into the LLM-Wiki under exam_traps/."""
        traps_dir = self.wiki_dir / "exam_traps"
        traps_dir.mkdir(parents=True, exist_ok=True)
        
        slug = f"trap-{vignette.get('vignette_id', 'drill')}-{selected_id.lower()}"
        trap_file = traps_dir / f"{slug}.md"

        trap_content = f"""---
title: Exam Trap - {vignette.get('topic', 'Clinical Medicine')}
error_taxonomy: {evaluation.get('error_taxonomy', 'CLINICAL_CONTRAINDICATION')}
date_logged: {datetime.date.today().isoformat()}
tags: [board-trap, student-error]
---

# Board Exam Trap: {vignette.get('topic')}

### Clinical Scenario
{vignette.get('stem')}

### Student Misconception
- Selected: **Option {selected_id}**
- Socratic Diagnosis: {evaluation.get('socratic_critique')}

### Correct Physiological Mechanism
{evaluation.get('mechanism_explanation')}

### Remediation Flashcard Generated
> **Prompt**: {evaluation.get('anki_card_candidate', {}).get('front', '')}
> **Answer**: {evaluation.get('anki_card_candidate', {}).get('back', '')}
"""
        trap_file.write_text(trap_content, encoding="utf-8")
        self.indexer.index_file(trap_file)
        
        # Log to log.md
        log_file = self.wiki_dir / "log.md"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n## [{datetime.date.today().isoformat()}] error_diagnostic | Missed `{slug}` -> Compiled to exam_traps/ and queued flashcard\n")
