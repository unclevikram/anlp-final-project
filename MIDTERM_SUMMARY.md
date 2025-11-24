# Midterm Report Summary: Argument Structure Analysis
**Team**: Aratrik Paul, Minkush Jain, Vikramsingh Rathod
**Project**: Argument Structure in Online Debates
**Date**: November 4, 2025

---

## Executive Summary

After comprehensive dataset analysis, we have refined our project scope to focus on **comparing argument structures between pro and con stances in persuasive essays**. We propose three testable hypotheses and have completed preliminary experiments that demonstrate project feasibility.

### Key Accomplishment: ✅ All Data Collected and Analyzed

We have thoroughly analyzed all available datasets and determined which are suitable for our research questions.

---

## 1. Data Collection (COMPLETE ✅)

### Datasets Acquired:

#### **1. Persuasive Essays (Stab & Gurevych 2017)** - PRIMARY DATASET
- **402 essays** with complete argument structure annotations
- **Annotations include**:
  - MajorClaims, Claims, Premises (component types)
  - Support and Attack relations between components
- **24 topics with exactly 2 essays** (potential pro/con pairs)
- **27 topics total** with multiple essays
- **Train/test split provided**
- **Status**: ✅ Fully annotated, ready for use

**Why this matters**: This is the ONLY dataset with full argument structure annotations, making it our gold standard for analysis.

#### **2. IBM Debater ArgKP-2021** - SECONDARY DATASET
- **27,519 argument-keypoint pairs** across 31 topics
- **Has**: PRO/CON stance labels
- **Does NOT have**: Argument structure annotations
- **Use case**: Future work on transfer learning

#### **3. IBM Debater Argument Quality** - SECONDARY DATASET
- **30,497 arguments** across 71 topics
- **Has**: PRO/CON stance labels, quality scores, train/dev/test splits
- **Does NOT have**: Argument structure annotations
- **28 topics overlap** with ArgKP dataset
- **Use case**: Test Hypothesis 3 (quality-structure correlation)

#### **4. ChangeMyView (CMV) Corpus** - EXCLUDED
- Contains conversation structure but **NO argument annotations**
- **Decision**: Excluded from project scope (would require extensive manual annotation)

### Dataset Analysis Results:

**Essay Topic Coverage**:
- 3 topics with 3 essays each (universities, zoos, etc.)
- 24 topics with exactly 2 essays (best for pro/con analysis)
- 372 unique topics total
- Topics include: education, technology, social policy, environment

**Example Pro/Con Pairs Found**:
1. Essays 047 & 173: Zoos (CON: "animals should live in natural habitats" vs PRO: "zoos are very useful")
2. Essays 080 & 194: Animal captivity
3. Essays 003 & 004: International tourism
4. Essays 014 & 136: Learning from teachers vs other sources
5. Essays 037 & 137: International sporting events

---

## 2. Refined Hypotheses

### **Hypothesis 1: Structural Differences Between Pro and Con Stances** ⭐ PRIMARY FOCUS

**Research Question**: Do pro-stance and con-stance arguments exhibit systematically different structural patterns?

**Specific Predictions**:
- **H1a**: Pro essays have deeper support chains (more premises per claim)
- **H1b**: Con essays have more attack relations (refuting opposing views)
- **H1c**: Evidence density differs between pro and con stances

**Why This Matters**:
- **Novel contribution**: Few studies compare how stance affects argument structure
- **Practical impact**: Informs debate training, writing instruction, automated assessment
- **Target audience**: Argumentation researchers, educators, computational linguists

**Feasibility**: ✅ HIGH - Can test using 24 essay pairs with gold annotations

---

### **Hypothesis 2: Cross-Domain Generalization**

**Research Question**: Can models trained on essays detect argument components in short-form arguments?

**Testable With**: Train on essays, apply to IBM arguments

**Feasibility**: ✅ MODERATE - Needs manual evaluation sample

---

