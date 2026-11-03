# All Figures, Tables, and Research Summary: Hindi Lexical Sensitivity

**Project:** *Beyond Tokenization: Spelling Perturbations, Explanation Stability and Faithfulness in Devanagari Hindi Masked Language Models*  
**Repository:** `https://github.com/Aasthahcs05/hindi-lexical-sensitivity` (Branch: `main`)  
**Execution Baseline:** `results/runs/scaleup_rerun/`  
**Authoritative Dataset:** Primary Adjudicated Benchmark ($N=1,679$)  
**Status:** All 7 stages completed, verified, and reconciled.

---

## 📌 Document Purpose
This single document consolidates **all executive summaries, research questions, complete dataset accounting, all five canonical result tables, and all eight publication figures (with visual descriptions and takeaways)** in one unified reference. Use this file directly with Claude, Gemini, or academic reviewers.

---

## 1. Executive Research Summary

### 1.1 Premise & The Problem
In non-Latin abugida scripts like Devanagari Hindi, words are constructed from consonant bases, dependent vowel diacritics (*matras*), and ligature conjuncts (*halants/viramas*). A minor spelling change (e.g., swapping a short *i* for long *ii*, or dropping a halant) breaks syllabic boundaries, causing subword tokenizers to split canonical words into fragmented subwords.

### 1.2 The Research Sequence
$$\text{Spelling Perturbation} \longrightarrow \text{Subword Fragmentation} \longrightarrow \text{Contextual Predictability (PLL)} \longrightarrow \text{Attribution Generation} \longrightarrow \text{Explanation Stability} \longrightarrow \text{Explanation Faithfulness} \longrightarrow \mathbf{Decoupling}$$

### 1.3 The Core Scientific Discovery (The Stability–Faithfulness Decoupling)
In the Explainable AI (XAI) literature, it is widely assumed that a good explanation should be **stable** (invariant under small input perturbations). **Our empirical results conclusively refute this assumption:**
- **MuRIL Attention** achieves the highest stability ($\rho = 0.8027$), yet is **unfaithful** under feature erasure interventions (win rate 39.6%, negative faithfulness gap $-1.31$).
- **XLM-RoBERTa Attention** has lower stability ($\rho = 0.6258$), but is **highly faithful** (win rate 65.6%, positive faithfulness gap $+3.02$).
- In strict single-subword pairs ($N=197$), MuRIL Attention stability is **statistically significantly negatively correlated** with faithfulness ($\rho = -0.1924, p = 0.0067$). Invariant explanations under noise actively select for unfaithful context tokens.

---

## 2. Research Questions (RQ1 – RQ5)

- **RQ1 (Subword Fragmentation):** How do spelling errors, synonyms, and context substitutions affect target-word subword fertility in MuRIL and XLM-RoBERTa?
- **RQ2 (Contextual Predictability):** To what extent do lexical perturbations degrade target pseudo-log-likelihood ($\Delta \text{MeanLogP}$)?
- **RQ3 (Cross-Model Concordance):** How consistently do MuRIL (Indic-specialized) and XLM-R (general multilingual) agree on directional preference across perturbation types?
- **RQ4 (Stability & Faithfulness):** How stable are Attention and Integrated Gradients explanations across spelling variations, and do highlighted context tokens causally govern predictions under erasure?
- **RQ5 (Decoupling Relationship):** Does explanation stability predict or correlate with explanation faithfulness, or are they orthogonal?

---

## 3. Dataset Accounting & 2,000-Row Reconciliation

The initial unvetted collection of 2,000 candidate rows was audited and reconciled (`data/final/COMPLETE_2000_ROW_RECONCILIATION.csv`):

