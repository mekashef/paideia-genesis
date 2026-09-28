// Paideia Genesis 2.0 Frontend Application Logic
// Integrating HippoRAG, LightRAG, and Mixed-Initiative On-The-Fly Knowledge

let currentVignette = null;
let selectedOptionId = null;
let currentLoadedPath = "index.md";
let isEditingPage = false;
let d3Simulation = null;

// Flashcard & Spaced-Repetition State
let ankiCurrentCards = [];
let ankiActiveCardIndex = 0;
let ankiIsStudyRevealed = false;
let ankiViewMode = "browse"; // "browse" or "study"
let ankiSearchDebounceTimer = null;


// Initialize app on DOM ready
document.addEventListener("DOMContentLoaded", () => {
    setupTabs();
    setupEventListeners();
    loadStatus();
    loadWikiTree();
    loadWikiPage("index.md");
    loadVignette();
    loadAnkiCards();
    loadCurriculum();

    // Initialize Mermaid for architectural diagrams
    if (window.mermaid) {
        try {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                themeVariables: {
                    darkMode: true,
                    background: '#0f172a',
                    primaryColor: '#6366f1',
                    primaryTextColor: '#f8fafc',
                    primaryBorderColor: '#818cf8',
                    lineColor: '#94a3b8',
                    secondaryColor: '#3b82f6',
                    tertiaryColor: '#1e293b'
                }
            });
        } catch (e) {
            console.warn("Mermaid init error:", e);
        }
    }

    // Initialize Interactive UI Walkthrough
    window.walkthroughManager = new UIWalkthroughManager();
    if (!localStorage.getItem("paideia_genesis_walkthrough_seen")) {
        setTimeout(() => {
            window.walkthroughManager.start(0);
        }, 600);
    }
});

// Setup tab navigation
function setupTabs() {
    const tabs = [
        { btn: "tabBtnWiki", view: "viewWiki" },
        { btn: "tabBtnGraph", view: "viewGraph" },
        { btn: "tabBtnTutor", view: "viewTutor" },
        { btn: "tabBtnAnki", view: "viewAnki" },
        { btn: "tabBtnCurriculum", view: "viewCurriculum" }
    ];

    tabs.forEach(t => {
        const btnEl = document.getElementById(t.btn);
        if (!btnEl) return;
        btnEl.addEventListener("click", () => {
            // Deactivate all
            tabs.forEach(o => {
                document.getElementById(o.btn).classList.remove("active", "text-indigo-400", "border-indigo-400");
                document.getElementById(o.btn).classList.add("text-slate-400", "border-transparent");
                document.getElementById(o.view).classList.add("hidden");
            });

            // Activate chosen
            btnEl.classList.add("active", "text-indigo-400", "border-indigo-400");
            btnEl.classList.remove("text-slate-400", "border-transparent");
            document.getElementById(t.view).classList.remove("hidden");

            if (t.view === "viewGraph") renderBrainGraph();
            if (t.view === "viewAnki") loadAnkiCards();
            if (t.view === "viewCurriculum") loadCurriculum();
        });
    });
}

function setupEventListeners() {
    // Course / Module Focus Filter Dropdown
    const courseFilter = document.getElementById("wikiCourseFilter");
    if (courseFilter) {
        courseFilter.addEventListener("change", () => {
            loadWikiTree();
        });
    }

    // Brain Graph Controls
    const graphCourse = document.getElementById("graphCourseFilter");
    if (graphCourse) {
        graphCourse.addEventListener("change", () => renderBrainGraph());
    }
    const graphLayer = document.getElementById("graphLayerFilter");
    if (graphLayer) {
        graphLayer.addEventListener("change", () => renderBrainGraph());
    }
    const graphColor = document.getElementById("graphColorMode");
    if (graphColor) {
        graphColor.addEventListener("change", () => renderBrainGraph());
    }
    const btnResetZoom = document.getElementById("btnResetGraphZoom");
    if (btnResetZoom) {
        btnResetZoom.addEventListener("click", () => resetGraphZoom());
    }
    const btnRefresh = document.getElementById("btnRefreshGraph");
    if (btnRefresh) {
        btnRefresh.addEventListener("click", () => renderBrainGraph());
    }
    const btnClearSpot = document.getElementById("btnClearSpotlight");
    if (btnClearSpot) {
        btnClearSpot.addEventListener("click", () => clearGraphSpotlight());
    }
    const graphSearch = document.getElementById("graphSearchInput");
    if (graphSearch) {
        graphSearch.addEventListener("input", (e) => searchAndFocusNode(e.target.value.trim()));
    }

    // Conversation & Discourse Capture Manager
    setupConversationCaptureManager();

    // Research Paper Importer & Deep Digestion Manager
    setupPaperImportManager();

    // Course Importer Modal
    const btnOpenImport = document.getElementById("btnOpenImportCourse");
    if (btnOpenImport) {
        btnOpenImport.addEventListener("click", () => {
            openModal("modalImportCourse");
        });
    }

    const btnSelectEecs = document.getElementById("btnSelectEecsPreset");
    if (btnSelectEecs) {
        btnSelectEecs.addEventListener("click", () => {
            const input = document.getElementById("importCourseUrlInput");
            if (input) input.value = "demo_data/MIT_6_033_Distributed_Systems_and_Networking.json";
            const title = document.getElementById("importPresetTitle");
            if (title) title.textContent = "Selected: MIT 6.033 Distributed Systems & Networking";
        });
    }

    const btnSubmitImport = document.getElementById("btnSubmitImportCourse");
    if (btnSubmitImport) {
        btnSubmitImport.addEventListener("click", async () => {
            const url = document.getElementById("importCourseUrlInput").value.trim();
            closeModal("modalImportCourse");
            showToast("Ingesting curriculum and compiling universal living wiki...", "info");
            try {
                let resp;
                if (url.endsWith(".json")) {
                    resp = await fetch("/api/course/import_manifest", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ manifest_path: url })
                    });
                } else {
                    resp = await fetch("/api/course/import_vision", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" }
                    });
                }
                const data = await resp.json();
                if (data.success) {
                    showToast(`Successfully imported ${data.course}! (${data.concepts_compiled} concepts, ${data.differentials_compiled} diffs)`, "success");
                    await loadWikiTree();
                    const firstSlug = (data.compiled_concepts && data.compiled_concepts[0]) || "vision-transformers-vit";
                    await loadWikiPage(`concepts/${firstSlug}.md`);
                    await loadStatus();
                    await loadCurriculum();
                    await loadAnkiCards();
                    if (!document.getElementById("viewGraph").classList.contains("hidden")) {
                        renderBrainGraph();
                    }
                } else {
                    showToast("Course import failed.", "error");
                }
            } catch (e) {
                showToast("Course import failed: " + e, "error");
            }
        });
    }

    // Quick-Capture Synapse Modal
    document.getElementById("btnOpenQuickCapture").addEventListener("click", () => {
        openModal("modalQuickCapture");
    });

    document.getElementById("btnSubmitQuickCapture").addEventListener("click", async () => {
        const topic = document.getElementById("qcTopicInput").value.trim();
        const note = document.getElementById("qcNoteInput").value.trim();
        if (!note) {
            showToast("Please enter a clinical pearl or note.", "info");
            return;
        }
        showToast("Weaving on-the-fly note into Paideia Genesis brain...", "info");
        try {
            const resp = await fetch("/api/wiki/quick_capture", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topic_hint: topic || "Clinical Pearl", note })
            });
            const data = await resp.json();
            closeModal("modalQuickCapture");
            document.getElementById("qcTopicInput").value = "";
            document.getElementById("qcNoteInput").value = "";
            showToast("Note woven into Wiki & Anki flashcard staged!", "success");
            await loadWikiTree();
            await loadWikiPage(data.rel_path);
            await loadStatus();
        } catch (e) {
            showToast("Quick-capture failed: " + e, "error");
        }
    });

    // Pull-In Knowledge Modal
    document.getElementById("btnOpenPullKnowledge").addEventListener("click", () => {
        openModal("modalPullKnowledge");
    });

    document.getElementById("btnSubmitPullKnowledge").addEventListener("click", async () => {
        const query = document.getElementById("pullQueryInput").value.trim();
        if (!query) {
            showToast("Please enter a medical topic or trial to pull.", "info");
            return;
        }
        showToast(`Pulling and synthesizing "${query}" on-the-fly...`, "info");
        closeModal("modalPullKnowledge");
        try {
            const resp = await fetch("/api/wiki/pull_external", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });
            const data = await resp.json();
            showToast(`Synthesized "${data.title}" into living wiki!`, "success");
            document.getElementById("pullQueryInput").value = "";
            await loadWikiTree();
            await loadWikiPage(data.rel_path);
            await loadStatus();
            if (!document.getElementById("viewGraph").classList.contains("hidden")) {
                renderBrainGraph();
            }
        } catch (e) {
            showToast("Knowledge pull-in failed: " + e, "error");
        }
    });

    // In-Place Markdown Editor
    document.getElementById("btnEditPage").addEventListener("click", () => {
        togglePageEditor();
    });

    document.getElementById("btnSavePage").addEventListener("click", async () => {
        await saveCurrentPageEdits();
    });

    // Refresh Brain Graph Physics
    document.getElementById("btnRefreshGraph").addEventListener("click", () => {
        renderBrainGraph();
    });

    // Download APKG button in header
    document.getElementById("btnDownloadApkg").addEventListener("click", () => {
        downloadAnkiDeck();
    });

    // FTS5 Search Input
    const searchInput = document.getElementById("wikiSearchInput");
    let debounceTimer;
    searchInput.addEventListener("input", (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();
        debounceTimer = setTimeout(() => {
            if (query.length > 1) {
                performWikiSearch(query);
            } else {
                loadWikiTree();
            }
        }, 300);
    });

    // Contextual Search Toggle Listener
    const chkContextual = document.getElementById("chkContextualSearch");
    if (chkContextual) {
        chkContextual.addEventListener("change", () => {
            const query = (document.getElementById("wikiSearchInput")?.value || "").trim();
            if (query.length > 1) {
                performWikiSearch(query);
            }
        });
    }

    // Socratic Topic Guidance & Challenge Buttons
    const btnTargeted = document.getElementById("btnTargetedChallenge");
    if (btnTargeted) {
        btnTargeted.addEventListener("click", () => {
            const topic = (document.getElementById("vignetteTopicInput")?.value || "").trim();
            const guidance = (document.getElementById("vignetteGuidanceInput")?.value || "").trim();
            const domain = document.getElementById("vignetteDomainSelect")?.value || "";
            loadVignette(topic, guidance, domain);
        });
    }

    // Next Vignette Button
    document.getElementById("btnNewVignette").addEventListener("click", () => {
        const topic = (document.getElementById("vignetteTopicInput")?.value || "").trim();
        const guidance = (document.getElementById("vignetteGuidanceInput")?.value || "").trim();
        const domain = document.getElementById("vignetteDomainSelect")?.value || "";
        loadVignette(topic, guidance, domain);
    });

    // Submit Answer Button
    document.getElementById("btnSubmitAnswer").addEventListener("click", () => {
        submitAnswer();
    });

    // AnkiConnect sync
    const btnSyncAnki = document.getElementById("btnSyncAnkiConnect");
    if (btnSyncAnki) {
        btnSyncAnki.addEventListener("click", async () => {
            showToast("Connecting to AnkiConnect at 127.0.0.1:8765...", "info");
            try {
                const resp = await fetch("/api/anki/sync_ankiconnect", { method: "POST" });
                const data = await resp.json();
                if (data.success) {
                    showToast(`Synced ${data.synced_count} cards to Anki Desktop!`, "success");
                } else {
                    showToast(data.message, "error");
                }
            } catch (e) {
                showToast("Could not reach AnkiConnect.", "error");
            }
        });
    }

    // Recompile from Wiki button
    const btnRecompile = document.getElementById("btnRecompileAnki");
    if (btnRecompile) {
        btnRecompile.addEventListener("click", recompileAnkiFromWiki);
    }

    // Anki Mission Control Filters
    const ankiCourse = document.getElementById("ankiCourseFilter");
    if (ankiCourse) ankiCourse.addEventListener("change", () => loadAnkiCards());

    const ankiSystem = document.getElementById("ankiSystemFilter");
    if (ankiSystem) ankiSystem.addEventListener("change", () => loadAnkiCards());

    const ankiType = document.getElementById("ankiTypeFilter");
    if (ankiType) ankiType.addEventListener("change", () => loadAnkiCards());

    const ankiMastery = document.getElementById("ankiMasteryFilter");
    if (ankiMastery) ankiMastery.addEventListener("change", () => loadAnkiCards());

    const ankiClozeMode = document.getElementById("ankiClozeModeFilter");
    if (ankiClozeMode) ankiClozeMode.addEventListener("change", () => loadAnkiCards());

    const ankiSearch = document.getElementById("ankiSearchInput");
    if (ankiSearch) {
        ankiSearch.addEventListener("input", () => {
            clearTimeout(ankiSearchDebounceTimer);
            ankiSearchDebounceTimer = setTimeout(() => loadAnkiCards(), 250);
        });
    }

    // Anki Mode Switcher
    const btnBrowseMode = document.getElementById("btnModeBrowseCards");
    if (btnBrowseMode) btnBrowseMode.addEventListener("click", () => setAnkiMode("browse"));

    const btnStudyMode = document.getElementById("btnModeStudyCards");
    if (btnStudyMode) btnStudyMode.addEventListener("click", () => setAnkiMode("study"));

    // Study Player Arena Buttons
    const btnExitStudy = document.getElementById("btnExitStudyMode");
    if (btnExitStudy) btnExitStudy.addEventListener("click", () => setAnkiMode("browse"));

    const btnRevealAnswer = document.getElementById("btnStudyRevealAnswer");
    if (btnRevealAnswer) btnRevealAnswer.addEventListener("click", revealStudyAnswer);

    const btnStudyWiki = document.getElementById("btnStudyWikiLink");
    if (btnStudyWiki) {
        btnStudyWiki.addEventListener("click", () => {
            const card = ankiCurrentCards[ankiActiveCardIndex];
            if (card && card.wiki_slug) {
                openWikiFromCard(card.wiki_slug);
            }
        });
    }

    // Global Keyboard Shortcuts for Flashcard Study Player
    document.addEventListener("keydown", (e) => {
        const ankiView = document.getElementById("viewAnki");
        if (!ankiView || ankiView.classList.contains("hidden")) return;
        if (ankiViewMode !== "study") return;
        if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement?.tagName)) return;

        if (e.code === "Space") {
            e.preventDefault();
            if (!ankiIsStudyRevealed) {
                revealStudyAnswer();
            }
        } else if (e.key === "1" && ankiIsStudyRevealed) {
            rateActiveCard(1);
        } else if (e.key === "2" && ankiIsStudyRevealed) {
            rateActiveCard(2);
        } else if (e.key === "3" && ankiIsStudyRevealed) {
            rateActiveCard(3);
        } else if (e.key === "4" && ankiIsStudyRevealed) {
            rateActiveCard(4);
        } else if (e.key === "Escape") {
            setAnkiMode("browse");
        }
    });
}