### **Hypothesis 3: Quality-Structure Correlation**

**Research Question**: Do higher-quality arguments have richer structures?

**Testable With**: Extract structures from IBM Quality dataset, correlate with scores

**Feasibility**: ⚠️ LOWER - Requires training model first (future work)

---

## 3. Preliminary Experiments

### **Experiment 1: Dataset Characterization** ✅ COMPLETE

**What We Did**:
- Analyzed all 402 essays for argument structure patterns
- Computed structural metrics across entire dataset
- Identified pro/con essay pairs

**Key Findings**:
```
ARGUMENT STRUCTURE CHARACTERISTICS (Dataset-wide):
- Average depth: 1.00 levels (mostly flat, single-level support)
- Average breadth: 1.41 supporters per claim
- Attack ratio: 0.057 (5.7% of relations are attacks)
- Evidence density: 1.75 premises per claim

COMPONENT DISTRIBUTION:
- Average major claims per essay: 1.87
- Average claims per essay: 3.75
- Average premises per essay: 9.53

RELATION PATTERNS:
- Support relations: avg 8.99 per essay
- Attack relations: avg 0.55 per essay
- Persuasive essays are predominantly supportive (not adversarial)
```

**Implications**:
- Essays build positive cases rather than attacking opponents
- Most arguments are shallow (depth=1) but broad (multiple parallel supports)
- Attack relations are rare, making them interesting when they do appear

**Files Generated**:
- `essay_analysis_results.json`: Complete dataset statistics
- `structural_analysis_results.json`: Per-essay structural features

---

### **Experiment 2: Pro vs Con Comparison Framework** ✅ DESIGNED

**What We Built**:
- Automated structural feature extraction from BRAT annotations
- Feature set for comparing essay structures:
  - **Depth**: Maximum chain length from major claim to premises
  - **Breadth**: Average supporters per claim
  - **Attack ratio**: Proportion of attack vs support relations
  - **Evidence density**: Premises per claim
  - **Component mix**: Distribution of claims vs premises

**Implementation**:
- `experiment2_structural_analysis.py`: Interactive stance annotation + analysis
- `experiment2_auto_analysis.py`: Automated analysis of all essays

**Next Steps** (Post-Midterm):
1. Manually annotate stance for 24 essay pairs (PRO vs CON)
2. Run statistical comparisons (paired t-tests, effect sizes)
3. Create visualizations (box plots, distributions)
4. Qualitative analysis of interesting cases

**Status**: Framework complete, ready for stance annotation phase

---

## 4. Evaluation Strategy

