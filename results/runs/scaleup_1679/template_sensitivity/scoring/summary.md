# Hindi Lexical Sensitivity - Pretrained Model PLL Scoring Summary

**Run Timestamp (UTC):** 2026-11-02T15:59:10.020940+00:00
**Run Type:** full
**Elapsed Time:** 228.65 seconds
**Input Dataset:** `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\data\final\TEMPLATE_SENSITIVITY_BENCHMARK.csv`
**Dataset SHA-256:** `b88160d39d1f7133391ff3aceff1faa2f157310833490e3765ae635c17e0155a`
**Non-Empty Input Rows:** 1957
**Total Pair Evaluations:** 3914 (2 models x 1957 pairs)

## 1. Models & Hardware Configuration
- **`FacebookAI/xlm-roberta-base`**: Class=`XLMRobertaForMaskedLM`, Vocab=`250002`, Device=`cuda`
- **`google/muril-base-cased`**: Class=`BertForMaskedLM`, Vocab=`197258`, Device=`cuda`

## 2. Mean PLL and Delta Log-Probability Across Tracks

> **Note on Comparability**: Raw PLL sums must NOT be compared directly across different model architectures or vocabularies. Comparisons are strictly within-model: $\Delta = \text{Contrast} - \text{Original}$.

| Model | Track | Pairs | Mean $\Delta$ PLL Sum | Mean $\Delta$ MeanLogP | Mean Original MeanLogP | Mean Contrast MeanLogP |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1260 | -8.9346 | -0.6941 | -2.4153 | -3.1094 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 385 | -0.2553 | -0.0026 | -2.7764 | -2.7790 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | -8.7187 | -1.0831 | -2.3210 | -3.4042 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1260 | -11.5112 | -1.0778 | -2.5692 | -3.6470 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 385 | -1.1595 | -0.1770 | -2.7789 | -2.9559 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | -12.9546 | -1.8470 | -2.4496 | -4.2965 |

## 3. Discrepancy Investigation & Data Integrity
- **Input SHA-256 Verified**: `b88160d39d1f7133391ff3aceff1faa2f157310833490e3765ae635c17e0155a`.
- **Discrepancy Explained**: `openpyxl` reports 200 data rows + 0 trailing empty rows because it adheres to the worksheet `<dimension ref="A1:R201"/>` boundary. The standard library XML reader reports 799 trailing empty rows because Excel allocated empty `<row>` XML elements up to row 1000. In both cases, the populated data rows are exactly 200.
- **Preserved Records**: All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and 6 annotation disagreements, are scored and preserved.

## 4. Artifacts Generated
- Results CSV: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\scoring\pll_scoring_results.csv` (3914 rows)
- Run Metadata: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\scoring\run_metadata.json`
- Summary Report: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\scoring\summary.md`
