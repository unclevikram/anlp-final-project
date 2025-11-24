# CRITICAL ANALYSIS: What Went Wrong & How to Answer Office Hours Questions

**Prepared for: Office Hours Meeting**
**Date: November 2024**

---

## 🚨 THE CORE PROBLEM

**YOU SUBMITTED DATASET EXPLORATION AND CALLED IT "EXPERIMENTS"**

The instructor is right to be confused because:
1. **NO MODEL WAS TRAINED** - Not BiLSTM, not BERT, nothing
2. **NO P/R/F1 SCORES REPORTED** - Because there's no model to evaluate
3. **"PRELIMINARY EXPERIMENTS"** were just parsing gold annotations and computing statistics

### What You Actually Delivered:
- ✅ Dataset statistics scripts
- ✅ Code to parse BRAT annotations
- ✅ Gold-label based analysis
- ❌ NO MODEL TRAINING
- ❌ NO MODEL EVALUATION
- ❌ NO PREDICTIONS
- ❌ NO COMPARISON TO BASELINES

---

## 📊 SPECIFIC FEEDBACK ITEMS - HOW TO RESPOND

### Issue #1: "have you trained a model to recognize the argument components?"

**HONEST ANSWER FOR OFFICE HOURS:**
> "No, we have not trained a model yet. We misunderstood the midterm requirements. Our 'Experiment 1' was actually just dataset analysis using the gold annotations from BRAT files. We computed statistics like average depth and breadth, but these were from gold labels, not model predictions. We now understand we need to actually train a component detection model (BiLSTM-CRF or BERT-based) and report P/R/F1 scores."

**WHY THIS HAPPENED:**
- Confused "analyzing existing annotations" with "running experiments"
- Thought dataset characterization counted as a preliminary experiment
- Misread the requirement - midterm needed actual model training

---

### Issue #2: "Nowhere here do you describe a model... or report P/R/F1"

**HONEST ANSWER:**
> "You're absolutely right. We stated we would 'evaluate component spans by P/R/F1' but we never actually trained a model to generate predictions. The metrics we reported (depth, breadth, attack ratio) were all computed from gold annotations, not from any model output. This was a critical oversight."

**THE MISMATCH:**
- **Said**: "Following precedent, we evaluate component spans by P/R/F1"
- **Did**: Computed statistics from gold labels
- **Should have done**: Trained a tagger, ran it on test set, reported actual P/R/F1

---

### Issue #3: "What's a 'conservative auto-label'? What exactly is the data being visualized in figs 1-3?"

**HONEST ANSWER:**
> "We apologize for the confusion. The term 'conservative auto-label' was used incorrectly - we were referring to gold labels from the BRAT annotations, not automatically predicted labels. Regarding figures 1-3, we don't actually have these figures in our submitted report. This appears to be a documentation error where we referenced visualizations we planned to create but didn't include in the submission."

**THE PROBLEM:**
- Used confusing terminology
- Referenced figures that don't exist
- Tried to sound sophisticated but ended up being unclear

---

### Issue #4: "none of the metrics... have confidence intervals!"

**HONEST ANSWER:**
> "You're correct. We reported mean statistics across essays but didn't include confidence intervals or standard errors. For the final project, we will include bootstrapped confidence intervals for all structural metrics and report statistical significance with proper confidence bounds."

**WHAT TO DO FOR FINAL:**
- When reporting means, always include 95% CI
- Use bootstrap or t-distribution for small samples
- Report: "Mean depth: 1.75 (95% CI: [1.62, 1.88])"

---

### Issue #5: "this work really needs to be grounded in some theoretical literature"

**HONEST ANSWER:**
> "We agree our literature review is too focused on technical methods and doesn't ground the research question in theory. We cited Stab & Gurevych, Levy et al., etc. for argument mining techniques, but we haven't cited work that:
> 1. Theorizes about how stance affects argumentative structure
> 2. Studies rhetorical differences between advocacy and refutation
> 3. Provides a theoretical framework for why pro/con arguments might differ

> We will revise the related work to include theories from rhetoric and argumentation studies that motivate our hypotheses."

**WHAT'S MISSING:**
- Rhetorical theory about constructive vs. critical arguments
- Prior empirical studies on stance and structure (if any exist)
- Clear theoretical predictions, not just "we expect differences"

---

### Issue #6: "What specific model are you training?"

**HONEST ANSWER:**
> "Our proposal mentioned BiLSTM-CRF and BERT models, but we haven't implemented either yet. For the final project, we will:
> 1. **Baseline**: BiLSTM-CRF sequence tagger with word embeddings for token-level BIO tagging
> 2. **Main model**: Fine-tuned BERT-base for span classification
> 3. **Relation classification**: Sentence-pair cross-encoder for support/attack classification
>
> We will report exact architectures, hyperparameters, and training procedures."

**BE SPECIFIC:**
- Don't say "transformer models" - say "BERT-base-uncased, 12 layers, 768 hidden"
- Don't say "baseline" - say "BiLSTM (256 hidden) + CRF with GloVe 300d embeddings"
- Include training details: optimizer, learning rate, epochs, batch size

