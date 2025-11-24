# Office Hours Talking Points - Quick Reference

## 🔴 OPENING: Acknowledge the Problems

**"We made critical mistakes in the midterm and want to discuss how to fix them for the final project."**

---

## 📋 KEY ADMISSIONS (Be Direct)

### 1. No Model Was Trained
**Q: "Have you trained a model?"**
**A:** "No. We analyzed gold annotations and mistakenly called it 'experiments.' We computed statistics from BRAT files but never trained a component detection model. We understand this is what you expected for preliminary experiments."

### 2. No P/R/F1 Reported
**Q: "Where are your P/R/F1 scores?"**
**A:** "We don't have them because we never trained a model. The metrics we reported (depth, breadth, attack ratio) were all from gold labels, not model predictions. We incorrectly thought dataset characterization counted as preliminary experiments."

### 3. Confusing Terminology
**Q: "What are 'conservative auto-labels' and figures 1-3?"**
**A:** "That was poor communication on our part. We meant gold BRAT labels but called them 'auto-labels.' The figures were referenced but not actually included in the submission - that was an error."

### 4. Weak Theory Grounding
**Q: "What theory motivates your research question?"**
**A:** "Our literature review focused too much on technical methods (Stab & Gurevych, etc.) and not enough on rhetorical theory about how stance affects structure. We need to add citations about constructive vs critical argumentation from rhetoric literature."

### 5. The Pro/Con Problem (CRITICAL)
**Q: "How do pro/con labels work when topics are phrased differently?"**
**A:** "You're absolutely right this is a problem. Essay 047's topic is 'Zoos should be built...' (argues CON), Essay 173's is 'Zoos have no useful purpose?' (argues PRO). These aren't the same topic with opposite stances - they're different phrasings. Our current 'pro/con' labels don't make sense."

---

## 💡 PROPOSED SOLUTION

### Reframe the Research Question

**OLD (BROKEN):**
"How do pro vs con stances differ in argument structure?"

**NEW (BETTER):**
"How do constructive vs critical argumentative modes differ in structure?"

**Define:**
- **Constructive**: High support ratio, low attacks (building a case)
- **Critical**: High attack ratio (refuting opponent's position)
- **Mixed**: Both construction and refutation

**Why better:**
- ✅ Grounded in rhetoric theory (advocacy vs refutation)
- ✅ Objectively measurable from gold annotations
- ✅ No ambiguous pro/con labeling
- ✅ Still tests interesting structural hypotheses

**ASK:** "Does this reframing make sense as a research direction?"

---

## 🎯 CONCRETE PLAN FOR FINAL PROJECT

### 1. Train Actual Models (Priority #1)
- BERT-base for component detection (span classification)
- Fine-tune on essay train set
- Evaluate on test set with span-level P/R/F1
- Compare to Stab & Gurevych 2017 baseline (~0.70-0.75 F1)
- Include exact hyperparameters, training details

### 2. Fix the Framing
- Classify essays by rhetorical mode using gold annotations
- Compare structural features across modes
- Ground hypotheses in rhetoric literature

### 3. Add Theory
- Cite rhetoric work on advocacy vs refutation (Toulmin, etc.)
- Find prior work on argument structure analysis
- Make clear theoretical predictions

### 4. Report Properly
- All metrics with 95% confidence intervals
- Figures that actually exist in the document
- Statistical significance tests
- Consistent terminology

---

## ❓ QUESTIONS TO ASK

1. **"Is the rhetorical mode reframing (constructive/critical) a better approach than trying to fix the pro/con labeling?"**

2. **"Should we implement BiLSTM-CRF as a baseline first, or is jumping straight to BERT acceptable?"**

3. **"What specific theoretical literature should we be citing to ground this work?"**

4. **"For model evaluation, is span-level F1 sufficient, or do you want token-level metrics too?"**

5. **"Can we use the gold annotations to classify rhetorical modes, or do we need a separate annotation pass?"**

---

## ⏱️ REALISTIC TIMELINE

**Week 1-2:**
- Train component detection model
- Report P/R/F1 with baselines

**Week 3:**
- Classify essays by rhetorical mode
- Rerun structural analysis
- Create proper visualizations

**Week 4:**
- Literature review updates
- Write final report
- Prepare presentation

---

## 🚫 WHAT NOT TO DO

❌ Make excuses about time
❌ Defend the midterm submission
❌ Be vague about fixes
❌ Blame the previous Claude assistant

✅ Take responsibility
✅ Show you understand requirements
✅ Have specific, concrete plan
✅ Ask for guidance on approach

---

## 💬 SAMPLE OPENING

"Thank you for meeting with us. We received your feedback on the midterm and we understand we made serious mistakes. Specifically:

1. We didn't train any models - we only analyzed existing gold annotations
2. We used confusing terminology and referenced figures that don't exist
3. Our pro/con framing has the fundamental problem you identified
4. Our literature review lacks theoretical grounding

We take full responsibility and want to discuss the best path forward for the final project. We're proposing to reframe the research question around constructive vs critical argumentative modes rather than ambiguous pro/con labels. Can we walk through this approach with you?"

---

## 📊 WHAT SUCCESS LOOKS LIKE (Final Project)

1. ✅ Trained model with documented architecture
2. ✅ Actual P/R/F1 scores on test set predictions
3. ✅ Comparison to published baselines
4. ✅ Clear research question grounded in theory
5. ✅ All figures included with confidence intervals
6. ✅ Consistent terminology throughout
7. ✅ Proper statistical testing
8. ✅ Honest discussion of limitations

---

**Key Message:** We made fundamental errors but now understand the requirements and have a concrete plan to deliver actual experiments with trained models for the final submission.
