# Argument Structure in Online Debates: Refined Project Plan
**Based on Comprehensive Dataset Analysis**

---

## Dataset Analysis Summary

### Available Data:
1. **Persuasive Essays (Stab & Gurevych 2017)**:
   - 402 essays with COMPLETE argument structure annotations
   - 24 topics with exactly 2 essays (potential pro/con pairs)
   - Annotations: MajorClaims, Claims, Premises, Support/Attack relations
   - **This is our GOLD resource**

2. **IBM ArgKP-2021**:
   - 27,519 arguments across 31 topics
   - Has PRO/CON stance labels
   - NO argument structure annotations
   - Task: argument-to-key point matching

3. **IBM Argument Quality**:
   - 30,497 arguments across 71 topics
   - Has PRO/CON stance labels + quality scores
   - Train/dev/test splits
   - NO argument structure annotations
   - 28 topics overlap with ArgKP

4. **CMV Corpus**:
   - Conversation data but NO argument annotations
   - **EXCLUDED from project scope**

---

## Three Testable Hypotheses

### **Hypothesis 1: Structural Differences Between Pro and Con Stances**
**Research Question**: Do pro-stance and con-stance arguments exhibit systematically different structural patterns in persuasive essays?

**Specific Predictions**:
- **H1a**: Pro-stance essays have deeper support chains (more premises per claim) as they build constructive cases
- **H1b**: Con-stance essays have more attack relations as they refute opposing views
- **H1c**: Pro and con stances differ in their use of evidence density (premises per major claim)

**Why This Matters**:
- **Community**: Computational argumentation researchers, debate coaches, writing instructors
- **Impact**: Understanding how stance affects argumentation strategy can improve:
  - Automated argument quality assessment
  - Debate training systems
  - Persuasive writing instruction

**Testable With**: Essay dataset (24 pro/con pairs across same topics)

---

### **Hypothesis 2: Argument Component Detection Generalizes Across Domains**
**Research Question**: Can argument structure detection models trained on persuasive essays successfully identify components in short-form debate arguments?

**Specific Predictions**:
- **H2a**: Models trained on essay data can identify claims in IBM arguments with reasonable accuracy
- **H2b**: Premise detection will degrade more than claim detection due to domain shift (essays vs. short arguments)
- **H2c**: Transfer learning with domain adaptation will improve performance over direct transfer

**Why This Matters**:
- **Community**: NLP researchers working on domain adaptation and argument mining
- **Impact**: Demonstrates feasibility of leveraging high-quality annotations for low-resource domains

**Testable With**: Train on essay data, apply to IBM arguments, evaluate on manual sample

---

### **Hypothesis 3: Argument Quality Correlates With Structural Complexity**
**Research Question**: Do higher-quality arguments (per IBM quality scores) exhibit richer argumentative structures when automatically extracted?

**Specific Predictions**:
- **H3a**: Higher-quality arguments will have more identifiable premises per claim
- **H3b**: Higher-quality arguments will have more explicit support relations
- **H3c**: The correlation holds across pro and con stances

**Why This Matters**:
- **Community**: Developers of argument quality assessment systems, educators
- **Impact**: Provides structural features for quality prediction; informs teaching of argumentation

**Testable With**: Extract structures from IBM Quality dataset, correlate with quality scores

---

## Preliminary Experiments (For Midterm Report - Due Nov 4)

### **Experiment 1: Baseline Argument Component Detection**
**Goal**: Train a baseline model to detect argument components and establish performance metrics

**Method**:
1. **Data Preparation**:
   - Use essay dataset train/test split (already provided in train-test-split.csv)
   - Extract component types: MajorClaim, Claim, Premise
   - Convert BRAT annotations to sequence labeling format (BIO tagging)

2. **Baseline Model**:
   - **Simple**: BiLSTM-CRF for token-level sequence tagging
   - **Features**: Word embeddings (GloVe or Word2Vec), POS tags, sentence position
   - **Implementation**: Use existing libraries (sklearn-crfsuite or simple PyTorch)

3. **Evaluation Metrics**:
   - Span-level F1 for each component type
   - Exact match and partial overlap
   - Confusion matrix between component types

4. **Expected Results**:
   - Based on Stab & Gurevych 2017: ~0.70-0.75 F1 for component detection
   - Document baseline performance for our reproduction

**Deliverable**:
- Training script
- Performance metrics table
- Error analysis on 20 examples

**Timeline**: 2-3 days (can complete before Nov 4)

---

