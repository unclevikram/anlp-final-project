# Detailed Analysis: What Went Wrong

## The Gap Between Proposal and Delivery

### PROPOSAL SAID (October):
```
Methods:
• BiLSTM-CRF sequence tagger for claim/premise spans
• Fine-tune BERT/Longformer for component detection
• Cross-encoder for relation modeling
• Evaluate with span-level P/R/F1

Timeline:
• October 20: Implement baseline models and generate initial metrics
• November 3: Fine-tune transformer model on primary dataset
```

### MIDTERM DELIVERED (November):
```
What was actually done:
✅ analyze_essay_prompts.py - Reads CSV, counts topics
✅ analyze_ibm_datasets.py - Prints dataset statistics
✅ experiment2_auto_analysis.py - Parses BRAT, computes gold-label statistics
✅ experiment2_structural_analysis.py - Interactive stance annotation tool

What was NOT done:
❌ No BiLSTM-CRF implementation
❌ No BERT fine-tuning
❌ No cross-encoder training
❌ No model predictions
❌ No P/R/F1 evaluation
❌ No training/test split usage
❌ No baseline comparison
```

---

## Line-by-Line: What the Code Actually Does

### File: `experiment2_auto_analysis.py`

**What the midterm report CLAIMED:**
> "Experiment 1: Baseline Argument Component Detection ✅ COMPLETE"
> "We evaluate component spans by P/R/F1 (exact and partial match)"

**What the code ACTUALLY DOES:**
```python
def parse_brat_annotation(ann_file):
    """Parse BRAT annotation file"""
    # Just reads the GOLD annotations from BRAT files
    # NO MODEL, NO PREDICTIONS
```

```python
def compute_structural_features(components, relations):
    """Compute structural features"""
    # Counts gold components and relations
    # NO MODEL EVALUATION
```

```python
for essay_file in essay_files:
    components, relations = parse_brat_annotation(ann_path)  # GOLD LABELS
    features = compute_structural_features(components, relations)  # GOLD STATS
```

**Reality:** This script just reads gold annotations and computes statistics. It's **dataset exploration**, not **model evaluation**.

---

### File: `analyze_essay_prompts.py`

**What it does:**
- Reads `prompts.csv`
- Counts how many essays per topic
- Identifies potential pro/con pairs
- NO MODELING

**Is this an experiment?** No. It's data exploration.

---

### File: `analyze_ibm_datasets.py`

**What it does:**
- Reads IBM CSV files
- Prints dataset statistics
- Shows examples
- NO MODELING

**Is this an experiment?** No. It's data exploration.

---

## The Fundamental Confusion

### What "Running an Experiment" Means in ML:

```python
# STEP 1: Train a model
model = BertForTokenClassification.from_pretrained('bert-base-uncased')
model.train()
for batch in train_loader:
    loss = model(**batch)
    loss.backward()
    optimizer.step()

# STEP 2: Make predictions
model.eval()
predictions = []
for batch in test_loader:
    pred = model(**batch)
    predictions.append(pred)

# STEP 3: Evaluate predictions against gold
from seqeval.metrics import f1_score
f1 = f1_score(gold_labels, predictions)
print(f"F1 Score: {f1:.3f}")  # THIS is what you report
```

### What You Actually Did:

```python
# Read gold labels
components, relations = parse_brat_annotation(file)

# Compute stats from gold labels
stats = {
    'claims': sum(1 for c in components if c['type'] == 'Claim'),
    'premises': sum(1 for c in components if c['type'] == 'Premise'),
}

print(f"Average claims: {mean(stats)}")  # This is NOT model evaluation
```

---

## Why This Happened

### Misunderstanding #1: "Preliminary Experiments"
**Thought:** Dataset exploration counts as preliminary work
**Reality:** Experiments require training and evaluating models

### Misunderstanding #2: "Gold Labels as Baselines"
**Thought:** Analyzing gold annotations shows what's possible
**Reality:** You need to compare MODEL PREDICTIONS to gold labels

