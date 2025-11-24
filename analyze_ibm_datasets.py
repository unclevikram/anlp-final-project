#!/usr/bin/env python3
"""
Analyze IBM datasets to understand:
1. What topics are available
2. What stance labels exist
3. What structural info (if any) is available
"""

import csv
from collections import Counter, defaultdict

print("="*80)
print("ANALYZING IBM ARGKP-2021 DATASET")
print("="*80)

# Analyze ArgKP dataset
argkp_data = []
with open('dataset/IBM_Debater_(R)_ArgKP-2021/ArgKP-2021_dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        argkp_data.append(row)

print(f"\nTotal argument-keypoint pairs: {len(argkp_data)}")
print(f"\nFirst row:")
for key, val in list(argkp_data[0].items()):
    print(f"  {key}: {val}")

# Count topics
topics = Counter(row['topic'] for row in argkp_data)
print(f"\n{len(topics)} unique topics:")
for topic, count in topics.most_common():
    print(f"  {count:5d} pairs: {topic}")

# Analyze stance distribution
stances = Counter(row['stance'] for row in argkp_data)
print(f"\nStance distribution:")
for stance, count in stances.items():
    label = "PRO" if stance == "1" else "CON"
    print(f"  {label}: {count}")

# Analyze labels
labels = Counter(row['label'] for row in argkp_data)
print(f"\nLabel distribution (matching vs non-matching):")
for label, count in labels.items():
    label_name = "MATCHING" if label == "1" else "NON-MATCHING"
    print(f"  {label_name}: {count}")

# Sample a topic to show structure
sample_topic = list(topics.keys())[0]
sample_rows = [r for r in argkp_data if r['topic'] == sample_topic][:3]
print(f"\nSample from topic '{sample_topic}':")
for i, row in enumerate(sample_rows, 1):
    print(f"\n  Example {i}:")
    print(f"    Argument: {row['argument'][:80]}...")
    print(f"    Key Point: {row['key_point']}")
    print(f"    Stance: {'PRO' if row['stance']=='1' else 'CON'}")
    print(f"    Matching: {'YES' if row['label']=='1' else 'NO'}")

print("\n" + "="*80)
print("ANALYZING IBM ARGUMENT QUALITY DATASET")
print("="*80)

# Analyze arg quality dataset
quality_data = []
with open('dataset/IBM_Debater_(R)_arg_quality_rank_30k/arg_quality_rank_30k.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        quality_data.append(row)

print(f"\nTotal arguments: {len(quality_data)}")
print(f"\nFirst row:")
for key, val in list(quality_data[0].items()):
    val_str = val[:60] if len(val) > 60 else val
    print(f"  {key}: {val_str}")

# Count topics
quality_topics = Counter(row['topic'] for row in quality_data)
print(f"\n{len(quality_topics)} unique topics:")
for topic, count in quality_topics.most_common(15):
    print(f"  {count:5d} args: {topic}")

# Analyze stance distribution
quality_stances = Counter(row['stance_WA'] for row in quality_data)
print(f"\nStance distribution:")
for stance, count in quality_stances.items():
    if stance == '1':
        label = "PRO"
    elif stance == '-1':
        label = "CON"
    else:
        label = "NEUTRAL/OTHER"
    print(f"  {label}: {count}")

# Analyze data splits
splits = Counter(row['set'] for row in quality_data)
print(f"\nData splits:")
for split, count in splits.items():
    print(f"  {split}: {count}")

# Sample topic
sample_topic_q = list(quality_topics.keys())[0]
sample_q = [r for r in quality_data if r['topic'] == sample_topic_q][:3]
print(f"\nSample from topic '{sample_topic_q}':")
for i, row in enumerate(sample_q, 1):
    print(f"\n  Example {i}:")
    print(f"    Argument: {row['argument'][:80]}...")
    print(f"    Topic: {row['topic']}")
    stance_label = "PRO" if row['stance_WA'] == '1' else ("CON" if row['stance_WA'] == '-1' else "OTHER")
    print(f"    Stance: {stance_label}")
    print(f"    Quality (WA): {row['WA']}")
    print(f"    Set: {row['set']}")

# Check for overlap in topics
common_topics = set(topics.keys()) & set(quality_topics.keys())
print(f"\n{'='*80}")
print(f"TOPIC OVERLAP BETWEEN DATASETS:")
print(f"{'='*80}")
print(f"\nTopics in both ArgKP and Quality datasets: {len(common_topics)}")
for topic in list(common_topics)[:10]:
    print(f"  - {topic}")

print(f"\n{'='*80}")
print("KEY FINDINGS:")
print(f"{'='*80}")
print(f"""
1. ArgKP Dataset:
   - {len(argkp_data)} argument-keypoint pairs
   - {len(topics)} topics
   - Has PRO/CON stance labels
   - Task: Match arguments to key points (summarization/grouping)
   - NO argument structure annotations (no Claims/Premises/Relations)

2. Quality Dataset:
   - {len(quality_data)} arguments
   - {len(quality_topics)} topics
   - Has PRO/CON stance labels
   - Has quality scores
   - Split into train/dev/test
   - NO argument structure annotations

3. Both datasets have stance labels but NO structural annotations
   like Claims, Premises, or Support/Attack relations

4. To get argument structures from these datasets, we would need to:
   - Train a model on the essay data
   - Apply it to extract structures from IBM arguments
   - Evaluate indirectly or via manual sampling
""")
