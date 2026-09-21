"""Socratic Living Teacher Engine: Generates multi-discipline drills, diagnoses reasoning errors, and updates the wiki.
Supports user guidance, engineering dilemmas, systems trade-offs, research edge-cases, and medical vignettes.
"""
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import WIKI_DIR
from src.llm.client import get_llm_client, BaseLLMClient
from src.llm.jev_client import jev_client
from src.tutor.student_profile import StudentProfile
from src.wiki.indexer import WikiIndexer

class SocraticTeacher:
    def __init__(self, llm_client: Optional[BaseLLMClient] = None, wiki_dir: Path = WIKI_DIR):
        self.wiki_dir = wiki_dir
        self.llm = llm_client or get_llm_client()
        self.student_profile = StudentProfile(wiki_dir / "student_profile")
        self.indexer = WikiIndexer(wiki_dir)

    def generate_adaptive_vignette(
        self,
        topic: Optional[str] = None,
        guidance: Optional[str] = None,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates a challenging problem dilemma, systems scenario, or board vignette.
        Allows explicit user topic guidance or automatically adapts to the learner's weakest areas.
        """
        schedule = self.student_profile.get_schedule()
        mastery = self.student_profile.get_mastery()
        
        # 1. Determine active topic and domain
        if topic and topic.strip():
            active_topic = topic.strip()
            active_domain = domain or ("Computer Science" if any(k in active_topic.lower() for k in ["raft", "paxos", "consensus", "storage", "lsm", "cache", "concurrency", "epoll"]) else "General")
        else:
            # Auto-adapt to weakest domain in profile
            weakest_system = min(mastery.items(), key=lambda x: x[1])[0] if mastery else "General"
            upcoming_topics = [t["name"] for t in schedule.get("topics", [])]
            active_topic = upcoming_topics[0] if upcoming_topics else weakest_system
            active_domain = domain or ("Computer Science" if any(k in active_topic.lower() for k in ["raft", "consensus", "storage", "concurrency", "distributed"]) else "Medicine")

        # 2. Search wiki for relevant context
        search_results = self.indexer.search(f"{active_topic}", limit=3)
        wiki_snippets = "\n".join([f"- {r['title']}: {r['match_snippet']}" for r in search_results]) if search_results else "- Standard foundational principles."

        user_guidance_clause = f"\nUser Focus & Guidance:\n{guidance}\n" if guidance else ""

        # 3. Construct domain-appropriate prompt
        if active_domain == "Computer Science" or any(k in active_topic.lower() for k in ["distributed", "consensus", "raft", "storage", "lsm", "concurrency", "epoll", "cache"]):
            prompt = f"""You are an elite Principal Systems Architect & CS Faculty Socratic Tutor.
Generate a challenging, real-world technical dilemma or system design problem for this learner.

Learner Context:
- Target Curriculum / Milestone: {schedule.get('target_exam')}
- Focus Topic: {active_topic}
{user_guidance_clause}
- Relevant Knowledge Base:
{wiki_snippets}

Requirements:
1. Create a realistic multi-step technical scenario (system architecture, failure mode, performance bottleneck, concurrency bug, or distributed partition).
2. Pose a question testing the underlying mechanism, theoretical invariant, or critical trade-off (incorporating a classic anti-pattern or trap).
3. Provide 4 options (A, B, C, D).
4. Specify the correct option, complete rationale, and a high-yield learning insight/pearl.

Respond strictly in JSON format with keys: vignette_id, topic, domain, stem, options (array with id and text), correct_option, explanation, learning_pearl, high_yield_tags."""
        else:
            prompt = f"""You are an expert Academic Tutor & Socratic Educator.
Generate a challenging problem dilemma or clinical vignette tailored for this learner.

Learner Context:
- Target Exam / Milestone: {schedule.get('target_exam')} in {schedule.get('days_remaining', 0)} days
- Focus Topic: {active_topic}
{user_guidance_clause}
- Relevant Knowledge Base:
{wiki_snippets}

Requirements:
1. Create a realistic multi-step problem scenario or clinical case.
2. Ask a question testing foundational mechanisms, discriminant features, or critical decisions (with a classic trap).
3. Provide 4 options (A, B, C, D).
4. Specify the correct option, complete rationale, and a high-yield learning pearl.

Respond strictly in JSON format with keys: vignette_id, topic, domain, stem, options (array with id and text), correct_option, explanation, learning_pearl, high_yield_tags."""

        res = self.llm.generate_json(prompt, system_prompt="You are an adaptive Socratic living educator.")
        if not isinstance(res, dict):
            res = {}
        if not res.get("domain"):
            res["domain"] = active_domain
        if not res.get("topic"):
            res["topic"] = active_topic
        return res

    def evaluate_response(
        self,
        vignette: Dict[str, Any],
        selected_option_id: str,
        student_reasoning: str = ""
    ) -> Dict[str, Any]:
        """Evaluates student's choice and reasoning, provides Socratic diagnosis, updates wiki and profile."""
        correct_id = vignette.get("correct_option")
        is_correct = (selected_option_id.strip().upper() == correct_id.strip().upper())
        topic = vignette.get("topic", "Systems Engineering")
        domain = vignette.get("domain", "General")

        # Step 1: Jev System 1 Diagnostic Triage (<100ms fast, typed decision)
        jev_diag = jev_client.diagnose_problem_reasoning(vignette, selected_option_id, student_reasoning, domain=domain)
        tax_ans = jev_diag.answers.get("error_taxonomy", {})
        jev_error_type = tax_ans.get("choice", "REASONING_GAP")
        jev_confidence = tax_ans.get("confidence", 0.9)
        jev_trap_prob = jev_diag.answers.get("board_trap_triggered", {}).get("noul", 0.0)
        jev_trap_triggered = jev_trap_prob > 0.5
        jev_soundness = jev_diag.answers.get("reasoning_soundness", {}).get("score", 1)

        # Step 2: System 2 Socratic dialogue generation (guided by Jev's diagnosis)
        prompt = f"""You are a Socratic Living Teacher and Cognitive Guide.
Evaluate this student's response to the technical problem or vignette.

Problem Stem:
{vignette.get('stem')}

Options:
{json.dumps(vignette.get('options', []))}

Correct Option: {correct_id}
Student Selected: {selected_option_id}
Student's Stated Reasoning: {student_reasoning if student_reasoning else "No reasoning provided."}

System 1 (Jev Decision Engine) Diagnostic Triage:
- Classified Misconception: {jev_error_type} (Confidence: {int(jev_confidence * 100)}%)
- Trap / Anti-Pattern Triggered: {jev_trap_triggered} (p={jev_trap_prob})
- Mechanistic Reasoning Depth: Level {jev_soundness}/2

Task:
1. Student correctness is {is_correct}.
2. Use error taxonomy: '{jev_error_type}'.
3. Provide a Socratic critique (ask a targeted probe that guides them to uncover why their reasoning led to this specific misconception).
4. Provide the concise underlying mechanism and principles explanation.
5. Provide a candidate high-yield Anki flashcard (cloze deletion format {{c1::...}}).

Respond strictly in JSON with keys: is_correct (bool), error_taxonomy, socratic_critique, mechanism_explanation, remediation_action, anki_card_candidate (with front and back)."""

        evaluation = self.llm.generate_json(prompt, system_prompt="You are a Socratic educator and technical tutor.")
        evaluation["is_correct"] = is_correct
        if not evaluation.get("error_taxonomy") or evaluation.get("error_taxonomy") == "REASONING_GAP":
            evaluation["error_taxonomy"] = jev_error_type

        # Attach Jev System 1 telemetry to evaluation
        evaluation["jev_system_one"] = {
            "active": True,
            "latency_ms": jev_diag.latency_ms,
            "model": jev_diag.model,
            "error_taxonomy": jev_error_type,
            "confidence": jev_confidence,
            "board_trap_triggered": jev_trap_triggered,
            "reasoning_soundness": jev_soundness
        }

        # 1. Update Student Profile
        error_type = evaluation.get("error_taxonomy", jev_error_type)
        details = evaluation.get("mechanism_explanation", "Student missed core discriminator.")
        self.student_profile.record_attempt(topic, is_correct, error_type=error_type, details=details)

        # 2. If incorrect, compile to Wiki exam_traps/
        if not is_correct:
            self._record_wiki_trap(vignette, selected_option_id, evaluation)

        return evaluation

    def _record_wiki_trap(self, vignette: Dict[str, Any], selected_id: str, evaluation: Dict[str, Any]):
        """Persists the student's missed concept into the LLM-Wiki under exam_traps/."""
        traps_dir = self.wiki_dir / "exam_traps"
        traps_dir.mkdir(parents=True, exist_ok=True)
        
        slug = f"trap-{vignette.get('vignette_id', 'drill')}-{selected_id.lower()}"
        trap_file = traps_dir / f"{slug}.md"
        topic = vignette.get('topic', 'Core Concept')

        trap_content = f"""---
title: Pitfall Trap - {topic}
domain: {vignette.get('domain', 'General')}
error_taxonomy: {evaluation.get('error_taxonomy', 'CRITICAL_PITFALL')}
date_logged: {datetime.date.today().isoformat()}
tags: [trap, misconception, student-error]
---

# Concept Trap / Anti-Pattern: {topic}

### Problem Scenario
{vignette.get('stem')}

### Student Misconception
- Selected: **Option {selected_id}**
- Socratic Diagnosis: {evaluation.get('socratic_critique')}

### Underlying Correct Mechanism
{evaluation.get('mechanism_explanation')}

### Remediation Flashcard Generated
> **Prompt**: {evaluation.get('anki_card_candidate', {}).get('front', '')}
> **Answer**: {evaluation.get('anki_card_candidate', {}).get('back', '')}
"""
        trap_file.write_text(trap_content, encoding="utf-8")
        self.indexer.index_file(trap_file)
        
        log_file = self.wiki_dir / "log.md"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n## [{datetime.date.today().isoformat()}] error_diagnostic | Missed `{slug}` -> Compiled to exam_traps/ and queued flashcard\n")