// Conversation Capture & Discourse Digestion State
let convActiveTab = "paste"; // "paste", "file", "audio"
let convMediaRecorder = null;
let convAudioChunks = [];
let convRecordTimerInterval = null;
let convRecordSeconds = 0;
let convRecordedAudioBlob = null;

function setupConversationCaptureManager() {
    const btnOpen = document.getElementById("btnOpenCaptureConversation");
    if (btnOpen) {
        btnOpen.addEventListener("click", () => {
            openModal("modalCaptureConversation");
        });
    }

    // Tab buttons
    const tabs = [
        { id: "convTabBtnPaste", panel: "convPanelPaste", tabName: "paste" },
        { id: "convTabBtnFile", panel: "convPanelFile", tabName: "file" },
        { id: "convTabBtnAudio", panel: "convPanelAudio", tabName: "audio" }
    ];

    tabs.forEach(t => {
        const btn = document.getElementById(t.id);
        if (!btn) return;
        btn.addEventListener("click", () => {
            convActiveTab = t.tabName;
            tabs.forEach(o => {
                const b = document.getElementById(o.id);
                const p = document.getElementById(o.panel);
                if (b) {
                    b.classList.remove("active", "bg-teal-600/30", "text-teal-300", "border-teal-500/50");
                    b.classList.add("text-slate-400", "border-transparent");
                }
                if (p) p.classList.add("hidden");
            });

            btn.classList.add("active", "bg-teal-600/30", "text-teal-300", "border-teal-500/50");
            btn.classList.remove("text-slate-400", "border-transparent");
            const panel = document.getElementById(t.panel);
            if (panel) panel.classList.remove("hidden");
        });
    });

    // File selection
    const fileInput = document.getElementById("convFileInput");
    const fileStatusLabel = document.getElementById("convFileStatusLabel");
    if (fileInput && fileStatusLabel) {
        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (file) {
                fileStatusLabel.textContent = `Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
                const titleInput = document.getElementById("convTitleInput");
                if (titleInput && !titleInput.value.trim()) {
                    titleInput.value = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
                }
            } else {
                fileStatusLabel.textContent = "Click to select document or drag & drop";
            }
        });
    }

    // Audio recording
    const btnRecordToggle = document.getElementById("btnRecordToggle");
    const recordDot = document.getElementById("recordDot");
    const recordLabel = document.getElementById("recordLabel");
    const recordTimer = document.getElementById("convRecordTimer");
    const recordStatusMsg = document.getElementById("recordStatusMsg");
    const audioPreview = document.getElementById("convAudioPreview");

    if (btnRecordToggle) {
        btnRecordToggle.addEventListener("click", async () => {
            if (convMediaRecorder && convMediaRecorder.state === "recording") {
                // Stop recording
                convMediaRecorder.stop();
                if (recordDot) recordDot.classList.add("hidden");
                if (recordLabel) recordLabel.textContent = "🔴 Record New";
                if (recordStatusMsg) recordStatusMsg.textContent = "Recording saved! Ready to transcribe or digest.";
                if (convRecordTimerInterval) {
                    clearInterval(convRecordTimerInterval);
                    convRecordTimerInterval = null;
                }
            } else {
                // Start recording
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    convAudioChunks = [];
                    convMediaRecorder = new MediaRecorder(stream);

                    convMediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            convAudioChunks.push(event.data);
                        }
                    };

                    convMediaRecorder.onstop = () => {
                        convRecordedAudioBlob = new Blob(convAudioChunks, { type: convMediaRecorder.mimeType || "audio/webm" });
                        if (audioPreview) {
                            audioPreview.src = URL.createObjectURL(convRecordedAudioBlob);
                            audioPreview.classList.remove("hidden");
                        }
                        stream.getTracks().forEach(track => track.stop());
                    };

                    convMediaRecorder.start();
                    convRecordSeconds = 0;
                    if (recordTimer) recordTimer.textContent = "00:00";
                    convRecordTimerInterval = setInterval(() => {
                        convRecordSeconds++;
                        const m = String(Math.floor(convRecordSeconds / 60)).padStart(2, "0");
                        const s = String(convRecordSeconds % 60).padStart(2, "0");
                        if (recordTimer) recordTimer.textContent = `${m}:${s}`;
                    }, 1000);

                    if (recordDot) recordDot.classList.remove("hidden");
                    if (recordLabel) recordLabel.textContent = "⏹️ Stop Recording";
                    if (recordStatusMsg) recordStatusMsg.textContent = "Recording in progress... speak clearly into mic.";
                } catch (err) {
                    console.error("Microphone access failed", err);
                    showToast("Microphone access denied or unavailable: " + err.message, "error");
                }
            }
        });
    }

    // Transcribe audio button
    const btnTranscribe = document.getElementById("btnTranscribeAudio");
    const transcribeProgress = document.getElementById("transcribeProgress");
    const transcribedTextArea = document.getElementById("convAudioTranscribedText");
    const audioFileInput = document.getElementById("convAudioFileInput");

    if (btnTranscribe) {
        btnTranscribe.addEventListener("click", async () => {
            let audioBlobOrFile = null;
            let filename = "recorded_audio.webm";

            if (audioFileInput && audioFileInput.files && audioFileInput.files[0]) {
                audioBlobOrFile = audioFileInput.files[0];
                filename = audioBlobOrFile.name;
            } else if (convRecordedAudioBlob) {
                audioBlobOrFile = convRecordedAudioBlob;
                filename = "live_recording.webm";
            }

            if (!audioBlobOrFile) {
                showToast("Please record audio or select an audio file first.", "info");
                return;
            }

            if (transcribeProgress) transcribeProgress.classList.remove("hidden");
            btnTranscribe.disabled = true;
            showToast("Transcribing speech via speech-to-text model...", "info");

            try {
                const formData = new FormData();
                formData.append("audio_file", audioBlobOrFile, filename);

                const resp = await fetch("/api/conversation/transcribe", {
                    method: "POST",
                    body: formData
                });
                const data = await resp.json();

                if (data.success && data.text) {
                    if (transcribedTextArea) {
                        transcribedTextArea.value = data.text;
                    }
                    showToast(`Transcription complete (${data.word_count || 0} words)!`, "success");
                } else {
                    showToast(data.message || "Audio transcription failed.", "error");
                }
            } catch (err) {
                showToast("Transcription failed: " + err.message, "error");
            } finally {
                if (transcribeProgress) transcribeProgress.classList.add("hidden");
                btnTranscribe.disabled = false;
            }
        });
    }

    // Submit Digestion Button
    const btnSubmit = document.getElementById("btnSubmitDigestConversation");
    if (btnSubmit) {
        btnSubmit.addEventListener("click", async () => {
            const titleInput = document.getElementById("convTitleInput");
            const participantsInput = document.getElementById("convParticipantsInput");
            const domainInput = document.getElementById("convDomainInput");
            const tagsInput = document.getElementById("convTagsInput");

            let title = titleInput?.value.trim() || "";
            const participants = participantsInput?.value.trim() || "";
            const domain = domainInput?.value.trim() || "Deep Learning & Computer Vision";
            const tagsRaw = tagsInput?.value.trim() || "";
            const tags = tagsRaw ? tagsRaw.split(",").map(t => t.trim()).filter(Boolean) : [];

            if (convActiveTab === "file") {
                const file = fileInput?.files?.[0];
                if (!file) {
                    showToast("Please choose a file to upload or switch to the Paste tab.", "info");
                    return;
                }
                if (!title) {
                    title = file.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
                }

                closeModal("modalCaptureConversation");
                showToast(`Uploading & digesting conversation from "${file.name}"...`, "info");

                try {
                    const formData = new FormData();
                    formData.append("file", file);
                    formData.append("title", title);
                    formData.append("participants", participants);
                    formData.append("domain", domain);
                    formData.append("tags", JSON.stringify(tags));

                    const resp = await fetch("/api/conversation/upload_and_digest", {
                        method: "POST",
                        body: formData
                    });
                    const data = await resp.json();

                    if (data.success) {
                        handleDigestionSuccess(data);
                    } else {
                        showToast(data.message || "Conversation digestion failed.", "error");
                    }
                } catch (err) {
                    showToast("Digestion error: " + err.message, "error");
                }
            } else if (convActiveTab === "audio") {
                const transcribedText = transcribedTextArea?.value.trim() || "";
                let audioBlobOrFile = null;
                let filename = "audio_memo.webm";

                if (audioFileInput?.files?.[0]) {
                    audioBlobOrFile = audioFileInput.files[0];
                    filename = audioBlobOrFile.name;
                } else if (convRecordedAudioBlob) {
                    audioBlobOrFile = convRecordedAudioBlob;
                }

                if (!transcribedText && !audioBlobOrFile) {
                    showToast("Please record or upload audio, or enter transcribed notes.", "info");
                    return;
                }

                if (!title) {
                    title = `Voice Memo: ${new Date().toLocaleDateString()}`;
                }

                closeModal("modalCaptureConversation");
                showToast(`Digesting audio conversation "${title}"...`, "info");

                try {
                    let resp;
                    if (transcribedText) {
                        resp = await fetch("/api/conversation/digest", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                title,
                                raw_text: transcribedText,
                                participants,
                                domain,
                                tags
                            })
                        });
                    } else {
                        const formData = new FormData();
                        formData.append("file", audioBlobOrFile, filename);
                        formData.append("title", title);
                        formData.append("participants", participants);
                        formData.append("domain", domain);
                        formData.append("tags", JSON.stringify(tags));

                        resp = await fetch("/api/conversation/upload_and_digest", {
                            method: "POST",
                            body: formData
                        });
                    }
                    const data = await resp.json();
                    if (data.success) {
                        handleDigestionSuccess(data);
                    } else {
                        showToast(data.message || "Audio conversation digestion failed.", "error");
                    }
                } catch (err) {
                    showToast("Digestion error: " + err.message, "error");
                }
            } else {
                // Paste text tab
                const rawText = document.getElementById("convTextInput")?.value.trim() || "";
                if (!rawText) {
                    showToast("Please paste or type conversation notes or transcript.", "info");
                    return;
                }
                if (!title) {
                    const firstLine = rawText.split("\n")[0].replace(/^[#\-*\s]+/, "").trim();
                    title = firstLine.slice(0, 45) || `Discourse: ${new Date().toLocaleDateString()}`;
                }

                closeModal("modalCaptureConversation");
                showToast(`Digesting conversation "${title}"...`, "info");

                try {
                    const resp = await fetch("/api/conversation/digest", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            title,
                            raw_text: rawText,
                            participants,
                            domain,
                            tags
                        })
                    });
                    const data = await resp.json();
                    if (data.success) {
                        handleDigestionSuccess(data);
                    } else {
                        showToast(data.message || "Conversation digestion failed.", "error");
                    }
                } catch (err) {
                    showToast("Digestion error: " + err.message, "error");
                }
            }
        });
    }

    async function handleDigestionSuccess(data) {
        showToast(`Digested "${data.title}"! Compounded concepts & ${data.staged_flashcards || 0} flashcards.`, "success");
        const titleInput = document.getElementById("convTitleInput");
        if (titleInput) titleInput.value = "";
        const participantsInput = document.getElementById("convParticipantsInput");
        if (participantsInput) participantsInput.value = "";
        const textInput = document.getElementById("convTextInput");
        if (textInput) textInput.value = "";
        const transText = document.getElementById("convAudioTranscribedText");
        if (transText) transText.value = "";
        const fInput = document.getElementById("convFileInput");
        if (fInput) fInput.value = "";
        const fLabel = document.getElementById("convFileStatusLabel");
        if (fLabel) fLabel.textContent = "Click to select document or drag & drop";
        const aInput = document.getElementById("convAudioFileInput");
        if (aInput) aInput.value = "";
        convRecordedAudioBlob = null;

        await loadWikiTree();
        if (data.rel_path) {
            await loadWikiPage(data.rel_path);
        }
        await loadStatus();
        await loadAnkiCards();
        if (!document.getElementById("viewGraph").classList.contains("hidden")) {
            renderBrainGraph();
        }
    }
}

// ==========================================
// RESEARCH PAPER DEEP DIGESTION & VISUAL SYNTHESIS
// ==========================================

function setupPaperImportManager() {
    const btnOpen = document.getElementById("btnOpenImportPaper");
    if (btnOpen) {
        btnOpen.addEventListener("click", () => {
            openModal("modalImportPaper");
        });
    }

    const btnFetch = document.getElementById("btnFetchPaperLink");
    const arxivInput = document.getElementById("paperArxivInput");

    async function fetchArxivDetails() {
        const val = arxivInput?.value.trim() || "";
        if (!val) {
            showToast("Please enter an arXiv ID or URL first.", "info");
            return;
        }
        if (btnFetch) {
            btnFetch.disabled = true;
            btnFetch.innerHTML = `<span>⏳</span> Fetching...`;
        }
        try {
            const resp = await fetch(`/api/paper/fetch_arxiv?url=${encodeURIComponent(val)}`);
            const data = await resp.json();
            if (data.success && data.metadata) {
                const m = data.metadata;
                const titleInput = document.getElementById("paperTitleInput");
                const abstractInput = document.getElementById("paperAbstractInput");
                const tagsInput = document.getElementById("paperTagsInput");
                if (titleInput && m.title) titleInput.value = m.title;
                if (abstractInput && m.abstract) abstractInput.value = m.abstract;
                if (tagsInput && m.categories && m.categories.length > 0 && !tagsInput.value) {
                    tagsInput.value = m.categories.join(", ");
                }
                showToast(`Fetched paper metadata: "${m.title.slice(0, 45)}..."`, "success");
            } else {
                showToast(data.message || "Could not fetch details. Please fill in title/abstract manually.", "info");
            }
        } catch (err) {
            console.warn("fetchArxivDetails error", err);
            showToast("Network error fetching paper link details.", "error");
        } finally {
            if (btnFetch) {
                btnFetch.disabled = false;
                btnFetch.innerHTML = `<span>⚡</span> Fetch Details`;
            }
        }
    }

    if (btnFetch) {
        btnFetch.addEventListener("click", fetchArxivDetails);
    }

    if (arxivInput) {
        // Auto-fetch on blur if title is currently empty
        arxivInput.addEventListener("blur", () => {
            const titleInput = document.getElementById("paperTitleInput");
            if (arxivInput.value.trim() && (!titleInput || !titleInput.value.trim())) {
                fetchArxivDetails();
            }
        });
        // Also support hitting Enter on the arXiv input
        arxivInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                fetchArxivDetails();
            }
        });
    }

    const btnSubmit = document.getElementById("btnSubmitImportPaper");
    if (btnSubmit) {
        btnSubmit.addEventListener("click", async () => {
            const titleInput = document.getElementById("paperTitleInput");
            const tagsInput = document.getElementById("paperTagsInput");
            const abstractInput = document.getElementById("paperAbstractInput");
            const contentInput = document.getElementById("paperContentInput");

            const arxiv = arxivInput?.value.trim() || "";
            let title = titleInput?.value.trim() || "";
            const abstract = abstractInput?.value.trim() || "";
            const content = contentInput?.value.trim() || "";
            const tagsRaw = tagsInput?.value.trim() || "";
            const tags = tagsRaw ? tagsRaw.split(",").map(t => t.trim()).filter(Boolean) : [];

            if (!title && !arxiv) {
                showToast("Please provide an arXiv URL/ID or enter a paper title.", "info");
                return;
            }

            if (!title && arxiv) {
                title = "arXiv Paper " + arxiv.replace(/https?:\/\/arxiv\.org\/(abs|pdf)\//, "").replace(/\.pdf$/, "");
            }

            closeModal("modalImportPaper");
            showToast(`Digesting paper "${title}" & synthesizing visual architecture...`, "info");

            try {
                const resp = await fetch("/api/wiki/import_paper", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        title,
                        abstract,
                        content,
                        arxiv_id: arxiv,
                        tags
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    handlePaperSuccess(data);
                } else {
                    showToast(data.message || "Paper digestion failed.", "error");
                }
            } catch (err) {
                showToast("Digestion error: " + err.message, "error");
            }
        });
    }

    async function handlePaperSuccess(data) {
        const figs = data.figures_count !== undefined ? data.figures_count : (data.extracted_figures?.length || 0);
        showToast(`Deeply digested "${data.title}"! Synthesized architecture & visual diagrams.`, "success");

        if (document.getElementById("paperTitleInput")) document.getElementById("paperTitleInput").value = "";
        if (document.getElementById("paperTagsInput")) document.getElementById("paperTagsInput").value = "";
        if (document.getElementById("paperArxivInput")) document.getElementById("paperArxivInput").value = "";
        if (document.getElementById("paperAbstractInput")) document.getElementById("paperAbstractInput").value = "";
        if (document.getElementById("paperContentInput")) document.getElementById("paperContentInput").value = "";

        await loadWikiTree();
        if (data.rel_path) {
            await loadWikiPage(data.rel_path);
        }
        await loadStatus();
        await loadAnkiCards();
        if (!document.getElementById("viewGraph").classList.contains("hidden")) {
            renderBrainGraph();
        }
    }
}

// Modal helpers
function openModal(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.remove("hidden");
        el.classList.add("flex");
    }
}

function closeModal(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.add("hidden");
        el.classList.remove("flex");
    }
}

// Load global status & metrics
async function loadStatus() {
    try {
        const resp = await fetch("/api/status");
        const data = await resp.json();
        const hDays = document.getElementById("headerDaysLeft");
        if (hDays) hDays.textContent = `${data.days_to_exam} days`;
        const hExam = document.getElementById("headerExamTitle");
        if (hExam) hExam.textContent = (data.target_exam || "").split(" ")[0];
        const tabCount = document.getElementById("tabCardCount");
        if (tabCount) tabCount.textContent = data.staged_flashcards;
    } catch (e) {
        console.error("Status load failed", e);
    }
}

// Collapsible accordion toggle for sidebar sections
function toggleTreeSection(sectionId) {
    const el = document.getElementById(sectionId);
    const icon = document.getElementById(`icon-${sectionId}`);
    if (!el) return;
    const isHidden = el.classList.toggle("hidden");
    if (icon) {
        icon.style.transform = isHidden ? "rotate(-90deg)" : "rotate(0deg)";
    }
}

// Robust KaTeX Math Tokenizer & Markdown Renderer
function renderMarkdownWithMath(markdownText) {
    if (!markdownText) return "";

    const mathBlocks = [];
    let mathIndex = 0;

    // 1. Protect block math $$...$$
    // Use alphanumeric token without underscores/asterisks so Marked won't parse it as bold/italic!
    let text = markdownText.replace(/\$\$([\s\S]+?)\$\$/g, (match, math) => {
        const id = `KATEXBLOCKTOKEN${mathIndex++}END`;
        mathBlocks.push({ id, math: math.trim(), display: true });
        return `\n\n${id}\n\n`;
    });

    // 2. Protect inline math $...$
    text = text.replace(/\$([^\$\n\r]+?)\$/g, (match, math) => {
        const id = `KATEXINLINETOKEN${mathIndex++}END`;
        mathBlocks.push({ id, math: math.trim(), display: false });
        return id;
    });

    // 3. Normalize GitHub / USMLE callouts (> [!NOTE] Title)
    text = text.replace(/^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)\](?:\s*(.*?))?$/gim, (match, type, title) => {
        const t = type.toUpperCase();
        const cleanTitle = title ? title.trim() : "";
        return `> **[${t}: ${cleanTitle}]**`;
    });

    // 4. Parse markdown with Marked.js
    let html = marked.parse(text);

    // 4.5. Render Mermaid Architectural Diagrams
    html = html.replace(/<pre><code class="(?:language-)?mermaid">([\s\S]*?)<\/code><\/pre>/gi, (match, code) => {
        const txt = document.createElement("textarea");
        txt.innerHTML = code;
        const decoded = txt.value.trim();
        return `<div class="mermaid my-4 p-4 bg-slate-900/90 rounded-xl border border-indigo-500/30 overflow-x-auto text-center flex justify-center">${decoded}</div>`;
    });

    // 5. Convert [[wikilinks]] to clickable links
    html = html.replace(/\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]/g, (match, target, text) => {
        const label = text || target;
        let targetPath = target.trim();
        if (!targetPath.endsWith(".md")) targetPath += ".md";
        if (!targetPath.includes("/")) {
            targetPath = `concepts/${targetPath}`;
        }
        return `<span class="wikilink" onclick="loadWikiPage('${targetPath}')">${label}</span>`;
    });

    // 6. Style Alert callout boxes
    html = html.replace(/<blockquote>\s*<p><strong>\[(NOTE|TIP|WARNING|CAUTION|IMPORTANT):\s*(.*?)\]<\/strong>(?:<br>)?\s*([\s\S]*?)<\/p>\s*<\/blockquote>/gi, (match, type, header, content) => {
        const t = type.toUpperCase();
        let boxClass = 'callout-note';
        let icon = '📌';
        let defaultTitle = 'Technical Note';
        if (t === 'TIP') {
            boxClass = 'callout-tip';
            icon = '💡';
            defaultTitle = 'Key Insight & Mathematical Principle';
        } else if (t === 'CAUTION') {
            boxClass = 'callout-caution';
            icon = '🚨';
            defaultTitle = 'Engineering Trap & Pitfall';
        } else if (t === 'WARNING' || t === 'IMPORTANT') {
            boxClass = 'callout-warning';
            icon = '⚠️';
            defaultTitle = 'Critical System Constraint';
        }
        const displayHeader = header && header.trim() ? header.trim() : defaultTitle;
        return `
            <div class="callout-box ${boxClass}">
                <div class="callout-header"><span>${icon}</span> <span>${displayHeader}</span></div>
                <div class="callout-content">${content}</div>
            </div>
        `;
    });

    // 7. Restore and render KaTeX math expressions
    mathBlocks.forEach(({ id, math, display }) => {
        let renderedMath = "";
        // Normalize double-escaped backslashes before LaTeX commands (e.g., \\mathcal -> \mathcal)
        const cleanMath = math.replace(/\\\\([a-zA-Z_{}])/g, '\\$1');
        try {
            if (window.katex) {
                renderedMath = katex.renderToString(cleanMath, {
                    displayMode: display,
                    throwOnError: false
                });
            } else {
                renderedMath = display
                    ? `<div class="katex-display font-mono text-indigo-300 text-xs py-2 my-2 bg-slate-900/60 rounded px-3 border border-indigo-900/40">${cleanMath}</div>`
                    : `<code class="bg-slate-800 text-indigo-300 px-1 rounded font-mono">${cleanMath}</code>`;
            }
        } catch (err) {
            renderedMath = `<span class="text-rose-400 font-mono text-xs">${cleanMath}</span>`;
        }

        // Handle standalone display formula paragraph wrapping
        if (display) {
            const pWrapped = new RegExp(`<p>\\s*${id}\\s*<\\/p>`, 'g');
            if (pWrapped.test(html)) {
                html = html.replace(pWrapped, renderedMath);
            }
        }
        html = html.split(id).join(renderedMath);
    });

    return html;
}

// Load Wiki Tree with Course Filtering
async function loadWikiTree() {
    try {
        const filterSelect = document.getElementById("wikiCourseFilter");
        const selectedCourse = filterSelect ? filterSelect.value : "all";

        const resp = await fetch(`/api/wiki/tree?course=${encodeURIComponent(selectedCourse)}`);
        const tree = await resp.json();
        currentTreeData = tree;

        let totalItems = 0;
        ["papers", "course_sessions", "conversations", "concepts", "entities", "differentials", "exam_traps"].forEach(k => {
            totalItems += (tree[k] || []).length;
        });

        const badgeEl = document.getElementById("activeCourseCountBadge");
        if (badgeEl) {
            if (selectedCourse === "vision") {
                badgeEl.textContent = `3D Vision (${totalItems})`;
            } else if (selectedCourse === "eecs") {
                badgeEl.textContent = `MIT 6.033 (${totalItems})`;
            } else {
                badgeEl.textContent = `All (${totalItems})`;
            }
        }

        renderTreeCategory("listPapers", "countPapers", tree.papers || []);
        renderTreeCategory("listLectures", "countLectures", tree.course_sessions || []);
        renderTreeCategory("listConversations", "countConversations", tree.conversations || []);
        renderTreeCategory("listConcepts", "countConcepts", tree.concepts || []);
        renderTreeCategory("listDifferentials", "countDifferentials", tree.differentials || []);
        renderTreeCategory("listTraps", "countTraps", tree.exam_traps || []);

        // Apply any active entity subfilter (models, algorithms, frameworks, or all)
        filterEntities(currentEntitySubfilter || "all");
    } catch (e) {
        console.error("Wiki tree load error", e);
    }
}

let currentTreeData = {};
let currentEntitySubfilter = "all";
let currentWikiSectionFilter = "all";

function filterEntities(subcat) {
    currentEntitySubfilter = subcat;
    // Update subfilter button styles
    const subfilterBtnMap = {
        all: "filterEntAll",
        architectures: "filterEntArchs",
        models: "filterEntArchs",
        algorithms: "filterEntAlgos",
        frameworks: "filterEntFrameworks"
    };

    ["filterEntAll", "filterEntArchs", "filterEntModels", "filterEntAlgos", "filterEntFrameworks"].forEach(id => {
        const btn = document.getElementById(id);
        if (!btn) return;
        const targetBtnId = subfilterBtnMap[subcat] || "filterEntAll";
        if (id === targetBtnId) {
            btn.className = "entity-subfilter bg-slate-700 text-slate-200 px-1.5 py-0.5 rounded font-medium transition shadow-sm";
        } else {
            btn.className = "entity-subfilter text-slate-400 hover:text-slate-200 px-1.5 py-0.5 rounded font-medium transition";
        }
    });

    const allEntities = (currentTreeData && currentTreeData.entities) || [];
    let filtered = allEntities;
    if (subcat === "models" || subcat === "architectures") {
        filtered = allEntities.filter(e => {
            const k = ((e.entity_type || "") + " " + (e.category || "") + " " + (e.tags || "") + " " + e.title + " " + e.slug).toLowerCase();
            return k.includes("architecture") || k.includes("model") || k.includes("backbone") || k.includes("encoder") || k.includes("decoder") || k.includes("transformer") || k.includes("nerf") || k.includes("splat") || k.includes("dust3r") || k.includes("representation");
        });
    } else if (subcat === "algorithms") {
        filtered = allEntities.filter(e => {
            const k = ((e.entity_type || "") + " " + (e.category || "") + " " + (e.tags || "") + " " + e.title + " " + e.slug).toLowerCase();
            return k.includes("algorithm") || k.includes("rasterizer") || k.includes("attention") || k.includes("estimator") || k.includes("density-control") || k.includes("matching") || k.includes("solver") || k.includes("optimization") || k.includes("optimizer") || k.includes("sampling");
        });
    } else if (subcat === "frameworks") {
        filtered = allEntities.filter(e => {
            const k = ((e.entity_type || "") + " " + (e.category || "") + " " + (e.tags || "") + " " + e.title + " " + e.slug).toLowerCase();
            return k.includes("framework") || k.includes("library") || k.includes("pipeline") || k.includes("cuda") || k.includes("pytorch") || k.includes("diffusers") || k.includes("engine") || k.includes("colmap") || k.includes("tool");
        });
    }
    renderTreeCategory("listEntities", "countEntities", filtered);
}

function filterWikiSection(section) {
    currentWikiSectionFilter = section;
    const pillIds = {
        all: "btnCatFilterAll",
        papers: "btnCatFilterPapers",
        conversations: "btnCatFilterConvs",
        models: "btnCatFilterModels",
        algorithms: "btnCatFilterAlgos",
        concepts: "btnCatFilterConcepts",
        differentials: "btnCatFilterDiffs",
        traps: "btnCatFilterTraps"
    };

    Object.entries(pillIds).forEach(([secKey, btnId]) => {
        const btn = document.getElementById(btnId);
        if (!btn) return;
        if (secKey === section) {
            btn.className = "wiki-cat-pill bg-indigo-600 text-white px-2 py-0.5 rounded-full font-medium transition shadow";
        } else {
            btn.className = "wiki-cat-pill bg-slate-800 text-slate-300 hover:bg-slate-700 px-2 py-0.5 rounded-full font-medium transition";
        }
    });

    const secCore = document.getElementById("treeSecCore");
    const secPapers = document.getElementById("treeSecPapers");
    const secLectures = document.getElementById("treeSecLectures");
    const secConvs = document.getElementById("treeSecConversations");
    const secConcepts = document.getElementById("treeSecConcepts");
    const secEntities = document.getElementById("treeSecEntities");
    const secDiffs = document.getElementById("treeSecDiffs");
    const secTraps = document.getElementById("treeSecTraps");

    if (section === "all") {
        [secCore, secPapers, secLectures, secConvs, secConcepts, secEntities, secDiffs, secTraps].forEach(s => s && s.classList.remove("hidden"));
        filterEntities("all");
    } else if (section === "papers") {
        [secCore, secLectures, secConvs, secConcepts, secEntities, secDiffs, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secPapers) secPapers.classList.remove("hidden");
    } else if (section === "conversations") {
        [secCore, secPapers, secLectures, secConcepts, secEntities, secDiffs, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secConvs) secConvs.classList.remove("hidden");
    } else if (section === "models") {
        [secCore, secPapers, secLectures, secConvs, secConcepts, secDiffs, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secEntities) secEntities.classList.remove("hidden");
        filterEntities("architectures");
    } else if (section === "algorithms") {
        [secCore, secPapers, secLectures, secConvs, secConcepts, secDiffs, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secEntities) secEntities.classList.remove("hidden");
        filterEntities("algorithms");
    } else if (section === "concepts") {
        [secCore, secPapers, secLectures, secConvs, secEntities, secDiffs, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secConcepts) secConcepts.classList.remove("hidden");
    } else if (section === "differentials") {
        [secCore, secPapers, secLectures, secConvs, secConcepts, secEntities, secTraps].forEach(s => s && s.classList.add("hidden"));
        if (secDiffs) secDiffs.classList.remove("hidden");
    } else if (section === "traps") {
        [secCore, secPapers, secLectures, secConvs, secConcepts, secEntities, secDiffs].forEach(s => s && s.classList.add("hidden"));
        if (secTraps) secTraps.classList.remove("hidden");
    }
}

function renderTreeCategory(listId, countId, items) {
    const listEl = document.getElementById(listId);
    const countEl = document.getElementById(countId);
    if (!listEl) return;

    countEl.textContent = items.length;
    listEl.innerHTML = "";

    if (items.length === 0) {
        listEl.innerHTML = `<li class="text-[11px] text-slate-500 italic px-2 py-0.5">None in selected filter</li>`;
        return;
    }

    items.forEach(item => {
        const li = document.createElement("li");
        const isActive = currentLoadedPath === item.rel_path;

        // Domain-aware category & type badge
        let sysPill = "";
        const etype = (item.entity_type || item.category || "").toLowerCase();
        const sysLower = (item.system || item.tags || item.course || "").toLowerCase();
        const domLower = (item.domain || "").toLowerCase();

        if (etype.includes("paper") || (item.rel_path && item.rel_path.startsWith("papers/"))) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-cyan-950 text-cyan-300 border border-cyan-800/60">Paper</span>`;
        } else if (etype.includes("conversation") || item.is_conversation || (item.rel_path && item.rel_path.startsWith("conversations/"))) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-teal-950 text-teal-300 border border-teal-800/60">Discourse</span>`;
        } else if (etype.includes("formulation") || (item.category && item.category.toLowerCase().includes("formulation"))) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-fuchsia-950 text-fuchsia-300 border border-fuchsia-800/60">Formula</span>`;
        } else if (etype.includes("theoretical") || (item.category && item.category.toLowerCase().includes("theoretical")) || (item.rel_path && item.rel_path.startsWith("concepts/"))) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-indigo-950 text-indigo-300 border border-indigo-800/60">Theory</span>`;
        } else if (etype.includes("architecture") || etype.includes("model") || etype.includes("backbone") || etype.includes("transformer") || etype.includes("splat") || etype.includes("nerf")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-purple-950 text-purple-300 border border-purple-800/60">Arch</span>`;
        } else if (etype.includes("algorithm") || etype.includes("estimator") || etype.includes("rasterizer") || etype.includes("flow")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-cyan-950 text-cyan-300 border border-cyan-800/60">Algo</span>`;
        } else if (etype.includes("framework") || etype.includes("library") || etype.includes("store") || etype.includes("tool") || etype.includes("pipeline")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-amber-950 text-amber-300 border border-amber-800/60">Framework</span>`;
        } else if (etype.includes("protocol")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-blue-950 text-blue-300 border border-blue-800/60">Proto</span>`;
        } else if (sysLower.includes("vision") || sysLower.includes("3d") || domLower.includes("vision") || domLower.includes("robot")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-indigo-950 text-indigo-300 border border-indigo-800/60">3D/CV</span>`;
        } else if (sysLower.includes("distributed") || sysLower.includes("6.033") || domLower.includes("computer")) {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-emerald-950 text-emerald-300 border border-emerald-800/60">Sys</span>`;
        } else {
            sysPill = `<span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-medium bg-slate-800 text-slate-300 border border-slate-700">Core</span>`;
        }

        li.innerHTML = `
            <button class="w-full text-left px-2 py-1 rounded hover:bg-slate-700/60 text-slate-300 text-xs truncate flex items-center justify-between group transition ${isActive ? 'tree-item-active' : ''}" onclick="loadWikiPage('${item.rel_path}')">
                <span class="truncate pr-1">${item.title}</span>
                <span class="flex items-center gap-1 flex-shrink-0">
                    ${sysPill}
                    <span class="text-[10px] text-slate-500 group-hover:text-slate-300">→</span>
                </span>
            </button>
        `;
        listEl.appendChild(li);
    });
}

