# Research Results: Authoritative Source of Truth

**Document Status**: Authoritative Reference Specification  
**Project**: Hindi Lexical Sensitivity Research (`hindi-lexical-sensitivity`)  
**Timestamp**: November 3, 2026  
**Primary Execution Baseline**: `results/runs/scaleup_rerun/`  
**Dataset Freeze Root**: `data/final/`  

---

## 1. Canonical Dataset Paths and Specifications

All primary and secondary experimental evaluations derive strictly from the frozen datasets in `data/final/`. The historical pilot is preserved separately in `data/raw/` and `results/runs/historical_pilot_200/`.

| Dataset Name | Relative Path | Sample Size ($N$) | Category Breakdown | Checksum (SHA-256) |
|---|---|---:|---|---|
| **Primary Adjudicated Benchmark** | `data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv` | 1,679 | `REALISTIC_SPELLING_ERROR`: 1,005<br>`SYNONYM_SUBSTITUTION`: 362<br>`VALID_WORD_CONTEXT`: 312 | `b769ccd82ee00b7930c8f32a7666e5d16897d0afc8c10c1cc97633334717fe18` |
| **Template Sensitivity Benchmark** | `data/final/TEMPLATE_SENSITIVITY_BENCHMARK.csv` | 1,957 | `REALISTIC_SPELLING_ERROR`: 1,260<br>`SYNONYM_SUBSTITUTION`: 385<br>`VALID_WORD_CONTEXT`: 312 | `b88160d39d1f7133391ff3aceff1faa2f157310833490e3765ae635c17e0155a` |
| **Auxiliary Multiword Probe** | `data/final/AUXILIARY_MULTIWORD_PROBE.csv` | 12 | `SYNONYM_SUBSTITUTION`: 8<br>`VALID_WORD_CONTEXT`: 3<br>`REALISTIC_SPELLING_ERROR`: 1 | `208aabab0056f8287297d8800462c703afc7506f0d3e5fd5e7ff08fc23cf096e` |
| **Complete Row Reconciliation** | `data/final/COMPLETE_2000_ROW_RECONCILIATION.csv` | 2,000 | 1,679 Primary + 278 Template + 12 Multiword + 31 Excluded | `2cbbf428e3a2c53f478a5dd9ca2cf245ee8feea3a2fa67fe53c07fc7e8140409` |
| **Adjudication Audit Log** | `data/final/ADJUDICATION_LOG.csv` | 23 | 23 formal edge-case adjudication entries | `cf12e09b85a3a7f83e29f3775ec32b9c3f25e903bc1026046e7f7223e74b9314` |
| **Historical Pilot Benchmark** | `data/raw/hindi_lexical_sensitivity_cleaned.xlsx` | 200 | 142 Context, 38 Synonym, 20 Spelling | `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44` |

---

## 2. Canonical Experiment Configurations

All inference pipelines were executed on frozen pretrained masked language model checkpoints using the exact parameters recorded below:

### 2.1 Model Checkpoints
- **MuRIL**: `google/muril-base-cased` (237,755,045 parameters, BERT architecture, WordPiece tokenization, 197,285 vocabulary size).
- **XLM-RoBERTa**: `FacebookAI/xlm-roberta-base` (278,295,186 parameters, RoBERTa architecture, SentencePiece BPE tokenization, 250,002 vocabulary size).
- **Execution Mode**: Evaluation only (`model.eval()`, frozen weights, `torch.no_grad()` for scoring/stability; autograd enabled only for Integrated Gradients).

### 2.2 Pseudo-Log-Likelihood (PLL) Scoring Configuration
- **Script**: `src/models/mlm_scoring.py` / `scripts/execute_scaleup_rerun.py`
- **Scoring Protocol**: Exact token-by-token masked language model log-probability accumulation.
- **Metric**: $\text{MeanLogP} = \frac{1}{|S|} \sum_{t \in S} \log P(w_t \mid S_{\setminus t})$
- **Batch Size**: 32 on CUDA device (`cuda:0`).
- **Precision**: `torch.float32`.

### 2.3 Feature Attribution & Explanation Stability Configuration
- **Script**: `src/analysis/explanation_stability.py` / `scripts/execute_scaleup_rerun.py`
- **Methods**:
  1. *Attention*: Layer-11 (last-layer) mean self-attention weights across all 12 attention heads.
  2. *Integrated Gradients (IG)*: Path integral from zero-embedding baseline to token embeddings.
     - **Integration Steps**: **$n_{\text{steps}} = 20$** (configured via `DEFAULT_N_STEPS = 20`).
     - **Baseline**: Zero-embedding baseline with padding tokens.
