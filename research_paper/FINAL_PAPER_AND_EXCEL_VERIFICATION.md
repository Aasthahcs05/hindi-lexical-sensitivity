# Final Paper and Excel Verification Report

**Project Title**: *Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi (D-SAFE)*  
**Verification Stage**: Stage 11 — Comprehensive Manuscript Revision & Excel Results Workbook Verification  
**Authoritative Experimental Run**: `results/runs/scaleup_rerun/`  
**Frozen Dataset Directory**: `data/final/`  
**Date & Timestamp**: 2026-11-03 (Verified)  
**Status**: **VERIFIED & FULLY SYNCHRONIZED**

---

## 1. Executive Summary & Verification Scope

This report documents the rigorous verification of the revised research manuscript, updated figure manifest, reproducibility guidelines, expanded experimental notebook, and newly generated 13-worksheet Excel results workbook (`expanded_experimental_results.xlsx`).

All numerical values, sample sizes, correlation metrics, effect sizes, and p-values have been audited directly against the authoritative computational rerun outputs in `results/runs/scaleup_rerun/` and frozen datasets in `data/final/`. The historical pilot ($N=200$) is preserved strictly for historical context, and the older baseline PDF (`final_research_paper.pdf`) has been treated exclusively as a structural and explanatory reference without adopting its obsolete sample sizes or exploratory conclusions.

### Guardrails Compliance Summary:
- [x] **Zero Model Inference Rerun**: Pretrained models remained untouched; no forward passes or GPU retraining performed.
- [x] **Zero Downloads**: No external models, tokenizers, or datasets downloaded.
- [x] **Frozen Datasets Untouched**: `data/final/*.csv` files maintain exact cryptographic and byte-level integrity.
- [x] **Experimental Result CSVs Untouched**: All files in `results/runs/scaleup_rerun/` remain strictly read-only and immutable.
- [x] **Methodology and Hypotheses Preserved**: RQs (RQ1–RQ5), model architectures (MuRIL and XLM-RoBERTa), and evaluation metrics preserved intact.
- [x] **Original Pilot Notebooks Untouched**: All seven original notebooks (`notebooks/01_*.ipynb` through `notebooks/07_*.ipynb`) retain their original timestamps and contents.
- [x] **Single Expanded Notebook Maintained**: `notebooks/expanded_experimental_results.ipynb` was corrected in-place; no duplicate notebook was created.
- [x] **Proper Publication Qualification**: Limitations, Out-of-Distribution (OOD) syntactic shifts, multi-subword averaging assumptions, and base-scale MLM scope are explicitly documented without unqualified publication claims.

---

## 2. Experimental Cohorts and Sample Size Verification

Every cohort is strictly segregated with unambiguous denominators throughout the manuscript, figures, notebook, and Excel sheets:

| Cohort Identifier | Sample Size ($N$ Minimal Pairs) | Evaluation Count ($2 \times N$ Sentences) | Composition & Track Breakdown | Methodological & Scientific Role |
|---|---|---|---|---|
| **Primary Benchmark** | **1,679** | 3,358 | - `REALISTIC_SPELLING_ERROR`: $1,005$ pairs (59.86%)<br>- `SYNONYM_SUBSTITUTION`: $362$ pairs (21.56%)<br>- `VALID_WORD_CONTEXT`: $312$ pairs (18.58%) | Authoritative core benchmark. 100% human-verified and adjudicated. Zero template repetitions. |
| **Secondary Template Sensitivity Benchmark** | **1,957** | 3,914 | - `REALISTIC_SPELLING_ERROR`: $1,260$ pairs (64.38%)<br>- `SYNONYM_SUBSTITUTION`: $385$ pairs (19.67%)<br>- `VALID_WORD_CONTEXT`: $312$ pairs (15.94%) | Contains Primary Benchmark ($N=1,679$) plus 278 template variants across 278 frames. **Explicitly NOT an independent dataset.** |
| **Auxiliary Multiword Probe** | **12** | 24 | - Gender/Number Agreement Ripple: $6$ pairs (50.0%)<br>- Repeated-Target Ambiguity: $4$ pairs (33.3%)<br>- Postpositional Insertion: $1$ pair (8.3%)<br>- Collocational Light-Verb Change: $1$ pair (8.3%) | Fine-grained 4-category taxonomy evaluating multiword syntactic ripples and token alignment edge cases. |
| **Historical Preliminary Pilot** | **200** | 400 | - `VALID_WORD_CONTEXT`: $142$ pairs (71.0%)<br>- `SYNONYM_SUBSTITUTION`: $38$ pairs (19.0%)<br>- `REALISTIC_SPELLING_ERROR`: $20$ pairs (10.0%) | Historical exploratory pilot preserved in `results/runs/historical_pilot_200/` for archival provenance only. |
| **Complete Reconciled Pool** | **2,000** | 4,000 | - Primary Included: $1,679$<br>- Template-Only Included: $278$<br>- Auxiliary-Only Included: $12$<br>- Excluded / Flagged: $31$ | Complete reconciliation audit: $1679 + 278 + 12 + 31 = 2000$. Exactly 0 unclassified or missing rows. |

