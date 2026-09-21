"""Unified multi-provider LLM gateway supporting Gemini, OpenAI-compatible (home GPU), and Mock.
Supports universal knowledge synthesis across Engineering, Computer Science, Research, and Medicine.
"""
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
        # Clean code block backticks if present
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

class MockUniversalLLMClient(BaseLLMClient):
    """Deterministic universal intelligence simulation for testing and offline pilot demonstrations.
    Handles Computer Science, Systems Engineering, Mathematics, Physics, and Medicine.
    """
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        prompt_lower = prompt.lower()

        # 1. Ingestion / Knowledge compilation
        if ("ingest" in prompt_lower or "compile" in prompt_lower or "extract" in prompt_lower) and (
            "curriculum compiler" in prompt_lower
            or "extract and synthesize:" in prompt_lower
            or "source filename:" in prompt_lower
            or "raw course" in prompt_lower
            or "process the following raw" in prompt_lower
        ):
            if any(k in prompt_lower for k in ["raft", "paxos", "consensus", "distributed", "storage", "concurrency", "eecs", "6.033"]):
                return json.dumps({
                    "concepts": [
                        {
                            "slug": "raft-distributed-consensus",
                            "title": "Raft Distributed Consensus Protocol",
                            "domain": "Computer Science",
                            "system": "Distributed Systems",
                            "tags": ["consensus", "fault-tolerance", "etcd"],
                            "summary": "Decomposed consensus algorithm structuring safety into leader election and log replication.",
                            "content": "### Protocol Invariants\nOnly candidates with the most up-to-date logs can win elections. Leaders never overwrite their own logs.\n\nRelated: [[entities/etcd]], [[differentials/raft-vs-multi-paxos]]."
                        }
                    ],
                    "entities": [
                        {
                            "slug": "etcd",
                            "title": "etcd",
                            "category": "distributed-store",
                            "high_yield_notes": "Raft-backed key-value store coordinating Kubernetes cluster state."
                        }
                    ],
                    "differentials": [
                        {
                            "slug": "raft-vs-multi-paxos",
                            "title": "Raft vs Multi-Paxos",
                            "summary": "Trade-offs between strong leader invariants and gap reconciliation.",
                            "content": "| Feature | Raft | Multi-Paxos |\n|---|---|---|\n| Leader | Strong | Weak |\n| Gaps | Prohibited | Allowed |"
                        }
                    ]
                })

            # Default to medical compilation
            return json.dumps({
                "concepts": [
                    {
                        "slug": "acute-decompensated-heart-failure",
                        "title": "Acute Decompensated Heart Failure (ADHF)",
                        "system": "Cardiovascular",
                        "domain": "Medicine",
                        "tags": ["cardiology", "hemodynamics", "pharmacology", "board-trap"],
                        "summary": "Severe exacerbation of cardiac dysfunction characterized by pulmonary congestion, elevated capillary wedge pressure, and dyspnea.",
                        "content": "### Pathophysiology\nADHF results from rapid elevation of left ventricular filling pressures leading to pulmonary interstitial and alveolar edema.\n\n### Pharmacotherapy\n- **Loop Diuretics (IV Furosemide)**: Cornerstone for volume overload.\n\n### Board Exam Traps & Pitfalls\n> [!CAUTION]\n> **Beta-Blocker Administration in Acute Decompensation**:\n> Initiating beta-blockers acutely is contraindicated!\n\nRelated: [[loop-diuretics]], [[beta-blockers-in-hf]]."
                    },
                    {
                        "slug": "loop-diuretics",
                        "title": "Loop Diuretics (Furosemide, Bumetanide, Torsemide)",
                        "system": "Renal & Cardiovascular",
                        "domain": "Medicine",
                        "tags": ["pharmacology", "renal", "electrolytes"],
                        "summary": "Potent natriuretic agents acting on the thick ascending limb of Henle.",
                        "content": "### Mechanism of Action\nInhibit the apical **Na+/K+/2Cl- cotransporter (NKCC2)** in the thick ascending limb."
                    }
                ],
                "entities": [
                    {
                        "slug": "furosemide",
                        "title": "Furosemide",
                        "category": "Loop Diuretic",
                        "high_yield_notes": "First-line IV therapy in acute pulmonary edema from heart failure."
                    },
                    {
                        "slug": "carvedilol",
                        "title": "Carvedilol",
                        "category": "Beta-Blocker",
                        "high_yield_notes": "Contraindicated in acute decompensation."
                    }
                ],
                "differentials": [
                    {
                        "slug": "loop-vs-thiazide-diuretics",
                        "title": "Loop vs Thiazide Diuretics Comparison",
                        "summary": "Key physiological discriminators between thick ascending limb and distal convoluted tubule diuretics.",
                        "content": "| Feature | Loop Diuretics | Thiazides |\n|---|---|---|\n| Site | Thick Ascending Limb | Distal Convoluted Tubule |"
                    }
                ]
            })

        # 2. Socratic evaluation
        if ("student selected" in prompt_lower or "evaluate this student" in prompt_lower or "student's stated reasoning" in prompt_lower):
            if any(k in prompt_lower for k in ["vio", "imu", "euler", "drift", "preintegration"]):
                return json.dumps({
                    "is_correct": False,
                    "error_taxonomy": "CRITICAL_PITFALL",
                    "socratic_critique": "You selected option A. Why would naive global-frame integration require recomputing the entire state trajectory whenever an earlier keyframe orientation changes during optimization? What happens to the rotated gravity vector when a 1-degree gyroscope bias exists?",
                    "mechanism_explanation": "Evaluating IMU integration in the global frame couples state propagation directly to the initial orientation R_0. Whenever the optimizer adjusts R_0, all subsequent integrated states become invalid. Furthermore, a 1° gyro bias projects gravity into false horizontal acceleration causing explosive quadratic position drift (8.5 meters in 10 seconds).",
                    "remediation_action": "Recorded anti-pattern: 'Naive global-frame IMU integration'. Added trap to wiki concept [[imu-preintegration-on-so3-manifolds]].",
                    "anki_card_candidate": {
                        "front": "Why is naive global-frame IMU numerical integration {{c1::prohibited in optimization-based VIO}}?",
                        "back": "Any update to initial orientation during bundle adjustment invalidates all integrated states, and uncorrected gyro bias causes {{c1::quadratic position divergence}} via gravity tilt."
                    }
                })

            if any(k in prompt_lower for k in ["4-node", "quorum", "raft", "split-brain", "consensus"]):
                return json.dumps({
                    "is_correct": False,
                    "error_taxonomy": "CRITICAL_PITFALL",
                    "socratic_critique": "You selected option A. Why would a 4-node cluster provide extra fault tolerance when a majority quorum requires floor(4/2) + 1 = 3 nodes? What happens if a network partition cleanly splits the nodes into groups of 2 and 2?",
                    "mechanism_explanation": "In a 4-node cluster, 3 nodes are required to reach a majority quorum. Thus, only 1 node failure can be tolerated—identical to a 3-node cluster. Furthermore, a 2-2 partition prevents either side from reaching quorum, causing total unavailability.",
                    "remediation_action": "Recorded anti-pattern: 'Configured even-numbered consensus quorum'. Added trap to wiki.",
                    "anki_card_candidate": {
                        "front": "Why does a 4-node Raft consensus cluster offer {{c1::zero additional fault tolerance}} compared to a 3-node cluster?",
                        "back": "Both require a majority quorum ({{c1::3 nodes for N=4}} vs {{c2::2 nodes for N=3}}), meaning both tolerate at most {{c3::1 failure}}."
                    }
                })

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

        # 3. Problem / Vignette generation
        if "vignette" in prompt_lower or "generate a challenging" in prompt_lower or "problem" in prompt_lower:
            if any(k in prompt_lower for k in ["vio", "imu", "odometry", "preintegration", "visual-inertial", "navigation"]):
                return json.dumps({
                    "vignette_id": "vio-imu-001",
                    "topic": "On-Manifold IMU Preintegration in Visual-Inertial Odometry",
                    "domain": "Engineering",
                    "stem": "You are developing a real-time Visual-Inertial Odometry (VIO) estimator for an autonomous drone. A roboticist on your team implements IMU numerical integration by accumulating accelerometer readings in the world frame: v_{t+1} = v_t + (R_t a_t + g) Δt. During non-linear pose-graph bundle adjustment, the optimizer updates the initial orientation R_0.\n\nWhat is the primary computational failure and physical consequence of this naive implementation?",
                    "options": [
                        {"id": "A", "text": "The implementation is sound and reduces memory usage by keeping IMU measurements in the global frame."},
                        {"id": "B", "text": "Whenever initial orientation R_0 updates during optimization, all intermediate IMU measurements must be re-integrated from scratch, creating an O(N) bottleneck and severe quadratic position drift from uncorrected gyroscope bias."},
                        {"id": "C", "text": "The naive integration automatically guarantees that the yaw angle around gravity remains fully observable without magnetometer input."},
                        {"id": "D", "text": "Global-frame integration prevents accelerometer bias from affecting horizontal velocity estimates."}
                    ],
                    "correct_option": "B",
                    "explanation": "On-manifold IMU Preintegration (Forster et al.) isolates relative motion deltas (ΔR, Δv, Δp) in the local coordinate frame of the initial keyframe. Without preintegration, every change to R_0 during nonlinear least-squares bundle adjustment invalidates all integrated states, forcing expensive numerical re-integration. Furthermore, a 1° gyro bias tilts the gravity vector into false horizontal acceleration causing rapid quadratic drift.",
                    "learning_pearl": "Always preintegrate IMU delta measurements in the local body frame so that optimization iterations do not require re-integrating high-rate sensor streams.",
                    "high_yield_tags": ["VIO", "IMU Preintegration", "SO(3)", "State Estimation", "MIT 16.485"]
                })

            if any(k in prompt_lower for k in ["mapanything", "dust3r", "3d", "reconstruction", "gaussian"]):
                return json.dumps({
                    "vignette_id": "3d-mapanything-001",
                    "topic": "MapAnything & Universal Feed-Forward Metric 3D Reconstruction",
                    "domain": "Computer Science",
                    "stem": "You are deploying a 3D mapping pipeline on an inspection robot capturing uncalibrated multi-view RGB images. Traditional Structure-from-Motion (COLMAP) fails to deliver real-time reconstructions due to slow incremental bundle adjustment. An engineer suggests deploying MapAnything.\n\nWhich of the following describes MapAnything's architectural strategy for achieving feed-forward metric 3D reconstruction?",
                    "options": [
                        {"id": "A", "text": "It executes 100 iterations of Levenberg-Marquardt optimization per frame to triangulate SIFT keypoints."},
                        {"id": "B", "text": "It factors multi-view geometry into per-view depth maps, local ray maps, 6-DoF poses, and a global metric scale factor, regressing 3D scenes in a single forward pass without test-time optimization."},
                        {"id": "C", "text": "It strictly requires calibrated stereo camera rigs and cannot reconstruct from monocular or heterogeneous image sets."},
                        {"id": "D", "text": "It only outputs implicit NeRF density fields that require volumetric ray-marching to extract meshes."}
                    ],
                    "correct_option": "B",
                    "explanation": "MapAnything decomposes 3D geometry into depth maps D, ray maps R, camera poses T, and a metric scale S. By predicting these factors in a unified Vision Transformer, it unifies over 12 tasks (SfM, MVS, localization, depth estimation) into a single feed-forward pass without iterative bundle adjustment.",
                    "learning_pearl": "Feed-forward foundation models replace fragile feature matching and slow non-linear optimization by directly regressing metric ray and depth structures.",
                    "high_yield_tags": ["MapAnything", "3D Reconstruction", "Foundation Models", "CVPR/3DV"]
                })

            if any(k in prompt_lower for k in ["dino", "latent", "world model"]):
                return json.dumps({
                    "vignette_id": "dinov2-latent-001",
                    "topic": "DINOv2 Latent Space Geometry & Dense Point Correspondence",
                    "domain": "Computer Science",
                    "stem": "You are designing an autonomous tabletop manipulation agent using Vision Transformer representations. You need to establish dense point-to-point physical correspondences across wide-baseline camera views without collecting ground-truth keypoint annotations.\n\nWhich representation extracted from a frozen DINOv2 model provides this capability, and what metric geometry governs the correspondence?",
                    "options": [
                        {"id": "A", "text": "The scalar output of the [CLS] classification token using Euclidean L1 norm distance."},
                        {"id": "B", "text": "The spatial patch tokens (z_i ∈ R^D) forming a dense feature manifold where corresponding physical surface points maximize cosine similarity."},
                        {"id": "C", "text": "A pixel-level diffusion decoder operating in RGB color space."},
                        {"id": "D", "text": "Language embeddings projected through a text tokenizer."}
                    ],
                    "correct_option": "B",
                    "explanation": "In DINOv2, the spatial patch tokens retain local geometric and semantic identity. Because the model is trained with self-distillation, physical points on the same object surface across different camera angles, scales, and lighting conditions naturally cluster together, maximizing cosine similarity.",
                    "learning_pearl": "DINOv2 patch tokens form an emergent metric manifold for dense geometric correspondence without any multi-view supervision.",
                    "high_yield_tags": ["DINOv2", "Latent Space", "Dense Correspondence", "ViT"]
                })

            if any(k in prompt_lower for k in ["distributed", "consensus", "raft", "cs", "computer", "engineering", "system"]):
                return json.dumps({
                    "vignette_id": "eecs-consensus-001",
                    "topic": "Distributed Consensus & Quorums",
                    "domain": "Computer Science",
                    "stem": "You are designing a fault-tolerant distributed configuration store using the Raft consensus protocol across 3 availability zones. A junior engineer proposes scaling the cluster from 3 nodes to 4 nodes to 'increase availability and tolerate more node failures'.\n\nWhich of the following architectural assessments is correct regarding the proposed 4-node cluster?",
                    "options": [
                        {"id": "A", "text": "The 4-node cluster increases fault tolerance, allowing the system to tolerate 2 node crashes."},
                        {"id": "B", "text": "The 4-node cluster provides zero additional crash fault tolerance (still tolerates only 1 failure) and introduces split-brain partition vulnerabilities."},
                        {"id": "C", "text": "The 4-node cluster guarantees zero split-vote states during randomized election timeouts."},
                        {"id": "D", "text": "The 4-node cluster reduces write amplification by allowing minority commits."}
                    ],
                    "correct_option": "B",
                    "explanation": "A quorum of N nodes requires floor(N/2) + 1 nodes. For N=3, quorum is 2 (tolerates 1 failure). For N=4, quorum is 3 (tolerates 1 failure). The 4-node cluster tolerates no more failures than 3 nodes, while a 2-2 network partition renders the entire cluster unavailable because neither side has a majority.",
                    "learning_pearl": "Consensus clusters should always use an odd number of voting members (2F + 1 nodes to tolerate F failures).",
                    "high_yield_tags": ["Raft", "Consensus", "Distributed Systems", "Quorums"]
                })

            return json.dumps({
                "vignette_id": "cardio-vignette-001",
                "topic": "Cardiovascular Pharmacology & Heart Failure",
                "domain": "Medicine",
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

        # 4. External synthesis
        # 4. External synthesis
        if "synthesize" in prompt_lower or "concept page" in prompt_lower or "raw material" in prompt_lower:
            topic_str = prompt_lower
            for line in prompt.splitlines():
                if line.lower().startswith("topic:"):
                    topic_str = line.lower()
                    break

            if "sglt2" in topic_str or "heart" in topic_str or "diuretic" in topic_str or "gliflozin" in topic_str:
                return json.dumps({
                    "slug": "sglt2-inhibitors-in-heart-failure",
                    "title": "SGLT2 Inhibitors (Empagliflozin, Dapagliflozin)",
                    "system": "Cardiovascular & Renal",
                    "domain": "Medicine",
                    "summary": "Sodium-glucose cotransporter-2 inhibitors that reduce cardiovascular mortality and heart failure hospitalizations.",
                    "content": "### Mechanism of Action\nSGLT2 inhibitors block sodium-glucose reabsorption in the proximal convoluted tubule.\n\n### Clinical Trials & Pearls\nDAPA-HF and EMPEROR-Reduced demonstrated significant mortality benefits.\n\nRelated: [[concepts/loop-diuretics]], [[concepts/acute-decompensated-heart-failure]].",
                    "candidate_card": {
                        "front": "What metabolic complication is uniquely associated with {{c1::SGLT2 inhibitors}}?",
                        "back": "{{c1::Euglycemic Diabetic Ketoacidosis (euDKA)}}",
                        "pearl": "Normal blood glucose (< 250 mg/dL) with profound anion-gap metabolic acidosis."
                    }
                })

            if any(k in topic_str for k in ["raft", "consensus", "distributed", "storage", "paxos"]):
                return json.dumps({
                    "slug": "raft-distributed-consensus",
                    "title": "Raft Distributed Consensus Protocol",
                    "domain": "Computer Science",
                    "system": "Distributed Systems",
                    "summary": "Decomposed consensus algorithm guaranteeing state machine safety through leader completeness and append-only logs.",
                    "content": "### Mechanism\nRaft guarantees that only candidates possessing all committed log entries can be elected leader.",
                    "candidate_card": {
                        "front": "In Raft, what prevents split-vote livelocks during leader elections?",
                        "back": "{{c1::Randomized election timeouts (e.g. 150ms-300ms)}}",
                        "pearl": "Randomized timers ensure one candidate times out and collects votes before peers."
                    }
                })

            return json.dumps({
                "slug": "sglt2-inhibitors-in-heart-failure",
                "title": "SGLT2 Inhibitors (Empagliflozin, Dapagliflozin)",
                "system": "Cardiovascular & Renal",
                "domain": "Medicine",
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
                "summary": "Mock synthesis completed successfully.",
                "data": {"result": "ok"}
            })

        if "cirrhosis" in prompt_lower or "ascites" in prompt_lower:
            return "In cirrhosis, sinusoidal portal hypertension triggers splanchnic arterial vasodilation, arterial underfilling, and secondary hyperaldosteronism producing ascites."

        return "Knowledge analysis complete. Core foundational mechanisms, structural invariants, and high-yield insights synthesized successfully."

# Backward compatibility alias
MockMedicalLLMClient = MockUniversalLLMClient

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

    return MockUniversalLLMClient()
