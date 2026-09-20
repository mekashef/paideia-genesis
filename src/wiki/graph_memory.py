"""HippoRAG-inspired Associative Memory & Spreading Activation for the Medical Wiki.
Implements Hippocampal Indexing Theory using Personalized PageRank (PPR) over the knowledge graph.
"""
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Optional
from src.config import WIKI_DIR
from src.wiki.indexer import WikiIndexer, parse_markdown_file
from src.tutor.student_profile import StudentProfile

class AssociativeGraphMemory:
    def __init__(self, wiki_dir: Path = WIKI_DIR):
        self.wiki_dir = wiki_dir
        self.indexer = WikiIndexer(wiki_dir)
        self.student_profile = StudentProfile(wiki_dir / "student_profile")

    def build_graph(self) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, Any]]]:
        """Builds directed adjacency list and node metadata map from the markdown wiki."""
        adj: Dict[str, List[str]] = {}
        nodes_meta: Dict[str, Dict[str, Any]] = {}

        for md_file in self.wiki_dir.rglob("*.md"):
            # Strictly exclude root administrative files and student profile
            if md_file.name in ["SCHEMA.md", "log.md", "index.md", "test-edit.md"] or md_file.parent.name == "student_profile":
                continue
            slug = md_file.stem
            rel_path = str(md_file.relative_to(self.wiki_dir))
            category = md_file.parent.name if md_file.parent != self.wiki_dir else "root"
            
            parsed = parse_markdown_file(md_file)
            sys_tag = parsed.get("system") or ""
            src_tag = parsed.get("source") or ""
            raw_tags = parsed.get("tags") or ""
            title = parsed["title"]
            title_lower = title.lower()
            stem_lower = slug.lower()

            # Determine clinical organ system
            system = "Gastroenterology"
            if any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["liver", "hepat", "cirrho", "meld", "bilirubin", "jaundice", "hepcidin", "wilson", "ugt1a1", "mrp2", "atp7b"]):
                system = "Hepatology"
            elif any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["pancrea", "biliary", "chole", "gallstone", "cholang", "ca-19-9", "trypsin"]):
                system = "Pancreaticobiliary"
            elif any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["gastric", "peptic", "pylori", "esophag", "gerd", "omeprazole", "bismuth", "motility", "achalasia", "barrett"]):
                system = "Gastroduodenal"
            elif any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["bowel", "diarrhea", "ibd", "crohn", "colitis", "celiac", "malabsorption", "polyps", "cftr", "cholera", "lipid", "galt", "colon", "rectal"]):
                system = "Luminal GI"
            elif any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["heart", "cardio", "adhf", "carvedilol"]):
                system = "Cardiology"
            elif any(k in stem_lower or k in title_lower or k in raw_tags.lower() for k in ["diuretic", "renal", "furosemide", "sulfa"]):
                system = "Renal"
            elif stem_lower in ["spironolactone"]:
                system = "Cardio-Hepatic"

            # Determine course curriculum association
            is_hst = (
                "hst.121" in src_tag.lower()
                or "hst.121" in raw_tags.lower()
                or category == "course_sessions"
                or system in ["Hepatology", "Pancreaticobiliary", "Gastroduodenal", "Luminal GI", "Gastroenterology", "Cardio-Hepatic"]
            )
            is_cardio = (
                "cardio" in raw_tags.lower()
                or "renal" in raw_tags.lower()
                or system in ["Cardiology", "Renal", "Cardio-Hepatic"]
                or "cardio" in title_lower
            )

            course = "HST.121" if is_hst and not is_cardio else ("Cardiopulmonary" if is_cardio and not is_hst else ("Both" if is_hst and is_cardio else "Core"))

            # Determine fine-grained entity type
            entity_type = category
            if category == "entities":
                if any(k in stem_lower for k in ["omeprazole", "spironolactone", "octreotide", "lactulose", "rifaximin", "infliximab", "azathioprine", "mesalamine", "d-penicillamine", "bismuth", "sofosbuvir", "cholestyramine", "furosemide", "carvedilol"]):
                    entity_type = "drug"
                elif any(k in stem_lower for k in ["pylori", "cholerae", "virus", "whipplei"]):
                    entity_type = "pathogen"
                elif any(k in stem_lower for k in ["transporter", "cftr", "asbt", "mrp2", "ugt1a1", "trypsin", "atp7b", "hepcidin"]):
                    entity_type = "transporter"
                else:
                    entity_type = "biomarker"

            nodes_meta[slug] = {
                "slug": slug,
                "title": title,
                "category": category,
                "entity_type": entity_type,
                "system": system,
                "course": course,
                "rel_path": rel_path,
                "tags": parsed["tags"]
            }
            adj.setdefault(slug, [])

            for target, _ in parsed["links"]:
                target_slug = Path(target).stem
                # Exclude links to administrative index/schema/logs
                if target_slug in ["index", "SCHEMA", "log", "test-edit"]:
                    continue
                adj[slug].append(target_slug)
                if target_slug not in adj:
                    adj[target_slug] = []

        return adj, nodes_meta

    def spreading_activation(self, seed_slugs: List[str], alpha: float = 0.85, max_iter: int = 25) -> Dict[str, float]:
        """Executes Personalized PageRank (PPR) starting from seed_slugs.
        Mimics hippocampal indexing: activation flows along multi-hop associative pathways.
        """
        adj, nodes_meta = self.build_graph()
        all_nodes = list(adj.keys())
        n = len(all_nodes)
        if n == 0:
            return {}

        # Filter valid seed slugs
        valid_seeds = [s for s in seed_slugs if s in adj]
        if not valid_seeds:
            # Fallback to all nodes uniformly
            teleport = {node: 1.0 / n for node in all_nodes}
        else:
            seed_weight = 1.0 / len(valid_seeds)
            teleport = {node: (seed_weight if node in valid_seeds else 0.0) for node in all_nodes}

        # Initialize rank scores with teleport distribution
        rank = dict(teleport)

        for _ in range(max_iter):
            next_rank = {node: (1.0 - alpha) * teleport[node] for node in all_nodes}
            
            for node, out_links in adj.items():
                if not out_links:
                    # Dangling node distribution
                    for target in all_nodes:
                        next_rank[target] += alpha * (rank[node] / n)
                else:
                    share = (alpha * rank[node]) / len(out_links)
                    for target in out_links:
                        if target in next_rank:
                            next_rank[target] += share

            rank = next_rank

        return rank

    def get_associative_context(self, seed_slugs: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """Returns the top associatively activated concepts for a set of seed terms."""
        ranks = self.spreading_activation(seed_slugs)
        adj, nodes_meta = self.build_graph()

        # Sort nodes by activation score, excluding seed slugs themselves if multiple exist
        sorted_nodes = sorted(ranks.items(), key=lambda x: x[1], reverse=True)
        results = []
        for slug, score in sorted_nodes:
            if slug in seed_slugs and len(sorted_nodes) > len(seed_slugs):
                continue
            meta = nodes_meta.get(slug, {"slug": slug, "title": slug.title(), "category": "concepts"})
            results.append({
                "slug": slug,
                "title": meta.get("title", slug),
                "category": meta.get("category", "concepts"),
                "rel_path": meta.get("rel_path", f"concepts/{slug}.md"),
                "activation_score": round(score, 4)
            })
            if len(results) >= top_k:
                break

        return results

    def get_brain_graph(self, course: Optional[str] = None, layer: Optional[str] = None) -> Dict[str, Any]:
        """Returns nodes and links enriched with student mastery, organ-system clustering, and layer filtering."""
        adj, nodes_meta = self.build_graph()
        mastery = self.student_profile.get_mastery()

        course_filter = (course or "all").lower().strip()
        layer_filter = (layer or "all").lower().strip()

        filtered_slugs = set()
        for slug, meta in nodes_meta.items():
            cat = meta.get("category", "concepts")
            c = meta.get("course", "HST.121")

            # Course filtering
            if course_filter in ["hst121", "hst-121", "gastroenterology"] and c not in ["HST.121", "Both"]:
                continue
            if course_filter in ["cardio", "cardiopulmonary", "renal"] and c not in ["Cardiopulmonary", "Both"]:
                continue

            # Layer filtering: "mechanisms" hides lecture sessions, "lectures" shows lectures + direct concepts
            if layer_filter in ["mechanisms", "pathophysiology"] and cat == "course_sessions":
                continue
            if layer_filter in ["lectures", "curriculum"] and cat not in ["course_sessions", "concepts"]:
                continue

            filtered_slugs.add(slug)

        nodes = []
        for slug in filtered_slugs:
            meta = nodes_meta[slug]
            category = meta.get("category", "concepts")
            system = meta.get("system", "Gastroenterology")
            
            # Default mastery inference based on category and organ system
            node_mastery = 65.0
            for sys_name, score in mastery.items():
                if sys_name.lower() in meta.get("title", "").lower() or sys_name.lower() in meta.get("tags", "").lower():
                    node_mastery = score
                    break

            if category == "exam_traps":
                node_mastery = 35.0  # Traps are flagged as urgent review

            # Calculate degree within the active filtered subnetwork
            degree = sum(1 for target in adj.get(slug, []) if target in filtered_slugs and target != slug)
            degree += sum(1 for src, targets in adj.items() if src in filtered_slugs and src != slug and slug in targets)

            nodes.append({
                "id": slug,
                "title": meta.get("title", slug),
                "category": category,
                "entity_type": meta.get("entity_type", category),
                "system": system,
                "course": meta.get("course", "HST.121"),
                "path": meta.get("rel_path", ""),
                "mastery": node_mastery,
                "degree": degree
            })

        links = []
        seen_edges = set()
        for source in filtered_slugs:
            for target in adj.get(source, []):
                if target in filtered_slugs and target != source:
                    edge_key = tuple(sorted([source, target]))
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        
                        src_meta = nodes_meta[source]
                        tgt_meta = nodes_meta[target]
                        if src_meta.get("system") == tgt_meta.get("system"):
                            edge_type = "intra_system"
                        elif src_meta.get("category") == "course_sessions" or tgt_meta.get("category") == "course_sessions":
                            edge_type = "lecture_curriculum"
                        else:
                            edge_type = "cross_system_bridge"

                        links.append({
                            "source": source,
                            "target": target,
                            "type": edge_type
                        })

        return {"nodes": nodes, "links": links}
