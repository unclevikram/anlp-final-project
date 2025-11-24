import json
import os
import re
import statistics
import zipfile
from collections import defaultdict
from typing import Dict, List, Tuple


AAEC_ZIP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../dataset/ArgumentAnnotatedEssays-2.0/brat-project-final.zip",
    )
)


def parse_ann(content: str) -> Tuple[Dict[str, Dict], List[Tuple[str, str, str]]]:
    components: Dict[str, Dict] = {}
    relations: List[Tuple[str, str, str]] = []  # (type, arg1_id, arg2_id)

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("T"):
            # Example: T1	Claim 10 25	text
            # or: T1	Premise 10 25	text
            try:
                tid, rest = line.split("\t", 1)
                label_span, text = rest.split("\t", 1)
                label = label_span.split()[0]
                components[tid] = {"label": label, "text": text}
            except ValueError:
                continue
        elif line.startswith("R"):
            # Example: R1	Supports Arg1:T2 Arg2:T1
            try:
                _, rest = line.split("\t", 1)
                m = re.match(r"(\w+)\s+Arg1:(T\d+)\s+Arg2:(T\d+)", rest)
                if m:
                    rtype, arg1, arg2 = m.group(1), m.group(2), m.group(3)
                    relations.append((rtype, arg1, arg2))
            except ValueError:
                continue
    return components, relations


def build_graph(components: Dict[str, Dict], relations: List[Tuple[str, str, str]]):
    out_edges: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    in_edges: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for rtype, arg1, arg2 in relations:
        # In BRAT, Supports Arg1:Premise Arg2:Claim (edge from premise -> claim)
        out_edges[arg1].append((rtype, arg2))
        in_edges[arg2].append((rtype, arg1))
    return out_edges, in_edges


def compute_depth_via_incoming_support(
    in_edges: Dict[str, List[Tuple[str, str]]], node: str, visited: set
) -> int:
    # Follow support edges from supporters (premises/sub-premises) into the node
    if node in visited:
        return 0
    visited.add(node)
    max_child = 0
    for rtype, parent in in_edges.get(node, []):
        if rtype.lower().startswith("support"):
            max_child = max(max_child, compute_depth_via_incoming_support(in_edges, parent, visited))
    visited.remove(node)
    return 1 + max_child if max_child > 0 else 1


def essay_metrics(components: Dict[str, Dict], relations: List[Tuple[str, str, str]]) -> Dict:
    out_edges, in_edges = build_graph(components, relations)

    labels = [c["label"].lower() for c in components.values()]
    num_major = sum(1 for l in labels if "major" in l)
    num_claims = sum(1 for l in labels if l == "claim")
    num_premises = sum(1 for l in labels if l == "premise")

    num_supports = sum(1 for r in relations if r[0].lower().startswith("support"))
    num_attacks = sum(1 for r in relations if r[0].lower().startswith("attack"))

    # Breadth: average number of supporters per claim (incoming support edges)
    claim_ids = [tid for tid, c in components.items() if c["label"].lower() == "claim"]
    claim_in_supports = []
    for tid in claim_ids:
        count = sum(1 for rtype, _ in in_edges.get(tid, []) if rtype.lower().startswith("support"))
        claim_in_supports.append(count)
    avg_breadth = statistics.mean(claim_in_supports) if claim_in_supports else 0.0

    # Evidence density: premises per claim
    evidence_density = (num_premises / num_claims) if num_claims > 0 else 0.0

    # Depth: longest chain of supporting links ending at any claim/major claim
    roots = [tid for tid, c in components.items() if c["label"].lower() in {"majorclaim", "major", "claim"}]
    depths = []
    for r in roots:
        depths.append(compute_depth_via_incoming_support(in_edges, r, set()))
    max_depth = max(depths) if depths else 0

    total_edges = max(1, (num_supports + num_attacks))
    attack_ratio = num_attacks / total_edges

    return {
        "major_claims": num_major,
        "claims": num_claims,
        "premises": num_premises,
        "supports": num_supports,
        "attacks": num_attacks,
        "max_depth": max_depth,
        "avg_breadth": avg_breadth,
        "attack_ratio": attack_ratio,
        "evidence_density": evidence_density,
    }


def analyze_aaec(zip_path: str) -> List[Dict]:
    results: List[Dict] = []
    with zipfile.ZipFile(zip_path) as zf:
        ann_files = [p for p in zf.namelist() if p.lower().endswith(".ann")]
        for ann_path in ann_files:
            try:
                content = zf.read(ann_path).decode("utf-8", errors="ignore")
            except KeyError:
                continue
            components, relations = parse_ann(content)
            metrics = essay_metrics(components, relations)
            metrics["essay_id"] = os.path.basename(ann_path)
            results.append(metrics)
    return results


def main():
    os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../analysis_outputs")), exist_ok=True)
    out_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../analysis_outputs/aaec_structural_metrics.json")
    )
    summaries = analyze_aaec(AAEC_ZIP_PATH)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)
    print(f"Wrote {len(summaries)} AAEC essays' metrics to {out_path}")


if __name__ == "__main__":
    main()


