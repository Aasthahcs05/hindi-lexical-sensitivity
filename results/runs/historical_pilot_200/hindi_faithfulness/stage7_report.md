# Stage 7: Faithfulness Evaluation for the Hindi NLP Research Project

## 1. Executive Summary & Experimental Context
- **Primary Track Evaluated**: `REALISTIC_SPELLING_ERROR` (20 curated sentence pairs)
- **Models Evaluated**: `google/muril-base-cased, FacebookAI/xlm-roberta-base`
- **Dataset SHA-256**: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
- **Timestamp (UTC)**: `2026-10-19T16:01:28.394138+00:00`
- **Explanation Methods**: `Self-Attention` (last layer, mean over heads) and `LayerIntegratedGradients` (embedding layer)
- **Intervention Protocol**: Visible target, masking context tokens at fractions `10%`, `20%`, and `30%` (`top_k`, `bottom_k`, `random_k`)

## 2. Scientific Problem Addressed
Stage 6 established that under a masked-target formulation, explanations exhibited perfect stability (Spearman rho = 1.0)
because masking the target word rendered the original and spelling-perturbed sentences identical.
Stage 7 addresses this by implementing a **Visible-Target Evaluation**:
1. The target word remains visible in the input sequence at all times.
2. The target score is defined as the mean unnormalized logit across the target word's subwords:
   $$\text{Score}(X; Y_{\text{target}}) = \frac{1}{k} \sum_{j=1}^k \text{Logit}(p_j, y_j)$$
3. Faithfulness is assessed by intervening strictly on **context tokens** while keeping the target word intact.
   A faithful explanation requires that removing top-ranked context tokens degrades the target score more than
   removing bottom-ranked control tokens ($\Delta S_{\text{top}} > \Delta S_{\text{bottom}}$).

## 3. Eligibility & Multi-Subword Scope

| Model | Total Evaluated | Single-Subword Strict (N) | All Scorable Visible (N) | Notes |
|---|---|---|---|---|
| `muril-base-cased` | 20 | 6 | 20 | Multi-subword mean-logit enables 100% scorable coverage |
| `xlm-roberta-base` | 20 | 4 | 20 | Multi-subword mean-logit enables 100% scorable coverage |

## 4. Faithfulness Summary Results

| Model | Method | Subset | Fraction (f) | Mean Top Drop | Mean Bottom Drop | Mean Random Drop | Faithfulness Gap | Win Rate vs Bottom |
|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.10 | -7.1884 | -11.2055 | -10.4672 | **4.017** | 77.5% |
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.20 | -7.1884 | -11.2055 | -9.3811 | **4.017** | 77.5% |
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.30 | -5.7907 | -10.9623 | -7.8549 | **5.1716** | 75.0% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.10 | -6.6611 | -11.0067 | -10.476 | **4.3456** | 75.0% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.20 | -6.6611 | -11.0067 | -9.3573 | **4.3456** | 75.0% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.30 | -4.6781 | -9.8578 | -5.297 | **5.1797** | 75.0% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.10 | -9.2775 | -11.1149 | -8.5007 | **1.8373** | 60.0% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.20 | -9.2775 | -11.1149 | -8.8719 | **1.8373** | 60.0% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.30 | -6.0091 | -9.3043 | -8.0449 | **3.2952** | 55.0% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.10 | -8.4179 | -11.6642 | -9.3838 | **3.2463** | 50.0% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.20 | -8.4179 | -11.6642 | -8.709 | **3.2463** | 50.0% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.30 | -3.3873 | -5.1837 | -5.8557 | **1.7964** | 50.0% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.10 | 0.5861 | 0.1683 | 1.9389 | **0.4177** | 60.0% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.20 | 0.5861 | 0.1683 | 1.3919 | **0.4177** | 60.0% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.30 | 5.925 | 0.1307 | 2.7604 | **5.7943** | 70.0% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.10 | 4.5524 | 1.8606 | 4.1405 | **2.6918** | 66.7% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.20 | 4.5524 | 1.8606 | 5.6763 | **2.6918** | 66.7% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.30 | 12.8274 | 4.0054 | 8.3652 | **8.822** | 75.0% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.10 | 2.3678 | 3.0533 | 2.0388 | **-0.6855** | 45.0% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.20 | 2.3678 | 3.0533 | 0.7603 | **-0.6855** | 45.0% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.30 | 5.115 | 5.0825 | 5.9468 | **0.0325** | 42.5% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.10 | 7.3422 | 4.577 | 7.2221 | **2.7651** | 50.0% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.20 | 7.3422 | 4.577 | 4.0903 | **2.7651** | 50.0% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.30 | 12.4055 | 11.4038 | 11.2199 | **1.0017** | 41.7% |

## 5. Relationship Between Stability and Faithfulness
Stage 6's masked-target stability (rho = 1.0) had zero variance, making direct correlation undefined.
Below, we examine the relationship between **Visible-Target Stability** and the **Faithfulness Gap** (at f = 0.20):

| Pair ID | Model | Method | Visible Stability (Rho) | Visible Cosine Sim | Faithfulness Gap (Mean f=20%) |
|---|---|---|---|---|---|
| HC_0005 | `muril-base-cased` | `attention` | 0.5 | 0.9483 | -3.2326 |
| HC_0005 | `muril-base-cased` | `integrated_gradients` | -0.5 | 0.9878 | -11.3476 |
| HC_0006 | `muril-base-cased` | `attention` | 0.5 | 0.9171 | 13.0375 |
| HC_0006 | `muril-base-cased` | `integrated_gradients` | 0.1 | 0.9935 | -10.1287 |
| HC_0007 | `muril-base-cased` | `attention` | 0.9 | 0.9847 | -1.8948 |
| HC_0007 | `muril-base-cased` | `integrated_gradients` | 0.7 | 0.9974 | -1.909 |
| HC_0008 | `muril-base-cased` | `attention` | 0.6 | 0.9802 | -6.6143 |
| HC_0008 | `muril-base-cased` | `integrated_gradients` | 0.7 | 0.9973 | -3.2093 |
| HC_0041 | `muril-base-cased` | `attention` | 0.5 | 0.883 | 8.7504 |
| HC_0041 | `muril-base-cased` | `integrated_gradients` | 1.0 | 0.9977 | 2.2349 |
| HC_0050 | `muril-base-cased` | `attention` | 0.6 | 0.9304 | 5.9074 |
| HC_0050 | `muril-base-cased` | `integrated_gradients` | 1.0 | 0.9923 | -6.2058 |
| HC_0076 | `muril-base-cased` | `attention` | 0.4 | 0.9722 | -3.5886 |
| HC_0076 | `muril-base-cased` | `integrated_gradients` | 0.2 | 0.9881 | -2.3585 |
| HC_0077 | `muril-base-cased` | `attention` | -0.8 | 0.9151 | 3.4282 |

## 6. Scientific Limitations & Research Integrity
1. **Masking Intervention Artifacts**: Masking context tokens with `[MASK]` introduces out-of-distribution (OOD)
   artifacts into pretrained language models. Score drops reflect both information removal and unnatural token sequences.
2. **Attention as Non-Causal**: Attention weights reflect query-key interaction, not verified causal mechanisms.
   While Attention often correlates with degradation, Integrated Gradients provides the mathematically grounded gradient attribution.
3. **Small Sample Interpretation**: With 20 pairs in the spelling-error track, findings are exploratory and demonstrate
   methodological feasibility rather than population-wide statistical claims.
