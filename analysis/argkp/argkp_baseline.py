import csv
import json
import os
import random
from typing import List, Tuple


ARGKP_CSV = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../dataset/IBM_Debater_(R)_ArgKP-2021/ArgKP-2021_dataset.csv",
    )
)

STOPWORDS = set(
    "a an the and or for of on in at to with by is are was were be being been it this that these those from as not no".split()
)


def tokenize(s: str) -> List[str]:
    return [t for t in ''.join(c.lower() if c.isalnum() else ' ' for c in s).split() if t and t not in STOPWORDS]


def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / max(1, len(sa | sb))


def load_pairs(csv_path: str, max_rows: int = 5000) -> List[Tuple[str, str, int]]:
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            arg = row.get('argument', '')
            kp = row.get('key_point', '')
            label = 1 if row.get('label', '0') == '1' else 0
            rows.append((arg, kp, label))
    random.seed(42)
    random.shuffle(rows)
    return rows[:max_rows]


def evaluate(threshold: float, data: List[Tuple[str, str, int]]):
    tp = fp = tn = fn = 0
    for arg, kp, label in data:
        s = jaccard(tokenize(arg), tokenize(kp))
        pred = 1 if s >= threshold else 0
        if pred == 1 and label == 1:
            tp += 1
        elif pred == 1 and label == 0:
            fp += 1
        elif pred == 0 and label == 0:
            tn += 1
        else:
            fn += 1
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0
    acc = (tp + tn) / max(1, (tp + tn + fp + fn))
    return {"precision": precision, "recall": recall, "f1": f1, "accuracy": acc}


def main():
    data = load_pairs(ARGKP_CSV, max_rows=5000)
    # simple split
    n = len(data)
    split = int(0.8 * n)
    train, test = data[:split], data[split:]
    # tune threshold on train
    best_t = 0.0
    best_f1 = -1.0
    for t in [i / 100 for i in range(1, 51)]:  # 0.01 .. 0.50
        m = evaluate(t, train)
        if m["f1"] > best_f1:
            best_f1 = m["f1"]
            best_t = t
    test_metrics = evaluate(best_t, test)
    out = {
        "threshold": best_t,
        "train_f1": best_f1,
        "test_metrics": test_metrics,
        "n_train": len(train),
        "n_test": len(test),
    }
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../analysis_outputs"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "argkp_baseline.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print(f"Wrote ArgKP baseline to {out_path}")


if __name__ == "__main__":
    main()



