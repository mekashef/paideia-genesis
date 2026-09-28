# 🏛 Paideia Genesis v1.2.0: Deep Learning & Vision Engine, Contextual Retrieval & Paper Digestion 🚀
**An Autonomous Living Education Assistant & Compounding Knowledge Engine**  
*Deep Learning & Vision Research &bull; Anthropic Contextual Retrieval &bull; Link-Only arXiv Digestion &bull; Discourse Capture &bull; Multi-Layer Entity Decomposition*

We are thrilled to announce **Paideia Genesis v1.2.0**, a major release that pivots Paideia Genesis into an advanced research environment for **Deep Learning and Computer Vision**, integrates Anthropic's breakthrough **Contextual Retrieval** architecture, and introduces automated **Link-Only Paper Digestion** and **Discourse Capture**!

---

## 🌟 What's New in v1.2.0

### 1. 📑 Dedicated Papers Sidebar & Streamlined arXiv Ingestion
- **Dedicated Papers Section**: Browse all ingested research papers directly in the left navigation sidebar under `📑 Papers`, with one-click full-screen reading.
- **Link-Only Paper Ingestion**: No manual PDF uploads required. Simply paste an arXiv URL or ID (e.g., `2308.04079` or `https://arxiv.org/abs/2112.10752`) to auto-fetch title, authors, and abstract via the arXiv Atom API.
- **Deep Visual & Mathematical Synthesis**: Ingested papers automatically generate:
  - Interactive **Mermaid architectural dataflow schematics** rendered in real time.
  - Rigorous **KaTeX mathematical formulas** for loss objectives and attention equations.
  - SOTA **empirical benchmark comparison tables** (PSNR, SSIM, mIoU, Top-1 accuracy, throughput).
  - Architectural tensor inventories, failure modes, and auto-staged SM-2 Anki flashcards.

### 2. 🧩 Multi-Layer Paper Decomposition (Architectures, Algorithms, Frameworks, Theories & Formulations)
- Research papers are automatically decomposed and compounded into specialized wiki files:
  - **Architectures** (`data/wiki/entities/`): Neural backbones, encoders, decoders, and representation layers.
  - **Algorithms** (`data/wiki/entities/`): Density control algorithms, rasterization kernels, self-distillation loops, and sampling schedules.
  - **Frameworks** (`data/wiki/entities/`): Hardware/CUDA engines, pretraining frameworks, and data pipelines.
  - **Theoretical Concepts** (`data/wiki/concepts/`): High-level inductive biases and foundational principles.
  - **Mathematical Formulations** (`data/wiki/concepts/`): Formal KaTeX derivations with complete parameter inventories.
- **UI Subfilters & Distinct Badges**: One-click subfilter buttons (`All`, `Architectures`, `Algorithms`, `Frameworks`) and color-coded badges (`Arch`, `Algo`, `Framework`, `Theory`, `Formula`, `Paper`, `Discourse`).
- **Knowledge Graph Synapses**: Bidirectional cross-links between master papers and all extracted components.

### 3. 🗣️ Conversational Discourse Capture & Audio Transcription
- Capture unstructured conversations from lab discussions, mentor meetings, or study groups.
- Supports copy-pasting raw text notes, uploading documents (`.txt`, `.md`, `.pdf`), or attaching audio recordings (`.mp3`, `.wav`, `.m4a`, `.webm`).
- Autonomous speech-to-text transcription powered by OpenAI Whisper / local speech models (with deterministic offline fallback).
- Automatically synthesizes master discourse logs, compiles distinct concepts and flashcards, and archives raw source backups.

### 4. ✨ Anthropic Contextual Retrieval Architecture
- **Situational Chunk Prepending**: Synthesizes document-level explanatory context for each chunk before indexing.
- **Contextual BM25 (SQLite FTS5)**: Lexical full-text index with exact terminology matching.
- **Contextual Embeddings**: High-dimensional semantic vectors situated by high-level context.
- **Hybrid Reciprocal Rank Fusion (RRF)**: Merges lexical and vector ranks ($RRF = \frac{1}{60 + r_{bm25}} + \frac{1}{60 + r_{embed}}$), reducing retrieval failure by **49%**.
- **Cross-Encoder Reranking**: Re-scores top candidate chunks against queries, cutting retrieval failure by up to **67%**.