---

## 3. Numerical Verification: Manuscript Tables vs. Authoritative Source CSVs

Every numerical table in the revised manuscript (`paper/research_paper.md`) has been cross-checked against its authoritative CSV file in `results/runs/scaleup_rerun/`:

### Table 1: Subword Tokenization & Target Word Fragmentation ($N=1,679$)
*Source*: `results/runs/scaleup_rerun/dashboard_data/tokenization_summary.csv`
- **MuRIL Single-Subword Collapse**: $91.7\% \to 20.1\%$ ($-71.6$ percentage points) on spelling errors.
- **XLM-RoBERTa Single-Subword Collapse**: $62.3\% \to 6.4\%$ ($-55.9$ percentage points) on spelling errors.
- **Sentence-Level Token Inflation**: $+1.13$ tokens in MuRIL; $+1.04$ tokens in XLM-RoBERTa.
- **Target Word Subword Inflation**: $1.12 \to 2.25$ (+1.13) in MuRIL; $1.63 \to 2.67$ (+1.04) in XLM-RoBERTa.
- **Audit Result**: **100% MATCH** across all 12 reported metrics.

### Table 2: Length-Normalized Plausibility Shifts ($\Delta \text{MeanLogP}$) ($N=1,679$)
*Source*: `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv`
- **MuRIL Spelling Errors** ($N=1,005$): Mean $\Delta = -1.2045$, Median $\Delta = -0.8892$, Std $= 1.3526$, IQR $= 1.7256$, Min $= -6.8610$, Max $= +2.3473$, Original Preferred $= 836$ ($83.2\%$).
- **MuRIL Context Contrasts** ($N=312$): Mean $\Delta = -1.8470$, Median $\Delta = -1.6755$, Std $= 1.3965$, IQR $= 1.6648$, Original Preferred $= 294$ ($94.2\%$).
- **MuRIL Synonym Substitutions** ($N=362$): Mean $\Delta = -0.1787$, Median $\Delta = -0.1049$, Std $= 0.8545$, IQR $= 0.8320$, Original Preferred $= 213$ ($58.8\%$).
- **XLM-RoBERTa Spelling Errors** ($N=1,005$): Mean $\Delta = -0.8864$, Median $\Delta = -0.7752$, Std $= 1.2929$, IQR $= 1.6561$, Min $= -6.4884$, Max $= +3.6106$, Original Preferred $= 768$ ($76.4\%$).
- **XLM-RoBERTa Context Contrasts** ($N=312$): Mean $\Delta = -1.0831$, Median $\Delta = -0.9464$, Std $= 1.2195$, IQR $= 1.4564$, Original Preferred $= 258$ ($82.7\%$).
- **XLM-RoBERTa Synonym Substitutions** ($N=362$): Mean $\Delta = -0.0098$, Median $\Delta = -0.0084$, Std $= 1.0110$, IQR $= 0.9386$, Original Preferred $= 183$ ($50.6\%$).
- **Audit Result**: **100% MATCH** across all reported values.

