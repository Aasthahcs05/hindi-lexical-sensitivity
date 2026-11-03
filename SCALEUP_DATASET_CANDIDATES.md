# SCALE-UP DATASET CANDIDATES: MASTER SPECIFICATION AND SELECTION GUIDE

**Project Title:** Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi  
**Phase:** Phase 2 — Final Dataset Adjudication and Scale-Up Readiness  
**Auditor:** Antigravity Research Assistant (Independent Verification Mode)  
**Date:** November 2026  

---

## Executive Summary

To support rigorous, publication-grade experimentation while preserving the integrity of the original benchmark, **six distinct candidate datasets** have been prepared, exported, and cryptographically verified. 

All candidate files are stored in [`data/scaleup_candidates/`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates). Each dataset preserves the original 18-column schema, stable `pair_id` identifiers, and UTF-8 encoding.

---

## Master Candidate Specification Table

| Candidate Identifier | File Name | Total Pairs ($N$) | Track Breakdown (Spelling / Synonym / Context) | Defining Scientific Property | Recommended Experimental Role |
|---|---|---|---|---|---|
| **Candidate 1** | [`scaleup_candidate_1_strict_accepted.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_1_strict_accepted.csv) | **1,676** | **1,005** / **362** / **309** | **Strict Minimal Pairs:** Excludes templates, multi-word rewrites, and flawed rows. Pristine Devanagari danda punctuation. | **PRIMARY BENCHMARK** (Main paper submission) |
| **Candidate 2** | [`scaleup_candidate_2_accepted_with_templates.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_2_accepted_with_templates.csv) | **1,954** | **1,259** / **386** / **309** | **Maximal Scale:** Includes the 278 template carrier sentences. 97.7% of raw dataset. | **SENSITIVITY ANALYSIS** (Appendix / Robustness) |
| **Candidate 3** | [`scaleup_candidate_3_accepted_excluding_templates.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_3_accepted_excluding_templates.csv) | **1,676** | **1,005** / **362** / **309** | **Syntactic Diversity:** Guaranteed zero template clustering; identical to Candidate 1. | **CONFIRMATORY BENCHMARK** |
| **Candidate 4** | [`scaleup_candidate_4_multiword_agreement.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_4_multiword_agreement.csv) | **12** | **1** / **8** / **3** | **Grammatical Concord Shifts:** Contains the 8 gender-agreement rewrites and 4 collocation shifts. | **AUXILIARY LINGUISTIC PROBE** |
| **Candidate 5** | [`scaleup_candidate_5_original_benchmark.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_5_original_benchmark.csv) | **199** | **20** / **38** / **141** | **Continuity Baseline:** Exactly the 199 accepted pairs from the original pilot study (excluding `HC_0178`). | **LONGITUDINAL BASELINE** (Validates pilot continuity) |
| **Candidate 6** | [`scaleup_candidate_6_newly_added_accepted.csv`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/data/scaleup_candidates/scaleup_candidate_6_newly_added_accepted.csv) | **1,487** | **985** / **328** / **174** | **Cohort Generalization:** Strictly newly authored examples (Rows 201–2000). | **GENERALIZATION VALIDATION** |

---

## Detailed Candidate Profiles

### Candidate 1: Strict Accepted Dataset (`scaleup_candidate_1_strict_accepted.csv`)
- **Sample Size:** **1,676 pairs** (3,352 sentences).
- **Composition:**
  - `REALISTIC_SPELLING_ERROR`: 1,005 pairs (59.96%)
  - `SYNONYM_SUBSTITUTION`: 362 pairs (21.60%)
  - `VALID_WORD_CONTEXT`: 309 pairs (18.44%)
- **Inclusion Criteria:** Zero technical or linguistic defects. All sentences end with standard danda (`।`). Exactly one target word changes. Clean single-word tokenization boundaries.
- **Why It Is Recommended:** This dataset adheres strictly to ACL/EMNLP standards for clean, uncontaminated minimal pairs. It eliminates template repetition confounding, avoids multi-word gender agreement shifts, and provides more than sufficient power ($N=1,005$ in spelling) for all explanation stability and faithfulness analyses.

### Candidate 2: Accepted Dataset with Templates (`scaleup_candidate_2_accepted_with_templates.csv`)
- **Sample Size:** **1,954 pairs** (3,908 sentences).
- **Composition:** Candidate 1 ($1,676$) + Template carrier sentences ($278$) = $1,954$ pairs.
  - `REALISTIC_SPELLING_ERROR`: 1,259 pairs (64.43%)
  - `SYNONYM_SUBSTITUTION`: 386 pairs (19.75%)
  - `VALID_WORD_CONTEXT`: 309 pairs (15.81%)
- **Why It Exists:** To provide a high-power sensitivity check. Demonstrating that findings obtained on Candidate 1 hold on Candidate 2 proves that findings are robust to syntactic clustering.

### Candidate 4: Multi-Word Agreement Subgroup (`scaleup_candidate_4_multiword_agreement.csv`)
- **Sample Size:** **12 pairs** (24 sentences).
- **Composition:** 8 true gender-agreement shifts (`मेहनत की` $\to$ `परिश्रम किया`, `यात्रा लंबी` $\to$ `सफर लंबा`, etc.) and 4 collocation shifts.
- **Why It Exists:** Rather than discarding these linguistically natural Hindi sentences, they form an auxiliary probe into how MLMs penalize or reward sentences where synonym substitution triggers necessary grammatical concord across word boundaries.

### Candidate 5: Original Benchmark Subset (`scaleup_candidate_5_original_benchmark.csv`)
- **Sample Size:** **199 pairs** (398 sentences).
- **Composition:** Matches the accepted subset of the original benchmark reported in `RESEARCH_PROJECT_HANDOVER.md` (Rows 1 to 200, excluding rejected `HC_0178`).
- **Why It Exists:** Enables the researcher to re-run the updated inference pipeline on the exact historical subset to verify that score calculations match prior reports.

### Candidate 6: Newly Added Accepted Subset (`scaleup_candidate_6_newly_added_accepted.csv`)
- **Sample Size:** **1,487 pairs** (2,974 sentences).
- **Composition:** Strictly newly created examples (Rows 201 to 2000) that passed strict acceptance criteria.
- **Why It Exists:** Allows testing whether newly authored examples exhibit identical effect sizes and distributions as the pilot set, proving that results are not driven by author cohort bias.

---

## Action Plan for Experiment Execution

Upon your approval:
1. **Primary Run:** Execute `pll_scoring.py`, `tokenization_experiment.py`, `explanation_stability.py`, and `hindi_faithfulness.py` on **Candidate 1 ($N=1,676$)**.
2. **Secondary Run (Sensitivity):** Execute scoring on **Candidate 2 ($N=1,954$)** to confirm robustness.
3. **Continuity Verification:** Score **Candidate 5 ($N=199$)** to confirm exact alignment with historical findings.
