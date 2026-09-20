"""HST.121 Full Course Sessions and Medical Entities Dataset.
Maps all 20 MIT OCW HST.121 lecture sessions and 28 essential GI/Hepatology entities (drugs, enzymes, pathogens, markers).
"""

HST121_SESSIONS_WIKI = [
    {
        "slug": "session-01-overview-of-embryology-and-physiology",
        "session_num": 1,
        "title": "HST.121 Session 1: Overview of GI Embryology & Physiology",
        "instructors": "Dr. Jonathan N. Glickman",
        "summary": "Embryogenesis of the primitive gut tube, foregut/midgut/hindgut vascular supply, 270-degree rotation, abdominal wall closure, and vitelline duct persistence.",
        "content": """### Session Objectives & Scope
- Anatomical partitioning of the primitive gut into Foregut (Celiac trunk), Midgut (SMA), and Hindgut (IMA).
- Morphogenetic mechanics of the 270° counterclockwise midgut rotation around the Superior Mesenteric Artery axis.
- Embryological etiology of midgut volvulus, omphalocele vs gastroschisis, and Meckel diverticulum.

### Lecture Key Takeaways
1. **Midgut Rotation**: Physiological herniation into the umbilical cord occurs in week 6; return to abdomen in week 10. Incomplete rotation leaves Ladd's bands predisposing to midgut volvulus.
2. **True vs False Diverticulum**: Meckel diverticulum is a true diverticulum of all 3 wall layers containing ectopic gastric or pancreatic mucosa.
3. **Abdominal Wall Defect Distinction**: Omphalocele has a peritoneal sac cover and frequent chromosomal anomalies; gastroschisis is bare bowel extrusion usually right of umbilicus.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/gi-embryology-and-malrotation]], [[concepts/intestinal-pathology-and-ischemia]].
- Entities: [[entities/helicobacter-pylori]]."""
    },
    {
        "slug": "session-02-gastroduodenal-pathophysiology-and-disorders",
        "session_num": 2,
        "title": "HST.121 Session 2: Gastroduodenal Pathophysiology & Motility",
        "instructors": "Dr. Helen Shields, Dr. Jonathan N. Glickman",
        "summary": "Gastric secretion physiology, parietal cell acid production, mucosal barrier defenses, H. pylori ulcerogenesis, and Zollinger-Ellison gastrinomas.",
        "content": """### Session Objectives & Scope
- Gastric acid secretion regulation: Histamine (H2/cAMP), Acetylcholine (M3/Ca2+), and Gastrin (CCK-B/Ca2+) stimulating parietal cell H+/K+ ATPase.
- Somatostatin D-cell negative feedback mechanism.
- Pathophysiology of Peptic Ulcer Disease (PUD), distinguishing duodenal vs gastric ulcers.

### Lecture Key Takeaways
1. **H. pylori Mechanism**: Bacterial urease hydrolyzes urea to ammonia, creating an alkaline microenvironment in the gastric mucus layer.
2. **Duodenal vs Gastric Ulcer Meal Pattern**: Duodenal ulcer pain improves with food; gastric ulcer pain worsens with food.
3. **Zollinger-Ellison Syndrome**: Gastrin-secreting neuroendocrine tumor; paradoxical rise in gastrin following intravenous secretin injection.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/peptic-ulcer-disease-and-h-pylori]], [[concepts/esophageal-disorders-and-motility]].
- Entities: [[entities/omeprazole-ppi]], [[entities/bismuth-subsalicylate]], [[entities/helicobacter-pylori]]."""
    },
    {
        "slug": "session-03-mucosal-immunology-of-the-gi-tract",
        "session_num": 3,
        "title": "HST.121 Session 3: Mucosal Immunology of the GI Tract",
        "instructors": "Dr. Richard S. Blumberg",
        "summary": "Architecture of gut-associated lymphoid tissue (GALT), M cell transcytosis, Secretory IgA biology, dendritic cell antigen presentation, and oral tolerance.",
        "content": """### Session Objectives & Scope
- Structure of Peyer's patches in the terminal ileum and follicle-associated epithelium.
- Function of Microfold (M) cells in antigen sampling and trans-epithelial transport.
- Secretory component role in preventing enzymatic cleavage of Secretory IgA (sIgA).
- Homeostatic balance between mucosal tolerance and pathological inflammation.

### Lecture Key Takeaways
1. **sIgA Assembly**: Dimeric IgA with J-chain is produced in lamina propria, bound by pIgR on enterocytes, transcytosed, and released with the secretory component.
2. **Non-Inflammatory Neutralization**: sIgA neutralizes toxins and agglutinates microbes without fixing complement, avoiding tissue damage.
3. **Oral Tolerance**: Dendritic cells presenting dietary antigens in mesenteric lymph nodes drive FoxP3+ regulatory T cell expansion.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/mucosal-immunology-and-galt]], [[concepts/lipid-malabsorption-and-celiac]].
- Entities: [[entities/secretory-iga]], [[entities/anti-ttg-iga]]."""
    },
    {
        "slug": "session-04-lipid-digestion-absorption-and-malabsorption",
        "session_num": 4,
        "title": "HST.121 Session 4: Lipid Digestion, Absorption & Malabsorption",
        "instructors": "Dr. Martin C. Carey",
        "summary": "Enzymatic hydrolysis of triglycerides, colipase mechanics, mixed micellar solubilization, enterocyte uptake, and chylomicron packaging.",
        "content": """### Session Objectives & Scope
- Sequential enzymatic digestion of dietary fats by lingual, gastric, and pancreatic lipases.
- Critical Micellar Concentration (CMC) of conjugated bile acids.
- Role of colipase in anchoring pancreatic lipase to bile-coated lipid droplets.
- Enterocyte fat transport, ApoB-48 packaging, and lymphatic absorption via lacteals.

### Lecture Key Takeaways
1. **Colipase Necessity**: Pancreatic lipase is inhibited by bile salts unless anchored by colipase.
2. **Abetalipoproteinemia**: MTP mutation impairs ApoB-48/ApoB-100 assembly $\\rightarrow$ fat accumulation in enterocytes, acanthocytes, ataxia.
3. **Terminal Ileum ASBT**: Active bile acid reabsorption via ASBT; resection leads to fat malabsorption and cholerrheic diarrhea.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/lipid-digestion-and-biochemistry]], [[concepts/lipid-malabsorption-and-celiac]].
- Entities: [[entities/asbt-bile-acid-transporter]], [[entities/cholestyramine]]."""
    },
    {
        "slug": "session-05-minicases-esophagus-and-gastric-disorders",
        "session_num": 5,
        "title": "HST.121 Session 5: Minicases: Esophagus and Gastric Disorders",
        "instructors": "Faculty",
        "summary": "Clinical cases analyzing achalasia manometry, Barrett's esophagus dysplasia progression, Mallory-Weiss tears, Boerhaave syndrome, and eosinophilic esophagitis.",
        "content": """### Session Objectives & Scope
- Clinical case presentations comparing motor disorders (Achalasia) with reflux injuries (GERD, Barrett's).
- Differentiating partial-thickness mucosal tears from full-thickness catastrophic esophageal rupture.
- Allergic esophagitis (EoE) diagnostic criteria.

### Lecture Key Takeaways
1. **Achalasia Manometry**: Incomplete LES relaxation and aperistalsis due to Auerbach plexus loss.
2. **Boerhaave vs Mallory-Weiss**: Boerhaave is full-thickness transmural perforation (Hamman's crunch, pneumomediastinum); Mallory-Weiss is longitudinal mucosal tear.
3. **Eosinophilic Esophagitis**: Concentric rings ("trachealized esophagus"), >15 eosinophils/HPF, non-responsive to PPI alone.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/esophageal-disorders-and-motility]], [[differentials/gerd-vs-eosinophilic-esophagitis]].
- Entities: [[entities/omeprazole-ppi]]."""
    },
    {
        "slug": "session-06-intestinal-pathophysiology-and-diarrheal-illness",
        "session_num": 6,
        "title": "HST.121 Session 6: Intestinal Pathophysiology & Diarrheal Illness",
        "instructors": "Dr. Wayne I. Lencer",
        "summary": "Mechanisms of intestinal electrolyte transport, CFTR chloride secretion, cholera toxin second-messenger cascades, and osmotic vs secretory diarrhea diagnosis.",
        "content": """### Session Objectives & Scope
- Cellular biology of intestinal fluid absorption (ENaC, SGLT1, NHE3) and secretion (CFTR, basolateral NKCC1).
- Toxin mechanisms: *Vibrio cholerae* (cAMP via Gs-alpha), ETEC (LT/cAMP and ST/cGMP).
- Neuroendocrine tumors causing diarrhea: VIPoma (WDHA syndrome).

### Lecture Key Takeaways
1. **Secretory Diarrhea**: Stool osmotic gap < 50 mOsm/kg; persistent diarrhea during fasting; nocturnal stooling.
2. **Osmotic Diarrhea**: Stool osmotic gap > 125 mOsm/kg; resolves completely when fasting; unabsorbed solutes draw water.
3. **Stool Gap Formula**: $290 - 2 \\times ([Na^+] + [K^+])$.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/diarrheal-illness-and-fluid-transport]], [[differentials/secretory-vs-osmotic-diarrhea]].
- Entities: [[entities/cftr]], [[entities/vibrio-cholerae]], [[entities/octreotide]]."""
    },
    {
        "slug": "session-07-pathology-of-the-intestines-ibd-ischemia-polyps",
        "session_num": 7,
        "title": "HST.121 Session 7: Pathology of the Intestines (IBD, Ischemia, Polyps)",
        "instructors": "Drs. Carolyn C. Compton and Jonathan N. Glickman",
        "summary": "Histopathology of Crohn's disease vs Ulcerative Colitis, mesenteric ischemia, watershed ischemic colitis, and adenomatous polyp classifications.",
        "content": """### Session Objectives & Scope
- Transmural inflammation, fissures, and noncaseating granulomas in Crohn's disease.
- Mucosal crypt architectural distortion, crypt abscesses, and continuous involvement in Ulcerative Colitis.
- Ischemic bowel disease: acute SMA occlusion vs watershed ischemic colitis.

### Lecture Key Takeaways
1. **Pathologic Hallmarks**: Crohn's = skip lesions + transmural granulomas; UC = continuous mucosal crypt abscesses.
2. **Watershed Zones**: Griffiths' point (splenic flexure) and Sudeck's point (rectosigmoid) vulnerable to systemic hypotension.
3. **Adenoma Architecture**: Villous adenomas carry much higher malignant potential than tubular adenomas ("villous is villainous").

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/inflammatory-bowel-disease]], [[concepts/intestinal-pathology-and-ischemia]], [[concepts/colorectal-neoplasms-and-polyps]].
- Entities: [[entities/mesalamine-5asa]], [[entities/infliximab]], [[entities/p-anca]], [[entities/asca]]."""
    },
    {
        "slug": "session-08-clinic-ibd-and-minicases-malabsorption",
        "session_num": 8,
        "title": "HST.121 Session 8: Clinic: IBD & Minicases: Malabsorption",
        "instructors": "Faculty",
        "summary": "Extraintestinal manifestations of IBD, medical pharmacotherapy ladders, and clinical differential diagnosis of malabsorption syndromes.",
        "content": """### Session Objectives & Scope
- Extraintestinal manifestations: Pyoderma gangrenosum, erythema nodosum, uveitis, ankylosing spondylitis, Primary Sclerosing Cholangitis (PSC).
- Celiac disease clinical diagnostics: anti-tTG IgA, duodenal biopsy villous atrophy, dermatitis herpetiformis.
- Rare malabsorptive enteropathies: Whipple disease, Tropical sprue.

### Lecture Key Takeaways
1. **PSC Association**: Strongly associated with Ulcerative Colitis (p-ANCA positive); elevates risk of cholangiocarcinoma.
2. **Celiac Diagnostics**: Anti-tTG IgA is first-line; false negatives occur in selective IgA deficiency.
3. **Whipple Disease**: Gram-positive bacillus *Tropheryma whipplei*, PAS-positive diastase-resistant macrophages, CAN triad (cardiac, arthralgias, neurologic).

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/inflammatory-bowel-disease]], [[concepts/lipid-malabsorption-and-celiac]], [[differentials/crohns-vs-ulcerative-colitis]].
- Entities: [[entities/tissue-transglutaminase-ttg]], [[entities/anti-ttg-iga]], [[entities/tropheryma-whipplei]]."""
    },
    {
        "slug": "session-09-gastrointestinal-neoplasms",
        "session_num": 9,
        "title": "HST.121 Session 9: Gastrointestinal Neoplasms & Carcinogenesis",
        "instructors": "Dr. Jonathan N. Glickman",
        "summary": "Molecular genetics of colorectal carcinoma: the chromosomal instability (CIN) pathway, microsatellite instability (MSI), FAP, and Lynch syndrome.",
        "content": """### Session Objectives & Scope
- The classical multi-hit adenoma-to-carcinoma sequence: APC, KRAS, and TP53.
- DNA mismatch repair deficiency (MSI-high pathway) in sporadic cancers and hereditary Lynch syndrome.
- Syndromic polyposis: FAP, Gardner, Turcot, Peutz-Jeghers.

### Lecture Key Takeaways
1. **CIN Pathway (85%)**: Loss of APC on 5q21 initiates polyps; KRAS drives adenoma enlargement; TP53 loss drives malignant invasion.
2. **Lynch Syndrome**: Germline MMR gene mutation (*MLH1, MSH2*); predominantly proximal/right colon; endometrial cancer is main extracolonic risk.
3. **FAP**: Autosomal dominant APC mutation, thousands of polyps, 100% colorectal cancer penetrance by age 40 without colectomy.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/colorectal-neoplasms-and-polyps]], [[differentials/fap-vs-lynch-syndrome]].
- Entities: [[entities/ca-19-9]], [[entities/alpha-fetoprotein-afp]]."""
    },
    {
        "slug": "session-10-physiological-chemistry-of-gi-lipids",
        "session_num": 10,
        "title": "HST.121 Session 10: Physiological Chemistry of GI Lipids",
        "instructors": "Dr. Martin C. Carey",
        "summary": "Physical chemistry of bile lipids, triangular phase diagrams, mixed micellar versus vesicular cholesterol transport, and thermodynamics of gallstone formation.",
        "content": """### Session Objectives & Scope
- Triangular coordinate phase diagram of Bile Salts, Lecithin (Phospholipids), and Cholesterol.
- Micellar zone versus metastable and supersaturated lithogenic zones.
- Pathophysiological mechanisms of cholesterol nucleation and crystal precipitation.

### Lecture Key Takeaways
1. **Lithogenic Index**: Ratio of cholesterol present to maximal cholesterol solubility; value > 1.0 indicates supersaturated bile.
2. **Nucleating Factors**: Mucus glycoproteins and immunoglobulins in gallbladder bile act as pronucleating agents accelerate crystallization.
3. **Bile Salt Chemistry**: Conjugation with glycine or taurine lowers pKa, ensuring bile salts remain ionized and effective detergents at duodenal pH.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/lipid-digestion-and-biochemistry]], [[concepts/gallstones-and-biliary-tract-disorders]].
- Entities: [[entities/asbt-bile-acid-transporter]], [[entities/cholestyramine]]."""
    },
    {
        "slug": "session-11-physiology-biochemistry-pancreas-pancreatitis",
        "session_num": 11,
        "title": "HST.121 Session 11: Physiology & Biochemistry of Pancreas; Pancreatitis",
        "instructors": "Faculty",
        "summary": "Regulation of exocrine pancreatic secretion, zymogen synthesis, premature trypsinogen activation, fat saponification, and acute vs chronic pancreatitis.",
        "content": """### Session Objectives & Scope
- Hormonal control of pancreatic secretion: Secretin (ductal HCO3- rich fluid) and CCK (acinar digestive enzymes).
- Protective mechanisms preventing autodigestion: SPINK1 inhibitor, low intra-acinar Ca2+, zymogen packaging.
- Autodigestive cascades of acute pancreatitis and structural destruction in chronic pancreatitis.

### Lecture Key Takeaways
1. **Trypsin as Master Trigger**: Premature intra-acinar cleavage of trypsinogen (PRSS1) to trypsin activates proelastase, phospholipase A2, and chymotrypsin.
2. **Fat Saponification**: Lipase-mediated fat necrosis releases free fatty acids that bind ionized calcium $\\rightarrow$ hypocalcemia.
3. **Pseudocyst Pathology**: Walled-off pancreatic collection lined by fibrous granulation tissue without epithelium.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/acute-and-chronic-pancreatitis]], [[exam_traps/biliary-and-pancreatic-board-traps]].
- Entities: [[entities/trypsinogen-trypsin]], [[entities/octreotide]]."""
    },
    {
        "slug": "session-12-pathology-of-pancreas-and-biliary-tract",
        "session_num": 12,
        "title": "HST.121 Session 12: Pathology of Pancreas & Biliary Tract",
        "instructors": "Dr. Jonathan N. Glickman",
        "summary": "Pancreatic ductal adenocarcinoma, CA 19-9, Trousseau syndrome, cystic pancreatic neoplasms, and cholangiocarcinoma.",
        "content": """### Session Objectives & Scope
- Molecular progression of PanIN (Pancreatic Intraepithelial Neoplasia) to invasive adenocarcinoma (KRAS, CDKN2A, TP53, SMAD4).
- Clinical signs of pancreatic head tumors: Courvoisier sign, painless obstructive jaundice, migratory thrombophlebitis (Trousseau syndrome).
- Differential of cystic neoplasms: Serous cystadenoma (benign) vs Mucinous cystic neoplasm (premalignant).

### Lecture Key Takeaways
1. **Biomarker**: CA 19-9 is elevated in pancreatic adenocarcinoma and cholangiocarcinoma.
2. **Courvoisier Law**: Palpable nontender gallbladder in a jaundiced patient strongly indicates malignant biliary obstruction, not gallstones.
3. **Trousseau Sign**: Hypercoagulable migratory superficial thrombophlebitis induced by tumor-derived procoagulants.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/acute-and-chronic-pancreatitis]], [[concepts/gallstones-and-biliary-tract-disorders]].
- Entities: [[entities/ca-19-9]]."""
    },
    {
        "slug": "session-13-biliary-secretion-cholestasis-gallstones",
        "session_num": 13,
        "title": "HST.121 Session 13: Biliary Secretion, Cholestasis & Gallstones",
        "instructors": "Dr. Martin C. Carey",
        "summary": "Mechanisms of bile flow, cholestatic liver injury, cholesterol vs pigment gallstones, acute cholecystitis, and ascending cholangitis.",
        "content": """### Session Objectives & Scope
- Canalicular bile secretion drivers: Bile salt-dependent flow (BSEP/ABCB11) and bile salt-independent flow.
- Pigment gallstone lithogenesis: Black stones (chronic hemolysis) vs Brown stones (biliary tract infection).
- Spectrum of gallstone disease: Biliary colic $\\rightarrow$ Cholecystitis $\\rightarrow$ Choledocholithiasis $\\rightarrow$ Cholangitis.

### Lecture Key Takeaways
1. **Ascending Cholangitis Triad/Pentad**: Charcot triad (fever, RUQ pain, jaundice); Reynolds pentad (+ hypotension, altered mental status). Emergency ERCP drainage required!
2. **Brown Stones**: Bacterial beta-glucuronidase (*E. coli, Clonorchis*) hydrolyzes conjugated bilirubin into insoluble calcium bilirubinate.
3. **Gallstone Ileus**: Fistulization into duodenum; stone lodges at ileocecal valve; Rigler's triad on imaging (SBO, gallstone in RLQ, pneumobilia).

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/gallstones-and-biliary-tract-disorders]], [[differentials/acute-cholecystitis-vs-ascending-cholangitis]].
- Entities: [[entities/asbt-bile-acid-transporter]], [[entities/cholestyramine]]."""
    },
    {
        "slug": "session-14-imaging-of-the-gi-tract-endoscopy",
        "session_num": 14,
        "title": "HST.121 Session 14: Imaging of the GI Tract; Diagnostic & Therapeutic Endoscopy",
        "instructors": "Faculty",
        "summary": "Endoscopic and cross-sectional imaging modalities in gastroenterology, diagnostic non-invasive MRCP versus interventional therapeutic ERCP.",
        "content": """### Session Objectives & Scope
- Diagnostic modalities: Upper endoscopy (EGD), colonoscopy, capsule endoscopy, CT enterography.
- Non-invasive MRCP (T2-weighted MRI) indications for biliary and pancreatic duct visualization.
- Therapeutic ERCP: Sphincterotomy, stone retrieval, stent placement, and prevention of post-ERCP pancreatitis.

### Lecture Key Takeaways
1. **MRCP vs ERCP**: MRCP is purely diagnostic, non-invasive, no pancreatitis risk. ERCP is therapeutic with 3-5% pancreatitis risk.
2. **Variceal Hemostasis**: Endoscopic band ligation is preferred over sclerotherapy for bleeding esophageal varices.
3. **CT Enterography**: Modality of choice for assessing Crohn's disease strictures, fistulae, and mural inflammation.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/gi-imaging-and-endoscopy]], [[concepts/esophageal-disorders-and-motility]].
- Entities: [[entities/octreotide]]."""
    },
    {
        "slug": "session-15-pathology-of-the-liver-hepatitis",
        "session_num": 15,
        "title": "HST.121 Session 15: Pathology of the Liver (Hepatitis, Steatohepatitis)",
        "instructors": "Dr. Jonathan N. Glickman",
        "summary": "Histopathology and serology of viral hepatitis, autoimmune hepatitis, non-alcoholic fatty liver disease (NAFLD/NASH), and alcoholic steatohepatitis.",
        "content": """### Session Objectives & Scope
- Histological features of acute vs chronic hepatitis: Interface hepatitis, bridging necrosis, Councilman/apoptotic bodies.
- Hepatitis B serological window period, active replication markers (HBeAg, HBV DNA), and vaccine differentiation.
- Alcoholic liver disease (Mallory-Denk bodies, neutrophilic infiltration, AST:ALT > 2) vs NAFLD/NASH.

### Lecture Key Takeaways
1. **HBV Window Period**: HBsAg cleared, Anti-HBs not yet risen; Anti-HBc IgM is the sole diagnostic marker.
2. **Vaccine vs Natural Immunity**: Vaccine produces isolated Anti-HBs(+); natural infection produces Anti-HBs(+) AND Anti-HBc IgG(+).
3. **Alcoholic Hepatitis Ratio**: AST > ALT (typically > 2:1) because alcohol causes mitochondrial damage (mitochondrial AST) and pyridoxal-5-phosphate deficiency impairs ALT synthesis.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/viral-hepatitis-and-serology]], [[exam_traps/hepatitis-b-serology-traps]].
- Entities: [[entities/hepatitis-b-virus]], [[entities/hepatitis-c-virus]], [[entities/sofosbuvir]]."""
    },
    {
        "slug": "session-16-immunology-of-the-liver",
        "session_num": 16,
        "title": "HST.121 Session 16: Immunology of the Liver & Sinusoidal Biology",
        "instructors": "Dr. Jack Wands",
        "summary": "Sinusoidal endothelium, Kupffer cell phagocytosis, hepatic antigen presentation, tolerogenic hepatic microenvironment, and graft rejection.",
        "content": """### Session Objectives & Scope
- Unique microvascular structure of liver sinusoids: highly fenestrated LSECs without basement membrane, permitting free access to Space of Disse.
- Kupffer cells: resident intravascular macrophages clearing gut-derived LPS and bacteria.
- Hepatic immune tolerance and mechanisms preventing systemic hyperactivation against dietary/commensal antigens.

### Lecture Key Takeaways
1. **Kupffer Clearance**: Removes >90% of portal venous endotoxin and particulate matter on first pass.
2. **Space of Disse**: Located between endothelial cells and hepatocytes; site of hepatic stellate cells storing Vitamin A and producing collagen when activated.
3. **Allograft Rejection**: Acute cellular rejection triad on biopsy: mixed portal triad infiltrates, bile ductitis (endotheliitis), and subendothelial venulitis.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/hepatic-immunology-and-transplantation]], [[concepts/pathophysiology-of-cirrhosis]].
- Entities: [[entities/alpha-fetoprotein-afp]]."""
    },
    {
        "slug": "session-17-jaundice-bilirubin-metabolism-dili",
        "session_num": 17,
        "title": "HST.121 Session 17: Jaundice, Bilirubin Metabolism & Drug-Induced Liver Disease",
        "instructors": "Dr. Raymond T. Chung",
        "summary": "Heme catabolism, UGT1A1 conjugation, MRP2 excretion, hereditary jaundice syndromes, and drug-induced liver injury (DILI) mechanisms.",
        "content": """### Session Objectives & Scope
- Enzymatic cascade: Heme $\\rightarrow$ Biliverdin $\\rightarrow$ Unconjugated Bilirubin (albumin-bound) $\\rightarrow$ UGT1A1 Conjugation $\\rightarrow$ Direct Bilirubin.
- Hereditary hyperbilirubinemias: Gilbert, Crigler-Najjar (Type I & II), Dubin-Johnson, and Rotor syndrome.
- Acetaminophen (APAP) hepatotoxicity mechanism via NAPQI and glutathione depletion.

### Lecture Key Takeaways
1. **Gilbert Syndrome**: Mild UGT1A1 downregulation (~30% activity); asymptomatic unconjugated hyperbilirubinemia triggered by fasting, stress, or illness.
2. **Dubin-Johnson vs Rotor**: Dubin-Johnson has MRP2 mutation with a black liver on gross inspection; Rotor has normal liver histology.
3. **APAP Toxicity**: Excess APAP saturates glucuronidation/sulfation, shunting to CYP2E1 $\\rightarrow$ toxic NAPQI. N-acetylcysteine (NAC) replenishes glutathione stores.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/disorders-of-bilirubin-metabolism]], [[differentials/unconjugated-vs-conjugated-hyperbilirubinemia]].
- Entities: [[entities/ugt1a1]], [[entities/mrp2-abcc2]]."""
    },
    {
        "slug": "session-18-physiology-and-biochemistry-of-the-liver",
        "session_num": 18,
        "title": "HST.121 Session 18: Physiology & Biochemistry of the Liver; Metabolic Diseases",
        "instructors": "Faculty",
        "summary": "Phase I/II drug biotransformation, urea cycle ammonia detoxification, and inborn errors of metabolism: Hemochromatosis, Wilson's, and A1AT deficiency.",
        "content": """### Session Objectives & Scope
- Hepatic synthetic function: Albumin, coagulation factors (II, VII, IX, X), thrombopoietin, and urea cycle.
- Hemochromatosis: HFE mutations (C282Y), hepcidin downregulation, ferroportin uninhibited, bronze diabetes, cardiomyopathy.
- Wilson Disease: ATP7B mutation, copper excretion failure, Kayser-Fleischer corneal rings, basal ganglia putamen necrosis.
- Alpha-1 Antitrypsin: PiZZ misfolded protein retention in hepatocytes (PAS-positive diastase-resistant globules) and panacinar emphysema.

### Lecture Key Takeaways
1. **Hemochromatosis**: Transferrin saturation > 45%; treated with therapeutic phlebotomy.
2. **Wilson Disease**: Low serum ceruloplasmin; copper chelation with D-penicillamine or trientine.
3. **A1AT Histology**: Periodic acid-Schiff (PAS) positive, diastase-resistant intra-hepatocytic granules.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/metabolic-liver-diseases]], [[concepts/pathophysiology-of-cirrhosis]].
- Entities: [[entities/hepcidin-ferroportin]], [[entities/atp7b]], [[entities/d-penicillamine]]."""
    },
    {
        "slug": "session-19-clinic-chronic-liver-disease-transplantation",
        "session_num": 19,
        "title": "HST.121 Session 19: Clinic: Chronic Liver Disease & Transplantation",
        "instructors": "Faculty",
        "summary": "Decompensated cirrhosis clinical management, Child-Pugh and MELD-Na scoring systems, spontaneous bacterial peritonitis, and hepatic encephalopathy.",
        "content": """### Session Objectives & Scope
- Clinical management of decompensated cirrhosis complications: Ascites, SBP, Hepatic Encephalopathy, Hepatorenal Syndrome.
- Objective prognostication with MELD-Na (Bilirubin, Creatinine, INR, Sodium) for deceased-donor liver allocation.
- Spontaneous Bacterial Peritonitis (SBP) diagnostic criteria and antibiotic therapy.

### Lecture Key Takeaways
1. **SBP Paracentesis Criterion**: Absolute Neutrophil Count (ANC) $\\ge 250\\;\\text{cells/mm}^3$; empiric IV 3rd-generation cephalosporin + IV albumin.
2. **Hepatic Encephalopathy Therapy**: Lactulose acidifies colonic lumen, trapping ammonia as nonabsorbable $NH_4^+$; Rifaximin eradicates ammonia-producing flora.
3. **Transplant Milan Criteria**: Single lesion $\\le 5\\;\\text{cm}$ or up to 3 lesions $\\le 3\\;\\text{cm}$ without vascular invasion.

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/chronic-liver-failure-and-meld]], [[concepts/hepatic-immunology-and-transplantation]].
- Entities: [[entities/lactulose]], [[entities/rifaximin]], [[entities/spironolactone]]."""
    },
    {
        "slug": "session-20-pathophysiological-consequences-of-cirrhosis",
        "session_num": 20,
        "title": "HST.121 Session 20: Pathophysiological Consequences of Cirrhosis & Portal HTN",
        "instructors": "Faculty",
        "summary": "Hemodynamics of portal hypertension, hepatic stellate cell collagen deposition, splanchnic vasodilation, RAAS activation, ascites, and varices.",
        "content": """### Session Objectives & Scope
- Hepatic stellate cell (Ito cell) transdifferentiation into myofibroblasts producing type I/III collagen in Space of Disse.
- Increased intrahepatic vascular resistance and sinusoidal portal pressure gradient (HVPG > 5 mmHg).
- Splanchnic arterial vasodilation mediated by local nitric oxide (NO) causing arterial underfilling and massive neurohormonal activation.

### Lecture Key Takeaways
1. **Neurohormonal Activation**: Mimics severe heart failure—intense activation of RAAS, sympathetic nervous system, and ADH, causing profound sodium and water retention.
2. **Ascites Diuretic Regimen**: Spironolactone (aldosterone antagonist) + Furosemide in a 100:40 mg ratio to counter secondary hyperaldosteronism while maintaining normokalemia.
3. **Portosystemic Shunts**: Left gastric vein to azygos (esophageal varices), paraumbilical to epigastric (caput medusae), superior rectal to middle/inferior rectal (anorectal varices).

### Associated Wiki Concepts & Entities
- Concepts: [[concepts/pathophysiology-of-cirrhosis]], [[concepts/chronic-liver-failure-and-meld]], [[concepts/acute-decompensated-heart-failure]].
- Entities: [[entities/spironolactone]], [[entities/furosemide]], [[entities/octreotide]]."""
    }
]