### Table 3: Cross-Model Comparison on $\Delta \text{MeanLogP}$ ($N=1,679$)
*Source*: `results/runs/scaleup_rerun/analysis/model_comparison.csv`
- **Overall Benchmark** ($N=1,679$): Directional Agreement $= 73.67\%$, Both Negative $= 1,055$, Both Positive $= 182$, XLM Neg / MuRIL Pos $= 154$, XLM Pos / MuRIL Neg $= 288$, Spearman $r_s = +0.5496, p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$.
- **Valid Word Context** ($N=312$): Agreement $= 84.62\%$, Spearman $r_s = +0.4590, p < 10^{-15}$, 95% CI $[0.3666, 0.5424]$.
- **Realistic Spelling Error** ($N=1,005$): Agreement $= 75.12\%$, Spearman $r_s = +0.5513, p < 10^{-15}$, 95% CI $[0.5067, 0.5929]$.
- **Synonym Substitution** ($N=362$): Agreement $= 60.22\%$, Spearman $r_s = +0.2271, p = 1.3 \times 10^{-5}$, 95% CI $[0.1269, 0.3226]$.
- **Audit Result**: **100% MATCH**.

### Table 4: Visible-Target Explanation Stability ($N=1,005$ Spelling Pairs)
*Source*: `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv`
- **XLM-RoBERTa Attention (Pooled $N=1,005$)**: Mean $\rho = 0.6258$, Median $\rho = 0.7333$, Mean Cosine $= 0.9353$, Median Cosine $= 0.9550$.
- **XLM-RoBERTa Attention (Strict Single $N=52$)**: Mean $\rho = 0.6306$, Median $\rho = 0.7746$, Mean Cosine $= 0.9349$, Median Cosine $= 0.9598$.
- **XLM-RoBERTa IG (Pooled $N=1,005$)**: Mean $\rho = 0.3319$, Median $\rho = 0.4000$, Mean Cosine $= 0.8890$, Median Cosine $= 0.9204$.
- **XLM-RoBERTa IG (Strict Single $N=52$)**: Mean $\rho = 0.4210$, Median $\rho = 0.5442$, Mean Cosine $= 0.9026$, Median Cosine $= 0.9313$.
- **MuRIL Attention (Pooled $N=1,005$)**: Mean $\rho = 0.8027$, Median $\rho = 0.8857$, Mean Cosine $= 0.9518$, Median Cosine $= 0.9733$.
- **MuRIL Attention (Strict Single $N=197$)**: Mean $\rho = 0.8053$, Median $\rho = 0.9000$, Mean Cosine $= 0.9725$, Median Cosine $= 0.9861$.
- **MuRIL IG (Pooled $N=1,005$)**: Mean $\rho = 0.2560$, Median $\rho = 0.3000$, Mean Cosine $= 0.9818$, Median Cosine $= 0.9867$.
- **MuRIL IG (Strict Single $N=197$)**: Mean $\rho = 0.3471$, Median $\rho = 0.4000$, Mean Cosine $= 0.9868$, Median Cosine $= 0.9885$.
- **Stage 6 Artifact Documented**: All conditions show masked target $\rho = 1.0000$ and cosine $= 1.0000$, documenting the artifact resolved by the Visible-Target protocol.
- **Audit Result**: **100% MATCH**.

### Table 5: Faithfulness Interventions under Discrete Context Erasure ($N=2,010$ Sentences)
*Source*: `results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv`
- **XLM-RoBERTa Attention (All-Scorable $N=2,010$)**:
  - $f=0.10$: Top Drop $= -6.2969$, Bottom Drop $= -8.7344$, Gap $= \mathbf{+2.4374}$, Win Rate vs Bottom $= \mathbf{63.53\%}$, vs Random $= 52.49\%$.
  - $f=0.20$: Top Drop $= -6.2915$, Bottom Drop $= -9.0881$, Gap $= \mathbf{+2.7966}$, Win Rate vs Bottom $= \mathbf{65.77\%}$, vs Random $= 55.92\%$.
  - $f=0.30$: Top Drop $= -4.4711$, Bottom Drop $= -8.2846$, Gap $= \mathbf{+3.8134}$, Win Rate vs Bottom $= \mathbf{67.46\%}$, vs Random $= 57.46\%$.
- **XLM-RoBERTa IG (All-Scorable $N=2,010$)**:
  - $f=0.10$: Gap $= +1.9847$, Win Rate $= 59.75\%$.
  - $f=0.20$: Gap $= +2.2477$, Win Rate $= 62.24\%$.
  - $f=0.30$: Gap $= +3.3957$, Win Rate $= 65.12\%$.
- **MuRIL Attention (All-Scorable $N=2,010$)**:
  - $f=0.10$: Gap $= -2.0168$, Win Rate $= 33.88\%$.
  - $f=0.20$: Gap $= -2.3213$, Win Rate $= 35.42\%$.
  - $f=0.30$: Gap $= +0.4001$, Win Rate $= 49.60\%$.