### 5. 🎯 Deep Learning & Computer Vision Foundation & UI Polish
- **Complete Medical Purge**: Purged all legacy medical data and curricula; 100% focused on Deep Learning and Computer Vision (3DGS, ViT, NeRF, Latent Diffusion, DINOv2, SAM).
- **Clean Mission Control Header**: Removed cluttered readiness boxes, standardized action button geometry, and fixed event listener lifecycles.
- **Interactive UI Walkthrough**: Persistent 7-step guided onboarding tour accessible anytime via `"🎓 UI Walkthrough"`.

---

# 🏛 Paideia Genesis v1.1.0: Contextual Retrieval & Guided UI Walkthrough 🚀
**An Autonomous Living Education Assistant & Compounding Knowledge Engine**  
*Anthropic Contextual Retrieval &bull; Interactive UI Onboarding &bull; Dual-Process AI &bull; Biomimetic Memory*

We are excited to announce **Paideia Genesis v1.1.0**, incorporating Anthropic's breakthrough **Contextual Retrieval** architecture ([Anthropic Engineering Guide](https://www.anthropic.com/engineering/contextual-retrieval)) and a comprehensive **Interactive UI Walkthrough** directly inside the Web Mission Control!

---

## 🌟 What's New in v1.1.0

### 1. ✨ Anthropic Contextual Retrieval Architecture
Traditional RAG breaks documents into isolated text chunks, stripping away higher-level context (e.g. an isolated chunk discussing *"the revenue grew 3% over previous quarter"* lacks entity, quarter, or document identity). Paideia Genesis v1.1.0 implements Anthropic's multi-stage Contextual Retrieval framework:
- **Situational Chunk Prepending**: Automatically synthesizes succinct, chunk-specific explanatory context situating each section within the broader document before indexing.
- **Contextual BM25 (SQLite FTS5)**: Lexical full-text index built on situational chunks, enabling exact matching on domain terminology and technical identifiers that would otherwise be missed.
- **Contextual Embeddings**: Semantic vector representations generated for situated chunks (supports Google Gemini `text-embedding-004`, local OpenAI-compatible GPU endpoints, and deterministic offline vectors).
- **Hybrid Reciprocal Rank Fusion (RRF)**: Merges lexical BM25 ranks with semantic embedding similarity ranks ($RRF = \frac{1}{60 + r_{bm25}} + \frac{1}{60 + r_{embed}}$), reducing retrieval failure rates by **49%**.
- **Cross-Encoder Reranking**: Re-scores top candidate chunks against the user query, filtering to the top-K highest-precision chunks and reducing retrieval failure by up to **67%**.
- **New API Endpoint**: `GET /api/wiki/contextual_search?q={query}&limit=15&rerank=true` returns rich situational metadata, section titles, RRF ranks, and cross-encoder scores.

### 2. 🎓 Interactive UI Walkthrough & Onboarding Tour
- **First-Time Guided Tour**: Automatically introduces new users to the closed cognitive learning loop with a clean 7-step guided modal overlay.
- **Step-by-Step Exploration**:
  1. *Welcome & System Overview*: Closed cognitive loop and Kahneman dual-process architecture.
  2. *Compounding Wiki & Contextual Search*: Browsing Karpathy 5-layer notes, hybrid search, and live editing.
  3. *Brain Graph (HippoRAG)*: Spreading activation and associative multi-hop memory cascades.
  4. *Socratic Living Tutor*: Steerable dilemmas, guidance constraints, and root misconception triage.
  5. *Anki Flashcard Center & Jev AI*: Free-text active recall and sub-200ms objective AI grading.
  6. *Curriculum Milestones & Diagnostics*: Exam countdowns, topic mastery heatmaps, and diagnostic logs.
  7. *Quick Capture & Ingestion*: Capturing pearls and pulling in external literature on-the-fly.
- **Persistent Header Access**: Click the new `"🎓 UI Walkthrough"` button in the navigation header anytime to re-launch the tour.
- **Keyboard & Tab Sync**: Supports `← Back`, `Next →`, keyboard arrows, and automatically switches tabs to display the relevant interface live.