---

### Issue #7: "What is a minimal lexical baseline... what is the task... why AP as a metric?"

**HONEST ANSWER:**
> "This reference to 'minimal lexical baseline with Jaccard similarity and AP=0.36' was confusing because:
> 1. It refers to the ArgKP dataset's key-point matching task, not our main task
> 2. We mentioned it to show we explored the IBM data, but it's not directly relevant
> 3. We should not have mixed metrics (AP for ArgKP vs P/R/F1 for component detection)
>
> For our actual task (component detection), we will use span-level P/R/F1 as stated in our evaluation section, not AP."

**THE CONFUSION:**
- Mixed up different tasks (key-point matching vs component detection)
- Mentioned ArgKP experiments that weren't central to the project
- Inconsistent metrics across different parts of the report

---

### Issue #8: "'Few studies' - are you able to cite some?"

**HONEST ANSWER:**
> "We claimed 'few studies' examine stance-structure relationships but didn't cite any. This was sloppy. We need to either:
> 1. Find and cite the actual 'few studies' that exist, or
> 2. Change our claim to 'To our knowledge, no prior work has systematically compared...'
>
> We will conduct a more thorough literature search for work on stance and argument structure."

**ACTION ITEMS:**
- Search: "stance argument structure"
- Search: "pro con argumentation patterns"
- Search: "advocacy refutation rhetoric"
- If nothing exists, say so explicitly
- If it does exist, cite it and differentiate your work

---

### Issue #9: THE FUNDAMENTAL PRO/CON PROBLEM 🚨

**THIS IS THE BIGGEST CONCEPTUAL ISSUE:**

**HONEST ANSWER:**
> "You've identified a critical flaw in our project design. Our essay dataset has a problem:
> - Essay 047: Topic is 'Zoos should be built to protect rural animals' - argues AGAINST
> - Essay 173: Topic is 'Zoos have no useful purpose?' - argues FOR zoos
>
> These are DIFFERENT topic phrasings, not the same topic with opposite stances. The 'pro' and 'con' labels are ambiguous because:
> - Pro on 'X should be banned' = Con on 'X should be allowed'
> - The essay prompts themselves frame the debate differently
>
> **Our revised approach:**
> We need to either:
> 1. Manually create a unified topic schema and re-label all essays consistently, OR
> 2. Change our research question to compare different RHETORICAL MODES:
>    - Essays that primarily BUILD a case (constructive)
>    - Essays that primarily REFUTE a position (critical)
>    - Essays that DO BOTH
>
> Option 2 is more feasible and actually more interesting theoretically."

**WHY THIS IS CRITICAL:**
- Your entire Hypothesis 1 depends on meaningful pro/con labels
- The current "pro/con" assignments are inconsistent
- Need to reframe the research question

---

## 💡 PROPOSED FIX FOR FINAL PROJECT

### New Research Direction (More Defensible):

**OLD (FLAWED) RQ:**
"How do pro vs con stances differ in argument structure?"

**NEW (BETTER) RQ:**
"How do different rhetorical modes (constructive, critical, mixed) differ in argument structure?"

**Why this is better:**
1. **Constructive arguments**: Build a positive case with evidence
2. **Critical arguments**: Refute an opposing view with counterarguments
3. **Mixed arguments**: Do both

You can identify these by:
- High support ratio, low attack ratio = Constructive
- High attack ratio = Critical
- Both = Mixed

This is:
- ✅ Theoretically grounded (rhetoric literature on advocacy vs refutation)
- ✅ Objectively measurable from gold annotations
- ✅ Doesn't rely on ambiguous pro/con labels
- ✅ Still tests interesting hypothesis about structure

---

## 🎯 WHAT YOU MUST DO FOR FINAL PROJECT

### Priority 1: TRAIN A MODEL (URGENT)
```
MUST HAVE:
1. Component detection model (BERT-based is fine)
2. Actual training code with documented hyperparameters
3. Evaluation on test set with P/R/F1 scores
4. Comparison to Stab & Gurevych 2017 baseline numbers
5. Error analysis with examples
```

### Priority 2: FIX THE PRO/CON PROBLEM
```
CHOOSE ONE:
A) Reframe as rhetorical mode analysis (constructive/critical)
   - Easier, more defensible
   - Can use gold annotations to classify
   - Grounded in rhetoric theory

B) Manual stance annotation with clear schema
   - More work
   - Need to define topics consistently
   - Harder to defend theoretically
```

### Priority 3: GROUND IN THEORY
```
ADD TO LITERATURE REVIEW:
- Rhetoric literature on advocacy vs refutation
- Toulmin's model of argumentation
- Prior work on argument structure analysis
- Theories about evidence use and counterarguments
```

### Priority 4: REPORT ACTUAL RESULTS
```
FOR EVERY CLAIM, INCLUDE:
- Exact model architecture and hyperparameters
- Training procedure (optimizer, learning rate, epochs)
- Results table with confidence intervals
- Statistical tests (t-test, effect size)
- Figures that actually exist in the document
```

---

