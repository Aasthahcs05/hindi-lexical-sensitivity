# Research Paper Table Update Audit

**Document:** `PAPER_TABLE_UPDATE_AUDIT.md`  
**Date:** 2026-11-03  
**Project:** `hindi-lexical-sensitivity`  
**Base Document (Structural Authority):** `final_research_paper (1).docx`  
**Backup Created:** `final_research_paper (1)_backup.docx`  
**Updated Document Saved As:** `final_research_paper_updated_results.docx`  
**Authoritative Latest Experiment Source:** Scaleup Rerun (`results/runs/scaleup_rerun/`)  
**Frozen Canonical Dataset:** Adjudicated Primary Benchmark ($N = 1,679$: 1,005 Spelling Error, 362 Synonym Substitution, 312 Valid-Word Context)

---

## 1. Executive Summary

This audit documents the complete, in-place update of the five original result tables in `final_research_paper (1).docx` to reflect the latest verified expanded experimental results ($N = 1,679$).

### Guiding Principles Strictly Preserved:
1. **Preservation of Original Table Designs**:
   - Zero new tables, replacement tables, or duplicate tables were created.
   - The document contains **strictly 5 tables**, preserving their exact positions, titles, column counts, column orders, and row structures.
2. **Authoritative Numerical Substitution**:
   - All historical $N = 200$ pilot values (and errant $1,280$ narrative placeholders) have been replaced with the verified results from `results/runs/scaleup_rerun/`.
   - Every metric was retrieved directly from canonical run outputs without manual estimation or rounding corruption.
3. **Harmonization of Narrative Text**:
   - 22 corresponding text paragraphs across the Abstract, Introduction, Methodology, Results, Discussion, Limitations, and Conclusion were updated to ensure full mathematical consistency with the updated tables.

---

## 2. Table-by-Table Update Audit

### Table 1 (Paper Table III): SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS

- **Location:** Body Table 1 (following paragraph 67 `SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS`).
- **Table Title:** `TABLE III. SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS`
- **Original Structure Preserved:** Exactly 3 rows $\times$ 4 columns (`Model`, `Original`, `Perturbed`, `Change`).
- **Sample Size / Cohort:** Expanded from $N = 20$ spelling pairs to $N = 1,005$ spelling pairs.
- **Canonical Source Files:**
  - `results/runs/scaleup_rerun/tokenization/tokenization_results.csv`
  - `results/runs/scaleup_rerun/dashboard_data/tokenization_summary.csv`

#### Numerical Comparison:

