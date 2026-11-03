# Stage 6: Hindi Explanation Stability Under Realistic Spelling Perturbations

## 1. Executive Summary and Experimental Context
- **Primary Track Evaluated**: `REALISTIC_SPELLING_ERROR` (all 20 pairs in the curated dataset)
- **Models Evaluated**: `google/muril-base-cased`, `FacebookAI/xlm-roberta-base`
- **Dataset SHA-256**: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
- **Timestamp (UTC)**: `2026-10-19T15:33:56.448712+00:00`
- **Explanation Methods**: `Self-Attention` (last-layer mean over heads) and `LayerIntegratedGradients` (embedding layer)
- **Target Definition**: Fixed canonical target logit at the masked position in both inputs (`Score = Logit(y_orig at m)`).

## 2. Methodology & Guardrails
1. **Fixed-Target Scoring**: Explains the model's evidence for the canonical intended word `y_orig` in both sentences.
   This holds the target concept constant, ensuring observed shifts are attributable strictly to the context spelling error.
2. **Region-Relative Context Alignment**: Because spelling errors alter character lengths (e.g., `स्वास्थ्य` [9 chars] $\to$ `स्वास्थ` [7 chars]),
   context tokens are aligned by region-relative offsets (`pre` and `post`). Special tokens and the target word are excluded.
   Attribution vectors are never zipped by token index.
3. **Strict Single-Subword Eligibility**: To avoid ambiguous unaggregated token-head attributions, only pairs where both original
   and contrast targets form a single subword are scored for stability. Multi-subword pairs are recorded explicitly with reasons.
4. **Stability Metrics**: Spearman rank correlation (rho), Top-k Jaccard overlap, and Cosine similarity over aligned context tokens.
   Undefined cases (insufficient tokens or zero variance) explicitly yield NaN.

## 3. Eligibility and Exclusion Summary

| Model | Total Evaluated | Eligible Pairs | Ineligible Pairs | Primary Exclusion Reasons |
|---|---|---|---|---|
| `google/muril-base-cased` | 20 | 6 | 14 | compound_subword_contrast_target (most frequent) |
| `FacebookAI/xlm-roberta-base` | 20 | 4 | 16 | compound_subword_contrast_target (most frequent) |

## 4. Stability Metric Summary (Exploratory Findings)

| Model | Method | Eligible (N) | Valid Metrics (N) | Spearman Rho (Mean) | Spearman Rho (Median) | Top-k Overlap (Mean) | Cosine Sim (Mean) |
|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `attention` | 4 | 4 | 1.0 | 1.0 | 1.0 | 1.0 |
| `xlm-roberta-base` | `integrated_gradients` | 4 | 4 | 1.0 | 1.0 | 1.0 | 1.0 |
| `muril-base-cased` | `attention` | 6 | 6 | 1.0 | 1.0 | 1.0 | 1.0 |
| `muril-base-cased` | `integrated_gradients` | 6 | 6 | 1.0 | 1.0 | 1.0 | 1.0 |

## 5. Pair-Level Results for Eligible Spelling Errors

| Pair ID | Model | Method | Target (Orig / Cont) | Delta Logit | Aligned Tokens | Spearman Rho | Top-k Overlap | Cosine Sim |
|---|---|---|---|---|---|---|---|---|
| HC_0077 | `muril-base-cased` | `attention` | परीक्षा / परिक्षा | 0.0 | 4 | 1.0 | 1.0 | 1.0 |
| HC_0077 | `muril-base-cased` | `integrated_gradients` | परीक्षा / परिक्षा | 0.0 | 4 | 1.0 | 1.0 | 1.0 |
| HC_0078 | `muril-base-cased` | `attention` | स्वास्थ्य / स्वास्थ | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0078 | `muril-base-cased` | `integrated_gradients` | स्वास्थ्य / स्वास्थ | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0118 | `muril-base-cased` | `attention` | महत्वपूर्ण / महत्त्वपूर्ण | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0118 | `muril-base-cased` | `integrated_gradients` | महत्वपूर्ण / महत्त्वपूर्ण | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0119 | `muril-base-cased` | `attention` | दी / दि | 0.0 | 4 | 1.0 | 1.0 | 1.0 |
| HC_0119 | `muril-base-cased` | `integrated_gradients` | दी / दि | 0.0 | 4 | 1.0 | 1.0 | 1.0 |
| HC_0120 | `muril-base-cased` | `attention` | संभावना / सम्भावना | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0120 | `muril-base-cased` | `integrated_gradients` | संभावना / सम्भावना | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0197 | `muril-base-cased` | `attention` | वापस / वापिस | 0.0 | 5 | 1.0 | 1.0 | 1.0 |
| HC_0197 | `muril-base-cased` | `integrated_gradients` | वापस / वापिस | 0.0 | 5 | 1.0 | 1.0 | 1.0 |
| HC_0088 | `xlm-roberta-base` | `attention` | घूम / घुम | 0.0 | 7 | 1.0 | 1.0 | 1.0 |
| HC_0088 | `xlm-roberta-base` | `integrated_gradients` | घूम / घुम | 0.0 | 7 | 1.0 | 1.0 | 1.0 |
| HC_0118 | `xlm-roberta-base` | `attention` | महत्वपूर्ण / महत्त्वपूर्ण | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0118 | `xlm-roberta-base` | `integrated_gradients` | महत्वपूर्ण / महत्त्वपूर्ण | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0119 | `xlm-roberta-base` | `attention` | दी / दि | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0119 | `xlm-roberta-base` | `integrated_gradients` | दी / दि | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0120 | `xlm-roberta-base` | `attention` | संभावना / सम्भावना | 0.0 | 6 | 1.0 | 1.0 | 1.0 |
| HC_0120 | `xlm-roberta-base` | `integrated_gradients` | संभावना / सम्भावना | 0.0 | 6 | 1.0 | 1.0 | 1.0 |

## 6. Scientific Limitations and Research Integrity
1. **Exploratory Sample Size**: Under strict single-subword criteria, only 6 pairs in MuRIL and 4 in XLM-R are eligible.
   No general inferential claims about Hindi language robustness can be made from this sample.
2. **Stability vs Faithfulness**: High explanation stability does NOT imply explanation faithfulness.
   Measuring whether stable explanations reflect actual model decision mechanisms requires independent perturbation/faithfulness testing (Stage 7).
3. **Attention as Non-Causal**: Attention weights reflect query-key routing inside the model, not verified causal importance.
