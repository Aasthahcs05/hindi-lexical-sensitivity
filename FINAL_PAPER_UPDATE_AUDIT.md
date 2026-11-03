# Final Paper Update Audit: Comprehensive Synchronization with Expanded Experimental Results

**Document:** `FINAL_PAPER_UPDATE_AUDIT.md`  
**Date:** 2026-11-03  
**Project:** `hindi-lexical-sensitivity`  
**Base Document (Structural & Formatting Authority):** `final_research_paper (1).docx`  
**Backup Preserved:** `final_research_paper (1)_backup.docx`  
**Output Document:** `final_research_paper_updated.docx` (2,513,463 bytes)  
**Authoritative Experimental Run:** Scaleup Rerun (`results/runs/scaleup_rerun/`)  
**Frozen Canonical Dataset:** Adjudicated Primary Benchmark ($N = 1,679$: 1,005 Spelling Error, 362 Synonym Substitution, 312 Valid-Word Context)

---

## 1. Executive Summary

This audit establishes the complete synchronization of the original research paper (`final_research_paper (1).docx`) with the authoritative expanded experimental results. 

The update adheres strictly to the principle of **evidence updating without unnecessary rewriting**:
1. **Preservation of Document Structure**: All original sections, headings, two-column flow, paragraph boundaries, and citations are preserved.
2. **Preservation of Table Layouts**: Exactly the five original tables remain in their original positions. No duplicate, replacement, or newly designed tables were added.
3. **Figure Replacement with High-Resolution Expanded Plots**: Embedded image parts in the Word package were replaced with their exact expanded counterparts from `results/runs/scaleup_rerun/figures/`, ensuring that visual plots, axis labels, legends, and data points agree with the updated result tables.
4. **Complete Text Harmonization**: Narrative text, figure captions, table footnotes, and statistical interpretations across the Abstract, Introduction, Methodology, Results, Discussion, Limitations, and Conclusion were updated to reflect the expanded $N = 1,679$ benchmark (and $N = 1,005$ spelling cohort).

---

## 2. Inventory of Sections Preserved vs. Methodologically Updated