// Perform SQLite FTS5 & Anthropic Contextual Search
async function performWikiSearch(query) {
    try {
        const useCtx = document.getElementById("chkContextualSearch")?.checked ?? true;
        const mode = useCtx ? "contextual" : "standard";
        const badgeEl = document.getElementById("searchResultModeBadge");
        if (badgeEl) {
            badgeEl.textContent = useCtx ? "Hybrid BM25+Vector" : "FTS5 Lexical";
        }

        const resp = await fetch(`/api/wiki/search?q=${encodeURIComponent(query)}&mode=${mode}`);
        const data = await resp.json();
        const listConcepts = document.getElementById("listConcepts");
        
        const modeLabel = useCtx ? "✨ Contextual Hybrid Search" : "FTS5 Lexical Search";
        listConcepts.innerHTML = `<div class="text-[11px] font-bold text-amber-300 px-2 py-1 flex items-center justify-between"><span>${modeLabel}</span><span class="text-[10px] text-slate-400 font-normal">"${query}"</span></div>`;

        if (!data.results || data.results.length === 0) {
            listConcepts.innerHTML += `<div class="text-[11px] text-slate-500 italic px-2 py-1">No matching concepts or contextual chunks found</div>`;
            return;
        }

        data.results.forEach(res => {
            const item = document.createElement("div");
            item.className = "p-2 bg-slate-900/70 rounded-lg border border-slate-700/80 mb-1.5 cursor-pointer hover:border-indigo-500 transition group shadow-sm";
            item.onclick = () => loadWikiPage(res.rel_path);

            const secBadge = res.section_title ? `<span class="text-[9px] bg-slate-800 text-indigo-300 px-1.5 py-0.5 rounded border border-slate-700 font-mono font-medium">${res.section_title}</span>` : "";
            const scoreBadge = (res.rerank_score !== undefined && res.rerank_score > 0) ? `<span class="text-[9px] text-sky-400 font-mono">Score: ${res.rerank_score}</span>` : "";
            const ctxBadge = res.context_summary ? `<div class="text-[10px] text-emerald-400/90 italic bg-emerald-950/30 p-1.5 rounded mt-1 border border-emerald-900/30 leading-snug">Context: ${res.context_summary}</div>` : "";

            item.innerHTML = `
                <div class="flex items-center justify-between gap-1">
                    <span class="font-semibold text-indigo-300 text-xs group-hover:text-indigo-200 truncate">${res.title}</span>
                    <span class="flex items-center gap-1 flex-shrink-0">${secBadge}${scoreBadge}</span>
                </div>
                ${ctxBadge}
                <div class="text-[10px] text-slate-400 mt-1 line-clamp-2 leading-relaxed">${res.match_snippet || ""}</div>
            `;
            listConcepts.appendChild(item);
        });
    } catch (e) {
        console.error("Search error", e);
    }
}

