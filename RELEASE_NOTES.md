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