---

# 🏛 Paideia Genesis v1.0.0: Going Public! 🚀
**An Autonomous Living Education Assistant & Compounding Knowledge Engine**  
*Deep Learning / ML Research &bull; Computer Systems & Engineering &bull; Mathematics &bull; Medicine &bull; Universal Sciences*

We are thrilled to officially announce the **v1.0.0 public open-source release** of Paideia Genesis!

Paideia Genesis transforms static study notes, lecture decks, and research preprints into an evolving, compounding cognitive learning engine. It combines an interlinked Karpathy-style knowledge base, Kahneman dual-process AI architecture, HippoRAG associative graph memory, and objective AI-graded SuperMemo-2 (SM-2) spaced repetition into a closed, self-reinforcing learning loop.

---

## 🌟 What's New & Included in v1.0.0

### 1. 🗂 Compounding Universal LLM-Wiki
- **Karpathy 5-Layer Knowledge Base**: Automatically structures ingested notes and documents into `course_sessions/`, `concepts/`, `entities/`, `differentials/`, and `exam_traps/`.
- **Clean Workspace by Default**: Starts with a pristine personal workspace (`AUTO_SEED_DEMO_DATA=false`) ready for your own notes and research, with optional one-click starter packs.
- **SQLite FTS5 Full-Text Search**: Instant lexical BM25 indexing across all compiled Markdown documents with real-time audit logging (`log.md`).

### 2. ⚡ Kahneman Dual-Process Cognitive Architecture
- **System 1 (Ultra-Fast Reflex)**: Sub-100ms machine-native decision primitives (`Choice`, `Score`, `Noul`) powered by TypeSafe AI Jev or local deterministic fallback.
- **System 2 (Analytical Synthesis)**: Deep multi-domain Socratic dialogue and dilemma generation powered by Google Gemini or local LLMs (Ollama/vLLM).
- **Zero Financial Risk**: Defaults to 100% offline deterministic execution. It is impossible to incur unexpected API bills without explicitly configuring paid keys.

### 3. 🏛 User-Guided Socratic Tutor
- **Custom Topic & Pedagogical Steering**: Direct problem generation with custom topic focus, pedagogical constraints, and domain hints.
- **Cognitive Misconception Triage**: Diagnoses root errors (e.g., `CRITICAL_PITFALL`, `INVARIANT_VIOLATION`, `CLINICAL_CONTRAINDICATION`) rather than just checking binary correctness.
- **Automated Remediation**: Instantly synthesizes and stages targeted remedial flashcards addressing diagnosed conceptual gaps.

### 4. 🧠 Biomimetic Brain Graph (HippoRAG)
- **Force-Directed Semantic Clustering**: Visualizes interdisciplinary knowledge networks with multi-domain clustering and cross-domain conceptual bridges.
- **Interactive Spreading Activation**: Click any node to illuminate 1-hop direct pathways in white and 2-hop associative cascades in soft blue.

### 5. 🎴 Objective AI-Graded Spaced Repetition (SM-2)
- **Typed Free-Text Active Recall**: Eliminates self-assessment bias ("illusion of competence"). Students type their causal reasoning from memory.
- **Sub-200ms Rubric Evaluation**: Grades explanations against gold-standard concepts and automatically updates SuperMemo-2 intervals and ease factors.
- **Anki Integration**: Export course-filtered `.apkg` packages or sync directly to local Anki Desktop via AnkiConnect (`localhost:8765`).

### 6. 🛡 Open-Source Governance & Community Health
- Complete open-source readiness with MIT License, `.env.example`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and comprehensive `THIRD_PARTY_NOTICES.md`.
- 100% offline-verifiable test suite (84 automated tests passing in ~45s).

---

## 📦 Standalone Binary Downloads

Standalone executables packaged with PyInstaller are available in the release assets below:

- **Linux (x86_64)**: `paideia-genesis-linux-x86_64.tar.gz`
- **macOS (Apple Silicon arm64)**: `paideia-genesis-macos-arm64.tar.gz`
- **Windows (x64)**: `paideia-genesis-windows-x64.zip`

---

## 🧪 Verification
- **84 automated tests passed** across all cognitive engines, compilers, and APIs.
