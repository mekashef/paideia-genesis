"""Wiki Flashcard Compiler for Paideia Genesis.
Synthesizes USMLE-grade Cloze and Q&A flashcards across all Medical Wiki modules:
- Differentials (tabular comparative contrasts)
- Exam Traps (high-yield board traps and pearls)
- Entities (pharmacology, pathogens, transporters, biomarkers)
- Concepts & Sessions (pathophysiology, clinical triads, formulas, embryology)
"""
import re
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

def get_clean_text(s: str) -> str:
    """Strips markdown bold, italics, and extra whitespace."""
    s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
    s = re.sub(r'\*(.*?)\*', r'\1', s)
    return s.strip()

def atomize_card(card: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Atomizes a multi-cloze card into distinct single-unknown cards while preserving Anki cloze syntax.
    
    Adheres to Piotr Wozniak's Minimum Information Principle for spaced repetition:
    each derived card tests strictly 1 unknown topic/blank, while preserving all other
    variables as revealed plain text for surrounding grammatical and clinical context.
    
    If the card already contains <= 1 cloze deletion or is standard Q&A, it is returned as-is.
    """
    text = card.get("text") or card.get("front") or ""
    cloze_pattern = re.compile(r'\{\{c(\d+)::([^}]+)\}\}')
    matches = list(cloze_pattern.finditer(text))

    if len(matches) <= 1:
        single_card = dict(card)
        single_card["is_atomic"] = True
        single_card["cloze_count"] = len(matches)
        single_card["cloze_index"] = 1 if len(matches) == 1 else 0
        single_card["total_clozes"] = len(matches)
        if len(matches) == 1:
            single_card["target_unknown"] = matches[0].group(2).split("::")[0]
        return [single_card]

    atomic_cards = []
    base_id = card.get("id", "card")
    base_tags = list(card.get("tags", []))
    if "Atomic" not in base_tags:
        base_tags.append("Atomic")
    if "Single-Unknown" not in base_tags:
        base_tags.append("Single-Unknown")

    atomic_states = card.get("atomic_states", {})

    for idx, match in enumerate(matches, 1):
        def repl(m):
            if m.start() == match.start():
                # Keep target cloze as valid Anki cloze c1
                return f"{{{{c1::{m.group(2)}}}}}"
            else:
                # Reveal surrounding context cloze as plain text (strip hint if any)
                return m.group(2).split("::")[0]

        single_text = cloze_pattern.sub(repl, text)
        target_answer = match.group(2).split("::")[0]
        child_id = f"{base_id}-c{idx}"

        child = dict(card)
        child["id"] = child_id
        child["parent_id"] = base_id
        child["text"] = single_text
        if "front" in child and card.get("front"):
            child["front"] = single_text
        child["target_unknown"] = target_answer
        child["cloze_index"] = idx
        child["total_clozes"] = len(matches)
        child["is_atomic"] = True
        child["cloze_count"] = 1
        child["tags"] = list(base_tags)
        child["subtitle"] = f"Unknown {idx} of {len(matches)}: {target_answer[:35]}"

        # If child card has its own recorded review in parent's atomic_states, apply it
        if child_id in atomic_states:
            st = atomic_states[child_id]
            child["repetitions"] = st.get("repetitions", 0)
            child["interval"] = st.get("interval", 1)
            child["ease_factor"] = st.get("ease_factor", 2.5)
            child["due_date"] = st.get("due_date", datetime.date.today().isoformat())
            child["last_reviewed"] = st.get("last_reviewed", None)
            child["mastery"] = st.get("mastery", "unreviewed")

        atomic_cards.append(child)

    return atomic_cards

class WikiFlashcardCompiler:
    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir

    def compile_all(self, existing_cards: Optional[List[Dict[str, Any]]] = None, atomic_cards: bool = False) -> List[Dict[str, Any]]:
        """Compiles cards from all wiki sources and preserves review state of existing cards."""
        existing_map = {}
        if existing_cards:
            for c in existing_cards:
                # Key by normalized text / front
                norm_key = re.sub(r'\s+', ' ', (c.get("text") or c.get("front") or "")).strip()
                if norm_key:
                    existing_map[norm_key] = c

        all_cards: List[Dict[str, Any]] = []

        # 1. Differentials
        all_cards.extend(self._compile_differentials())
        # 2. Exam Traps
        all_cards.extend(self._compile_exam_traps())
        # 3. Entities (Pharmacology & Pathogens)
        all_cards.extend(self._compile_entities())
        # 4. Concepts & Pathophysiology
        all_cards.extend(self._compile_concepts())
        # 5. Course Sessions
        all_cards.extend(self._compile_sessions())
        # 6. EECS & Engineering Starter Cards
        all_cards.extend(self._compile_eecs_cards())
        # 7. Dynamic extraction from all wiki markdown files
        all_cards.extend(self._compile_from_markdown_files())

        # Merge with existing cards to preserve review history and custom user cards
        merged: List[Dict[str, Any]] = []
        seen_texts = set()

        for card in all_cards:
            norm_key = re.sub(r'\s+', ' ', (card.get("text") or card.get("front") or "")).strip()
            if not norm_key or norm_key in seen_texts:
                continue
            seen_texts.add(norm_key)

            if norm_key in existing_map:
                old = existing_map[norm_key]
                # Preserve review state
                card["repetitions"] = old.get("repetitions", 0)
                card["interval"] = old.get("interval", 1)
                card["ease_factor"] = old.get("ease_factor", 2.5)
                card["due_date"] = old.get("due_date", datetime.date.today().isoformat())
                card["last_reviewed"] = old.get("last_reviewed", None)
                card["mastery"] = old.get("mastery", "unreviewed")
                if "id" in old:
                    card["id"] = old["id"]
                if "atomic_states" in old:
                    card["atomic_states"] = old["atomic_states"]
            else:
                card["repetitions"] = 0
                card["interval"] = 1
                card["ease_factor"] = 2.5
                card["due_date"] = datetime.date.today().isoformat()
                card["last_reviewed"] = None
                card["mastery"] = "unreviewed"

            merged.append(card)

        # Also preserve any user-created custom cards (e.g. quick capture cards not in static templates)
        if existing_cards:
            for old in existing_cards:
                norm_key = re.sub(r'\s+', ' ', (old.get("text") or old.get("front") or "")).strip()
                if norm_key and norm_key not in seen_texts:
                    seen_texts.add(norm_key)
                    merged.append(old)

        # Assign sequential IDs if missing
        for idx, card in enumerate(merged, start=1):
            if not card.get("id"):
                card["id"] = f"card-{idx:03d}"

        if atomic_cards:
            derived_atomic: List[Dict[str, Any]] = []
            for card in merged:
                derived_atomic.extend(atomize_card(card))
            return derived_atomic

        return merged

    def _compile_differentials(self) -> List[Dict[str, Any]]:
        cards = []
        diff_dir = self.wiki_dir / "differentials"
        if not diff_dir.exists() or not any(diff_dir.glob("*.md")):
            return cards

        # 1. Crohn's vs Ulcerative Colitis
        cards.append({
            "type": "differential",
            "text": "The microscopic hallmark distinguishing Crohn's disease from Ulcerative Colitis is the presence of {{c1::noncaseating granulomas}} and {{c2::transmural inflammation}}.",
            "pearl": "Ulcerative colitis features crypt abscesses limited to mucosal and submucosal layers.",
            "tags": ["HST121", "Gastroenterology", "IBD", "USMLE-Step-1"],
            "source": "differentials/crohns-vs-ulcerative-colitis.md",
            "wiki_slug": "differentials/crohns-vs-ulcerative-colitis.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "Gross endoscopic examination showing {{c1::skip lesions, cobblestone mucosa, and creeping fat}} indicates {{c2::Crohn's disease}}, whereas continuous rectosigmoid involvement with a {{c3::lead-pipe sign}} indicates {{c4::Ulcerative Colitis}}.",
            "pearl": "Crohn's can involve any segment from mouth to anus; UC is strictly colonic starting at the rectum.",
            "tags": ["HST121", "Gastroenterology", "IBD", "Pathology"],
            "source": "differentials/crohns-vs-ulcerative-colitis.md",
            "wiki_slug": "differentials/crohns-vs-ulcerative-colitis.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "In inflammatory bowel disease, cigarette smoking {{c1::worsens}} Crohn's disease, but is paradoxically {{c2::protective}} against Ulcerative Colitis.",
            "pearl": "Classic Step 1 question: former smoker who recently quit develops bloody diarrhea, diagnosing UC flare.",
            "tags": ["HST121", "Gastroenterology", "IBD", "Board-Trap"],
            "source": "differentials/crohns-vs-ulcerative-colitis.md",
            "wiki_slug": "differentials/crohns-vs-ulcerative-colitis.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "In patients with Crohn's disease involving the terminal ileum, calcium oxalate nephrolithiasis occurs because unabsorbed {{c1::fatty acids}} bind luminal {{c2::calcium}}, leaving {{c3::oxalate}} unbound for hyperabsorption.",
            "pearl": "Enteric hyperoxaluria is a direct result of terminal ileal lipid malabsorption.",
            "tags": ["HST121", "Renal-GI-Crosslink", "Board-Trap", "USMLE-Step-1"],
            "source": "differentials/crohns-vs-ulcerative-colitis.md",
            "wiki_slug": "differentials/crohns-vs-ulcerative-colitis.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 3
        })
        cards.append({
            "type": "differential",
            "text": "The characteristic serological antibody finding in Crohn's disease is {{c1::ASCA (Anti-Saccharomyces cerevisiae)}} (+), whereas Ulcerative Colitis is associated with {{c2::p-ANCA (perinuclear antineutrophil cytoplasmic antibody)}} (+).",
            "pearl": "p-ANCA in UC is also linked with primary sclerosing cholangitis (PSC).",
            "tags": ["HST121", "Gastroenterology", "Serology", "IBD"],
            "source": "differentials/crohns-vs-ulcerative-colitis.md",
            "wiki_slug": "differentials/crohns-vs-ulcerative-colitis.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # 2. Secretory vs Osmotic Diarrhea
        cards.append({
            "type": "differential",
            "text": "A stool osmotic gap of {{c1::< 50 mOsm/kg}} indicates {{c2::secretory diarrhea}} (which persists during fasting), whereas a gap of {{c3::> 125 mOsm/kg}} indicates {{c4::osmotic diarrhea}} (which stops with fasting).",
            "pearl": "Formula: Stool Osmotic Gap = 290 - 2 * ([Na+]stool + [K+]stool).",
            "tags": ["HST121", "Physiology", "Diarrhea", "High-Yield"],
            "source": "differentials/secretory-vs-osmotic-diarrhea.md",
            "wiki_slug": "differentials/secretory-vs-osmotic-diarrhea.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "Secretory diarrhea is caused by active electrolyte secretion driven by elevated {{c1::cAMP (e.g. Vibrio cholerae)}} or {{c2::VIP (VIPoma)}}, whereas osmotic diarrhea is caused by unabsorbed solutes such as {{c3::lactose}} or {{c4::polyethylene glycol}}.",
            "pearl": "Secretory diarrhea features large-volume watery stool (>1 L/day) unaffected by oral NPO status.",
            "tags": ["HST121", "Physiology", "Diarrhea", "Endocrine"],
            "source": "differentials/secretory-vs-osmotic-diarrhea.md",
            "wiki_slug": "differentials/secretory-vs-osmotic-diarrhea.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # 3. Unconjugated vs Conjugated Hyperbilirubinemia
        cards.append({
            "type": "differential",
            "text": "In unconjugated (indirect) hyperbilirubinemia, urine bilirubin is {{c1::absent}} because unconjugated bilirubin is {{c2::insoluble in water (tightly bound to albumin)}} and cannot filter across glomeruli.",
            "pearl": "Conjugated (direct) bilirubin is water-soluble and excreted in urine, causing dark tea-colored urine.",
            "tags": ["HST121", "Hepatology", "Jaundice", "Biochemistry"],
            "source": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "wiki_slug": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "The hereditary hyperbilirubinemia caused by a mutation in canalicular transporter MRP2 (ABCC2), characterized by conjugated hyperbilirubinemia and a grossly {{c1::black/pigmented liver}}, is {{c2::Dubin-Johnson syndrome}}.",
            "pearl": "Rotor syndrome presents similarly with direct hyperbilirubinemia, but has normal liver pigmentation.",
            "tags": ["HST121", "Hepatology", "Jaundice", "Genetics"],
            "source": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "wiki_slug": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "differential",
            "text": "Gilbert syndrome is caused by a mild hereditary reduction in {{c1::UGT1A1 (UDP-glucuronosyltransferase)}} activity, producing benign episodic {{c2::unconjugated}} jaundice during {{c3::fasting, illness, or physical exertion}}.",
            "pearl": "Liver biopsy and standard hepatic enzymes (AST, ALT, Alk Phos) are completely normal.",
            "tags": ["HST121", "Hepatology", "Genetics", "USMLE-Step-1"],
            "source": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "wiki_slug": "differentials/unconjugated-vs-conjugated-hyperbilirubinemia.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 1
        })

        # 4. Loop vs Thiazide Diuretics
        cards.append({
            "type": "differential",
            "text": "Regarding urinary calcium handling: Loop diuretics cause {{c1::hypocalcemia ('Loops Lose Ca2+')}}, whereas thiazide diuretics cause {{c2::hypercalcemia ('Thiazides Take Ca2+')}}.",
            "pearl": "Thiazides are clinically favored in hypertensive patients with recurrent calcium oxalate nephrolithiasis or osteoporosis.",
            "tags": ["Cardiology", "Renal", "Pharmacology", "USMLE-Step-1"],
            "source": "differentials/loop-vs-thiazide-diuretics.md",
            "wiki_slug": "differentials/loop-vs-thiazide-diuretics.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 1
        })
        cards.append({
            "type": "differential",
            "text": "Loop diuretics inhibit the {{c1::NKCC2 cotransporter}} in the {{c2::thick ascending limb of Henle}}, while thiazide diuretics inhibit the {{c3::NCC cotransporter}} in the {{c4::distal convoluted tubule}}.",
            "pearl": "Loops abolish the corticomedullary hyperosmolar gradient, producing profound diuresis.",
            "tags": ["Cardiology", "Renal", "Physiology", "High-Yield"],
            "source": "differentials/loop-vs-thiazide-diuretics.md",
            "wiki_slug": "differentials/loop-vs-thiazide-diuretics.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 1
        })

        # 5. GERD vs Eosinophilic Esophagitis
        cards.append({
            "type": "differential",
            "text": "A young male with dysphagia and food impaction whose esophageal biopsy demonstrates {{c1::>= 15 eosinophils per high-power field}} and endoscopy reveals {{c2::stacked circular rings (trachealization)}} that fail to respond to PPIs has {{c3::Eosinophilic Esophagitis (EoE)}}.",
            "pearl": "EoE is an immune-mediated condition strongly linked with asthma, eczema, and allergic rhinitis.",
            "tags": ["HST121", "Gastroenterology", "Esophagus", "Immunology"],
            "source": "differentials/gerd-vs-eosinophilic-esophagitis.md",
            "wiki_slug": "differentials/gerd-vs-eosinophilic-esophagitis.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # 6. Acute Cholecystitis vs Ascending Cholangitis
        cards.append({
            "type": "differential",
            "text": "Acute cholecystitis is characterized by gallbladder inflammation with a positive {{c1::Murphy sign}}, whereas ascending cholangitis involves common bile duct obstruction and presents with Charcot's triad: {{c2::fever, RUQ pain, and jaundice}}.",
            "pearl": "Ascending cholangitis escalates to Reynolds' pentad with shock and altered mental status, requiring urgent ERCP.",
            "tags": ["HST121", "Biliary", "Surgery", "Emergency"],
            "source": "differentials/acute-cholecystitis-vs-ascending-cholangitis.md",
            "wiki_slug": "differentials/acute-cholecystitis-vs-ascending-cholangitis.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })

        # 7. FAP vs Lynch Syndrome
        cards.append({
            "type": "differential",
            "text": "Familial Adenomatous Polyposis (FAP) is caused by autosomal dominant germline mutations in {{c1::APC (chromosome 5q)}} with thousands of polyps, whereas Lynch syndrome is caused by defective {{c2::DNA mismatch repair (MSH2, MLH1, MSH6, PMS2)}} with microsatellite instability.",
            "pearl": "Lynch syndrome features predominantly right-sided proximal colon cancer and extracolonic endometrial carcinoma.",
            "tags": ["HST121", "Oncology", "Genetics", "Colorectal"],
            "source": "differentials/fap-vs-lynch-syndrome.md",
            "wiki_slug": "differentials/fap-vs-lynch-syndrome.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        return cards

    def _compile_exam_traps(self) -> List[Dict[str, Any]]:
        cards = []
        trap_dir = self.wiki_dir / "exam_traps"
        if not trap_dir.exists() or not any(trap_dir.glob("*.md")):
            return cards

        # 1. HBV Serology Traps
        cards.append({
            "type": "trap",
            "text": "During the serological 'Window Period' of acute Hepatitis B infection, both {{c1::HBsAg}} and {{c2::Anti-HBs}} are negative, and the sole diagnostic marker present is {{c3::Anti-HBc IgM}}.",
            "pearl": "Anti-HBc IgM indicates acute infection; Anti-HBc IgG denotes chronic infection or past exposure.",
            "tags": ["HST121", "Hepatology", "Serology", "Board-Trap"],
            "source": "exam_traps/hepatitis-b-serology-traps.md",
            "wiki_slug": "exam_traps/hepatitis-b-serology-traps.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "trap",
            "text": "An individual vaccinated against Hepatitis B will be positive for {{c1::Anti-HBs only}}, while {{c2::Anti-HBc}} will be completely {{c3::negative}}.",
            "pearl": "Recombinant HBV vaccine contains HBsAg only, so the host never generates antibodies to the core antigen.",
            "tags": ["HST121", "Hepatology", "Immunology", "Board-Trap"],
            "source": "exam_traps/hepatitis-b-serology-traps.md",
            "wiki_slug": "exam_traps/hepatitis-b-serology-traps.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 1
        })
        cards.append({
            "type": "trap",
            "text": "In chronic Hepatitis B, the presence of {{c1::HBeAg}} correlates with high active viral replication and {{c2::extreme infectivity}}, whereas seroconversion to {{c3::Anti-HBe}} signals low replication.",
            "pearl": "Vertical transmission risk to newborns is >90% when the mother is HBeAg-positive without immunoprophylaxis.",
            "tags": ["HST121", "Hepatology", "Virology", "USMLE-Step-2-CK"],
            "source": "exam_traps/hepatitis-b-serology-traps.md",
            "wiki_slug": "exam_traps/hepatitis-b-serology-traps.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # 2. Biliary & Pancreatic Traps
        cards.append({
            "type": "trap",
            "text": "The wall of a pancreatic pseudocyst is composed of {{c1::fibrous and granulation tissue}}, lacking a true {{c2::epithelial lining}}.",
            "pearl": "This distinguishes pseudocysts from true cystic neoplasms like mucinous cystadenomas, which have malignant potential.",
            "tags": ["HST121", "Pancreas", "Pathology", "Board-Trap"],
            "source": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "wiki_slug": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "trap",
            "text": "Gallstone ileus occurs when a cholecystoenteric fistula allows a gallstone to migrate and obstruct the narrowest portion of the bowel: the {{c1::ileocecal valve}}.",
            "pearl": "Rigler's triad on abdominal plain film: small bowel obstruction, gallstone in right iliac fossa, and pneumobilia.",
            "tags": ["HST121", "Biliary", "Surgery", "Board-Trap"],
            "source": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "wiki_slug": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "trap",
            "text": "Spontaneous bacterial peritonitis (SBP) in cirrhotic ascites is diagnosed when diagnostic paracentesis shows an ascitic fluid absolute neutrophil count (ANC) of {{c1::>= 250 cells/mm3}}, requiring immediate empiric IV {{c2::cefotaxime or ceftriaxone}}.",
            "pearl": "Do NOT wait for fluid culture results before starting antibiotics; cultures can take 48h and up to 40% are negative.",
            "tags": ["HST121", "Hepatology", "Critical-Care", "Board-Trap"],
            "source": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "wiki_slug": "exam_traps/biliary-and-pancreatic-board-traps.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # 3. Cardiovascular & Diuretic Traps
        cards.append({
            "type": "trap",
            "text": "Initiating or escalating beta-blockers (e.g., carvedilol) during acute decompensated heart failure is {{c1::contraindicated}} because acute {{c2::negative inotropy}} blunts sympathetic compensatory drive and precipitates {{c3::cardiogenic shock}}.",
            "pearl": "Beta-blockers provide clear mortality benefit in STABLE chronic HFrEF, but are hazardous during acute congestion.",
            "tags": ["Cardiology", "Pharmacology", "Contraindications", "Board-Trap"],
            "source": "exam_traps/trap-cardio-vignette-001-a.md",
            "wiki_slug": "exam_traps/trap-cardio-vignette-001-a.md",
            "course": "Cardiopulmonary",
            "system": "Cardiology",
            "difficulty": 2
        })
        cards.append({
            "type": "trap",
            "text": "In a patient with severe sulfa allergy who requires potent loop diuresis, the only non-sulfa loop diuretic available is {{c1::ethacrynic acid}}.",
            "pearl": "Ethacrynic acid carries a higher risk of ototoxicity compared to furosemide and bumetanide.",
            "tags": ["Renal", "Pharmacology", "Allergy", "Board-Trap"],
            "source": "concepts/capture-sulfa-allergy-in-diuretics.md",
            "wiki_slug": "concepts/capture-sulfa-allergy-in-diuretics.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 2
        })
        cards.append({
            "type": "trap",
            "text": "The major USMLE board trap associated with SGLT2 inhibitors (e.g. empagliflozin) during surgical stress or starvation is {{c1::euglycemic diabetic ketoacidosis (euDKA)}}.",
            "pearl": "Serum glucose remains < 250 mg/dL due to persistent glycosuria, masking severe metabolic acidosis.",
            "tags": ["Endocrine", "Pharmacology", "Board-Trap"],
            "source": "concepts/sglt2-inhibitors.md",
            "wiki_slug": "concepts/sglt2-inhibitors.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 3
        })

        return cards

    def _compile_entities(self) -> List[Dict[str, Any]]:
        cards = []
        ent_dir = self.wiki_dir / "entities"
        if not ent_dir.exists() or not any(ent_dir.glob("*.md")):
            return cards

        # Pharmacology Entities
        cards.append({
            "type": "cloze",
            "text": "Lactulose treats hepatic encephalopathy by bacterial fermentation into short-chain fatty acids, acidifying the colonic lumen ($H^+$) and converting diffusible, neurotoxic {{c1::ammonia (NH3)}} into non-absorbable {{c2::ammonium (NH4+)}}, trapping it for excretion.",
            "pearl": "Dosing is titrated to achieve 2 to 3 soft bowel movements per day.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "High-Yield"],
            "source": "entities/lactulose.md",
            "wiki_slug": "entities/lactulose.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Rifaximin is an oral non-absorbable rifamycin antibiotic added to lactulose in refractory hepatic encephalopathy that acts by inhibiting bacterial {{c1::DNA-dependent RNA polymerase}}, reducing colonic {{c2::ammonia-producing flora}}.",
            "pearl": "Because it has < 0.4% systemic bioavailability, rifaximin has minimal systemic adverse effects.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "USMLE-Step-1"],
            "source": "entities/rifaximin.md",
            "wiki_slug": "entities/rifaximin.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Mesalamine (5-aminosalicylic acid / 5-ASA) is first-line maintenance therapy for {{c1::Ulcerative Colitis}}, functioning topically in the colonic mucosa by inhibiting {{c2::5-lipoxygenase (LOX) and leukotriene synthesis}}.",
            "pearl": "Unlike sulfasalazine, mesalamine lacks the sulfapyridine moiety and does not cause sulfa-mediated adverse effects or male infertility.",
            "tags": ["HST121", "Gastroenterology", "Pharmacology", "IBD"],
            "source": "entities/mesalamine-5asa.md",
            "wiki_slug": "entities/mesalamine-5asa.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Infliximab is a chimeric monoclonal antibody directed against {{c1::tumor necrosis factor-alpha (TNF-alpha)}}, indicated for induction and maintenance of moderate-to-severe and fistulizing {{c2::Crohn's disease}}.",
            "pearl": "Pre-treatment screening with PPD/IGRA is mandatory to rule out latent tuberculosis reactivation.",
            "tags": ["HST121", "Pharmacology", "Biologics", "IBD"],
            "source": "entities/infliximab.md",
            "wiki_slug": "entities/infliximab.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Sofosbuvir is a direct-acting antiviral for Hepatitis C that acts as a uridine nucleotide analog inhibitor of the HCV {{c1::NS5B RNA-dependent RNA polymerase}}, halting viral RNA chain elongation.",
            "pearl": "Co-administration with amiodarone is contraindicated due to severe symptomatic bradycardia.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "Virology"],
            "source": "entities/sofosbuvir.md",
            "wiki_slug": "entities/sofosbuvir.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Omeprazole produces profound gastric acid suppression by covalently binding and irreversibly inhibiting the {{c1::H+/K+ ATPase proton pump}} in gastric {{c2::parietal cells}}.",
            "pearl": "Long-term PPI therapy is associated with hypomagnesemia, impaired calcium absorption (osteoporotic fractures), and C. difficile infection.",
            "tags": ["HST121", "Gastroenterology", "Pharmacology", "PUD"],
            "source": "entities/omeprazole-ppi.md",
            "wiki_slug": "entities/omeprazole-ppi.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Cholestyramine is a bile acid sequestrant resin used to treat secretory diarrhea resulting from {{c1::terminal ileal resection or bile acid malabsorption}}, preventing bile acids from stimulating colonic chloride secretion.",
            "pearl": "Cholestyramine can bind and impair intestinal absorption of fat-soluble vitamins (A, D, E, K) and drugs like warfarin.",
            "tags": ["HST121", "Pharmacology", "Diarrhea", "High-Yield"],
            "source": "entities/cholestyramine.md",
            "wiki_slug": "entities/cholestyramine.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Octreotide is a synthetic somatostatin analog that controls acute esophageal variceal bleeding by inhibiting {{c1::glucagon and vasoactive peptide release}}, inducing selective {{c2::splanchnic arterial vasoconstriction}}.",
            "pearl": "Also used in VIPoma to suppress severe refractory watery secretory diarrhea.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "Critical-Care"],
            "source": "entities/octreotide.md",
            "wiki_slug": "entities/octreotide.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Azathioprine is a prodrug converted to {{c1::6-mercaptopurine (6-MP)}} that blocks purine nucleotide synthesis. It is inactivated by {{c2::thiopurine methyltransferase (TPMT)}} and {{c3::xanthine oxidase}}.",
            "pearl": "Co-administration with allopurinol (xanthine oxidase inhibitor) drastically spikes 6-thioguanine levels, causing life-threatening bone marrow suppression!",
            "tags": ["HST121", "Pharmacology", "Oncology", "Board-Trap"],
            "source": "entities/azathioprine-6mp.md",
            "wiki_slug": "entities/azathioprine-6mp.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 3
        })
        cards.append({
            "type": "cloze",
            "text": "D-penicillamine is a copper chelating agent containing a free sulfhydryl group that binds divalent copper to promote urinary excretion in {{c1::Wilson disease}}.",
            "pearl": "Requires co-administration with pyridoxine (vitamin B6) because penicillamine antagonizes B6.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "Genetics"],
            "source": "entities/d-penicillamine.md",
            "wiki_slug": "entities/d-penicillamine.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The primary diuretic of choice for cirrhotic ascites is {{c1::spironolactone (aldosterone antagonist)}} because splanchnic arterial vasodilation triggers severe secondary {{c2::hyperaldosteronism}}.",
            "pearl": "Furosemide is added in a 40 mg to 100 mg spironolactone ratio to maintain normokalemia.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "Cardiology"],
            "source": "entities/spironolactone.md",
            "wiki_slug": "entities/spironolactone.md",
            "course": "Both",
            "system": "Cardio-Hepatic",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Bismuth subsalicylate exerts antimicrobial action against {{c1::Helicobacter pylori}}, coats gastric mucosal ulcer beds, and inhibits {{c2::prostaglandin synthesis and chloride secretion}} in traveler's diarrhea.",
            "pearl": "Harmlessly causes dark black tongue and stool due to precipitation of bismuth sulfide.",
            "tags": ["HST121", "Gastroenterology", "Pharmacology", "Infectious-Disease"],
            "source": "entities/bismuth-subsalicylate.md",
            "wiki_slug": "entities/bismuth-subsalicylate.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Furosemide produces rapid symptomatic relief in acute pulmonary edema primarily by inducing {{c1::systemic venodilation (reducing preload)}} via prostaglandins, followed by {{c2::loop diuresis}}.",
            "pearl": "Co-administration with NSAIDs blunts furosemide's venodilatory and diuretic action by blocking prostaglandin synthesis.",
            "tags": ["Cardiology", "Renal", "Pharmacology", "USMLE-Step-1"],
            "source": "entities/furosemide.md",
            "wiki_slug": "entities/furosemide.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Carvedilol provides a proven mortality benefit in chronic HFrEF by blocking {{c1::beta-1, beta-2, and alpha-1 receptors}}, reducing neurohormonal sympathetic toxicity and decreasing {{c2::afterload}}.",
            "pearl": "Must only be initiated once the patient is euvolemic and stable after acute congestion is resolved.",
            "tags": ["Cardiology", "Pharmacology", "Heart-Failure", "High-Yield"],
            "source": "entities/carvedilol.md",
            "wiki_slug": "entities/carvedilol.md",
            "course": "Cardiopulmonary",
            "system": "Cardiology",
            "difficulty": 2
        })

        # Pathogens, Transporters & Biomarkers Entities
        cards.append({
            "type": "cloze",
            "text": "Helicobacter pylori produces bacterial {{c1::urease}}, converting urea into {{c2::ammonia and carbon dioxide}}, which neutralizes gastric acid locally and allows colonization of gastric mucosa.",
            "pearl": "This reaction forms the basis of the urea breath test and rapid urease biopsy test.",
            "tags": ["HST121", "Microbiology", "PUD", "High-Yield"],
            "source": "entities/helicobacter-pylori.md",
            "wiki_slug": "entities/helicobacter-pylori.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Cholera toxin produced by Vibrio cholerae causes profuse secretory rice-water diarrhea by ADP-ribosylating {{c1::Gs alpha}}, permanently activating adenylyl cyclase, raising intracellular {{c2::cAMP}}, and keeping {{c3::CFTR chloride channels}} open.",
            "pearl": "Oral rehydration solution works because sodium-glucose cotransport (SGLT1) remains intact despite CFTR hypersecretion.",
            "tags": ["HST121", "Microbiology", "Physiology", "Diarrhea"],
            "source": "entities/vibrio-cholerae.md",
            "wiki_slug": "entities/vibrio-cholerae.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Whipple disease (caused by Tropheryma whipplei) is diagnosed on duodenal lamina propria biopsy by the presence of foamy macrophages containing {{c1::PAS (Periodic acid-Schiff) positive}}, diastase-resistant and acid-fast negative rod-shaped bacilli.",
            "pearl": "Classic clinical tetrad: diarrhea/malabsorption, weight loss, migratory polyarthritis, and neurologic/cardiac symptoms.",
            "tags": ["HST121", "Microbiology", "Pathology", "Board-Trap"],
            "source": "entities/tropheryma-whipplei.md",
            "wiki_slug": "entities/tropheryma-whipplei.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 3
        })
        cards.append({
            "type": "cloze",
            "text": "Hepatitis C virus is a positive-sense single-stranded {{c1::RNA flavivirus}} that lacks {{c2::3' to 5' exonuclease proofreading activity}}, resulting in hypervariable envelope glycoproteins (E2) and high rates of chronic persistence (>80%).",
            "pearl": "Because of hypervariable antigenicity, developing an effective HCV vaccine has been elusive.",
            "tags": ["HST121", "Virology", "Hepatology", "USMLE-Step-1"],
            "source": "entities/hepatitis-c-virus.md",
            "wiki_slug": "entities/hepatitis-c-virus.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Hepatitis D virus (Delta agent) is a defective circular ssRNA virus that requires co-infection or superinfection with {{c1::Hepatitis B}} because it requires the {{c2::HBsAg envelope}} to coat its genome and enter hepatocytes.",
            "pearl": "Superinfection of a chronic HBV carrier with HDV dramatically escalates the risk of fulminant hepatitis and cirrhosis.",
            "tags": ["HST121", "Virology", "Hepatology", "High-Yield"],
            "source": "concepts/viral-hepatitis-and-serology.md",
            "wiki_slug": "concepts/viral-hepatitis-and-serology.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Wilson disease is caused by autosomal recessive mutations in {{c1::ATP7B (chromosome 13)}}, which impairs copper incorporation into {{c2::ceruloplasmin}} and biliary excretion of copper.",
            "pearl": "Features low serum ceruloplasmin, elevated urinary copper, Kayser-Fleischer rings, and basal ganglia degeneration.",
            "tags": ["HST121", "Hepatology", "Genetics", "USMLE-Step-1"],
            "source": "entities/atp7b.md",
            "wiki_slug": "entities/atp7b.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "In Hereditary Hemochromatosis, homozygous {{c1::HFE C282Y}} mutations downregulate hepatic synthesis of {{c2::hepcidin}}, leading to unrestrained iron export via enterocyte {{c3::ferroportin}} into systemic circulation.",
            "pearl": "Triad of 'bronze diabetes': micronodular cirrhosis, skin hyperpigmentation, and pancreatic beta-cell destruction.",
            "tags": ["HST121", "Hepatology", "Metabolic", "High-Yield"],
            "source": "entities/hepcidin-ferroportin.md",
            "wiki_slug": "entities/hepcidin-ferroportin.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Alpha-1 antitrypsin deficiency is caused by protein misfolding (most severe phenotype: {{c1::PiZZ}}), resulting in intrahepatocyte accumulation of {{c2::PAS-positive, diastase-resistant globules}} and uninhibited {{c3::neutrophil elastase}} in lung alveoli.",
            "pearl": "Causes both panacinar pulmonary emphysema and childhood/adult cirrhosis.",
            "tags": ["HST121", "Hepatology", "Pulmonology", "Pathology"],
            "source": "concepts/metabolic-liver-diseases.md",
            "wiki_slug": "concepts/metabolic-liver-diseases.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The premature intra-acinar activation of {{c1::trypsinogen to trypsin}} within pancreatic acinar cells is the critical initiating event that triggers enzymatic autodigestion in {{c2::acute pancreatitis}}.",
            "pearl": "Active trypsin subsequently cleaves prophospholipase A2 and proelastase, producing coagulative and liquefactive necrosis.",
            "tags": ["HST121", "Pancreas", "Biochemistry", "Pathology"],
            "source": "entities/trypsinogen-trypsin.md",
            "wiki_slug": "entities/trypsinogen-trypsin.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "In Cystic Fibrosis, autosomal recessive mutations in {{c1::CFTR}} impair cyclic-AMP regulated chloride and bicarbonate transport, causing dehydrated, viscous secretions that obstruct pancreatic ducts and cause {{c2::exocrine pancreatic insufficiency}}.",
            "pearl": "Patients present with steatorrhea, failure to thrive, and fat-soluble vitamin deficiencies (A, D, E, K).",
            "tags": ["HST121", "Pancreas", "Genetics", "Pediatrics"],
            "source": "entities/cftr.md",
            "wiki_slug": "entities/cftr.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The primary apical transporter mediating active conjugated bile acid reabsorption in the terminal ileum is {{c1::ASBT (Apical Sodium-dependent Bile acid Transporter)}}.",
            "pearl": "Disease or resection of > 100 cm of terminal ileum overwhelms hepatic bile acid synthesis, resulting in severe steatorrhea.",
            "tags": ["HST121", "Physiology", "Enterocyte", "Transport"],
            "source": "entities/asbt-bile-acid-transporter.md",
            "wiki_slug": "entities/asbt-bile-acid-transporter.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The most sensitive and specific serological screening test for Celiac Disease in an IgA-competent individual is {{c1::serum IgA anti-tissue transglutaminase (anti-tTG)}}.",
            "pearl": "Always check total serum IgA levels concurrently; selective IgA deficiency can cause false-negative IgA anti-tTG results!",
            "tags": ["HST121", "Gastroenterology", "Immunology", "Celiac"],
            "source": "entities/tissue-transglutaminase-ttg.md",
            "wiki_slug": "entities/tissue-transglutaminase-ttg.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The serum tumor marker used for periodic surveillance of hepatocellular carcinoma (HCC) in patients with cirrhosis is {{c1::Alpha-fetoprotein (AFP)}}.",
            "pearl": "Ultrasound combined with AFP every 6 months is standard recommended surveillance.",
            "tags": ["HST121", "Oncology", "Hepatology", "Biomarkers"],
            "source": "entities/alpha-fetoprotein-afp.md",
            "wiki_slug": "entities/alpha-fetoprotein-afp.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "The serum tumor marker associated with {{c1::pancreatic ductal adenocarcinoma}} and cholangiocarcinoma is {{c2::CA 19-9}}.",
            "pearl": "CA 19-9 is a sialylated Lewis blood group antigen used to monitor response to therapy and recurrence.",
            "tags": ["HST121", "Oncology", "Pancreas", "Biomarkers"],
            "source": "entities/ca-19-9.md",
            "wiki_slug": "entities/ca-19-9.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 1
        })

        return cards

    def _compile_concepts(self) -> List[Dict[str, Any]]:
        cards = []
        con_dir = self.wiki_dir / "concepts"
        if not con_dir.exists() or not any(con_dir.glob("*.md")):
            return cards

        # 1. Cirrhosis Pathophysiology
        cards.append({
            "type": "cloze",
            "text": "The Serum-Ascites Albumin Gradient (SAAG) is calculated as {{c1::Serum Albumin - Ascitic Fluid Albumin}}. A SAAG of {{c2::>= 1.1 g/dL}} indicates {{c3::portal hypertension}}.",
            "pearl": "High SAAG (>=1.1): Cirrhosis, Heart Failure, Budd-Chiari; Low SAAG (<1.1): Peritoneal carcinomatosis, TB peritonitis, Nephrotic syndrome.",
            "tags": ["HST121", "Hepatology", "Cirrhosis", "Calculations"],
            "source": "concepts/pathophysiology-of-cirrhosis.md",
            "wiki_slug": "concepts/pathophysiology-of-cirrhosis.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "In cirrhosis, sinusoidal portal hypertension stimulates endothelial nitric oxide release in the splanchnic circulation, causing massive {{c1::splanchnic arterial vasodilation}}, which drops effective circulating blood volume and triggers severe compensatory {{c2::RAAS and sympathetic activation}}.",
            "pearl": "This compensatory renal vasoconstriction eventually causes hepatorenal syndrome (HRS).",
            "tags": ["HST121", "Hepatology", "Physiology", "Cirrhosis"],
            "source": "concepts/pathophysiology-of-cirrhosis.md",
            "wiki_slug": "concepts/pathophysiology-of-cirrhosis.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "The MELD (Model for End-Stage Liver Disease) score utilized for liver transplant allocation is calculated from {{c1::Serum Bilirubin}}, {{c2::INR (prothrombin time)}}, {{c3::Serum Creatinine}}, and {{c4::Serum Sodium}}.",
            "pearl": "Higher MELD scores correlate linearly with 90-day pre-transplant mortality.",
            "tags": ["HST121", "Hepatology", "Transplantation", "Scoring"],
            "source": "concepts/chronic-liver-failure-and-meld.md",
            "wiki_slug": "concepts/chronic-liver-failure-and-meld.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # 2. Biliary Disorders
        cards.append({
            "type": "cloze",
            "text": "Biliary cholesterol gallstones form when the ratio of cholesterol to {{c1::bile salts and phospholipids (lecithin)}} exceeds the solubilization threshold, compounded by {{c2::gallbladder hypomotility}}.",
            "pearl": "Risk factors: Female, Forty, Fertile, Fat (estrogen increases HMG-CoA reductase and cholesterol saturation).",
            "tags": ["HST121", "Biliary", "Biochemistry", "High-Yield"],
            "source": "concepts/gallstones-and-biliary-tract-disorders.md",
            "wiki_slug": "concepts/gallstones-and-biliary-tract-disorders.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Black pigment gallstones are composed of calcium bilirubinate and form in the setting of {{c1::chronic hemolysis (sickle cell, spherocytosis, beta-thalassemia)}} or cirrhosis.",
            "pearl": "Brown pigment stones arise from biliary tract bacterial or parasitic infections (e.g. Clonorchis sinensis) producing bacterial beta-glucuronidase.",
            "tags": ["HST121", "Biliary", "Hematology", "Pathology"],
            "source": "concepts/gallstones-and-biliary-tract-disorders.md",
            "wiki_slug": "concepts/gallstones-and-biliary-tract-disorders.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Primary Biliary Cholangitis (PBC) is an autoimmune destruction of intrahepatic interlobular bile ducts that occurs predominantly in middle-aged women, characterized serologically by {{c1::Anti-Mitochondrial Antibodies (AMA >= 1:40)}}.",
            "pearl": "Presents with pruritus, fatigue, and cholestatic jaundice. First-line therapy is Ursodeoxycholic acid (UDCA).",
            "tags": ["HST121", "Hepatology", "Immunology", "USMLE-Step-1"],
            "source": "concepts/gallstones-and-biliary-tract-disorders.md",
            "wiki_slug": "concepts/gallstones-and-biliary-tract-disorders.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Primary Sclerosing Cholangitis (PSC) is characterized by concentric 'onion-skin' periductal fibrosis causing a {{c1::beaded appearance on MRCP/ERCP}}, strongly associated with {{c2::Ulcerative Colitis (70-80%)}}, and confers high risk for {{c3::cholangiocarcinoma}}.",
            "pearl": "Typically p-ANCA positive; unlike PBC, AMA is negative.",
            "tags": ["HST121", "Hepatology", "Biliary", "IBD"],
            "source": "concepts/gallstones-and-biliary-tract-disorders.md",
            "wiki_slug": "concepts/gallstones-and-biliary-tract-disorders.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })

        # 3. Esophageal Pathophysiology
        cards.append({
            "type": "cloze",
            "text": "Achalasia is characterized by failure of the Lower Esophageal Sphincter (LES) to relax and absent esophageal peristalsis due to degeneration of {{c1::nitric oxide and VIP-releasing inhibitory neurons}} in the {{c2::myenteric (Auerbach) plexus}}.",
            "pearl": "High-resolution manometry is the gold standard diagnostic test; barium swallow shows classic 'bird's beak' tapering.",
            "tags": ["HST121", "Esophagus", "Physiology", "High-Yield"],
            "source": "concepts/esophageal-disorders-and-motility.md",
            "wiki_slug": "concepts/esophageal-disorders-and-motility.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Boerhaave syndrome is a {{c1::transmural, full-thickness rupture}} of the distal esophagus typically caused by violent retching, presenting with severe retrosternal pain, subcutaneous emphysema, and {{c2::pneumomediastinum}}.",
            "pearl": "In contrast, a Mallory-Weiss tear is a non-transmural longitudinal mucosal laceration at the gastroesophageal junction.",
            "tags": ["HST121", "Esophagus", "Emergency", "Pathology"],
            "source": "concepts/esophageal-disorders-and-motility.md",
            "wiki_slug": "concepts/esophageal-disorders-and-motility.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # 4. Acid Peptic & Gastric Pathophysiology
        cards.append({
            "type": "cloze",
            "text": "Duodenal ulcers are typically associated with H. pylori antral gastritis and {{c1::hyperchlorhydria}}, presenting with epigastric pain that is {{c2::relieved by food}}, whereas gastric ulcers present with pain {{c3::worsened by food}} and require biopsy to rule out malignancy.",
            "pearl": "Duodenal ulcers carry virtually zero malignant potential; gastric ulcers can harbor gastric adenocarcinoma.",
            "tags": ["HST121", "Gastroenterology", "PUD", "Pathology"],
            "source": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "wiki_slug": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "Zollinger-Ellison Syndrome is a neuroendocrine tumor (gastrinoma) located in the duodenum or pancreas that secretes autonomous gastrin, producing hyperplastic gastric rugae, refractory peptic ulcers in atypical locations (e.g. {{c1::jejunum}}), and {{c2::secretory diarrhea}}.",
            "pearl": "Diagnosed by elevated fasting serum gastrin that fails to suppress (paradoxically increases) following intravenous secretin injection.",
            "tags": ["HST121", "Endocrine", "PUD", "Oncology"],
            "source": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "wiki_slug": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # 5. Colorectal Neoplasms
        cards.append({
            "type": "cloze",
            "text": "In the classical chromosomal instability (adenoma-to-carcinoma) sequence of colorectal cancer, the earliest initiating event is loss or mutation of {{c1::APC (5q)}}, followed by activating mutation in {{c2::KRAS (adenoma enlargement)}}, and finally loss of tumor suppressors {{c3::TP53 and DCC}}.",
            "pearl": "AK-53 mnemonic: APC -> KRAS -> p53.",
            "tags": ["HST121", "Oncology", "Pathology", "Genetics"],
            "source": "concepts/colorectal-neoplasms-and-polyps.md",
            "wiki_slug": "concepts/colorectal-neoplasms-and-polyps.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # 6. Intestinal Ischemia
        cards.append({
            "type": "cloze",
            "text": "Acute mesenteric ischemia classically presents with severe, sudden abdominal pain {{c1::out of proportion to physical examination findings}}, most frequently caused by an acute embolus occluding the {{c2::superior mesenteric artery (SMA)}}.",
            "pearl": "Atrial fibrillation is the most common predisposing risk factor.",
            "tags": ["HST121", "Surgery", "Vascular", "Emergency"],
            "source": "concepts/intestinal-pathology-and-ischemia.md",
            "wiki_slug": "concepts/intestinal-pathology-and-ischemia.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Ischemic colitis classically occurs in elderly patients following transient systemic hypotension, preferentially affecting 'watershed' colonic areas: the {{c1::splenic flexure (Griffiths point)}} and the {{c2::rectosigmoid junction (Sudeck point)}}.",
            "pearl": "Presents with cramping lower abdominal pain followed by hematochezia; CT reveals thumbprinting sign.",
            "tags": ["HST121", "Pathology", "Vascular", "USMLE-Step-1"],
            "source": "concepts/intestinal-pathology-and-ischemia.md",
            "wiki_slug": "concepts/intestinal-pathology-and-ischemia.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # 7. Embryology & Pediatric GI
        cards.append({
            "type": "cloze",
            "text": "During embryonic development, the physiological herniation of the midgut through the umbilical ring undergoes a total of {{c1::270 degrees counterclockwise rotation}} around the axis of the {{c2::superior mesenteric artery (SMA)}}.",
            "pearl": "Incomplete rotation leads to midgut malrotation, fibrous peritoneal Ladd bands, and catastrophic midgut volvulus.",
            "tags": ["HST121", "Embryology", "Pediatrics", "High-Yield"],
            "source": "concepts/gi-embryology-and-malrotation.md",
            "wiki_slug": "concepts/gi-embryology-and-malrotation.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Hirschsprung disease is caused by failure of {{c1::neural crest cells}} to migrate caudally into the distal rectum and colon, resulting in congenital absence of both the {{c2::submucosal (Meissner) and myenteric (Auerbach) plexuses}}.",
            "pearl": "Presents as failure to pass meconium within 48 hours of life; rectal suction biopsy confirms diagnosis.",
            "tags": ["HST121", "Pediatrics", "Embryology", "Pathology"],
            "source": "concepts/gi-embryology-and-malrotation.md",
            "wiki_slug": "concepts/gi-embryology-and-malrotation.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        return cards

    def _compile_sessions(self) -> List[Dict[str, Any]]:
        cards = []
        sess_dir = self.wiki_dir / "course_sessions"
        if not sess_dir.exists() or not any(sess_dir.glob("*.md")):
            return cards

        # Pancreatitis
        cards.append({
            "type": "cloze",
            "text": "The two most common etiologies of acute pancreatitis in adults are {{c1::biliary gallstone migration (40%)}} and {{c2::alcohol consumption (35%)}}.",
            "pearl": "Diagnostic confirmation requires at least 2 of 3 criteria: characteristic epigastric pain radiating to back, serum lipase >= 3x ULN, or cross-sectional imaging findings.",
            "tags": ["HST121", "Pancreas", "Pathology", "High-Yield"],
            "source": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "wiki_slug": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "The classic clinical triad of chronic pancreatitis consists of {{c1::pancreatic calcifications on imaging}}, {{c2::steatorrhea (exocrine failure)}}, and {{c3::type 3c diabetes mellitus (endocrine failure)}}.",
            "pearl": "Serum amylase and lipase may be completely normal in advanced chronic pancreatitis due to acinar burnout.",
            "tags": ["HST121", "Pancreas", "Gastroenterology", "USMLE-Step-1"],
            "source": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "wiki_slug": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })

        # Celiac Disease Pathology
        cards.append({
            "type": "cloze",
            "text": "Small intestinal endoscopic biopsy of the distal duodenum in Celiac Disease classically reveals {{c1::villous blunting/atrophy}}, {{c2::crypt hyperplasia}}, and {{c3::increased intraepithelial lymphocytes}}.",
            "pearl": "Cutaneous manifestation is dermatitis herpetiformis, characterized by granular IgA deposits in dermal papillae.",
            "tags": ["HST121", "Gastroenterology", "Pathology", "Celiac"],
            "source": "course_sessions/session-04-lipid-digestion-absorption-and-malabsorption.md",
            "wiki_slug": "concepts/lipid-malabsorption-and-celiac.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # Vascular Liver
        cards.append({
            "type": "cloze",
            "text": "Budd-Chiari syndrome is caused by thrombotic occlusion of the {{c1::hepatic veins or inferior vena cava}}, leading to severe centrilobular congestion, hepatomegaly, ascites, and a 'nutmeg liver' gross appearance.",
            "pearl": "Most frequently associated with myeloproliferative neoplasms (polycythemia vera / JAK2 V617F) and hypercoagulable states.",
            "tags": ["HST121", "Hepatology", "Hematology", "Vascular"],
            "source": "course_sessions/session-15-pathology-of-the-liver-hepatitis.md",
            "wiki_slug": "course_sessions/session-15-pathology-of-the-liver-hepatitis.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Reye syndrome is characterized by acute encephalopathy and microvesicular hepatic steatosis caused by administering {{c1::aspirin}} to children during viral infections (influenza, varicella), which inhibits mitochondrial {{c2::beta-oxidation}}.",
            "pearl": "Acetaminophen is the antipyretic of choice in children with fever to avoid Reye syndrome.",
            "tags": ["HST121", "Pediatrics", "Hepatology", "Pharmacology"],
            "source": "course_sessions/session-17-jaundice-bilirubin-metabolism-dili.md",
            "wiki_slug": "course_sessions/session-17-jaundice-bilirubin-metabolism-dili.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # Small Bowel & Malabsorption
        cards.append({
            "type": "cloze",
            "text": "Abetalipoproteinemia is an autosomal recessive deficiency of {{c1::microsomal triglyceride transfer protein (MTP)}}, preventing the assembly and secretion of {{c2::ApoB-48 and ApoB-100}} containing lipoproteins.",
            "pearl": "Presents in infancy with severe steatorrhea, failure to thrive, acanthocytosis (spurred RBCs), and progressive ataxia / retinitis pigmentosa.",
            "tags": ["HST121", "Biochemistry", "Pediatrics", "Malabsorption"],
            "source": "course_sessions/session-04-lipid-digestion-absorption-and-malabsorption.md",
            "wiki_slug": "course_sessions/session-04-lipid-digestion-absorption-and-malabsorption.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 3
        })

        # Embryology & Anatomy: Pectinate Line
        cards.append({
            "type": "cloze",
            "text": "Above the pectinate line, the anal canal is derived from {{c1::endoderm}}, receives visceral innervation (producing {{c2::painless internal hemorrhoids}}), and drains lymphatically to the {{c3::internal iliac lymph nodes}}.",
            "pearl": "Below the pectinate line: derived from ectoderm, somatic innervation (exquisitely painful external hemorrhoids), drains to superficial inguinal nodes.",
            "tags": ["HST121", "Anatomy", "Embryology", "High-Yield"],
            "source": "course_sessions/session-01-overview-of-embryology-and-physiology.md",
            "wiki_slug": "course_sessions/session-01-overview-of-embryology-and-physiology.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # Gastroduodenal: Parietal Cell Signaling
        cards.append({
            "type": "cloze",
            "text": "Gastric parietal cell acid secretion is stimulated by three physiological agonists: Histamine (acts on {{c1::H2 receptor via Gs/cAMP}}), Gastrin (acts on {{c2::CCK-B receptor via Gq/Ca2+}}), and Acetylcholine (acts on {{c3::M3 receptor via Gq/Ca2+}}).",
            "pearl": "Somatostatin and prostaglandins inhibit acid secretion by activating Gi, decreasing cAMP.",
            "tags": ["HST121", "Physiology", "PUD", "Pharmacology"],
            "source": "course_sessions/session-02-gastroduodenal-pathophysiology-and-disorders.md",
            "wiki_slug": "course_sessions/session-02-gastroduodenal-pathophysiology-and-disorders.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Autoimmune Metaplastic Atrophic Gastritis (AMAG) involves CD4+ T-cell and autoantibody destruction of gastric {{c1::parietal cells and intrinsic factor}}, causing achlorhydria, marked compensatory {{c2::hypergastrinemia}}, and {{c3::pernicious anemia (B12 deficiency)}}.",
            "pearl": "AMAG predominantly affects the body and fundus of the stomach, sparring the antrum.",
            "tags": ["HST121", "Hematology", "Immunology", "Pathology"],
            "source": "course_sessions/session-02-gastroduodenal-pathophysiology-and-disorders.md",
            "wiki_slug": "course_sessions/session-02-gastroduodenal-pathophysiology-and-disorders.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # Mucosal Immunology: M Cells & sIgA
        cards.append({
            "type": "cloze",
            "text": "In the gut-associated lymphoid tissue (GALT), specialized {{c1::M (microfold) cells}} overlying Peyer patches endocytose and deliver intact luminal antigens across the epithelial barrier directly to {{c2::dendritic cells and macrophages}}.",
            "pearl": "Pathogens such as Shigella, Salmonella, and Yersinia exploit M cells as portals of entry into the host.",
            "tags": ["HST121", "Immunology", "Physiology", "Microbiology"],
            "source": "course_sessions/session-03-mucosal-immunology-of-the-gi-tract.md",
            "wiki_slug": "course_sessions/session-03-mucosal-immunology-of-the-gi-tract.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # Esophageal Motility: Diffuse Esophageal Spasm & Plummer-Vinson
        cards.append({
            "type": "cloze",
            "text": "Diffuse esophageal spasm (DES) presents with episodic retrosternal chest pain mimicking myocardial infarction and dysphagia for solids and liquids, demonstrating a classic {{c1::'corkscrew' or 'rosary-bead' esophagus}} on barium swallow.",
            "pearl": "Manometry demonstrates repetitive, simultaneous high-amplitude non-peristaltic contractions.",
            "tags": ["HST121", "Esophagus", "Cardiology-Differential", "High-Yield"],
            "source": "course_sessions/session-05-minicases-esophagus-and-gastric-disorders.md",
            "wiki_slug": "course_sessions/session-05-minicases-esophagus-and-gastric-disorders.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Plummer-Vinson syndrome classically presents with the triad of {{c1::dysphagia due to upper esophageal webs}}, {{c2::iron deficiency anemia}}, and {{c3::glossitis / koilonychia (spoon nails)}}.",
            "pearl": "Carries an increased risk of esophageal squamous cell carcinoma.",
            "tags": ["HST121", "Hematology", "Oncology", "Pathology"],
            "source": "course_sessions/session-05-minicases-esophagus-and-gastric-disorders.md",
            "wiki_slug": "course_sessions/session-05-minicases-esophagus-and-gastric-disorders.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # Intestinal Pathology: C. difficile & Carcinoid
        cards.append({
            "type": "cloze",
            "text": "Clostridioides difficile colitis produces yellow-white mucosal pseudomembranes composed of {{c1::fibrin, mucin, and necrotic neutrophils}}, mediated by Toxin A (enterotoxin) and Toxin B (cytotoxin) which inactivate {{c2::Rho GTPases}} to disrupt the actin cytoskeleton.",
            "pearl": "First-line antimicrobial therapy is oral vancomycin or oral fidaxomicin.",
            "tags": ["HST121", "Microbiology", "Pharmacology", "Pathology"],
            "source": "course_sessions/session-07-pathology-of-the-intestines-ibd-ischemia-polyps.md",
            "wiki_slug": "course_sessions/session-07-pathology-of-the-intestines-ibd-ischemia-polyps.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Carcinoid syndrome (episodic cutaneous flushing, watery diarrhea, wheezing, and tricuspid regurgitation) occurs only after a neuroendocrine tumor has {{c1::metastasized to the liver (or originates extra-intestinally)}}, bypassing hepatic {{c2::monoamine oxidase (MAO)}} degradation of serotonin.",
            "pearl": "Diagnosed by elevated 24-hour urine 5-HIAA (5-hydroxyindoleacetic acid).",
            "tags": ["HST121", "Endocrine", "Oncology", "Cardiology"],
            "source": "course_sessions/session-07-pathology-of-the-intestines-ibd-ischemia-polyps.md",
            "wiki_slug": "course_sessions/session-07-pathology-of-the-intestines-ibd-ischemia-polyps.md",
            "course": "HST.121",
            "system": "Luminal GI",
            "difficulty": 2
        })

        # GI Neoplasms: Gastric Adenocarcinoma & Krukenberg
        cards.append({
            "type": "cloze",
            "text": "Diffuse gastric adenocarcinoma is characterized histologically by {{c1::signet-ring cells (mucin displacing nucleus to the periphery)}} and gross thickening of the stomach wall ('linitis plastica' or leather-bottle appearance) due to loss of the cell adhesion protein {{c2::E-cadherin (CDH1)}}.",
            "pearl": "Not associated with H. pylori or chronic atrophic gastritis.",
            "tags": ["HST121", "Oncology", "Pathology", "Genetics"],
            "source": "course_sessions/session-09-gastrointestinal-neoplasms.md",
            "wiki_slug": "course_sessions/session-09-gastrointestinal-neoplasms.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "A Krukenberg tumor represents metastasis of a mucin-producing signet-ring cell adenocarcinoma (most commonly from the {{c1::stomach}}) to the {{c2::bilateral ovaries}}.",
            "pearl": "Sister Mary Joseph nodule refers to subcutaneous metastasis to the umbilicus.",
            "tags": ["HST121", "Oncology", "Pathology", "USMLE-Step-1"],
            "source": "course_sessions/session-09-gastrointestinal-neoplasms.md",
            "wiki_slug": "course_sessions/session-09-gastrointestinal-neoplasms.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # Lipid Biochemistry: CYP7A1
        cards.append({
            "type": "cloze",
            "text": "The rate-limiting enzymatic step in hepatic de novo bile acid synthesis from cholesterol is catalyzed by {{c1::cholesterol 7-alpha-hydroxylase (CYP7A1)}}, which is subject to feedback inhibition by {{c2::bile acids (via FXR nuclear receptor)}}.",
            "pearl": "Fibrate medications inhibit CYP7A1, increasing biliary cholesterol saturation and predisposing to cholesterol gallstones.",
            "tags": ["HST121", "Biochemistry", "Biliary", "Pharmacology"],
            "source": "course_sessions/session-10-physiological-chemistry-of-gi-lipids.md",
            "wiki_slug": "course_sessions/session-10-physiological-chemistry-of-gi-lipids.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 3
        })

        # Pancreatic & Biliary Neoplasms
        cards.append({
            "type": "cloze",
            "text": "Pancreatic head adenocarcinoma classically presents with {{c1::painless obstructive jaundice}}, weight loss, and a palpable, non-tender gallbladder (known as {{c2::Courvoisier sign}}).",
            "pearl": "Migratory superficial thrombophlebitis in pancreatic cancer is known as Trousseau syndrome.",
            "tags": ["HST121", "Oncology", "Pancreas", "Surgery"],
            "source": "course_sessions/session-12-pathology-of-pancreas-and-biliary-tract.md",
            "wiki_slug": "course_sessions/session-12-pathology-of-pancreas-and-biliary-tract.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "A Klatskin tumor is a cholangiocarcinoma arising specifically at the {{c1::confluence of the right and left hepatic ducts (biliary bifurcation)}}, presenting with severe progressive jaundice and marked intrahepatic duct dilation.",
            "pearl": "Strong risk factors: Primary Sclerosing Cholangitis (PSC) and Clonorchis sinensis infection.",
            "tags": ["HST121", "Oncology", "Biliary", "Pathology"],
            "source": "course_sessions/session-12-pathology-of-pancreas-and-biliary-tract.md",
            "wiki_slug": "course_sessions/session-12-pathology-of-pancreas-and-biliary-tract.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 2
        })

        # Hepatic Immunology & Allograft
        cards.append({
            "type": "cloze",
            "text": "Autoimmune Hepatitis (AIH Type 1) occurs predominantly in young women, presenting with hypergammaglobulinemia (elevated IgG), interface hepatitis rich in {{c1::plasma cells}}, and positivity for {{c2::Antinuclear Antibodies (ANA) and Anti-Smooth Muscle Antibodies (ASMA)}}.",
            "pearl": "Standard medical therapy is systemic corticosteroids (prednisone) combined with azathioprine.",
            "tags": ["HST121", "Hepatology", "Immunology", "High-Yield"],
            "source": "course_sessions/session-16-immunology-of-the-liver.md",
            "wiki_slug": "course_sessions/session-16-immunology-of-the-liver.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Acute cellular allograft rejection following liver transplantation is mediated by recipient T-lymphocytes attacking the portal triad, histologically demonstrating the classic triad of: {{c1::portal inflammation}}, {{c2::bile ductitis (endothelialitis)}}, and {{c3::endotheliitis (subendothelial infiltration of portal/central veins)}}.",
            "pearl": "Responsive to high-dose pulse intravenous corticosteroid therapy.",
            "tags": ["HST121", "Hepatology", "Transplantation", "Immunology"],
            "source": "course_sessions/session-16-immunology-of-the-liver.md",
            "wiki_slug": "course_sessions/session-16-immunology-of-the-liver.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 3
        })

        # End-Stage Liver Disease: HRS & HPS
        cards.append({
            "type": "cloze",
            "text": "Hepatorenal syndrome (HRS) is functional, progressive renal vasoconstriction occurring in end-stage cirrhosis with ascites, diagnosed when serum creatinine rises without intrinsic renal disease and fails to improve after {{c1::withdrawal of diuretics and 2 days of IV albumin volume expansion}}.",
            "pearl": "Medical treatment combines IV albumin with vasoconstrictors: terlipressin or norepinephrine.",
            "tags": ["HST121", "Hepatology", "Renal", "Critical-Care"],
            "source": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "wiki_slug": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 3
        })
        cards.append({
            "type": "cloze",
            "text": "Hepatopulmonary syndrome (HPS) consists of the triad of advanced liver disease, intrapulmonary precapillary vascular dilatations, and arterial hypoxemia that paradoxically worsens in the upright position (known as {{c1::platypnea-orthodeoxia}}).",
            "pearl": "Confirmed by contrast-enhanced agitated saline echocardiography showing delayed microbubbles in the left atrium (>3 cardiac cycles).",
            "tags": ["HST121", "Hepatology", "Pulmonology", "High-Yield"],
            "source": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "wiki_slug": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 3
        })

        # Portal Hypertension & Variceal Prophylaxis
        cards.append({
            "type": "cloze",
            "text": "Primary pharmacological prophylaxis against variceal hemorrhage in cirrhotic patients with medium-to-large esophageal varices is achieved with {{c1::non-selective beta-blockers (propranolol or nadolol)}}, which decrease portal inflow by blocking {{c2::beta-2 splanchnic vasodilation (allowing unopposed alpha-1 vasoconstriction)}}.",
            "pearl": "Beta-1 blockade also reduces cardiac output, further attenuating portal pressures.",
            "tags": ["HST121", "Hepatology", "Pharmacology", "High-Yield"],
            "source": "course_sessions/session-20-pathophysiological-consequences-of-cirrhosis.md",
            "wiki_slug": "course_sessions/session-20-pathophysiological-consequences-of-cirrhosis.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # Cardiopulmonary Inotropes & Heart Failure Pharmacology
        cards.append({
            "type": "cloze",
            "text": "Milrinone is a selective {{c1::phosphodiesterase-3 (PDE3) inhibitor}} used in cardiogenic shock that prevents cAMP degradation, producing increased intracellular calcium in cardiac myocytes ({{c2::positive inotropy}}) and vascular smooth muscle relaxation ({{c3::vasodilation / afterload reduction}}).",
            "pearl": "Classified as an 'inodilator'; excreted by kidneys and requires dose reduction in renal insufficiency.",
            "tags": ["Cardiology", "Pharmacology", "Critical-Care", "High-Yield"],
            "source": "concepts/acute-decompensated-heart-failure.md",
            "wiki_slug": "concepts/acute-decompensated-heart-failure.md",
            "course": "Cardiopulmonary",
            "system": "Cardiology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "Dobutamine is a synthetic catecholamine with predominant {{c1::beta-1 adrenergic agonist}} activity (and mild beta-2/alpha-1), used in cardiogenic shock to increase {{c2::cardiac contractility and stroke volume}} with minimal change in vascular resistance.",
            "pearl": "Can trigger ventricular arrhythmias and increases myocardial oxygen demand.",
            "tags": ["Cardiology", "Pharmacology", "Critical-Care"],
            "source": "concepts/acute-decompensated-heart-failure.md",
            "wiki_slug": "concepts/acute-decompensated-heart-failure.md",
            "course": "Cardiopulmonary",
            "system": "Cardiology",
            "difficulty": 2
        })
        cards.append({
            "type": "cloze",
            "text": "In patients with chronic Heart Failure with reduced Ejection Fraction (HFrEF), ACE inhibitors (e.g. lisinopril) provide proven long-term survival benefit by decreasing {{c1::Angiotensin II and Aldosterone}}, halting adverse {{c2::ventricular remodeling}} and decreasing {{c3::afterload}}.",
            "pearl": "Most common adverse effect is dry cough due to accumulation of bradykinin and substance P.",
            "tags": ["Cardiology", "Pharmacology", "Heart-Failure", "High-Yield"],
            "source": "concepts/acute-decompensated-heart-failure.md",
            "wiki_slug": "concepts/acute-decompensated-heart-failure.md",
            "course": "Cardiopulmonary",
            "system": "Cardiology",
            "difficulty": 1
        })
        cards.append({
            "type": "cloze",
            "text": "High-dose or rapid intravenous administration of loop diuretics (especially {{c1::ethacrynic acid}} or furosemide) can cause {{c2::ototoxicity (tinnitus, vertigo, or hearing loss)}}, which is synergistic when co-administered with {{c3::aminoglycosides (e.g. gentamicin)}}.",
            "pearl": "Caused by alteration of electrolyte gradients in the stria vascularis of the inner ear.",
            "tags": ["Renal", "Pharmacology", "Adverse-Effects", "Board-Trap"],
            "source": "concepts/loop-diuretics.md",
            "wiki_slug": "concepts/loop-diuretics.md",
            "course": "Cardiopulmonary",
            "system": "Renal",
            "difficulty": 2
        })

        # Crigler-Najjar vs Gilbert
        cards.append({
            "type": "differential",
            "text": "Crigler-Najjar syndrome Type 1 is caused by complete absence of hepatic {{c1::UGT1A1}}, resulting in severe unconjugated hyperbilirubinemia (> 20-50 mg/dL) presenting in neonates with fatal {{c2::kernicterus}} unless treated with continuous phototherapy or liver transplantation.",
            "pearl": "Type 2 has partial UGT1A1 activity (< 10%) and responds to enzyme induction with phenobarbital.",
            "tags": ["HST121", "Hepatology", "Genetics", "Pediatrics"],
            "source": "concepts/disorders-of-bilirubin-metabolism.md",
            "wiki_slug": "concepts/disorders-of-bilirubin-metabolism.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # SBP Albumin Co-Administration
        cards.append({
            "type": "cloze",
            "text": "In patients with spontaneous bacterial peritonitis (SBP), co-administering intravenous {{c1::albumin}} alongside cefotaxime/ceftriaxone decreases in-hospital mortality by 66% and prevents the development of {{c2::hepatorenal syndrome (HRS)}}.",
            "pearl": "Dosing protocol: 1.5 g/kg IV within 6 hours of diagnosis, followed by 1.0 g/kg on day 3.",
            "tags": ["HST121", "Hepatology", "Critical-Care", "High-Yield"],
            "source": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "wiki_slug": "course_sessions/session-19-clinic-chronic-liver-disease-transplantation.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 3
        })

        # Severe Acute Pancreatitis Signs
        cards.append({
            "type": "cloze",
            "text": "In severe necrotizing acute pancreatitis, retroperitoneal hemorrhage manifests physically as ecchymosis in the flank ({{c1::Grey Turner sign}}) or periumbilical region ({{c2::Cullen sign}}).",
            "pearl": "Both signs indicate tracking of blood from the retroperitoneum through tissue planes and carry high mortality.",
            "tags": ["HST121", "Pancreas", "Emergency", "Physical-Exam"],
            "source": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "wiki_slug": "course_sessions/session-11-physiology-biochemistry-pancreas-pancreatitis.md",
            "course": "HST.121",
            "system": "Pancreaticobiliary",
            "difficulty": 1
        })

        # Splanchnic Anatomy: Celiac Trunk
        cards.append({
            "type": "cloze",
            "text": "The celiac trunk arises from the abdominal aorta at the level of T12 and gives rise to three main branches supplying the foregut: the {{c1::Left gastric artery}}, {{c2::Splenic artery}}, and {{c3::Common hepatic artery}}.",
            "pearl": "Erosion of a posterior duodenal bulb ulcer characteristically bleeds from the gastroduodenal artery (GDA), a branch of the common hepatic.",
            "tags": ["HST121", "Anatomy", "Vascular", "Surgery"],
            "source": "course_sessions/session-01-overview-of-embryology-and-physiology.md",
            "wiki_slug": "course_sessions/session-01-overview-of-embryology-and-physiology.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 2
        })

        # Wilson Disease Diagnostics
        cards.append({
            "type": "cloze",
            "text": "The classic laboratory confirmation of Wilson disease includes decreased serum {{c1::ceruloplasmin (< 20 mg/dL)}}, markedly elevated 24-hour urinary {{c2::copper excretion (> 100 mcg/24h)}}, and golden-brown {{c3::Kayser-Fleischer rings}} in Descemet's membrane on slit-lamp exam.",
            "pearl": "Liver biopsy demonstrating quantitative hepatic copper concentration > 250 mcg/g dry weight is the definitive gold standard.",
            "tags": ["HST121", "Hepatology", "Genetics", "Diagnostics"],
            "source": "concepts/metabolic-liver-diseases.md",
            "wiki_slug": "concepts/metabolic-liver-diseases.md",
            "course": "HST.121",
            "system": "Hepatology",
            "difficulty": 2
        })

        # Gastric vs Duodenal Ulcers
        cards.append({
            "type": "differential",
            "text": "In peptic ulcer disease, gastric ulcers typically present with burning epigastric pain that is {{c1::worsened by meals (leading to weight loss)}}, whereas duodenal ulcers present with pain that is {{c2::relieved by food (leading to weight gain)}}.",
            "pearl": "Duodenal ulcers are almost always benign (>95% caused by H. pylori); gastric ulcers must be biopsied to exclude adenocarcinoma.",
            "tags": ["HST121", "Gastroenterology", "PUD", "Differential"],
            "source": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "wiki_slug": "concepts/peptic-ulcer-disease-and-h-pylori.md",
            "course": "HST.121",
            "system": "Gastroduodenal",
            "difficulty": 1
        })

        return cards

    def _compile_eecs_cards(self) -> List[Dict[str, Any]]:
        """Compiles starter cards from EECS Distributed Systems curriculum if present in wiki."""
        if not self.wiki_dir or not self.wiki_dir.exists():
            return []

        has_eecs = any(
            "6.033" in p.name or "eecs" in p.name or "consensus" in p.name
            for p in self.wiki_dir.rglob("*.md")
        )
        if not has_eecs:
            return []

        try:
            from src.wiki.eecs_curriculum import EECS_FLASHCARDS
            return [dict(c) for c in EECS_FLASHCARDS]
        except Exception:
            return []

    def _compile_from_markdown_files(self) -> List[Dict[str, Any]]:
        """Dynamically scans all markdown files across all subjects in wiki/ for cloze deletions.
        
        Enables universal living compilation: any topic (engineering, math, biology, research)
        added to the wiki with {{c1::...}} syntax is automatically converted into active recall cards.
        """
        cards = []
        if not self.wiki_dir or not self.wiki_dir.exists():
            return cards

        search_dirs = [
            self.wiki_dir / "concepts",
            self.wiki_dir / "differentials",
            self.wiki_dir / "entities",
            self.wiki_dir / "exam_traps",
            self.wiki_dir / "course_sessions",
            self.wiki_dir / "research",
        ]
        
        cloze_pattern = re.compile(r'\{\{c\d+::.+?\}\}')

        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for md_file in sdir.glob("*.md"):
                try:
                    text = md_file.read_text(encoding="utf-8")
                except Exception:
                    continue

                frontmatter: Dict[str, Any] = {}
                body = text
                if text.startswith("---"):
                    parts = text.split("---", 2)
                    if len(parts) >= 3:
                        body = parts[2]
                        for line in parts[1].splitlines():
                            if ":" in line:
                                k, v = line.split(":", 1)
                                frontmatter[k.strip().lower()] = v.strip()

                domain = frontmatter.get("domain", "General")
                course = frontmatter.get("course", "General")
                system = frontmatter.get("system", frontmatter.get("field", "Core"))
                tags_str = frontmatter.get("tags", "")
                tags = [t.strip().strip("[]'\"") for t in tags_str.split(",") if t.strip().strip("[]'\"")]
                if not tags:
                    tags = ["CompoundedNote", md_file.stem]

                lines = body.splitlines()
                for i, line in enumerate(lines):
                    line_clean = line.strip()
                    if cloze_pattern.search(line_clean):
                        # Clean leading list markers like "- " or "1. " or "> "
                        cleaned_line = re.sub(r'^(?:[-*+]|\d+\.|\>)\s*', '', line_clean)
                        # Look ahead for a pearl or explanation in the next 1-2 lines
                        pearl = ""
                        for j in range(i + 1, min(i + 3, len(lines))):
                            nxt = lines[j].strip()
                            if nxt.startswith(("> Pearl:", "> Tip:", "Pearl:", "Tip:", "Note:", "> Note:", "Insight:", "> Insight:")):
                                pearl = re.sub(r'^(?:> ?)?(?:Pearl|Tip|Note|Insight):\s*', '', nxt)
                                break
                        if not pearl and frontmatter.get("summary"):
                            pearl = frontmatter.get("summary")

                        rel_path = str(md_file.relative_to(self.wiki_dir))
                        cards.append({
                            "type": "cloze",
                            "text": cleaned_line,
                            "pearl": pearl,
                            "tags": list(tags),
                            "source": rel_path,
                            "wiki_slug": rel_path,
                            "course": course,
                            "domain": domain,
                            "system": system,
                            "difficulty": 2
                        })

        return cards