- **MuRIL IG (All-Scorable $N=2,010$)**:
  - $f=0.10$: Gap $= -0.2998$, Win Rate $= 49.90\%$.
  - $f=0.20$: Gap $= -0.5137$, Win Rate $= 49.40\%$.
  - $f=0.30$: Gap $= -1.0845$, Win Rate $= 46.72\%$.
- **Strict Single-Subword Subsets**:
  - XLM-R Attention Strict ($N=104, f=0.20$): Gap $= +3.6064$, Win Rate $= 69.23\%$.
  - XLM-R IG Strict ($N=104, f=0.20$): Gap $= +2.8543$, Win Rate $= 64.42\%$.
  - MuRIL Attention Strict ($N=394, f=0.20$): Gap $= -1.1714$, Win Rate $= 40.36\%$.
  - MuRIL IG Strict ($N=394, f=0.20$): Gap $= -1.5219$, Win Rate $= 47.46\%$.
- **Audit Result**: **100% MATCH**.

---

## 4. Specific Verification: Table 6 and RQ5 Nuanced Interpretation

The user prompt explicitly specified:
> "Do not state that all stability-faithfulness correlations are non-significant. The reported MuRIL Attention results include:
> - Pooled Pearson: r = -0.0790, p = 0.0248.
> - Strict single-subword Spearman: rho = -0.1924, p = 0.0067.
> The appropriate overall interpretation is that there is no consistent positive association between explanation stability and faithfulness. Some weak negative associations occur for MuRIL Attention, while other combinations are non-significant.
> Do not claim that the results prove independence, establish causation, or rule out all sample-size limitations."

### Comprehensive Verification of Table 6 Correlations:
*Source*: `results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv`

| Model Checkpoint | Explanation Method | Evaluated Subset | Sample Size ($N$) | Spearman $r_s$ | $p$-value ($r_s$) | Pearson $r$ | $p$-value ($r$) | Exact Verified Statistical Interpretation |
|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | Attention | Pooled (All-Scorable) | 953 | **+0.0607** | $0.0612$ | +0.0564 | $0.0816$ | Non-Significant ($p > 0.05$) |
| **XLM-RoBERTa** | Attention | Strict Single-Subword | 52 | **+0.2472** | $0.0773$ | **+0.2949** | **$0.0338$** | Non-Significant Rank ($p > 0.05$); Weak Positive Linear ($p < 0.05$) |
| **XLM-RoBERTa** | Integrated Gradients | Pooled (All-Scorable) | 953 | **+0.0632** | $0.0510$ | +0.0495 | $0.1270$ | Non-Significant ($p > 0.05$) |
| **XLM-RoBERTa** | Integrated Gradients | Strict Single-Subword | 52 | **+0.1647** | $0.2434$ | +0.1464 | $0.3005$ | Non-Significant ($p > 0.05$) |
| **MuRIL** | Attention | Pooled (All-Scorable) | 808 | **-0.0442** | $0.2099$ | **-0.0790** | **$0.0248$** | Non-Significant Rank ($p > 0.05$); **Weak Inverse Linear ($p < 0.05$)** |
| **MuRIL** | Attention | Strict Single-Subword | 197 | **-0.1924** | **$0.0067$** | -0.1129 | $0.1141$ | **Weak Inverse Rank ($r_s < 0, p < 0.01$)**; Non-Significant Linear |
| **MuRIL** | Integrated Gradients | Pooled (All-Scorable) | 808 | **+0.0214** | $0.5442$ | +0.0290 | $0.4108$ | Non-Significant ($p > 0.05$) |
| **MuRIL** | Integrated Gradients | Strict Single-Subword | 197 | **+0.0344** | $0.6316$ | -0.0037 | $0.9592$ | Non-Significant ($p > 0.05$) |

### Compliance Checks Across Deliverables:
1. **Manuscript (`research_paper.md`)**:
   - Abstract, Section 1, Section 5.6, Section 6.1, Section 8, and Section 10 have been thoroughly revised.
   - Zero claims stating "all correlations are non-significant" remain.
   - MuRIL Attention pooled Pearson ($r = -0.0790, p = 0.0248$) and strict Spearman ($\rho = -0.1924, p = 0.0067$) are explicitly documented in prose and tables.
   - Core finding formulated as: **no consistent positive association between explanation stability and faithfulness**.
   - No claims of mathematical proof of independence, causation, or ruling out all sample-size limitations are made.
