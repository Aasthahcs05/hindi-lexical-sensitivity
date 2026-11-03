# SCALE-UP READINESS REPORT: HINDI LEXICAL PERTURBATION BENCHMARK

**Project Title:** Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi  
**Phase:** Phase 2 — Final Dataset Adjudication and Scale-Up Readiness  
**Auditor:** Antigravity Research Assistant (Independent Verification Mode)  
**Date:** November 2026  
**Status:** Verification Complete — Awaiting Human Research Approval (No model inference executed)

---

## Executive Summary & Readiness Assessment

Following the initial quality audit of the new **2,000-example Hindi lexical sensitivity dataset** (`hindi_lexical_sensitivity_cleaned - Sheet1 (1).csv`), this report provides the final scientific adjudication, template investigation, linguistic triage, and scale-up readiness determination.

### Core Audit Verification Verdict
Independent programmatic re-verification confirms the dataset accounting:
- **Total Raw Records:** Exactly **2,000 sentence pairs** (18 columns, 0 null cells).
- **Strictly Accepted Subset:** **1,676 pairs (83.80%)** — 100% compliant with single-word minimal-pair criteria, pristine Devanagari orthography, and clean danda (`।`) punctuation.
- **Review Required Subset:** **309 pairs (15.45%)** — 278 template carrier sentences, 12 non-minimal/gender-agreement shifts, 6 spelling errors forming valid words, 6 ambiguous target occurrences, and 7 interrogatives.
- **Strictly Rejected Subset:** **15 pairs (0.75%)** — 5 exact duplicate pairs, 6 bare isolated words, 2 target-sentence mismatches, 1 Unicode corruption, and 1 prior adjudication rejection.

```
Total Dataset: 2,000 Pairs (100.0%)
 ├── Candidate 1 (Strict Accepted, No Templates):    1,676 Pairs (83.80%)  <-- RECOMMENDED PRIMARY
 ├── Candidate 2 (Accepted Including Templates):     1,954 Pairs (97.70%)  <-- SENSITIVITY CANDIDATE
 ├── Candidate 4 (Multi-Word Agreement Subgroup):       12 Pairs ( 0.60%)  <-- AUXILIARY PROBE
 ├── Candidate 5 (Original Benchmark Subset):          199 Pairs ( 9.95%)  <-- CONTINUITY BASELINE
 └── Candidate 6 (Newly Added Accepted Subset):      1,487 Pairs (74.35%)  <-- GENERALIZATION TEST
```

---

## 1. Verification of Prior Audit Outputs

Every output artifact from the initial quality audit has been independently re-inspected against the raw dataset:
1. **Count Verification:** Sum of Accepted ($1,676$) + Review ($309$) + Rejected ($15$) = **$2,000$** ($100\%$ partition, $0$ overlapping IDs).
2. **Accepted Subset Integrity:** Re-inspection of all 1,676 rows in `DATASET_2000_ACCEPTED.csv` revealed **zero** missing values, zero bare words, zero punctuation anomalies, and zero multiple target occurrences. All 1,676 original and contrast words are present in their respective sentences.
3. **Rejected Subset Integrity:** All 15 rows in `DATASET_2000_REJECTED.csv` exhibit documented technical failure modes (e.g., bare words in Rows 887, 892, 897; duplicate pairs in Rows 164, 1599, 1803; target mismatch in Rows 1051, 1159).
4. **Column & ID Stability:** All original 18 column headers and ID formats (`HC_0001` to `HC_2000`) have been strictly preserved.

---

## 2. Key Linguistic & Methodological Investigations

### 2.1 The 278 Template-Heavy Examples
A major discovery of the audit was that between Rows 603 and 1499, **278 examples belong to 14 repetitive sentence template families** (e.g., `मैंने [TARGET] शब्द अपनी कॉपी में लिखा।` [45 pairs], `हमें [TARGET] से जुड़ी जानकारी मिली।` [44 pairs], `शिक्षक ने [TARGET] का उल्लेख किया।` [43 pairs]).
- **Linguistic Quality:** Every template sentence is authentic, 100% grammatically correct Hindi.
- **Confounding Risk:** Repeating identical carrier sentences 40+ times reduces context diversity, potentially biasing MLM pseudo-log-likelihood (PLL) scoring and causing attention weights to cluster on identical context tokens.
- **Scientific Decision:** We have isolated these into two distinct scale-up candidates:
  - **Candidate 1 ($N=1,676$):** Excludes templates to guarantee maximum syntactic diversity and statistical independence.
  - **Candidate 2 ($N=1,954$):** Includes templates to evaluate model behavior under massive scale ($97.7\%$ of data).
  *(See [`TEMPLATE_REPETITION_ANALYSIS.md`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/TEMPLATE_REPETITION_ANALYSIS.md) for full forensic analysis).*