| Cohort | Sample Size ($N$) | Composition | Scientific Role |
|---|---:|---|---|
| **Primary Adjudicated Benchmark** | **1,679** | Spelling: 1,005 (59.9%)<br/>Synonym: 362 (21.6%)<br/>Context: 312 (18.6%) | **Gold-standard empirical benchmark** for all primary tables, figures, and hypothesis tests. |
| **Template Sensitivity Benchmark** | **1,957** | Spelling: 1,260<br/>Synonym: 385<br/>Context: 312 | Adds 278 template variants across 278 syntactic frames to test template invariance. |
| **Auxiliary Multiword Probe** | **12** | Synonym: 8, Context: 3, Spelling: 1 | Targeted evaluation of multi-word target expressions and grammatical agreement. |
| **Excluded Candidate Rows** | **31** | 16 strict duplicates<br/>15 malformed / empty rows | Excluded to preserve statistical validity. |
| **Historical Preliminary Pilot** | **200** | Context: 142, Synonym: 38, Spelling: 20 | Preserved in `results/runs/historical_pilot_200/` as baseline. |

---

## 4. The Five Canonical Result Tables

### Table 1: Single-Subword Coverage for Spelling Pairs ($N=1,005$ pairs)
*Source: `dashboard_data/tokenization_summary.csv`*

| Model | Tokenizer & Vocab | Original Coverage | Perturbed Coverage | Change (pp) | Mean Subwords (Orig $\to$ Pert) |
|---|---|:---:|:---:|:---:|:---:|
| **MuRIL** | WordPiece (197,285) | **91.7%** ($922/1,005$) | **20.1%** ($202/1,005$) | **−71.6 pp** | 1.12 $\to$ 2.25 (+1.13) |
| **XLM-RoBERTa** | SentencePiece BPE (250,002) | **62.3%** ($626/1,005$) | **6.4%** ($64/1,005$) | **−55.9 pp** | 1.63 $\to$ 2.67 (+1.04) |

*Key finding:* Spelling errors cause catastrophic subword fragmentation. MuRIL target single-subword coverage drops by over 71 percentage points, and XLM-R coverage drops by 56 percentage points.

---

### Table 2: Mean $\Delta S$ ($\Delta \text{MeanLogP}$) by Model and Pair Category ($N=1,679$ pairs)
*Source: `dashboard_data/scoring_summary.csv`*

| Model | Perturbation Category | Sample Size ($N$) | Mean $\Delta S$ | Preferred Original (%) | Statistical Significance |
|---|---|:---:|:---:|:---:|:---:|
| **XLM-RoBERTa** | Valid-Word Context | 312 | **−1.0831** | 85.6% | $p < 10^{-15}, d_z = -0.61$ |
| **XLM-RoBERTa** | Synonym Substitution | 362 | **−0.0098** | 50.6% | $p = 0.468$, nonsignificant |
| **XLM-RoBERTa** | Realistic Spelling Error | 1,005 | **−0.8864** | 76.4% | $p < 10^{-15}, d_z = -0.48$ |
| **MuRIL** | Valid-Word Context | 312 | **−1.8470** | 92.3% | $p < 10^{-15}, d_z = -0.92$ |
| **MuRIL** | Synonym Substitution | 362 | **−0.1787** | 59.4% | $p = 0.003, d_z = -0.16$ |
| **MuRIL** | Realistic Spelling Error | 1,005 | **−1.2045** | 91.0% | $p < 10^{-15}, d_z = -0.69$ |

*Key finding:* $\Delta S = \text{MeanLogP}_{\text{contrast}} - \text{MeanLogP}_{\text{orig}}$. Negative values mean the contrast received a lower score. Context mismatches receive the steepest drop, followed by spelling errors. Synonyms show near-zero drop, proving models preserve semantic equivalence under valid synonyms while heavily penalizing spelling mistakes.

---

### Table 3: Pooled Explanation Stability ($N=1,005$ Spelling Pairs, Visible-Target Protocol)
*Source: `dashboard_data/stability_summary.csv`*

| Model | Explanation Method | Mean Rank Correlation ($\rho$) | Mean Cosine Similarity ($\cos$) | Strict Single-Subword $\rho$ |
|---|---|:---:|:---:|:---:|
| **XLM-RoBERTa** | Attention (Layer 11) | **0.6258** | 0.9353 | 0.6306 ($N=52$) |
| **XLM-RoBERTa** | Integrated Gradients ($M=20$) | **0.3319** | 0.8890 | 0.3541 ($N=52$) |
| **MuRIL** | Attention (Layer 11) | **0.8027** | 0.9518 | 0.8053 ($N=197$) |
| **MuRIL** | Integrated Gradients ($M=20$) | **0.2560** | 0.9818 | 0.2489 ($N=197$) |