2. **Notebook (`notebooks/expanded_experimental_results.ipynb`)**:
   - Cell 0 (Roadmap item 8), Cell 29, Cell 30 (code interpretation logic), Cell 32 (narrative synthesis), and Cell 40 (major findings) are updated to communicate identical nuanced conclusions.
3. **Figure Manifest (`figure_manifest.md`)**:
   - Figure 8 caption updated to document both the weak negative MuRIL Attention associations and the non-significant conditions.
4. **Excel Workbook (`expanded_experimental_results.xlsx`)**:
   - Sheet 11 presents the complete correlation matrix, chart, and detailed notes incorporating these exact statistical results and nuances.

---

## 5. Canonical Figure Verification (Figures 1–8)

All eight canonical figures exist in `results/runs/scaleup_rerun/figures/` and are resolved dynamically in both `paper/` and `research_paper/`:

| Figure ID | Canonical Image File | Resolution | Key Finding Visualized | Render in DOCX | Render in PDF |
|---|---|---|---|---|---|
| **Figure 1** | `fig1_delta_meanlp_by_track.png` | 1800×1200 | Boxplots of signed $\Delta \text{MeanLogP}$ by track across MuRIL and XLM-RoBERTa | **Verified** | **Verified** |
| **Figure 2** | `fig2_token_delta_vs_meanlp.png` | 1800×1200 | Sentence token delta vs. plausibility shifts across 3,358 evaluations | **Verified** | **Verified** |
| **Figure 3** | `fig3_target_token_delta_vs_meanlp.png` | 1800×1200 | Target-specific token inflation vs. plausibility penalties | **Verified** | **Verified** |
| **Figure 4** | `fig4_model_comparison_scatter.png` | 1800×1200 | Cross-model scatter plot (XLM-R vs. MuRIL $\Delta \text{MeanLogP}$, $r_s = +0.5496$) | **Verified** | **Verified** |
| **Figure 5** | `fig5_direction_agreement.png` | 1800×1200 | Directional agreement proportions across tracks (84.62% context, 75.12% spelling, 60.22% synonym) | **Verified** | **Verified** |
| **Figure 6** | `fig6_explanation_stability.png` | 3000×1350 | Visible-target rank $\rho$ vs. cosine similarity (Attention vs. IG) | **Verified** | **Verified** |
| **Figure 7** | `fig7_faithfulness_interventions.png` | 3300×1350 | Faithfulness gaps and win rates across masking fractions $f \in \{0.10, 0.20, 0.30\}$ | **Verified** | **Verified** |
| **Figure 8** | `fig8_stability_vs_faithfulness.png` | 3300×1440 | Scatter plots of visible-target stability vs. mean faithfulness gap ($f=0.20$) | **Verified** | **Verified** |

- Total embedded images in DOCX: **8**.
- Total embedded images in PDF: **8**.
- Numbering, cross-references, and text discussions verified throughout.

---

## 6. Excel Workbook Verification (`expanded_experimental_results.xlsx`)

The generated workbook `paper/expanded_experimental_results.xlsx` (59,279 bytes) was verified using OpenPyXL:

