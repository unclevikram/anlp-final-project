#!/usr/bin/env python3
"""
Experiment 2: Automated Structural Analysis (Without Manual Stance Annotation)
Analyzes ALL essays and compares structural patterns
"""

import os
import re
from collections import defaultdict
import json

BRAT_DIR = 'dataset/ArgumentAnnotatedEssays-2.0/brat-project-final'

def parse_brat_annotation(ann_file):
    """Parse BRAT annotation file"""
    with open(ann_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    components = {}
    for line in lines:
        if line.startswith('T'):
            parts = line.strip().split('\t')
            comp_id = parts[0]
            type_span = parts[1].split(' ', 1)
            comp_type = type_span[0]
            text = parts[2] if len(parts) > 2 else ""
            components[comp_id] = {'id': comp_id, 'type': comp_type, 'text': text}

    relations = []
    for line in lines:
        if line.startswith('R'):
            parts = line.strip().split()
            rel_type = parts[1]
            arg1 = parts[2].split(':')[1]
            arg2 = parts[3].split(':')[1]
            relations.append({'type': rel_type, 'from': arg1, 'to': arg2})

    return components, relations


def compute_structural_features(components, relations):
    """Compute structural features"""
    major_claims = sum(1 for c in components.values() if c['type'] == 'MajorClaim')
    claims = sum(1 for c in components.values() if c['type'] == 'Claim')
    premises = sum(1 for c in components.values() if c['type'] == 'Premise')
    supports = sum(1 for r in relations if r['type'] == 'supports')
    attacks = sum(1 for r in relations if r['type'] == 'attacks')

    children = defaultdict(list)
    for rel in relations:
        children[rel['to']].append(rel['from'])

    def get_max_depth(start_id):
        if not children[start_id]:
            return 1
        return 1 + max(get_max_depth(child) for child in children[start_id])

    major_claim_ids = [c['id'] for c in components.values() if c['type'] == 'MajorClaim']
    max_depth = max((get_max_depth(mc_id) for mc_id in major_claim_ids), default=0)

    all_claims = [c['id'] for c in components.values() if c['type'] in ['Claim', 'MajorClaim']]
    breadths = [len(children[claim_id]) for claim_id in all_claims]
    avg_breadth = sum(breadths) / len(breadths) if breadths else 0

    attack_ratio = attacks / (supports + attacks) if (supports + attacks) > 0 else 0
    total_claims = major_claims + claims
    evidence_density = premises / total_claims if total_claims > 0 else 0

    return {
        'major_claims': major_claims,
        'claims': claims,
        'premises': premises,
        'supports': supports,
        'attacks': attacks,
        'max_depth': max_depth,
        'avg_breadth': avg_breadth,
        'attack_ratio': attack_ratio,
        'evidence_density': evidence_density,
    }


def main():
    print("="*80)
    print("AUTOMATED STRUCTURAL ANALYSIS OF ALL ESSAYS")
    print("="*80)

    all_features = []

    # Analyze all essays
    essay_files = sorted([f for f in os.listdir(BRAT_DIR) if f.endswith('.ann')])

    for essay_file in essay_files:
        ann_path = os.path.join(BRAT_DIR, essay_file)
        components, relations = parse_brat_annotation(ann_path)
        features = compute_structural_features(components, relations)
        features['essay_id'] = essay_file
        all_features.append(features)

    print(f"\nAnalyzed {len(all_features)} essays")

    # Compute statistics
    feature_names = ['max_depth', 'avg_breadth', 'attack_ratio', 'evidence_density',
                    'major_claims', 'claims', 'premises', 'supports', 'attacks']

    print("\n" + "="*80)
    print("OVERALL STATISTICS ACROSS ALL ESSAYS:")
    print("="*80)
    print(f"\n{'Feature':<25} {'Mean':>12} {'Min':>12} {'Max':>12} {'Std Dev':>12}")
    print("-" * 77)

    for fname in feature_names:
        vals = [f[fname] for f in all_features]
        mean = sum(vals) / len(vals)
        min_val = min(vals)
        max_val = max(vals)

        # Calculate std dev
        variance = sum((x - mean) ** 2 for x in vals) / len(vals)
        std_dev = variance ** 0.5

        print(f"{fname:<25} {mean:>12.3f} {min_val:>12.3f} {max_val:>12.3f} {std_dev:>12.3f}")

    # Save results
    with open('structural_analysis_results.json', 'w') as f:
        json.dump(all_features, f, indent=2)

    print("\n" + "="*80)
    print("KEY INSIGHTS:")
    print("="*80)

    print(f"""
1. ARGUMENT STRUCTURE CHARACTERISTICS:
   - Average depth of argument chains: {sum(f['max_depth'] for f in all_features)/len(all_features):.2f} levels
   - Average breadth per claim: {sum(f['avg_breadth'] for f in all_features)/len(all_features):.2f} supporters
   - Attack vs Support ratio: {sum(f['attack_ratio'] for f in all_features)/len(all_features):.4f}
   - Evidence density: {sum(f['evidence_density'] for f in all_features)/len(all_features):.2f} premises per claim

2. COMPONENT DISTRIBUTION:
   - Average major claims: {sum(f['major_claims'] for f in all_features)/len(all_features):.2f}
   - Average claims: {sum(f['claims'] for f in all_features)/len(all_features):.2f}
   - Average premises: {sum(f['premises'] for f in all_features)/len(all_features):.2f}

3. RELATION PATTERNS:
   - Support relations dominate over attack relations
   - Most essays have tree-like structures (low attack ratio)
   - Persuasive essays focus on building positive cases

4. NEXT STEPS FOR HYPOTHESIS 1 TESTING:
   - Need manual stance annotation for essay pairs
   - Then compare pro vs con using these structural metrics
   - Run statistical significance tests
   - Create visualizations

Results saved to: structural_analysis_results.json
    """)


if __name__ == '__main__':
    main()