### **Experiment 2: Pro vs Con Structural Analysis**
**Goal**: Test Hypothesis 1 by comparing argument structures in essay pairs

**Method**:
1. **Identify Pro/Con Pairs**:
   - Manually verify 10 essay pairs (20 essays total) from the 24 candidates
   - Determine each essay's stance based on major claim

2. **Extract Structural Features**:
   For each essay, compute:
   - **Depth**: Max chain length from major claim to leaf premise
   - **Breadth**: Average number of direct supporters per claim
   - **Attack ratio**: Proportion of attack vs support relations
   - **Evidence density**: Total premises / total claims
   - **Component mix**: Ratio of claims to premises

3. **Statistical Analysis**:
   - Compare pro vs con using paired t-tests (since same topics)
   - Effect size calculations (Cohen's d)
   - Visualizations: Box plots, scatter plots

4. **Qualitative Analysis**:
   - Examine 3 pairs in detail
   - Identify recurring rhetorical patterns

**Deliverable**:
- Statistical comparison table
- Visualization plots
- Qualitative analysis write-up

**Timeline**: 1-2 days (can complete before Nov 4)

---

## Evaluation Strategy

### For Experiment 1 (Component Detection):
- **Metric**: Span-level Precision, Recall, F1 (micro and macro)
- **Baselines**: Compare against Stab & Gurevych 2017 reported results
- **Error Analysis**: Categorize errors (boundary, type, missed components)

### For Experiment 2 (Structural Comparison):
- **Metrics**: Mean, std dev, effect sizes for each structural feature
- **Statistical Tests**: Paired t-tests, Wilcoxon signed-rank (if non-normal)
- **Significance**: p < 0.05 threshold
- **Visualization**: Box plots, distributions

### For Future Work (Not in Midterm):
- **Manual Evaluation**: Annotate 100 IBM arguments for structure validation
- **Cross-Domain**: Test on subset of IBM data
- **Quality Correlation**: Spearman correlation between structure and quality scores

---

## Updated Team Responsibilities

**Aratrik Paul**:
- Literature review updates (if needed based on refined hypotheses)
- Implement Experiment 1 (baseline model)
- Coordinate write-up for midterm report

**Minkush Jain**:
- Complete dataset preparation and statistics
- Implement Experiment 2 (structural analysis)
- Create visualizations and statistical analysis

**Vikramsingh Rathod**:
- Develop evaluation scripts
- Error analysis for both experiments
- Prepare slides/presentation materials

---

## Expected Contributions (Updated)

1. **Empirical Analysis**: First systematic comparison of pro vs con argument structures in persuasive essays

2. **Reproduced Baselines**: Replication of Stab & Gurevych 2017 component detection with documented code

3. **Methodological Framework**: Blueprint for analyzing argument structure differences across stances
   - Can be applied to other domains (social media, news, etc.)
   - Extensible to other structural dimensions

4. **Dataset Documentation**: Comprehensive analysis of available argumentation corpora and their uses

---

## Midterm Deliverables Checklist (Nov 4, 2pm)

- [x] Dataset collection complete
- [ ] Literature review (refined to emphasize stance and structure)
- [ ] Experiment 1: Baseline model results
- [ ] Experiment 2: Pro/Con structural analysis
- [ ] Evaluation metrics defined
- [ ] Preliminary results and discussion
- [ ] Updated project timeline

---

## Why This Project Matters

### Target Audience:
1. **Argument Mining Researchers**: Novel focus on stance-structure relationship
2. **Computational Social Scientists**: Methods for analyzing debate discourse
3. **Educators**: Insights into how stance shapes argumentative writing
4. **NLP Practitioners**: Transfer learning case study for argument mining

### Research Gap:
- Most work focuses on DETECTING arguments or CLASSIFYING stance
- Few studies examine HOW stance affects argumentative STRUCTURE
- Our work bridges argument mining and rhetorical analysis

### Practical Impact:
- **Debate Training**: Teach students how pro/con positions structure differently
- **Argument Quality Systems**: Use structural features for assessment
- **Persuasion Analysis**: Understand what makes arguments effective
- **Automated Debate Systems**: Generate structurally appropriate arguments for given stance

---

## Key Decisions Made:

1. ✅ **Excluded CMV corpus**: No argument annotations, not feasible without manual work
2. ✅ **Primary analysis on essays**: Only dataset with full structure annotations
3. ✅ **Focus on pro/con pairs**: 24 topics provide solid foundation
4. ✅ **Two preliminary experiments**: Both completable before deadline
5. ✅ **IBM data for future work**: Can extend with transfer learning post-midterm