// Load a single Wiki page
async function loadWikiPage(relPath) {
    // Switch to Wiki view if in another tab
    document.getElementById("tabBtnWiki").click();

    // Reset editor if open
    isEditingPage = false;
    document.getElementById("pageEditorContainer").classList.add("hidden");
    document.getElementById("pageBody").classList.remove("hidden");
    document.getElementById("btnSavePage").classList.add("hidden");
    document.getElementById("btnEditPage").textContent = "✏️ Edit";

    try {
        const resp = await fetch(`/api/wiki/page?path=${encodeURIComponent(relPath)}`);
        if (!resp.ok) {
            showToast("Could not load page: " + relPath, "error");
            return;
        }
        const data = await resp.json();
        currentLoadedPath = data.rel_path;
        document.getElementById("pageTitle").textContent = data.title;
        document.getElementById("pagePath").textContent = data.rel_path;
        document.getElementById("pageBadge").textContent = data.rel_path.split("/")[0] || "wiki";

        // Update Course Badge in reader header
        const courseBadge = document.getElementById("pageCourseBadge");
        if (courseBadge) {
            const pLower = data.rel_path.toLowerCase();
            const cLower = (data.content || "").toLowerCase();
            if (pLower.startsWith("papers/")) {
                courseBadge.textContent = "Research Preprint";
                courseBadge.className = "text-xs font-semibold px-2 py-0.5 rounded bg-cyan-950/80 text-cyan-300 border border-cyan-700/60";
            } else if (pLower.startsWith("conversations/")) {
                courseBadge.textContent = "Discourse / Meeting";
                courseBadge.className = "text-xs font-semibold px-2 py-0.5 rounded bg-teal-950/80 text-teal-300 border border-teal-700/60";
            } else if (pLower.includes("course_sessions") || cLower.includes("vision") || pLower.includes("vision")) {
                courseBadge.textContent = "3D Vision / AI";
                courseBadge.className = "text-xs font-semibold px-2 py-0.5 rounded bg-indigo-900/60 text-indigo-300 border border-indigo-700/60";
            } else {
                courseBadge.textContent = "Paideia Core";
                courseBadge.className = "text-xs font-semibold px-2 py-0.5 rounded bg-slate-700 text-slate-300 border border-slate-600";
            }
        }

        document.getElementById("pageEditorTextarea").value = data.content;

        // Render Markdown with KaTeX math protection and USMLE callouts
        document.getElementById("pageBody").innerHTML = renderMarkdownWithMath(data.body);

        // Render synthesized Mermaid diagrams
        if (window.mermaid) {
            try {
                mermaid.run({ querySelector: '#pageBody .mermaid' });
            } catch (err) {
                console.warn("Mermaid rendering warning:", err);
            }
        }

        // Highlight the active page in the sidebar
        document.querySelectorAll("#wikiTreeContainer button").forEach(btn => {
            const clickAttr = btn.getAttribute("onclick") || "";
            if (clickAttr.includes(`'${data.rel_path}'`)) {
                btn.classList.add("tree-item-active");
            } else {
                btn.classList.remove("tree-item-active");
            }
        });

        // Trigger HippoRAG associative spreading activation for this page
        loadAssociativeRecall(relPath);

    } catch (e) {
        console.error("Load wiki page failed", e);
    }
}

// HippoRAG Associative Spreading Recall
async function loadAssociativeRecall(relPath) {
    const slug = relPath.split("/").pop().replace(".md", "");
    const tagsContainer = document.getElementById("associativeTags");
    tagsContainer.innerHTML = `<span class="text-[11px] text-slate-500 italic">Activating hippocampus...</span>`;

    try {
        const resp = await fetch(`/api/wiki/associative_recall?slug=${encodeURIComponent(slug)}&top_k=4`);
        const data = await resp.json();
        tagsContainer.innerHTML = "";

        if (!data.associative_concepts || data.associative_concepts.length === 0) {
            tagsContainer.innerHTML = `<span class="text-[11px] text-slate-500 italic">No associative pathways</span>`;
            return;
        }

        data.associative_concepts.forEach(c => {
            const badge = document.createElement("button");
            badge.className = "bg-indigo-950/70 hover:bg-indigo-900 border border-indigo-700/60 text-indigo-300 text-[10px] px-2 py-0.5 rounded-full transition flex items-center gap-1";
            badge.title = `Activation Score: ${c.activation_score}`;
            badge.innerHTML = `<span>⚡</span> <span>${c.title}</span>`;
            badge.onclick = () => loadWikiPage(c.rel_path);
            tagsContainer.appendChild(badge);
        });
    } catch (e) {
        tagsContainer.innerHTML = "";
    }
}