### Misunderstanding #3: "Framework = Results"
**Thought:** Building analysis scripts is completing the experiment
**Reality:** You need to actually RUN experiments and report results

---

## Specific Claims vs Reality

### Claim 1:
> "Following precedent, we evaluate component spans by P/R/F1 (both exact and partial)"

**Reality:** Never computed P/R/F1 because never made predictions

### Claim 2:
> "Experiment 1: Baseline Argument Component Detection ✅ COMPLETE"

**Reality:** No baseline model was trained or evaluated

### Claim 3:
> "Using conservative auto-labels and gold BRAT graphs"

**Reality:** Only used gold labels, no "auto-labels" exist

### Claim 4:
> "Baseline model results" in expected deliverables

**Reality:** No model exists, so no results exist

### Claim 5:
> "We will report P/R/F1 scores on test set predictions"

**Reality:** No test set was used, no predictions made

---

## The Pro/Con Labeling Problem

### What You Claimed:
> "24 topics with exactly 2 essays (potential pro/con pairs)"

### The Reality:

**Essay 047:**
- **Topic**: "Zoos should be built to protect rural animals"
- **Stance**: AGAINST zoos (argues they harm animals)
- **Label**: This is "CON" on the topic AS PHRASED

**Essay 173:**
- **Topic**: "Zoos have no useful purpose?"  (DIFFERENT PHRASING!)
- **Stance**: FOR zoos (argues they are useful)
- **Label**: This is "PRO" on the topic AS PHRASED

**The Problem:**
- These are NOT the same topic with opposite stances
- They're two different topic phrasings
- "Pro on topic A" ≠ "Con on topic B"
- Pro on "should zoos be built?" is NOT the same as Con on "do zoos have no purpose?"

**Why the instructor is right:**
> "the pro stance in a topic like 'climate change is real' would be the con stance in 'climate change is fake' so what exactly is the context in which pro and con are meaningful labels?"

Your labels are meaningless without a UNIFIED topic framing.

---

## What You Should Have Done

### For the Midterm:

#### Experiment 1: Baseline Component Detection

```python
# 1. Load and split data
train_essays = load_essays('train-test-split.csv', split='TRAIN')
test_essays = load_essays('train-test-split.csv', split='TEST')

# 2. Prepare for sequence tagging
X_train, y_train = convert_to_bio_tags(train_essays)
X_test, y_test = convert_to_bio_tags(test_essays)

# 3. Train a baseline model
from sklearn_crfsuite import CRF
crf = CRF()
crf.fit(X_train, y_train)

# 4. Predict on test set
y_pred = crf.predict(X_test)

# 5. Evaluate predictions
from seqeval.metrics import classification_report
print(classification_report(y_test, y_pred))
# Output:
#              precision    recall  f1-score
# MajorClaim      0.65      0.58      0.61
# Claim           0.68      0.63      0.65
# Premise         0.72      0.71      0.71
```

**Then you could claim:**
✅ "We trained a CRF baseline and achieved 0.65 F1 for claims"
✅ "This is below the BERT-based results from Stab & Gurevych (0.75 F1)"
✅ "For the final project, we will implement BERT to close this gap"

#### Experiment 2: Pro/Con Analysis (If Fixed)

```python
# 1. Manually create unified topic labels
topic_mapping = {
    'essay047': {'topic': 'zoos', 'stance': 'con'},
    'essay173': {'topic': 'zoos', 'stance': 'pro'},
    # ... for all 24 pairs
}

# 2. Load gold structures for annotated essays
pro_essays = [e for e in essays if stance[e] == 'pro']
con_essays = [e for e in essays if stance[e] == 'con']

# 3. Compare structural features
pro_depth = mean([structure_depth(e) for e in pro_essays])
con_depth = mean([structure_depth(e) for e in con_essays])

# 4. Statistical test
from scipy.stats import ttest_rel
t_stat, p_value = ttest_rel(pro_depths, con_depths)
print(f"Pro mean depth: {pro_depth:.2f}")
print(f"Con mean depth: {con_depth:.2f}")
print(f"Difference: t={t_stat:.2f}, p={p_value:.3f}")

# 5. Confidence intervals
ci = bootstrap_ci(pro_depths - con_depths, confidence=0.95)
print(f"95% CI for difference: [{ci[0]:.2f}, {ci[1]:.2f}]")
```