### For Structural Analysis (Hypothesis 1):
- **Metrics**: Mean, standard deviation, effect size (Cohen's d)
- **Statistical Tests**: Paired t-tests (same topics, different stances)
- **Significance Level**: p < 0.05
- **Visualization**: Box plots, scatter plots, heat maps

### For Component Detection (Hypothesis 2 - Future):
- **Metrics**: Span-level Precision, Recall, F1
- **Baseline**: Stab & Gurevych 2017 reported ~0.70-0.75 F1
- **Error Analysis**: Boundary errors, type confusion, missed components

### For Quality Correlation (Hypothesis 3 - Future):
- **Metrics**: Spearman correlation coefficient
- **Controls**: Stance, topic, argument length

---

## 5. Literature Review Updates Needed

Based on instructor feedback and our refined focus, we need to emphasize:

### **Add Section: Stance and Argument Structure**
- How stance affects rhetorical strategy (pro = constructive, con = critical?)
- Existing work on argument structure analysis
- Gap: Most work focuses on detection OR stance classification, not their interaction

### **Strengthen Motivation Section**:
**Who cares about this?**
1. **Computational Argumentation Researchers**: Novel empirical study of stance-structure relationship
2. **Debate Coaches & Writing Instructors**: Evidence-based insights into how to structure arguments by stance
3. **NLP Practitioners**: Transfer learning case study for low-resource argument mining
4. **Social Scientists**: Methods for analyzing argumentative discourse

**Why does it matter?**
- Understanding stance-structure patterns can improve:
  - Automated argument generation systems
  - Argument quality assessment
  - Debate strategy teaching
  - Persuasion analysis in social media

### **Update Related Work**:
- Keep technical methods (Levy et al., Rinott et al., Stab & Gurevych)
- Add: Work on stance detection and its applications
- Add: Rhetorical structure analysis (beyond argument mining)
- Frame our gap: "While stance detection and argument mining have advanced separately, few studies examine how stance shapes argumentative structure"

---

## 6. Addressing Instructor Feedback

### **Original Feedback**:
> "you will need to do much more to motivate this as a research question that people want to know the answer to. What specific hypotheses are you starting out trying to test (and what community cares about it)?"

### **Our Response**:

**Specific Hypothesis**: Pro-stance essays have fundamentally different argument structures than con-stance essays on the same topics.

**Who Cares**:
1. **Argumentation Mining Community**: This is a novel empirical question not addressed in prior work
2. **Computational Social Science**: Methods for analyzing how people argue across different positions
3. **Education Research**: Insights for teaching argumentation and persuasive writing
4. **Practical NLP**: Improves argument generation, quality assessment, and debate systems

**Why It's Important**:
- **Scientific**: Tests theoretical claims about rhetoric (construction vs. refutation)
- **Practical**: Informs how to build, teach, and evaluate arguments
- **Methodological**: Demonstrates value of structural analysis beyond component detection

---

## 7. Expected Contributions

### **1. Empirical Findings** (Novel)
- First systematic comparison of pro vs con argument structures in persuasive essays
- Quantitative evidence for/against rhetorical theories about stance and structure

### **2. Methodological Framework** (Reusable)
- Feature set for comparing argument structures
- Analysis pipeline for stance-aware structural analysis
- Can be applied to other domains (social media, news, legal arguments)

### **3. Reproduced Baseline** (Contribution to Science)
- Replication of Stab & Gurevych 2017 with documented code
- Serves as foundation for future work

### **4. Dataset Documentation** (Resource)
- Comprehensive analysis of available argumentation corpora
- Guidance on which datasets suit which research questions

---

## 8. Team Responsibilities (Updated)

**Aratrik Paul** (Literature & Modeling Lead):
- Refine literature review with stance-structure emphasis
- (Post-midterm) Implement baseline component detection model
- Coordinate report writing

**Minkush Jain** (Data & Analysis Lead):
- Complete stance annotation for essay pairs
- Run statistical analyses for Hypothesis 1
- Create visualizations

**Vikramsingh Rathod** (Experiments & Evaluation Lead):
- Develop evaluation framework
- Error analysis and interpretation
- Presentation materials

---

## 9. Timeline

### ✅ **Completed (Before Nov 4)**:
- Dataset collection and analysis
- Hypothesis formulation
- Preliminary experiment 1 (dataset characterization)
- Experiment 2 framework implementation
- Project plan refinement

### **Week of Nov 4-10** (Post-Midterm):
- Manual stance annotation (24 pairs = ~2-3 hours)
- Statistical analysis and visualization
- Literature review updates
- Begin baseline model implementation

### **Week of Nov 11-17**:
- Complete baseline model
- Cross-domain experiments
- Error analysis

### **Week of Nov 18-24**:
- Quality correlation analysis
- Final experiments and ablations
- Draft final report

### **Week of Nov 25 - Dec 4**:
- Final report writing
- Presentation preparation
- Submission

---

## 10. Files Delivered

### Analysis Scripts:
- `analyze_essay_prompts.py`: Essay dataset analysis
- `analyze_ibm_datasets.py`: IBM dataset analysis
- `experiment2_auto_analysis.py`: Automated structural analysis
- `experiment2_structural_analysis.py`: Interactive pro/con analysis

### Results Files:
- `essay_analysis_results.json`: Essay statistics and pairs
- `structural_analysis_results.json`: Per-essay structural features

### Documentation:
- `PROJECT_PLAN.md`: Comprehensive project plan with hypotheses
- `MIDTERM_SUMMARY.md`: This document

### Data:
- All datasets in `dataset/` directory
- BRAT annotations extracted and ready to use

---

## 11. Key Decisions & Rationale

| Decision | Rationale |
|----------|-----------|
| **Exclude CMV corpus** | No argument annotations; manual annotation not feasible in timeline |
| **Focus on essay dataset** | Only data with complete structure annotations |
| **24 pro/con pairs** | Sufficient for statistical analysis, manageable for manual verification |
| **Hypothesis 1 as primary** | Most feasible, most novel, most impactful |
| **Hypotheses 2 & 3 as secondary** | Interesting but require more time/resources |
| **Manual stance annotation** | Necessary step; only ~2 hours of work for 24 pairs |

---

## 12. Feasibility Demonstration

### **Evidence That Our Project Is Feasible**:

✅ **Data**: We have high-quality annotated data
✅ **Tools**: Analysis scripts working and producing results
✅ **Baseline**: Can reproduce existing work (Stab & Gurevych 2017)
✅ **Hypothesis**: Testable with available data
✅ **Timeline**: Realistic schedule with clear milestones
✅ **Team**: Clear division of labor

### **Risks & Mitigation**:

| Risk | Mitigation |
|------|------------|
| Stance annotation errors | Double-check by reading full essays, not just claims |
| Small sample size (24 pairs) | Use effect sizes, not just p-values; qualitative analysis |
| No pro/con differences found | Still scientifically valuable null result |
| Cross-domain transfer fails | Focus on Hypothesis 1; transfer is stretch goal |

---

## 13. Preliminary Results

From automated analysis of all 402 essays:

### **Structural Patterns**:
- Essays have **shallow but broad** structures
- **5.7% attack relations** - mostly cooperative argumentation
- **Average 1.75 premises per claim** - moderate evidence density
- **Average 1.41 supporters per claim** - some parallel reasoning

### **Implications for Hypothesis 1**:
Given low attack baseline (5.7%), even small differences between pro/con could be significant. We predict:
- Con essays: Higher attack ratio (refuting opposing view)
- Pro essays: Higher evidence density (building positive case)
- Both: Similar depth (constrained by essay format)

**Testable in next phase with stance-annotated pairs.**

---

## 14. Summary

We have successfully:
1. ✅ Collected and analyzed all relevant datasets
2. ✅ Formulated three testable hypotheses grounded in available data
3. ✅ Completed preliminary structural analysis showing dataset characteristics
4. ✅ Built analysis framework for pro/con comparison
5. ✅ Identified 24 essay pairs for stance-based comparison
6. ✅ Defined clear evaluation strategy
7. ✅ Established feasibility through working code and preliminary results

**Next steps**: Stance annotation → Statistical testing → Visualization → Literature review updates → Final report

**Bottom line**: The project is feasible, well-scoped, and positioned to make a novel contribution to argument mining research.

---

## References for Midterm

1. Stab, C., & Gurevych, I. (2017). Parsing argumentation structures in persuasive essays. *Computational Linguistics*, 43(3), 619–659.

2. Levy, R., et al. (2014). Context dependent claim detection. *Proceedings of COLING 2014*.

3. Rinott, R., et al. (2015). Show me your evidence – An automatic method for context dependent evidence detection. *Proceedings of EMNLP 2015*.

4. Lawrence, J., & Reed, C. (2019). Argument mining: A survey. *Computational Linguistics*, 45(4), 765–818.

5. Park, J., & Cardie, C. (2018). A corpus of eRulemaking user comments for measuring evaluability of arguments. *Proceedings of LREC 2018*.

---

**For questions or clarifications, contact the team members.**