// Toggle Live In-Place Markdown Editor
function togglePageEditor() {
    isEditingPage = !isEditingPage;
    const bodyEl = document.getElementById("pageBody");
    const editorContainer = document.getElementById("pageEditorContainer");
    const btnEdit = document.getElementById("btnEditPage");
    const btnSave = document.getElementById("btnSavePage");

    if (isEditingPage) {
        bodyEl.classList.add("hidden");
        editorContainer.classList.remove("hidden");
        editorContainer.classList.add("flex");
        btnSave.classList.remove("hidden");
        btnEdit.textContent = "👁️ Preview";
    } else {
        bodyEl.classList.remove("hidden");
        editorContainer.classList.add("hidden");
        editorContainer.classList.remove("flex");
        btnSave.classList.add("hidden");
        btnEdit.textContent = "✏️ Edit";
    }
}

// Save Current Page Edits
async function saveCurrentPageEdits() {
    const content = document.getElementById("pageEditorTextarea").value;
    showToast("Saving and reindexing page...", "info");

    try {
        const resp = await fetch("/api/wiki/page", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path: currentLoadedPath, content })
        });
        if (!resp.ok) throw new Error("Save failed");
        showToast("Page saved and FTS5 reindexed!", "success");
        await loadWikiPage(currentLoadedPath);
        await loadWikiTree();
    } catch (e) {
        showToast("Failed to save page: " + e, "error");
    }
}

// Graph Visual State
let d3ZoomBehavior = null;
let graphSvgGroup = null;
let currentGraphNodes = [];
let currentGraphLinks = [];
let activeSpotlightNodeId = null;
let graphNodeSelection = null;
let graphLinkSelection = null;
let graphLabelSelection = null;

// Dynamic Legend Bar Updater
function updateGraphLegend(colorMode) {
    const bar = document.getElementById("graphLegendBar");
    if (!bar) return;
    if (colorMode === "category") {
        bar.innerHTML = `
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500 shadow-sm shadow-indigo-500/50"></span> 💡 Concepts</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-purple-500 shadow-sm shadow-purple-500/50"></span> 🤖 Models & Architectures</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400 shadow-sm shadow-cyan-400/50"></span> ⚡ Algorithms & Estimators</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50"></span> 🛠️ Frameworks & Tools</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-500 shadow-sm shadow-sky-500/50"></span> ⚖️ Differentials</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-sm shadow-rose-500/50"></span> 🚨 Traps</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-yellow-400 shadow-sm shadow-yellow-400/50"></span> 🎓 Lectures</div>
        `;
    } else {
        bar.innerHTML = `
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50"></span> Mastered (&ge;70%)</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-400 shadow-sm shadow-amber-400/50"></span> Review Needed (50-69%)</div>
            <div class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 shadow-sm shadow-rose-500/50"></span> Trap / Failure Mode (<50%)</div>
        `;
    }
}

// Multi-Foci Spatial Clustering Coordinates
function getClusterFocus(node, width, height) {
    const sys = (node.system || "").toLowerCase();
    const etype = (node.entity_type || "").toLowerCase();
    const title = (node.title || node.id || "").toLowerCase();
    const combo = `${sys} ${etype} ${title}`;

    // 1. 3D Vision, Radiance Fields & Foundation Models (Top-Left)
    if (combo.includes("nerf") || combo.includes("splat") || combo.includes("gaussian") || 
        combo.includes("mapanything") || combo.includes("dinov2") || combo.includes("latent") || 
        combo.includes("pointcloud") || combo.includes("metric") || combo.includes("depth") || 
        combo.includes("geometry") || combo.includes("radiance")) {
        return { x: width * 0.26, y: height * 0.28 };
    }

    // 2. High-Speed VIO, State Estimation & SLAM (Top-Right)
    if (combo.includes("vio") || combo.includes("imu") || combo.includes("odometry") || 
        combo.includes("preintegration") || combo.includes("factor") || combo.includes("slam") || 
        combo.includes("filter") || combo.includes("estimator") || combo.includes("bundle") ||
        combo.includes("kalman") || combo.includes("quaternion") || combo.includes("lie")) {
        return { x: width * 0.74, y: height * 0.30 };
    }

    // 3. Aerial Robotics, Drones & UAV Flow (Center)
    if (combo.includes("drone") || combo.includes("uav") || combo.includes("aerial") || 
        combo.includes("event") || combo.includes("rotor") || combo.includes("fpv") || 
        combo.includes("eventsplat") || combo.includes("normal flow")) {
        return { x: width * 0.50, y: height * 0.48 };
    }

    // 4. Distributed Systems, Consensus & Fault Tolerance (Bottom-Right)
    if (combo.includes("consensus") || combo.includes("raft") || combo.includes("paxos") || 
        combo.includes("distributed") || combo.includes("rpc") || combo.includes("replicated") || 
        combo.includes("eecs") || combo.includes("6.033") || combo.includes("cardio") || combo.includes("renal")) {
        return { x: width * 0.76, y: height * 0.72 };
    }

    // 5. Deep Learning & Latent Dynamics (Bottom-Left)
    if (combo.includes("world model") || combo.includes("planning") || combo.includes("mpc") || 
        combo.includes("backprop") || combo.includes("transformer") || combo.includes("attention") || 
        combo.includes("luminal") || combo.includes("hepat")) {
        return { x: width * 0.24, y: height * 0.70 };
    }

    // Default center
    return { x: width * 0.50, y: height * 0.50 };
}

// Dynamic Node Color
function getNodeColor(d, colorMode) {
    if (colorMode === "mastery") {
        if (d.category === "exam_traps" || d.mastery < 50) return "#f43f5e"; // Rose
        if (d.mastery >= 70) return "#10b981"; // Emerald
        return "#f59e0b"; // Amber
    }

    // Color by Category & Entity Type
    if (d.category === "concepts") return "#6366f1"; // Indigo
    if (d.category === "course_sessions") return "#eab308"; // Yellow
    if (d.category === "differentials") return "#0284c7"; // Sky
    if (d.category === "exam_traps") return "#f43f5e"; // Rose
    
    // STEM / ML / CV Entity classifications
    const etype = (d.entity_type || "").toLowerCase();
    if (etype.includes("model") || etype.includes("architecture")) return "#a855f7"; // Purple
    if (etype.includes("algorithm") || etype.includes("estimator") || etype.includes("vio") || etype.includes("filter")) return "#06b6d4"; // Cyan
    if (etype.includes("framework") || etype.includes("tool") || etype.includes("library") || etype.includes("protocol")) return "#f59e0b"; // Amber
    if (etype.includes("hardware") || etype.includes("kernel") || etype.includes("sensor")) return "#14b8a6"; // Teal
    
    // Medical fallback
    if (etype === "drug") return "#10b981"; // Emerald
    if (etype === "pathogen") return "#a855f7"; // Purple
    if (etype === "transporter") return "#14b8a6"; // Teal
    if (etype === "biomarker") return "#ec4899"; // Pink
    
    return "#64748b"; // Slate
}

// Reset Zoom & Fit
function resetGraphZoom() {
    const svg = d3.select("#brainGraphSvg");
    if (svg && d3ZoomBehavior) {
        svg.transition().duration(750).call(d3ZoomBehavior.transform, d3.zoomIdentity);
    }
}

// Mechanism Spotlighting
function spotlightNode(selectedNode) {
    activeSpotlightNodeId = selectedNode.id;
    const connectedIds = new Set([selectedNode.id]);

    currentGraphLinks.forEach(l => {
        const sId = l.source.id || l.source;
        const tId = l.target.id || l.target;
        if (sId === selectedNode.id) connectedIds.add(tId);
        if (tId === selectedNode.id) connectedIds.add(sId);
    });

    // 2-Hop expansion
    currentGraphLinks.forEach(l => {
        const sId = l.source.id || l.source;
        const tId = l.target.id || l.target;
        if (connectedIds.has(sId)) connectedIds.add(tId);
        if (connectedIds.has(tId)) connectedIds.add(sId);
    });

    if (graphNodeSelection) {
        graphNodeSelection
            .attr("opacity", d => connectedIds.has(d.id) ? 1.0 : 0.12)
            .attr("stroke", d => d.id === selectedNode.id ? "#ffffff" : "#0f172a")
            .attr("stroke-width", d => d.id === selectedNode.id ? 3.5 : 2);
    }

    if (graphLinkSelection) {
        graphLinkSelection
            .attr("opacity", l => {
                const sId = l.source.id || l.source;
                const tId = l.target.id || l.target;
                return connectedIds.has(sId) && connectedIds.has(tId) ? 0.9 : 0.05;
            })
            .attr("stroke-width", l => {
                const sId = l.source.id || l.source;
                const tId = l.target.id || l.target;
                return (sId === selectedNode.id || tId === selectedNode.id) ? 2.5 : 1.2;
            });
    }

    if (graphLabelSelection) {
        graphLabelSelection
            .attr("opacity", d => connectedIds.has(d.id) ? 1.0 : 0.12)
            .attr("font-weight", d => d.id === selectedNode.id ? "bold" : (connectedIds.has(d.id) ? "600" : "normal"));
    }

    const btnClear = document.getElementById("btnClearSpotlight");
    if (btnClear) btnClear.classList.remove("hidden");
}

function clearGraphSpotlight() {
    activeSpotlightNodeId = null;
    if (graphNodeSelection) {
        graphNodeSelection
            .attr("opacity", 1.0)
            .attr("stroke", "#0f172a")
            .attr("stroke-width", 2);
    }
    if (graphLinkSelection) {
        graphLinkSelection
            .attr("opacity", 0.6)
            .attr("stroke-width", 1.5);
    }
    if (graphLabelSelection) {
        graphLabelSelection
            .attr("opacity", 1.0)
            .attr("font-weight", "normal");
    }

    const btnClear = document.getElementById("btnClearSpotlight");
    if (btnClear) btnClear.classList.add("hidden");
    const searchInput = document.getElementById("graphSearchInput");
    if (searchInput) searchInput.value = "";
}

function searchAndFocusNode(query) {
    if (!query) {
        clearGraphSpotlight();
        return;
    }
    const q = query.toLowerCase();
    const target = currentGraphNodes.find(n => n.title.toLowerCase().includes(q) || n.id.toLowerCase().includes(q));
    if (target && target.x != null && target.y != null) {
        spotlightNode(target);
        const svg = d3.select("#brainGraphSvg");
        const container = document.getElementById("brainGraphSvg");
        const width = container.clientWidth || 800;
        const height = container.clientHeight || 650;

        const transform = d3.zoomIdentity
            .translate(width / 2 - target.x * 1.5, height / 2 - target.y * 1.5)
            .scale(1.5);
        svg.transition().duration(600).call(d3ZoomBehavior.transform, transform);
    }
}