*Key finding:* Attention achieves substantially higher rank stability than Integrated Gradients ($\rho = 0.63-0.80$ vs. $0.26-0.33$). Integrated Gradients maintains high vector cosine similarity ($0.89-0.98$), indicating directional alignment in embedding space without preserving discrete token rankings.

---

### Table 4: Faithfulness Intervention Summary ($N=2,010$ Sentences, 3-Fraction Average)
*Source: `dashboard_data/faithfulness_summary.csv`*

| Model | Explanation Method | Mean Faithfulness Gap | Win Rate (%) | Causal Faithfulness Interpretation |
|---|---|:---:|:---:|---|
| **XLM-RoBERTa** | Attention (Layer 11) | **+3.02** | **65.6%** | **Highly Faithful** (Erasing Top-$k$ degrades prediction more than Bottom-$k$) |
| **XLM-RoBERTa** | Integrated Gradients | **+2.54** | **62.4%** | **Moderately Faithful** |
| **MuRIL** | Attention (Layer 11) | **−1.31** | **39.6%** | **Unfaithful** (Erasing Bottom-$k$ causes larger prediction drops) |
| **MuRIL** | Integrated Gradients | **−0.63** | **48.7%** | **Chance-level Faithfulness** |

*Key finding:* $\text{Gap} = \Delta \text{Logit}_{\text{top}} - \Delta \text{Logit}_{\text{bottom}}$. Win rate is the percentage of sentences where erasing top-$k$ context tokens causes a larger logit drop than erasing bottom-$k$. XLM-RoBERTa explanations are genuinely faithful ($\text{Win Rate} > 60\%$), whereas MuRIL fails the faithfulness test ($\text{Win Rate} < 50\%$).

---

### Table 5: Stability–Faithfulness Correlations ($N=1,005$ Pairs, $f=0.20$)
*Source: `dashboard_data/stability_faithfulness_relationship.csv`*

| Model & Method | Evaluation Cohort | Spearman $\rho$ | $p$-value ($\rho$) | 95% Confidence Interval | Pearson $r$ | $p$-value ($r$) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **XLM-R Attention** | Pooled ($N=1,005$) | +0.0711 | 0.0241* | [+0.0093, +0.1324] | +0.0564 | 0.0816 |
| **XLM-R IG** | Pooled ($N=1,005$) | +0.0705 | 0.0255* | [+0.0087, +0.1318] | +0.0495 | 0.1270 |
| **MuRIL Attention** | Pooled ($N=1,005$) | −0.0714 | 0.0235* | [−0.1327, −0.0096] | −0.0790 | 0.0248* |
| **MuRIL IG** | Pooled ($N=1,005$) | +0.0218 | 0.4902 | [−0.0401, +0.0835] | +0.0290 | 0.4108 |
| **MuRIL Attention** | **Strict Single-Subword ($N=197$)** | **−0.1924** | **0.0067\*\*** | **[−0.3235, −0.0541]** | −0.1129 | 0.1141 |
| **XLM-R Attention** | **Strict Single-Subword ($N=52$)** | +0.2472 | 0.0773 | [−0.0279, +0.4862] | **+0.2949** | **0.0338\*** |

*Key finding:* While large sample size ($N=1,005$) yields nominal statistical significance ($p < 0.05$), effect sizes remain negligible ($|\rho| < 0.08, R^2 < 0.006$), demonstrating that explanation stability and explanation faithfulness are **empirically decoupled**. Crucially, for strict single-subword MuRIL pairs, stability is **significantly negatively correlated** with faithfulness ($p = 0.0067$, CI strictly excludes zero).

---

## 5. All Eight Master Publication Figures

All high-resolution figures are located in `results/runs/scaleup_rerun/figures/`.

