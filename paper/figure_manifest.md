# Figure Manifest

This manifest documents all verified figures included in the research paper *"Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi"*.

All figures are stored in `outputs/analysis/figures/` (regenerated from `results/runs/scaleup_rerun/figures/`) and referenced within `research_paper/research_paper.md`, `research_paper/research_paper.docx`, and `research_paper/research_paper.pdf`.

---

## Manifest Summary Table

| Figure Number | Image File | Dimensions / Format | Underlying Source Data | Section Referenced |
|---|---|---|---|---|
| **Figure 1** | `outputs/analysis/figures/fig1_delta_meanlp_by_track.png` | 1800×1200 PNG | `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv` | Section 5.2 |
| **Figure 2** | `outputs/analysis/figures/fig2_token_delta_vs_meanlp.png` | 1800×1200 PNG | `results/runs/scaleup_rerun/analysis/combined_pair_level_results.csv` | Section 5.2 |
| **Figure 3** | `outputs/analysis/figures/fig3_target_token_delta_vs_meanlp.png` | 1800×1200 PNG | `results/runs/scaleup_rerun/analysis/combined_pair_level_results.csv` | Section 5.2 |
| **Figure 4** | `outputs/analysis/figures/fig4_model_comparison_scatter.png` | 1800×1200 PNG | `results/runs/scaleup_rerun/analysis/model_comparison.csv` | Section 5.3 |
| **Figure 5** | `outputs/analysis/figures/fig5_direction_agreement.png` | 1800×1200 PNG | `results/runs/scaleup_rerun/analysis/model_comparison.csv` | Section 5.3 |
| **Figure 6** | `outputs/analysis/figures/fig6_explanation_stability.png` | 3000×1350 PNG | `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv` | Section 5.4 |
| **Figure 7** | `outputs/analysis/figures/fig7_faithfulness_interventions.png` | 3300×1350 PNG | `results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv` | Section 5.5 |
| **Figure 8** | `outputs/analysis/figures/fig8_stability_vs_faithfulness.png` | 3300×1440 PNG | `results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv` | Section 5.6 |

---

## Detailed Figure Descriptions and Captions

### Figure 1: Distribution of Length-Normalized Plausibility Shifts ($\Delta \text{MeanLogP}$) by Experimental Track
- **File**: `outputs/analysis/figures/fig1_delta_meanlp_by_track.png`
- **Caption**: **Figure 1**: Boxplot distributions of signed length-normalized pseudo-log-likelihood deltas ($\Delta \text{MeanLogP} = \text{Contrast} - \text{Original}$) across `VALID_WORD_CONTEXT` ($N=312$), `SYNONYM_SUBSTITUTION` ($N=362$), and `REALISTIC_SPELLING_ERROR` ($N=1,005$) for XLM-RoBERTa (blue) and MuRIL (orange) on the primary benchmark ($N=1,679$). Negative values indicate that the canonical original sentence is preferred over the contrast. MuRIL imposes substantially harsher penalties on orthographic errors (mean $\mu = -1.2045$, median $=-0.8892$) than XLM-RoBERTa (mean $\mu = -0.8864$, median $=-0.7752$).
- **Source Artifact**: `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv`
- **Linguistic/Statistical Nuance**: Synonyms exhibit near-zero plausibility deltas ($\mu = -0.0098$ for XLM-R), confirming high semantic preservation.

### Figure 2: Relationship Between Sentence Token Length Delta and Plausibility Shift ($\Delta \text{MeanLogP}$)
- **File**: `outputs/analysis/figures/fig2_token_delta_vs_meanlp.png`
- **Caption**: **Figure 2**: Scatter plot relating full sentence subword length changes ($\Delta \text{Tokens} = |W_{\text{cont}}| - |W_{\text{orig}}|$) to plausibility shifts ($\Delta \text{MeanLogP}$) across all 3,358 model evaluation rows ($N=1,679$ pairs). Target fragmentation in Devanagari spelling errors causes sharp plausibility penalties even under length-normalized scoring.
- **Source Artifact**: `results/runs/scaleup_rerun/analysis/combined_pair_level_results.csv`

### Figure 3: Target Word Tokenization Inflation vs. Plausibility Shift ($\Delta \text{MeanLogP}$)
- **File**: `outputs/analysis/figures/fig3_target_token_delta_vs_meanlp.png`
- **Caption**: **Figure 3**: Plausibility shifts ($\Delta \text{MeanLogP}$) plotted specifically against the subword change localized within the target word ($\Delta \text{Target Tokens}$). Devanagari spelling errors consistently generate $\Delta \text{Target Tokens} \ge +1$, directly driving the observed score penalties in both models.
- **Source Artifact**: `results/runs/scaleup_rerun/analysis/combined_pair_level_results.csv`