- **Scoring Protocols**:
  - *Visible-Target Protocol* (Canonical): Target word token remains unmasked and visible in both original and perturbed sentences. Context attributions are evaluated across identically aligned context tokens.
  - *Target-Masked Protocol* (Artifact Diagnostic): Target word masked in both sentences; produces trivial stability ($\rho = 1.0, \cos = 1.0$) due to identical masked contexts.

### 2.4 Faithfulness Erasure Intervention Configuration
- **Script**: `src/analysis/hindi_faithfulness.py` / `scripts/execute_scaleup_rerun.py`
- **Erasure Budgets**: $f \in \{0.10, 0.20, 0.30\}$ of non-target context tokens ($k = \lceil f \cdot |C| \rceil$).
- **Intervention Baselines**:
  1. `top_k`: Mask top-$k$ highest-attribution context tokens.
  2. `bottom_k`: Mask bottom-$k$ lowest-attribution context tokens.
  3. `random_k`: Mask random-$k$ context tokens (averaged over 5 independent random trials).
- **Evaluation Target**: Pretrained target token logit drop: $\Delta \text{Logit} = \text{Logit}_{\text{masked}} - \text{Logit}_{\text{unmasked}}$.
- **Faithfulness Gap**: $\text{Gap} = \Delta \text{Logit}_{\text{top}} - \Delta \text{Logit}_{\text{bottom}}$.
- **Win Rate**: Proportion of sentences where $\text{Gap} > 0$ (top-k erasure produces greater degradation than bottom-k).

---

## 3. Canonical Result CSV Files

The authoritative outputs are organized under `results/runs/scaleup_rerun/`:

| Output File Path | Rows | Purpose & Contents |
|---|---:|---|
| `tokenization/tokenization_results.csv` | 3,358 | Token counts, target subwords, and offset maps for 1,679 pairs $\times 2$ models. |
| `scoring/pll_scoring_results.csv` | 3,358 | PLL sums, MeanLogP, $\Delta \text{MeanLogP}$, and preference labels. |
| `analysis/combined_pair_level_results.csv` | 3,358 | Merged tokenization and PLL results with pair metadata. |
| `analysis/descriptive_statistics.csv` | 12 | Summary statistics (mean, median, SD, IQR, min, max, preference counts) by track. |
| `analysis/model_comparison.csv` | 4 | Cross-model concordance, directional agreement rates, and Spearman correlations. |
| `analysis/correlation_results.csv` | 64 | Complete hypothesis test matrix with raw p-values, 95% CIs, and Benjamini-Hochberg FDR flags. |
| `stability/stability_pair_level.csv` | 4,020 | Pair-level stability evaluations (1,005 spelling pairs $\times 2$ models $\times 2$ methods). |
| `stability/stability_summary.csv` | 12 | Aggregate stability metrics by method, model, and subset (all-scorable vs. strict single-subword). |
| `faithfulness/faithfulness_pair_level.csv` | 72,360 | Full intervention records (2,010 sentences $\times 2$ methods $\times 3$ fractions $\times 6$ baselines). |
| `faithfulness/faithfulness_summary.csv` | 24 | Mean logit drops, faithfulness gaps, and win rates by fraction, method, model, and subset. |
| `faithfulness/stability_faithfulness_relationship.csv` | 4,020 | Merged pair-level visible-target stability vs. mean faithfulness gap at $f=0.20$. |
| `dashboard_data/tokenization_summary.csv` | 6 | Clean summary table for tokenization dynamics. |
| `dashboard_data/scoring_summary.csv` | 6 | Clean summary table for PLL shifts and preference rates. |
| `dashboard_data/stability_summary.csv` | 12 | Clean summary table for explanation stability. |
| `dashboard_data/faithfulness_summary.csv` | 24 | Clean summary table for faithfulness metrics. |
| `dashboard_data/stability_faithfulness_relationship.csv` | 4,020 | Clean correlation dataset for RQ5. |
| `template_sensitivity/analysis/descriptive_statistics.csv` | 12 | Descriptive statistics for Template Benchmark ($N=1,957$). |
| `template_sensitivity/analysis/model_comparison.csv` | 4 | Cross-model concordance for Template Benchmark ($N=1,957$). |
| `auxiliary_probe/analysis/combined_pair_level_results.csv` | 24 | Complete pair-level evaluations for Auxiliary Multiword Probe ($N=12 \times 2$). |
| `auxiliary_probe/analysis/model_comparison.csv` | 4 | Cross-model comparison for Auxiliary Multiword Probe ($N=12$). |

---

## 4. Canonical Figures

All publication figures are stored in `results/runs/scaleup_rerun/figures/` (mirrored to `outputs/analysis/figures/`):

