"""Unified multi-provider LLM gateway supporting Gemini, OpenAI-compatible (home GPU), and Mock.
Supports universal knowledge synthesis across Engineering, Computer Science, Research, and Medicine.
"""
import re
import math
import json
import base64
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

    def embed_text(self, text: str) -> List[float]:
        """Generates a dense vector embedding for semantic similarity search."""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Batch generates dense vector embeddings."""
        return [self._offline_deterministic_embedding(t) for t in texts]

    def generate_contextual_prefix(self, document_content: str, chunk_content: str) -> str:
        """Anthropic Contextual Retrieval: situates a chunk within the overall document.
        Prepend chunk-specific explanatory context before embedding and BM25 indexing.
        """
        prompt = f"""<document>
{document_content[:6000]}
</document>
Here is the chunk we want to situate within the whole document
<chunk>
{chunk_content[:2000]}
</chunk>
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else."""
        try:
            context = self.generate(prompt, temperature=0.1).strip()
            # Clean any wrapping quotes or prefixes
            context = re.sub(r'^(Context:|Summary:)\s*', '', context, flags=re.IGNORECASE).strip()
            return context
        except Exception as e:
            logger.warning(f"Contextual prefix generation failed: {e}. Using rule-based fallback.")
            return self._fallback_contextual_prefix(document_content, chunk_content)

    def rerank(self, query: str, documents: List[str]) -> List[float]:
        """Reranks candidate documents for relevance against query (scores 0.0 to 1.0)."""
        if not documents:
            return []
        scores = []
        q_vec = self.embed_text(query)
        q_tokens = set(re.findall(r'\b\w+\b', query.lower()))
        for doc in documents:
            d_vec = self.embed_text(doc)
            cos_sim = sum(a * b for a, b in zip(q_vec, d_vec))
            d_tokens = set(re.findall(r'\b\w+\b', doc.lower()))
            jaccard = len(q_tokens & d_tokens) / max(1, len(q_tokens | d_tokens))
            score = 0.6 * max(0.0, cos_sim) + 0.4 * jaccard
            scores.append(round(score, 4))
        return scores

    @staticmethod
    def _offline_deterministic_embedding(text: str, dim: int = 64) -> List[float]:
        import math
        import hashlib
        tokens = re.findall(r'\b\w+\b', text.lower())
        if not tokens:
            return [0.0] * dim
        vec = [0.0] * dim
        for tok in tokens:
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % dim
            sign = 1.0 if ((h >> 8) & 1) else -1.0
            vec[idx] += sign * (1.0 / (1.0 + len(tok) ** 0.5))
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [round(x / norm, 5) for x in vec]
        return vec

    @staticmethod
    def _fallback_contextual_prefix(document_content: str, chunk_content: str) -> str:
        # Extract title and top headers from document
        lines = [line.strip() for line in document_content.splitlines() if line.strip()]
        doc_title = "Document"
        for l in lines:
            if l.startswith("# "):
                doc_title = l[2:].strip()
                break
            elif l.startswith("title:"):
                doc_title = l.split(":", 1)[1].strip().strip('"\'')
                break
        return f"This chunk discusses aspects of {doc_title} within the broader curriculum."

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav", mime_type: str = "audio/wav") -> str:
        """Transcribes recorded or uploaded audio into text."""
        return self._offline_mock_transcribe(audio_bytes, filename)

    def _offline_mock_transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """Deterministic transcript fallback for offline test suites and mock runs."""
        return (
            "[Speaker 1]: We discussed scaling laws for 3D Gaussian Splatting and dense feature distillation with DINOv2.\n"
            "[Speaker 2]: The key bottleneck is camera parallax. If the baseline is too narrow, Gaussians overfit along viewing rays as floater artifacts.\n"
            "[Speaker 1]: Exactly. We agreed to incorporate bilateral grid regularization and test on the multi-view benchmark tomorrow."
        )

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

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav", mime_type: str = "audio/wav") -> str:
        url = f"{self.base_url}/audio/transcriptions"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        files = {
            "file": (filename, audio_bytes, mime_type)
        }
        data = {
            "model": "whisper-1"
        }
        try:
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=90)
            resp.raise_for_status()
            res_json = resp.json()
            return res_json.get("text", "")
        except Exception as e:
            logger.warning(f"OpenAI/Whisper transcription failed: {e}. Falling back to deterministic mock.")
            return self._offline_mock_transcribe(audio_bytes, filename)

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

    def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav", mime_type: str = "audio/wav") -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        payload = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": mime_type, "data": b64_audio}},
                    {"text": "Please transcribe this conversation verbatim. Accurately preserve speaker labels (e.g. [Speaker 1], [Speaker 2]) and all technical and research terms."}
                ]
            }]
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=90)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.warning(f"Gemini audio transcription failed: {e}. Falling back to deterministic mock.")
            return self._offline_mock_transcribe(audio_bytes, filename)

class MockUniversalLLMClient(BaseLLMClient):
    """Deterministic universal intelligence simulation for testing and offline pilot demonstrations.
    Handles Computer Science, Systems Engineering, Mathematics, Physics, and Medicine.
    """
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.2) -> str:
        prompt_lower = prompt.lower()

        # Contextual Retrieval prefix generation (Anthropic method)
        if "<document>" in prompt and "<chunk>" in prompt and "situate this chunk" in prompt_lower:
            doc_match = re.search(r'<document>(.*?)</document>', prompt, re.DOTALL)
            chunk_match = re.search(r'<chunk>(.*?)</chunk>', prompt, re.DOTALL)
            doc_text = doc_match.group(1) if doc_match else ""
            chunk_text = chunk_match.group(1) if chunk_match else ""
            doc_title = "Document"
            for line in doc_text.splitlines():
                line = line.strip()
                if line.startswith("# "):
                    doc_title = line[2:].strip()
                    break
                elif line.startswith("title:"):
                    doc_title = line.split(":", 1)[1].strip().strip('"\'')
                    break
            section_name = ""
            for line in chunk_text.splitlines():
                line = line.strip()
                if line.startswith("#"):
                    section_name = line.lstrip("#").strip()
                    break
            if section_name:
                return f"This chunk is from '{doc_title}', section '{section_name}', detailing high-yield mechanisms and clinical/systems principles."
            return f"This chunk is part of '{doc_title}', discussing foundational concepts and implementation nuances."

        # Conversation & Discourse Digestion
        if "conversation" in prompt_lower and ("digest" in prompt_lower or "discourse" in prompt_lower or "transcript" in prompt_lower):
            return json.dumps({
                "title": "3D Gaussian Splatting and Feature Distillation Discussion",
                "summary": "Technical consultation examining camera parallax constraints in 3D Gaussian Splatting, mitigation of floater artifacts, and integration with DINOv2 visual features.",
                "insights": [
                    "Narrow baseline camera setups cause 3D Gaussians to overfit along viewing rays as planar floater artifacts.",
                    "Bilateral grid regularization and depth supervision prevent depth ambiguity under small baselines.",
                    "DINOv2 features provide dense semantic geometry priors that accelerate Gaussian optimization."
                ],
                "action_items": [
                    "Benchmark bilateral grid regularization on the custom drone dataset.",
                    "Implement depth-guided densification threshold in CUDA rasterizer.",
                    "Test DINOv2 ViT-B/14 semantic feature distillation on novel view synthesis."
                ],
                "concepts": [
                    {
                        "slug": "gaussian-floater-regularization",
                        "title": "3D Gaussian Floater Regularization & Depth Constraints",
                        "domain": "Computer Science & AI",
                        "system": "3D Vision & Neural Rendering",
                        "tags": ["3DGS", "Artifacts", "Regularization", "Discussion"],
                        "summary": "Techniques for eliminating ray-aligned planar floaters under narrow-baseline camera trajectories.",
                        "content": "### Problem & Mechanism\nWhen camera translation baseline is small relative to scene depth, the epipolar geometry lacks sufficient triangulation angle.\n\n### Mitigation Strategies\n1. Depth-guided regularization.\n2. Bilateral grid smoothing.\n\nRelated: [[concepts/3d-gaussian-splatting]]."
                    }
                ],
                "entities": [
                    {
                        "slug": "bilateral-grid",
                        "title": "Bilateral Grid Regularizer",
                        "category": "Algorithm",
                        "high_yield_notes": "Edge-preserving 3D spatial smoothing grid for radiance fields."
                    }
                ],
                "differentials": [
                    {
                        "slug": "depth-supervised-vs-unsupervised-3dgs",
                        "title": "Depth-Supervised vs Unsupervised 3DGS",
                        "summary": "Comparison of reconstruction fidelity under narrow camera baselines.",
                        "content": "| Feature | Depth-Supervised 3DGS | Vanilla 3DGS |\n|---|---|---|\n| Floater Artifacts | Low | High on narrow parallax |\n| Geometry Accuracy | High | Prone to degenerate depth |"
                    }
                ],
                "flashcards": [
                    {
                        "front": "Under narrow camera parallax baselines, 3D Gaussians tend to overfit as {{c1::planar floater artifacts}} along camera viewing rays.",
                        "back": "Resolved via depth supervision and bilateral grid smoothing."
                    }
                ]
            })

        # 0c. Research Paper Deep Digestion & Visual Synthesis
        if any(k in prompt_lower for k in [
            "analyze the following academic research paper",
            "deep technical deconstruction",
            "research paper preprint",
            "visual architecture schematic"
        ]):
            title_match = re.search(r'Title:\s*(.*?)\n', prompt)
            paper_title = title_match.group(1).lower() if title_match else prompt_lower[:250]

            is_vit = any(k in paper_title for k in ["transformer", "vit", "16x16", "dosovitskiy"])
            is_diff = any(k in paper_title for k in ["diffusion", "score", "denois", "latent"])
            is_nerf = any(k in paper_title for k in ["nerf", "mildenhall", "view synthesis"])
            is_dino = any(k in paper_title for k in ["dino", "dinov2"])
            is_sam = any(k in paper_title for k in ["segment anything", "sam"])

            if is_vit:
                return json.dumps({
                    "title": "Vision Transformers (ViT)",
                    "summary": "Vision Transformer (ViT) treats image patches as visual tokens, demonstrating that standard Transformer encoder architectures can supersede inductive biases of convolutional networks at scale.",
                    "mermaid_diagram": "flowchart TD\n  Img[Input Image HxWxC] --> Patches[Linear Patch Projection: N x D]\n  Patches --> PosEnc[Add Learnable Positional Embeddings + [CLS] Token]\n  PosEnc --> EncBlock[L x Transformer Encoder Blocks: LayerNorm, Multi-Head Self-Attention, MLP]\n  EncBlock --> Head[MLP Classification Head on [CLS] Token]",
                    "components": [
                        {"name": "Patch Projection Embedding", "type": "Tokenization", "description": "Flattens image into PxP non-overlapping patches linearly projected to dimension D."},
                        {"name": "Multi-Head Self-Attention", "type": "Attention Engine", "description": "Computes all-to-all quadratic attention across visual tokens."}
                    ],
                    "mathematical_formulations": [
                        {
                            "slug": "vit-scaled-dot-product-formulation",
                            "title": "Scaled Dot-Product Self-Attention Formulation",
                            "latex": "\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V",
                            "explanation": "Scales matrix product of Query and Key tokens by square root of head dimension d_k to prevent gradient saturation."
                        }
                    ],
                    "architectures": [
                        {
                            "slug": "transformer-encoder-backbone",
                            "title": "Standard Transformer Encoder Backbone",
                            "category": "Architecture",
                            "entity_type": "Architecture",
                            "high_yield_notes": "Pre-LN multi-head attention stack with GeLU MLP feed-forward."
                        }
                    ],
                    "algorithms": [
                        {
                            "slug": "vit-scaled-dot-product-attention",
                            "title": "Scaled Dot-Product Self-Attention Algorithm",
                            "category": "Algorithm",
                            "entity_type": "Algorithm",
                            "high_yield_notes": "All-to-all quadratic attention mechanism computing normalized dot-product affinities."
                        }
                    ],
                    "frameworks": [
                        {
                            "slug": "vit-pytorch-pipeline",
                            "title": "PyTorch Vision Transformer Pipeline",
                            "category": "Framework",
                            "entity_type": "Framework",
                            "high_yield_notes": "Modular execution framework for Vision Transformers."
                        }
                    ],
                    "theoretical_concepts": [
                        {
                            "slug": "patch-tokenization",
                            "title": "Patch-Based Visual Tokenization",
                            "category": "Theoretical Concept",
                            "summary": "Decomposing continuous 2D images into sequence of token embeddings.",
                            "content": "Treats patches analogously to text word tokens, relaxing translation invariance."
                        }
                    ],
                    "empirical_benchmarks": [
                        {"benchmark": "ImageNet-1k", "baselines": "ResNet-152, BiT", "metric_1": "88.55% Top-1", "metric_2": "632M FLOPs", "fps_latency": "85 img/s"}
                    ],
                    "engineering_traps": [
                        {"trap": "Quadratic Memory Bottleneck O(N^2)", "pitfall": "Reducing patch size P from 16 to 8 quadruples token length, exploding self-attention memory by 16x.", "mitigation": "Use FlashAttention or hierarchical windowed attention (Swin)."}
                    ],
                    "pseudocode": "def forward_vit(x):\n    tokens = patch_embed(x) + pos_embed\n    for layer in layers:\n        tokens = layer(tokens)\n    return mlp_head(tokens[:, 0])",
                    "concepts": [
                        {"slug": "patch-tokenization", "title": "Patch-Based Visual Tokenization", "summary": "Decomposing continuous 2D images into sequence of token embeddings.", "content": "Treats patches analogously to text word tokens."}
                    ],
                    "entities": [
                        {"slug": "transformer-encoder-backbone", "title": "Standard Transformer Encoder Backbone", "category": "Architecture", "high_yield_notes": "Pre-LN multi-head attention stack"}
                    ],
                    "differentials": [
                        {"slug": "vit-vs-deep-convnets", "title": "ViT vs Deep Convolutions", "summary": "Global attention vs local translation invariance.", "content": "| Feature | ViT | CNN |\n|---|---|---|\n| Inductive Bias | Minimal | Strong translation invariance |\n| Data Hunger | High | Moderate |"}
                    ],
                    "flashcards": [
                        {"front": "In standard Vision Transformers, self-attention memory scales as {{c1::O(N^2)}} with respect to the number of image patches N.", "back": "Halving patch size quadruples sequence length N and increases attention memory 16-fold."}
                    ]
                })

            if is_diff:
                return json.dumps({
                    "title": "High-Resolution Image Synthesis with Latent Diffusion Models",
                    "summary": "Latent Diffusion Models achieve state-of-the-art image synthesis while reducing compute requirements by training diffusion models in the compressed latent space of pretrained autoencoders.",
                    "mermaid_diagram": "flowchart LR\n  Pixel[High-Res Pixel Image x] --> Enc[Pretrained VAE Encoder E]\n  Enc --> Latent[Latent Representation z]\n  Latent --> Diff[Denoising U-Net with Cross-Attention]\n  Diff --> Pred[Noise Estimate ε_θ]\n  Diff --> Dec[Pretrained VAE Decoder D]\n  Dec --> Recon[High-Fidelity Synthesized Image]",
                    "components": [
                        {"name": "Latent Denoising U-Net", "type": "Denoising Backbone", "description": "Time-conditioned convolutional U-Net with cross-attention layers conditioning on text or semantic layouts."},
                        {"name": "First-Stage Autoencoder", "type": "Perceptual Compression", "description": "Learns perceptually lossless latent representation z = E(x) with 8x spatial downsampling."}
                    ],
                    "mathematical_formulations": [
                        {
                            "slug": "ldm-latent-denoising-loss-objective",
                            "title": "Latent Diffusion Loss Objective (L_LDM)",
                            "latex": "\\mathcal{L}_{LDM} = \\mathbb{E}_{\\mathcal{E}(x), \\epsilon \\sim \\mathcal{N}(0, 1), t}\\left[ \\| \\epsilon - \\epsilon_\\theta(z_t, t, \\tau_\\theta(y)) \\|_2^2 \\right]",
                            "explanation": "Denoises latent variable z_t conditioned on timestep t and text conditioning vector tau_theta(y)."
                        }
                    ],
                    "architectures": [
                        {
                            "slug": "ldm-denoising-unet-backbone",
                            "title": "Latent Denoising U-Net Backbone",
                            "category": "Architecture",
                            "entity_type": "Architecture",
                            "high_yield_notes": "Time-conditioned convolutional U-Net with cross-attention layers conditioning on text or semantic layouts."
                        }
                    ],
                    "algorithms": [
                        {
                            "slug": "ldm-denoising-score-matching",
                            "title": "Denoising Score Matching Algorithm",
                            "category": "Algorithm",
                            "entity_type": "Algorithm",
                            "high_yield_notes": "Optimizes mean squared error between injected Gaussian noise ε and predicted noise ε_θ(z_t, t, c)."
                        }
                    ],
                    "frameworks": [
                        {
                            "slug": "huggingface-diffusers-pipeline",
                            "title": "Hugging Face Diffusers Pipeline Framework",
                            "category": "Framework",
                            "entity_type": "Framework",
                            "high_yield_notes": "Modular diffusion execution ecosystem providing schedulers (DDIM, DPMSolver), checkpoint management, and GPU memory optimizations."
                        }
                    ],
                    "theoretical_concepts": [
                        {
                            "slug": "perceptual-vs-semantic-compression-duality",
                            "title": "Perceptual vs Semantic Compression Duality",
                            "category": "Theoretical Concept",
                            "summary": "Separates high-frequency perceptual pixel details from core semantic structure.",
                            "content": "First stage autoencoder removes imperceptible high-frequency noise; second stage diffusion model operates exclusively in computationally efficient latent space."
                        }
                    ],
                    "empirical_benchmarks": [
                        {"benchmark": "ImageNet 256x256", "baselines": "ADM, BigGAN", "metric_1": "10.56 FID", "metric_2": "0.32 s/sample", "fps_latency": "3.1 samples/s"}
                    ],
                    "engineering_traps": [
                        {"trap": "Overly Aggressive Autoencoder Compression", "pitfall": "Spatial downsampling factor f > 16 introduces blur and loss of high-frequency textures.", "mitigation": "Use perceptual LPIPS loss combined with patch-based adversarial discriminator."}
                    ],
                    "pseudocode": "def sample_ldm(model, z_T, text_cond):\n    z = z_T\n    for t in timesteps:\n        noise = model(z, t, text_cond)\n        z = scheduler.step(noise, t, z).prev_sample\n    return vae.decode(z)",
                    "differentials": [
                        {"slug": "ldm-vs-pixel-diffusion", "title": "LDM vs Pixel-Space Diffusion", "summary": "Latent space vs pixel space training.", "content": "| Feature | LDM | Pixel-Space (DDPM) |\n|---|---|---|\n| Resolution | 512x512 | 64x64 or Cascaded |\n| Training Cost | Moderate | Extremely High |"}
                    ],
                    "flashcards": [
                        {"front": "In Latent Diffusion Models, high-frequency details are separated from semantic composition by operating in the {{c1::latent space of a pretrained autoencoder}}.", "back": "Avoids spending 90% of diffusion compute on imperceptible pixel details."}
                    ]
                })

            if is_nerf:
                return json.dumps({
                    "title": "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis",
                    "summary": "NeRF represents 3D scenes as continuous volumetric functions parameterized by 5D coordinate MLPs optimized via differentiable volumetric raymarching.",
                    "mermaid_diagram": "flowchart LR\n  Ray[Camera Ray r(t) = o + td] --> PosEnc[Positional Encoding γ(x), γ(d)]\n  PosEnc --> MLP[8-Layer MLP Network]\n  MLP --> Out[Volume Density σ & RGB Color c]\n  Out --> March[Numerical Quadrature Raymarching]\n  March --> Pixel[Rendered Pixel Color C(r)]",
                    "components": [
                        {"name": "Volumetric Radiance Field MLP", "type": "Implicit Neural Representation", "description": "8-layer MLP with 256 channels mapping 3D coordinates x to volume density σ and view-dependent color c."},
                        {"name": "Hierarchical Volume Sampling", "type": "Sampling Engine", "description": "Coarse and fine networks stratified along camera rays using inverse transform sampling."}
                    ],
                    "mathematical_formulations": [
                        {
                            "slug": "nerf-volume-rendering-integral",
                            "title": "Continuous Volumetric Rendering Integral",
                            "latex": "C(r) = \\int_{t_n}^{t_f} T(t) \\sigma(r(t)) c(r(t), d) \\, dt, \\quad T(t) = \\exp\\left(-\\int_{t_n}^t \\sigma(r(s)) \\, ds\\right)",
                            "explanation": "Computes expected color of camera ray by integrating radiance weighted by transmittance T(t) and density sigma."
                        }
                    ],
                    "architectures": [
                        {
                            "slug": "nerf-coordinate-mlp-backbone",
                            "title": "NeRF Coordinate-Based Radiance Field MLP",
                            "category": "Architecture",
                            "entity_type": "Architecture",
                            "high_yield_notes": "8-layer fully-connected network with skip connections at layer 4 and high-frequency sinusoidal positional encodings."
                        }
                    ],
                    "algorithms": [
                        {
                            "slug": "nerf-hierarchical-volume-sampling",
                            "title": "Hierarchical Volume Sampling Algorithm",
                            "category": "Algorithm",
                            "entity_type": "Algorithm",
                            "high_yield_notes": "Stratified random sampling followed by probability density function (PDF) importance sampling along camera rays."
                        }
                    ],
                    "frameworks": [
                        {
                            "slug": "nerf-pytorch-raymarching-framework",
                            "title": "PyTorch Volumetric Raymarching Framework",
                            "category": "Framework",
                            "entity_type": "Framework",
                            "high_yield_notes": "Numerical quadrature raymarching engine for implicit continuous radiance fields."
                        }
                    ],
                    "theoretical_concepts": [
                        {
                            "slug": "continuous-implicit-neural-fields",
                            "title": "Continuous Implicit Neural Fields",
                            "category": "Theoretical Concept",
                            "summary": "Encoding 3D visual environments as continuous coordinate-to-value mappings without explicit polygonal meshes.",
                            "content": "Eliminates discretization artifacts and voxel grid memory bottlenecks, achieving continuous view synthesis."
                        }
                    ],
                    "empirical_benchmarks": [
                        {"benchmark": "Synthetic NeRF Blender", "baselines": "SRN, NV, LLFF", "metric_1": "31.01 dB PSNR", "metric_2": "0.947 SSIM", "fps_latency": "0.03 FPS"}
                    ],
                    "engineering_traps": [
                        {"trap": "High-Frequency Spectral Bias (Saturation)", "pitfall": "Standard MLPs are biased toward low-frequency functions and cannot reconstruct sharp textures.", "mitigation": "Apply Fourier positional encoding gamma(p) = [sin(2^k pi p), cos(2^k pi p)]."}
                    ],
                    "pseudocode": "def render_ray(ray_o, ray_d, mlp):\n    points = sample_along_ray(ray_o, ray_d)\n    density, colors = mlp(positional_encoding(points))\n    weights = compute_transmittance(density)\n    return torch.sum(weights * colors, dim=-2)",
                    "differentials": [
                        {"slug": "nerf-vs-explicit-voxels", "title": "NeRF vs Voxel Grids", "summary": "Continuous implicit MLP vs discrete voxel grids.", "content": "| Feature | NeRF | Voxels |\n|---|---|---|\n| Memory | Low (MLP weights) | High O(N^3) |\n| Rendering Speed | Slow | Fast |"}
                    ],
                    "flashcards": [
                        {"front": "In NeRF, MLPs overcome spectral bias against high frequencies via {{c1::sinusoidal positional encodings}}.", "back": "Maps low-dimensional coordinates into a higher-dimensional Fourier space."}
                    ]
                })

            if is_dino:
                return json.dumps({
                    "title": "DINOv2: Learning Robust Visual Features without Supervision",
                    "summary": "DINOv2 demonstrates that self-supervised pretraining on massive uncurated visual datasets yields multipurpose visual representations that perform competitively with weakly-supervised models.",
                    "mermaid_diagram": "flowchart TD\n  Img[Uncurated Image Set] --> Crop[Multi-Crop View Augmentations]\n  Crop --> Student[Student ViT with iBOT Masking]\n  Crop --> Teacher[Teacher ViT with EMA Weights]\n  Student --> Loss[Cross-Entropy Centering + Swapped Loss]\n  Teacher --> Target[Sinkhorn-Knopp Centered Targets]\n  Target --> Loss",
                    "components": [
                        {"name": "Vision Transformer Backbone (ViT-g/14)", "type": "Feature Extractor", "description": "1B parameter Vision Transformer backbone with SwiGLU activations and LayerScale."},
                        {"name": "iBOT Masked Image Modeling Head", "type": "Token-Level Objective", "description": "Predicts visual tokens for masked patch tokens concurrently with global DINO loss."}
                    ],
                    "mathematical_formulations": [
                        {
                            "slug": "dinov2-cross-entropy-loss",
                            "title": "DINO Self-Distillation Cross-Entropy Loss",
                            "latex": "\\mathcal{L}_{DINO} = - \\sum_{i} P_t(i) \\log P_s(i), \\quad P_s(i) = \\frac{\\exp(g_s(x)_i / \\tau_s)}{\\sum_j \\exp(g_s(x)_j / \\tau_s)}",
                            "explanation": "Minimizes cross-entropy between student softmax probabilities P_s and centered teacher probabilities P_t."
                        }
                    ],
                    "architectures": [
                        {
                            "slug": "dinov2-vit-giant-backbone",
                            "title": "DINOv2 ViT-Giant Architecture Backbone",
                            "category": "Architecture",
                            "entity_type": "Architecture",
                            "high_yield_notes": "1-Billion parameter Vision Transformer with patch size 14x14 and SwiGLU feed-forward networks."
                        }
                    ],
                    "algorithms": [
                        {
                            "slug": "dinov2-student-teacher-distillation",
                            "title": "DINOv2 Student-Teacher Self-Distillation Algorithm",
                            "category": "Algorithm",
                            "entity_type": "Algorithm",
                            "high_yield_notes": "Student network trained via SGD while teacher network parameters updated via exponential moving average (EMA)."
                        }
                    ],
                    "frameworks": [
                        {
                            "slug": "dinov2-self-supervised-pretraining-framework",
                            "title": "DINOv2 Large-Scale Pretraining Framework",
                            "category": "Framework",
                            "entity_type": "Framework",
                            "high_yield_notes": "Distributed PyTorch data curation, deduplication, and mixed-precision self-supervised pretraining pipeline."
                        }
                    ],
                    "theoretical_concepts": [
                        {
                            "slug": "self-supervised-feature-emergence",
                            "title": "Emergence of Dense Semantic Layouts in Self-Supervised Vision",
                            "category": "Theoretical Concept",
                            "summary": "Dense spatial feature representations emerge purely from self-distillation without human annotation.",
                            "content": "Self-supervised ViTs produce PCA feature maps that segment semantic boundaries and object parts without supervisory labels."
                        }
                    ],
                    "empirical_benchmarks": [
                        {"benchmark": "ImageNet-1k Linear Probe", "baselines": "OpenCLIP, DINOv1, MAE", "metric_1": "86.5% Top-1", "metric_2": "Zero-shot depth", "fps_latency": "14ms"}
                    ],
                    "engineering_traps": [
                        {"trap": "Mode Collapse into Constant Output", "pitfall": "Student and teacher networks converge to predicting uniform constant representations.", "mitigation": "Apply centering on teacher outputs and sharpening with temperature tau."}
                    ],
                    "pseudocode": "def train_step(student, teacher, x1, x2):\n    p_s = student(x1)\n    with torch.no_grad():\n        p_t = teacher(x2)\n    loss = cross_entropy(p_s, center_and_sharpen(p_t))\n    update_ema(teacher, student)\n    return loss",
                    "differentials": [
                        {"slug": "dinov2-vs-mae", "title": "DINOv2 vs Masked Autoencoders (MAE)", "summary": "Self-distillation vs pixel reconstruction.", "content": "| Feature | DINOv2 | MAE |\n|---|---|---|\n| Linear Probing | State-of-the-Art | Requires Fine-Tuning |\n| Dense Features | Highly semantic | Low-level reconstruction |"}
                    ],
                    "flashcards": [
                        {"front": "In DINOv2 self-supervised distillation, representation collapse is avoided via {{c1::centering and sharpening}} of teacher outputs.", "back": "Centering prevents one dimension from dominating; sharpening prevents uniform distributions."}
                    ]
                })

            if is_sam:
                return json.dumps({
                    "title": "Segment Anything (SAM)",
                    "summary": "Segment Anything Model (SAM) introduces a promptable segmentation foundation model and data engine that enables zero-shot general-purpose segmentation across images.",
                    "mermaid_diagram": "flowchart LR\n  Img[High-Res Input Image] --> Enc[Heavyweight Image Encoder: ViT-H/16]\n  Enc --> Embed[Image Embedding: 1x256x64x64]\n  Prompt[User Points / Boxes / Text] --> PEnc[Prompt Encoder]\n  Embed --> Dec[Lightweight Two-Way Transformer Decoder]\n  PEnc --> Dec\n  Dec --> Mask[High-Quality Segmentation Masks + IoU Scores]",
                    "components": [
                        {"name": "Heavyweight Image Encoder", "type": "Feature Extraction", "description": "MAE-pretrained Vision Transformer (ViT-H/16) generating dense image embeddings in one pass."},
                        {"name": "Prompt Encoder & Mask Decoder", "type": "Interactive Engine", "description": "Lightweight two-way cross-attention transformer generating valid masks in <50ms."}
                    ],
                    "mathematical_formulations": [
                        {
                            "slug": "sam-focal-dice-loss",
                            "title": "SAM Composite Focal & Dice Segmentation Loss",
                            "latex": "\\mathcal{L}_{mask} = \\alpha \\mathcal{L}_{Focal}(y, \\hat{y}) + \\beta \\mathcal{L}_{Dice}(y, \\hat{y})",
                            "explanation": "Balances hard pixel mining via focal loss with global spatial overlap preservation via dice loss."
                        }
                    ],
                    "architectures": [
                        {
                            "slug": "sam-promptable-mask-decoder",
                            "title": "SAM Promptable Two-Way Transformer Mask Decoder",
                            "category": "Architecture",
                            "entity_type": "Architecture",
                            "high_yield_notes": "Two-way cross-attention decoder mapping prompt tokens and image embeddings into segmentation masks."
                        }
                    ],
                    "algorithms": [
                        {
                            "slug": "sam-ambiguity-aware-multi-mask-prediction",
                            "title": "Ambiguity-Aware Multi-Mask Output Algorithm",
                            "category": "Algorithm",
                            "entity_type": "Algorithm",
                            "high_yield_notes": "Predicts 3 candidate masks (whole, part, subpart) for ambiguous single-point prompts and ranks by predicted IoU."
                        }
                    ],
                    "frameworks": [
                        {
                            "slug": "sam-data-engine-loop",
                            "title": "SAM Interactive Annotation Data Engine Framework",
                            "category": "Framework",
                            "entity_type": "Framework",
                            "high_yield_notes": "Three-stage human-in-the-loop data curation framework producing the 11M image / 1B mask SA-1B dataset."
                        }
                    ],
                    "theoretical_concepts": [
                        {
                            "slug": "promptable-foundation-segmentation",
                            "title": "Promptable Segmentation Task Formulation",
                            "category": "Theoretical Concept",
                            "summary": "Formulating visual segmentation as a promptable task analogous to prompting in language models.",
                            "content": "Given any prompt (points, box, mask, text), the model must return a valid segmentation mask even in ambiguous contexts."
                        }
                    ],
                    "empirical_benchmarks": [
                        {"benchmark": "SA-1B Zero-Shot Transfer", "baselines": "R50-Cascade, ViTDet", "metric_1": "Zero-shot mIoU competitive with supervised", "metric_2": "1.1B masks", "fps_latency": "50ms decoder"}
                    ],
                    "engineering_traps": [
                        {"trap": "Single-Point Prompt Ambiguity", "pitfall": "A single foreground point on a person's shirt can legitimately refer to the shirt, the torso, or the entire person.", "mitigation": "Predict 3 disambiguated hierarchical output masks and output predicted IoU scores."}
                    ],
                    "pseudocode": "def segment_image(image, points):\n    image_embed = image_encoder(image)\n    prompt_embed = prompt_encoder(points)\n    masks, iou_preds = mask_decoder(image_embed, prompt_embed)\n    return select_best_mask(masks, iou_preds)",
                    "differentials": [
                        {"slug": "sam-vs-semantic-segmentation", "title": "Promptable SAM vs Closed-Set Semantic Segmentation", "summary": "Open-world promptable mask generation vs fixed-class semantic segmentation.", "content": "| Feature | SAM | Mask R-CNN |\n|---|---|---|\n| Vocabulary | Zero-shot open-world | Fixed closed vocabulary |\n| Latency | 50ms (decoder reuse) | Per-image backbone forward |"}
                    ],
                    "flashcards": [
                        {"front": "In Segment Anything (SAM), single-point prompt ambiguity is resolved by outputting {{c1::3 hierarchical masks (whole, part, subpart)}} with predicted IoU scores.", "back": "Prevents the model from averaging disparate plausible segmentations into a blurry prediction."}
                    ]
                })

            # Default to 3DGS or generic high-yield visual paper
            return json.dumps({
                "title": "3D Gaussian Splatting for Real-Time Radiance Field Rendering",
                "summary": "3D Gaussian Splatting introduces anisotropic 3D Gaussians as a flexible, explicit radiance representation optimized via differentiable tile-based rasterization achieving 100+ FPS.",
                "mermaid_diagram": "flowchart LR\n  A[Camera Pose & SfM Points] --> B[3D Gaussians: Position, Covariance Σ, SH Colors, Opacity]\n  B --> C[Tile-Based Differentiable Rasterizer]\n  C --> D[Rendered Alpha-Blended Frame Î]\n  D --> E[Photometric Loss: L1 + SSIM]\n  E --> F[Adaptive Density Control: Clone / Split / Prune]\n  F --> B",
                "components": [
                    {"name": "Anisotropic 3D Gaussians", "type": "Explicit Geometry", "description": "Parametrized by center position x, 3D covariance matrix Σ = RSS^TR^T, opacity α, and Spherical Harmonics."},
                    {"name": "Tile-Based Rasterizer", "type": "Rendering Pipeline", "description": "Sorts Gaussians by tile key on GPU and executes front-to-back α-blending in sub-10ms."}
                ],
                "mathematical_formulations": [
                    {
                        "slug": "3dgs-anisotropic-covariance-formulation",
                        "title": "Anisotropic Covariance Parametrization",
                        "latex": "\\Sigma = R S S^T R^T, \\quad G(x) = \\exp\\left(-\\frac{1}{2}(x - \\mu)^T \\Sigma^{-1} (x - \\mu)\\right)",
                        "explanation": "Ensures covariance matrix Σ remains positive semi-definite by factoring into scaling matrix S and rotation matrix R (quaternions)."
                    },
                    {
                        "slug": "3dgs-photometric-loss-formulation",
                        "title": "Composite Photometric L1 + D-SSIM Loss",
                        "latex": "\\mathcal{L}_{render} = (1 - \\lambda) \\mathcal{L}_1(I, \\hat{I}) + \\lambda \\mathcal{L}_{SSIM}(I, \\hat{I})",
                        "explanation": "Balances pixel-wise L1 color reconstruction with structural perceptual SSIM fidelity (typically λ = 0.2)."
                    }
                ],
                "architectures": [
                    {
                        "slug": "3dgs-anisotropic-gaussian-representation",
                        "title": "Anisotropic 3D Gaussian Representation",
                        "category": "Architecture",
                        "entity_type": "Architecture",
                        "high_yield_notes": "Explicit radiance representation parameterized by center position, 3D covariance matrix Σ = RSS^TR^T, opacity α, and spherical harmonics."
                    }
                ],
                "algorithms": [
                    {
                        "slug": "3dgs-tile-based-differentiable-rasterizer",
                        "title": "Tile-Based Differentiable Rasterizer",
                        "category": "Algorithm",
                        "entity_type": "Algorithm",
                        "high_yield_notes": "Sorts 3D Gaussians by 16x16 screen-space tiles and computes front-to-back α-blending in sub-10ms."
                    },
                    {
                        "slug": "3dgs-adaptive-density-control",
                        "title": "Adaptive Density Control Algorithm",
                        "category": "Algorithm",
                        "entity_type": "Algorithm",
                        "high_yield_notes": "Clones under-reconstructed Gaussians and splits oversized Gaussians."
                    }
                ],
                "frameworks": [
                    {
                        "slug": "3dgs-cuda-rasterization-engine",
                        "title": "CUDA Rasterization Engine & Kernel Stack",
                        "category": "Framework",
                        "entity_type": "Framework",
                        "high_yield_notes": "High-throughput CUDA execution framework for fast tile-based rasterization."
                    }
                ],
                "theoretical_concepts": [
                    {
                        "slug": "3dgs-explicit-vs-implicit-radiance-duality",
                        "title": "Explicit vs Implicit Scene Radiance Duality",
                        "category": "Theoretical Concept",
                        "summary": "Duality between continuous coordinate MLPs and discretized point Gaussians.",
                        "content": "Implicit methods evaluate dense raymarching; explicit Gaussians eliminate empty-space queries."
                    }
                ],
                "empirical_benchmarks": [
                    {"benchmark": "Mip-NeRF 360", "baselines": "Instant-NGP, Plenoxels", "metric_1": "27.5 dB PSNR", "metric_2": "0.815 SSIM", "fps_latency": "135 FPS"},
                    {"benchmark": "Tanks & Temples", "baselines": "NeRF, Mip-NeRF", "metric_1": "23.8 dB PSNR", "metric_2": "0.840 SSIM", "fps_latency": "110 FPS"}
                ],
                "engineering_traps": [
                    {"trap": "Planar Floater Overfitting", "pitfall": "Gaussians elongate along camera viewing rays in narrow baseline setups.", "mitigation": "Apply depth supervision regularization and isotropic covariance penalty."}
                ],
                "pseudocode": "def forward_render(gaussians, camera):\n    tiles = bin_gaussians_to_tiles(gaussians, camera)\n    image = tile_rasterize(tiles, sort_depth=True)\n    return image",
                "concepts": [
                    {"slug": "adaptive-density-control", "title": "Adaptive Density Control in 3DGS", "summary": "Splitting and cloning under-reconstructed or over-sized 3D Gaussians.", "content": "Periodically prunes transparent Gaussians and splits large Gaussians along principal axes."}
                ],
                "entities": [
                    {"slug": "cuda-tile-rasterizer", "title": "Tile-Based Differentiable Rasterizer", "category": "Renderer", "high_yield_notes": "CUDA parallel sort & blend kernel"}
                ],
                "differentials": [
                    {"slug": "3dgs-vs-implicit-nerf", "title": "3DGS vs Implicit NeRF", "summary": "Explicit rasterization vs volume raymarching.", "content": "| Feature | 3DGS | NeRF |\n|---|---|---|\n| Speed | >100 FPS | 0.2 FPS |\n| Memory | High (VRAM) | Low |"}
                ],
                "flashcards": [
                    {"front": "In 3D Gaussian Splatting, covariance is kept positive semi-definite by parameterizing Σ as {{c1::R S S^T R^T}} using rotation quaternions and scale vectors.", "back": "Prevents degenerate negative eigenvalues during gradient descent."}
                ]
            })

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