### Figure 4: Cross-Model Comparison of Plausibility Shifts (XLM-RoBERTa vs. MuRIL)
- **File**: `outputs/analysis/figures/fig4_model_comparison_scatter.png`
- **Caption**: **Figure 4**: Cross-model scatter plot comparing within-model $\Delta \text{MeanLogP}$ between XLM-RoBERTa ($x$-axis) and MuRIL ($y$-axis) across all 1,679 primary pairs. The models exhibit strong rank concordance (Spearman $r_s = +0.5496, p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$). Concordance is strongest on contextual contrasts ($r_s = +0.4590$) and spelling errors ($r_s = +0.5513$), while decoupling on synonyms ($r_s = +0.2271$).
- **Source Artifact**: `results/runs/scaleup_rerun/analysis/model_comparison.csv`

### Figure 5: Directional Plausibility Agreement Proportions Between Models Across Tracks
- **File**: `outputs/analysis/figures/fig5_direction_agreement.png`
- **Caption**: **Figure 5**: Proportions of directional agreement between XLM-RoBERTa and MuRIL on canonical sentence preference ($\Delta \text{MeanLogP} < 0$). Directional agreement is highest in `VALID_WORD_CONTEXT` (84.62%), strong in `REALISTIC_SPELLING_ERROR` (75.12%), and lowest in `SYNONYM_SUBSTITUTION` (60.22%), with overall benchmark agreement at 73.67% ($N=1,679$).
- **Source Artifact**: `results/runs/scaleup_rerun/analysis/model_comparison.csv`

### Figure 6: Explanation Stability under Devanagari Spelling Perturbations
- **File**: `outputs/analysis/figures/fig6_explanation_stability.png`
- **Caption**: **Figure 6**: Visible-target explanation stability under authentic Devanagari spelling noise ($N=1,005$ pairs) comparing Last-Layer Self-Attention and Layer Integrated Gradients across XLM-RoBERTa and MuRIL. (a) Rank stability (Spearman $\rho$): Attention achieves $1.9\times$ to $3.1\times$ higher rank stability than Integrated Gradients (pooled mean $0.8027$ vs. $0.2560$ in MuRIL; $0.6258$ vs. $0.3319$ in XLM-R). (b) Vector directional stability (Cosine Similarity): Cosine similarity remains high across all conditions ($0.8890$ to $0.9818$), demonstrating that gradient attributions retain overall vector trajectory while local token rankings fluctuate heavily.
- **Source Artifact**: `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv`

### Figure 7: Explanation Faithfulness under Discrete Context Token Erasure
- **File**: `outputs/analysis/figures/fig7_faithfulness_interventions.png`
- **Caption**: **Figure 7**: Context erasure faithfulness across masking fractions $f \in \{0.10, 0.20, 0.30\}$ ($N=2,010$ evaluated sentences per model across 1,005 spelling pairs). (a) Mean Faithfulness Gap ($\Delta S_{\text{top}} - \Delta S_{\text{bottom}}$): Attention maintains consistently positive gaps in XLM-RoBERTa ($+2.44$ to $+3.81$), while Integrated Gradients in MuRIL exhibits negative gaps ($-0.30$ to $-1.08$). (b) Win Rate vs. Bottom-$k$ Control: Attention achieves win rates of 63.53%–67.46% in XLM-RoBERTa, whereas Integrated Gradients operates near or below chance in MuRIL (46.72%–49.90%).
- **Source Artifact**: `results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv`

### Figure 8: Relationship Between Visible-Target Stability and Explanation Faithfulness
- **File**: `outputs/analysis/figures/fig8_stability_vs_faithfulness.png`
- **Caption**: **Figure 8**: Scatter plot of visible-target explanation stability (Spearman $\rho$, $x$-axis) versus mean faithfulness gap ($f=0.20$, $y$-axis) across Devanagari spelling pairs ($N=1,005$) for (a) XLM-RoBERTa ($N=953$ scorable) and (b) MuRIL ($N=808$ scorable). Across all evaluated configurations, there is no consistent positive association between explanation stability and faithfulness. Some weak negative associations occur for MuRIL Attention (pooled Pearson $r = -0.0790, p = 0.0248$; strict single-subword Spearman $\rho = -0.1924, p = 0.0067$), while other combinations are non-significant (XLM-R Attention pooled $r_s = +0.0607, p = 0.0612$; XLM-R IG pooled $r_s = +0.0632, p = 0.0510$; MuRIL IG pooled $r_s = +0.0214, p = 0.5442$). These empirical observations demonstrate that explanation stability under spelling noise cannot serve as a reliable proxy for causal explanation faithfulness.
- **Source Artifact**: `results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv`