| Figure File | Dimensions / Format | Content & Research Domain |
|---|---|---|
| `fig1_delta_meanlp_by_track.png` | PNG (65 KB) | Violin/box distributions of $\Delta \text{MeanLogP}$ across tracks for MuRIL vs. XLM-R (RQ2). |
| `fig2_token_delta_vs_meanlp.png` | PNG (143 KB) | Sentence-level token count inflation vs. $\Delta \text{MeanLogP}$ scatter with regression fit. |
| `fig3_target_token_delta_vs_meanlp.png` | PNG (140 KB) | Target-word subword fragmentation vs. $\Delta \text{MeanLogP}$ scatter (RQ1). |
| `fig4_model_comparison_scatter.png` | PNG (270 KB) | Cross-model $\Delta \text{MeanLogP}$ correlation (MuRIL vs. XLM-R) faceted by track (RQ3). |
| `fig5_direction_agreement.png` | PNG (43 KB) | Cross-model directional preference agreement rates (%) across experimental tracks (RQ3). |
| `fig6_explanation_stability.png` | PNG (219 KB) | Explanation stability: Mean rank $\rho$ and cosine similarity for Attention vs. IG (RQ4). |
| `fig7_faithfulness_interventions.png` | PNG (322 KB) | Faithfulness gaps and win rates across erasure budgets $f \in \{0.10, 0.20, 0.30\}$ (RQ4). |
| `fig8_stability_vs_faithfulness.png` | PNG (652 KB) | Stability vs. Faithfulness decoupling scatter plots faceted by model, method, and subset (RQ5). |

---

## 5. Major Reported Results: Traceability Matrix

Every key quantitative finding reported in the research paper and workbook maps to an exact source file and row:

| Research Question / Table | Reported Metric | Numerical Value | Authoritative Source File & Key |
|---|---|---|---|
| **RQ1 / Table 1** | MuRIL Spelling Single-Subword Coverage | Orig: 91.7%, Cont: 20.1%, $\Delta$: −71.6 pp | `dashboard_data/tokenization_summary.csv` (Row 3) |
| **RQ1 / Table 1** | XLM-R Spelling Single-Subword Coverage | Orig: 62.3%, Cont: 6.4%, $\Delta$: −55.9 pp | `dashboard_data/tokenization_summary.csv` (Row 0) |
| **RQ1 / Table 1** | MuRIL Spelling Target Tokens | Orig: 1.12, Cont: 2.25, $\Delta$: +1.13 | `dashboard_data/tokenization_summary.csv` (Row 3) |
| **RQ1 / Table 1** | XLM-R Spelling Target Tokens | Orig: 1.63, Cont: 2.67, $\Delta$: +1.04 | `dashboard_data/tokenization_summary.csv` (Row 0) |
| **RQ2 / Table 2** | XLM-R Valid-Word Context Mean $\Delta S$ | −1.0831 (Preferred Orig: 85.6%) | `dashboard_data/scoring_summary.csv` (Row 2) |
| **RQ2 / Table 2** | XLM-R Synonym Substitution Mean $\Delta S$ | −0.0098 (Preferred Orig: 50.6%) | `dashboard_data/scoring_summary.csv` (Row 1) |
| **RQ2 / Table 2** | XLM-R Spelling Error Mean $\Delta S$ | −0.8864 (Preferred Orig: 76.4%) | `dashboard_data/scoring_summary.csv` (Row 0) |
| **RQ2 / Table 2** | MuRIL Valid-Word Context Mean $\Delta S$ | −1.8470 (Preferred Orig: 92.3%) | `dashboard_data/scoring_summary.csv` (Row 5) |
| **RQ2 / Table 2** | MuRIL Synonym Substitution Mean $\Delta S$ | −0.1787 (Preferred Orig: 59.4%) | `dashboard_data/scoring_summary.csv` (Row 4) |
| **RQ2 / Table 2** | MuRIL Spelling Error Mean $\Delta S$ | −1.2045 (Preferred Orig: 91.0%) | `dashboard_data/scoring_summary.csv` (Row 3) |
| **RQ3 / Table 3** | Global Cross-Model Directional Agreement | 73.67% ($N=1,679$) | `analysis/model_comparison.csv` (Row 0) |
| **RQ3 / Table 3** | Global Cross-Model Spearman $r_s$ | +0.5496 ($p < 10^{-15}, N=1,679$) | `analysis/model_comparison.csv` (Row 0) |
| **RQ3 / Table 3** | Spelling Cross-Model Directional Agreement | 83.18% ($N=1,005$) | `analysis/model_comparison.csv` (Row 3) |
| **RQ3 / Table 3** | Spelling Cross-Model Spearman $r_s$ | +0.5513 ($p < 10^{-15}, N=1,005$) | `analysis/model_comparison.csv` (Row 3) |
| **RQ4 / Table 4** | XLM-R Attention Pooled Stability | Rank $\rho$: 0.6258, Cosine: 0.9353 ($N=1,005$) | `dashboard_data/stability_summary.csv` (Row 0) |
| **RQ4 / Table 4** | XLM-R IG Pooled Stability | Rank $\rho$: 0.3319, Cosine: 0.8890 ($N=1,005$) | `dashboard_data/stability_summary.csv` (Row 3) |
| **RQ4 / Table 4** | MuRIL Attention Pooled Stability | Rank $\rho$: 0.8027, Cosine: 0.9518 ($N=1,005$) | `dashboard_data/stability_summary.csv` (Row 6) |
| **RQ4 / Table 4** | MuRIL IG Pooled Stability | Rank $\rho$: 0.2560, Cosine: 0.9818 ($N=1,005$) | `dashboard_data/stability_summary.csv` (Row 9) |
| **RQ4 / Table 4** | MuRIL Attention Strict Single-Subword Stability | Rank $\rho$: 0.8053, Cosine: 0.9725 ($N=197$) | `dashboard_data/stability_summary.csv` (Row 7) |
| **RQ4 / Table 4** | XLM-R Attention Strict Single-Subword Stability | Rank $\rho$: 0.6306, Cosine: 0.9349 ($N=52$) | `dashboard_data/stability_summary.csv` (Row 1) |
| **RQ4 / Table 5** | XLM-R Attention Faithfulness (3-Fraction Avg) | Mean Gap: +3.02, Win Rate: 65.6% | `dashboard_data/faithfulness_summary.csv` (Rows 0-2) |
| **RQ4 / Table 5** | XLM-R IG Faithfulness (3-Fraction Avg) | Mean Gap: +2.54, Win Rate: 62.4% | `dashboard_data/faithfulness_summary.csv` (Rows 6-8) |
| **RQ4 / Table 5** | MuRIL Attention Faithfulness (3-Fraction Avg) | Mean Gap: −1.31, Win Rate: 39.6% | `dashboard_data/faithfulness_summary.csv` (Rows 12-14) |
| **RQ4 / Table 5** | MuRIL IG Faithfulness (3-Fraction Avg) | Mean Gap: −0.63, Win Rate: 48.7% | `dashboard_data/faithfulness_summary.csv` (Rows 18-20) |
| **RQ5 / Table 6** | XLM-R Attention Pooled Correlation | Spearman $\rho = +0.0607 (p=0.0612)$; Pearson $r = +0.0564 (p=0.0816)$ | `dashboard_data/stability_faithfulness_relationship.csv` ($N=953$) |
| **RQ5 / Table 6** | XLM-R IG Pooled Correlation | Spearman $\rho = +0.0632 (p=0.0510)$; Pearson $r = +0.0495 (p=0.1270)$ | `dashboard_data/stability_faithfulness_relationship.csv` ($N=953$) |
| **RQ5 / Table 6** | MuRIL Attention Pooled Correlation | Spearman $\rho = -0.0442 (p=0.2099)$; **Pearson $r = -0.0790 (p=0.0248)$** | `dashboard_data/stability_faithfulness_relationship.csv` ($N=808$) |
| **RQ5 / Table 6** | MuRIL Attention Strict Correlation | **Spearman $\rho = -0.1924 (p=0.0067)$**; Pearson $r = -0.1129 (p=0.1141)$ | `dashboard_data/stability_faithfulness_relationship.csv` ($N=197$) |
| **RQ5 / Table 6** | XLM-R Attention Strict Correlation | Spearman $\rho = +0.2472 (p=0.0773)$; **Pearson $r = +0.2949 (p=0.0338)$** | `dashboard_data/stability_faithfulness_relationship.csv` ($N=52$) |
| **RQ5 / Table 6** | MuRIL IG Pooled Correlation | Spearman $\rho = +0.0214 (p=0.5442)$; Pearson $r = +0.0290 (p=0.4108)$ | `dashboard_data/stability_faithfulness_relationship.csv` ($N=808$) |
| **Section 9** | Template Benchmark Agreement ($N=1,957$) | Agreement: 71.28%, Spearman $r_s = +0.5344$ | `template_sensitivity/analysis/model_comparison.csv` |
| **Section 10** | Auxiliary Probe Agreement ($N=12$) | Agreement: 41.67%, Spearman $r_s = +0.6364$ | `auxiliary_probe/analysis/model_comparison.csv` |