| Table Cell / Metric | Old Reported Value (N=20 Pilot Basis) | New Canonical Value (N=1,005 Expanded Basis) | Difference | Canonical Source File | Verification Status |
|---|---|---|---|---|---|
| **MuRIL \| Original** | 90% ($18/20$) | **91.7%** ($922/1,005$) | +1.7 pp | `tokenization_results.csv` | **Updated & Verified** |
| **MuRIL \| Perturbed** | 30% ($6/20$) | **20.1%** ($202/1,005$) | −9.9 pp | `tokenization_results.csv` | **Updated & Verified** |
| **MuRIL \| Change** | −60 pp | **−71.6 pp** | −11.6 pp | `tokenization_results.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Original** | 70% ($14/20$) | **62.3%** ($626/1,005$) | −7.7 pp | `tokenization_results.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Perturbed** | 20% ($4/20$) | **6.4%** ($64/1,005$) | −13.6 pp | `tokenization_results.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Change** | −50 pp | **−55.9 pp** | −5.9 pp | `tokenization_results.csv` | **Updated & Verified** |

#### Footnote Update:
- **Old Footnote (P69):** `Coverage is the share of target words represented by exactly one subword token (N = 1280 pairs per model). pp = percentage points.`
- **New Footnote (P69):** `Coverage is the share of target words represented by exactly one subword token (N = 1,005 pairs per model). pp = percentage points.`

---

### Table 2 (Paper Table IV): MEAN ΔS BY MODEL AND PAIR CATEGORY

- **Location:** Body Table 2 (following paragraph 78 `MEAN ΔS BY MODEL AND PAIR CATEGORY`).
- **Table Title:** `TABLE IV. MEAN ΔS BY MODEL AND PAIR CATEGORY`
- **Original Structure Preserved:** Exactly 7 rows $\times$ 3 columns (`Model`, `Category`, `Mean ΔS`).
- **Sample Size / Cohort:** Expanded from $N = 200$ (142 context, 38 synonym, 20 spelling) to $N = 1,679$ (312 context, 362 synonym, 1,005 spelling).
- **Metric Definition:** $\Delta S = \text{MeanLogP}(W_{\text{contrast}}) - \text{MeanLogP}(W_{\text{original}})$.
- **Canonical Source Files:**
  - `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv`
  - `results/runs/scaleup_rerun/scoring/pll_scoring_results.csv`

#### Numerical Comparison:

| Table Cell / Metric | Old Reported Value (N=200 Basis) | New Canonical Value (N=1,679 Basis) | Difference | Canonical Source File | Verification Status |
|---|---|---|---|---|---|
| **XLM-RoBERTa \| Valid-word context** | −1.0933 ($N=142$) | **−1.0831** ($N=312$) | +0.0102 | `descriptive_statistics.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Synonym substitution** | −0.0655 ($N=38$) | **−0.0098** ($N=362$) | +0.0557 | `descriptive_statistics.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Spelling error** | −0.6695 ($N=20$) | **−0.8864** ($N=1,005$) | −0.2169 | `descriptive_statistics.csv` | **Updated & Verified** |
| **MuRIL \| Valid-word context** | −1.9141 ($N=142$) | **−1.8470** ($N=312$) | +0.0671 | `descriptive_statistics.csv` | **Updated & Verified** |
| **MuRIL \| Synonym substitution** | −0.5810 ($N=38$) | **−0.1787** ($N=362$) | +0.4023 | `descriptive_statistics.csv` | **Updated & Verified** |
| **MuRIL \| Spelling error** | −2.0368 ($N=20$) | **−1.2045** ($N=1,005$) | +0.8323 | `descriptive_statistics.csv` | **Updated & Verified** |

#### Footnote Update:
- **Old Footnote (P79):** `ΔS = MeanLogP(contrast) − MeanLogP(original). Negative values mean the contrast sentence received a lower mean token log-probability. Pairs: 142 valid-word context, 38 synonym substitution, 1280 spelling error.`
- **New Footnote (P79):** `ΔS = MeanLogP(contrast) − MeanLogP(original). Negative values mean the contrast sentence received a lower mean token log-probability. Pairs: 312 valid-word context, 362 synonym substitution, 1,005 spelling error (N = 1,679 total).`

---

### Table 3 (Paper Table V): POOLED EXPLANATION STABILITY

- **Location:** Body Table 3 (following paragraph 83 `POOLED EXPLANATION STABILITY`).
- **Table Title:** `TABLE V. POOLED EXPLANATION STABILITY`
- **Original Structure Preserved:** Exactly 5 rows $\times$ 4 columns (`Model`, `Method`, `Mean rank ρ`, `Mean cosine`).
- **Sample Size / Cohort:** Expanded from $N = 20$ spelling pairs to $N = 1,005$ spelling pairs (Stage 7 Visible-Target Protocol, `all_scorable_pooled`).
- **Canonical Source Files:**
  - `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv`
  - `results/runs/scaleup_rerun/stability/stability_pair_level.csv`

#### Numerical Comparison:

| Table Cell / Metric | Old Reported Value (N=20 Basis) | New Canonical Value (N=1,005 Basis) | Difference | Canonical Source File | Verification Status |
|---|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Mean rank ρ** | 0.7425 | **0.6258** | −0.1167 | `stability_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Attention \| Mean cosine** | 0.9648 | **0.9353** | −0.0295 | `stability_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| Mean rank ρ** | 0.3589 | **0.3319** | −0.0270 | `stability_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| Mean cosine** | 0.8994 | **0.8890** | −0.0104 | `stability_summary.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| Mean rank ρ** | 0.7043 | **0.8027** | +0.0984 | `stability_summary.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| Mean cosine** | 0.9639 | **0.9518** | −0.0121 | `stability_summary.csv` | **Updated & Verified** |
| **MuRIL \| IG \| Mean rank ρ** | 0.2632 | **0.2560** | −0.0072 | `stability_summary.csv` | **Updated & Verified** |
| **MuRIL \| IG \| Mean cosine** | 0.9880 | **0.9818** | −0.0062 | `stability_summary.csv` | **Updated & Verified** |

#### Strict Single-Subword Subset Documentation:
- In the expanded run, the strict single-subword target subset expanded from $N = 4$ to **$N = 52$ pairs** for XLM-RoBERTa (Attention $\rho = 0.6306$, cosine $= 0.9349$; IG $\rho = 0.4210$, cosine $= 0.9026$), and from $N = 6$ to **$N = 197$ pairs** for MuRIL (Attention $\rho = 0.8053$, cosine $= 0.9725$; IG $\rho = 0.3471$, cosine $= 0.9868$). This is explicitly documented in the accompanying narrative paragraph (P87).

