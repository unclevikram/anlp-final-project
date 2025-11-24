#!/usr/bin/env python3
"""
Experiment 2: Pro vs Con Structural Analysis
Compares argument structures between pro and con essays on same topics
"""

import os
import re
from collections import defaultdict
import json

# Configuration
BRAT_DIR = 'dataset/ArgumentAnnotatedEssays-2.0/brat-project-final'

def parse_brat_annotation(ann_file):
    """Parse BRAT annotation file and extract argument structure"""
    with open(ann_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse components
    components = {}
    for line in lines:
        if line.startswith('T'):
            parts = line.strip().split('\t')
            comp_id = parts[0]
            type_span = parts[1].split(' ', 1)
            comp_type = type_span[0]
            text = parts[2] if len(parts) > 2 else ""
            components[comp_id] = {
                'id': comp_id,
                'type': comp_type,
                'text': text
            }

    # Parse relations
    relations = []
    for line in lines:
        if line.startswith('R'):
            # Format: R1	supports Arg1:T4 Arg2:T3
            parts = line.strip().split()
            rel_type = parts[1]
            arg1 = parts[2].split(':')[1]
            arg2 = parts[3].split(':')[1]
            relations.append({
                'type': rel_type,
                'from': arg1,
                'to': arg2
            })

    return components, relations


def compute_structural_features(components, relations):
    """Compute structural features for an essay"""

    # Count components
    major_claims = sum(1 for c in components.values() if c['type'] == 'MajorClaim')
    claims = sum(1 for c in components.values() if c['type'] == 'Claim')
    premises = sum(1 for c in components.values() if c['type'] == 'Premise')

    # Count relation types
    supports = sum(1 for r in relations if r['type'] == 'supports')
    attacks = sum(1 for r in relations if r['type'] == 'attacks')

    # Build adjacency for depth calculation
    children = defaultdict(list)
    for rel in relations:
        children[rel['to']].append(rel['from'])

    # Calculate maximum depth (BFS from major claims)
    def get_max_depth(start_id):
        if not children[start_id]:
            return 1
        max_child_depth = max(get_max_depth(child) for child in children[start_id])
        return 1 + max_child_depth

    major_claim_ids = [c['id'] for c in components.values() if c['type'] == 'MajorClaim']
    max_depth = max((get_max_depth(mc_id) for mc_id in major_claim_ids), default=0)

    # Calculate breadth (average supporters per claim)
    all_claims = [c['id'] for c in components.values() if c['type'] in ['Claim', 'MajorClaim']]
    breadths = [len(children[claim_id]) for claim_id in all_claims]
    avg_breadth = sum(breadths) / len(breadths) if breadths else 0

    # Calculate ratios
    attack_ratio = attacks / (supports + attacks) if (supports + attacks) > 0 else 0
    total_claims = major_claims + claims
    evidence_density = premises / total_claims if total_claims > 0 else 0
    claim_premise_ratio = total_claims / premises if premises > 0 else 0

    return {
        'major_claims': major_claims,
        'claims': claims,
        'premises': premises,
        'total_components': major_claims + claims + premises,
        'supports': supports,
        'attacks': attacks,
        'total_relations': supports + attacks,
        'max_depth': max_depth,
        'avg_breadth': avg_breadth,
        'attack_ratio': attack_ratio,
        'evidence_density': evidence_density,
        'claim_premise_ratio': claim_premise_ratio
    }


def determine_essay_stance(essay_id, components):
    """
    Determine essay stance by reading first paragraph and major claim
    This is a MANUAL verification step - needs human judgment
    Returns: 'PRO', 'CON', or 'UNKNOWN'
    """
    txt_file = os.path.join(BRAT_DIR, essay_id.replace('.ann', '.txt'))

    # Get major claim text
    major_claims = [c['text'] for c in components.values() if c['type'] == 'MajorClaim']

    # Read first paragraph
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        topic = lines[0].strip() if lines else ""
        first_para = lines[2].strip() if len(lines) > 2 else ""

    print(f"\n{'='*80}")
    print(f"Essay: {essay_id}")
    print(f"Topic: {topic}")
    print(f"\nMajor Claim(s):")
    for mc in major_claims:
        print(f"  - {mc}")
    print(f"\nFirst sentence: {first_para[:150]}...")
    print(f"{'='*80}")

    # Manual annotation
    stance = input("Enter stance (PRO/CON/SKIP): ").strip().upper()
    return stance if stance in ['PRO', 'CON'] else 'UNKNOWN'


def main():
    print("="*80)
    print("EXPERIMENT 2: PRO VS CON STRUCTURAL ANALYSIS")
    print("="*80)

    # Load previously identified pairs
    with open('essay_analysis_results.json', 'r') as f:
        analysis = json.load(f)

    pairs = analysis['pair_examples'][:15]  # Top 15 pairs

    print(f"\nFound {len(pairs)} potential pro/con pairs")
    print("\nSTEP 1: Manual Stance Annotation")
    print("For each essay pair, we'll determine the stance...\n")

    # Annotate stances
    stance_annotations = {}

    for i, pair_info in enumerate(pairs[:10], 1):  # Annotate first 10 pairs
        print(f"\n{'*'*80}")
        print(f"PAIR {i}/10: {pair_info['topic'][:70]}")
        print(f"{'*'*80}")

        essays = pair_info['essays']

        for essay_id in essays:
            ann_file = os.path.join(BRAT_DIR, essay_id.replace('.txt', '.ann'))
            if not os.path.exists(ann_file):
                continue

            components, relations = parse_brat_annotation(ann_file)
            stance = determine_essay_stance(essay_id, components)

            if stance != 'UNKNOWN':
                features = compute_structural_features(components, relations)
                stance_annotations[essay_id] = {
                    'stance': stance,
                    'features': features,
                    'topic': pair_info['topic']
                }

        # Check if we have a valid pro/con pair
        if len(stance_annotations) >= 2:
            stances_in_pair = [stance_annotations[e]['stance'] for e in essays if e in stance_annotations]
            if 'PRO' in stances_in_pair and 'CON' in stances_in_pair:
                print(f"\n✓ Valid PRO/CON pair found!")
            else:
                print(f"\n✗ Both essays have same stance - not a valid pair")

    # Save annotations
    with open('stance_annotations.json', 'w') as f:
        json.dump(stance_annotations, f, indent=2)

    print(f"\n{'='*80}")
    print(f"Annotated {len(stance_annotations)} essays")
    print(f"Saved to stance_annotations.json")
    print(f"{'='*80}")

    # Analyze pro vs con
    print("\n" + "="*80)
    print("STEP 2: STRUCTURAL COMPARISON")
    print("="*80)

    pro_features = [data['features'] for data in stance_annotations.values() if data['stance'] == 'PRO']
    con_features = [data['features'] for data in stance_annotations.values() if data['stance'] == 'CON']

    print(f"\nPRO essays: {len(pro_features)}")
    print(f"CON essays: {len(con_features)}")

    if pro_features and con_features:
        feature_names = ['max_depth', 'avg_breadth', 'attack_ratio', 'evidence_density',
                        'claim_premise_ratio', 'total_components', 'total_relations']

        print(f"\n{'Feature':<25} {'PRO Mean':>12} {'CON Mean':>12} {'Difference':>12}")
        print("-" * 65)

        for fname in feature_names:
            pro_vals = [f[fname] for f in pro_features]
            con_vals = [f[fname] for f in con_features]

            pro_mean = sum(pro_vals) / len(pro_vals)
            con_mean = sum(con_vals) / len(con_vals)
            diff = pro_mean - con_mean

            print(f"{fname:<25} {pro_mean:>12.3f} {con_mean:>12.3f} {diff:>12.3f}")

        print("\n" + "="*80)
        print("PRELIMINARY FINDINGS:")
        print("="*80)
        print("""
        Note: These results are based on manual annotation of essay pairs.
        Statistical significance testing requires more samples.

        Next steps:
        1. Complete annotation of all 24 pairs
        2. Run statistical tests (t-tests, effect sizes)
        3. Create visualizations
        4. Qualitative analysis of 3 example pairs
        """)


if __name__ == '__main__':
    main()