| Section | Status | Preservation Details | Updated Elements & Rationale |
|---|---|---|---|
| **Title & Frontmatter** | **Preserved** | Title, author affiliations, IEEE styling, and keywords preserved intact. | None. |
| **Abstract** | **Synchronized** | Overall structure and research framing preserved. | Updated sample size ($N = 1,679$), category breakdown, tokenization collapse metrics (MuRIL: −71.6 pp; XLM-R: −55.9 pp), PLL drops, stability scores, and the non-significance/negligible effect size ($|\rho| < 0.08$) of the stability–faithfulness link. |
| **Introduction** | **Preserved / Synchronized** | Research motivation, linguistic challenges in Devanagari, theoretical context, and research questions preserved. | Contributions 1, 3, and 4 (P18, P20, P21) updated to reflect the 1,679-pair benchmark and 1,005-pair explainability evaluation. |
| **Related Work** | **100% Preserved** | Tokenization literature, MLM scoring background, and XAI stability/faithfulness reviews retained with all citations. | None required (literature foundation remains fully applicable). |
| **Dataset & Methodology** | **Synchronized** | Mathematical definitions of $\Delta T$, single-subword coverage, PLL, $\text{MeanLogP}$, Attention, Integrated Gradients, visible-target logit scoring, and masking intervention protocols preserved identically. | Updated dataset description (P31) and validation status (P32) to reflect the frozen 1,679 adjudicated benchmark. Methodology pipeline diagram (`image1.png`) updated to show "1,679 Hindi sentence pairs". |
| **Results (Tokenization)** | **Synchronized** | Presentation flow, Table III structure, and Fig. 1 schematic preserved. | Table III updated with $N = 1,005$ coverage values; footnote and narrative discussion (P69, P71) aligned. |
| **Results (PLL Scoring)** | **Synchronized** | Table IV structure, metric definition, and comparative framing preserved. | Table IV updated with all 6 category means; footnote (P79) and narrative text (P81) updated. |
| **Results (Explanation Stability)** | **Synchronized** | Table V structure, alignment protocol description, and visible-target motivation preserved. | Table V updated with pooled rank $\rho$ and cosine similarities; Fig. 3 image replaced with `fig6_explanation_stability.png`; strict single-subword coverage ($N = 52$ for XLM-R; $N = 197$ for MuRIL) documented in P87. |
| **Results (Faithfulness)** | **Synchronized** | Table VI structure, top-vs-bottom intervention framework, and metric definitions preserved. | Table VI updated with 3-fraction mean gaps and win rates; Fig. 4 image replaced with `fig7_faithfulness_interventions.png`; footnote (P91) and narrative (P95) updated to reflect $N = 2,010$ evaluated sentences ($1,005 \times 2$). |
| **Results (Stability vs. Faithfulness)** | **Synchronized** | Table VII structure and Spearman correlation methodology preserved. | Table VII updated with expanded $N = 1,005$ correlations and $p$-values; Fig. 2 image replaced with `fig8_stability_vs_faithfulness.png`; narrative (P104) updated to interpret nominal $p < 0.05$ alongside negligible effect size ($R^2 < 0.006$). |
| **Discussion** | **Synchronized** | Core analytical arguments regarding vocabulary fragmentation, model plausibility, and XAI decoupling preserved. | In-text citations of stability metrics, win rates, and figure references updated (P112, P113, P115–P117). |
| **Limitations** | **Synchronized** | Identification of OOD masking shock, subword aggregation, and evaluation constraints preserved. | Sample size bounds updated to $N = 1,005$ spelling pairs and strict target alignment numbers updated (P119, P120). |
| **Conclusion & Future Work**| **Synchronized** | Concluding recommendations and research directions preserved. | Replaced outdated $N = 1,280$ mentions with $N = 1,005$ and reaffirmed the orthogonality of explanation stability and faithfulness. |
| **References** | **100% Preserved** | All 15 original references and bibliographic formats retained. | None. |

---

## 3. Detailed Audit of the Five Original Result Tables

### Table 1 (Paper Table III): SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS
*Preserved Title:* `TABLE III. SINGLE-SUBWORD COVERAGE FOR SPELLING PAIRS`  
*Preserved Layout:* `Model | Original | Perturbed | Change`  
*Evaluated Cohort:* $N = 1,005$ realistic spelling error pairs (expanded from $N = 20$).  
*Canonical Sources:* `results/runs/scaleup_rerun/tokenization/tokenization_results.csv`, `dashboard_data/tokenization_summary.csv`

| Cell Location | Row Label / Metric | Old Value ($N=20$) | New Canonical Value ($N=1,005$) | Difference | Verification Status |
|---|---|:---:|:---:|:---:|:---:|
| Row 1, Col 1 | MuRIL \| Original | 90% | **91.7%** ($922/1,005$) | +1.7 pp | **Confirmed** |
| Row 1, Col 2 | MuRIL \| Perturbed | 30% | **20.1%** ($202/1,005$) | −9.9 pp | **Confirmed** |
| Row 1, Col 3 | MuRIL \| Change | −60 pp | **−71.6 pp** | −11.6 pp | **Confirmed** |
| Row 2, Col 1 | XLM-RoBERTa \| Original | 70% | **62.3%** ($626/1,005$) | −7.7 pp | **Confirmed** |
| Row 2, Col 2 | XLM-RoBERTa \| Perturbed | 20% | **6.4%** ($64/1,005$) | −13.6 pp | **Confirmed** |
| Row 2, Col 3 | XLM-RoBERTa \| Change | −50 pp | **−55.9 pp** | −5.9 pp | **Confirmed** |