---

### Table 4 (Paper Table VI): FAITHFULNESS INTERVENTION SUMMARY

- **Location:** Body Table 4 (following paragraph 89 `FAITHFULNESS INTERVENTION SUMMARY`).
- **Table Title:** `TABLE VI. FAITHFULNESS INTERVENTION SUMMARY`
- **Original Structure Preserved:** Exactly 5 rows $\times$ 4 columns (`Model`, `Method`, `Mean gap`, `Win rate`).
- **Sample Size / Cohort:** Expanded from $N = 40$ evaluated sentences ($20 \text{ pairs} \times 2$) to **$N = 2,010$ evaluated sentences** ($1,005 \text{ pairs} \times 2$) per fraction ($6,030$ total evaluations across fractions 10%, 20%, and 30%).
- **Canonical Source Files:**
  - `results/runs/scaleup_rerun/faithfulness/faithfulness_summary.csv`
  - `results/runs/scaleup_rerun/faithfulness/faithfulness_pair_level.csv`

#### Numerical Comparison:

| Table Cell / Metric | Old Reported Value (N=40 Basis) | New Canonical Value (N=2,010 Basis) | Difference | Canonical Source File | Verification Status |
|---|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Mean gap** | 4.40 | **3.02** ($3.0158$) | −1.38 | `faithfulness_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Attention \| Win rate** | 76.7% | **65.6%** ($65.59\%$) | −11.1% | `faithfulness_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| Mean gap** | 2.32 | **2.54** ($2.5427$) | +0.22 | `faithfulness_summary.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| Win rate** | 58.3% | **62.4%** ($62.37\%$) | +4.1% | `faithfulness_summary.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| Mean gap** | 2.21 | **−1.31** ($−1.3127$) | −3.52 | `faithfulness_summary.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| Win rate** | 63.3% | **39.6%** ($39.63\%$) | −23.7% | `faithfulness_summary.csv` | **Updated & Verified** |
| **MuRIL \| IG \| Mean gap** | −0.45 | **−0.63** ($−0.6327$) | −0.18 | `faithfulness_summary.csv` | **Updated & Verified** |
| **MuRIL \| IG \| Win rate** | 44.2% | **48.7%** ($48.67\%$) | +4.5% | `faithfulness_summary.csv` | **Updated & Verified** |

#### Fraction-by-Fraction Breakdown (3-Fraction Average):
- **XLM-RoBERTa Attention:** $f=0.10$ (+2.44, 63.5%), $f=0.20$ (+2.80, 65.8%), $f=0.30$ (+3.81, 67.5%) $\to$ Average Gap: **+3.02**, Average Win Rate: **65.6%**.
- **XLM-RoBERTa IG:** $f=0.10$ (+1.98, 59.8%), $f=0.20$ (+2.25, 62.2%), $f=0.30$ (+3.40, 65.1%) $\to$ Average Gap: **+2.54**, Average Win Rate: **62.4%**.
- **MuRIL Attention:** $f=0.10$ (−2.02, 33.9%), $f=0.20$ (−2.32, 35.4%), $f=0.30$ (+0.40, 49.6%) $\to$ Average Gap: **−1.31**, Average Win Rate: **39.6%**.
- **MuRIL IG:** $f=0.10$ (−0.30, 49.9%), $f=0.20$ (−0.51, 49.4%), $f=0.30$ (−1.08, 46.7%) $\to$ Average Gap: **−0.63**, Average Win Rate: **48.7%**.

#### Footnote Update:
- **Old Footnote (P91):** `Averaged over masking fractions of 10%, 20% and 30%; N = 40 sentences per fraction (20 pairs × 2). Gap = Dtop − Dbottom; win rate = share of sentences with Dtop > Dbottom. IG = Integrated Gradients.`
- **New Footnote (P91):** `Averaged over masking fractions of 10%, 20% and 30%; N = 2,010 sentences per fraction (1,005 pairs × 2). Gap = Dtop − Dbottom; win rate = share of sentences with Dtop > Dbottom. IG = Integrated Gradients.`

---

### Table 5 (Paper Table VII): STABILITY–FAITHFULNESS CORRELATIONS

- **Location:** Body Table 5 (following paragraph 97 `STABILITY–FAITHFULNESS CORRELATIONS`).
- **Table Title:** `TABLE VII. STABILITY–FAITHFULNESS CORRELATIONS`
- **Original Structure Preserved:** Exactly 5 rows $\times$ 5 columns (`Model`, `Method`, `Spearman ρ`, ``, `p-value` — preserving the original table cell structure).
- **Sample Size / Cohort:** Expanded from $N = 20$ pairs ($df = 18$) to **$N = 1,005$ pairs** ($df = 1,003$).
- **Metric Definition:** Spearman rank correlation between visible-target stability ($\rho$) and mean faithfulness gap at 20% masking fraction ($f = 0.20$).
- **Canonical Source Files:**
  - `results/runs/scaleup_rerun/faithfulness/stability_faithfulness_relationship.csv`
  - `results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv`

#### Numerical Comparison:

| Table Cell / Metric | Old Reported Value (N=20 Basis) | New Canonical Value (N=1,005 Basis) | Difference | Canonical Source File | Verification Status |
|---|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Spearman ρ** | 0.2704 | **0.0711** | −0.1993 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| Attention \| p-value** | 0.2490 | **0.0241** ($2.41 \times 10^{-2}$) | −0.2249 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| Spearman ρ** | 0.1583 | **0.0705** | −0.0878 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **XLM-RoBERTa \| IG \| p-value** | 0.5052 | **0.0255** ($2.55 \times 10^{-2}$) | −0.4797 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| Spearman ρ** | −0.1611 | **−0.0714** | +0.0897 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **MuRIL \| Attention \| p-value** | 0.4974 | **0.0235** ($2.35 \times 10^{-2}$) | −0.4739 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **MuRIL \| IG \| Spearman ρ** | 0.0075 | **0.0218** | +0.0143 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |
| **MuRIL \| IG \| p-value** | 0.9749 | **0.4902** ($4.90 \times 10^{-1}$) | −0.4847 | `stability_faithfulness_relationship.csv` | **Updated & Verified** |

#### Footnote & Scientific Interpretation Update:
- **Old Footnote (P100):** `Spearman correlation between visible-target stability and the mean faithfulness gap at a masking fraction of f = 0.20; N = 200 spelling pairs per model and method. None of the correlations is significant at p < .05. IG = Integrated Gradients.`
- **New Footnote (P100):** `Spearman rank correlation between visible-target stability (rank ρ) and mean faithfulness gap at 20% masking; N = 1,005 spelling pairs per model and method. While correlations of small magnitude (|ρ| ≈ 0.07) reach nominal statistical significance (p < 0.05) due to large sample power, effect sizes remain negligible (|ρ| < 0.10). IG = Integrated Gradients.`
- **Statistical Interpretation:** With $N = 1,005$, the statistical power to detect minute correlations is high. However, an effect size of $|\rho| \approx 0.07$ accounts for less than $0.6\%$ of the shared variance ($R^2 < 0.006$). This demonstrates conclusively that attribution stability cannot serve as an empirical proxy for explanation faithfulness.

---

## 3. Audit of Harmonized Narrative Text Paragraphs

| Paragraph # | Section | Context / Topic | Old Text Summary | Updated Text Summary |
|---|---|---|---|---|
| **P14** | Abstract | Cohort, tokenization collapse, PLL drops, stability & correlation findings | 2000 pairs, 1280 spelling, drops: 90% $\to$ 30% / 70% $\to$ 20%, stability 0.743 / 0.704 | Adjudicated $N = 1,679$ benchmark (1,005 spelling, 362 synonym, 312 context), drops: 91.7% $\to$ 20.1% / 62.3% $\to$ 6.4%, stability: 0.803 / 0.626, $|\rho| < 0.08$ |
| **P18** | Introduction | Primary resource contribution | 2000-pair Devanagari Hindi dataset | Adjudicated 1,679-pair Devanagari Hindi benchmark (312 context, 362 synonym, 1,005 spelling) |
| **P31** | Dataset | Benchmark composition | 2000 pairs (322 context, 398 synonym, 1280 spelling) | Adjudicated 1,679 pairs (312 context, 362 synonym, 1,005 spelling) |
| **P32** | Dataset | Validation report status | 2000 rows, 1999 accepted, 1 rejected, 6 review cases | 1,679 pairs with unanimous agreement or consensus adjudication, Unicode verified |
| **P33** | Dataset | Spelling track description | 1,280 pairs | 1,005 pairs covering authentic Devanagari orthographic variation |
| **P69** | Results | Table III Footnote | $N = 1280$ pairs | $N = 1,005$ pairs per model |
| **P71** | Results | Subword fragmentation narrative | 1280 spelling pairs | 1,005 spelling pairs, MuRIL: 91.7% $\to$ 20.1% (−71.6 pp), XLM-R: 62.3% $\to$ 6.4% (−55.9 pp) |
| **P79** | Results | Table IV Footnote | 142 context, 38 synonym, 1280 spelling | 312 context, 362 synonym, 1,005 spelling ($N = 1,679$ total) |
| **P81** | Results | PLL scoring narrative | General description | MuRIL: −1.2045 (spelling), −1.8470 (context), −0.1787 (synonym); XLM-R: −0.8864, −1.0831, −0.0098 |
| **P85** | Results | Stability sample size | 1280 spelling pairs | 1,005 spelling pairs per model and method (2,010 forward passes) |
| **P87** | Results | Single-subword eligibility | 4 XLM-R and 6 MuRIL pairs | 52 XLM-R and 197 MuRIL pairs; reports subset stabilities (MuRIL Attn: 0.8053; XLM-R Attn: 0.6306) |
| **P91** | Results | Table VI Footnote | $N = 40$ sentences (20 pairs $\times$ 2) | $N = 2,010$ sentences per fraction (1,005 pairs $\times$ 2) |
| **P95** | Results | Faithfulness results narrative | XLM-R Attention higher, MuRIL IG slightly negative | XLM-R gaps +3.02 and +2.54 (win rate > 62%); MuRIL aggregate gaps −1.31 and −0.63 |
| **P100** | Results | Table VII Footnote | $N = 200$ spelling pairs, none significant | $N = 1,005$ spelling pairs, nominal $p < 0.05$, negligible effect size ($|\rho| < 0.10$) |
| **P101** | Results | Figure 2 caption | 1280 pairs | 1,005 pairs for each model and method; $|\rho| < 0.08$ |
| **P104** | Results | Stability-faithfulness narrative | None achieves $p < 0.05$ | High power yields nominal $p < 0.05$, but $|\rho| \le 0.0714$ ($R^2 < 0.006$, negligible effect size) |
| **P106** | Results | Figure 3 caption | 1280 spelling pairs | 1,005 spelling pairs per model |
| **P112** | Results | Figure 3 discussion | Old stability values: 0.743 vs 0.359 / 0.704 vs 0.263 | New values: 0.626 vs 0.332 for XLM-R; 0.803 vs 0.256 for MuRIL; cosine 0.889 / 0.982 |
| **P113** | Results | Figure 4 discussion | Old win rates (75–77.5%) | New win rates (XLM-R 63.5–67.5%, gaps +2.44 to +3.81; MuRIL Attn −2.02 to +0.40) |
| **P119** | Limitations | Sample size limitations | 1280 spelling pairs | 1,005 spelling pairs (2,010 evaluated sentences per fraction) |
| **P120** | Limitations | Target alignment | 4 XLM-R and 6 MuRIL pairs | 52 XLM-R and 197 MuRIL pairs |
| **P127** | Conclusion | Overall correlation conclusion | 1280 spelling pairs, no significant link | 1,005 spelling pairs, correlations bounded within $|\rho| < 0.08$, confirming orthogonality |

---

## 4. Final Validation Checklist

- [x] **Table count preserved**: Exactly 5 tables exist in the document (zero duplicate or newly designed result tables).
- [x] **Table positions preserved**: All 5 tables remain in their exact original locations.
- [x] **Table titles unchanged**: All original table titles (TABLE III through TABLE VII) are preserved character-for-character.
- [x] **Table column structures preserved**: Column counts, headers, and orders are 100% identical to `final_research_paper (1).docx`.
- [x] **Table row structures preserved**: Row definitions and labels are identical.
- [x] **Latest expanded values applied**: All numbers reflect the canonical `results/runs/scaleup_rerun/` outputs.
- [x] **Accurate denominators & sample sizes**: All footnotes reflect the actual $N = 1,005$ spelling pairs and $N = 1,679$ total benchmark pairs.
- [x] **Narrative agreement**: All surrounding text paragraphs, figure captions, and conclusion statements agree with the updated tables.
- [x] **Zero lingering placeholders**: Validated that 0 instances of `1280` or outdated pilot percentages remain.
- [x] **Document integrity verified**: Document re-opened, programmatically asserted, and verified intact at `final_research_paper_updated_results.docx` (2,068,733 bytes).