// Interactive D3 Force-Directed Brain Graph
async function renderBrainGraph() {
    const svg = d3.select("#brainGraphSvg");
    svg.selectAll("*").remove();

    const container = document.getElementById("brainGraphSvg");
    const width = container.clientWidth || 800;
    const height = container.clientHeight || 650;

    const tooltip = d3.select("#graphTooltip");

    // Read Toolbar Filters
    const courseVal = document.getElementById("graphCourseFilter")?.value || "all";
    const layerVal = document.getElementById("graphLayerFilter")?.value || "mechanisms";
    const colorMode = document.getElementById("graphColorMode")?.value || "category";

    updateGraphLegend(colorMode);
    showToast("Constructing biomimetic organ constellations...", "info");

    try {
        const resp = await fetch(`/api/wiki/brain_graph?course=${encodeURIComponent(courseVal)}&layer=${encodeURIComponent(layerVal)}`);
        const graphData = await resp.json();

        currentGraphNodes = graphData.nodes || [];
        currentGraphLinks = graphData.links || [];

        // Update stats badge
        const statsBadge = document.getElementById("graphStatsBadge");
        if (statsBadge) {
            statsBadge.textContent = `${currentGraphNodes.length} Nodes • ${currentGraphLinks.length} Mechanism Links`;
        }

        if (currentGraphNodes.length === 0) {
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", height / 2)
                .attr("text-anchor", "middle")
                .attr("fill", "#64748b")
                .attr("font-size", "14px")
                .text("No matching concepts found in this filter.");
            return;
        }

        // SVG Background click clears spotlight
        svg.on("click", (event) => {
            if (event.target.tagName === "svg" || event.target.tagName === "rect") {
                clearGraphSpotlight();
            }
        });

        graphSvgGroup = svg.append("g");

        // D3 Zoom
        d3ZoomBehavior = d3.zoom()
            .scaleExtent([0.2, 4])
            .on("zoom", (event) => {
                graphSvgGroup.attr("transform", event.transform);
            });
        svg.call(d3ZoomBehavior);

        // D3 Multi-Foci Force Simulation
        d3Simulation = d3.forceSimulation(currentGraphNodes)
            .force("link", d3.forceLink(currentGraphLinks).id(d => d.id).distance(d => {
                if (d.type === "intra_system") return 60;
                if (d.type === "cross_system_bridge") return 120;
                return 85;
            }).strength(0.55))
            .force("charge", d3.forceManyBody().strength(-190))
            .force("x", d3.forceX(d => getClusterFocus(d, width, height).x).strength(0.18))
            .force("y", d3.forceY(d => getClusterFocus(d, width, height).y).strength(0.18))
            .force("collision", d3.forceCollide().radius(d => Math.max(12, Math.min(26, (d.degree || 1) * 2.2 + 8))));

        // Draw Links
        graphLinkSelection = graphSvgGroup.append("g")
            .selectAll("line")
            .data(currentGraphLinks)
            .join("line")
            .attr("stroke-width", d => d.type === "cross_system_bridge" ? 2 : 1.5)
            .attr("stroke", d => d.type === "cross_system_bridge" ? "#818cf8" : (d.type === "lecture_curriculum" ? "#f59e0b" : "#475569"))
            .attr("stroke-opacity", 0.65)
            .attr("stroke-dasharray", d => d.type === "cross_system_bridge" ? "4,4" : "none");

        // Draw Nodes
        graphNodeSelection = graphSvgGroup.append("g")
            .selectAll("circle")
            .data(currentGraphNodes)
            .join("circle")
            .attr("r", d => Math.max(7, Math.min(22, (d.degree || 1) * 1.8 + 7)))
            .attr("fill", d => getNodeColor(d, colorMode))
            .attr("stroke", "#0f172a")
            .attr("stroke-width", 2)
            .attr("cursor", "pointer")
            .call(drag(d3Simulation));

        // Draw Labels
        graphLabelSelection = graphSvgGroup.append("g")
            .selectAll("text")
            .data(currentGraphNodes)
            .join("text")
            .text(d => d.title.length > 22 ? d.title.substring(0, 20) + "…" : d.title)
            .attr("font-size", "10px")
            .attr("font-family", "sans-serif")
            .attr("fill", "#e2e8f0")
            .attr("dx", d => Math.max(7, Math.min(22, (d.degree || 1) * 1.8 + 7)) + 4)
            .attr("dy", 4)
            .attr("pointer-events", "none");

        // Interactions: Hover Tooltip
        graphNodeSelection
            .on("mouseover", (event, d) => {
                const sysLabel = d.system || "General";
                const catLabel = d.entity_type || d.category;
                tooltip.style("display", "block")
                    .html(`
                        <div class="font-bold text-white text-sm mb-1">${d.title}</div>
                        <div class="flex items-center gap-1.5 mb-1.5">
                            <span class="px-1.5 py-0.5 rounded bg-indigo-950 border border-indigo-700/60 text-indigo-300 text-[10px] uppercase font-semibold">${sysLabel}</span>
                            <span class="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 text-[10px] uppercase font-semibold">${catLabel}</span>
                        </div>
                        <div class="text-[11px] text-slate-300 space-y-0.5">
                            <div><span class="text-slate-400">Mastery Readiness:</span> <span class="font-semibold text-emerald-400">${d.mastery}%</span></div>
                            <div><span class="text-slate-400">Direct Connections:</span> <span class="font-semibold text-amber-300">${d.degree}</span></div>
                        </div>
                        <div class="mt-2 pt-1.5 border-t border-slate-700/60 text-[10px] text-slate-400 italic">
                            Click to spotlight pathways • Double-click to open in Wiki
                        </div>
                    `);
            })
            .on("mousemove", (event) => {
                const rect = container.getBoundingClientRect();
                tooltip.style("left", (event.clientX - rect.left + 15) + "px")
                    .style("top", (event.clientY - rect.top - 10) + "px");
            })
            .on("mouseout", () => {
                tooltip.style("display", "none");
            })
            .on("click", (event, d) => {
                event.stopPropagation();
                spotlightNode(d);
            })
            .on("dblclick", (event, d) => {
                event.stopPropagation();
                if (d.path) {
                    loadWikiPage(d.path);
                }
            });

        // Tick simulation
        d3Simulation.on("tick", () => {
            graphLinkSelection
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            graphNodeSelection
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);

            graphLabelSelection
                .attr("x", d => d.x)
                .attr("y", d => d.y);
        });

    } catch (e) {
        console.error("Brain graph failed", e);
    }
}

// Drag behavior for D3 nodes
function drag(simulation) {
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }
    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }
    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

// Load Socratic vignette or targeted problem
async function loadVignette(customTopic, customGuidance, customDomain) {
    const stemEl = document.getElementById("vignetteStem");
    const optionsEl = document.getElementById("vignetteOptions");
    const topicEl = document.getElementById("vignetteTopic");
    const feedbackContent = document.getElementById("feedbackContent");
    const feedbackPlaceholder = document.getElementById("feedbackPlaceholder");
    const verdictBadge = document.getElementById("verdictBadge");
    const domainBadge = document.getElementById("vignetteDomainBadge");

    stemEl.textContent = "Synthesizing personalized Socratic challenge and diagnostic scenario...";
    optionsEl.innerHTML = "";
    feedbackContent.classList.add("hidden");
    feedbackPlaceholder.classList.remove("hidden");
    verdictBadge.classList.add("hidden");
    selectedOptionId = null;

    try {
        const payload = {};
        if (customTopic) payload.topic = customTopic;
        if (customGuidance) payload.guidance = customGuidance;
        if (customDomain) payload.domain = customDomain;

        const resp = await fetch("/api/tutor/generate_vignette", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        currentVignette = await resp.json();

        topicEl.textContent = currentVignette.topic || "Core Systems & Concepts";
        if (domainBadge) {
            domainBadge.textContent = currentVignette.domain || "Universal";
        }
        stemEl.textContent = currentVignette.stem;

        optionsEl.innerHTML = "";
        currentVignette.options.forEach(opt => {
            const btn = document.createElement("button");
            btn.className = "option-btn w-full text-left p-3 rounded-lg border border-slate-700 bg-slate-900/60 hover:bg-slate-700/50 text-xs text-slate-200 transition flex items-start gap-3";
            btn.dataset.id = opt.id;
            btn.innerHTML = `
                <span class="font-bold px-2 py-0.5 rounded bg-slate-800 border border-slate-600 text-slate-300">${opt.id}</span>
                <span class="flex-1">${opt.text}</span>
            `;
            btn.onclick = () => {
                document.querySelectorAll(".option-btn").forEach(b => {
                    b.classList.remove("border-indigo-500", "bg-indigo-950/40");
                });
                btn.classList.add("border-indigo-500", "bg-indigo-950/40");
                selectedOptionId = opt.id;
            };
            optionsEl.appendChild(btn);
        });
    } catch (e) {
        stemEl.textContent = "Error generating clinical vignette: " + e;
    }
}

// Submit answer to Living Teacher
async function submitAnswer() {
    if (!selectedOptionId) {
        showToast("Please select an option before submitting.", "info");
        return;
    }
    const reasoning = document.getElementById("studentReasoningInput").value.trim();

    showToast("Analyzing clinical reasoning with Living Teacher...", "info");

    try {
        const resp = await fetch("/api/tutor/evaluate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                vignette: currentVignette,
                selected_option_id: selectedOptionId,
                student_reasoning: reasoning
            })
        });
        const evalData = await resp.json();

        // Render feedback
        document.getElementById("feedbackPlaceholder").classList.add("hidden");
        const feedbackContent = document.getElementById("feedbackContent");
        feedbackContent.classList.remove("hidden");

        const verdictBadge = document.getElementById("verdictBadge");
        verdictBadge.classList.remove("hidden");
        if (evalData.is_correct) {
            verdictBadge.textContent = "CORRECT";
            verdictBadge.className = "text-xs font-bold px-2.5 py-0.5 rounded bg-emerald-900/80 text-emerald-200 border border-emerald-600";
        } else {
            verdictBadge.textContent = "BOARD TRAP MISSED";
            verdictBadge.className = "text-xs font-bold px-2.5 py-0.5 rounded bg-rose-900/80 text-rose-200 border border-rose-600";
        }

        document.getElementById("feedbackCritique").textContent = evalData.socratic_critique;
        document.getElementById("feedbackMechanism").textContent = evalData.mechanism_explanation;
        document.getElementById("feedbackTaxonomy").textContent = evalData.error_taxonomy || "REASONING_GAP";
        document.getElementById("feedbackRemediation").textContent = evalData.remediation_action || "";

        const cardCand = evalData.anki_card_candidate;
        if (cardCand) {
            document.getElementById("feedbackCardFront").textContent = cardCand.front;
            document.getElementById("feedbackCardBack").textContent = cardCand.back;
        }

        // Render Jev System 1 telemetry if present
        const jevBadge = document.getElementById("feedbackJevBadge");
        if (evalData.jev_system_one && jevBadge) {
            jevBadge.classList.remove("hidden");
            const jev = evalData.jev_system_one;
            document.getElementById("jevLatencyBadge").textContent = `${jev.latency_ms}ms (Jev)`;
            document.getElementById("jevTaxonomyVal").textContent = jev.error_taxonomy || "REASONING_GAP";
            document.getElementById("jevConfidenceVal").textContent = `${Math.round(jev.confidence * 100)}%`;
            const trapEl = document.getElementById("jevTrapVal");
            if (jev.board_trap_triggered) {
                trapEl.textContent = "TRIGGERED (High Risk)";
                trapEl.className = "font-mono font-bold text-rose-400";
            } else {
                trapEl.textContent = "Not Triggered (Clean)";
                trapEl.className = "font-mono font-bold text-emerald-400";
            }
        } else if (jevBadge) {
            jevBadge.classList.add("hidden");
        }

        showToast(evalData.is_correct ? "Correct! Mastery updated." : "Missed trap recorded in Wiki & Anki queued.", evalData.is_correct ? "success" : "info");
        await loadStatus();
        await loadWikiTree();
    } catch (e) {
        showToast("Evaluation failed: " + e, "error");
    }
}

// ================= ANKI FLASHCARD CENTER & STUDY PLAYER =================

// Load staged Anki Flashcards with active filters
async function loadAnkiCards() {
    try {
        const course = document.getElementById("ankiCourseFilter")?.value || "all";
        const system = document.getElementById("ankiSystemFilter")?.value || "all";
        const cardType = document.getElementById("ankiTypeFilter")?.value || "all";
        const mastery = document.getElementById("ankiMasteryFilter")?.value || "all";
        const clozeMode = document.getElementById("ankiClozeModeFilter")?.value || "atomic";
        const query = document.getElementById("ankiSearchInput")?.value || "";

        const params = new URLSearchParams();
        if (course !== "all") params.set("course", course);
        if (system !== "all") params.set("system", system);
        if (cardType !== "all") params.set("card_type", cardType);
        if (mastery !== "all") params.set("mastery", mastery);
        if (clozeMode) params.set("cloze_mode", clozeMode);
        if (query.trim()) params.set("query", query.trim());

        const resp = await fetch("/api/anki/cards?" + params.toString());
        const data = await resp.json();
        ankiCurrentCards = data.cards || [];

        // Update statistics and progress bar
        updateAnkiStats(data.stats, data.filtered_count);

        // Render card grid in Browse Mode
        renderAnkiCardGrid(ankiCurrentCards);

        // If in Study Mode, refresh active card
        if (ankiViewMode === "study") {
            renderCurrentStudyCard();
        }
    } catch (e) {
        console.error("Load anki cards failed", e);
    }
}

// Update deck progress bar and stat counters
function updateAnkiStats(stats, filteredCount) {
    if (!stats) return;
    const total = stats.total || 0;
    const mastered = stats.mastered || 0;
    const learning = stats.learning || 0;
    const struggling = stats.struggling || 0;
    const unreviewed = stats.unreviewed || 0;
    const due = stats.due || 0;

    const statPercent = document.getElementById("ankiStatPercent");
    if (statPercent) statPercent.textContent = `${stats.mastery_percentage || 0}%`;

    const elTotal = document.getElementById("ankiStatTotal");
    if (elTotal) elTotal.textContent = total;

    const elDue = document.getElementById("ankiStatDue");
    if (elDue) elDue.textContent = due;

    const elLearning = document.getElementById("ankiStatLearning");
    if (elLearning) elLearning.textContent = learning;

    const elMastered = document.getElementById("ankiStatMastered");
    if (elMastered) elMastered.textContent = mastered;

    // Progress bar segment widths
    if (total > 0) {
        const pMastered = (mastered / total) * 100;
        const pLearning = (learning / total) * 100;
        const pStruggling = (struggling / total) * 100;
        const pUnreviewed = (unreviewed / total) * 100;

        const barM = document.getElementById("ankiBarMastered");
        if (barM) barM.style.width = `${pMastered}%`;
        const barL = document.getElementById("ankiBarLearning");
        if (barL) barL.style.width = `${pLearning}%`;
        const barS = document.getElementById("ankiBarStruggling");
        if (barS) barS.style.width = `${pStruggling}%`;
        const barU = document.getElementById("ankiBarUnreviewed");
        if (barU) barU.style.width = `${pUnreviewed}%`;
    }

    const badge = document.getElementById("ankiStatsBadge");
    if (badge) badge.textContent = `${total} High-Yield Cards`;

    const countLabel = document.getElementById("ankiCardCountLabel");
    if (countLabel) countLabel.textContent = `Showing ${filteredCount} of ${total} cards`;
}

