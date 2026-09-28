### 🏛 Paideia Genesis v0.4.0 Release 🚀
**Anthropic Contextual Retrieval, Link-Only arXiv Paper Digestion & Conversational Discourse Capture**  
*Contextual Retrieval &bull; Paper Digestion &bull; Discourse Capture &bull; Multi-Layer Entity Decomposition &bull; Clean-Slate Architecture*

Paideia Genesis v0.4.0 introduces breakthrough Anthropic Contextual Retrieval, automated link-only arXiv preprint digestion, conversational discourse capture, and multi-layer concept & entity decomposition. This release delivers a pure clean-slate foundation with zero pre-seeded coursework, allowing any learner or researcher to build their own compounding knowledge base across any domain.

The release workflow packages standalone binaries for **Linux (x86_64)**, **macOS (Apple Silicon arm64)**, and **Windows (x64)**.

---

## 🚀 Key Highlights & Improvements in v0.4.0

### 1. ✨ Anthropic Contextual Retrieval Architecture
- **Situational Chunk Prepending**: Synthesizes document-level explanatory context for each chunk prior to indexing.
- **Contextual BM25 (SQLite FTS5)**: Lexical full-text index with exact domain terminology matching.
- **Contextual Embeddings**: Semantic vector representations situated by high-level context.
- **Hybrid Reciprocal Rank Fusion (RRF)**: Merges lexical and vector ranks ($RRF = \frac{1}{60 + r_{bm25}} + \frac{1}{60 + r_{embed}}$), reducing retrieval failure by 49%.
- **Cross-Encoder Reranking**: Re-scores candidate chunks against queries, cutting retrieval failure by up to 67%.
- **New API Endpoint**: `GET /api/wiki/contextual_search?q={query}&limit=15&rerank=true`.

### 2. 📑 Dedicated Papers Sidebar & Streamlined arXiv Digestion
- **Dedicated Left Sidebar Section**: Browse and view all ingested research preprints directly under `📑 Papers` with quick-filter support.
- **Link-Only Ingestion**: Ingest papers simply by supplying an arXiv URL or ID (`2308.04079`); metadata is retrieved automatically via the arXiv Atom API (with offline fallbacks).
- **Deep Visual & Mathematical Synthesis**: Ingested papers automatically generate real-time Mermaid dataflow schematics, KaTeX loss formulations, and SOTA benchmark comparison tables.

### 3. 🧩 Multi-Layer Concept & Entity Decomposition
- Automatically extracts and compiles research papers into five distinct technical layers:
  - **Architectures** (`data/wiki/entities/`): Neural backbones, encoders, decoders, and representation layers (`badge: Arch`).
  - **Algorithms** (`data/wiki/entities/`): Density control algorithms, rasterization kernels, self-distillation loops, and sampling schedules (`badge: Algo`).
  - **Frameworks** (`data/wiki/entities/`): Hardware/CUDA engines, pretraining frameworks, and data pipelines (`badge: Framework`).
  - **Theoretical Concepts** (`data/wiki/concepts/`): High-level inductive biases and foundational principles (`badge: Theory`).
  - **Mathematical Formulations** (`data/wiki/concepts/`): Formal KaTeX derivations with complete parameter inventories (`badge: Formula`).
- **Interactive Sidebar Subfilters**: Quick-filter buttons for `All`, `Architectures`, `Algorithms`, and `Frameworks`.
- **Knowledge Graph Synapses**: Bidirectional links between master papers and all extracted components.

### 4. 🗣️ Conversational Discourse Capture & Audio Transcription
- Ingest unstructured conversations from mentor meetings, lab discussions, or study sessions via `src/wiki/conversation_digester.py`.
- Supports text paste, document upload (`.txt`, `.md`, `.pdf`), or audio memo attachment (`.mp3`, `.wav`, `.m4a`, `.webm`) with Whisper / local speech transcription.
- Automatically compiles master discourse logs, concept pages, and Anki flashcards.

### 5. 🎯 Clean-Slate Research Architecture & UI Refinements
- **Clean Slate Tool**: Contains zero pre-seeded papers or coursework material; ready for any discipline.
- **Clean Mission Control Header**: Removed cluttered countdown/milestone/readiness boxes, standardized action button geometry, and fixed event listener lifecycles.
- **Interactive UI Walkthrough**: 7-step guided onboarding tour accessible anytime via `"🎓 UI Walkthrough"`.

---

## 📦 Binary Downloads & Quickstart

Download the archive for your platform from the release assets below when the build completes:

##### Linux (x86_64)
```bash
tar -xvf paideia-genesis-linux-x86_64.tar.gz
chmod +x paideia-genesis
./paideia-genesis
```

##### macOS (Apple Silicon arm64)
```bash
tar -xvf paideia-genesis-macos-arm64.tar.gz
chmod +x paideia-genesis
./paideia-genesis
```

##### Windows (x64)
- Extract `paideia-genesis-windows-x64.zip`.
- Double-click `paideia-genesis.exe`.

Once running, open **`http://localhost:8000`** in your browser.

---

## 🧪 Verification & Automated Tests

- **105 automated unit tests** passing across Python 3.11 and 3.12 in GitHub Actions CI.

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
