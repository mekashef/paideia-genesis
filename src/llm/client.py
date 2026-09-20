"""Unified multi-provider LLM gateway supporting Gemini, OpenAI-compatible (home GPU), and Mock."""
import json
import logging
from typing import Dict, Any, List, Optional
import requests
from src.config import (
    LLM_PROVIDER,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL
)

logger = logging.getLogger("paideia_genesis.llm")

class BaseLLMClient:
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        raise NotImplementedError

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        resp = self.generate(prompt, system_prompt=system_prompt, temperature=0.1)
        # Attempt to clean code block backticks if present
        clean = resp.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return json.loads(clean.strip())

class OpenAICompatibleClient(BaseLLMClient):
    """Client for local/remote OpenAI-compatible APIs (Ollama, vLLM, LM Studio on home GPUs)."""
    def __init__(self, base_url: str = OPENAI_BASE_URL, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI-compatible request failed: {e}")
            raise

class GeminiLLMClient(BaseLLMClient):
    """Client for Google Gemini API."""
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Directive: {system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow your directives."}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temperature}
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

class MockMedicalLLMClient(BaseLLMClient):
    """Deterministic medical intelligence simulation for testing and offline pilot demonstrations."""
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        prompt_lower = prompt.lower()
        if "ingest" in prompt_lower or "compile" in prompt_lower or "extract" in prompt_lower:
            return json.dumps({
                "concepts": [
                    {
                        "slug": "acute-decompensated-heart-failure",
                        "title": "Acute Decompensated Heart Failure (ADHF)",
                        "system": "Cardiovascular",
                        "tags": ["cardiology", "hemodynamics", "pharmacology", "board-trap"],
                        "summary": "Severe exacerbation of cardiac dysfunction characterized by pulmonary congestion, elevated capillary wedge pressure, and dyspnea.",
                        "content": "### Pathophysiology\nADHF results from rapid elevation of left ventricular filling pressures leading to pulmonary interstitial and alveolar edema. Hallmark symptoms include orthopnea, paroxysmal nocturnal dyspnea, and bilateral crackles.\n\n### Pharmacotherapy\n- **Loop Diuretics (IV Furosemide)**: Cornerstone for volume overload. Works by inhibiting the Na+/K+/2Cl- cotransporter in the thick ascending limb of the loop of Henle.\n- **Vasodilators (Nitroglycerin, Nitroprusside)**: Reduce preload and afterload.\n- **Inotropes (Dobutamine, Milrinone)**: Indicated in cardiogenic shock.\n\n### Board Exam Traps & Pitfalls\n> [!CAUTION]\n> **Beta-Blocker Administration in Acute Decompensation**:\n> Although beta-blockers (carvedilol, metoprolol succinate) improve long-term mortality in stable chronic HFrEF, initiating or up-titrating beta-blockers during an **acute decompensation** is contraindicated because acute negative inotropic effects precipitate cardiogenic shock! Continue low dose only if already chronic, never start acute.\n\nRelated: [[loop-diuretics]], [[beta-blockers-in-hf]], [[renin-angiotensin-aldosterone-system]]."
                    },
                    {
                        "slug": "loop-diuretics",
                        "title": "Loop Diuretics (Furosemide, Bumetanide, Torsemide)",
                        "system": "Renal & Cardiovascular",
                        "tags": ["pharmacology", "renal", "electrolytes"],
                        "summary": "Potent natriuretic agents acting on the thick ascending limb of Henle.",
                        "content": "### Mechanism of Action\nInhibit the apical **Na+/K+/2Cl- cotransporter (NKCC2)** in the thick ascending limb. Abolish the hypertonic medullary gradient, leading to profound excretion of water, sodium, potassium, chloride, calcium, and magnesium.\n\n### Adverse Effects (Mnemonic: OH DANG!)\n- **O**totoxicity (especially with aminoglycosides)\n- **H**ypokalemia & Hypomagnesemia\n- **D**ehydration / Hypovolemia\n- **A**llergy (Sulfa drugs - except Ethacrynic acid)\n- **N**ephritis (interstitial)\n- **G**out (hyperuricemia from competitive uric acid reabsorption)\n\nRelated: [[acute-decompensated-heart-failure]], [[renin-angiotensin-aldosterone-system]]."
                    }
                ],
                "entities": [
                    {
                        "slug": "furosemide",
                        "title": "Furosemide",
                        "category": "Loop Diuretic",
                        "high_yield_notes": "First-line IV therapy in acute pulmonary edema from heart failure. Monitor K+ and Mg2+."
                    },
                    {
                        "slug": "carvedilol",
                        "title": "Carvedilol",
                        "category": "Non-selective Beta + Alpha-1 Blocker",
                        "high_yield_notes": "Mortality benefit in stable chronic HFrEF. Contraindicated in acute decompensation / pulmonary edema."
                    }
                ],
                "differentials": [
                    {
                        "slug": "loop-vs-thiazide-diuretics",
                        "title": "Loop vs Thiazide Diuretics Comparison",
                        "summary": "Key physiological discriminators between thick ascending limb and distal convoluted tubule diuretics.",
                        "content": "| Feature | Loop Diuretics (Furosemide) | Thiazides (HCTZ, Chlorthalidone) |\n|---|---|---|\n| **Site of Action** | Thick Ascending Limb (NKCC2) | Distal Convoluted Tubule (NCC) |\n| **Efficacy** | High Ceiling (Potent) | Moderate |\n| **Urinary Calcium** | **Hypocalcemia** (Loops lose Ca2+) | **Hypercalcemia** (Thiazides save Ca2+) |\n| **Primary Clinical Role** | Edema, ADHF, fluid overload | Essential Hypertension, recurrent Ca2+ stones |"
                    }
                ]
            })

        if "evaluate" in prompt_lower or "diagnostic" in prompt_lower or "student selected" in prompt_lower:
            # Socratic feedback simulation
            return json.dumps({
                "is_correct": False,
                "error_taxonomy": "CLINICAL_CONTRAINDICATION",
                "socratic_critique": "You selected option A. While your choice of IV Furosemide for acute preload reduction was spot on, adding or initiating Carvedilol right now is a classic board trap! What physiological effect does a beta-blocker exert on ventricular contractility in a failing heart that is dependent on sympathetic tone to maintain cardiac output?",
                "mechanism_explanation": "Beta-blockers have immediate negative inotropic and chronotropic effects. In acute pulmonary edema, the patient's heart is barely compensating using catecholamine drive. Blocking beta-1 receptors acutely removes that sympathetic crutch, leading to sudden cardiovascular collapse.",
                "remediation_action": "Updating student profile with misconception: 'Initiated beta-blocker during acute decompensation'. Added warning to wiki concept [[acute-decompensated-heart-failure]].",
                "anki_card_candidate": {
                    "front": "Why is initiating or uptitrating a beta-blocker (e.g., carvedilol) {{c1::contraindicated}} during {{c2::acute decompensated heart failure}}?",
                    "back": "Beta-blockers exert acute {{c1::negative inotropic}} effects, which blunt sympathetic compensation and can precipitate {{c2::cardiogenic shock}}."
                }
            })

        if "vignette" in prompt_lower or "generate a challenging" in prompt_lower:
            return json.dumps({
                "vignette_id": "cardio-vignette-001",
                "topic": "Cardiovascular Pharmacology & Heart Failure",
                "stem": "A 64-year-old male with a history of hypertension and ischemic cardiomyopathy presents to the emergency department with acute shortness of breath that awoke him from sleep. He has been sleeping on three pillows for the past two weeks. Physical examination reveals blood pressure 158/94 mmHg, heart rate 104/min, jugular venous distention to the angle of the jaw, bilateral coarse inspiratory crackles halfway up both lung fields, and 3+ pitting edema to the mid-shins. Chest radiography confirms pulmonary edema with cephalization of pulmonary vessels and bilateral pleural effusions.\n\nWhich of the following represents the most appropriate immediate pharmacotherapy, and which medication is strictly contraindicated to initiate at this juncture?",
                "options": [
                    {"id": "A", "text": "Initiate IV Furosemide; initiate Oral Carvedilol"},
                    {"id": "B", "text": "Initiate IV Furosemide; hold/do not initiate Beta-Blockers acutely"},
                    {"id": "C", "text": "Initiate IV Digoxin; initiate Oral Lisinopril"},
                    {"id": "D", "text": "Initiate IV Metoprolol tartrate; initiate Spironolactone"}
                ],
                "correct_option": "B",
                "explanation": "The patient is in Acute Decompensated Heart Failure (ADHF) with severe pulmonary edema. Immediate treatment requires IV loop diuretics (Furosemide) to reduce preload and alleviate pulmonary capillary hydrostatic pressure. Initiating beta-blockers (like Carvedilol or Metoprolol) during an acute decompensated state is strictly contraindicated due to negative inotropy, which can precipitate cardiogenic shock.",
                "learning_pearl": "Remember the board pearl: Beta-blockers SAVE lives in stable chronic HFrEF, but KILL in acute pulmonary edema decompensation.",
                "high_yield_tags": ["Heart Failure", "Pharmacology", "Contraindications", "USMLE Step 1"]
            })
        if "synthesize" in prompt_lower or "concept page" in prompt_lower or "raw material" in prompt_lower or "sglt2" in prompt_lower:
            return json.dumps({
                "slug": "sglt2-inhibitors-in-heart-failure",
                "title": "SGLT2 Inhibitors (Empagliflozin, Dapagliflozin)",
                "system": "Cardiovascular & Renal",
                "summary": "Sodium-glucose cotransporter-2 inhibitors that reduce cardiovascular mortality and heart failure hospitalizations.",
                "content": "### Mechanism of Action\nSGLT2 inhibitors block sodium-glucose reabsorption in the proximal convoluted tubule.\n\n### Clinical Trials & Pearls\nDAPA-HF and EMPEROR-Reduced demonstrated significant mortality benefits.\n\nRelated: [[concepts/loop-diuretics]], [[concepts/acute-decompensated-heart-failure]].",
                "candidate_card": {
                    "front": "What metabolic complication is uniquely associated with {{c1::SGLT2 inhibitors}}?",
                    "back": "{{c1::Euglycemic Diabetic Ketoacidosis (euDKA)}}",
                    "pearl": "Normal blood glucose (< 250 mg/dL) with profound anion-gap metabolic acidosis."
                }
            })

        if (system_prompt and "json" in system_prompt.lower()) or "json" in prompt_lower or "question" in prompt_lower:
            return json.dumps({
                "status": "success",
                "summary": "Mock medical synthesis completed successfully.",
                "data": {"result": "ok"}
            })

        return "Medical intelligence analysis complete."

def get_llm_client() -> BaseLLMClient:
    """Factory to instantiate the appropriate LLM client based on configuration."""
    provider = LLM_PROVIDER.lower()
    if provider == "gemini" and GEMINI_API_KEY:
        try:
            return GeminiLLMClient()
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini client: {e}. Falling back to Mock.")
    elif provider == "openai_compatible" and OPENAI_BASE_URL:
        try:
            return OpenAICompatibleClient()
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI-compatible client: {e}. Falling back to Mock.")
            
    return MockMedicalLLMClient()