*Updated Footnote:* `Coverage is the share of target words represented by exactly one subword token (N = 1,005 pairs per model). pp = percentage points.`

---

### Table 2 (Paper Table IV): MEAN ΔS BY MODEL AND PAIR CATEGORY
*Preserved Title:* `TABLE IV. MEAN ΔS BY MODEL AND PAIR CATEGORY`  
*Preserved Layout:* `Model | Category | Mean ΔS`  
*Evaluated Cohort:* $N = 1,679$ primary benchmark pairs (312 context, 362 synonym, 1,005 spelling).  
*Canonical Sources:* `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv`, `scoring/pll_scoring_results.csv`

| Cell Location | Model & Category | Old Mean ΔS ($N=200$) | New Canonical Mean ΔS ($N=1,679$) | Sample Size ($N$) | Verification Status |
|---|---|:---:|:---:|:---:|:---:|
| Row 1 | XLM-RoBERTa \| Valid-word context | −1.0933 | **−1.0831** | $N = 312$ | **Confirmed** |
| Row 2 | XLM-RoBERTa \| Synonym substitution | −0.0655 | **−0.0098** | $N = 362$ | **Confirmed** |
| Row 3 | XLM-RoBERTa \| Spelling error | −0.6695 | **−0.8864** | $N = 1,005$ | **Confirmed** |
| Row 4 | MuRIL \| Valid-word context | −1.9141 | **−1.8470** | $N = 312$ | **Confirmed** |
| Row 5 | MuRIL \| Synonym substitution | −0.5810 | **−0.1787** | $N = 362$ | **Confirmed** |
| Row 6 | MuRIL \| Spelling error | −2.0368 | **−1.2045** | $N = 1,005$ | **Confirmed** |

*Updated Footnote:* `ΔS = MeanLogP(contrast) − MeanLogP(original). Negative values mean the contrast sentence received a lower mean token log-probability. Pairs: 312 valid-word context, 362 synonym substitution, 1,005 spelling error (N = 1,679 total).`

---

### Table 3 (Paper Table V): POOLED EXPLANATION STABILITY
*Preserved Title:* `TABLE V. POOLED EXPLANATION STABILITY`  
*Preserved Layout:* `Model | Method | Mean rank ρ | Mean cosine`  
*Evaluated Cohort:* $N = 1,005$ spelling pairs under Stage 7 Visible-Target Protocol (`all_scorable_pooled`).  
*Canonical Sources:* `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv`, `stability/stability_pair_level.csv`

| Cell Location | Model & Method | Old Mean rank ρ | New Mean rank ρ | Old Mean cosine | New Mean cosine | Verification Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Row 1 | XLM-RoBERTa \| Attention | 0.7425 | **0.6258** | 0.9648 | **0.9353** | **Confirmed** |
| Row 2 | XLM-RoBERTa \| IG | 0.3589 | **0.3319** | 0.8994 | **0.8890** | **Confirmed** |
| Row 3 | MuRIL \| Attention | 0.7043 | **0.8027** | 0.9639 | **0.9518** | **Confirmed** |
| Row 4 | MuRIL \| IG | 0.2632 | **0.2560** | 0.9880 | **0.9818** | **Confirmed** |

*Sub-cohort Documentation:* Strict single-subword eligibility ($N = 52$ for XLM-R; $N = 197$ for MuRIL) yields rank stabilities of $0.6306$ (XLM-R Attention) and $0.8053$ (MuRIL Attention), fully confirming pooled trends (documented in narrative paragraph P87).

---

### Table 4 (Paper Table VI): FAITHFULNESS INTERVENTION SUMMARY
*Preserved Title:* `TABLE VI. FAITHFULNESS INTERVENTION SUMMARY`  
*Preserved Layout:* `Model | Method | Mean gap | Win rate`  
*Evaluated Cohort:* $N = 2,010$ evaluated sentences per fraction ($1,005 \text{ pairs} \times 2$) across 10%, 20%, and 30% context masking.  
*Canonical Sources:* `results/runs/scaleup_rerun/faithfulness/faithfulness_summary.csv`, `faithfulness/faithfulness_pair_level.csv`