HST121_ENTITIES_WIKI = [
    {
        "slug": "omeprazole-ppi",
        "title": "Omeprazole (Proton Pump Inhibitor)",
        "category": "entities",
        "summary": "Irreversible inhibitor of the gastric parietal cell H+/K+ ATPase, producing profound suppression of basal and stimulated gastric acid.",
        "content": """### Mechanism of Action
- Prodrug that enters parietal cell canaliculi and undergoes acid-catalyzed conversion to an active sulfenamide.
- Forms a covalent disulfide bond with the **$H^+/K^+$ ATPase** proton pump, irreversibly inactivating it.
- Restores gastric mucosal pH $> 4$, promoting ulcer healing.

### Indications & USMLE Pearls
- **Indications**: GERD, Peptic Ulcer Disease (duodenal and gastric ulcers), Zollinger-Ellison syndrome, H. pylori eradication regimens.
- **Adverse Effects & Traps**:
  - Decreased calcium and magnesium absorption $\\rightarrow$ increased risk of **osteoporotic bone fractures** and hypomagnesemia.
  - Decreased gastric acid barrier $\\rightarrow$ increased susceptibility to ***Clostridioides difficile*** colitis and community-acquired pneumonia.
  - Interacts with **Clopidogrel**: Inhibits CYP2C19, decreasing clopidogrel activation and antiplatelet efficacy.

Related: [[concepts/peptic-ulcer-disease-and-h-pylori]], [[concepts/esophageal-disorders-and-motility]]."""
    },
    {
        "slug": "spironolactone",
        "title": "Spironolactone (Aldosterone Receptor Antagonist)",
        "category": "entities",
        "summary": "Potassium-sparing mineralocorticoid receptor antagonist acting in the late distal tubule and collecting duct, primary diuretic for cirrhotic ascites.",
        "content": """### Mechanism of Action
- Competitively binds intracellular **mineralocorticoid receptors** in the cortical collecting tubule principal cells.
- Inhibits transcription of epithelial sodium channels (ENaC) and basolateral Na+/K+ ATPase pumps, promoting mild natriuresis while preventing potassium and hydrogen secretion.

### Cirrhotic Ascites Regimen
- Splanchnic arterial vasodilation causes profound arterial underfilling, driving massive secondary **hyperaldosteronism**.
- **Cornerstone Therapy**: Spironolactone is first-line; paired with **Furosemide in a 100 mg : 40 mg ratio** to maximize natriuresis while maintaining serum potassium neutrality!
- **Adverse Effects**: Hyperkalemia, metabolic acidosis, anti-androgenic effects (**gynecomastia**, erectile dysfunction, menstrual irregularities; eplerenone is a more selective alternative).

Related: [[concepts/pathophysiology-of-cirrhosis]], [[concepts/acute-decompensated-heart-failure]], [[entities/furosemide]]."""
    },
    {
        "slug": "octreotide",
        "title": "Octreotide (Somatostatin Analog)",
        "category": "entities",
        "summary": "Long-acting somatostatin receptor agonist, potent splanchnic vasoconstrictor used in acute variceal hemorrhage and VIPoma diarrhea.",
        "content": """### Mechanism of Action
- Synthetic 8-amino acid cyclic peptide with prolonged half-life (1.5 hours vs 2 minutes for native somatostatin).
- Binds somatostatin receptors (SSTR2, SSTR5), inhibiting secretion of serotonin, gastrin, VIP, glucagon, secretin, and motilin.
- Directly induces **splanchnic arteriolar vasoconstriction**, reducing portal venous inflow and decreasing variceal pressure.

### Clinical Indications
1. **Acute Esophageal Variceal Hemorrhage**: Administered as an immediate IV bolus and continuous infusion to achieve hemostasis before and during endoscopy.
2. **VIPoma**: Halts massive watery secretory diarrhea by inhibiting tumor VIP secretion.
3. **Carcinoid Syndrome**: Relieves flushing, wheezing, and secretory diarrhea.

Related: [[concepts/pathophysiology-of-cirrhosis]], [[concepts/diarrheal-illness-and-fluid-transport]]."""
    },
    {
        "slug": "lactulose",
        "title": "Lactulose (Non-Absorbable Synthetic Disaccharide)",
        "category": "entities",
        "summary": "Colonic acidifying agent and osmotic cathartic, first-line medical therapy for hepatic encephalopathy.",
        "content": """### Mechanism of Action
- Synthetic disaccharide (galactose + fructose) resistant to small intestinal disaccharidases.
- Reaches colon intact, where bacterial flora ferment it into short-chain fatty acids (lactic acid, acetic acid).
- **Ammonia Trapping**: Acidification of colonic lumen ($H^+$) protonates diffusible, neurotoxic **Ammonia ($NH_3$)** into non-absorbable **Ammonium ($NH_4^+$)**, trapping it in stool for fecal excretion.
- Also exerts an osmotic laxative effect, accelerating transit time and reducing bacterial colonization.

### Clinical Target & Monitoring
- **Dosing Goal**: Titrated to produce **2 to 3 soft bowel movements daily** in patients with hepatic encephalopathy.

Related: [[concepts/chronic-liver-failure-and-meld]], [[concepts/pathophysiology-of-cirrhosis]]."""
    },
    {
        "slug": "rifaximin",
        "title": "Rifaximin (Non-Absorbable Oral Rifamycin)",
        "category": "entities",
        "summary": "Non-systemic oral antibiotic that inhibits bacterial RNA polymerase, used as adjunct therapy for recurrent hepatic encephalopathy.",
        "content": """### Mechanism of Action
- Binds the beta-subunit of bacterial **DNA-dependent RNA polymerase**, inhibiting RNA synthesis in colonic microflora.
- Negligible systemic absorption (<0.4%); acts locally within the intestinal lumen.
- Eradicates urease-producing gut bacteria (*Klebsiella, Proteus, E. coli*), decreasing gut production of ammonia at the source.

### Clinical Indication
- Added to **Lactulose** for secondary prevention of recurrent hepatic encephalopathy in cirrhosis. Also indicated for traveler's diarrhea.

Related: [[concepts/chronic-liver-failure-and-meld]], [[entities/lactulose]]."""
    },
    {
        "slug": "infliximab",
        "title": "Infliximab (Anti-TNF-Alpha Monoclonal Antibody)",
        "category": "entities",
        "summary": "Chimeric IgG1 monoclonal antibody neutralizing soluble and transmembrane TNF-alpha, inducing mucosal healing in Crohn's and Ulcerative Colitis.",
        "content": """### Mechanism of Action
- High-affinity binding to both soluble and membrane-bound **Tumor Necrosis Factor-alpha (TNF-alpha)**, blocking interaction with TNFR1 and TNFR2.
- Induces apoptosis of activated inflammatory T cells and monocytes; promotes rapid mucosal healing in IBD.

### Indications & USMLE Black Box Traps
- **Indications**: Moderate-to-severe Crohn's disease (including fistulizing Crohn's) and Ulcerative Colitis refractory to corticosteroids/5-ASA.
- **Pre-Treatment Screening**: Must perform **PPD or Interferon-Gamma Release Assay (IGRA)** and chest X-ray to rule out **latent Tuberculosis**, as anti-TNF therapy causes breakdown of granulomas, leading to disseminated TB and fungal infections (*Histoplasmosis*).

Related: [[concepts/inflammatory-bowel-disease]], [[differentials/crohns-vs-ulcerative-colitis]]."""
    },
    {
        "slug": "mesalamine-5asa",
        "title": "Mesalamine (5-Aminosalicylic Acid / 5-ASA)",
        "category": "entities",
        "summary": "Topical mucosal anti-inflammatory agent, first-line therapy for induction and maintenance of remission in mild-to-moderate Ulcerative Colitis.",
        "content": """### Mechanism of Action
- Inhibits **cyclooxygenase (COX)** and **5-lipoxygenase (5-LOX)** pathways, diminishing production of inflammatory leukotrienes ($LTB_4$) and prostaglandins.
- Acts as a free radical scavenger and peroxisome proliferator-activated receptor-gamma (PPAR-gamma) agonist in colonic mucosa.

### Formulations & Delivery
- **Oral Preparations**: Delayed-release coatings (Asacol, Pentasa, Lialda) deliver active 5-ASA past the stomach to the distal ileum and colon.
- **Rectal Suppositories/Enemas**: Directly treat proctitis and left-sided ulcerative colitis with minimal systemic absorption.

Related: [[concepts/inflammatory-bowel-disease]], [[differentials/crohns-vs-ulcerative-colitis]]."""
    },
    {
        "slug": "azathioprine-6mp",
        "title": "Azathioprine & 6-Mercaptopurine (Purine Antimetabolites)",
        "category": "entities",
        "summary": "Thiopurine immunosuppressants blocking de novo purine nucleotide synthesis, used for steroid-sparing maintenance in IBD.",
        "content": """### Mechanism of Action & Metabolism
- Azathioprine is a prodrug non-enzymatically cleaved into **6-Mercaptopurine (6-MP)**.
- Converted by HGPRT into **6-Thioguanine nucleotides (6-TGN)**, which incorporate into DNA/RNA and inhibit de novo purine synthesis, arresting leukocyte proliferation.
- Competing metabolic pathways:
  1. **Thiopurine S-methyltransferase (TPMT)** $\\rightarrow$ inactive 6-MMP.
  2. **Xanthine Oxidase (XO)** $\\rightarrow$ inactive 6-thiouric acid.

### Landmark Drug Interaction & Toxicity
- Co-administration with **Allopurinol** (xanthine oxidase inhibitor) massively shunts 6-MP toward toxic 6-TGN metabolites $\\rightarrow$ catastrophic **severe bone marrow suppression / pancytopenia**! Azathioprine dose must be reduced by 75%.
- TPMT genetic testing is mandatory before initiating therapy.

Related: [[concepts/inflammatory-bowel-disease]]."""
    },
    {
        "slug": "d-penicillamine",
        "title": "D-Penicillamine (Copper Chelating Agent)",
        "category": "entities",
        "summary": "Thiol-containing copper and heavy metal chelating agent, primary therapy for Wilson disease.",
        "content": """### Mechanism of Action
- Contains a free sulfhydryl group that forms a stable, soluble ring complex with divalent copper ions ($Cu^{2+}$).
- Mobilizes copper from hepatic and extrahepatic tissue stores, promoting rapid **urinary copper excretion**.

### Adverse Effects & Traps
- **Drug-Induced Lupus**: Formation of anti-histone and ANA antibodies.
- **Nephrotic Syndrome**: Membranous nephropathy due to immune complex deposition in glomeruli.
- **Bone marrow aplasia**: Requires frequent monitoring of CBC and urinalysis.

Related: [[concepts/metabolic-liver-diseases]], [[entities/atp7b]]."""
    },
    {
        "slug": "bismuth-subsalicylate",
        "title": "Bismuth Subsalicylate",
        "category": "entities",
        "summary": "Gastroprotective mucosal coating agent and antimicrobial, core component of quadruple therapy for H. pylori eradication.",
        "content": """### Mechanism of Action
- Coats gastric mucosal base, binds to ulcer craters, and stimulates endogenous mucosal prostaglandin and bicarbonate secretion.
- Possesses direct **antimicrobial activity against *Helicobacter pylori*** by disrupting cell wall architecture and inhibiting urease activity.

### Clinical Pearls
- Key component of **Bismuth Quadruple Therapy**: Bismuth + Metronidazole + Tetracycline + PPI for 14 days.
- Harmless side effect: Reacts with intestinal hydrogen sulfide to produce bismuth sulfide, causing **black/dark stool** and a black tongue (must distinguish from true melena!).

Related: [[concepts/peptic-ulcer-disease-and-h-pylori]], [[entities/helicobacter-pylori]]."""
    },
    {
        "slug": "sofosbuvir",
        "title": "Sofosbuvir (Hepatitis C NS5B Polymerase Inhibitor)",
        "category": "entities",
        "summary": "Uridine nucleotide analog direct-acting antiviral (DAA) that causes RNA chain termination in Hepatitis C virus.",
        "content": """### Mechanism of Action
- Prodrug intracellularly triphosphorylated by cellular kinases into active GS-461203.
- Competes with native UTP for incorporation by the **HCV NS5B RNA-dependent RNA polymerase**, acting as an obligate RNA chain terminator.
- High barrier to resistance; active across all HCV genotypes 1-6.

### Clinical Impact
- Combined with NS5A inhibitors (Ledipasvir, Velpatasvir) in all-oral, interferon-free regimens yielding **Sustained Virologic Response (SVR) > 95-98%**, effectively curing chronic Hepatitis C infection.

Related: [[concepts/viral-hepatitis-and-serology]], [[entities/hepatitis-c-virus]]."""
    },
    {
        "slug": "cholestyramine",
        "title": "Cholestyramine (Bile Acid Sequestrant)",
        "category": "entities",
        "summary": "Non-absorbable anion-exchange resin that binds bile acids in the intestinal lumen, preventing reabsorption.",
        "content": """### Mechanism of Action
- High-molecular-weight quaternary ammonium polymer with chloride counterions.
- Binds negatively charged bile acids in the intestinal lumen, forming an insoluble complex excreted in feces.
- Disrupts enterohepatic circulation, forcing the liver to convert endogenous cholesterol into new bile acids, thereby upregulating LDL receptors and lowering serum LDL.

### GI Indications
- **Choleretic (Bile Acid) Diarrhea**: After ileal resection or in mild Crohn's disease, unabsorbed bile salts spill into the colon, stimulating secretagogue chloride secretion; cholestyramine binds bile acids and cures the secretory diarrhea.
- **Cholestatic Pruritus**: Binds circulating bile salt pruritogens in primary biliary cholangitis.

Related: [[concepts/lipid-digestion-and-biochemistry]], [[concepts/diarrheal-illness-and-fluid-transport]]."""
    },
    {
        "slug": "ugt1a1",
        "title": "UGT1A1 (UDP-Glucuronosyltransferase 1A1)",
        "category": "entities",
        "summary": "Hepatic microsomal enzyme catalyzing glucuronidation of unconjugated bilirubin to water-soluble bilirubin monoglucuronide and diglucuronide.",
        "content": """### Biological Function
- Located in the endoplasmic reticulum of hepatocytes.
- Transfers glucuronic acid from UDP-glucuronic acid to the propionic acid side chains of water-insoluble unconjugated bilirubin, converting it into water-soluble **conjugated (direct) bilirubin**.

### Pathology & Genetic Syndromes
- **Gilbert Syndrome**: TATA box promoter polymorphism ($A(TA)_7TAA$ vs normal $(TA)_6$), reducing transcription by ~70%. Mild, benign unconjugated hyperbilirubinemia under fasting/stress.
- **Crigler-Najjar Type I**: Complete absence of catalytic activity (frameshift or nonsense mutations); kernicterus in infancy; fatal without liver transplantation.
- **Crigler-Najjar Type II**: Point mutation with residual ~10% activity; responds to **Phenobarbital** (which induces UGT1A1 enzyme synthesis).

Related: [[concepts/disorders-of-bilirubin-metabolism]], [[differentials/unconjugated-vs-conjugated-hyperbilirubinemia]]."""
    },
    {
        "slug": "mrp2-abcc2",
        "title": "MRP2 / ABCC2 (Multidrug Resistance-Associated Protein 2)",
        "category": "entities",
        "summary": "ATP-binding cassette export pump on the hepatocyte canalicular membrane responsible for biliary excretion of conjugated bilirubin.",
        "content": """### Biological Function
- Primary active transporter located exclusively on the **apical (canalicular) membrane** of hepatocytes.
- Hydrolyzes ATP to pump conjugated bilirubin diglucuronide, glutathione conjugates, and organic anions against a steep concentration gradient into the bile canaliculus.

### Genetic Deficiency: Dubin-Johnson Syndrome
- Autosomal recessive loss-of-function mutation in the *ABCC2* gene.
- Conjugated bilirubin cannot be excreted into bile and regurgitates back into sinusoidal blood $\\rightarrow$ **Direct (conjugated) hyperbilirubinemia** with urinary bilirubin excretion.
- **Black Liver**: Impaired excretion of epinephrine metabolites that accumulate in hepatocyte lysosomes, giving the liver a characteristic dark black appearance.

Related: [[concepts/disorders-of-bilirubin-metabolism]], [[exam_traps/gi-board-traps]]."""
    },
    {
        "slug": "cftr",
        "title": "CFTR (Cystic Fibrosis Transmembrane Conductance Regulator)",
        "category": "entities",
        "summary": "cAMP-regulated apical chloride and bicarbonate channel in mucosal crypt enterocytes, the molecular engine of secretory diarrhea.",
        "content": """### Cellular Physiology in the Intestine
- Located on the luminal (apical) membrane of crypt enterocytes throughout the small intestine and colon.
- Phosphorylation of regulatory (R) domain by **Protein Kinase A (PKA)** and ATP binding to nucleotide-binding domains opens the pore, driving active $Cl^-$ and $HCO_3^-$ exit into the lumen.
- Sodium and water follow paracellularly, maintaining luminal fluidity.

### Pathological Hyperactivation
- Exploited by *Vibrio cholerae* (via Gs-alpha ADP-ribosylation) and ETEC (heat-labile toxin) to generate massive, uncontrolled intracellular cAMP $\\rightarrow$ continuous open state of CFTR $\\rightarrow$ massive secretagogue rice-water diarrhea (>10-20 L/day).

Related: [[concepts/diarrheal-illness-and-fluid-transport]], [[entities/vibrio-cholerae]]."""
    },
    {
        "slug": "tissue-transglutaminase-ttg",
        "title": "Tissue Transglutaminase (tTG)",
        "category": "entities",
        "summary": "Calcium-dependent cross-linking enzyme that deamidates gliadin peptides in Celiac disease, forming the primary neoepitope driving enteropathy.",
        "content": """### Enzymatic Role in Celiac Pathogenesis
- Calcium-dependent enzyme released from damaged intestinal mucosa and fibroblasts.
- Deamidates uncharged **glutamine residues** in dietary gluten (gliadin) into negatively charged **glutamic acid**.
- Negatively charged deamidated gliadin peptides fit with high affinity into the positively charged binding grooves of **HLA-DQ2 and HLA-DQ8** molecules on antigen-presenting cells.
- Triggers vigorous CD4+ Th1 response ($IFN-\\gamma$, mucosal apoptosis) and autoantibody formation against tTG itself.

### Serological Diagnostic Gold Standard
- **Anti-tTG IgA**: Sensitivity and specificity $>95\\%$ for Celiac disease.

Related: [[concepts/lipid-malabsorption-and-celiac]], [[entities/anti-ttg-iga]]."""
    },
    {
        "slug": "trypsinogen-trypsin",
        "title": "Trypsinogen & Trypsin (PRSS1 / SPINK1)",
        "category": "entities",
        "summary": "Pancreatic endopeptidase zymogen whose premature intracellular activation initiates the autodigestive cascade of acute pancreatitis.",
        "content": """### Normal Physiology
- Synthesized by acinar cells as inactive **trypsinogen (PRSS1)** and packaged with **SPINK1** (serine protease inhibitor Kazal-type 1).
- Secreted into duodenum; cleaved at Lys23-Ile24 by brush-border **Enteropeptidase (Enterokinase)** into active **Trypsin**.
- Trypsin then cleaves all other pancreatic zymogens (chymotrypsinogen, proelastase, prophospholipase A2, procarboxypeptidase).

### Role in Pancreatitis
- Premature intra-acinar activation (triggered by bile reflux, hypercalcemia, or PRSS1 gain-of-function mutation) overwhelms SPINK1 defenses.
- Trypsin activates surrounding proenzymes $\\rightarrow$ vascular necrosis (elastase), fat necrosis (phospholipase A2), and systemic shock.

Related: [[concepts/acute-and-chronic-pancreatitis]], [[exam_traps/biliary-and-pancreatic-board-traps]]."""
    },
    {
        "slug": "asbt-bile-acid-transporter",
        "title": "ASBT (Apical Sodium-Bile Acid Cotransporter / SLC10A2)",
        "category": "entities",
        "summary": "Sodium-dependent cotransporter in the brush border of the terminal ileum, responsible for 95% enterohepatic recycling of bile salts.",
        "content": """### Physiological Mechanism
- Located in the apical microvilli of enterocytes in the **terminal ileum**.
- Couples the uphill transport of conjugated bile acid anions with the downhill influx of two sodium ions ($Na^+$).
- Transports bile acids across enterocytes to basolateral heterodimer OST-alpha/OST-beta for exit into portal venous blood.

### Clinical Pathology
- Resection of the terminal ileum (e.g. for Crohn's disease) removes ASBT $\\rightarrow$ loss of bile acid recycling:
  - If $<100\\;\\text{cm}$ resected: excess bile acids spill into colon causing **choleretic secretory diarrhea** (treated with cholestyramine).
  - If $>100\\;\\text{cm}$ resected: hepatic synthesis cannot keep pace; bile acid pool is exhausted $\\rightarrow$ **severe fat malabsorption and steatorrhea**.

Related: [[concepts/lipid-digestion-and-biochemistry]], [[entities/cholestyramine]]."""
    },
    {
        "slug": "hepcidin-ferroportin",
        "title": "Hepcidin & Ferroportin (Systemic Iron Regulatory Axis)",
        "category": "entities",
        "summary": "Master hormonal regulatory axis governing systemic iron homeostasis, disrupted in hereditary hemochromatosis and anemia of chronic disease.",
        "content": """### Normal Physiological Axis
- **Ferroportin**: The sole cellular iron export channel; located on the basolateral membrane of duodenal enterocytes, macrophages, and hepatocytes.
- **Hepcidin**: 25-amino acid peptide hormone produced by hepatocytes in response to elevated circulating transferrin saturation (sensed via HFE, TFR2, and HJV/SMAD pathways).
- **Mechanism**: Hepcidin binds to ferroportin, causing its internalization and lysosomal degradation. This shuts down duodenal iron absorption and traps iron inside macrophages.

### Pathology in Hereditary Hemochromatosis
- Mutated *HFE* fails to interact with TFR1 $\\rightarrow$ hepatocytes falsely sense low iron stores $\\rightarrow$ **abnormally low hepcidin production**.
- Unchecked ferroportin activity results in continuous, unregulated intestinal iron hyperabsorption (10-20 mg/day) and progressive multi-organ parenchymal iron toxicity.

Related: [[concepts/metabolic-liver-diseases]]."""
    },
    {
        "slug": "atp7b",
        "title": "ATP7B (Copper-Transporting P-Type ATPase)",
        "category": "entities",
        "summary": "Transmembrane copper export pump on chromosome 13, defective in autosomal recessive Wilson disease.",
        "content": """### Biological Function
- Expressed predominantly in hepatocytes in the trans-Golgi network.
- Functions:
  1. Transports copper into the Golgi lumen for incorporation into **apoceruloplasmin** to create mature functional ceruloplasmin.
  2. Under high intracellular copper conditions, traffics to canalicular vesicles to export excess copper into bile for fecal excretion.

### Wilson Disease Pathophysiology
- Loss-of-function mutation on chromosome 13 prevents biliary copper excretion and ceruloplasmin synthesis.
- Copper accumulates in hepatocytes, overflows into plasma as toxic non-ceruloplasmin bound free copper, and deposits in the brain (putamen/basal ganglia), cornea (Kayser-Fleischer rings), kidneys, and joints.

Related: [[concepts/metabolic-liver-diseases]], [[entities/d-penicillamine]]."""
    },
    {
        "slug": "helicobacter-pylori",
        "title": "Helicobacter pylori",
        "category": "entities",
        "summary": "Curved gram-negative microaerophilic bacterium colonizing gastric mucosa, primary cause of gastritis, peptic ulcers, MALT lymphoma, and gastric adenocarcinoma.",
        "content": """### Microbiology & Virulence Factors
- **Flagella**: Allows motile penetration through thick gastric mucus layer.
- **Urease**: Hydrolyzes urea into carbon dioxide and ammonia ($NH_3$), buffering microenvironmental gastric acid and allowing bacterial survival.
- **CagA (Cytotoxin-Associated Gene A)**: Injected into epithelial cells via Type IV secretion system; disrupts tight junctions and cytoskeletal signaling.
- **VacA (Vacuolating Cytotoxin A)**: Induces epithelial vacuolation and apoptosis.

### Disease Associations
- Chronic active antral gastritis (leading to hypergastrinemia and duodenal ulcers in 90%).
- Pangastritis (leading to gastric mucosal atrophy, hypochlorhydria, and gastric ulcers in 70%).
- **Gastric Adenocarcinoma** and **MALT Lymphoma** (extranodal marginal zone B-cell lymphoma; can regress completely with antibiotic eradication!).

Related: [[concepts/peptic-ulcer-disease-and-h-pylori]], [[entities/bismuth-subsalicylate]], [[entities/omeprazole-ppi]]."""
    },
    {
        "slug": "vibrio-cholerae",
        "title": "Vibrio cholerae",
        "category": "entities",
        "summary": "Comma-shaped, oxidase-positive gram-negative bacterium producing cholera toxin, the prototype cause of massive secretory diarrhea.",
        "content": """### Microbiology & Pathogenicity
- Comma-shaped (vibrio), motile with single polar flagellum, grows on TCBS (thiosulfate-citrate-bile salts-sucrose) agar. Acid-sensitive (high infectious dose required unless on PPIs or gastrectomy).
- **Cholera Toxin (AB5 Toxin)**:
  - B-subunit binds ganglioside GM1 on enterocytes.
  - A-subunit undergoes endocytosis and catalyzes the **ADP-ribosylation of $G_{s\\alpha}$** subunit of G-protein.
  - Keeps adenylyl cyclase permanently in the active state $\\rightarrow$ massive rise in intracellular **cAMP** $\\rightarrow$ persistent opening of **CFTR** chloride channels.
- Produces profuse, odorless, non-bloody **"rice-water" stools** with flecks of mucus.

Related: [[concepts/diarrheal-illness-and-fluid-transport]], [[entities/cftr]]."""
    },
    {
        "slug": "hepatitis-b-virus",
        "title": "Hepatitis B Virus (HBV)",
        "category": "entities",
        "summary": "Partially double-stranded circular DNA hepadnavirus encoding reverse transcriptase, cause of acute and chronic hepatitis and hepatocellular carcinoma.",
        "content": """### Virology & Genome Organization
- Enveloped virion containing a partially double-stranded circular DNA genome.
- Replicates via an intermediate RNA pregenome using its own viral **Reverse Transcriptase / DNA Polymerase**.
- Viral Antigens:
  - **HBsAg**: Envelope surface glycoprotein.
  - **HBcAg**: Core nucleocapsid protein.
  - **HBeAg**: Cleaved secretory nucleocapsid protein indicating active viral replication.

### Transmission & Oncogenesis
- Parenteral, sexual, and vertical (perinatal) transmission.
- Perinatal transmission carries a 90% risk of chronicity.
- Unlike HCV, HBV can cause **Hepatocellular Carcinoma (HCC) without preceding cirrhosis** due to integration of viral DNA into host genome, activating proto-oncogenes.

Related: [[concepts/viral-hepatitis-and-serology]], [[exam_traps/hepatitis-b-serology-traps]]."""
    },
    {
        "slug": "hepatitis-c-virus",
        "title": "Hepatitis C Virus (HCV)",
        "category": "entities",
        "summary": "Positive-sense single-stranded RNA flavivirus characterized by genetic hypervariability, high rate of chronicity, and curability via DAAs.",
        "content": """### Virology & Immune Evasion
- Enveloped, positive-sense single-stranded RNA virus belonging to the *Flaviviridae* family.
- Lacks a 3'-to-5' exonuclease proofreading function in its RNA-dependent RNA polymerase.
- Generates rapid mutations in envelope glycoprotein genes (**Hypervariable Region 1 [HVR1] of E2**), producing thousands of circulating quasispecies that evade host neutralizing antibodies.

### Clinical Spectrum
- Acute infection is usually asymptomatic (80%).
- Progression to **chronic hepatitis in 80%**; 20-30% develop cirrhosis over 20-30 years.
- Major risk factor for Hepatocellular Carcinoma.
- Extrahepatic manifestations: **Mixed Cryoglobulinemia** (type II, with palpable purpura and membranoproliferative glomerulonephritis MPGN), Porphyria Cutanea Tarda (PCT).

Related: [[concepts/viral-hepatitis-and-serology]], [[entities/sofosbuvir]]."""
    },
    {
        "slug": "tropheryma-whipplei",
        "title": "Tropheryma whipplei",
        "category": "entities",
        "summary": "Gram-positive actinomycete bacterium causing Whipple disease, characterized by PAS-positive foamy macrophages in the small intestinal lamina propria.",
        "content": """### Microbiology & Pathology
- Fastidious, rod-shaped, gram-positive actinomycete bacterium.
- Infiltrates the small bowel lamina propria, where bacterial cell wall peptidoglycans are phagocytosed by macrophages.
- **Diagnostic Biopsy**: Dense accumulation of foamy macrophages that stain intensely with **Periodic acid-Schiff (PAS) and are diastase-resistant**, but are **Acid-Fast Negative** (distinguishes from *Mycobacterium avium-intracellulare* in HIV patients!).

### Clinical Triad (CAN Mnemonic)
- **C**ardiac symptoms (endocarditis, pericarditis).
- **A**rthralgias / migratory non-deforming polyarthritis (often years before GI symptoms).
- **N**eurologic manifestations (dementia, seizures, oculomasticatory myorhythmia).
- Plus malabsorption, steatorrhea, weight loss, and hyperpigmentation.

Related: [[concepts/lipid-malabsorption-and-celiac]]."""
    },
    {
        "slug": "secretory-iga",
        "title": "Secretory IgA (sIgA)",
        "category": "entities",
        "summary": "Dimeric mucosal immunoglobulin equipped with a J-chain and epithelial secretory component, defending gut mucosal surfaces.",
        "content": """### Structure & Biosynthesis
- Dimeric molecule composed of two IgA monomers linked by a 15-kDa joining (**J**) chain synthesized by plasma cells.
- Binds to the polymeric immunoglobulin receptor (**pIgR**) on enterocyte basolateral surfaces, undergoes vesicular transcytosis, and is cleaved to release the **secretory component**.
- Secretory component shields the immunoglobulin against luminal proteolytic degradation by pepsin, trypsin, and chymotrypsin.

### Biological Function
- Performs **immune exclusion**: Binds and agglutinates bacteria, neutralizes bacterial exotoxins, and blocks viral entry without triggering inflammatory complement activation.

Related: [[concepts/mucosal-immunology-and-galt]]."""
    },
    {
        "slug": "ca-19-9",
        "title": "CA 19-9 (Carbohydrate Antigen 19-9)",
        "category": "entities",
        "summary": "Serum sialylated Lewis(a) blood group antigen biomarker used in pancreatic ductal adenocarcinoma and cholangiocarcinoma.",
        "content": """### Clinical Characteristics
- Sialylated Lewis(a) tetrasaccharide expressed on glycolipids and glycoproteins.
- Note: Individuals lacking the Lewis enzyme (genotype Le(a-b-), ~5-10% of population) cannot synthesize CA 19-9 regardless of tumor burden.

### Diagnostic Role & USMLE Pearls
- Not recommended for general asymptomatic screening due to false positives in benign cholestasis, acute pancreatitis, and cirrhosis.
- Primarily used for **monitoring treatment response and disease recurrence** in pancreatic ductal adenocarcinoma and cholangiocarcinoma.

Related: [[concepts/acute-and-chronic-pancreatitis]], [[concepts/gallstones-and-biliary-tract-disorders]]."""
    },
    {
        "slug": "alpha-fetoprotein-afp",
        "title": "Alpha-Fetoprotein (AFP)",
        "category": "entities",
        "summary": "Major fetal serum protein and oncofetal biomarker utilized in screening for Hepatocellular Carcinoma (HCC) and testicular germ cell tumors.",
        "content": """### Biological Function
- Main serum protein synthesized by the embryonic yolk sac and fetal liver; serves as the fetal equivalent of adult albumin.
- Serum levels decline rapidly after birth to < 10-20 ng/mL in adults.

### Clinical Utility in Hepatology
- Elevated in **Hepatocellular Carcinoma (HCC)**: Serum level > 500 ng/mL in a cirrhotic patient is highly diagnostic of HCC.
- Used in conjunction with **RUQ ultrasound every 6 months** for HCC surveillance in patients with cirrhosis.
- Also elevated in non-seminomatous testicular germ cell tumors (yolk sac tumors) and neural tube defects (in maternal serum).

Related: [[concepts/pathophysiology-of-cirrhosis]], [[concepts/chronic-liver-failure-and-meld]]."""
    }
]