| Sheet # | Worksheet Title | Dimensions | Freeze Panes | Auto-Filter Range | Native Chart Type | Source Data Citation |
|---|---|---|---|---|---|---|
| **1** | `Dataset Overview & Distribution` | `A1:F42` | `A6` | `A14:F31` | Clustered Column (Track Counts) | `data/final/COMPLETE_2000_ROW_RECONCILIATION.csv` |
| **2** | `Tokenization & Fragmentation` | `A1:L20` | `A5` | `A4:L10` | Clustered Column (Subword Collapse) | `scaleup_rerun/dashboard_data/tokenization_summary.csv` |
| **3** | `MuRIL PLL Results` | `A1:O8` | `A5` | `A4:O8` | Clustered Column ($\Delta$MeanLogP) | `scaleup_rerun/analysis/descriptive_statistics.csv` |
| **4** | `XLM-R PLL Results` | `A1:O8` | `A5` | `A4:O8` | Clustered Column ($\Delta$MeanLogP) | `scaleup_rerun/analysis/descriptive_statistics.csv` |
| **5** | `Cross-Model Comparison` | `A1:L19` | `A5` | `A4:L8` | Clustered Column (Agreement & $r_s$) | `scaleup_rerun/analysis/model_comparison.csv` |
| **6** | `Explanation Stability` | `A1:K27` | `A5` | `A4:K16` | Clustered Column (Rank $\rho$ vs Cosine) | `scaleup_rerun/dashboard_data/stability_summary.csv` |
| **7** | `Strict Single-Subword Stability` | `A1:M38` | `A6` | `A5:H9` | Clustered Column (Strict Stability) | `scaleup_rerun/stability/stability_pair_level.csv` |
| **8** | `Faithfulness - 10% Erasure` | `A1:P17` | `A5` | `A4:P12` | Clustered Column (Win Rate & Gap) | `scaleup_rerun/dashboard_data/faithfulness_summary.csv` |
| **9** | `Faithfulness - 20% Erasure` | `A1:P17` | `A5` | `A4:P12` | Clustered Column (Win Rate & Gap) | `scaleup_rerun/dashboard_data/faithfulness_summary.csv` |
| **10** | `Faithfulness - 30% Erasure` | `A1:P17` | `A5` | `A4:P12` | Clustered Column (Win Rate & Gap) | `scaleup_rerun/dashboard_data/faithfulness_summary.csv` |
| **11** | `Stability-Faithfulness Corrs` | `A1:J28` | `A5` | `A4:J12` | Clustered Column (Spearman vs Pearson) | `scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv` |
| **12** | `Template Sensitivity` | `A1:M29` | `A6` | `A5:M11` | Clustered Column (Primary vs Template) | `scaleup_rerun/template_sensitivity/analysis/` |
| **13** | `Auxiliary Multiword Probe` | `A1:I31` | `A6` | `A14:I26` | Clustered Column (MuRIL vs XLM-R) | `data/final/AUXILIARY_MULTIWORD_PROBE.csv` |

- Zero blank or unpopulated sheets.
- Zero `#REF!`, `#VALUE!`, or `#N/A` formula errors.
- Decimal formatting preserved: 4 decimal places for correlations and PLL deltas; 1-2 decimal places for percentages; integer formatting for counts.
- Readable column widths auto-fitted across all columns.

---

## 7. Deliverables Synchronization Status

All core delivery artifacts have been generated, tested, and synchronized across `paper/` and `research_paper/`:

| Delivery Artifact | Primary Path (`paper/`) | Mirror Path (`research_paper/`) | Size | Status |
|---|---|---|---|---|
| **Research Manuscript (Markdown)** | `paper/research_paper.md` | `research_paper/research_paper.md` | 74,300 bytes | **Synchronized** |
| **Research Paper (DOCX)** | `paper/research_paper.docx` | `research_paper/research_paper.docx` | 1,810,839 bytes | **Synchronized** |
| **Research Paper (PDF)** | `paper/research_paper.pdf` | `research_paper/research_paper.pdf` | 2,236,171 bytes | **Synchronized** |
| **Excel Results Workbook** | `paper/expanded_experimental_results.xlsx` | `research_paper/expanded_experimental_results.xlsx` | 59,279 bytes | **Synchronized** |
| **Figure Manifest** | `paper/figure_manifest.md` | `research_paper/figure_manifest.md` | 8,529 bytes | **Synchronized** |
| **Reproducibility Guide** | `paper/reproducibility.md` | `research_paper/reproducibility.md` | 8,330 bytes | **Synchronized** |
| **Expanded Notebook** | `notebooks/expanded_experimental_results.ipynb` | *(canonical path)* | 2,618,088 bytes | **Verified** |
| **Final Verification Report** | `paper/FINAL_PAPER_AND_EXCEL_VERIFICATION.md` | `research_paper/FINAL_PAPER_AND_EXCEL_VERIFICATION.md` | *(this document)* | **Generated** |

---

## 8. Unresolved Issues and Exceptions

- **Unresolved Inconsistencies**: **NONE**.
- **Missing or Fabricated Values**: **NONE**.
- **Broken Figures or Tables**: **NONE**.
- All nine scale-up computational rerun stages completed successfully, all eight canonical figures render properly in both DOCX and PDF formats, and all thirteen Excel worksheets are populated directly from verified source CSVs.

---
*Report certified by Antigravity Autonomous Coding Agent on 2026-11-03.*
