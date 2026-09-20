### ⚕ Paideia Genesis v0.2.0 Release ⚕
**Dual-Process Kahneman Architecture (Jev System 1) & Single-Unknown Atomic Flashcards**

Paideia Genesis v0.2.0 introduces deep integration with **Jev (TypeSafe AI)** for sub-100ms machine-native clinical triage and automated active recall grading, alongside **Single-Unknown (Atomic) Flashcard Derivation** adhering to Piotr Wozniak's *Minimum Information Principle*.

Precompiled, standalone zero-dependency binary executables are available below for **Linux (x86_64)**, **macOS (Apple Silicon arm64)**, and **Windows (x64)**.

---

## ⚡ How to Configure & Use Jev (TypeSafe AI)

Paideia Genesis implements a **Kahneman Dual-Process Cognitive Architecture**:
- **System 1 (Jev `jev-1.13.0`)**: Fast, typed, machine-native decision primitives (`Choice`, `Score`, `Noul`) executing in **sub-second inference (~80ms–400ms)** with calibrated confidence.
- **System 2 (Gemini / Claude / Local LLM)**: Multi-turn analytical Socratic tutoring, diagnostic remediation, and vignette authoring.

### 1. Setting Your Jev API Key
To enable live Jev System 1 inference:
1. Copy `.env.example` (or create a `.env` file) in the directory where you run Paideia Genesis:
   ```bash
   cp .env.example .env
   ```
2. Add your TypeSafe AI API key:
   ```env
   TYPESAFE_API_KEY=ts_live_your_actual_api_key_here
   ENABLE_JEV_SYSTEM_ONE=true
   ```
   *Alternatively, export it directly in your shell or terminal before running:*
   ```bash
   export TYPESAFE_API_KEY="ts_live_your_actual_api_key_here"
   export ENABLE_JEV_SYSTEM_ONE="true"
   ```

### 2. Verifying Jev Connection
Start Paideia Genesis:
```bash
./paideia-genesis   # or: python3 run.py
```
Open your browser to **`http://localhost:8000`** and verify:
- **API Status**: Check `http://localhost:8000/api/status`:
  ```json
  {
    "status": "online",
    "system_one": {
      "model": "jev",
      "enabled": true,
      "has_api_key": true
    }
  }
  ```
- **Web Dashboard**: Look at the top navigation bar. When live Jev is connected, a green status pill will indicate:
  `⚡ Jev System 1: Active (Live)`

### 3. Trying Out Jev in Action
- **🩺 Socratic Teacher (Vignette Drill)**:
  - Generate an adaptive clinical case.
  - Pick an answer and type your pathophysiological reasoning.
  - Watch the **Jev System 1 Reflex Box**: in **sub-100ms**, Jev pre-classifies your error taxonomy (`CLINICAL_CONTRAINDICATION`, `MECHANISM_GAP`, `DISCRIMINATOR_CONFUSION`, `READING_SLIP`) and flags USMLE board traps with calibrated confidence before the generative tutor speaks.
- **🎴 Active Recall Flashcard Auto-Grading**:
  - Open the **Anki Flashcard Center** and click **🚀 Study Mode**.
  - Type your clinical mechanism or drug target into the **"✍️ Type Your Active Recall"** box.
  - Click **"⚡ Auto-Grade with Jev System 1"**.
  - Jev grades your recall accuracy on a 5-tier rubric (Levels 0–4) in **~180ms**, updates the SuperMemo-2 (SM-2) review interval, and flips the card to reveal the clinical pearl.

### 4. Zero-Config Offline Fallback
If no API key is set, Paideia Genesis **never crashes**. It automatically falls back to an internal deterministic mock decision engine with simulated latencies, allowing full offline studying, unit testing, and demonstration.

---

## 🎯 Single-Unknown (Atomic) Flashcards

Medical cards often test 2 to 4 clozes at once (e.g. skip lesions, cobblestone mucosa, Crohn's, Ulcerative Colitis). Testing all 4 simultaneously overwhelms working memory. 

In v0.2.0, students can now toggle between:
1. **🎯 Single Unknown (1 topic / Atomic 1-by-1)**:
   - Derives focused child cards where **strictly 1 cloze blank (`{{c1::...}}`) is tested**, while revealing all other clozes as plain text for context.
   - Child cards track review histories and SM-2 curves independently in `parent.atomic_states` without modifying the base Anki format.
2. **📦 Combined (Multi-cloze)**:
   - Preserves multi-cloze board contrast cards in their original layout.
3. **Bi-Directional Switching**:
   - Switch anytime via the **Focus Mode** dropdown in the toolbar.
   - Export either Single-Unknown or Combined decks via the **⬇️ Download .apkg** button or API (`GET /api/anki/export?atomic=true`).

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

Once running, navigate to:
👉 **`http://localhost:8000`**

---

## 🧪 Verification & Automated Tests
- Full test suite: **77 / 77 unit tests passing** across all subsystems.
- CI/CD verified on GitHub Actions with Python 3.11 & 3.12 matrices.
