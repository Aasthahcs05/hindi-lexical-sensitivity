# Hindi Lexical Sensitivity - Pretrained Model PLL Scoring Summary

**Run Timestamp (UTC):** 2026-10-19T13:59:36.192093+00:00
**Run Type:** pilot
**Elapsed Time:** 25.27 seconds
**Input Dataset:** `D:\hindi-lexical-sensitivity\data\raw\hindi_lexical_sensitivity_cleaned.xlsx`
**Dataset SHA-256:** `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
**Non-Empty Input Rows:** 200
**Total Pair Evaluations:** 14 (2 models x 7 pairs)

## 1. Models & Hardware Configuration
- **`FacebookAI/xlm-roberta-base`**: Class=`XLMRobertaForMaskedLM`, Vocab=`250002`, Device=`cpu`
- **`google/muril-base-cased`**: Class=`BertForMaskedLM`, Vocab=`197285`, Device=`cpu`

## 2. Mean PLL and Delta Log-Probability Across Tracks

> **Note on Comparability**: Raw PLL sums must NOT be compared directly across different model architectures or vocabularies. Comparisons are strictly within-model: $\Delta = \text{Contrast} - \text{Original}$.

| Model | Track | Pairs | Mean $\Delta$ PLL Sum | Mean $\Delta$ MeanLogP | Mean Original MeanLogP | Mean Contrast MeanLogP |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 2 | -16.6084 | -2.2499 | -2.3347 | -4.5846 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 2 | -2.6590 | -0.4630 | -2.8089 | -3.2718 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | -12.4450 | -1.9114 | -2.6803 | -4.5916 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 2 | -22.4880 | -2.8967 | -2.7534 | -5.6501 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 2 | -2.8771 | -0.5211 | -2.2809 | -2.8020 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | -8.6719 | -1.3675 | -2.3315 | -3.6991 |

## 3. Discrepancy Investigation & Data Integrity
- **Input SHA-256 Verified**: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`.
- **Discrepancy Explained**: `openpyxl` reports 200 data rows + 0 trailing empty rows because it adheres to the worksheet `<dimension ref="A1:R201"/>` boundary. The standard library XML reader reports 799 trailing empty rows because Excel allocated empty `<row>` XML elements up to row 1000. In both cases, the populated data rows are exactly 200.
- **Preserved Records**: All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and 6 annotation disagreements, are scored and preserved.

## 4. Artifacts Generated
- Results CSV: `D:\hindi-lexical-sensitivity\outputs\scoring\pilot\pll_scoring_results.csv` (14 rows)
- Run Metadata: `D:\hindi-lexical-sensitivity\outputs\scoring\pilot\run_metadata.json`
- Summary Report: `D:\hindi-lexical-sensitivity\outputs\scoring\pilot\summary.md`
