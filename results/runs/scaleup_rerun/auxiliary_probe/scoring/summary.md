# Hindi Lexical Sensitivity - Pretrained Model PLL Scoring Summary

**Run Timestamp (UTC):** 2026-11-02T17:29:05.316776+00:00
**Run Type:** full
**Elapsed Time:** 12.12 seconds
**Input Dataset:** `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\data\final\AUXILIARY_MULTIWORD_PROBE.csv`
**Dataset SHA-256:** `208aabab0056f8287297d8800462c703afc7506f0d3e5fd5e7ff08fc23cf096e`
**Non-Empty Input Rows:** 12
**Total Pair Evaluations:** 24 (2 models x 12 pairs)

## 1. Models & Hardware Configuration
- **`FacebookAI/xlm-roberta-base`**: Class=`XLMRobertaForMaskedLM`, Vocab=`250002`, Device=`cuda`
- **`google/muril-base-cased`**: Class=`BertForMaskedLM`, Vocab=`197258`, Device=`cuda`

## 2. Mean PLL and Delta Log-Probability Across Tracks

> **Note on Comparability**: Raw PLL sums must NOT be compared directly across different model architectures or vocabularies. Comparisons are strictly within-model: $\Delta = \text{Contrast} - \text{Original}$.

| Model | Track | Pairs | Mean $\Delta$ PLL Sum | Mean $\Delta$ MeanLogP | Mean Original MeanLogP | Mean Contrast MeanLogP |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | -11.5767 | -1.2863 | -2.9785 | -4.2648 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | +3.0792 | +1.6957 | -4.7855 | -3.0898 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | -26.0177 | -3.3733 | -1.9615 | -5.3349 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | -13.2067 | -1.4674 | -2.4535 | -3.9209 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | -4.3458 | -0.5527 | -3.1854 | -3.7381 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | -16.9322 | -2.4124 | -1.9621 | -4.3745 |

## 3. Discrepancy Investigation & Data Integrity
- **Input SHA-256 Verified**: `208aabab0056f8287297d8800462c703afc7506f0d3e5fd5e7ff08fc23cf096e`.
- **Discrepancy Explained**: `openpyxl` reports 200 data rows + 0 trailing empty rows because it adheres to the worksheet `<dimension ref="A1:R201"/>` boundary. The standard library XML reader reports 799 trailing empty rows because Excel allocated empty `<row>` XML elements up to row 1000. In both cases, the populated data rows are exactly 200.
- **Preserved Records**: All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and 6 annotation disagreements, are scored and preserved.

## 4. Artifacts Generated
- Results CSV: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\scoring\pll_scoring_results.csv` (24 rows)
- Run Metadata: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\scoring\run_metadata.json`
- Summary Report: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\scoring\summary.md`
