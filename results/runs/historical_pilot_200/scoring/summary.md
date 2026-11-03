# Hindi Lexical Sensitivity - Pretrained Model PLL Scoring Summary

**Run Timestamp (UTC):** 2026-10-19T14:13:44.047114+00:00
**Run Type:** full
**Elapsed Time:** 88.90 seconds
**Input Dataset:** `D:\hindi-lexical-sensitivity\data\raw\hindi_lexical_sensitivity_cleaned.xlsx`
**Dataset SHA-256:** `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
**Non-Empty Input Rows:** 200
**Total Pair Evaluations:** 400 (2 models x 200 pairs)

## 1. Models & Hardware Configuration
- **`FacebookAI/xlm-roberta-base`**: Class=`Cached`, Vocab=`Cached`, Device=`cpu`
- **`google/muril-base-cased`**: Class=`BertForMaskedLM`, Vocab=`197285`, Device=`cpu`

## 2. Mean PLL and Delta Log-Probability Across Tracks

> **Note on Comparability**: Raw PLL sums must NOT be compared directly across different model architectures or vocabularies. Comparisons are strictly within-model: $\Delta = \text{Contrast} - \text{Original}$.

| Model | Track | Pairs | Mean $\Delta$ PLL Sum | Mean $\Delta$ MeanLogP | Mean Original MeanLogP | Mean Contrast MeanLogP |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | -7.7439 | -0.6695 | -2.7353 | -3.4049 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | -1.4183 | -0.0655 | -2.3344 | -2.3999 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 142 | -7.7425 | -1.0933 | -2.4307 | -3.5241 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | -16.1899 | -2.0368 | -2.5585 | -4.5953 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | -3.9947 | -0.5810 | -2.0416 | -2.6227 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 142 | -12.5616 | -1.9141 | -2.4972 | -4.4113 |

## 3. Discrepancy Investigation & Data Integrity
- **Input SHA-256 Verified**: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`.
- **Discrepancy Explained**: `openpyxl` reports 200 data rows + 0 trailing empty rows because it adheres to the worksheet `<dimension ref="A1:R201"/>` boundary. The standard library XML reader reports 799 trailing empty rows because Excel allocated empty `<row>` XML elements up to row 1000. In both cases, the populated data rows are exactly 200.
- **Preserved Records**: All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and 6 annotation disagreements, are scored and preserved.

## 4. Artifacts Generated
- Results CSV: `D:\hindi-lexical-sensitivity\outputs\scoring\pll_scoring_results.csv` (400 rows)
- Run Metadata: `D:\hindi-lexical-sensitivity\outputs\scoring\run_metadata.json`
- Summary Report: `D:\hindi-lexical-sensitivity\outputs\scoring\summary.md`