### 2.2 The 12 Non-Minimal Gender-Agreement Cases
Inspection revealed that **8 pairs in `SYNONYM_SUBSTITUTION`** altered multiple words because Hindi synonyms of differing grammatical gender force gender concord changes on adjacent verbs or adjectives (e.g., `मेहनत की` [fem] $\to$ `परिश्रम किया` [masc]; `यात्रा लंबी` [fem] $\to$ `सफर लंबा` [masc]). The remaining 4 cases were single-word substitutions containing duplicate substrings (e.g., `की` occurring twice).
- **Scientific Decision:** The 12 pairs violate strict single-word minimal-pair isolation and are excluded from the primary scale-up candidate. They have been isolated into **Candidate 4 (`scaleup_candidate_4_multiword_agreement.csv`)** as an auxiliary linguistic probe.
  *(See [`LINGUISTIC_ADJUDICATION_REPORT.md`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/LINGUISTIC_ADJUDICATION_REPORT.md) for details).*

### 2.3 The 6 Spelling Errors Forming Real Hindi Words
In 6 pairs within `REALISTIC_SPELLING_ERROR`, the orthographic typo forms an existing dictionary word (e.g., `गृह` [home] $\to$ `ग्रह` [planet]; `दिन` [day] $\to$ `दीन` [poor]; `हार` [defeat] $\to$ `हर` [every]).
- **Scientific Decision:** In human writing, these represent authentic cognitive typos (matra/conjunct confusion). However, in an MLM, they induce valid-word contextual competition rather than out-of-vocabulary fragmentation. They are preserved in `REVIEW` pending your decision to reclassify them as `VALID_WORD_CONTEXT`.

---

## 3. Scale-Up Feasibility on Host System

The host workstation environment has been assessed for executing inference across the expanded benchmark:
- **Processor:** AMD Ryzen 7 7840HS (8 cores, 16 threads @ 3.80 GHz).
- **System Memory:** 16 GB Installed Physical RAM.
- **Dedicated GPU:** NVIDIA GeForce RTX 3050 6GB Laptop GPU (CUDA 13.1 supported, PyTorch 2.14.1+cu126).
- **Execution Feasibility:** 
  - Evaluating 1,676 pairs $\times$ 2 models = **3,352 model forward passes**.
  - With batch size = 1 and max sequence length $\le 64$, GPU VRAM allocation will not exceed **2.2 GB** (well within the 6.0 GB hardware limit).
  - Estimated inference time for full PLL scoring: **~8–12 minutes on GPU**.
  - Estimated time for Integrated Gradients (20 steps) on single-subword spelling subset: **~15–20 minutes on GPU**.

---

## 4. Final Recommendation to the Principal Investigator

We recommend adopting a **Two-Tier Experimental Design**:

1. **Tier 1 (Primary Benchmark): Candidate 1 — Strict Accepted (`scaleup_candidate_1_strict_accepted.csv`, $N=1,676$)**
   - **Rationale:** 100% clean minimal pairs. Maximizes context diversity, eliminates template repetition confounding, enforces strict single-word tokenization alignment, and completely avoids multi-word gender ripple effects.
   - **Composition:** 1,005 Spelling Errors ($60.0\%$), 362 Synonyms ($21.6\%$), 309 Contextual Substitutions ($18.4\%$).
2. **Tier 2 (Robustness & Sensitivity Probe): Candidate 2 (`scaleup_candidate_2_accepted_with_templates.csv`, $N=1,954$)**
   - **Rationale:** Evaluates whether model plausibility and explanation stability findings generalize to template-heavy carrier frames ($+278$ pairs).
3. **Tier 3 (Continuity Baseline): Candidate 5 (`scaleup_candidate_5_original_benchmark.csv`, $N=199$)**
   - **Rationale:** Re-scores the original 199 accepted benchmark pairs to provide a direct bridge to the preliminary results reported in `RESEARCH_PROJECT_HANDOVER.md`.

---

## Action Items Awaiting Your Approval

Before we run model inference, please confirm:
1. **Approval of Candidate 1 ($N=1,676$)** as the primary dataset for scale-up experiments.
2. **Decision on the 278 template examples:** Should they be evaluated as a secondary sensitivity tier (recommended) or completely discarded?
3. **Decision on the 6 valid-word spelling errors:** Should they be reclassified into `VALID_WORD_CONTEXT` or retained as spelling noise?

*No models have been executed, and no experimental files have been modified.*
