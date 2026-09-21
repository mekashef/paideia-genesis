"""HippoRAG-inspired Associative Memory & Spreading Activation for the Universal Wiki.
Implements Hippocampal Indexing Theory using Personalized PageRank (PPR) over the knowledge graph.
Supports any discipline: Computer Science, Engineering, Research, Sciences, and Medicine.
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
            fm = parsed.get("frontmatter", {})
            sys_tag = fm.get("system") or parsed.get("system") or ""
            domain_tag = fm.get("domain") or parsed.get("domain") or ""
            src_tag = fm.get("source") or parsed.get("source") or ""
            crs_tag = fm.get("course") or fm.get("course_code") or ""
            raw_tags = parsed.get("tags") or ""
            title = parsed["title"]
            title_lower = title.lower()
            stem_lower = slug.lower()
            tags_lower = raw_tags.lower()
            src_lower = src_tag.lower()

            # Determine discipline domain and system/field
            if domain_tag:
                domain = domain_tag
            elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["raft", "paxos", "lsm", "tlb", "epoll", "mesi", "wal", "btree", "b-tree", "consensus", "distributed", "concurrency", "deadlock", "paging", "cache", "protobuf", "grpc", "etcd", "rocksdb"]):
                domain = "Computer Science"
            elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["liver", "hepat", "cirrho", "heart", "cardio", "gi", "bowel", "diarrhea", "pancrea", "biliary", "chole", "gastric", "peptic", "renal", "diuretic"]):
                domain = "Medicine"
            else:
                domain = "General"

            # Determine field / system within domain
            if sys_tag:
                system = sys_tag
            elif domain == "Computer Science":
                if any(k in stem_lower or k in title_lower or k in tags_lower for k in ["raft", "paxos", "consensus", "etcd", "distributed", "cap", "pacelc"]):
                    system = "Distributed Systems"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["lsm", "btree", "b-tree", "wal", "storage", "rocksdb", "database", "2pl", "occ"]):
                    system = "Storage & Databases"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["mesi", "cache", "tlb", "virtual-memory", "paging", "mmu", "hardware", "cpu"]):
                    system = "Computer Architecture"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["epoll", "socket", "network", "tcp", "udp", "rpc", "grpc"]):
                    system = "Systems Programming & Networks"
                else:
                    system = "Systems Engineering"
            elif domain == "Medicine":
                if any(k in stem_lower or k in title_lower or k in tags_lower for k in ["liver", "hepat", "cirrho", "meld", "bilirubin", "jaundice", "hepcidin", "wilson", "ugt1a1", "mrp2", "atp7b"]):
                    system = "Hepatology"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["pancrea", "biliary", "chole", "gallstone", "cholang", "ca-19-9", "trypsin"]):
                    system = "Pancreaticobiliary"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["gastric", "peptic", "pylori", "esophag", "gerd", "omeprazole", "bismuth", "motility", "achalasia", "barrett"]):
                    system = "Gastroduodenal"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["bowel", "diarrhea", "ibd", "crohn", "colitis", "celiac", "malabsorption", "polyps", "cftr", "cholera", "lipid", "galt", "colon", "rectal"]):
                    system = "Luminal GI"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["heart", "cardio", "adhf", "carvedilol"]):
                    system = "Cardiology"
                elif any(k in stem_lower or k in title_lower or k in tags_lower for k in ["diuretic", "renal", "furosemide", "sulfa"]):
                    system = "Renal"
                elif stem_lower in ["spironolactone"]:
                    system = "Cardio-Hepatic"
                else:
                    system = "Gastroenterology"
            else:
                system = "General Science"

            # Determine course curriculum association
            if crs_tag:
                course = crs_tag
            elif any(k in src_lower or k in tags_lower or k in stem_lower for k in ["vision", "3d", "mapanything", "dinov2", "vio", "dust3r", "splat", "drone", "uav"]):
                course = "3D-Vision"
            elif "6.033" in src_lower or "6.004" in src_lower:
                course = "MIT 6.033"
            else:
                is_hst = (
                    "hst.121" in src_lower
                    or "hst.121" in tags_lower
                    or category == "course_sessions"
                    or system in ["Hepatology", "Pancreaticobiliary", "Gastroduodenal", "Luminal GI", "Gastroenterology", "Cardio-Hepatic"]
                )
                is_cardio = (
                    "cardio" in tags_lower
                    or "renal" in tags_lower
                    or system in ["Cardiology", "Renal", "Cardio-Hepatic"]
                    or "cardio" in title_lower
                )
                course = "HST.121" if is_hst and not is_cardio else ("Cardiopulmonary" if is_cardio and not is_hst else ("Both" if is_hst and is_cardio else "Core"))

            # Determine fine-grained entity type
            raw_cat = (fm.get("category") or "").strip().lower()
            explicit_type = (fm.get("entity_type") or "").strip().lower()
            entity_type = explicit_type or raw_cat or category
            if category == "entities":
                if explicit_type:
                    entity_type = explicit_type
                elif raw_cat:
                    entity_type = raw_cat
                elif any(k in stem_lower for k in ["foundation-model", "model", "transformer", "backbone", "nerf", "splat", "dust3r", "mapanything", "droid"]):
                    entity_type = "model-architecture"
                elif any(k in stem_lower for k in ["algorithm", "estimator", "vio", "slam", "filter", "consensus", "msckf", "vins", "raft", "paxos", "normal-flow", "uav-flow"]):
                    entity_type = "algorithm"
                elif any(k in stem_lower for k in ["framework", "library", "gtsam", "conceptfusion", "etcd", "rocksdb"]):
                    entity_type = "framework"
                elif any(k in stem_lower for k in ["protocol", "standard", "grpc", "protobuf", "mesi"]):
                    entity_type = "protocol"
                elif any(k in stem_lower for k in ["kernel", "hardware", "epoll", "tlb", "wal"]):
                    entity_type = "hardware-kernel"
                elif domain == "Medicine":
                    if any(k in stem_lower for k in ["omeprazole", "spironolactone", "octreotide", "lactulose", "rifaximin", "infliximab", "azathioprine", "mesalamine", "d-penicillamine", "bismuth", "sofosbuvir", "cholestyramine", "furosemide", "carvedilol"]):
                        entity_type = "drug"
                    elif any(k in stem_lower for k in ["pylori", "cholerae", "virus", "whipplei"]):
                        entity_type = "pathogen"
                    elif any(k in stem_lower for k in ["transporter", "cftr", "asbt", "mrp2", "ugt1a1", "trypsin", "atp7b", "hepcidin"]):
                        entity_type = "transporter"
                    else:
                        entity_type = "biomarker"
                else:
                    entity_type = "component"

            nodes_meta[slug] = {
                "slug": slug,
                "title": title,
                "category": category,
                "entity_type": entity_type,
                "domain": domain,
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

        valid_seeds = [s for s in seed_slugs if s in adj]
        if not valid_seeds:
            teleport = {node: 1.0 / n for node in all_nodes}
        else:
            seed_weight = 1.0 / len(valid_seeds)
            teleport = {node: (seed_weight if node in valid_seeds else 0.0) for node in all_nodes}

        rank = dict(teleport)

        for _ in range(max_iter):
            next_rank = {node: (1.0 - alpha) * teleport[node] for node in all_nodes}
            
            for node, out_links in adj.items():
                if not out_links:
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
                "domain": meta.get("domain", "General"),
                "rel_path": meta.get("rel_path", f"concepts/{slug}.md"),
                "activation_score": round(score, 4)
            })
            if len(results) >= top_k:
                break

        return results

    def get_brain_graph(self, course: Optional[str] = None, layer: Optional[str] = None) -> Dict[str, Any]:
        """Returns nodes and links enriched with student mastery, domain clustering, and layer filtering."""
        adj, nodes_meta = self.build_graph()
        mastery = self.student_profile.get_mastery()

        course_filter = (course or "all").lower().strip()
        layer_filter = (layer or "all").lower().strip()

        filtered_slugs = set()
        for slug, meta in nodes_meta.items():
            cat = meta.get("category", "concepts")
            c = meta.get("course", "Core").lower()
            domain = meta.get("domain", "General").lower()

            # Course filtering
            if course_filter != "all":
                if course_filter in ["vision", "3d-vision", "3d", "robotics", "drone"]:
                    if not ("vision" in c or "3d" in c or "robot" in domain or "uav" in domain):
                        continue
                elif course_filter in ["hst121", "hst-121", "gastroenterology"]:
                    if not ("hst" in c or "gastro" in c or c == "both"):
                        continue
                elif course_filter in ["cardio", "cardiopulmonary", "renal"]:
                    if not ("cardio" in c or "renal" in c or c == "both"):
                        continue
                elif course_filter in ["eecs", "6.033", "6.004", "cs", "computer"]:
                    if not ("6.033" in c or "6.004" in c or "computer" in domain):
                        continue
                elif course_filter not in c and course_filter not in domain:
                    continue

            # Layer filtering
            etype = meta.get("entity_type", "")
            if layer_filter in ["models", "model-architecture"]:
                if etype not in ["model-architecture", "foundation-model"]:
                    continue
            elif layer_filter in ["algorithms", "algorithm"]:
                if etype not in ["algorithm", "estimator"]:
                    continue
            elif layer_filter in ["mechanisms", "concepts", "theories"] and cat != "concepts":
                continue
            elif layer_filter in ["traps", "exam_traps"] and cat != "exam_traps":
                continue
            elif layer_filter in ["lectures", "curriculum", "sessions"] and cat != "course_sessions":
                continue

            filtered_slugs.add(slug)

        nodes = []
        domains_set = set()
        systems_set = set()

        for slug in filtered_slugs:
            meta = nodes_meta[slug]
            category = meta.get("category", "concepts")
            domain = meta.get("domain", "General")
            system = meta.get("system", "General")
            domains_set.add(domain)
            systems_set.add(system)
            
            # Default mastery inference based on category and domain/system
            node_mastery = 65.0
            for topic_name, score in mastery.items():
                if (topic_name.lower() in meta.get("title", "").lower()
                    or topic_name.lower() in meta.get("tags", "").lower()
                    or topic_name.lower() in system.lower()):
                    node_mastery = score
                    break

            if category == "exam_traps":
                node_mastery = 35.0  # Traps are flagged for review

            degree = sum(1 for target in adj.get(slug, []) if target in filtered_slugs and target != slug)
            degree += sum(1 for src, targets in adj.items() if src in filtered_slugs and src != slug and slug in targets)

            nodes.append({
                "id": slug,
                "title": meta.get("title", slug),
                "category": category,
                "entity_type": meta.get("entity_type", category),
                "domain": domain,
                "system": system,
                "course": meta.get("course", "Core"),
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
                        if src_meta.get("domain") != tgt_meta.get("domain"):
                            edge_type = "cross_domain_bridge"
                        elif src_meta.get("system") == tgt_meta.get("system"):
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

        return {
            "nodes": nodes,
            "links": links,
            "domains": sorted(list(domains_set)),
            "systems": sorted(list(systems_set))
        }

    def get_graph_stats(self) -> Dict[str, Any]:
        """Returns structural statistics of the knowledge graph including domain clusters."""
        bg = self.get_brain_graph()
        return {
            "nodes_count": len(bg["nodes"]),
            "edges_count": len(bg["links"]),
            "domain_clusters": bg.get("domains", []),
            "system_clusters": bg.get("systems", [])
        }