## 📝 FOR OFFICE HOURS: KEY TALKING POINTS

### 1. Acknowledge the Problems

**SAY THIS:**
> "We made critical errors in the midterm:
> 1. We didn't train any models - we only analyzed gold annotations
> 2. We used confusing terminology ('conservative auto-labels')
> 3. We didn't include the figures we referenced
> 4. Our pro/con framing has fundamental issues you correctly identified
> 5. Our literature review lacks theoretical grounding
>
> We take full responsibility and want to correct course for the final project."

### 2. Show You Understand the Real Requirements

**SAY THIS:**
> "We now understand that 'preliminary experiments' means:
> - Training actual models
> - Reporting P/R/F1 on predictions (not gold labels)
> - Comparing to baselines with real numbers
> - Including confidence intervals
>
> Not just computing statistics from existing annotations."

### 3. Propose Concrete Fixes

**SAY THIS:**
> "For the final project, we will:
> 1. **Train a BERT-based component detection model** - we'll document the full architecture and training procedure
> 2. **Reframe the research question** - Instead of ambiguous 'pro vs con', we'll study constructive vs critical vs mixed argumentative modes
> 3. **Ground in rhetoric theory** - We'll cite work on advocacy and refutation from argumentation studies
> 4. **Report actual model performance** - P/R/F1 with confidence intervals, comparison to Stab & Gurevych baseline
> 5. **Include all referenced figures** - With proper confidence intervals
>
> Can we discuss whether the new rhetorical mode framing makes sense?"

### 4. Ask for Guidance

**ASK:**
> "Given the issues with pro/con labeling you identified, would you recommend:
> A) Reframing as rhetorical mode analysis (constructive/critical), or
> B) Doing manual stance annotation with a clear unified topic schema, or
> C) A different approach entirely?"

> "For the model training, is BERT-base sufficient, or should we implement the BiLSTM-CRF baseline first?"

> "What specific theoretical literature should we be citing to ground the research question?"

---

## ⚠️ WHAT NOT TO SAY

### DON'T Make Excuses
❌ "We ran out of time"
❌ "We misunderstood the requirements"
❌ "The previous Claude Code told us this was fine"

### DON'T Defend the Flawed Work
❌ "Our dataset analysis was still valuable"
❌ "We can just add model training later"
❌ "The pro/con labels make sense if you look at it this way..."

### DON'T Be Vague
❌ "We'll train some models for the final"
❌ "We'll add more theory to the lit review"
❌ "We'll fix the pro/con issue somehow"

### DO Be Specific
✅ "We'll train BERT-base with these exact hyperparameters..."
✅ "We'll reframe as rhetorical mode analysis using this definition..."
✅ "We'll cite these specific rhetoric papers that theorize about..."

---

## 📚 IMMEDIATE ACTION ITEMS (Before Final Project)

### Week 1: Model Training
- [ ] Implement BERT-based component detection
- [ ] Train on essay dataset train split
- [ ] Evaluate on test split
- [ ] Report P/R/F1 with confidence intervals
- [ ] Compare to Stab & Gurevych 2017 numbers

### Week 2: Reframe Analysis
- [ ] Read rhetoric literature on constructive vs critical arguments
- [ ] Classify essays by rhetorical mode (using gold annotations)
- [ ] Rerun structural analysis with new framing
- [ ] Create figures with confidence intervals

### Week 3: Literature Review
- [ ] Find and cite theoretical work on argument structure
- [ ] Find and cite work on advocacy vs refutation
- [ ] Explicitly state your theoretical predictions
- [ ] Ground hypotheses in cited theory

### Week 4: Write-up
- [ ] Clear methods section with exact model details
- [ ] Results section with all figures included
- [ ] Confidence intervals on all metrics
- [ ] Discussion of theoretical implications

---

## 🎓 LEARNING POINTS

### What "Experiments" Actually Means in ML:
1. **Train** a model on training data
2. **Predict** on test data
3. **Evaluate** predictions against gold labels
4. **Report** metrics (P/R/F1) on those predictions
5. **Compare** to baselines

### What "Experiments" Does NOT Mean:
- Computing statistics from gold labels
- Analyzing existing annotations
- Exploring datasets
- Creating frameworks for future analysis

### Remember:
> **Gold labels are not predictions**
> **Dataset exploration is not model evaluation**
> **Planning to do something is not doing it**

---

## BOTTOM LINE FOR OFFICE HOURS

**BE HONEST:**
"We submitted dataset analysis and mistakenly called it experiments. We didn't train any models. We understand this is a serious problem and we're committed to doing real experiments for the final project."

**BE SPECIFIC:**
"We will train a BERT-based component detector, evaluate it properly, and reframe our analysis around rhetorical modes instead of ambiguous pro/con labels."

**BE PROACTIVE:**
"We're asking for your guidance on the best way to fix the pro/con labeling issue and which theoretical literature we should be grounding this in."

**BE REALISTIC:**
"We now understand the scope of work required and have a concrete plan to deliver actual experiments with trained models for the final submission."

---

**Good luck in office hours. Be honest, take responsibility, and show you have a concrete plan forward.**