// Render cards in Browse Grid view
function renderAnkiCardGrid(cards) {
    const container = document.getElementById("ankiCardsGrid");
    if (!container) return;
    container.innerHTML = "";

    if (cards.length === 0) {
        container.innerHTML = `
            <div class="col-span-2 text-center text-slate-500 text-xs py-12 bg-slate-900/50 rounded-xl border border-slate-800">
                <div class="text-3xl mb-2">🔍</div>
                <div class="font-semibold text-slate-300">No flashcards match active filters.</div>
                <div class="mt-1 text-slate-500">Try resetting course, system, or search parameters.</div>
            </div>`;
        return;
    }

    cards.forEach(card => {
        const cardEl = document.createElement("div");
        cardEl.className = "bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col justify-between hover:border-indigo-500/50 transition shadow-sm";

        // Cloze highlighting
        let formattedText = card.text || card.front || "";
        formattedText = formattedText.replace(/\{\{c\d+::([^}]+)\}\}/g, '<span class="cloze-preview">$1</span>');

        // Difficulty stars
        const diff = card.difficulty || 2;
        const stars = diff === 1 ? "★☆☆" : diff === 2 ? "★★☆" : "★★★";

        // System badge pill
        const sys = card.system || "Core";
        let sysClass = "system-pill-core";
        const sysLow = sys.toLowerCase();
        if (sysLow.includes("hepat") || sysLow.includes("liver")) sysClass = "system-pill-gi";
        else if (sysLow.includes("luminal") || sysLow.includes("gi") || sysLow.includes("gastrod")) sysClass = "system-pill-gi";
        else if (sysLow.includes("cardio")) sysClass = "system-pill-cardio";
        else if (sysLow.includes("renal")) sysClass = "system-pill-renal";
        else if (sysLow.includes("pancrea") || sysLow.includes("biliary")) sysClass = "system-pill-micro";

        // Mastery badge
        const mastery = card.mastery || "unreviewed";
        const masteryBadgeClass = `mastery-badge-${mastery}`;
        const masteryLabel = mastery.charAt(0).toUpperCase() + mastery.slice(1);

        // Tags
        const tagsHtml = (card.tags || []).slice(0, 3).map(t => `<span class="text-[10px] bg-slate-700/80 text-slate-300 px-2 py-0.5 rounded-full font-medium">${t}</span>`).join(" ");

        // Source & Wiki link
        const wikiSlug = card.wiki_slug || "";
        const wikiBtnHtml = wikiSlug ? `
            <button onclick="openWikiFromCard('${wikiSlug}')" class="text-indigo-400 hover:text-indigo-300 text-[11px] font-semibold flex items-center gap-1 transition">
                <span>📖</span> Wiki
            </button>
        ` : '';

        // Atomic subtitle/pill
        const atomicPillHtml = card.subtitle ? `
            <span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-700/50">${card.subtitle}</span>
        ` : (card.is_atomic ? `<span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-700/50">🎯 Single Unknown</span>` : '');

        cardEl.innerHTML = `
            <div>
                <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-1.5 flex-wrap">
                        <span class="system-pill ${sysClass}">${sys}</span>
                        <span class="text-[10px] font-mono text-slate-400 uppercase">${card.type || "cloze"}</span>
                        ${atomicPillHtml}
                        <span class="text-[10px] text-amber-400 font-mono">${stars}</span>
                    </div>
                    <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full ${masteryBadgeClass}">${masteryLabel}</span>
                </div>
                <div class="text-sm text-slate-200 leading-relaxed font-normal my-2">${formattedText}</div>
                ${card.pearl ? `
                    <div class="mt-2.5 p-2 bg-emerald-950/30 border-l-2 border-emerald-500 text-emerald-300 text-[11px] rounded-r leading-relaxed">
                        <span class="font-bold">Pearl:</span> ${card.pearl}
                    </div>` : ''}
            </div>
            <div class="mt-3 pt-2.5 border-t border-slate-700/60 flex items-center justify-between text-xs text-slate-400">
                <div class="flex items-center gap-1.5 overflow-hidden">
                    ${tagsHtml}
                </div>
                <div class="flex items-center gap-2">
                    ${wikiBtnHtml}
                    <button onclick="drillSpecificCard('${card.id}')" class="bg-slate-700 hover:bg-slate-600 text-slate-200 text-[11px] px-2 py-1 rounded transition flex items-center gap-1">
                        <span>🚀</span> Drill
                    </button>
                </div>
            </div>
        `;
        container.appendChild(cardEl);
    });
}

// Switch between Browse Deck and Interactive Study Mode
function setAnkiMode(mode) {
    ankiViewMode = mode;
    const btnBrowse = document.getElementById("btnModeBrowseCards");
    const btnStudy = document.getElementById("btnModeStudyCards");
    const arena = document.getElementById("ankiStudyArena");
    const browse = document.getElementById("ankiBrowseContainer");

    if (mode === "study") {
        if (btnStudy) {
            btnStudy.classList.add("bg-indigo-600", "text-white");
            btnStudy.classList.remove("text-slate-400");
        }
        if (btnBrowse) {
            btnBrowse.classList.remove("bg-indigo-600", "text-white");
            btnBrowse.classList.add("text-slate-400");
        }
        if (browse) browse.classList.add("hidden");
        if (arena) arena.classList.remove("hidden");
        ankiActiveCardIndex = 0;
        renderCurrentStudyCard();
    } else {
        if (btnBrowse) {
            btnBrowse.classList.add("bg-indigo-600", "text-white");
            btnBrowse.classList.remove("text-slate-400");
        }
        if (btnStudy) {
            btnStudy.classList.remove("bg-indigo-600", "text-white");
            btnStudy.classList.add("text-slate-400");
        }
        if (arena) arena.classList.add("hidden");
        if (browse) browse.classList.remove("hidden");
    }
}

// Render active card in Study Player Arena
function renderCurrentStudyCard() {
    const arena = document.getElementById("ankiStudyArena");
    if (!arena || ankiViewMode !== "study") return;

    if (ankiCurrentCards.length === 0) {
        document.getElementById("studyCardPrompt").innerHTML = `<span class="text-slate-500 text-sm">No flashcards available in this filter. Reset filters to study!</span>`;
        document.getElementById("studyRevealContainer").classList.add("hidden");
        document.getElementById("studyAnswerContainer").classList.add("hidden");
        return;
    }

    if (ankiActiveCardIndex >= ankiCurrentCards.length) {
        ankiActiveCardIndex = 0;
    }

    const card = ankiCurrentCards[ankiActiveCardIndex];
    ankiIsStudyRevealed = false;

    // Counter
    document.getElementById("studyQueueCounter").textContent = `Card ${ankiActiveCardIndex + 1} of ${ankiCurrentCards.length}`;
    document.getElementById("studyQueueBadge").textContent = `${card.course || 'HST.121'} • ${card.system || 'Core'}`;

    // Badges
    document.getElementById("studyCardSystemBadge").textContent = card.system || "Medical Core";
    document.getElementById("studyCardTypeBadge").textContent = `${card.type || "cloze"} card`;
    const diff = card.difficulty || 2;
    document.getElementById("studyCardDifficulty").textContent = diff === 1 ? "★☆☆" : diff === 2 ? "★★☆" : "★★★";

    // Atomic / Single-Unknown Badge
    const atomicBadge = document.getElementById("studyCardAtomicBadge");
    if (atomicBadge) {
        if (card.is_atomic || card.cloze_count === 1) {
            atomicBadge.classList.remove("hidden");
            atomicBadge.textContent = (card.cloze_index && card.total_clozes > 1)
                ? `🎯 Unknown ${card.cloze_index} of ${card.total_clozes}`
                : `🎯 Single Unknown`;
        } else {
            atomicBadge.classList.add("hidden");
        }
    }

    const masteryBadge = document.getElementById("studyCardMasteryBadge");
    const mastery = card.mastery || "unreviewed";
    masteryBadge.className = `text-xs font-semibold px-2.5 py-0.5 rounded-full mastery-badge-${mastery}`;
    masteryBadge.textContent = mastery.charAt(0).toUpperCase() + mastery.slice(1);

    // Front: Hide cloze deletion with [ ... ] placeholder
    let promptText = card.text || card.front || "";
    promptText = promptText.replace(/\{\{c\d+::([^}]+)\}\}/g, '<span class="cloze-hidden">[ ... ]</span>');
    document.getElementById("studyCardPrompt").innerHTML = promptText;

    // Back Pearl
    document.getElementById("studyCardPearl").textContent = card.pearl || card.back || "Review this concept or mechanism in the compounding wiki.";

    // Show reveal button, hide rating bar
    document.getElementById("studyRevealContainer").classList.remove("hidden");
    document.getElementById("studyAnswerContainer").classList.add("hidden");

    // Reset Jev Active Recall Input and Telemetry Badge
    const recallInput = document.getElementById("studyRecallInput");
    if (recallInput) {
        recallInput.value = "";
        if (card.is_atomic && card.total_clozes > 1) {
            recallInput.placeholder = `Type the target blank (Unknown ${card.cloze_index} of ${card.total_clozes}) from memory...`;
        } else {
            recallInput.placeholder = "Type the core mechanism, mathematical formula, or key insight from memory...";
        }
    }
    const recallBadge = document.getElementById("jevRecallFeedbackBadge");
    if (recallBadge) {
        recallBadge.classList.add("hidden");
        recallBadge.textContent = "";
    }
}

// Reveal Cloze Answer & Key Insight in Study Mode
function revealStudyAnswer() {
    if (ankiCurrentCards.length === 0) return;
    const card = ankiCurrentCards[ankiActiveCardIndex];
    ankiIsStudyRevealed = true;

    // Replace cloze deletions with highlighted answers
    let revealedText = card.text || card.front || "";
    revealedText = revealedText.replace(/\{\{c\d+::([^}]+)\}\}/g, '<span class="cloze-preview">$1</span>');
    document.getElementById("studyCardPrompt").innerHTML = revealedText;

    // Toggle reveal button and answer rating bar
    document.getElementById("studyRevealContainer").classList.add("hidden");
    document.getElementById("studyAnswerContainer").classList.remove("hidden");
}

// Auto-Grade Active Recall using Jev System 1 Decision Model
async function gradeActiveCardWithJev() {
    if (ankiCurrentCards.length === 0) return;
    const card = ankiCurrentCards[ankiActiveCardIndex];
    const inputEl = document.getElementById("studyRecallInput");
    const studentAnswer = inputEl ? inputEl.value.trim() : "";

    if (!studentAnswer) {
        showToast("Type your recall in the box before auto-grading.", "info");
        return;
    }

    showToast("Evaluating active recall with Jev System 1...", "info");
    try {
        const resp = await fetch("/api/anki/cards/grade_recall", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                card_id: card.id,
                student_answer: studentAnswer
            })
        });
        const data = await resp.json();
        if (data.success && data.grading) {
            const g = data.grading;
            const badge = document.getElementById("jevRecallFeedbackBadge");
            if (badge) {
                badge.classList.remove("hidden");
                badge.textContent = `⚡ Jev: ${g.feedback_label} (${g.latency_ms}ms, ${Math.round(g.confidence * 100)}% conf)`;
                badge.className = g.sm2_rating >= 3
                    ? "text-xs font-mono font-bold px-2.5 py-1 rounded bg-emerald-950 text-emerald-300 border border-emerald-700"
                    : "text-xs font-mono font-bold px-2.5 py-1 rounded bg-rose-950 text-rose-300 border border-rose-700";
            }

            // Update local card state and stats
            ankiCurrentCards[ankiActiveCardIndex] = data.card;
            updateAnkiStats(data.stats, ankiCurrentCards.length);

            // Reveal the answer so student can compare their recall with gold-standard pearl
            revealStudyAnswer();
            showToast(`Jev rated: ${g.feedback_label} in ${g.latency_ms}ms`, g.sm2_rating >= 3 ? "success" : "info");
        }
    } catch (e) {
        showToast("Jev auto-grading failed: " + e, "error");
    }
}

// Record SM-2 review rating for active study card
async function rateActiveCard(rating) {
    if (ankiCurrentCards.length === 0) return;
    const card = ankiCurrentCards[ankiActiveCardIndex];

    try {
        const resp = await fetch("/api/anki/cards/review", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                card_id: card.id,
                rating: rating
            })
        });
        const data = await resp.json();
        if (data.success && data.card) {
            // Update local card state
            ankiCurrentCards[ankiActiveCardIndex] = data.card;
            updateAnkiStats(data.stats, ankiCurrentCards.length);

            const ratingLabels = { 1: "Struggling (Review <10m)", 2: "Hard (Review 1d)", 3: "Good (Review 3d)", 4: "Mastered (Review 7d)" };
            showToast(`${ratingLabels[rating] || 'Rating recorded'}.`, rating >= 3 ? "success" : "info");

            // Advance to next card in queue
            ankiActiveCardIndex = (ankiActiveCardIndex + 1) % ankiCurrentCards.length;
            renderCurrentStudyCard();
        }
    } catch (e) {
        showToast("Review failed to record: " + e, "error");
    }
}

// Jump directly to a card in Study Mode
function drillSpecificCard(cardId) {
    const idx = ankiCurrentCards.findIndex(c => c.id === cardId);
    if (idx >= 0) {
        ankiActiveCardIndex = idx;
    }
    setAnkiMode("study");
}

// Jump from card directly to Compounding Wiki reader
function openWikiFromCard(wikiSlug) {
    if (!wikiSlug) return;
    // Switch tab to Wiki
    const wikiTabBtn = document.getElementById("tabBtnWiki");
    if (wikiTabBtn) wikiTabBtn.click();

    loadWikiPage(wikiSlug);
    showToast(`Navigated to ${wikiSlug}`, "info");
}

// Recompile all cards from Compounding Wiki
async function recompileAnkiFromWiki() {
    showToast("Recompiling high-yield cards across all wiki files...", "info");
    try {
        const resp = await fetch("/api/anki/compile_from_wiki", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ atomic: false }) // Preserves base Anki format in storage, derives on-the-fly
        });
        const data = await resp.json();
        if (data.success) {
            showToast(`Recompiled ${data.total_cards} cards from Wiki!`, "success");
            await loadAnkiCards();
            await loadStatus();
        } else {
            showToast("Recompile failed.", "error");
        }
    } catch (e) {
        showToast("Recompile error: " + e, "error");
    }
}

// Download .apkg deck (respecting active course and cloze focus mode)
function downloadAnkiDeck() {
    const course = document.getElementById("ankiCourseFilter")?.value || "all";
    const clozeMode = document.getElementById("ankiClozeModeFilter")?.value || "atomic";
    const isAtomic = clozeMode === "atomic";
    showToast(`Compiling ${course !== "all" ? course.toUpperCase() : "Master"} ${isAtomic ? "Single-Unknown" : "Combined"} .apkg deck...`, "info");
    
    const params = new URLSearchParams();
    if (course !== "all") params.set("course", course);
    if (isAtomic) params.set("atomic", "true");

    const url = "/api/anki/export?" + params.toString();
    window.location.href = url;
}


