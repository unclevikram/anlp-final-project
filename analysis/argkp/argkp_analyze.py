import csv
import json
import os
from collections import defaultdict, Counter


ARGKP_CSV = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../dataset/IBM_Debater_(R)_ArgKP-2021/ArgKP-2021_dataset.csv",
    )
)


def analyze_argkp(csv_path: str):
    topic_to_counts = defaultdict(lambda: Counter())
    stance_to_counts = Counter()
    total_rows = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            topic = row.get('topic', 'UNKNOWN')
            stance = row.get('stance', '')
            label = row.get('label', '')  # 1 matching / 0 non-matching
            topic_to_counts[topic]['pairs'] += 1
            if label == '1':
                topic_to_counts[topic]['matches'] += 1
            if stance:
                stance_to_counts[stance] += 1

    summary = {
        "total_pairs": total_rows,
        "stance_distribution": dict(stance_to_counts),
        "topics": {
            t: {
                "pairs": int(c['pairs']),
                "matches": int(c.get('matches', 0)),
                "match_rate": (int(c.get('matches', 0)) / int(c['pairs'])) if int(c['pairs']) > 0 else 0.0,
            }
            for t, c in topic_to_counts.items()
        },
    }
    return summary


def main():
    os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../analysis_outputs")), exist_ok=True)
    out_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../analysis_outputs/argkp_summary.json")
    )
    summary = analyze_argkp(ARGKP_CSV)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote ArgKP summary to {out_path}")


if __name__ == "__main__":
    main()