| Cell Location | Model & Method | Old Mean gap | New Mean gap (3-Frac Avg) | Old Win rate | New Win rate (3-Frac Avg) | Verification Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Row 1 | XLM-RoBERTa \| Attention | 4.40 | **3.02** ($3.0158$) | 76.7% | **65.6%** ($65.59\%$) | **Confirmed** |
| Row 2 | XLM-RoBERTa \| IG | 2.32 | **2.54** ($2.5427$) | 58.3% | **62.4%** ($62.37\%$) | **Confirmed** |
| Row 3 | MuRIL \| Attention | 2.21 | **−1.31** ($−1.3127$) | 63.3% | **39.6%** ($39.63\%$) | **Confirmed** |
| Row 4 | MuRIL \| IG | −0.45 | **−0.63** ($−0.6327$) | 44.2% | **48.7%** ($48.67\%$) | **Confirmed** |

*Updated Footnote:* `Averaged over masking fractions of 10%, 20% and 30%; N = 2,010 sentences per fraction (1,005 pairs × 2). Gap = Dtop − Dbottom; win rate = share of sentences with Dtop > Dbottom. IG = Integrated Gradients.`

---

### Table 5 (Paper Table VII): STABILITY–FAITHFULNESS CORRELATIONS
*Preserved Title:* `TABLE VII. STABILITY–FAITHFULNESS CORRELATIONS`  
*Preserved Layout:* `Model | Method | Spearman ρ | | p-value` (5-column layout preserved)  
*Evaluated Cohort:* $N = 1,005$ spelling pairs ($df = 1,003$) correlated at 20% masking fraction.  
*Canonical Sources:* `results/runs/scaleup_rerun/faithfulness/stability_faithfulness_relationship.csv`, `dashboard_data/stability_faithfulness_relationship.csv`

| Cell Location | Model & Method | Old Spearman ρ | New Spearman ρ | Old p-value | New p-value | Verification Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Row 1 | XLM-RoBERTa \| Attention | 0.2704 | **0.0711** | 0.2490 | **0.0241** ($2.41 \times 10^{-2}$) | **Confirmed** |
| Row 2 | XLM-RoBERTa \| IG | 0.1583 | **0.0705** | 0.5052 | **0.0255** ($2.55 \times 10^{-2}$) | **Confirmed** |
| Row 3 | MuRIL \| Attention | −0.1611 | **−0.0714** | 0.4974 | **0.0235** ($2.35 \times 10^{-2}$) | **Confirmed** |
| Row 4 | MuRIL \| IG | 0.0075 | **0.0218** | 0.9749 | **0.4902** ($4.90 \times 10^{-1}$) | **Confirmed** |

*Updated Footnote:* `Spearman rank correlation between visible-target stability (rank ρ) and mean faithfulness gap at 20% masking; N = 1,005 spelling pairs per model and method. While correlations of small magnitude (|ρ| ≈ 0.07) reach nominal statistical significance (p < 0.05) due to large sample power, effect sizes remain negligible (|ρ| < 0.10). IG = Integrated Gradients.`

---

## 4. Audit of Figure and Visualization Updates

