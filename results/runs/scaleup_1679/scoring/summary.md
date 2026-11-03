# Hindi Lexical Sensitivity - Pretrained Model PLL Scoring Summary

**Run Timestamp (UTC):** 2026-11-02T15:32:12.328148+00:00
**Run Type:** full
**Elapsed Time:** 206.98 seconds
**Input Dataset:** `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\data\final\PRIMARY_BENCHMARK_ADJUDICATED.csv`
**Dataset SHA-256:** `b769ccd82ee00b7930c8f32a7666e5d16897d0afc8c10c1cc97633334717fe18`
**Non-Empty Input Rows:** 1679
**Total Pair Evaluations:** 3358 (2 models x 1679 pairs)

## 1. Models & Hardware Configuration
- **`FacebookAI/xlm-roberta-base`**: Class=`XLMRobertaForMaskedLM`, Vocab=`250002`, Device=`cuda`
- **`google/muril-base-cased`**: Class=`BertForMaskedLM`, Vocab=`197258`, Device=`cuda`

## 2. Mean PLL and Delta Log-Probability Across Tracks

> **Note on Comparability**: Raw PLL sums must NOT be compared directly across different model architectures or vocabularies. Comparisons are strictly within-model: $\Delta = \text{Contrast} - \text{Original}$.

| Model | Track | Pairs | Mean $\Delta$ PLL Sum | Mean $\Delta$ MeanLogP | Mean Original MeanLogP | Mean Contrast MeanLogP |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1005 | -10.2231 | -0.8864 | -2.2198 | -3.1062 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 362 | -0.3040 | -0.0098 | -2.7942 | -2.8040 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | -8.7187 | -1.0831 | -2.3210 | -3.4042 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1005 | -12.0761 | -1.2045 | -2.4127 | -3.6172 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 362 | -1.1435 | -0.1787 | -2.7603 | -2.9390 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | -12.9546 | -1.8470 | -2.4496 | -4.2965 |

## 3. Discrepancy Investigation & Data Integrity
- **Input SHA-256 Verified**: `b769ccd82ee00b7930c8f32a7666e5d16897d0afc8c10c1cc97633334717fe18`.
- **Discrepancy Explained**: `openpyxl` reports 200 data rows + 0 trailing empty rows because it adheres to the worksheet `<dimension ref="A1:R201"/>` boundary. The standard library XML reader reports 799 trailing empty rows because Excel allocated empty `<row>` XML elements up to row 1000. In both cases, the populated data rows are exactly 200.
- **Preserved Records**: All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and 6 annotation disagreements, are scored and preserved.

## 4. Artifacts Generated
- Results CSV: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\scoring\pll_scoring_results.csv` (3358 rows)
- Run Metadata: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\scoring\run_metadata.json`
- Summary Report: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\scoring\summary.md`
