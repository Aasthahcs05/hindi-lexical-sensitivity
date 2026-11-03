# Verification of Original Research Paper Tables (Strictly N=200 Baseline)

**Document:** `ORIGINAL_200_TABLE_VERIFICATION.md`  
**Date:** 2026-11-03  
**Project:** `hindi-lexical-sensitivity`  
**Reference Original Paper:** `final_research_paper (1).docx` (Document tables 1–5 / Paper Tables III–VII)  
**Authoritative Baseline Experiment:** Historical Pilot Run (`results/runs/historical_pilot_200/`)  
**Authoritative Raw Dataset:** `data/raw/hindi_lexical_sensitivity_cleaned.xlsx` (SHA-256: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`)  
**Cohort Restriction:** Strictly $N=200$ pilot cohort. No expanded benchmark ($N=1,679$), template benchmark ($N=1,957$), or auxiliary probe ($N=12$) data was used.

---

## 1. Executive Summary

This report establishes whether the five tables published in the original research paper (`final_research_paper (1).docx`) accurately reflect the original 200-sample experiment, and traces each reported statistic to its source data and calculation formulas.

### Key Conclusions:
1. **100% Numerical Accuracy Confirmed**: Every single numerical metric reported in all five original tables—including percentages, percentage-point changes, Pseudo-Log-Likelihood score differences, mean rank stabilities, cosine similarities, faithfulness gaps, win rates, Spearman rank correlations, and $p$-values—is **mathematically confirmed and reproduced to the exact decimal place** from the original 200-sample experiment files under `results/runs/historical_pilot_200/`.
2. **Resolution of the "1,280 Pairs" Narrative Discrepancy**: While the original paper's footnotes and surrounding prose claim in several places that the spelling analyses were conducted on $N=1,280$ pairs, **the numerical values in all five tables were computed exclusively on the $N=20$ spelling pairs of the 200-sample pilot dataset**:
   - In Table III, $90\%$ and $30\%$ represent $18/20$ and $6/20$ pairs for MuRIL; $70\%$ and $20\%$ represent $14/20$ and $4/20$ pairs for XLM-RoBERTa.
   - In Table IV, the footnote correctly lists $142$ valid-word context and $38$ synonym pairs ($142 + 38 = 180$), but prints $1,280$ instead of $20$ for spelling, even though the reported mean drops ($-0.6695$ and $-2.0368$) are the exact means over the $20$ spelling pairs.
   - In Table VI, the footnote explicitly reveals the true sample size: *"N = 40 sentences per fraction (20 pairs × 2)"*.
   - In Table VII, the reported correlation $p$-values ($p = 0.2490$ for $r_s = 0.2704$; $p = 0.4974$ for $r_s = -0.1611$) are mathematically possible only with degrees of freedom $df = 20 - 2 = 18$ ($N=20$). If $N$ had been $1,280$, $r_s = 0.2704$ would have yielded $p = 4.8 \times 10^{-23}$.
3. **Data Completeness**: The original 200-sample experiment outputs in `results/runs/historical_pilot_200/` are complete, self-contained, and fully sufficient to reproduce all five original tables without relying on any expanded data.

---

## 2. Inventory of Original Sources Traced

| Artifact Category | File Path | Verification Status & Checksum / Shape |
|---|---|---|
| **Original Dataset** | `data/raw/hindi_lexical_sensitivity_cleaned.xlsx` | Shape: $200 \times 18$. SHA-256: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`. Tracks: 142 Valid-Word Context, 38 Synonym, 20 Realistic Spelling. |
| **Tokenization Outputs** | `results/runs/historical_pilot_200/tokenization/tokenization_results.csv` | Shape: $400 \times 39$ ($200 \text{ pairs} \times 2 \text{ models}$). |
| **Tokenization Summary** | `results/runs/historical_pilot_200/dashboard_data/tokenization_summary.csv` | 6 rows ($3 \text{ tracks} \times 2 \text{ models}$). |
| **PLL Scoring Outputs** | `results/runs/historical_pilot_200/scoring/pll_scoring_results.csv` | Shape: $400 \times 31$ ($200 \text{ pairs} \times 2 \text{ models}$). |
| **Descriptive Statistics** | `results/runs/historical_pilot_200/analysis/descriptive_statistics.csv` | 12 rows (track-level statistics including/excluding rejected row HC_0185). |
| **Stability Pair-Level** | `results/runs/historical_pilot_200/hindi_explanation_stability/stability_pair_level.csv` | Shape: $80 \times 33$ ($20 \text{ spelling pairs} \times 2 \text{ models} \times 2 \text{ methods}$). |
| **Stability Summary** | `results/runs/historical_pilot_200/dashboard_data/stability_summary.csv` | 12 rows (Stage 7 visible-target protocol and Stage 6 masked-target protocol). |
| **Faithfulness Pair-Level**| `results/runs/historical_pilot_200/hindi_faithfulness/faithfulness_pair_level.csv` | Shape: $1,440 \times 28$ ($40 \text{ sentences} \times 2 \text{ models} \times 2 \text{ methods} \times 3 \text{ fractions} \times 3 \text{ interventions}$). |
| **Faithfulness Summary** | `results/runs/historical_pilot_200/hindi_faithfulness/faithfulness_summary.csv` | 24 rows ($2 \text{ models} \times 2 \text{ methods} \times 2 \text{ subsets} \times 3 \text{ fractions}$). |
| **Stability-Faithfulness**| `results/runs/historical_pilot_200/hindi_faithfulness/stability_faithfulness_relationship.csv` | Shape: $80 \times 11$ ($20 \text{ spelling pairs} \times 2 \text{ models} \times 2 \text{ methods}$). |
| **Original Paper Document**| `final_research_paper (1).docx` | Contains the 5 authoritative tables (Docx Tables 1–5). |
| **Original Notebooks** | `notebooks/01_dataset_curation_and_validation.ipynb` through `07_paper_synthesis_and_dashboard_integration.ipynb` | Execution pipeline for the 200-sample pilot. |

---

## 3. Meticulous Table-by-Table Verification

### Table 1 (Paper Table III): SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS

#### Original Paper Table Layout & Values:
| Model | Original | Perturbed | Change |
|---|---|---|---|
| MuRIL | 90% | 30% | −60 pp |
| XLM-RoBERTa | 70% | 20% | −50 pp |

*Footnote in original paper:* `"Coverage is the share of target words represented by exactly one subword token (N = 1280 pairs per model). pp = percentage points."*

#### Detailed Verification & Recalculation:
- **Cohort Evaluated**: `REALISTIC_SPELLING_ERROR` track ($N = 20$ pairs).
- **MuRIL**:
  - Original target word represented by 1 subword: $18 / 20 = 90.0\%$
  - Perturbed (contrast) target word represented by 1 subword: $6 / 20 = 30.0\%$
  - Difference: $30.0\% - 90.0\% = -60.0\text{ pp}$
- **XLM-RoBERTa**:
  - Original target word represented by 1 subword: $14 / 20 = 70.0\%$
  - Perturbed (contrast) target word represented by 1 subword: $4 / 20 = 20.0\%$
  - Difference: $20.0\% - 70.0\% = -50.0\text{ pp}$

#### Cell-by-Cell Comparison:

| Original table value | Recalculated N=200 value | Difference | Source file | Verification status |
|---|---|---|---|---|
| **MuRIL \| Original: 90%** | 90.0% (18/20 pairs) | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Perturbed: 30%** | 30.0% (6/20 pairs) | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Change: −60 pp** | −60.0 pp | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Original: 70%** | 70.0% (14/20 pairs) | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Perturbed: 20%** | 20.0% (4/20 pairs) | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Change: −50 pp** | −50.0 pp | 0.0 pp | `tokenization/tokenization_results.csv` | **Confirmed** (Exact Match) |

*Audit Finding on Sample Size:* The values $90\%$, $30\%$, $-60\text{ pp}$ and $70\%$, $20\%$, $-50\text{ pp}$ match the $N=20$ spelling pair calculations exactly. The footnote text stating `N = 1280 pairs per model` is a narrative erratum; the underlying mathematical calculation was performed strictly on $N=20$.

---

### Table 2 (Paper Table IV): MEAN ΔS BY MODEL AND PAIR CATEGORY

#### Original Paper Table Layout & Values:
| Model | Category | Mean ΔS |
|---|---|---|
| XLM-RoBERTa | Valid-word context | −1.0933 |
| XLM-RoBERTa | Synonym substitution | −0.0655 |
| XLM-RoBERTa | Spelling error | −0.6695 |
| MuRIL | Valid-word context | −1.9141 |
| MuRIL | Synonym substitution | −0.5810 |
| MuRIL | Spelling error | −2.0368 |

*Footnote in original paper:* `"Pairs: 142 valid-word context, 38 synonym substitution, 1280 spelling error."*

#### Detailed Verification & Recalculation:
- **Metric**: $\Delta S = \Delta \text{MeanLogP} = \text{MeanLogP}(W_{\text{contrast}}) - \text{MeanLogP}(W_{\text{original}})$.
- **Source Data**: `results/runs/historical_pilot_200/analysis/descriptive_statistics.csv` and `results/runs/historical_pilot_200/scoring/pll_scoring_results.csv`.
- **Sample Counts**:
  - `VALID_WORD_CONTEXT`: $N = 142$ pairs
  - `SYNONYM_SUBSTITUTION`: $N = 38$ pairs
  - `REALISTIC_SPELLING_ERROR`: $N = 20$ pairs

#### Cell-by-Cell Comparison:

| Original table value | Recalculated N=200 value | Difference | Source file | Verification status |
|---|---|---|---|---|
| **XLM-RoBERTa \| Valid-word context: −1.0933** | −1.0933 (N=142) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Synonym substitution: −0.0655** | −0.0655 (N=38) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Spelling error: −0.6695** | −0.6695 (N=20) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Valid-word context: −1.9141** | −1.9141 (N=142) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Synonym substitution: −0.5810** | −0.5810 (N=38) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Spelling error: −2.0368** | −2.0368 (N=20) | 0.0000 | `analysis/descriptive_statistics.csv` | **Confirmed** (Exact Match) |

*Audit Finding on Sample Size:* The footnote correctly cites $142$ valid-word context pairs and $38$ synonym pairs ($142 + 38 = 180$, which exactly matches the 200-sample dataset structure $142 + 38 + 20 = 200$). The footnote text `1280 spelling error` is an erratum for `20 spelling error`, as the reported means ($-0.6695$ and $-2.0368$) are the exact arithmetic means of the $N=20$ spelling pairs.

---

### Table 3 (Paper Table V): POOLED EXPLANATION STABILITY

#### Original Paper Table Layout & Values:
| Model | Method | Mean rank ρ | Mean cosine |
|---|---|---|---|
| XLM-RoBERTa | Attention | 0.7425 | 0.9648 |
| XLM-RoBERTa | IG | 0.3589 | 0.8994 |
| MuRIL | Attention | 0.7043 | 0.9639 |
| MuRIL | IG | 0.2632 | 0.9880 |

*Footnote in original paper:* `"Target-word tokens kept visible during attribution; pooled across 1280 spelling pairs per model."*

#### Detailed Verification & Recalculation:
- **Evaluation Protocol**: Stage 7 Visible-Target Protocol (`all_scorable_pooled`, $N = 20$ spelling pairs).
  *(Note: In Stage 6, masking the target word resulted in identical input sequences, yielding an artificial $\rho = 1.000$; Stage 7 resolved this by keeping target tokens visible during attribution).*
- **Source Data**: `results/runs/historical_pilot_200/dashboard_data/stability_summary.csv` and `results/runs/historical_pilot_200/hindi_explanation_stability/stability_pair_level.csv`.

#### Cell-by-Cell Comparison:

| Original table value | Recalculated N=200 value | Difference | Source file | Verification status |
|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Mean rank ρ: 0.7425** | 0.7425 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Attention \| Mean cosine: 0.9648** | 0.9648 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| Mean rank ρ: 0.3589** | 0.3589 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| Mean cosine: 0.8994** | 0.8994 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| Mean rank ρ: 0.7043** | 0.7043 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| Mean cosine: 0.9639** | 0.9639 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| Mean rank ρ: 0.2632** | 0.2632 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| Mean cosine: 0.9880** | 0.9880 (N=20) | 0.0000 | `dashboard_data/stability_summary.csv` | **Confirmed** (Exact Match) |

*Audit Finding on Sample Size & Subsets:* All 8 values match the 20-pair pooled averages to 4 decimal places. Furthermore, the paper text states: *"For the single-subword target protocol only 4 XLM-RoBERTa pairs and 6 MuRIL pairs were eligible."* This sentence explicitly confirms that the experiment operated on the $N=20$ spelling pairs of the pilot dataset (where exactly 4 XLM-R and 6 MuRIL pairs had single-subword alignment).

---

### Table 4 (Paper Table VI): FAITHFULNESS INTERVENTION SUMMARY

#### Original Paper Table Layout & Values:
| Model | Method | Mean gap | Win rate |
|---|---|---|---|
| XLM-RoBERTa | Attention | 4.40 | 76.7% |
| XLM-RoBERTa | IG | 2.32 | 58.3% |
| MuRIL | Attention | 2.21 | 63.3% |
| MuRIL | IG | −0.45 | 44.2% |

*Footnote in original paper:* `"Averaged over masking fractions of 10%, 20% and 30%; N = 40 sentences per fraction (20 pairs × 2). Gap = Dtop − Dbottom; win rate = share of sentences with Dtop > Dbottom."*

#### Detailed Verification & Recalculation:
- **Intervention Protocol**: Token erasure intervention at $f \in \{0.10, 0.20, 0.30\}$ on $N = 40$ sentences (20 spelling pairs $\times$ 2 sentences per pair).
- **Source Data**: `results/runs/historical_pilot_200/hindi_faithfulness/faithfulness_summary.csv` and `faithfulness_pair_level.csv`.
- **Fraction-Level Data from `faithfulness_summary.csv`**:
  - **XLM-RoBERTa Attention**:
    - $f=0.10$: $\text{Gap} = +4.0170, \text{Win Rate} = 77.5\%$ (31/40)
    - $f=0.20$: $\text{Gap} = +4.0170, \text{Win Rate} = 77.5\%$ (31/40)
    - $f=0.30$: $\text{Gap} = +5.1716, \text{Win Rate} = 75.0\%$ (30/40)
    - Average across fractions: $\text{Mean Gap} = \frac{4.0170 + 4.0170 + 5.1716}{3} = 4.4019 \approx 4.40$; $\text{Mean Win Rate} = \frac{77.5 + 77.5 + 75.0}{3} = 76.67\% \approx 76.7\%$
  - **XLM-RoBERTa Integrated Gradients**:
    - $f=0.10$: $\text{Gap} = +1.8373, \text{Win Rate} = 60.0\%$ (24/40)
    - $f=0.20$: $\text{Gap} = +1.8373, \text{Win Rate} = 60.0\%$ (24/40)
    - $f=0.30$: $\text{Gap} = +3.2952, \text{Win Rate} = 55.0\%$ (22/40)
    - Average across fractions: $\text{Mean Gap} = \frac{1.8373 + 1.8373 + 3.2952}{3} = 2.3233 \approx 2.32$; $\text{Mean Win Rate} = \frac{60.0 + 60.0 + 55.0}{3} = 58.33\% \approx 58.3\%$
  - **MuRIL Attention**:
    - $f=0.10$: $\text{Gap} = +0.4177, \text{Win Rate} = 60.0\%$ (24/40)
    - $f=0.20$: $\text{Gap} = +0.4177, \text{Win Rate} = 60.0\%$ (24/40)
    - $f=0.30$: $\text{Gap} = +5.7943, \text{Win Rate} = 70.0\%$ (28/40)
    - Average across fractions: $\text{Mean Gap} = \frac{0.4177 + 0.4177 + 5.7943}{3} = 2.2099 \approx 2.21$; $\text{Mean Win Rate} = \frac{60.0 + 60.0 + 70.0}{3} = 63.33\% \approx 63.3\%$
  - **MuRIL Integrated Gradients**:
    - $f=0.10$: $\text{Gap} = -0.6855, \text{Win Rate} = 45.0\%$ (18/40)
    - $f=0.20$: $\text{Gap} = -0.6855, \text{Win Rate} = 45.0\%$ (18/40)
    - $f=0.30$: $\text{Gap} = +0.0325, \text{Win Rate} = 42.5\%$ (17/40)
    - Average across fractions: $\text{Mean Gap} = \frac{-0.6855 + -0.6855 + 0.0325}{3} = -0.4462 \approx -0.45$; $\text{Mean Win Rate} = \frac{45.0 + 45.0 + 42.5}{3} = 44.17\% \approx 44.2\%$

#### Cell-by-Cell Comparison:

| Original table value | Recalculated N=200 value | Difference | Source file | Verification status |
|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Mean gap: 4.40** | 4.4019 (rounded: 4.40) | 0.00 | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Attention \| Win rate: 76.7%** | 76.67% (rounded: 76.7%) | 0.0% | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| Mean gap: 2.32** | 2.3233 (rounded: 2.32) | 0.00 | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| Win rate: 58.3%** | 58.33% (rounded: 58.3%) | 0.0% | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| Mean gap: 2.21** | 2.2099 (rounded: 2.21) | 0.00 | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| Win rate: 63.3%** | 63.33% (rounded: 63.3%) | 0.0% | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| Mean gap: −0.45** | −0.4462 (rounded: −0.45) | 0.00 | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| Win rate: 44.2%** | 44.17% (rounded: 44.2%) | 0.0% | `hindi_faithfulness/faithfulness_summary.csv` | **Confirmed** (Exact Match) |

*Audit Finding on Sample Size:* The footnote in this table accurately specifies the true cohort: *"N = 40 sentences per fraction (20 pairs × 2)"*. This explicitly confirms that the experiment evaluated exactly the 20 spelling pairs of the pilot dataset.

---

### Table 5 (Paper Table VII): STABILITY–FAITHFULNESS CORRELATIONS

#### Original Paper Table Layout & Values:
| Model | Method | Spearman ρ | p-value |
|---|---|---|---|
| XLM-RoBERTa | Attention | 0.2704 | 0.2490 |
| XLM-RoBERTa | IG | 0.1583 | 0.5052 |
| MuRIL | Attention | −0.1611 | 0.4974 |
| MuRIL | IG | 0.0075 | 0.9749 |

*Footnote in original paper:* `"Spearman rank correlation between attribution stability (rank ρ) and faithfulness gap at 20% masking. N = 1280 pairs per cell; no correlation is significant at p < 0.05."*

#### Detailed Verification & Recalculation:
- **Correlated Variables**:
  - Variable 1: `visible_target_stability_rho` (Stage 7 visible-target Spearman rank stability).
  - Variable 2: `mean_faithfulness_gap_f20` (Mean top-vs-bottom faithfulness gap at 20% masking fraction).
- **Source Data**: `results/runs/historical_pilot_200/hindi_faithfulness/stability_faithfulness_relationship.csv` ($N = 20$ pairs per model-method combination).
- **Independent Statistical Recalculation (using SciPy / statsmodels)**:
  - **XLM-RoBERTa Attention ($N=20$)**:
    - Spearman $r_s = +0.270443$, two-tailed $p = 0.248956 \approx 0.2490$.
    - Pearson $r = +0.255745$, two-tailed $p = 0.2766$.
  - **XLM-RoBERTa Integrated Gradients ($N=20$)**:
    - Spearman $r_s = +0.158327$, two-tailed $p = 0.505191 \approx 0.5052$.
    - Pearson $r = +0.259207$, two-tailed $p = 0.2697$.
  - **MuRIL Attention ($N=20$)**:
    - Spearman $r_s = -0.161108$, two-tailed $p = 0.497424 \approx 0.4974$.
    - Pearson $r = -0.193910$, two-tailed $p = 0.4126$.
  - **MuRIL Integrated Gradients ($N=20$)**:
    - Spearman $r_s = +0.007548$, two-tailed $p = 0.974864 \approx 0.9749$.
    - Pearson $r = +0.018247$, two-tailed $p = 0.9394$.

#### Cell-by-Cell Comparison:

| Original table value | Recalculated N=200 value | Difference | Source file | Verification status |
|---|---|---|---|---|
| **XLM-RoBERTa \| Attention \| Spearman ρ: 0.2704** | 0.2704 (N=20) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| Attention \| p-value: 0.2490** | 0.2490 (df=18) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| Spearman ρ: 0.1583** | 0.1583 (N=20) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **XLM-RoBERTa \| IG \| p-value: 0.5052** | 0.5052 (df=18) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| Spearman ρ: −0.1611** | −0.1611 (N=20) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| Attention \| p-value: 0.4974** | 0.4974 (df=18) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| Spearman ρ: 0.0075** | 0.0075 (N=20) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |
| **MuRIL \| IG \| p-value: 0.9749** | 0.9749 (df=18) | 0.0000 | `hindi_faithfulness/stability_faithfulness_relationship.csv` | **Confirmed** (Exact Match) |

*Mathematical Proof of Sample Size:* In Spearman rank correlation testing, the $t$-statistic is given by $t = r_s \sqrt{\frac{N - 2}{1 - r_s^2}}$.
- For $r_s = 0.270443$ with $N = 20$ ($df = 18$):
  $$t = 0.270443 \times \sqrt{\frac{18}{1 - 0.270443^2}} = 0.270443 \times 4.4069 = 1.1918 \implies p = 0.248956 \approx 0.2490$$
- If $N$ had been $1,280$ ($df = 1278$):
  $$t = 0.270443 \times \sqrt{\frac{1278}{1 - 0.270443^2}} = 0.270443 \times 37.119 = 10.038 \implies p = 4.8 \times 10^{-23}$$
Because the reported $p$-value is $0.2490$, it proves beyond all mathematical doubt that the calculation was performed on $N = 20$ pairs.

---

## 4. Synthesis and Audit Questions

### 1. Which original values are confirmed?
**Every single numerical value across all five tables is confirmed:**
- **Table III**: All 6 values (4 single-subword percentages and 2 percentage-point changes) are confirmed.
- **Table IV**: All 6 mean $\Delta S$ values are confirmed to 4 decimal places.
- **Table V**: All 8 stability values (4 mean rank $\rho$ and 4 mean cosine similarities) are confirmed to 4 decimal places.
- **Table VI**: All 8 faithfulness intervention values (4 mean gaps and 4 win rates) are confirmed.
- **Table VII**: All 8 correlation values (4 Spearman $\rho$ and 4 $p$-values) are confirmed to 4 decimal places.

### 2. Which values differ?
**Zero numerical statistics differ.**  
The only discrepancy is textual/narrative: footnotes and body paragraphs in the original paper state that the spelling evaluations comprise $N = 1,280$ pairs, whereas every statistical formula was evaluated on the $N = 20$ spelling pairs of the 200-sample pilot.

### 3. Which values cannot be reconstructed?
**None.** Every metric was independently recomputed from `results/runs/historical_pilot_200/` and matched to full precision.

### 4. Is the original 200-sample data sufficient to reproduce all five tables?
**Yes, completely.** The experiment files under `results/runs/historical_pilot_200/` contain the full pair-level and summary tables required to regenerate all five original tables without missing a single data point.

---

## 5. Summary Verification Matrix

| Table # | Table Name | Total Cells Audited | Exact Matches | Discrepancies in Numbers | Cohort Used in Calculation | Reported N in Footnote | Actual N in Math |
|---|---|:---:|:---:|:---:|---|:---:|:---:|
| **Table III** | Single-Subword Coverage for Spelling Pairs | 6 | 6 / 6 (100%) | 0 | Spelling track | 1,280 | 20 |
| **Table IV** | Mean ΔS by Model and Pair Category | 6 | 6 / 6 (100%) | 0 | Context, Synonym, Spelling | 142 / 38 / 1,280 | 142 / 38 / 20 |
| **Table V** | Pooled Explanation Stability | 8 | 8 / 8 (100%) | 0 | Spelling track (Visible target) | 1,280 | 20 |
| **Table VI** | Faithfulness Intervention Summary | 8 | 8 / 8 (100%) | 0 | Spelling track (10%, 20%, 30%) | 40 sentences (20 pairs × 2) | 40 sentences (20 pairs × 2) |
| **Table VII**| Stability–Faithfulness Correlations | 8 | 8 / 8 (100%) | 0 | Spelling track ($f=0.20$) | 1,280 | 20 |
| **Total** | | **36** | **36 / 36 (100%)**| **0** | Pilot Cohort ($N=200$) | Mixed | Pilot Cohort ($N=200$) |

---

*Report compiled independently in accordance with strict cohort restriction protocols (excluding N=1,679, N=1,957, and N=12 expanded cohorts).*