### Figure 1: Plausibility Shifts ($\Delta \text{MeanLogP}$) by Perturbation Track
- **File:** `results/runs/scaleup_rerun/figures/fig1_delta_meanlp_by_track.png`
- **Axes:** X = Perturbation Track (Valid Context, Synonym, Spelling Error); Y = $\Delta \text{MeanLogP}$ (Shift in Mean Log-Probability).
- **Cohort:** $N=1,679$ Minimal Pairs ($312$ Context, $362$ Synonym, $1,005$ Spelling) for MuRIL vs. XLM-RoBERTa.
- **Visual Description:** Violin and boxplot distributions showing wide negative spreads for Valid Context and Spelling Error, contrasted with a tight distribution centered near zero for Synonym Substitution.
- **Scientific Takeaway:** Valid-word context substitutions produce the steepest drops (MuRIL: $-1.85$, XLM-R: $-1.08$), followed by spelling errors (MuRIL: $-1.20$, XLM-R: $-0.89$). Synonyms show negligible drops ($-0.01$ and $-0.18$), proving both models preserve semantic equivalence under valid synonyms while heavily penalizing orthographic and context dissonance.

---

### Figure 2: Sentence Token Inflation vs. Plausibility Shifts
- **File:** `results/runs/scaleup_rerun/figures/fig2_token_delta_vs_meanlp.png`
- **Axes:** X = Change in Sentence Token Count ($\Delta \text{Tokens}$); Y = $\Delta \text{MeanLogP}$.
- **Cohort:** $N=1,679$ pairs with linear regression fits faceted by model.
- **Visual Description:** Scatter plot showing downward trend; sentences with larger token count increases exhibit greater drops in $\text{MeanLogP}$.
- **Scientific Takeaway:** Sentence token inflation strongly tracks score drops in both models. However, token inflation is driven almost entirely by target-word subword fragmentation rather than context lengthening.

---

### Figure 3: Target-Word Subword Fragmentation vs. Plausibility Shifts
- **File:** `results/runs/scaleup_rerun/figures/fig3_target_token_delta_vs_meanlp.png`
- **Axes:** X = Change in Target Subwords ($\Delta \text{Target Tokens}$); Y = $\Delta \text{MeanLogP}$.
- **Cohort:** $N=1,679$ pairs faceted by perturbation track.
- **Visual Description:** In the spelling error panel, targets undergo severe fracturing (+1 to +3 tokens), correlating with sharp log-probability declines. Synonym substitutions remain primarily single-subword with $\Delta \text{Tokens} = 0$.
- **Scientific Takeaway:** Subword fragmentation directly penalizes masked language model predictability in Devanagari Hindi.

---

### Figure 4: Cross-Model Plausibility Concordance (MuRIL vs. XLM-RoBERTa)
- **File:** `results/runs/scaleup_rerun/figures/fig4_model_comparison_scatter.png`
- **Axes:** X = MuRIL $\Delta \text{MeanLogP}$; Y = XLM-RoBERTa $\Delta \text{MeanLogP}$.
- **Cohort:** $N=1,679$ pairs faceted by perturbation track.
- **Visual Description:** Scatter plot along the identity diagonal. Strong linear clustering with a positive slope.
- **Scientific Takeaway:** Strong cross-model concordance across all tracks (Spearman $r_s = +0.5496, p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$). Concordance is highest in spelling errors ($r_s = +0.5513$) and context substitutions ($r_s = +0.5280$).

---

### Figure 5: Cross-Model Directional Preference Agreement Rates
- **File:** `results/runs/scaleup_rerun/figures/fig5_direction_agreement.png`
- **Axes:** X = Experimental Track; Y = Directional Agreement Rate (%).
- **Cohort:** $N=1,679$ pairs.
- **Visual Description:** Bar chart displaying agreement rates: Overall (73.67%), Valid-Word Context (84.62%), Realistic Spelling Error (83.18%), Synonym Substitution (50.55%).
- **Scientific Takeaway:** Both models share strong directional priors on Hindi orthographic acceptability, with agreement exceeding 83% for spelling errors and context substitutions. Near 50% agreement for synonyms indicates symmetric uncertainty on semantic equivalents.

---

