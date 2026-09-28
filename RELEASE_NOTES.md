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

### 🏛 Paideia Genesis v0.3.1 Release 🧠
**Clearer Multi-Domain Wiki Navigation & Reliable Math Rendering**  
*Knowledge Graph &bull; Wiki Explorer &bull; KaTeX &bull; Active Recall*

Paideia Genesis v0.3.1 makes the universal knowledge base easier to browse across disciplines. Wiki pages now carry their own domain and entity metadata through the API and graph, while the interface provides focused category filters and clearer labels. This release also fixes display and inline math rendering in wiki notes and keeps flashcards aligned with the current wiki.

The release workflow packages standalone binaries for **Linux (x86_64)**, **macOS (Apple Silicon arm64)**, and **Windows (x64)**.

---

## 🚀 Key Highlights & Improvements in v0.3.1

### 1. 🗂 More Precise Wiki Navigation
- **Metadata-Aware Pages**: The wiki index and tree API expose each page's `domain`, `course`, `category`, and `entity_type` when provided in frontmatter.
- **Focused Filters**: Browse models, algorithms, concepts, differentials, and traps from the wiki sidebar. Entity subfilters make large collections easier to scan.
- **Clearer Labels**: Wiki entries show type and subject badges that distinguish models, algorithms, tools, protocols, and medical topics.

### 2. 🧠 A More Useful Knowledge Graph
- **Explicit Entity Types**: Graph nodes respect `entity_type` frontmatter, with broader fallback classification for models, algorithms, frameworks, protocols, and other entities.
- **Focused Views**: Filter graph nodes by models, algorithms, concepts, traps, or lectures. Updated colors and the legend reflect these types.
- **Course Context**: Graph filtering recognizes 3D vision and robotics material when those subjects are present in an imported wiki.

### 3. ∑ Improved Mathematical Notes
- **Reliable KaTeX Blocks**: Display equations survive Markdown parsing and render as standalone math blocks.
- **Cleaner LaTeX Input**: The renderer normalizes doubled backslashes in math commands and improves the fallback display when KaTeX is unavailable.
- **General-Purpose Callouts**: Default note and warning labels now fit technical subjects beyond medicine.

### 4. 🃏 Flashcards That Follow Your Wiki
- **Stale Card Cleanup**: Recompiling cards drops cards tied to deleted wiki pages and removes legacy medical cards when that curriculum is absent.
- **Personal Cards Preserved**: User-created cards without a removed source remain in the deck.

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
- **14 targeted tests passed** for graph memory, wiki indexing, and equation formatting.

