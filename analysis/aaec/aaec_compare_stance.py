import csv
import json
import os
import statistics
from typing import Dict, List


METRICS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../analysis_outputs/aaec_structural_metrics.json",
    )
)
STANCE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "stance_labels.csv",
    )
)


def load_metrics(path: str) -> Dict[str, Dict]:
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    return {it["essay_id"]: it for it in items}


def load_stances(path: str) -> List[Dict]:
    rows: List[Dict] = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def cohen_d(x: List[float], y: List[float]) -> float:
    if not x or not y:
        return 0.0
    mean_x = statistics.mean(x)
    mean_y = statistics.mean(y)
    var_x = statistics.pvariance(x) if len(x) > 1 else 0.0
    var_y = statistics.pvariance(y) if len(y) > 1 else 0.0
    # pooled std
    n_x, n_y = max(1, len(x)), max(1, len(y))
    pooled = ((n_x - 1) * var_x + (n_y - 1) * var_y) / max(1, (n_x + n_y - 2))
    sd = pooled ** 0.5
    if sd == 0:
        return 0.0
    return (mean_x - mean_y) / sd


def main():
    metrics = load_metrics(METRICS_PATH)
    stances = load_stances(STANCE_PATH)

    # Group by topic -> {pro: [essay_ids], con: [essay_ids]}
    topic_to_ids: Dict[str, Dict[str, List[str]]] = {}
    for r in stances:
        eid = r.get("essay_id", "").strip()
        topic = r.get("topic", "").strip()
        stance = ((r.get("stance") or "").strip().lower())
        if not eid or not topic or stance not in {"pro", "con"}:
            continue
        if topic not in topic_to_ids:
            topic_to_ids[topic] = {"pro": [], "con": []}
        topic_to_ids[topic][stance].append(eid)

    # Compute per-topic differences (pro - con) for metrics
    metric_keys = [
        "attack_ratio",
        "evidence_density",
        "avg_breadth",
        "max_depth",
    ]
    per_topic_diffs: Dict[str, Dict[str, float]] = {}
    pro_values: Dict[str, List[float]] = {k: [] for k in metric_keys}
    con_values: Dict[str, List[float]] = {k: [] for k in metric_keys}

    for topic, groups in topic_to_ids.items():
        pros = groups.get("pro", [])
        cons = groups.get("con", [])
        if not pros or not cons:
            continue
        # Aggregate by mean across multiple essays per stance if present
        def agg(vals: List[str], key: str) -> float:
            xs = [metrics[e][key] for e in vals if e in metrics]
            return statistics.mean(xs) if xs else 0.0

        diffs = {}
        for k in metric_keys:
            p = agg(pros, k)
            c = agg(cons, k)
            diffs[k] = p - c
            pro_values[k].append(p)
            con_values[k].append(c)
        per_topic_diffs[topic] = diffs

    # Overall stats
    summary = {"per_topic_diffs": per_topic_diffs, "overall": {}}
    for k in metric_keys:
        xs = pro_values[k]
        ys = con_values[k]
        mean_x = statistics.mean(xs) if xs else 0.0
        mean_y = statistics.mean(ys) if ys else 0.0
        d = cohen_d(xs, ys)
        summary["overall"][k] = {
            "pro_mean": mean_x,
            "con_mean": mean_y,
            "difference": mean_x - mean_y,
            "cohen_d": d,
            "n_topics": min(len(xs), len(ys)),
        }

    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../analysis_outputs"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "aaec_stance_comparison.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote stance comparison to {out_path}")


if __name__ == "__main__":
    main()