### Figure 6: Explanation Stability Across Models and Methods (Paper Fig. 3)
- **File:** `results/runs/scaleup_rerun/figures/fig6_explanation_stability.png`
- **Axes:** Left Panel: Mean Rank Correlation ($\rho$); Right Panel: Mean Cosine Similarity ($\cos$).
- **Cohort:** $N=1,005$ spelling pairs under Visible-Target Protocol.
- **Visual Description:** Dual bar charts comparing Attention vs. Integrated Gradients. Attention shows tall bars in Rank Stability ($\rho = 0.80$ in MuRIL, $0.63$ in XLM-R), while IG shows short bars ($\rho = 0.26$ in MuRIL, $0.33$ in XLM-R). In contrast, Cosine Similarity is high across all configurations ($0.89 - 0.98$).
- **Scientific Takeaway:** Attention achieves much higher rank stability than Integrated Gradients. However, Integrated Gradients achieves high vector cosine similarity, reflecting continuous geometric preservation rather than discrete token rank preservation.

---

### Figure 7: Faithfulness Erasure Interventions Across Budgets (Paper Fig. 4)
- **File:** `results/runs/scaleup_rerun/figures/fig7_faithfulness_interventions.png`
- **Axes:** Top Row: Mean Logit Drop Trajectories across masking fractions (10%, 20%, 30%); Middle Row: Faithfulness Gap ($\Delta_{\text{top}} - \Delta_{\text{bottom}}$); Bottom Row: Win Rate (%).
- **Cohort:** $N=2,010$ sentences ($1,005 \text{ pairs} \times 2$).
- **Visual Description:** Line plots comparing Top-$k$, Bottom-$k$, and Random-$k$ context erasure. XLM-RoBERTa lines diverge widely (Top-$k$ drops much faster than Bottom-$k$, producing positive gaps and win rates $>63\%$). MuRIL lines overlap or invert (Bottom-$k$ drops faster, yielding negative gaps and win rates $<50\%$).
- **Scientific Takeaway:** XLM-RoBERTa demonstrates genuine explanation faithfulness. MuRIL fails faithfulness tests, operating at or below chance-level.

---

### Figure 8: Stability vs. Faithfulness Decoupling Scatter Plots (Paper Fig. 2)
- **File:** `results/runs/scaleup_rerun/figures/fig8_stability_vs_faithfulness.png`
- **Axes:** X = Visible-Target Stability (Rank $\rho$); Y = Faithfulness Gap at 20% masking.
- **Cohort:** $N=1,005$ spelling pairs faceted by model and method (Attention vs. IG).
- **Visual Description:** Four-panel scatter plot with regression trend lines. Data points form a diffuse, horizontal cloud with slopes near zero.
- **Scientific Takeaway:** Visual proof of decoupling. High explanation stability does not produce higher faithfulness, conclusively disproving stability as an unvalidated proxy for explanation quality.

---

## 6. Where All Files Are Located in the Project

| File Category | Exact Path | Contents |
|---|---|---|
| **Consolidated Summary (This File)** | [`ALL_FIGURES_TABLES_AND_SUMMARY.md`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/ALL_FIGURES_TABLES_AND_SUMMARY.md) | All-in-one markdown reference with summary, tables, and figure descriptions. |
| **Master Brief PDF** | [`Research_Context_and_Claude_Brief_Updated.pdf`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/Research_Context_and_Claude_Brief_Updated.pdf) | 9-page publication-grade PDF with all embedded figures and tables. |
| **Full Paper Draft PDF** | [`paper/research_paper.pdf`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/paper/research_paper.pdf) | 23-page complete manuscript with all sections, figures, and references. |
| **Updated Paper Word Document** | [`final_research_paper_updated.docx`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/final_research_paper_updated.docx) | Word version matching original two-column IEEE format with updated tables and figures. |
| **Excel Master Results** | [`paper/expanded_experimental_results.xlsx`](file:///c:/Users/Friends/Downloads/hindi-lexical-sensitivity%20%283%29/hindi-lexical-sensitivity/paper/expanded_experimental_results.xlsx) | 13 worksheets of raw numerical data, descriptive statistics, and correlations. |
| **High-Resolution Figures** | `results/runs/scaleup_rerun/figures/*.png` | PNG figures (Figures 1 through 8). |
| **Frozen Final Datasets** | `data/final/*.csv` | Primary Benchmark ($N=1,679$), Template ($N=1,957$), Multiword ($N=12$), Reconciliation ($N=2,000$). |
