## Midterm Analysis Update: Argument Structure and Early Feasibility

### Scope and datasets
We analyze four datasets for argument structure and stance-aware patterns: (1) Persuasive Essays (gold component spans and support/attack relations); (2) IBM ArgKP-2021 (argument–key point pairs with stance, matching labels); (3) IBM Argument Quality 30k (argument-level stance and quality); and (4) CMV (conversational threads, no gold structure). For midterm evaluation, we focus on essays (gold) and ArgKP (feasibility + stance-partitioned proxies), while documenting the others.

### Hypotheses (testable now)
- H1 (Primary): Pro vs. con positions differ structurally (attack ratio, evidence density, breadth, depth) within topics.
- H2 (Transfer): Essay-trained models can support proxy extraction in short-form arguments (ArgKP/CMV).
- H3 (Quality–Structure): Structural richness correlates with argument quality (future extension).

### Methods and recent fixes
- Graph metrics from gold BRAT: We corrected breadth and depth definitions to follow BRAT edge semantics (supports are Premise→Claim). Breadth now counts incoming support edges to claims; depth follows chains of incoming support into claims/major claims. This resolves the earlier “flat breadth” artifact and produces meaningful differences by stance.
- Stance labeling (essays): We auto-labeled stance using both essay body and claim texts, with heuristics for agree/disagree, should/should not, positive/negative trend, allow/ban, good/bad idea, and advantages-vs-disadvantages patterns. Ambiguous cases remain blank to preserve precision; we’ll complete these with a brief manual pass.
- ArgKP baseline: A minimal Jaccard-similarity matcher provides a sanity benchmark for argument→key point matching; it shows high recall and low precision, motivating a learned cross-encoder next.

### Results (current, evolving as stances finalize)
- AAEC stance comparison (n_topics currently small due to conservative auto-labeling):
  - Attack ratio: pro < con (difference ~ −0.02), consistent with con essays using more refutation.
  - Evidence density: pro > con (difference ~ +0.42), consistent with pro building positive cases.
  - Breadth (supporters per claim): pro > con (difference ~ +0.36) after fixing edge direction.
  - Depth: similar, small swings by topic (essays are mostly shallow).
  - Figures: `reports/figures/aaec_attack_ratio.png`, `aaec_evidence_density.png`, `aaec_avg_breadth.png`.
- ArgKP minimal baseline (5k pairs split 80/20): F1 ≈ 0.356 (precision ≈ 0.23, recall ≈ 0.79). This establishes feasibility and a clear headroom for cross-encoders.

### Why some results were unexpected and how we fixed them
- Average breadth initially plotted as near zero because we counted support edges as Claim→Premise (outgoing). BRAT encodes Supports as Premise→Claim; switching to incoming supports at claims corrected this and revealed stance differences.
- Sparse attack edges can mute stance effects; we quantify with effect sizes and plan topic-paired tests to increase sensitivity.
- Auto-labeling is intentionally conservative to avoid bias; expanding heuristics and a 10–15 minute manual pass will raise coverage and stabilize estimates.

### Next improvements (methods we will use)
- Essay models: fine-tuned transformer for component spans; pairwise transformer for relations; light constraints to ensure coherent graphs. This strengthens H1 and enables transfer to ArgKP/CMV for proxies.
- ArgKP: replace Jaccard with a cross-encoder (e.g., RoBERTa) for matching; then compute stance-partitioned breadth/density proxies per topic/key point.
- Robust stats: paired tests within topics, bootstrap CIs, and effect sizes to handle small n and skewed distributions.
- Quality correlation (Arg 30k): derive structure proxies with the essay model and test quality–structure associations controlling for length.

### Plan and expected outcomes
- Finalize stances: complete auto-label coverage, then quickly verify ambiguous rows manually.
- Recompute AAEC comparisons and figures with full topics; report per-topic diffs and overall effect sizes.
- Train minimal learned baselines (essay spans/relations; ArgKP cross-encoder); add one table per dataset and 2–3 plots.
- Document error modes (boundary errors, relation confusion, proxy noise) and show how improved models reduce them.

Together, these steps address feasibility, explain current limitations, and commit to stronger methods that should yield clearer, more reliable stance–structure findings across datasets.