**Then you could claim:**
✅ "Pro essays have significantly deeper structures (M=2.1) than con essays (M=1.6), t(23)=2.8, p=0.01, 95% CI [0.2, 0.8]"

---

## Comparison: Claim vs Reality

| **What Report Claims** | **What Code Does** | **What Should Have Been Done** |
|------------------------|--------------------|---------------------------------|
| "Trained baseline model" | Parses gold annotations | Train CRF or BiLSTM on train set |
| "Evaluated with P/R/F1" | Counts gold components | Predict on test set, compute F1 |
| "Preliminary experiments complete" | Dataset exploration | Actual model training & eval |
| "Conservative auto-labels" | Gold BRAT labels | Model predictions vs gold |
| "Statistical tests with effect sizes" | Means without tests | t-tests, Cohen's d, CI |
| "Confidence intervals" | No CIs reported | Bootstrap or t-distribution |

---

## The Three Critical Errors

### Error #1: Confusing Exploration with Experiments
- **What you did:** Analyzed existing data
- **What you claimed:** Ran experiments
- **Fix:** Actually train models and evaluate them

### Error #2: Treating Gold Labels as Results
- **What you did:** Computed statistics from gold annotations
- **What you claimed:** These are "experiment results"
- **Fix:** Model predictions vs gold is what you evaluate

### Error #3: Planning ≠ Doing
- **What you did:** Created code framework for analysis
- **What you claimed:** "Experiments complete"
- **Fix:** Actually run the full pipeline and report results

---

## For the Final Project: Checklist

### ✅ Must Have for Model Training

- [ ] **Load train/test split** from `train-test-split.csv`
- [ ] **Convert BRAT to BIO tags** for sequence labeling
- [ ] **Train a model** (CRF baseline + BERT)
- [ ] **Make predictions** on test set
- [ ] **Evaluate predictions** vs gold labels
- [ ] **Report metrics** with confidence intervals
- [ ] **Compare to baseline** (Stab & Gurevych 2017)
- [ ] **Error analysis** with examples
- [ ] **Document everything** (hyperparameters, training procedure)

### ✅ Must Have for Pro/Con Analysis

- [ ] **Fix labeling problem** - either:
  - Option A: Reframe as rhetorical mode (constructive/critical)
  - Option B: Manual unified topic annotation
- [ ] **Clear operational definitions** of categories
- [ ] **Statistical tests** with p-values and effect sizes
- [ ] **Confidence intervals** on all reported means
- [ ] **Visualizations** (box plots, distributions)
- [ ] **Grounding in theory** (cite rhetoric literature)

### ✅ Must Have for Report

- [ ] **All referenced figures** actually included
- [ ] **Consistent terminology** throughout
- [ ] **No claims without evidence** (if you say you did it, show results)
- [ ] **Theoretical motivation** for hypotheses
- [ ] **Honest limitations** discussion

---

## Bottom Line

**What you delivered:** Dataset exploration scripts
**What you claimed:** Complete preliminary experiments
**Gap:** NO MODEL TRAINING, NO EVALUATION, NO RESULTS

**For the final project:** Actually train models, evaluate them properly, and fix the pro/con framing issue.

**The good news:** You have clean data, clear task definition, and now understand what's required. You CAN deliver a solid final project if you focus on:
1. Training actual models
2. Reporting actual results
3. Fixing the conceptual issues