| Figure Number in Paper | In-Package Image File | Replacement Source File | Underlying Canonical Data | Nature of Visual Update | Verification Status |
|---|---|---|---|---|---|
| **Pipeline Flowchart** (Methodology) | `word/media/image1.png` | `extracted_docx_images/image1_updated.png` | Primary Adjudicated Benchmark ($N = 1,679$) | Top box updated seamlessly from "2000 Hindi sentence pairs" to "1,679 Hindi sentence pairs" with matched typography and background. | **Replaced & Verified** |
| **Figure 1** (Schematic) | `word/media/image2.png` | Preserved intact | Conceptual diagram | Conceptual schematic of subword token splitting. Contains no empirical numbers; preserved. | **Preserved** |
| **Figure 2** (Scatter Plot) | `word/media/image3.png` | `results/runs/scaleup_rerun/figures/fig8_stability_vs_faithfulness.png` | `dashboard_data/stability_faithfulness_relationship.csv` ($N = 1,005$) | Replaced pilot $N=20$ scatter plot with high-resolution $N=1,005$ scatter plot showing XLM-R and MuRIL stability vs faithfulness distributions. | **Replaced & Verified** |
| **Figure 3** (Bar Charts) | `word/media/image4.png` | `results/runs/scaleup_rerun/figures/fig6_explanation_stability.png` | `dashboard_data/stability_summary.csv` ($N = 1,005$) | Replaced pilot bar charts with expanded bar charts: Rank Stability (0.626 / 0.332 for XLM-R; 0.803 / 0.256 for MuRIL) and Directional Stability (0.935 / 0.889; 0.952 / 0.982). | **Replaced & Verified** |
| **Figure 4** (Intervention Curves)| `word/media/image5.png` | `results/runs/scaleup_rerun/figures/fig7_faithfulness_interventions.png` | `dashboard_data/faithfulness_summary.csv` ($N = 2,010$) | Replaced pilot 40-sentence line charts with expanded 2,010-sentence curves for faithfulness gap and win rates across 10%, 20%, and 30% masking. | **Replaced & Verified** |

---

## 5. Summary of Figure Captions and Narrative Explanations Updated

- **Figure 2 Caption (P101)**: Updated sample size from "1280 pairs" to "1,005 pairs for each model and method", and noted that while large sample size yields nominal $p < 0.05$, correlation coefficients remain negligible ($|\rho| < 0.08$).
- **Figure 3 Caption (P106)**: Updated to "Pooled explanation stability for 1,005 spelling pairs per model."
- **Figure 4 Caption (P110)**: Updated to reflect evaluation across 2,010 sentences per fraction ($1,005 \text{ pairs} \times 2$).
- **Figure 3 Narrative Discussion (P112)**: Aligned numerical values in prose with the updated figure: Attention achieves $0.626$ vs $0.332$ in XLM-R, and $0.803$ vs $0.256$ in MuRIL; cosine similarities are $0.889$ (XLM-R IG) and $0.982$ (MuRIL IG).
- **Figure 4 Narrative Discussion (P113)**: Updated win rate ranges and faithfulness gaps to match the expanded figure: XLM-R attention win rate spans 63.5%–67.5% (gap $+2.44$ to $+3.81$); MuRIL IG win rate spans 46.7%–49.9% (gap $-0.30$ to $-1.08$).
- **Stability-Faithfulness Relationship (P104)**: Clarified that the emergence of nominal $p < 0.05$ is driven by large statistical power ($N = 1,005$), while the practical effect size is negligible ($R^2 < 0.006$), confirming orthogonality.

---

## 6. Document Validation Checklist

Programmatic inspection of `final_research_paper_updated.docx` confirms:
- [x] **Section Structure Preserved**: Document contains 154 paragraphs and all original sections in identical sequence.
- [x] **Exact Table Count**: Exactly 5 tables exist in the document (zero extra, replacement, or duplicate tables).
- [x] **Table Titles & Layouts**: All 5 table titles and column/row structures are 100% identical to `final_research_paper (1).docx`.
- [x] **Numerical Precision**: All 36 table cells match canonical scaleup CSV files.
- [x] **Media Files**: Exactly 5 media files are present in the package, with 4 replaced by updated expanded graphics.
- [x] **Textual Consistency**: Zero instances of the narrative placeholder `1280` or outdated pilot percentages remain.
- [x] **File Status**: Generated cleanly at `final_research_paper_updated.docx` (2,513,463 bytes).

