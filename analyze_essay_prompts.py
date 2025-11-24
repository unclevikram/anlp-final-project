#!/usr/bin/env python3
"""
Analyze essay dataset to find:
1. Topics with multiple essays
2. Stance distribution per topic
3. Argument structure statistics
"""

import csv
import re
from collections import defaultdict, Counter
import os
import json

# Read prompts
essays = []
with open('dataset/ArgumentAnnotatedEssays-2.0/prompts.csv', 'r', encoding='latin-1') as f:
    reader = csv.DictReader(f, delimiter=';')
    for row in reader:
        essays.append(row)

print(f"Total essays: {len(essays)}")
print(f"\nFirst essay:")
print(essays[0])

# Group by prompt to find topics with multiple essays
prompt_to_essays = defaultdict(list)
for essay in essays:
    prompt = essay['PROMPT']
    essay_id = essay['ESSAY']
    prompt_to_essays[prompt].append(essay_id)

prompt_counts = [(prompt, len(essay_ids)) for prompt, essay_ids in prompt_to_essays.items()]
prompt_counts.sort(key=lambda x: x[1], reverse=True)

print(f"\n{'='*80}")
print("TOPICS WITH MULTIPLE ESSAYS:")
print(f"{'='*80}")
topics_with_multiple = [p for p in prompt_counts if p[1] > 1]
print(f"\nFound {len(topics_with_multiple)} topics with multiple essays")
print(f"Total unique topics: {len(prompt_counts)}")
print(f"\nTop 20 topics by number of essays:")
for prompt, count in prompt_counts[:20]:
    prompt_short = prompt[:70] + "..." if len(prompt) > 70 else prompt
    print(f"{count:3d} essays: {prompt_short}")

# Get essay IDs for topics with multiple essays
print(f"\n{'='*80}")
print("ESSAY PAIRS FOR SAME TOPICS:")
print(f"{'='*80}")

# Focus on topics with exactly 2 essays (likely pro/con pairs)
pairs = {prompt: essay_ids for prompt, essay_ids in prompt_to_essays.items() if len(essay_ids) == 2}
print(f"\nTopics with exactly 2 essays (potential pro/con pairs): {len(pairs)}")
pair_list = []
for topic, essay_ids in list(pairs.items())[:15]:
    topic_short = topic[:55] + "..." if len(topic) > 55 else topic
    print(f"  {essay_ids[0]}, {essay_ids[1]}: {topic_short}")
    pair_list.append({'essays': essay_ids, 'topic': topic})

# Analyze annotation files to check structure
print(f"\n{'='*80}")
print("ANALYZING ARGUMENT STRUCTURES:")
print(f"{'='*80}")

brat_dir = 'dataset/ArgumentAnnotatedEssays-2.0/brat-project-final'
structure_stats = []

# Analyze a sample of essays
sample_essays = [e['ESSAY'] for e in essays[:20]]

for essay_id in sample_essays:
    ann_file = os.path.join(brat_dir, f'{essay_id}.ann')
    if not os.path.exists(ann_file):
        continue

    with open(ann_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Count components
    major_claims = sum(1 for l in lines if '\tMajorClaim' in l)
    claims = sum(1 for l in lines if '\tClaim' in l and 'MajorClaim' not in l)
    premises = sum(1 for l in lines if '\tPremise' in l)

    # Count relations
    supports = sum(1 for l in lines if l.startswith('R') and 'supports' in l)
    attacks = sum(1 for l in lines if l.startswith('R') and 'attacks' in l)

    structure_stats.append({
        'essay': essay_id,
        'major_claims': major_claims,
        'claims': claims,
        'premises': premises,
        'supports': supports,
        'attacks': attacks,
        'total_components': major_claims + claims + premises,
        'total_relations': supports + attacks
    })

print("\nSample argument structure statistics:")
print(f"{'Essay':<12} {'MajClaim':>8} {'Claims':>8} {'Premises':>8} {'Supports':>8} {'Attacks':>8}")
print("-" * 70)
for stat in structure_stats:
    print(f"{stat['essay']:<12} {stat['major_claims']:>8} {stat['claims']:>8} {stat['premises']:>8} "
          f"{stat['supports']:>8} {stat['attacks']:>8}")

if structure_stats:
    avg_components = sum(s['total_components'] for s in structure_stats) / len(structure_stats)
    avg_relations = sum(s['total_relations'] for s in structure_stats) / len(structure_stats)
    total_supports = sum(s['supports'] for s in structure_stats)
    total_attacks = sum(s['attacks'] for s in structure_stats)

    print(f"\nAverage components per essay: {avg_components:.1f}")
    print(f"Average relations per essay: {avg_relations:.1f}")
    print(f"Support vs Attack ratio: {total_supports}:{total_attacks}")

# Analyze specific pairs to check stance
print(f"\n{'='*80}")
print("CHECKING ZOO TOPIC ESSAYS (047 vs 173):")
print(f"{'='*80}")

for essay_id in ['essay047.txt', 'essay173.txt']:
    txt_file = os.path.join(brat_dir, essay_id)
    if os.path.exists(txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"\n{essay_id}:")
            print(f"Topic: {lines[0].strip()}")
            print(f"First sentence: {lines[2].strip()[:100]}...")

# Save results
output = {
    'total_essays': len(essays),
    'unique_topics': len(prompt_counts),
    'topics_with_pairs': len(pairs),
    'topics_with_multiple': len(topics_with_multiple),
    'pair_examples': pair_list[:20],
    'structure_statistics': structure_stats[:20]
}

with open('essay_analysis_results.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*80}")
print("Analysis complete! Results saved to essay_analysis_results.json")
print(f"{'='*80}")
