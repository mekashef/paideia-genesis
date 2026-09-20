"""Comprehensive MIT OpenCourseWare HST.121 Gastroenterology Curriculum Data.
Covers all 20 lecture sessions with board-yield concepts, comparative differentials,
diagnostic traps, and Anki cloze flashcards.
"""

HST121_CONCEPTS = [
    {
        "slug": "gi-embryology-and-malrotation",
        "title": "GI Embryology, Midgut Volvulus & Vitelline Anomalies",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Embryology", "Pediatrics", "HST.121"],
        "summary": "Developmental gut morphogenesis including 270-degree midgut rotation, vascular axes, omphalocele vs gastroschisis, and vitelline duct remnants (Meckel diverticulum).",
        "content": """### Embryological Divisions & Vascular Supply
1. **Foregut**: Celiac artery supply. Extends from pharynx to proximal duodenum (above ampulla of Vater).
2. **Midgut**: Superior Mesenteric Artery (SMA) supply. Distal duodenum to proximal 2/3 of transverse colon.
3. **Hindgut**: Inferior Mesenteric Artery (IMA) supply. Distal 1/3 of transverse colon to upper anal canal (above pectinate line).

### Midgut Rotation & Malrotation
- During week 6, the midgut herniates through the umbilical ring. It undergoes a **270° counterclockwise rotation** around the SMA axis before returning to the abdominal cavity during week 10.
- **Malrotation**: Failure of complete rotation results in Ladd bands (fibrous bands compressing the duodenum) and a narrow mesenteric base, predisposing to **Midgut Volvulus** (twisting around the SMA leading to catastrophic bowel necrosis; presents with bilious emesis in a neonate).

### Abdominal Wall Defects
- **Omphalocele**: Herniation of abdominal contents into the umbilical cord, covered by a 3-layer sac (peritoneum + amnion). Associated with trisomies 13, 18, and Beckwith-Wiedemann syndrome. Elevated maternal AFP.
- **Gastroschisis**: Full-thickness lateral abdominal wall defect (usually right of umbilicus) with extruded bowel **NOT covered** by a protective sac. Not typically associated with chromosomal anomalies.

### Vitelline (Omphalomesenteric) Duct Remnants
- Failure of obliteration by week 7:
  - **Meckel Diverticulum**: Partial persistence; true diverticulum (all 3 bowel layers: mucosa, submucosa, muscularis). *Rule of 2s*: 2% of population, 2 inches long, within 2 feet of ileocecal valve, 2 types of ectopic tissue (**gastric mucosa** causing painless lower GI bleeding, or **pancreatic tissue**). Diagnosed via Technetium-99m pertechnetate scan (uptake by ectopic gastric parietal cells).
  - **Vitelline Fistula**: Complete failure to close $\\rightarrow$ continuous fecal drainage from the umbilicus.

Related: [[intestinal-pathology-and-ischemia]], [[peptic-ulcer-disease-and-h-pylori]]."""
    },
    {
        "slug": "esophageal-disorders-and-motility",
        "title": "Esophageal Motility, GERD, Barrett's & Esophageal Neoplasms",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Pathology", "Oncology", "HST.121"],
        "summary": "Mechanisms of esophageal clearance, lower esophageal sphincter dysmotility (Achalasia), acid reflux, Barrett's metaplasia, and esophageal tears (Mallory-Weiss vs Boerhaave).",
        "content": """### Esophageal Dysmotility: Achalasia
- **Pathophysiology**: Selective degeneration of inhibitory postganglionic nitrinergic neurons in the **myenteric (Auerbach) plexus**. Loss of NO and VIP causes failure of the Lower Esophageal Sphincter (LES) to relax and aperistalsis of the esophageal body.
- **Secondary Achalasia**: Chagas disease (*Trypanosoma cruzi* destroys myenteric plexuses; leads to megaesophagus, megacolon, dilated cardiomyopathy).
- **Diagnostics**: Barium esophagram shows dilated esophagus with smooth tapered narrowing (**"bird's beak"** sign). High-resolution manometry is gold standard (high resting LES pressure > 45 mmHg).

### Gastroesophageal Reflux Disease (GERD) & Barrett's Metaplasia
- **GERD**: Caused by transient LES relaxations (TLESRs), hypotensive LES, or sliding hiatal hernia. Presents with heartburn, regurgitation, water brash, nocturnal cough, and enamel erosion.
- **Barrett's Esophagus**: Specialized intestinal metaplasia where normal nonkeratinized stratified squamous epithelium is replaced by **nonciliated columnar epithelium with goblet cells** (alcian blue positive) in response to chronic acid and bile exposure.
- **Malignancy Risk**: Strongly predisposes to **Esophageal Adenocarcinoma** (distal 1/3 of esophagus). In contrast, **Squamous Cell Carcinoma** arises in the upper/mid esophagus and is linked to alcohol, tobacco, hot beverages, and Plummer-Vinson syndrome.

### Esophageal Ruptures & Tears
- **Mallory-Weiss Syndrome**: Longitudinal mucosal/submucosal tear at the gastroesophageal junction caused by severe retching/vomiting (classically alcoholics or bulimics). Presents with painful hematemesis. Benign, self-limiting.
- **Boerhaave Syndrome**: Full-thickness **transmural rupture** of the distal esophagus, usually on the left posterolateral wall, secondary to violent pressure increase during emesis. Leads to pneumomediastinum, subcutaneous emphysema (**Hamman sign** = crunching sound synchronous with heartbeat), and septic mediastinitis. High mortality, emergency surgical repair.

Related: [[peptic-ulcer-disease-and-h-pylori]], [[gi-imaging-and-endoscopy]]."""
    },
    {
        "slug": "mucosal-immunology-and-galt",
        "title": "Mucosal Immunology of the GI Tract & Secretory IgA",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Immunology", "Pathology", "HST.121"],
        "summary": "Architecture of gut mucosal immunity: Gut-Associated Lymphoid Tissue (GALT), Peyer's patches, M cells, dendritic cells, Secretory IgA, and oral tolerance.",
        "content": """### GALT Architecture & Antigen Sampling
- **Peyer's Patches**: Aggregated lymphoid follicles located predominantly in the antimesenteric wall of the **ileum**. Overlaid by specialized follicle-associated epithelium (FAE).
- **Microfold (M) Cells**: Specialized epithelial cells lacking apical microvilli and thick glycocalyx. They continuously sample luminal bacteria, viruses, and dietary antigens via transcytosis, delivering them to underlying subepithelial dendritic cells and B/T lymphocytes.
- Pathogens exploiting M cells for entry: *Salmonella enterica*, *Shigella flexneri*, *Yersinia pestis*, *Poliovirus*, and *Prions* (BSE/vCJD).

### Secretory IgA (sIgA) Synthesis & Function
1. Naive B cells in Peyer's patches undergo class-switch recombination to IgA under the influence of **TGF-beta** and **IL-5** secreted by regulatory T cells ($T_{reg}$) and dendritic cells.
2. Dimeric IgA (two monomeric units joined by a joining [J] chain) is produced by lamina propria plasma cells.
3. Transcytosis: Dimeric IgA binds the **polymeric immunoglobulin receptor (pIgR)** on the basolateral membrane of enterocytes and is transcytosed to the apical lumen.
4. Cleavage: The pIgR is enzymatically cleaved, leaving the **secretory component** attached to dimeric IgA. The secretory component protects sIgA against proteolytic degradation by gastric and pancreatic enzymes.
5. **Mechanism of Action**: Immune exclusion—neutralizes viral toxins and inhibits bacterial adherence without initiating inflammatory complement cascades (sIgA is non-complement-fixing).

### Oral Tolerance & Breakdown
- Continuous exposure to harmless dietary antigens induces peripheral tolerance mediated by FoxP3+ CD4+ $T_{reg}$ cells secreting IL-10 and TGF-beta.
- Breakdown of oral tolerance produces conditions such as **Celiac Disease** (gliadin hypersensitivity) and **Food Protein-Induced Enterocolitis**.

Related: [[lipid-malabsorption-and-celiac]], [[inflammatory-bowel-disease]]."""
    },
    {
        "slug": "peptic-ulcer-disease-and-h-pylori",
        "title": "Peptic Ulcer Disease & Helicobacter pylori",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Microbiology", "Pharmacology", "HST.121"],
        "summary": "Mucosal ulcerations primarily caused by H. pylori infection or NSAID usage, characterized by epigastric pain and bleeding risk.",
        "content": """### Pathophysiology
- **Helicobacter pylori**: Urease-producing, curved, gram-negative rod. Urease converts urea to ammonia ($NH_3$) and $CO_2$, buffering gastric acid to survive the acidic stomach. Induces chronic active antral gastritis, increasing gastrin secretion and acid output -> **Duodenal Ulcers (90%)** and **Gastric Ulcers (70%)**.
- **Duodenal vs Gastric Ulcer**:
  - *Duodenal*: Pain **improves** with meals (food stimulates alkaline duodenal secretions). Almost always benign.
  - *Gastric*: Pain **worsens** with meals (acid secretion on open mucosal erosion). 2-3% malignant (biopsy mandatory).

### Pharmacotherapy & Triple Therapy
- **First-line Quadruple Therapy**: Bismuth subsalicylate + Metronidazole + Tetracycline + PPI.
- **Classic Triple Therapy**: Clarithromycin + Amoxicillin (or Metronidazole if penicillin allergic) + PPI for 14 days.

### Board Exam Traps & Pitfalls
> [!CAUTION]
> **Zollinger-Ellison Syndrome (Gastrinoma)**:
> Suspect in patients with multiple, refractory, or jejunal ulcers with chronic diarrhea. Diagnosed via elevated fasting serum gastrin (>1000 pg/mL) and paradoxical increase in gastrin with secretin infusion!

Related: [[acute-decompensated-heart-failure]], [[renin-angiotensin-aldosterone-system]]."""
    },
    {
        "slug": "lipid-digestion-and-biochemistry",
        "title": "Biochemistry of Lipid Digestion, Micelles & Enterohepatic Circulation",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Biochemistry", "Physiology", "HST.121"],
        "summary": "Enzymatic hydrolysis of dietary triglycerides, mixed micellar solubilization, enterocyte absorption, chylomicron packaging, and bile acid cycling.",
        "content": """### Stages of Lipid Assimilation
1. **Emulsification**: Gastric churning and bile salts break large lipid droplets into micro-droplets ($1\\;\\mu\\text{m}$), greatly increasing surface area for enzymatic attack.
2. **Enzymatic Hydrolysis**:
   - **Pancreatic Lipase**: Cleaves dietary triglycerides at sn-1 and sn-3 positions into 2-monoacylglycerol (2-MAG) and 2 free fatty acids.
   - **Colipase**: Secreted as pro-colipase (cleaved by trypsin); anchors pancreatic lipase to the oil-water interface by displacing inhibitory bile salts.
   - **Cholesterol Esterase & Phospholipase A2**: Hydrolyzes cholesteryl esters and lecithin.
3. **Mixed Micellar Solubilization**:
   - Bile acids, when above their **Critical Micellar Concentration (CMC)**, spontaneously aggregate into polymolecular cylinders with hydrophobic cores containing 2-MAG, cholesterol, fatty acids, and fat-soluble vitamins (A, D, E, K).
4. **Enterocyte Uptake & Re-esterification**:
   - Micelles diffuse through the unstirred water layer; lipids dissociate and enter enterocytes via passive diffusion and NPC1L1 transporter (inhibited by Ezetimibe).
   - In the smooth ER, 2-MAG and fatty acids are re-synthesized into triglycerides by DGAT.

### Chylomicron Assembly & Abetalipoproteinemia
- Re-esterified triglycerides and cholesteryl esters are packaged with **Apolipoprotein B-48** mediated by **Microsomal Triglyceride Transfer Protein (MTP)**.
- Chylomicrons are exocytosed into intestinal lacteals (lymphatics), bypassing initial hepatic portal circulation.
- **Abetalipoproteinemia**: Autosomal recessive mutation in MTP gene. Enterocytes cannot package or secrete ApoB-48/ApoB-100 lipoproteins. Presents with severe fat malabsorption, failure to thrive, steatorrhea, ataxia (vitamin E deficiency), and **acanthocytes (spur cells)** on peripheral blood smear.

### Enterohepatic Circulation of Bile Acids
- 95% of bile acids are actively reabsorbed in the **terminal ileum** via the Apical Sodium-dependent Bile Acid Transporter (ASBT).
- Ileal resection (or severe Crohn's ileitis) halts bile acid recycling $\\rightarrow$ bile acid pool depletes $\\rightarrow$ unabsorbed bile salts spill into colon causing secretory diarrhea; fat malabsorption and gallstones result.

Related: [[lipid-malabsorption-and-celiac]], [[gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "lipid-malabsorption-and-celiac",
        "title": "Malabsorption Syndromes & Celiac Disease",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Immunology", "Pathology", "HST.121"],
        "summary": "Impaired nutrient assimilation caused by gluten-sensitive enteropathy, mucosal atrophy, and fat malabsorption.",
        "content": """### Celiac Disease (Gluten-Sensitive Enteropathy)
- **Immunopathogenesis**: Gliadin peptide interacts with HLA-DQ2 / HLA-DQ8. Deamidated by **tissue transglutaminase (tTG)**, presented by APCs to CD4+ T cells -> intraepithelial lymphocytosis, crypt hyperplasia, and **blunting / atrophy of duodenal villi**.
- **Serology**: Anti-tTG IgA (high sensitivity & specificity), Anti-endomysial IgA (EMA), Anti-deamidated gliadin peptide.
- **Clinical Presentation**: Steatorrhea, weight loss, iron-deficiency anemia, osteomalacia (vitamin D malabsorption), and **Dermatitis herpetiformis** (pruritic papulovesicles on extensor surfaces).

### Whipple Disease (Tropheryma whipplei)
- Gram-positive bacillus causing cardiac symptoms, arthralgias, neurologic symptoms, and diarrhea with **PAS-positive, acid-fast negative macrophages** in the lamina propria.

Related: [[inflammatory-bowel-disease]]."""
    },
    {
        "slug": "diarrheal-illness-and-fluid-transport",
        "title": "Diarrheal Pathophysiology, Fluid Transport & VIPoma",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Physiology", "Infectious-Disease", "HST.121"],
        "summary": "Intestinal fluid secretion and absorption mechanisms, distinguishing osmotic from secretory diarrhea using stool osmotic gap and clinical triggers.",
        "content": """### Intestinal Fluid Mechanics
The gastrointestinal tract receives ~9 Liters of fluid daily (2 L ingested, 7 L endogenous secretions: saliva, gastric, bile, pancreatic, succus entericus).
- Small intestine absorbs ~7 L.
- Colon absorbs 1.5 - 1.9 L, leaving only 100-200 mL excreted in stool daily.
- Diarrhea occurs when stool output exceeds 200 g/24h.

### Secretory Diarrhea Pathophysiology
- Driven by active chloride and bicarbonate secretion via the **CFTR (Cystic Fibrosis Transmembrane Conductance Regulator)** channel in crypt enterocytes.
- Second Messenger Cascades:
  - **cAMP Activation**: *Vibrio cholerae* (Cholera toxin ADP-ribosylates $G_{s\\alpha}$, keeping adenylyl cyclase permanently active); *Enterotoxigenic E. coli* (ETEC heat-labile toxin [LT]).
  - **cGMP Activation**: ETEC heat-stable toxin [ST]; activates guanylyl cyclase C.
  - **VIPoma (Verner-Morrison Syndrome / WDHA)**: Pancreatic islet tumor secreting Vasoactive Intestinal Peptide (VIP). Causes **W**atery **D**iarrhea, **H**ypokalemia, **A**chlorhydria.
- **Hallmark**: Stool Osmotic Gap is **normal (< 50 mOsm/kg)**. Diarrhea **persists despite fasting** and nocturnal stooling is common.

### Osmotic Diarrhea Pathophysiology
- Caused by ingestion of poorly absorbed, osmotically active solutes drawing water into the intestinal lumen.
- Etiologies: Lactase deficiency, Celiac disease, ingestion of magnesium-containing antacids or polyethylene glycol (osmotic laxatives).
- **Hallmark**: Stool Osmotic Gap is **elevated (> 125 mOsm/kg)**. Diarrhea **ceases during fasting**.

### Stool Osmotic Gap Formula
$$\\text{Stool Osmotic Gap} = 290 - 2 \\times \\left([\\text{Na}^+]_{\\text{stool}} + [\\text{K}^+]_{\\text{stool}}\\right)$$
- Normal ($< 50\\;\\text{mOsm/kg}$): Pure secretory diarrhea.
- Elevated ($> 125\\;\\text{mOsm/kg}$): Osmotic diarrhea.

Related: [[differentials/secretory-vs-osmotic-diarrhea]], [[inflammatory-bowel-disease]]."""
    },
    {
        "slug": "intestinal-pathology-and-ischemia",
        "title": "Intestinal Ischemia, Angiodysplasia & Small Bowel Obstruction",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Pathology", "Vascular", "HST.121"],
        "summary": "Vascular insufficiency of the mesentery, watershed areas, thumbprinting on imaging, angiodysplasia in Heyde syndrome, and mechanical bowel obstruction.",
        "content": """### Acute Mesenteric Ischemia
- **Etiology**: Embolic occlusion of the Superior Mesenteric Artery (SMA, ~50%, usually from cardiac source: atrial fibrillation or left ventricular mural thrombus), thrombosis overlying atherosclerosis, or nonocclusive mesenteric ischemia (NOMI) from shock/hypoperfusion.
- **Clinical Presentation**: Severe, diffuse abdominal **pain out of proportion to physical examination**. Later signs: peritoneal signs, hematochezia, severe lactic acidosis (bowel infarction).
- **Diagnosis & Treatment**: CT angiography showing SMA filling defect. Immediate surgical embolectomy / revascularization and resection of nonviable necrotic bowel.

### Ischemic Colitis (Watershed Distribution)
- Caused by systemic transient hypoperfusion (hypotension, heart failure, bypass surgery) affecting the low-flow watershed zones:
  1. **Griffiths' Point**: Splenic flexure (junction of SMA and IMA).
  2. **Sudeck's Point**: Rectosigmoid junction (junction of IMA and hypogastric/internal iliac).
- **Presentation**: Crampy lower left quadrant abdominal pain followed within 24 hours by mild hematochezia.
- **Imaging & Colonoscopy**: Plain radiographs / CT show **"thumbprinting"** (submucosal hemorrhage and edema). Colonoscopy shows segmental pale, edematous mucosa with petechial hemorrhages.

### Angiodysplasia of the GI Tract
- Tortuous, dilated submucosal arteriovenous malformations occurring predominantly in the cecum and ascending colon of elderly patients (>60 years).
- **Heyde Syndrome**: Strong clinical association between **Angiodysplasia and Aortic Stenosis**. High shear stress across the stenotic aortic valve cleaves high-molecular-weight von Willebrand Factor (vWF) multimers (acquired type 2A vWD), predisposing friable angiodysplastic vessels to massive bleeding. Cured by aortic valve replacement!

Related: [[gi-embryology-and-malrotation]], [[differentials/crohns-vs-ulcerative-colitis]]."""
    },
    {
        "slug": "inflammatory-bowel-disease",
        "title": "Inflammatory Bowel Disease (Crohn's Disease vs Ulcerative Colitis)",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Pathology", "Immunology", "HST.121"],
        "summary": "Chronic relapsing intestinal inflammation driven by immune dysregulation, categorized into transmural Crohn's and mucosal-limited Ulcerative Colitis.",
        "content": """### Pathophysiology & Genetics
- **Crohn's Disease (CD)**: Driven by Th1/Th17 response ($IFN-\\gamma$, $IL-17$, $IL-23$). Transmural inflammation with noncaseating granulomas, skip lesions, cobblestone mucosa, creeping fat, and linear fissures. Can affect anywhere from **mouth to anus** (terminal ileum most common).
- **Ulcerative Colitis (UC)**: Driven by Th2-like response ($IL-13$, $IL-5$). Mucosal and submucosal inflammation beginning in the **rectum and extending continuously proximally**. Crypt abscesses with neutrophils.

### Complications
- *Crohn's*: Fistulas (enterocutaneous, enterovesical), strictures, bowel obstruction, malabsorption (Vitamin B12 deficiency in terminal ileum resection), calcium oxalate kidney stones.
- *UC*: Toxic megacolon, massive hemorrhage, colorectal carcinoma, Primary Sclerosing Cholangitis (PSC).

Related: [[differentials/crohns-vs-ulcerative-colitis]], [[lipid-malabsorption-and-celiac]]."""
    },
    {
        "slug": "colorectal-neoplasms-and-polyps",
        "title": "Colorectal Carcinogenesis, Polyps & Hereditary Syndromes",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Oncology", "Genetics", "HST.121"],
        "summary": "The adenoma-to-carcinoma sequence, serrated polyp pathways, Microsatellite Instability (MSI), FAP, Gardner, Turcot, and Lynch syndrome.",
        "content": """### Non-Neoplastic vs Neoplastic Polyps
- **Hyperplastic Polyps**: Non-neoplastic, small (< 5 mm), rectosigmoid. Serrated architecture ("sawtooth") confined to upper third of crypts. No malignant potential.
- **Adenomatous Polyps**: Neoplastic premalignant lesions:
  - *Tubular*: Most common (80%); branching tubules; lower malignant risk.
  - *Villous*: Long, finger-like projections; highest malignant potential (**"Villous is Villainous"**); can cause secretory diarrhea with hypokalemia.
  - *Sessile Serrated Adenoma*: Sawtooth architecture extending to crypt base with lateral crypt dilation ("boot-shaped" crypts); driven by BRAF mutations and CpG Island Methylator Phenotype (CIMP).

### Adenoma-to-Carcinoma Sequence (Chromosomal Instability, 85%)
1. **APC Gene Inactivation (5q21)**: Tumor suppressor loss causes beta-catenin accumulation, translocating to nucleus and driving cell proliferation $\\rightarrow$ Normal epithelium becomes hyperproliferative.
2. **K-RAS Mutation (12p12)**: Proto-oncogene activation (GTPase signaling) allows unregulated growth $\\rightarrow$ Small adenoma enlarges.
3. **Loss of Tumor Suppressors (TP53 on 17p, DCC on 18q)**: Inactivation of p53 halts DNA repair and apoptosis $\\rightarrow$ Progression to invasive carcinoma.

### Microsatellite Instability Pathway (MSI, 15%)
- Caused by germline or epigenetic silencing of **DNA Mismatch Repair (MMR)** genes (*MLH1, MSH2, MSH6, PMS2*).
- Unrepaired replication slippage causes expansion/contraction of tandem nucleotide repeats (microsatellites).

### Hereditary Colorectal Syndromes
- **Familial Adenomatous Polyposis (FAP)**: Autosomal dominant germline mutation in APC gene. 1000s of polyps by age 20; 100% risk of colorectal carcinoma by age 40 without prophylactic proctocolectomy.
  - *Gardner Syndrome*: FAP + Osteomas (mandible/skull) + Desmoid tumors + Congenital hypertrophy of retinal pigment epithelium (CHRPE).
  - *Turcot Syndrome*: FAP or Lynch + CNS tumors (medulloblastoma, glioblastoma).
- **Lynch Syndrome (HNPCC)**: Autosomal dominant MMR gene mutation. Colorectal cancer at young age (<50 years), predominantly right-sided/proximal colon. Associated with extracolonic malignancies: **Endometrial cancer** (most common extracolonic), ovarian, stomach, biliary.

Related: [[differentials/fap-vs-lynch-syndrome]], [[gi-imaging-and-endoscopy]]."""
    },
    {
        "slug": "acute-and-chronic-pancreatitis",
        "title": "Pathophysiology of Acute & Chronic Pancreatitis",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Pathology", "Biochemistry", "HST.121"],
        "summary": "Enzymatic autodigestion of pancreatic parenchyma, systemic SIRS complications, and chronic fibro-inflammatory parenchymal destruction.",
        "content": """### Acute Pancreatitis:
- **Triggers**: Gallstones (40%), Alcohol (35%), Hypertriglyceridemia ($>1000\\text{ mg/dL}$), ERCP, Drugs (azathioprine, thiazides, didanosine).
- **Enzyme Cascades**: Premature intrapancreatic activation of **trypsinogen to trypsin** within acinar cells. Trypsin cleaves proelastase -> vascular necrosis; phospholipase A2 -> coagulation necrosis of fat. Fat necrosis binds calcium (**saponification**), producing hypocalcemia.
- **Complications**: Pancreatic pseudocyst (fibrous granulation tissue without epithelial lining), necrotizing pancreatitis, ARDS, hypocalcemia (poor prognostic indicator in Ranson's criteria).

### Chronic Pancreatitis:
Characterized by irreversible fibrosis, ductal calcifications, endocrine insufficiency (pancreatogenic diabetes), and exocrine insufficiency (steatorrhea, deficiency of fat-soluble vitamins A, D, E, K).

Related: [[lipid-malabsorption-and-celiac]], [[gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "gallstones-and-biliary-tract-disorders",
        "title": "Biliary Secretion, Cholelithiasis & Ascending Cholangitis",
        "system": "Hepatology",
        "tags": ["Hepatology", "Pathology", "Surgery", "HST.121"],
        "summary": "Physicochemical lithogenesis of cholesterol and pigment gallstones, acute cholecystitis, choledocholithiasis, and life-threatening ascending cholangitis.",
        "content": """### Biliary Secretion & Cholesterol Lithogenesis
Bile contains bile acids (67%), phospholipids/lecithin (22%), and cholesterol (4.5%).
- Cholesterol is water-insoluble and kept in solution within mixed micelles and unilamellar vesicles.
- **Cholesterol Gallstones (80%)**: Form when cholesterol supersaturates relative to bile acids and lecithin (elevated lithogenic index). Precipitated by:
  1. Excessive cholesterol secretion (obesity, estrogen therapy / oral contraceptives via increased HMG-CoA reductase).
  2. Diminished bile salt secretion (ileal disease/resection, fibrate therapy via inhibition of 7-alpha-hydroxylase).
  3. Gallbladder hypomotility (pregnancy, rapid weight loss, octreotide, total parenteral nutrition TPN).
- **Pigment Gallstones (20%)**:
  - *Black Stones*: Sterile gallbladder; formed from calcium bilirubinate due to high unconjugated bilirubin in **chronic extravascular hemolysis** (sickle cell disease, hereditary spherocytosis, beta-thalassemia) and cirrhosis. Radio-opaque.
  - *Brown Stones*: Located in bile ducts; associated with **biliary tract infection / parasites** (*Clonorchis sinensis*, *Ascaris lumbricoides*). Bacterial beta-glucuronidases hydrolyze conjugated bilirubin into insoluble unconjugated bilirubin. Soft, radiolucent.

### Clinical Syndromes of Cholelithiasis
1. **Biliary Colic**: Transient impaction of gallstone in the cystic duct. Waxing/waning postprandial RUQ pain radiating to the right shoulder/scapula (phrenic nerve). No peritoneal signs or fever.
2. **Acute Cholecystitis**: Impacted stone in cystic duct with secondary chemical inflammation and bacterial infection (*E. coli, Klebsiella*). Constant RUQ pain, fever, leukocytosis, positive **Murphy sign** (inspiratory arrest on deep RUQ palpation).
3. **Choledocholithiasis**: Stone in the common bile duct. Causes biliary ductal dilation, direct hyperbilirubinemia, elevated alkaline phosphatase, and GGT.
4. **Ascending Cholangitis**: Life-threatening bacterial infection superimposed on biliary tract obstruction.
   - **Charcot Triad**: Fever + RUQ pain + Jaundice.
   - **Reynolds Pentad**: Charcot triad + **Hypotension (Septic shock) + Altered Mental Status**. Requires emergency biliary decompression via ERCP!

Related: [[disorders-of-bilirubin-metabolism]], [[differentials/acute-cholecystitis-vs-ascending-cholangitis]]."""
    },
    {
        "slug": "gi-imaging-and-endoscopy",
        "title": "Diagnostic & Interventional GI Imaging, MRCP & ERCP",
        "system": "Gastroenterology",
        "tags": ["Gastroenterology", "Radiology", "Procedures", "HST.121"],
        "summary": "Principles and indications for upper endoscopy (EGD), colonoscopy, barium esophagram, non-invasive MRCP, and therapeutic ERCP.",
        "content": """### Upper Endoscopy (Esophagogastroduodenoscopy - EGD)
- **Indications**: Dysphagia, dyspepsia with alarm features (>55 years, weight loss, anemia, vomiting), refractory GERD, upper GI bleeding (variceal ligation, heater probe, clip placement).
- Direct mucosal visualization and targeted biopsies for H. pylori, Barrett's esophagus, and malignancies.

### Endoscopic Retrograde Cholangiopancreatography (ERCP) vs MRCP
- **Magnetic Resonance Cholangiopancreatography (MRCP)**:
  - Non-invasive, diagnostic T2-weighted MRI technique exploiting high signal intensity of static fluid in biliary and pancreatic ducts.
  - No ionizing radiation, no iodinated contrast, zero risk of pancreatitis. Purely diagnostic (cannot perform interventions).
- **ERCP**:
  - Combined fluoroscopy and side-viewing duodenoscopy. Cannulates the ampulla of Vater to inject radiopaque contrast into bile and pancreatic ducts.
  - Primarily **therapeutic**: Sphincterotomy, stone extraction using balloon/Dormia basket, biliary stent placement for malignant strictures.
  - **Major Complication**: **Post-ERCP Pancreatitis** in 3-5% of patients (caused by hydrostatic injury, thermal injury from cautery, or contrast toxicity). Prophylaxis includes rectal indomethacin and pancreatic duct stenting.

### Cross-Sectional Imaging
- **CT Enterography**: High-resolution thin-cut CT with negative oral contrast (water/PEG) to distend small bowel. Gold standard for evaluating Crohn's disease transmural strictures, fistulae, and creeping fat.
- **Barium Swallow / Esophagram**: First-line evaluation for dysphagia (detects achalasia bird's beak, Zenker diverticulum, esophageal webs/Schatzki rings).

Related: [[esophageal-disorders-and-motility]], [[gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "viral-hepatitis-and-serology",
        "title": "Viral Hepatitis Pathophysiology & Serological Interpretation",
        "system": "Hepatology",
        "tags": ["Hepatology", "Infectious-Disease", "Microbiology", "HST.121"],
        "summary": "Virology and clinical pathology of Hepatitis A-E viruses, with deep algorithmic interpretation of Hepatitis B serological panels.",
        "content": """### Overview of Hepatotropic Viruses
- **Hepatitis A (HAV)**: Naked positive-sense ssRNA picornavirus. Fecal-oral transmission (contaminated shellfish, travel). Acute, self-limiting; no chronic carrier state. Anti-HAV IgM indicates acute infection; IgG indicates immunity.
- **Hepatitis B (HBV)**: Enveloped partially double-stranded circular DNA hepadnavirus. Carries reverse transcriptase. Parenteral/sexual/perinatal transmission. 90% of neonates progress to chronic hepatitis; only 5% of adults do.
- **Hepatitis C (HCV)**: Enveloped positive-sense ssRNA flavivirus. Lack of 3'-to-5' exonuclease proofreading activity yields hypervariable envelope glycoproteins (E2), preventing immune clearance. 80% progress to chronic hepatitis; major cause of cirrhosis and hepatocellular carcinoma (HCC). Curable with direct-acting antivirals (DAAs: Sofosbuvir, Ledipasvir).
- **Hepatitis D (HDV)**: Defective circular negative-sense ssRNA delta virus. Requires Hepatitis B Surface Antigen (HBsAg) coat to penetrate hepatocytes. Coinfection vs Superinfection (superinfection on chronic HBV causes fulminant hepatitis and accelerated cirrhosis).
- **Hepatitis E (HEV)**: Naked ssRNA hepevirus. Fecal-oral. High mortality rate (~20%) due to fulminant hepatic failure in **pregnant women**!

### Hepatitis B Serology Matrix
| Serological Marker | Meaning |
|---|---|
| **HBsAg** | Active infection (present in both acute and chronic infection). |
| **Anti-HBs** | Neutralizing antibody; indicates **immunity** (from resolved infection or vaccination). |
| **HBcAg** | Core antigen inside nucleocapsid; not detectable in serum. |
| **Anti-HBc IgM** | Marker of **acute infection**; sole positive marker during the **"Window Period"**! |
| **Anti-HBc IgG** | Indicates **past exposure** or chronic infection. Never present in vaccinated individuals! |
| **HBeAg** | Secretory protein indicating active viral replication and **high infectivity**. |
| **Anti-HBe** | Indicates cessation of active viral replication and low infectivity. |

### Differentiating Vaccination vs Natural Immunity
- **Vaccinated Patient**: Isolated **Anti-HBs (+)**; all core antibodies (**Anti-HBc**) are completely **negative**!
- **Resolved Natural Infection**: Both **Anti-HBs (+)** AND **Anti-HBc IgG (+)**.

Related: [[exam_traps/hepatitis-b-serology-traps]], [[pathophysiology-of-cirrhosis]]."""
    },
    {
        "slug": "disorders-of-bilirubin-metabolism",
        "title": "Disorders of Bilirubin Metabolism & Jaundice",
        "system": "Hepatology",
        "tags": ["Hepatology", "Biochemistry", "Pathology", "HST.121"],
        "summary": "Metabolic defects in bilirubin conjugation and excretion producing unconjugated or conjugated hyperbilirubinemia.",
        "content": """### Bilirubin Metabolism Pathway
1. Heme breakdown produces water-insoluble **unconjugated (indirect) bilirubin**, transported bound to albumin.
2. Hepatic uptake and conjugation by **UDP-glucuronosyltransferase (UGT1A1)** yielding water-soluble **conjugated (direct) bilirubin**.
3. Excretion via canalicular multidrug resistance protein 2 (**MRP2**).

### Key Clinical Syndromes
- **Gilbert Syndrome**: Mild decrease (~30% of normal) in UGT1A1 activity. Mild unconjugated hyperbilirubinemia provoked by fasting, stress, illness, or exertion. Completely benign, normal liver histology.
- **Crigler-Najjar Syndrome**:
  - *Type I*: Complete absence of UGT1A1. Fatal in infancy due to kernicterus unless liver transplanted.
  - *Type II*: Marked deficiency (~10% normal). Responds to phenobarbital (induces enzyme synthesis).
- **Dubin-Johnson Syndrome**: Defective biliary excretion of conjugated bilirubin (mutation in MRP2 / ABCC2). Characterized by direct hyperbilirubinemia and a grossly **black liver** due to epinephrine metabolite deposition.

Related: [[pathophysiology-of-cirrhosis]], [[gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "metabolic-liver-diseases",
        "title": "Metabolic Liver Diseases: Hemochromatosis, Wilson's & A1AT Deficiency",
        "system": "Hepatology",
        "tags": ["Hepatology", "Genetics", "Metabolic", "HST.121"],
        "summary": "Inborn errors of metabolism affecting the liver: HFE iron overload, ATP7B copper toxicity, and SERPINA1 misfolded protein accumulation.",
        "content": """### Hereditary Hemochromatosis
- **Genetics**: Autosomal recessive mutation in **HFE gene** (chromosome 6p; classically C282Y > H63D). Loss of HFE function fails to sense iron stores, resulting in abnormally low **hepcidin** production by hepatocytes.
- **Pathophysiology**: Unregulated ferroportin activity causes unrestricted intestinal iron absorption ($1\\text{-}2\\text{ g/year}$ vs $1\\text{ mg/day}$ normal). Total body iron accumulates (up to 50 g).
- **Clinical Pentad ("Bronze Diabetes")**:
  1. Micronodular Cirrhosis and elevated HCC risk (200x increase).
  2. "Bronze" skin hyperpigmentation (melanin + iron deposition).
  3. Diabetes mellitus (pancreatic islet beta cell destruction).
  4. Dilated or restrictive cardiomyopathy / arrhythmias.
  5. Arthropathy (calcium pyrophosphate dihydrate / pseudogout in 2nd and 3rd MCP joints) and hypogonadism.
- **Labs & Treatment**: Elevated transferrin saturation (>45%), ferritin > 1000 ng/mL. Prussian blue iron stain reveals blue hemosiderin deposits in hepatocytes. First-line therapy: therapeutic phlebotomy.

### Wilson Disease (Hepatolenticular Degeneration)
- **Genetics**: Autosomal recessive mutation in **ATP7B gene** (chromosome 13), encoding a copper-transporting P-type ATPase.
- **Pathophysiology**: Impairs biliary excretion of copper and prevents copper incorporation into apoceruloplasmin. Free toxic copper leaks into circulation and deposits in tissues.
- **Clinical Presentation**:
  - *Hepatic*: Acute liver failure, chronic hepatitis, cirrhosis.
  - *Neurological/Psychiatric*: Basal ganglia atrophy (putamen necrosis), parkinsonian tremor, ataxia, choreoathetosis, dysarthria, personality changes.
  - *Ophthalmologic*: **Kayser-Fleischer rings** (copper deposition in Descemet's membrane of the cornea; detected by slit-lamp examination).
- **Diagnostics & Treatment**: **Low serum ceruloplasmin** (< 20 mg/dL), elevated 24-hour urinary copper excretion. Treatment: copper chelation with D-penicillamine or Trientine; oral zinc (competes for intestinal copper absorption).

### Alpha-1 Antitrypsin (A1AT) Deficiency
- **Genetics**: Autosomal co-dominant mutation in *SERPINA1* gene. Normal allele is PiM; severe mutant allele is **PiZ** (PiZZ homozygote).
- **Pathophysiology**: Z-variant A1AT undergoes abnormal folding and polymerizes within the endoplasmic reticulum of hepatocytes.
- **Histology**: Intra-hepatocytic round, eosinophilic cytoplasmic globules that stain intensely with **Periodic acid-Schiff (PAS) and resist diastase digestion**!
- **Clinical Dual Pathology**:
  1. *Liver*: Misfolded protein retention causes neonatal cholestasis, cirrhosis, and HCC.
  2. *Lungs*: Lack of circulating A1AT (serine protease inhibitor) leaves neutrophil elastase unopposed, destroying alveolar elastin $\\rightarrow$ **Panacinar Emphysema** (predominantly in lower lung lobes; exacerbated by smoking).

Related: [[pathophysiology-of-cirrhosis]], [[disorders-of-bilirubin-metabolism]]."""
    },
    {
        "slug": "hepatic-immunology-and-transplantation",
        "title": "Hepatic Immunology, Kupffer Cells & Liver Transplantation",
        "system": "Hepatology",
        "tags": ["Hepatology", "Immunology", "Surgery", "HST.121"],
        "summary": "Hepatic vascular sinusoids, Kupffer cell scavenger mechanics, liver tolerogenicity, and indications/criteria for orthotopic liver transplantation.",
        "content": """### Sinusoidal Microarchitecture & Hepatic Tolerance
- **Dual Blood Supply**: 75% portal vein (nutrient-rich, low-pressure, carrying gut-derived bacterial endotoxins and microbial antigens); 25% hepatic artery (oxygen-rich).
- **Liver Sinusoidal Endothelial Cells (LSECs)**: Discontinuous, highly fenestrated endothelium without a true basement membrane, allowing free bidirectional solute exchange with hepatocytes across the **Space of Disse**.
- **Kupffer Cells**: Tissue-resident macrophages anchored to sinusoidal walls. Constitute >80% of total body tissue macrophages. Continuous phagocytic clearance of particulate matter, lipopolysaccharide (LPS), and senescent erythrocytes without mounting destructive systemic inflammation (**hepatic immune tolerance**).

### Orthotopic Liver Transplantation (OLT)
- **Indications**: End-stage liver disease / decompensated cirrhosis (MELD score >= 15), Acute liver failure (King's College criteria), Unresectable Hepatocellular Carcinoma (within Milan criteria), refractory pruritus in cholestatic liver diseases.
- **Milan Criteria for HCC Transplantation**:
  - Solitary tumor diameter $\\le 5\\;\\text{cm}$, OR
  - Up to 3 tumors, each $\\le 3\\;\\text{cm}$ in diameter.
  - No gross vascular invasion, and no extrahepatic nodal or distant metastasis.
  - Achieves 5-year post-transplant survival rates >75%.

### Post-Transplant Rejection & Immunosuppression
- **Hyperacute Rejection**: Preformed donor-specific anti-HLA antibodies; immediate thrombosis of hepatic graft.
- **Acute Cellular Rejection**: T-cell mediated (CD4+ and CD8+) attack on portal triads, presenting with fever, RUQ pain, rising bilirubin and ALT/AST. Liver biopsy triad: mixed portal inflammation, bile duct injury (endotheliitis), and subendothelial phlebitis. Responsive to high-dose IV methylprednisolone.
- **Maintenance Regimens**: Calcineurin inhibitors (Tacrolimus/Cyclosporine) + antimetabolite (Mycophenolate Mofetil) + tapered corticosteroids.

Related: [[pathophysiology-of-cirrhosis]], [[chronic-liver-failure-and-meld]]."""
    },
    {
        "slug": "pathophysiology-of-cirrhosis",
        "title": "Pathophysiology of Cirrhosis & Portal Hypertension",
        "system": "Hepatology",
        "tags": ["Hepatology", "Hemodynamics", "Pathophysiology", "HST.121"],
        "summary": "End-stage liver fibrosis with regenerating nodules, portal hypertension, splanchnic vasodilation, and multi-organ decompensation.",
        "content": """### Hemodynamics & Portal Hypertension
Hepatic stellate cell activation (storing Vitamin A -> producing Type I collagen) distorts sinusoidal architecture.
Portal pressure gradient ($HVPG > 5\\text{ mmHg}$; clinically significant $> 10\\text{ mmHg}$) leads to:
1. **Portosystemic Shunts**: Esophageal varices, caput medusae, anorectal varices.
2. **Splanchnic Vasodilation**: Driven by excessive local **Nitric Oxide (NO)** release, causing arterial underfilling.
3. **Neurohormonal Activation**: Massive activation of the **Renin-Angiotensin-Aldosterone System (RAAS)**, Sympathetic Nervous System, and Vasopressin (ADH).
4. **Ascites & Hepatorenal Syndrome (HRS)**: Intense renal vasoconstriction responding to perceived hypovolemia.

### Board Exam Traps & Cross-System Links
> [!IMPORTANT]
> **Cross-System Link with Cardiology & Renal**:
> The splanchnic arterial vasodilation in advanced cirrhosis mirrors the neurohormonal state of severe heart failure. Patients develop marked sodium retention.
> First-line diuretic therapy is **Spironolactone (Aldosterone antagonist) + Furosemide (Loop diuretic)** in a 100:40 mg ratio to prevent hypokalemia!

Related: [[renin-angiotensin-aldosterone-system]], [[loop-diuretics]], [[acute-decompensated-heart-failure]]."""
    },
    {
        "slug": "chronic-liver-failure-and-meld",
        "title": "Decompensated Cirrhosis, MELD Score & Hepatic Encephalopathy",
        "system": "Hepatology",
        "tags": ["Hepatology", "Critical-Care", "Pharmacology", "HST.121"],
        "summary": "Prognostication systems (Child-Pugh, MELD-Na), spontaneous bacterial peritonitis diagnostic criteria, and hepatic encephalopathy management.",
        "content": """### Scoring Systems for End-Stage Liver Disease
1. **Child-Turcotte-Pugh (CTP) Score**:
   - Variables: Total Bilirubin, Serum Albumin, INR, Ascites severity, Encephalopathy grade.
   - Class A (5-6 points, well-compensated), Class B (7-9 points, significant functional compromise), Class C (10-15 points, decompensated, 1-year survival ~45%).
2. **Model for End-Stage Liver Disease (MELD-Na)**:
   - Objective, continuous logarithmic equation using **Serum Bilirubin, Serum Creatinine, INR, and Serum Sodium**.
   - Primary organ allocation instrument for deceased-donor liver transplantation; predicts 90-day pre-transplant mortality.

### Spontaneous Bacterial Peritonitis (SBP)
- Spontaneous infection of ascitic fluid without an intra-abdominal surgically treatable source. Pathogenesis: bacterial translocation from the gut across permeable mucosal barriers into mesenteric lymphatics, followed by bacteremia and ascitic seedling.
- Most common organisms: Aerobic gram-negative rods (*Escherichia coli* 50%, *Klebsiella pneumoniae*) and gram-positive cocci (*Streptococcus pneumoniae*).
- **Diagnostic Gold Standard**: Diagnostic paracentesis demonstrating **Ascitic fluid Absolute Neutrophil Count (ANC) $\\ge 250\\;\\text{cells/mm}^3$** (calculated as $\\text{total WBC} \\times \\%\\text{neutrophils}$).
- **First-Line Therapy**: IV 3rd-generation cephalosporin (Cefotaxime or Ceftriaxone) + IV albumin (reduces incidence of hepatorenal syndrome and mortality).

### Hepatic Encephalopathy
- Reversible neuropsychiatric abnormality caused by accumulation of neurotoxins (predominantly **Ammonia, $NH_3$**) bypassing the dysfunctional liver through portosystemic shunts.
- Ammonia crosses the blood-brain barrier; converted in astrocytes to **glutamine** by glutamine synthetase $\\rightarrow$ astrocyte osmotic swelling and cerebral edema.
- **Clinical Signs**: Reversal of sleep-wake cycle, asterixis ("flapping tremor" on dorsiflexion of hands), confusion, coma.
- **Treatment**:
  - **Lactulose**: Non-absorbable synthetic disaccharide degraded by colonic bacteria into lactic and acetic acids. Acidification of colonic lumen ($H^+$) converts diffusible $NH_3$ to non-absorbable ammonium ($NH_4^+$) ("ammonia trapping"). Also exerts an osmotic cathartic effect.
  - **Rifaximin**: Non-absorbable oral rifamycin antibiotic that eradicates urease-producing gut flora, reducing ammonia production at the source.

Related: [[pathophysiology-of-cirrhosis]], [[hepatic-immunology-and-transplantation]]."""
    }
]

HST121_DIFFERENTIALS = [
    {
        "slug": "crohns-vs-ulcerative-colitis",
        "title": "Crohn's Disease vs Ulcerative Colitis Differential",
        "content": """# Crohn's Disease vs Ulcerative Colitis Comparison

| Feature | Crohn's Disease | Ulcerative Colitis |
|---|---|---|
| **Location** | Any segment of GI tract (mouth to anus); Terminal ileum most common | Confined to colon; Begins in rectum and extends continuously proximally |
| **Gross Morphology** | **Skip lesions**, cobblestone mucosa, strictures, creeping fat | Continuous involvement, pseudopolyps, lead-pipe sign |
| **Depth of Inflammation** | **Transmural** (all bowel layers) | **Mucosal and submucosal** only |
| **Microscopic Hallmark** | **Noncaseating granulomas** (50%), lymphoid aggregates | **Crypt abscesses** with neutrophilic infiltration, no granulomas |
| **Complications** | Strictures, **Fistulas**, malabsorption, perianal disease | **Toxic megacolon**, massive hemorrhage, colorectal cancer |
| **Smoking Effect** | Smoking **worsens** disease | Smoking is paradoxically protective |
| **Serology** | Anti-Saccharomyces cerevisiae (ASCA +) | Perinuclear antineutrophil cytoplasmic antibody (p-ANCA +) |

Related: [[inflammatory-bowel-disease]]."""
    },
    {
        "slug": "unconjugated-vs-conjugated-hyperbilirubinemia",
        "title": "Unconjugated vs Conjugated Jaundice Comparison",
        "content": """# Unconjugated vs Conjugated Hyperbilirubinemia Differential

| Parameter | Unconjugated (Indirect) | Conjugated (Direct) |
|---|---|---|
| **Water Solubility** | Insoluble (lipid soluble; bound to albumin) | Water soluble (freely filtered by kidneys) |
| **Urine Bilirubin** | **Absent** (cannot be filtered into urine) | **Present** (dark tea-colored urine) |
| **Stool Color** | Normal | Pale / clay-colored (if biliary obstruction) |
| **Common Causes** | Hemolysis (sickle cell, G6PD), Gilbert syndrome, Crigler-Najjar | Biliary obstruction (stones, pancreatic cancer), Dubin-Johnson, Viral hepatitis |
| **Risk in Neonates** | **Kernicterus** (crosses blood-brain barrier) | No risk of kernicterus |

Related: [[disorders-of-bilirubin-metabolism]]."""
    },
    {
        "slug": "secretory-vs-osmotic-diarrhea",
        "title": "Secretory vs Osmotic Diarrhea Differential",
        "content": """# Secretory vs Osmotic Diarrhea Differential Diagnosis

| Clinical Feature | Secretory Diarrhea | Osmotic Diarrhea |
|---|---|---|
| **Underlying Mechanism** | Active ion secretion ($Cl^-, HCO_3^-$) or inhibited absorption | Ingestion of poorly absorbed osmotically active solutes |
| **Stool Osmotic Gap** | **Normal (< 50 mOsm/kg)** | **Elevated (> 125 mOsm/kg)** |
| **Response to Fasting** | **Diarrhea persists** (> 1 L/day) | **Diarrhea completely ceases** |
| **Nocturnal Diarrhea** | Common (wakes patient from sleep) | Rare |
| **Stool Volume** | Large (> 1 L/24h) | Moderate (< 1 L/24h) |
| **Classic Etiologies** | *Vibrio cholerae*, ETEC, VIPoma, Carcinoid, Bile salt diarrhea | Lactase deficiency, Celiac disease, Polyethylene glycol, Sorbitol |

Related: [[diarrheal-illness-and-fluid-transport]]."""
    },
    {
        "slug": "gerd-vs-eosinophilic-esophagitis",
        "title": "GERD vs Eosinophilic Esophagitis Differential",
        "content": """# GERD vs Eosinophilic Esophagitis (EoE) Comparison

| Feature | GERD | Eosinophilic Esophagitis (EoE) |
|---|---|---|
| **Pathophysiology** | Transient LES relaxations with acid/pepsin reflux | Allergic / Th2-mediated food antigen immune hypersensitivity |
| **Demographics** | Obese adults, pregnancy, smokers | Young males, history of atopy (asthma, eczema, rhinitis) |
| **Classic Presentation** | Heartburn, regurgitation, water brash | **Solid food dysphagia**, episodic food impaction |
| **Endoscopy** | Normal, erosive distal esophagitis, or Barrett's | Multiple stacked concentric mucosal rings (**"trachealized esophagus"**), linear furrows, white plaques |
| **Histology** | Basal zone hyperplasia, scattered eosinophils (< 15/HPF) | Dense intraepithelial eosinophilia (**> 15 eosinophils/HPF**), eosinophil microabscesses |
| **Response to PPIs** | Resolves symptoms and mucosal lesions | Refractory to standard PPI; responds to topical swallowed steroids (Fluticasone) or dietary elimination |

Related: [[esophageal-disorders-and-motility]]."""
    },
    {
        "slug": "acute-cholecystitis-vs-ascending-cholangitis",
        "title": "Acute Cholecystitis vs Ascending Cholangitis Differential",
        "content": """# Acute Cholecystitis vs Ascending Cholangitis Differential

| Feature | Acute Cholecystitis | Ascending Cholangitis |
|---|---|---|
| **Site of Obstruction** | **Cystic Duct** | **Common Bile Duct (CBD)** |
| **Jaundice** | Absent (or minimal $< 2\\text{ mg/dL}$) | **Prominent direct hyperbilirubinemia** and pruritus |
| **Clinical Signs** | Murphy's sign, localized RUQ tenderness | **Charcot's Triad** (Fever + Jaundice + RUQ pain); **Reynolds' Pentad** (+ Shock + AMS) |
| **Alkaline Phosphatase** | Normal or mildly elevated | **Markedly elevated** (ductal cholestatic pattern) |
| **Ultrasound Findings** | Gallbladder wall thickening ($> 4\\text{ mm}$), pericholecystic fluid, sonographic Murphy's sign | Dilated extrahepatic and intrahepatic biliary ducts |
| **Management** | Urgent laparoscopic cholecystectomy within 24-72 hours | **Emergency ERCP biliary decompression** + broad-spectrum IV antibiotics |

Related: [[gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "fap-vs-lynch-syndrome",
        "title": "FAP vs Lynch Syndrome (HNPCC) Comparison",
        "content": """# Familial Adenomatous Polyposis vs Lynch Syndrome

| Feature | Familial Adenomatous Polyposis (FAP) | Lynch Syndrome (HNPCC) |
|---|---|---|
| **Gene Mutated** | **APC** (chromosome 5q21) | **DNA Mismatch Repair** (*MLH1, MSH2, MSH6, PMS2*) |
| **Carcinogenesis Pathway** | Chromosomal Instability (CIN, Wnt/beta-catenin) | **Microsatellite Instability (MSI)** |
| **Polyp Burden** | **Hundreds to Thousands** of adenomas | Few adenomas; rapid transition from adenoma to carcinoma |
| **Cancer Location** | Diffuse throughout colon, left > right | Predominantly **Right-sided / Proximal Colon** (60-70%) |
| **Penetrance** | 100% colorectal cancer by age 40 | ~80% lifetime colorectal cancer risk |
| **Associated Syndromes** | Gardner (osteomas, desmoids, CHRPE), Turcot (medulloblastoma) | Muir-Torre (sebaceous neoplasms), Turcot (glioblastoma) |
| **Extracolonic Cancer Risk** | Duodenal / periampullary adenocarcinomas | **Endometrial adenocarcinoma (40-60%)**, ovarian, gastric |

Related: [[colorectal-neoplasms-and-polyps]]."""
    }
]

HST121_TRAPS = [
    {
        "slug": "gi-board-traps",
        "title": "High-Yield GI & Hepatology Board Exam Traps",
        "content": """# High-Yield Gastroenterology & Hepatology Board Traps

### 1. Dubin-Johnson vs Rotor Syndrome
- **Trap**: Confusing which hereditary direct hyperbilirubinemia features dark liver pigmentation.
- **Pearl**: Dubin-Johnson has a grossly **dark/black liver** due to impaired excretion of epinephrine metabolites in lysosomes. Rotor syndrome has a completely normal liver.

### 2. Crohn's Disease Oxalate Kidney Stones
- **Trap**: Why do Crohn's patients with terminal ileal resection develop calcium oxalate renal calculi?
- **Pearl**: Unabsorbed fatty acids in the lumen bind free calcium (saponification). Normally, calcium binds oxalate to prevent oxalate absorption. Without free calcium, oxalate is freely absorbed in the colon $\\rightarrow$ **hyperoxaluria** and calcium oxalate stones!

### 3. Spironolactone in Cirrhotic Ascites
- **Trap**: Using loop diuretics alone for cirrhotic ascites.
- **Pearl**: Marked secondary hyperaldosteronism is the primary driver of renal sodium retention in cirrhosis. **Spironolactone** is the cornerstone; loops are only added to maintain potassium balance.

### 4. Celiac Disease vs IgA Deficiency
- **Trap**: False negative anti-tTG IgA serology.
- **Pearl**: Celiac disease is strongly associated with **selective IgA deficiency**. In patients with high suspicion and negative IgA serologies, total serum IgA or anti-tTG **IgG** must be measured!
"""
    },
    {
        "slug": "hepatitis-b-serology-traps",
        "title": "Hepatitis B Serology & Window Period Board Traps",
        "content": """# High-Yield Hepatitis B Serology Traps

### 1. The "Window Period" Trap
- **Trap**: Diagnosing a patient in the acute window phase when both HBsAg and Anti-HBs are negative.
- **Pearl**: Between the clearance of HBsAg and the appearance of neutralizing Anti-HBs, there is a serological gap of several weeks to months. The **ONLY detectable marker of acute HBV infection** during this window is **Anti-HBc IgM**!

### 2. Distinguishing Vaccination from Prior Resolved Infection
- **Trap**: Confusing isolated anti-HBs with past infection.
- **Pearl**: 
  - The HBV vaccine contains recombinant **HBsAg only**. Therefore, a vaccinated individual will possess **Anti-HBs (+)**, but **Anti-HBc will be NEGATIVE**.
  - A patient who contracted native HBV and cleared it will have both **Anti-HBs (+)** and **Anti-HBc IgG (+)**.

### 3. HBeAg vs Anti-HBe
- **Pearl**: Presence of **HBeAg** indicates high levels of active viral replication and extreme infectivity (e.g. 90% vertical transmission risk to newborn). Seroconversion to **Anti-HBe** signals low infectivity and lower viral load.
"""
    },
    {
        "slug": "biliary-and-pancreatic-board-traps",
        "title": "Biliary, Gallstone & Pancreatic Board Exam Traps",
        "content": """# High-Yield Biliary & Pancreatic Traps

### 1. Pancreatic Pseudocyst vs Cystadenoma
- **Trap**: Misinterpreting the wall structure of a post-pancreatitis pseudocyst.
- **Pearl**: A pseudocyst is lined by **granulation and fibrous connective tissue**, with **NO TRUE EPITHELIAL LINING**. In contrast, mucinous cystic neoplasms are lined by mucin-producing columnar epithelium and carry malignant potential!

### 2. Gallstone Ileus & Rigler's Triad
- **Trap**: Looking for small bowel obstruction from adhesions when a gallstone is the culprit.
- **Pearl**: Recurrent cholecystitis produces a fistula between gallbladder and duodenum (cholecystoduodenal fistula). A large stone passes into the bowel and lodges at the narrowest segment: the **ileocecal valve**. Classical radiologic **Rigler's Triad**:
  1. Small bowel obstruction.
  2. Gallstone in the right iliac fossa.
  3. **Pneumobilia** (air in the biliary tree).

### 3. Spontaneous Bacterial Peritonitis (SBP) Diagnostic Threshold
- **Trap**: Waiting for ascitic fluid culture before starting antibiotics.
- **Pearl**: Cultures take 48-72 hours and may be negative in 40% of true cases. Initiation of IV cefotaxime/ceftriaxone must be triggered immediately if ascitic **Absolute Neutrophil Count (ANC) $\\ge 250\\;\\text{cells/mm}^3$**!
"""
    }
]

HST121_FLASHCARDS = [
    {
        "type": "cloze",
        "text": "The microscopic hallmark distinguishing Crohn's disease from Ulcerative Colitis is the presence of {{c1::noncaseating granulomas}} and {{c2::transmural inflammation}}.",
        "pearl": "Ulcerative colitis features crypt abscesses limited to mucosal and submucosal layers.",
        "tags": ["PaideiaGenesis", "HST121", "Gastroenterology", "IBD"],
        "source": "MIT HST.121 Session 7"
    },
    {
        "type": "cloze",
        "text": "In patients with Crohn's disease involving the terminal ileum, calcium oxalate nephrolithiasis occurs because unabsorbed {{c1::fatty acids}} bind luminal {{c2::calcium}}, leaving {{c3::oxalate}} unbound for hyperabsorption.",
        "pearl": "This classic board trap illustrates lipid malabsorption causing enteric hyperoxaluria.",
        "tags": ["PaideiaGenesis", "HST121", "Renal-GI-Crosslink", "Board-Trap"],
        "source": "MIT HST.121 Session 4 & 7"
    },
    {
        "type": "cloze",
        "text": "The hereditary hyperbilirubinemia characterized by defective canalicular excretion (MRP2 mutation) and a grossly {{c1::black/dark liver}} is {{c2::Dubin-Johnson syndrome}}.",
        "pearl": "Rotor syndrome presents similarly with conjugated hyperbilirubinemia, but liver pigmentation is completely normal.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Jaundice"],
        "source": "MIT HST.121 Session 17"
    },
    {
        "type": "cloze",
        "text": "The primary diuretic of choice for cirrhotic ascites is {{c1::spironolactone (aldosterone antagonist)}} because splanchnic arterial vasodilation triggers severe secondary {{c2::hyperaldosteronism}}.",
        "pearl": "Furosemide is added in a 40 mg to 100 mg spironolactone ratio to maintain normokalemia.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Pharmacology"],
        "source": "MIT HST.121 Session 20"
    },
    {
        "type": "cloze",
        "text": "During the serological 'Window Period' of acute Hepatitis B infection, both {{c1::HBsAg}} and {{c2::Anti-HBs}} are negative, and the sole diagnostic marker present is {{c3::Anti-HBc IgM}}.",
        "pearl": "Anti-HBc IgM indicates acute infection, whereas Anti-HBc IgG indicates chronic infection or past exposure.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Serology"],
        "source": "MIT HST.121 Session 15"
    },
    {
        "type": "cloze",
        "text": "Achalasia is characterized by failure of the LES to relax due to loss of {{c1::nitric oxide (NO) and VIP}}-producing neurons in the {{c2::myenteric (Auerbach) plexus}}.",
        "pearl": "Barium esophagram classically demonstrates a smooth tapering bird's beak sign.",
        "tags": ["PaideiaGenesis", "HST121", "Gastroenterology", "Esophagus"],
        "source": "MIT HST.121 Session 2"
    },
    {
        "type": "cloze",
        "text": "In the chromosomal instability pathway of colorectal adenocarcinoma, the initial mutation inactivates the {{c1::APC tumor suppressor gene (5q)}}, followed by activating mutations in {{c2::KRAS}} and loss of {{c3::TP53}}.",
        "pearl": "FAP is caused by a germline mutation in APC, predisposing to thousands of adenomatous polyps.",
        "tags": ["PaideiaGenesis", "HST121", "Oncology", "Pathology"],
        "source": "MIT HST.121 Session 9"
    },
    {
        "type": "cloze",
        "text": "A stool osmotic gap of {{c1::< 50 mOsm/kg}} indicates {{c2::secretory diarrhea}} (which persists during fasting), whereas a gap of {{c3::> 125 mOsm/kg}} indicates {{c4::osmotic diarrhea}}.",
        "pearl": "Secretory diarrhea is seen in cholera and VIPoma; osmotic diarrhea is seen in lactase deficiency and celiac disease.",
        "tags": ["PaideiaGenesis", "HST121", "Physiology", "Diarrhea"],
        "source": "MIT HST.121 Session 6"
    },
    {
        "type": "cloze",
        "text": "Spontaneous bacterial peritonitis (SBP) is diagnosed when ascitic fluid diagnostic paracentesis demonstrates an absolute neutrophil count (ANC) of {{c1::>= 250 cells/mm3}}, treated empirically with IV {{c2::cefotaxime or ceftriaxone}}.",
        "pearl": "E. coli and Klebsiella are the most common translocated pathogens.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Critical-Care"],
        "source": "MIT HST.121 Session 19"
    },
    {
        "type": "cloze",
        "text": "Hereditary hemochromatosis is caused by mutations in the {{c1::HFE gene (C282Y)}}, which downregulates {{c2::hepcidin}} synthesis, leading to unrestrained enterocyte {{c3::ferroportin}} iron absorption.",
        "pearl": "Classical presentation includes micronodular cirrhosis, bronze skin pigmentation, and diabetes mellitus.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Metabolic"],
        "source": "MIT HST.121 Session 18"
    },
    {
        "type": "cloze",
        "text": "Wilson disease is caused by autosomal recessive mutations in {{c1::ATP7B (chromosome 13)}}, resulting in defective copper excretion into bile, low serum {{c2::ceruloplasmin}}, and {{c3::Kayser-Fleischer rings}}.",
        "pearl": "Copper chelation therapy is performed using penicillamine or trientine.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Genetics"],
        "source": "MIT HST.121 Session 18"
    },
    {
        "type": "cloze",
        "text": "Ascending cholangitis presents with Charcot's triad ({{c1::fever}}, {{c2::RUQ pain}}, {{c3::jaundice}}), which escalates to Reynolds' pentad with the addition of {{c4::hypotension/shock}} and {{c5::altered mental status}}.",
        "pearl": "Reynolds' pentad requires emergency biliary drainage via ERCP.",
        "tags": ["PaideiaGenesis", "HST121", "Hepatology", "Biliary"],
        "source": "MIT HST.121 Session 13"
    },
    {
        "type": "cloze",
        "text": "The wall of a pancreatic pseudocyst is lined by {{c1::fibrous and granulation tissue}}, lacking a true {{c2::epithelial lining}}.",
        "pearl": "This distinguishes pseudocysts from true cystic neoplasms like mucinous cystadenomas.",
        "tags": ["PaideiaGenesis", "HST121", "Gastroenterology", "Pancreas"],
        "source": "MIT HST.121 Session 11"
    },
    {
        "type": "cloze",
        "text": "Gallstone ileus occurs when a cholecystoenteric fistula allows a gallstone to obstruct the {{c1::ileocecal valve}}, presenting with the classic triad of small bowel obstruction, gallstone in the right iliac fossa, and {{c2::pneumobilia (air in biliary tree)}}.",
        "pearl": "This radiologic finding is known as Rigler's triad.",
        "tags": ["PaideiaGenesis", "HST121", "Gastroenterology", "Surgery"],
        "source": "MIT HST.121 Session 13"
    }
]

HST121_CURRICULUM_TOPICS = [
    {"name": "Inflammatory Bowel Disease (Crohn's vs UC)", "priority": "CRITICAL"},
    {"name": "Bilirubin Metabolism & Jaundice", "priority": "CRITICAL"},
    {"name": "Cirrhosis & Splanchnic Hemodynamics", "priority": "HIGH"},
    {"name": "Peptic Ulcer Disease & H. Pylori", "priority": "HIGH"},
    {"name": "Acute & Chronic Pancreatitis", "priority": "HIGH"},
    {"name": "Colorectal Carcinogenesis (FAP vs Lynch)", "priority": "HIGH"},
    {"name": "Gallstones & Ascending Cholangitis", "priority": "HIGH"},
    {"name": "Metabolic Liver Diseases (Hemochromatosis, Wilson, A1AT)", "priority": "HIGH"},
    {"name": "Viral Hepatitis & Serology Interpretation", "priority": "HIGH"},
    {"name": "Esophageal Motility & Barrett's Adenocarcinoma", "priority": "MEDIUM"},
    {"name": "Diarrheal Illness & Fluid Secretion", "priority": "MEDIUM"},
    {"name": "GI Embryology & Malrotation", "priority": "MEDIUM"}
]
