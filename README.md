# Paideia Genesis 🏛

<div align="center">

```
   ____       _     _      _          ____                       _     
  |  _ \ __ _(_) __| | ___(_) __ _   / ___| ___ _ __   ___  ___(_)___ 
  | |_) / _` | |/ _` |/ _ \ |/ _` | | |  _ / _ \ '_ \ / _ \/ __| / __|
  |  __/ (_| | | (_| |  __/ | (_| | | |_| |  __/ | | |  __/\__ \ \__ \
  |_|   \__,_|_|\__,_|\___|_|\__,_|  \____|\___|_| |_|\___||___/_|___/
```

**An Autonomous Living Education Assistant & Compounding Knowledge Engine**  
*Transforming static notes into an evolving, self-reinforcing learning loop.*

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![CI Tests](https://img.shields.io/badge/CI%20Tests-84%2F84%20Passing-brightgreen.svg)](#-running-tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 🌟 What is Paideia Genesis?

Static study notes and syllabus PDFs often turn into write-only graveyards. Meanwhile, traditional flashcards suffer from the *"illusion of competence"* during manual self-scoring, and standard chat-based LLM tutors introduce high latency, hallucinations, and runaway token costs.

**Paideia Genesis** unifies your learning into a closed cognitive loop:
1. **Compounding Knowledge Base**: Ingests notes, papers, and syllabi into an interlinked Markdown wiki (sessions, concepts, entities, comparative differentials, and critical pitfalls).
2. **Socratic Living Teacher**: Generates adaptive conceptual dilemmas based on your custom topic guidance, probing your reasoning rather than just spoon-feeding answers.
3. **Biomimetic Brain Graph**: Explores relationships across disciplines with interactive multi-hop spreading activation and force clustering.
4. **Objective AI-Graded Spaced Repetition**: Type your active recall explanations in free text; an ultra-fast evaluation engine scores conceptual depth against gold standards and schedules SuperMemo-2 (SM-2) intervals without self-assessment bias.
5. **Local-First & Offline-Ready**: Out of the box, works 100% offline with zero external API dependencies using deterministic engines, or connects seamlessly to Google Gemini, local Ollama/vLLM, or TypeSafe AI Jev.

> 📖 **Looking for in-depth system architecture, sequence diagrams, and mathematical formulations?**  
> See the complete technical design in [**docs/ARCHITECTURE.md**](docs/ARCHITECTURE.md).

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.11+
- Virtual environment (`venv`)

### 2. Installation

```bash
# Clone the repository
git clone git@github.com:mekashef/paideia-genesis.git
cd paideia-genesis

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch

```bash
# Option A: Clean Personal Workspace (Default)
# Starts with an empty, pristine workspace ready for your personal notes
python3 run.py

# Option B: Pre-Seeded Starter Pack
# Loads sample technical and biomedical concept starter packs
python3 run.py --seed

# Option C: Clean Slate Reset
# Resets wiki back to initial templates
python3 run.py --clean
```

Open your browser to: **`http://localhost:8000`**

---

## 🧪 Running Tests

The test suite runs completely offline with zero API keys required:

```bash
python3 -m unittest discover tests/ -v
```

```
----------------------------------------------------------------------
Ran 84 tests in ~45s

OK
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` to configure your environment:

```bash
cp .env.example .env
```

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `mock` | `mock` (offline), `gemini`, or `openai_compatible` |
| `GEMINI_API_KEY` | `""` | Optional Google Gemini API key |
| `OPENAI_BASE_URL` | `http://localhost:11434/v1` | URL for local LLM engines (Ollama, vLLM, LM Studio) |
| `OPENAI_MODEL` | `llama3.1:8b` | Model name for local inference |
| `TYPESAFE_API_KEY`| `""` | Optional API key for live TypeSafe AI Jev System 1 |
| `HOST` / `PORT` | `0.0.0.0` / `8000` | Web server host and port |
| `AUTO_SEED_DEMO_DATA` | `false` | Pre-seed starter datasets on initial launch |

---

## 📁 Repository Structure

```
paideia-genesis/
├── src/
│   ├── anki/             # Spaced repetition compiler & SuperMemo-2 scheduler
│   ├── api/              # FastAPI server & endpoints
│   ├── llm/              # Unified gateway (Gemini, local OpenAI-compatible, Jev, Mock)
│   ├── tutor/            # Socratic dilemma engine & misconception tracking
│   └── wiki/             # Compounding Markdown compiler, SQLite FTS5, Brain Graph
├── static/               # Web mission control (Tailwind, D3.js, KaTeX)
├── tests/                # 84 automated offline unit & integration tests
├── docs/                 # Detailed architectural documentation
│   └── ARCHITECTURE.md   # Complete technical specifications & sequence flows
├── .env.example          # Environment configuration template
├── CONTRIBUTING.md       # Contribution guidelines
├── CODE_OF_CONDUCT.md    # Community code of conduct
├── SECURITY.md           # Security reporting policy
├── THIRD_PARTY_NOTICES.md# Attributions and license notices
└── run.py                # Application entry point
```

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Third-party libraries and reference material attributions are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
