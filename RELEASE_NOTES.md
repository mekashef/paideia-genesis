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