// Load Curriculum & Diagnostics view
async function loadCurriculum() {
    try {
        const respCurr = await fetch("/api/curriculum");
        const currData = await respCurr.json();

        document.getElementById("currTargetExam").textContent = currData.target_exam;
        document.getElementById("currDaysLeft").textContent = currData.days_remaining;
        document.getElementById("currBlockName").textContent = currData.current_block;

        const topicsList = document.getElementById("currTopicsList");
        topicsList.innerHTML = "";
        (currData.topics || []).forEach(t => {
            const li = document.createElement("li");
            const priorityColor = t.priority === "CRITICAL" ? "text-rose-400" : "text-amber-300";
            li.innerHTML = `<span class="font-bold ${priorityColor}">[${t.priority}]</span> ${t.name}`;
            topicsList.appendChild(li);
        });

        // Load Student Profile
        const respProf = await fetch("/api/student/profile");
        const profData = await respProf.json();

        const currReadinessEl = document.getElementById("currReadiness");
        if (currReadinessEl) currReadinessEl.textContent = `${profData.readiness_score}%`;
        const headerReadinessEl = document.getElementById("headerReadiness");
        if (headerReadinessEl) headerReadinessEl.textContent = `${profData.readiness_score}%`;
        const currBar = document.getElementById("currReadinessBar");
        if (currBar) currBar.style.width = `${profData.readiness_score}%`;

        // Mastery Breakdown
        const masteryBreakdown = document.getElementById("masteryBreakdown");
        masteryBreakdown.innerHTML = "";
        for (const [sys, score] of Object.entries(profData.mastery || {})) {
            const card = document.createElement("div");
            card.className = "bg-slate-900/70 border border-slate-700/80 rounded-lg p-3";
            const color = score >= 70 ? "text-emerald-400" : (score >= 55 ? "text-amber-300" : "text-rose-400");
            card.innerHTML = `
                <div class="flex items-center justify-between text-xs mb-1">
                    <span class="font-semibold text-slate-300">${sys}</span>
                    <span class="font-bold ${color}">${score}%</span>
                </div>
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div class="bg-indigo-500 h-full rounded-full" style="width: ${score}%;"></div>
                </div>
            `;
            masteryBreakdown.appendChild(card);
        }

        // Misconceptions log
        document.getElementById("misconceptionsContainer").textContent = profData.misconceptions_raw || "No errors recorded yet.";

    } catch (e) {
        console.error("Load curriculum failed", e);
    }
}

// Show notification toast
function showToast(msg, type = "info") {
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toastMsg");
    const toastIcon = document.getElementById("toastIcon");

    toastMsg.textContent = msg;
    toastIcon.textContent = type === "success" ? "✅" : (type === "error" ? "❌" : "ℹ️");

    toast.classList.remove("translate-y-20", "opacity-0", "pointer-events-none");
    setTimeout(() => {
        toast.classList.add("translate-y-20", "opacity-0", "pointer-events-none");
    }, 3500);
}

// ==========================================
// INTERACTIVE UI WALKTHROUGH & ONBOARDING
// ==========================================

const WALKTHROUGH_STEPS = [
    {
        id: "step-welcome",
        view: "viewWiki",
        icon: "🏛",
        title: "Welcome to Paideia Genesis",
        badge: "Step 1 of 7: Overview",
        description: "Paideia Genesis turns static lecture notes and research papers into an evolving, compounding cognitive learning engine with a closed self-reinforcing learning loop.",
        highlights: [
            "• <strong>Closed Cognitive Loop:</strong> Ingests notes, forms graph memory, challenges reasoning with Socratic drills, and schedules objective active recall.",
            "• <strong>Dual-Process Intelligence:</strong> Sub-100ms reflex heuristics (TypeSafe AI Jev System 1) + deep analytical reasoning (System 2).",
            "• <strong>100% Offline-First:</strong> Works completely offline with zero mandatory API dependencies."
        ]
    },
    {
        id: "step-wiki",
        view: "viewWiki",
        icon: "📚",
        title: "Compounding Wiki & Anthropic Contextual Retrieval",
        badge: "Step 2 of 7: Knowledge Base",
        description: "Browse your notes structured into Karpathy's 5-layer knowledge architecture: course sessions, concepts, entities, comparative differentials, and critical pitfalls.",
        highlights: [
            "• <strong>✨ Anthropic Contextual Retrieval:</strong> Prepends chunk-specific explanatory context to every section before indexing, eliminating lost context in semantic chunks.",
            "• <strong>Hybrid BM25 + Vector + Reranking:</strong> Combines lexical precision with semantic embeddings and cross-scoring, reducing retrieval failure by up to 67%.",
            "• <strong>Live In-Place Editor:</strong> Click '✏️ Edit' on any note to compound findings directly in markdown with immediate FTS5 re-indexing."
        ]
    },
    {
        id: "step-graph",
        view: "viewGraph",
        icon: "🧠",
        title: "Biomimetic Brain Graph (HippoRAG)",
        badge: "Step 3 of 7: Associative Memory",
        description: "Visualize knowledge connections across multiple disciplines using hippocampal indexing theory and personalized PageRank (PPR).",
        highlights: [
            "• <strong>Interactive Spreading Activation:</strong> Click any concept node to illuminate its 1-hop direct connections and 2-hop associative ripple effects.",
            "• <strong>Cross-Disciplinary Force Clustering:</strong> Automatically clusters Distributed Systems, Computer Science, and Medicine while surfacing bridging concepts.",
            "• <strong>Layer Toggles:</strong> Filter the graph by high-yield mechanisms, technical entities, or differential diagnoses."
        ]
    },
    {
        id: "step-tutor",
        view: "viewTutor",
        icon: "🎓",
        title: "Socratic Living Tutor & Misconception Triage",
        badge: "Step 4 of 7: Active Socratic Drill",
        description: "Engage in adaptive conceptual dilemmas designed to challenge and probe your reasoning rather than simply spoon-feeding answers.",
        highlights: [
            "• <strong>Steerable Dilemma Generation:</strong> Enter custom guidance or focus topics (e.g. 'Raft split-brain invariants' or 'SGLT2 inhibitors').",
            "• <strong>Root Misconception Triage:</strong> Diagnoses underlying errors (e.g. CRITICAL_PITFALL, INVARIANT_VIOLATION) when evaluating free-text student explanations.",
            "• <strong>Auto-Remediation:</strong> Instantly stages targeted remedial flashcards addressing diagnosed conceptual gaps."
        ]
    },
    {
        id: "step-anki",
        view: "viewAnki",
        icon: "🎴",
        title: "Objective AI-Graded Spaced Repetition (SM-2 & Jev)",
        badge: "Step 5 of 7: Flashcard Center",
        description: "Eliminate the 'illusion of competence' of manual self-scoring. Type your active recall explanations in free text for sub-200ms objective AI evaluation.",
        highlights: [
            "• <strong>Free-Text Active Recall:</strong> Machine-native evaluation scores depth against gold standards and schedules SuperMemo-2 (SM-2) intervals.",
            "• <strong>Study Mode:</strong> Flip through cards, reveal gold answers, or let the AI grade your typed explanations.",
            "• <strong>AnkiConnect & .apkg Export:</strong> One-click export of course-filtered .apkg decks or direct sync to local desktop Anki."
        ]
    },
    {
        id: "step-curriculum",
        view: "viewCurriculum",
        icon: "🎯",
        title: "Curriculum Milestones & Diagnostic Analytics",
        badge: "Step 6 of 7: Diagnostics",
        description: "Monitor your exam countdown and topic-by-topic readiness scores to target weaknesses before high-stakes milestones.",
        highlights: [
            "• <strong>Countdown & Readiness Tracker:</strong> Days remaining and overall readiness metrics updated on every review.",
            "• <strong>Topic Mastery Heatmap:</strong> Visual breakdown of mastery across modules and systems.",
            "• <strong>Diagnosed Misconceptions Log:</strong> Live audit trail of traps you've encountered with direct remediation drills."
        ]
    },
    {
        id: "step-actions",
        view: "viewWiki",
        icon: "🚀",
        title: "Quick Capture & Curriculum Ingestion",
        badge: "Step 7 of 7: Power Actions",
        description: "You're all set! Use the header quick-action buttons anytime to build and expand your personal knowledge brain.",
        highlights: [
            "• <strong>🗣️ Capture Conversation:</strong> Record audio memos, upload documents (.pdf, .txt, .md), or paste transcripts. Automatically transcribes, digests concepts, trade-offs, and stages flashcards.",
            "• <strong>📄 Import Paper:</strong> Ingest Deep Learning and Computer Vision papers with automated contextual situating and dense indexing.",
            "• <strong>📝 Quick Capture:</strong> Capture algorithmic insights or research notes on-the-fly and automatically stage flashcards.",
            "• <strong>🌐 Pull-In Subject Concept:</strong> Query arXiv / Wikipedia / verified literature and synthesize a full concept page on-the-fly.",
            "• <strong>📥 Import Curriculum:</strong> Ingest full manifests (like DL/CV Foundations or MIT 6.033) with one click.",
            "• <strong>🎓 UI Walkthrough:</strong> Replay this walkthrough anytime by clicking 'UI Walkthrough' in the header bar."
        ]
    }
];

class UIWalkthroughManager {
    constructor() {
        this.currentStep = 0;
        this.overlay = document.getElementById("walkthroughOverlay");
        this.titleEl = document.getElementById("walkthroughTitle");
        this.iconEl = document.getElementById("walkthroughIcon");
        this.badgeEl = document.getElementById("walkthroughStepBadge");
        this.descEl = document.getElementById("walkthroughDescription");
        this.highlightsEl = document.getElementById("walkthroughHighlights");
        this.dotsEl = document.getElementById("walkthroughDots");
        this.prevBtn = document.getElementById("btnWalkthroughPrev");
        this.nextBtn = document.getElementById("btnWalkthroughNext");
        this.skipBtn = document.getElementById("btnWalkthroughSkip");
        this.closeBtn = document.getElementById("btnWalkthroughClose");

        this.initEventListeners();
    }

    initEventListeners() {
        if (!this.overlay) return;

        this.prevBtn?.addEventListener("click", () => this.prev());
        this.nextBtn?.addEventListener("click", () => this.next());
        this.skipBtn?.addEventListener("click", () => this.close());
        this.closeBtn?.addEventListener("click", () => this.close());

        document.getElementById("btnStartWalkthrough")?.addEventListener("click", () => {
            this.start(0);
        });

        // Keyboard navigation
        document.addEventListener("keydown", (e) => {
            if (!this.isOpen()) return;
            if (e.key === "ArrowRight") this.next();
            if (e.key === "ArrowLeft") this.prev();
            if (e.key === "Escape") this.close();
        });
    }

    isOpen() {
        return this.overlay && !this.overlay.classList.contains("hidden");
    }

    start(stepIndex = 0) {
        this.currentStep = stepIndex;
        if (!this.overlay) return;
        this.overlay.classList.remove("hidden");
        this.overlay.classList.add("flex");
        this.renderStep();
    }

    close() {
        if (!this.overlay) return;
        this.overlay.classList.add("hidden");
        this.overlay.classList.remove("flex");
        localStorage.setItem("paideia_genesis_walkthrough_seen", "true");
    }

    next() {
        if (this.currentStep < WALKTHROUGH_STEPS.length - 1) {
            this.currentStep++;
            this.renderStep();
        } else {
            this.close();
            showToast("Walkthrough completed! Welcome to Paideia Genesis.", "success");
        }
    }

    prev() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.renderStep();
        }
    }

    renderStep() {
        const step = WALKTHROUGH_STEPS[this.currentStep];
        if (!step) return;

        // Switch to the view tab for this step
        if (step.view) {
            const tabMap = {
                "viewWiki": "tabBtnWiki",
                "viewGraph": "tabBtnGraph",
                "viewTutor": "tabBtnTutor",
                "viewAnki": "tabBtnAnki",
                "viewCurriculum": "tabBtnCurriculum"
            };
            const btnId = tabMap[step.view];
            if (btnId) {
                document.getElementById(btnId)?.click();
            }
        }

        // Update step UI elements
        if (this.titleEl) this.titleEl.textContent = step.title;
        if (this.iconEl) this.iconEl.textContent = step.icon;
        if (this.badgeEl) this.badgeEl.textContent = step.badge;
        if (this.descEl) this.descEl.innerHTML = step.description;

        // Render highlights
        if (this.highlightsEl) {
            this.highlightsEl.innerHTML = step.highlights.map(h => `<div class="leading-relaxed">${h}</div>`).join("");
        }

        // Render progress dots
        if (this.dotsEl) {
            this.dotsEl.innerHTML = WALKTHROUGH_STEPS.map((s, idx) => {
                const isActive = idx === this.currentStep;
                return `<button class="w-2 h-2 rounded-full transition-all duration-300 ${
                    isActive ? 'bg-indigo-400 w-5 shadow-sm shadow-indigo-400/50' : 'bg-slate-700 hover:bg-slate-600'
                }" onclick="window.walkthroughManager.start(${idx})" title="Go to step ${idx + 1}"></button>`;
            }).join("");
        }

        // Update button labels
        if (this.prevBtn) {
            this.prevBtn.disabled = this.currentStep === 0;
        }
        if (this.nextBtn) {
            if (this.currentStep === WALKTHROUGH_STEPS.length - 1) {
                this.nextBtn.textContent = "Finish Tour 🎉";
                this.nextBtn.className = "text-xs text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 px-4 py-1.5 rounded-lg font-semibold shadow-md transition cursor-pointer";
            } else {
                this.nextBtn.textContent = "Next →";
                this.nextBtn.className = "text-xs text-white bg-gradient-to-r from-indigo-600 to-sky-600 hover:from-indigo-500 hover:to-sky-500 px-4 py-1.5 rounded-lg font-semibold shadow-md transition cursor-pointer";
            }
        }
    }
}
