import csv
import os
import re
import zipfile
from typing import Dict, List, Tuple


AAEC_ZIP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../dataset/ArgumentAnnotatedEssays-2.0/brat-project-final.zip",
    )
)
STANCE_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "stance_labels.csv"))


AGREE_PAT = re.compile(r"\b(i\s+)?(strongly\s+|completely\s+)?agree\b", re.I)
DISAGREE_PAT = re.compile(r"\b(i\s+)?(strongly\s+|completely\s+)?disagree\b", re.I)
SHOULD_PAT = re.compile(r"\bshould(?!\s*not)\b", re.I)
SHOULD_NOT_PAT = re.compile(r"\bshould\s*not\b|shouldn['’]t\b", re.I)
POSITIVE_PAT = re.compile(r"\b(positive|beneficial|good|advantage|advantages)\b", re.I)
NEGATIVE_PAT = re.compile(r"\b(negative|harmful|bad|disadvantage|disadvantages)\b", re.I)
GOOD_IDEA_PAT = re.compile(r"\bgood\s+idea\b", re.I)
BAD_IDEA_PAT = re.compile(r"\bbad\s+idea\b", re.I)
ALLOW_PAT = re.compile(r"\b(allow|allowed|legalize|legalised|legalized)\b", re.I)
BAN_PAT = re.compile(r"\b(ban|banned|illegal|prohibit|forbid|forbidden)\b", re.I)


def load_essay_texts(zip_path):
    texts = {}
    with zipfile.ZipFile(zip_path) as zf:
        txt_files = [p for p in zf.namelist() if p.lower().endswith(".txt")]
        for p in txt_files:
            base = os.path.basename(p)
            try:
                content = zf.read(p).decode("utf-8", errors="ignore")
            except KeyError:
                continue
            texts[base] = content
    return texts


def load_claim_texts(zip_path) -> Dict[str, List[str]]:
    claims: Dict[str, List[str]] = {}
    with zipfile.ZipFile(zip_path) as zf:
        ann_files = [p for p in zf.namelist() if p.lower().endswith(".ann")]
        for p in ann_files:
            base = os.path.basename(p)
            try:
                content = zf.read(p).decode("utf-8", errors="ignore")
            except KeyError:
                continue
            claim_texts: List[str] = []
            for line in content.splitlines():
                line = line.strip()
                if not line or not line.startswith("T"):
                    continue
                try:
                    tid, rest = line.split("\t", 1)
                    label_span, text = rest.split("\t", 1)
                except ValueError:
                    continue
                label = label_span.split()[0].lower()
                if label in {"claim", "majorclaim"}:
                    claim_texts.append(text)
            claims[base] = claim_texts
    return claims


def infer_stance(text: str, prompt: str, claim_texts: List[str]) -> str:
    if not text:
        return ""
    # Primary cues: explicit agree/disagree
    if DISAGREE_PAT.search(text):
        return "con"
    if AGREE_PAT.search(text):
        return "pro"
    # Consider claims (often clearer than body)
    combined = " \n ".join(claim_texts + [text])
    t = combined.lower()

    # Generic should/should not
    if SHOULD_NOT_PAT.search(combined):
        return "con"
    if SHOULD_PAT.search(combined):
        return "pro"

    # Positive/negative trend prompts
    if re.search(r"positive\s+trend|good\s+thing", prompt, re.I):
        if POSITIVE_PAT.search(combined):
            return "pro"
        if NEGATIVE_PAT.search(combined):
            return "con"

    # Good/bad idea prompts
    if re.search(r"good\s+idea|bad\s+idea", prompt, re.I) or re.search(r"Do you think.*good idea", prompt, re.I):
        if GOOD_IDEA_PAT.search(combined):
            return "pro"
        if BAD_IDEA_PAT.search(combined):
            return "con"

    # Allow vs ban prompts
    if re.search(r"(allow|ban|legalize|illegal)", prompt, re.I):
        if ALLOW_PAT.search(combined):
            return "pro"
        if BAN_PAT.search(combined):
            return "con"

    # Advantages outweigh disadvantages prompts
    if re.search(r"advantages?\s+outweigh\s+disadvantages?", prompt, re.I):
        if re.search(r"advantages?\s+outweigh\s+disadvantages?", combined, re.I):
            return "pro"
        if re.search(r"disadvantages?\s+outweigh\s+advantages?", combined, re.I):
            return "con"

    return ""


def main():
    texts = load_essay_texts(AAEC_ZIP_PATH)
    claims_by_ann = load_claim_texts(AAEC_ZIP_PATH)
    rows = []
    with open(STANCE_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    updated = 0
    for r in rows:
        if (r.get('stance') or '').strip():
            continue
        essay_id = (r.get('essay_id') or '').strip()
        prompt = (r.get('topic') or '').strip()
        if not essay_id:
            continue
        txt_name = essay_id.replace('.ann', '.txt')
        text = texts.get(txt_name, '')
        claim_texts = claims_by_ann.get(essay_id, [])
        stance = infer_stance(text, prompt, claim_texts)
        if stance:
            r['stance'] = stance
            updated += 1

    fieldnames = ['essay_id', 'topic', 'stance']
    with open(STANCE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, '') for k in fieldnames})

    print(f"Auto-labeled {updated} stance entries; wrote back to {STANCE_CSV}")


if __name__ == "__main__":
    main()


