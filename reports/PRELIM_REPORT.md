## Argument Structure in Online Debates: Data, Hypotheses, and Feasibility (Midterm)

### Datasets (scope and usage)
- Persuasive Essays (Stab & Gurevych, 2017): Fully annotated argumentative structures with component spans (MajorClaim, Claim, Premise) and relations (Support, Attack). We use this as the gold standard for span detection, relation classification, and structural metrics (depth, breadth, density, attack ratio, evidence density).
- IBM Debater ArgKP-2021: Argument–key point pairs with topic and stance. We use “matching” as a support proxy (argument supports key point) and compute stance-partitioned structural proxies (e.g., key point breadth = number of supporting arguments per key point; argument density per topic).
- IBM Debater Argument Quality (30k): Standalone arguments with stance and quality labels. We use an essay-trained component detector to derive structure proxies (component count, premises/claim ratio) and correlate with quality (controlled for length).
- ChangeMyView (CMV) Corpus: Conversation threads without gold argument spans/relations. We use light proxy signals (argumentative sentence detection via transfer, reply-graph heuristics for support/attack direction) for exploratory comparisons only.

### Hypotheses (testable with current data)
- H1 (Primary, Essays): Pro and con positions within the same topic exhibit distinct argument structures. Predictions: con has higher attack ratio; pro has higher evidence density; depth comparable or slightly higher for pro.
- H2 (Transfer): Models trained on essays generalize to short-form arguments. Predictions: span F1 declines on ArgKP excerpts; relation accuracy degrades more than spans; still usable for proxy-level analysis.
- H3 (Quality–Structure): Higher-quality arguments correlate with richer structures. Predictions: positive correlation between quality and structural proxies after controlling for length.

### Annotations and schema
- Unified schema: nodes {MajorClaim, Claim, Premise, KeyPoint}, edges {Support, Attack, Match}. Map ArgKP Match→Support proxy. For CMV/IBM sentences without spans, use sentence-level spans as proxies. For side-aware essay comparisons, we annotate stance at the essay level using a lightweight CSV template.

### Preliminary experiments (feasibility)
- Essays (gold):
  - Span detection: fine-tune a transformer token/sequence tagger; report span P/R/F1 (exact and partial).
  - Relation classification: pairwise classifier for Support/Attack/None; report macro-F1; light constraints to ensure coherent graphs.
  - Structural metrics: depth (longest support chain), breadth (avg supporters per claim), attack ratio, evidence density; stance-partitioned comparisons on paired topics.
- ArgKP-2021:
  - Matching: cross-encoder for argument→key point (match vs non-match); report F1/AUC.
  - Proxies: per-topic stance-partitioned breadth/density (arguments per key point; arguments per topic) to compare rhetorical tendencies.
- Arg Quality 30k:
  - Proxies via transfer: apply essay-trained component detector; compute component count and premises/claim ratio; correlate with quality (Spearman), control for length.
- CMV (exploratory):
  - Argumentative sentence detection via transfer; reply-graph directionality as support/attack proxy; small manual validation for precision.

### Evaluation metrics (minimal, per dataset)
- Essays: span P/R/F1; relation macro-F1; structural differences tested with paired or nonparametric tests and reported with Cohen’s d; visualizations (box plots of attack ratio, evidence density, breadth by stance).
- ArgKP: match F1/AUC; stance-partitioned proxy metrics with bootstrap CIs; permutation tests for differences.
- Arg Quality: Spearman ρ between quality and proxies with bootstrap CIs; partial correlations controlling for length.
- CMV: proxy distributions and small-sample validation accuracy; caveats noted.

### Data handling plan
- Essays: parse BRAT annotations from the provided project archive; derive graphs and metrics; annotate stance via `analysis/aaec/stance_annotation_template.csv` and run paired comparisons.
- ArgKP: load CSV, compute topic/stance summaries, train/evaluate a simple matching classifier for feasibility, and extract breadth/density proxies by stance.
- Quality 30k: compute structure proxies via transferred component detector; run correlation analyses.
- CMV: run exploratory proxy pipeline only; keep excluded from primary evaluation.

### Early findings and feasibility
- Essays exhibit shallow-but-broad structures with predominantly supportive relations. This supports H1’s focus on attack ratio and evidence density as discriminative stance features. Our EDA scripts generate per-essay structural metrics and ArgKP topic/stance summaries, confirming data readiness for the next phase.

### What we will evaluate now
- Primary evaluation concentrates on essays and ArgKP: component/relations + structural comparisons for essays; match classification and stance-partitioned proxies for ArgKP. Additional datasets are documented and integrated via proxies but not the focus of the midterm evaluation.

### Risks and next steps
- Risks: cross-domain degradation, sparse attacks, proxy noise (non-gold spans). Mitigations: effect sizes and CIs; manual sanity checks (50–100 items) for transfer and proxy validity; constraint-based graph cleanup.
- Next steps: finalize stance annotations; run statistical tests and plots; train minimal baselines; report findings; extend to quality correlations and CMV proxies as time allows.



