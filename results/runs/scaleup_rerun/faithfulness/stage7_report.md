# Stage 7: Faithfulness Evaluation for the Hindi NLP Research Project

## 1. Executive Summary & Experimental Context
- **Primary Track Evaluated**: `REALISTIC_SPELLING_ERROR` (20 curated sentence pairs)
- **Models Evaluated**: `google/muril-base-cased, FacebookAI/xlm-roberta-base`
- **Dataset SHA-256**: `b769ccd82ee00b7930c8f32a7666e5d16897d0afc8c10c1cc97633334717fe18`
- **Timestamp (UTC)**: `2026-11-02T17:23:42.108862+00:00`
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
| `muril-base-cased` | 1005 | 197 | 1005 | Multi-subword mean-logit enables 100% scorable coverage |
| `xlm-roberta-base` | 1005 | 52 | 1005 | Multi-subword mean-logit enables 100% scorable coverage |

## 4. Faithfulness Summary Results

| Model | Method | Subset | Fraction (f) | Mean Top Drop | Mean Bottom Drop | Mean Random Drop | Faithfulness Gap | Win Rate vs Bottom |
|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.10 | -6.2969 | -8.7344 | -7.8968 | **2.4374** | 63.5% |
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.20 | -6.2915 | -9.0881 | -8.3099 | **2.7966** | 65.8% |
| `xlm-roberta-base` | `attention` | `all_scorable` | 0.30 | -4.4711 | -8.2846 | -6.6174 | **3.8134** | 67.5% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.10 | -2.1218 | -4.8635 | -4.3861 | **2.7417** | 69.2% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.20 | -1.5806 | -5.187 | -3.9164 | **3.6064** | 69.2% |
| `xlm-roberta-base` | `attention` | `strict_single_subword` | 0.30 | 0.2633 | -2.9888 | -1.8542 | **3.2521** | 59.6% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.10 | -6.995 | -8.9797 | -7.8777 | **1.9847** | 59.8% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.20 | -7.012 | -9.2597 | -8.0825 | **2.2477** | 62.2% |
| `xlm-roberta-base` | `integrated_gradients` | `all_scorable` | 0.30 | -4.7837 | -8.1795 | -6.7426 | **3.3957** | 65.1% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.10 | -3.3843 | -5.079 | -4.0995 | **1.6947** | 54.8% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.20 | -2.2529 | -5.1072 | -3.6447 | **2.8543** | 64.4% |
| `xlm-roberta-base` | `integrated_gradients` | `strict_single_subword` | 0.30 | 1.7194 | -2.9455 | -0.3833 | **4.6649** | 64.4% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.10 | -0.7615 | 1.2553 | 1.5249 | **-2.0168** | 33.9% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.20 | 0.8319 | 3.1532 | 3.1754 | **-2.3213** | 35.4% |
| `muril-base-cased` | `attention` | `all_scorable` | 0.30 | 4.4916 | 4.0916 | 4.9273 | **0.4001** | 49.6% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.10 | 3.7321 | 4.1364 | 5.0855 | **-0.4042** | 40.4% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.20 | 7.0699 | 8.2413 | 8.9152 | **-1.1714** | 40.4% |
| `muril-base-cased` | `attention` | `strict_single_subword` | 0.30 | 12.8258 | 10.2288 | 12.4061 | **2.597** | 56.6% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.10 | 1.3262 | 1.626 | 1.8552 | **-0.2998** | 49.9% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.20 | 2.7479 | 3.2616 | 3.7076 | **-0.5137** | 49.4% |
| `muril-base-cased` | `integrated_gradients` | `all_scorable` | 0.30 | 4.5079 | 5.5924 | 5.321 | **-1.0845** | 46.7% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.10 | 4.4698 | 5.2449 | 5.5086 | **-0.775** | 51.5% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.20 | 7.9625 | 9.4844 | 9.5399 | **-1.5219** | 47.5% |
| `muril-base-cased` | `integrated_gradients` | `strict_single_subword` | 0.30 | 11.7011 | 14.0597 | 13.5496 | **-2.3586** | 45.4% |

## 5. Relationship Between Stability and Faithfulness
Stage 6's masked-target stability (rho = 1.0) had zero variance, making direct correlation undefined.
Below, we examine the relationship between **Visible-Target Stability** and the **Faithfulness Gap** (at f = 0.20):

| Pair ID | Model | Method | Visible Stability (Rho) | Visible Cosine Sim | Faithfulness Gap (Mean f=20%) |
|---|---|---|---|---|---|
| HC_0005 | `muril-base-cased` | `attention` | 0.5 | 0.9483 | -3.2327 |
| HC_0005 | `muril-base-cased` | `integrated_gradients` | -0.5 | 0.9878 | -11.3476 |
| HC_0006 | `muril-base-cased` | `attention` | 0.5 | 0.9171 | 13.0374 |
| HC_0006 | `muril-base-cased` | `integrated_gradients` | 0.1 | 0.9934 | -10.1285 |
| HC_0007 | `muril-base-cased` | `attention` | 0.9 | 0.9847 | -1.8949 |
| HC_0007 | `muril-base-cased` | `integrated_gradients` | 0.7 | 0.9974 | -1.9091 |
| HC_0008 | `muril-base-cased` | `attention` | 0.6 | 0.9802 | -6.6141 |
| HC_0008 | `muril-base-cased` | `integrated_gradients` | 0.7 | 0.9973 | -3.2093 |
| HC_0041 | `muril-base-cased` | `attention` | 0.5 | 0.883 | 8.7503 |
| HC_0041 | `muril-base-cased` | `integrated_gradients` | 1.0 | 0.9976 | 2.2349 |
| HC_0050 | `muril-base-cased` | `attention` | 0.6 | 0.9304 | 5.9073 |
| HC_0050 | `muril-base-cased` | `integrated_gradients` | 1.0 | 0.9923 | -6.206 |
| HC_0076 | `muril-base-cased` | `attention` | 0.4 | 0.9722 | -3.5887 |
| HC_0076 | `muril-base-cased` | `integrated_gradients` | 0.2 | 0.9881 | -2.3585 |
| HC_0077 | `muril-base-cased` | `attention` | -0.8 | 0.9151 | 3.428 |

## 6. Scientific Limitations & Research Integrity
1. **Masking Intervention Artifacts**: Masking context tokens with `[MASK]` introduces out-of-distribution (OOD)
   artifacts into pretrained language models. Score drops reflect both information removal and unnatural token sequences.
2. **Attention as Non-Causal**: Attention weights reflect query-key interaction, not verified causal mechanisms.
   While Attention often correlates with degradation, Integrated Gradients provides the mathematically grounded gradient attribution.
3. **Small Sample Interpretation**: With 20 pairs in the spelling-error track, findings are exploratory and demonstrate
   methodological feasibility rather than population-wide statistical claims.
