"""Student and Learner Diagnostic Profile and Curriculum Tracker.
Supports dynamic multi-discipline mastery tracking across Engineering, Science, Research, and Medicine.
"""
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.config import WIKI_DIR

PROFILE_DIR = WIKI_DIR / "student_profile"

DEFAULT_SCHEDULE = {
    "current_block": "Active Research & Deep Learning / ML Engineering",
    "target_exam": "Deep Learning / ML Research & Engineering Milestone",
    "exam_date": (datetime.date.today() + datetime.timedelta(days=14)).isoformat(),
    "topics": [
        {"name": "Deep Learning Architectures & Transformer Attention", "priority": "CRITICAL"},
        {"name": "Distributed Training, Data & Pipeline Parallelism", "priority": "HIGH"},
        {"name": "Model Optimization, Quantization & KV Cache", "priority": "HIGH"},
        {"name": "Empirical Research & Benchmark Evaluation", "priority": "MEDIUM"}
    ]
}

DEFAULT_MASTERY = {
    "Deep Learning": 72.0,
    "Machine Learning": 75.0,
    "Distributed Training": 68.0,
    "Transformer Architectures": 70.0,
    "Model Optimization": 65.0,
    "Cardiovascular": 68.0,
    "Renal": 54.0,
    "Pharmacology": 62.0,
    "Distributed Systems": 65.0,
    "Storage Engines": 58.0
}

class StudentProfile:
    def __init__(self, profile_dir: Path = PROFILE_DIR):
        self.profile_dir = profile_dir
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_file = self.profile_dir / "knowledge_state.json"
        self.schedule_file = self.profile_dir / "schedule.json"
        self.misconceptions_file = self.profile_dir / "misconceptions.md"
        self._init_files()

    def _init_files(self):
        if not self.knowledge_file.exists():
            self.knowledge_file.write_text(json.dumps(DEFAULT_MASTERY, indent=2), encoding="utf-8")
        if not self.schedule_file.exists():
            self.schedule_file.write_text(json.dumps(DEFAULT_SCHEDULE, indent=2), encoding="utf-8")
        if not self.misconceptions_file.exists():
            self.misconceptions_file.write_text(
                "# Learner Misconceptions & Diagnostic Error Log\n\n"
                "Chronological ledger of diagnostic errors, reasoning slips, and anti-patterns.\n",
                encoding="utf-8"
            )

    def get_schedule(self) -> Dict[str, Any]:
        data = json.loads(self.schedule_file.read_text(encoding="utf-8"))
        exam_date = datetime.date.fromisoformat(data["exam_date"])
        today = datetime.date.today()
        days_left = max(0, (exam_date - today).days)
        data["days_remaining"] = days_left
        return data

    def update_schedule(self, schedule_data: Dict[str, Any]):
        self.schedule_file.write_text(json.dumps(schedule_data, indent=2), encoding="utf-8")

    def get_mastery(self) -> Dict[str, float]:
        return json.loads(self.knowledge_file.read_text(encoding="utf-8"))

    def record_attempt(self, topic: str, is_correct: bool, error_type: Optional[str] = None, details: Optional[str] = None):
        """Updates mastery scores and logs misconceptions if incorrect."""
        mastery = self.get_mastery()
        matched_system = None

        # Look for existing matching domain/system
        for sys in mastery.keys():
            if sys.lower() in topic.lower() or topic.lower() in sys.lower():
                matched_system = sys
                break

        # If not found, dynamically register new topic
        if not matched_system:
            if "Cardio" in topic:
                matched_system = "Cardiovascular"
            elif any(k in topic.lower() for k in ["raft", "consensus", "paxos", "distributed"]):
                matched_system = "Distributed Systems"
            elif any(k in topic.lower() for k in ["storage", "lsm", "btree", "disk"]):
                matched_system = "Storage Engines"
            else:
                matched_system = topic.strip()
                mastery[matched_system] = 60.0

        current = mastery.get(matched_system, 60.0)
        if is_correct:
            new_score = min(100.0, current + 4.0)
        else:
            new_score = max(20.0, current - 7.0)
            self._log_misconception(topic, error_type or "REASONING_GAP", details or "Missed critical discriminator.")

        mastery[matched_system] = round(new_score, 1)
        self.knowledge_file.write_text(json.dumps(mastery, indent=2), encoding="utf-8")

    def _log_misconception(self, topic: str, error_type: str, details: str):
        today = datetime.date.today().isoformat()
        entry = f"""
### [{today}] {topic}
- **Error Taxonomy**: `{error_type}`
- **Diagnostic Note**: {details}
"""
        with open(self.misconceptions_file, "a", encoding="utf-8") as f:
            f.write(entry)

    def get_profile_summary(self) -> Dict[str, Any]:
        schedule = self.get_schedule()
        mastery = self.get_mastery()
        misconceptions = self.misconceptions_file.read_text(encoding="utf-8")

        avg_mastery = sum(mastery.values()) / max(1, len(mastery))

        return {
            "schedule": schedule,
            "mastery": mastery,
            "readiness_score": round(avg_mastery, 1),
            "misconceptions_raw": misconceptions
        }
