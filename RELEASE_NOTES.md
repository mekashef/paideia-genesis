### 🏛 Paideia Genesis v0.3.0 Release 🧠
**Universal Living Education Assistant & Compounding LLM-Wiki for All Disciplines**
*Deep Learning / ML Research &bull; Computer Systems & Engineering &bull; Mathematics &bull; Medicine &bull; Humanities*

Paideia Genesis v0.3.0 generalizes the platform from a medical-only tutor into an **Autonomous Universal Living Education Assistant & Compounding LLM-Wiki**. The system now natively supports any academic or technical discipline with interactive user-guided topic steering, multi-domain HippoRAG associative graph memory, universal engineering error taxonomies, and a pristine personal research setup by default.

Precompiled, zero-dependency standalone binary executables are available below for **Linux (x86_64)**, **macOS (Apple Silicon arm64)**, and **Windows (x64)**.

---

## 🚀 Key Highlights & New Capabilities in v0.3.0

### 1. 🗂 Universal Karpathy 5-Layer LLM-Wiki
- **Multi-Domain Schema**: Every markdown note in the Karpathy-style knowledge base now features first-class `domain`, `field`, `course`, `system`, and arbitrary `tags` frontmatter.
- **Hierarchical Knowledge Organization**:
  - `course_sessions/`: Module readings, syllabus sessions, and lecture decks.
  - `concepts/`: Core mechanisms, state machines, and algorithmic proofs.
  - `entities/`: Protocols, components, drugs, and biomarkers.
  - `differentials/`: Side-by-side trade-off matrices (*Raft vs Paxos*, *B+Trees vs LSM-Trees*, *Crohn's vs UC*).
  - `exam_traps/`: Critical engineering anti-patterns and high-yield traps.
- **Universal Manifest Importer**: Ingest arbitrary JSON curriculum manifests via `POST /api/course/import_manifest`.

### 2. 🏛 User-Guided Socratic Living Teacher & Topic Steering
- **Targeted Dilemma Generation**: Steer Socratic problem generation with explicit controls:
  - **Topic**: Target subject or concept (e.g., *"Distributed Consensus Quorums"* or *"Transformer Attention"*).
  - **Guidance**: Pedagogical focus or constraints (e.g., *"Focus on why an even 4-node cluster fails to increase fault tolerance under network partitions"*).
  - **Domain & Difficulty**: Support for Computer Science, Engineering, Mathematics, and Medicine across beginner, intermediate, and advanced levels.
- **Sub-500ms Reasoning Evaluation**: Analyzes submitted rationale alongside option selection, diagnosing traps in real time without giving away answers.

### 3. ⚡ Universal Kahneman Dual-Process AI (Jev System 1)
- **Universal Error Taxonomies**:
  - **Engineering & CS**: `CRITICAL_PITFALL`, `INVARIANT_VIOLATION`, `RACE_CONDITION`, `OVERFLOW_HAZARD`, `SCALE_BOTTLENECK`
  - **Biomedicine & Natural Sciences**: `CLINICAL_CONTRAINDICATION`, `MECHANISM_GAP`, `DISCRIMINATOR_CONFUSION`, `READING_SLIP`
- **Objective Active Recall (SM-2)**: Free-text typed explanations graded by Jev in **~180ms** against gold-standard rubrics, updating SuperMemo-2 intervals without self-assessment bias.

### 4. 🧠 Multi-Domain Cognitive Brain Graph (HippoRAG)
- **Domain-Aware Semantic Clustering**: Group nodes into field-specific constellations (e.g., Computer Systems, Storage Engines, Biomedicine).
- **HippoRAG Mechanism Spotlighting**: Click any node to illuminate 1-hop direct pathways (bright white) and 2-hop associative cascades (soft blue), dimming unrelated nodes to 12% opacity.
- **Cross-Domain Bridges**: Visualizes architectural parallels and cross-disciplinary concepts (e.g., state machine replication and physiological homeostasis).

### 5. 💻 Built-In Starter Pack: MIT 6.033 Distributed Systems
- Ingested from MIT OpenCourseWare:
  - **10 In-Depth Sessions**: RPC, Virtual Memory/TLB, Concurrency/Deadlocks, WAL/ARIES, Paxos, Raft, B+Trees vs LSM-Trees, Cache Coherence (MESI), Linux Epoll, CAP Theorem.
  - **8 Core Concepts**: State machines, quorum invariants, compaction mechanics.
  - **8 Key Entities**: etcd, RocksDB, gRPC, Epoll, TLB, WAL, MESI Protocol.
  - **5 Comparative Differentials**: Detailed trade-off matrices.
  - **5 Critical Engineering Traps**: Even-numbered consensus quorums, un-cached TLB shootdowns, and edge-triggered epoll starvation.

### 6. 🧹 Pristine Personal Research Setup by Default
- **Zero Default Pollution**: Starts with an empty, clean workspace (`AUTO_SEED_DEMO_DATA=false`) ready for your personal research, work notes, or course projects.
- **Seeding on Demand**: Bootstrap starter curricula anytime with `python3 run.py --seed` or import via the web UI.
- **Clean Slate Command**: Purge and reset wiki state anytime with `python3 run.py --clean` or `POST /api/wiki/reset`.

---

## 📦 Binary Downloads & Quickstart

Standalone, precompiled executables — no Python or Node required:

##### Linux (Ubuntu / Debian / Fedora x86_64)
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
- Extract `paideia-genesis-windows-x64.zip`
- Double-click `paideia-genesis.exe`

Once running, open your browser to:
👉 **`http://localhost:8000`**

---

## 🧪 Verification & Automated Tests
- **83 / 83 unit tests passing** cleanly across all modules and curricula.
- Full CI/CD matrix passing on GitHub Actions (Python 3.11 & 3.12).
