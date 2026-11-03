# Hindi Lexical Sensitivity - Tokenization Experiment Summary

**Run Timestamp (UTC):** 2026-10-19T07:12:56.190999+00:00
**Input Dataset:** `D:\hindi-lexical-sensitivity\data\raw\hindi_lexical_sensitivity_cleaned.xlsx`
**Dataset SHA-256:** `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
**Input Data Rows:** 200 (799 empty trailing rows ignored)
**Total Evaluations:** 400 rows (2 models x 200 sentence pairs)

## 1. Models Evaluated
- **`FacebookAI/xlm-roberta-base`**: Fast Tokenizer=`True`, Vocab Size=`250002`, Class=`XLMRobertaTokenizerFast`
- **`google/muril-base-cased`**: Fast Tokenizer=`True`, Vocab Size=`197285`, Class=`BertTokenizerFast`

## 2. Alignment Outcomes

| Model | Original Unique | Original Ambiguous | Original Missing | Contrast Unique | Contrast Ambiguous | Contrast Missing |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | 200 | 0 | 0 | 200 | 0 | 0 |
| `google/muril-base-cased` | 200 | 0 | 0 | 200 | 0 | 0 |

## 3. Token Count Distribution Across Tracks (Signed Delta: Contrast - Original)

| Model | Track | Count | Mean Inclusive Delta | Min Inclusive Delta | Max Inclusive Delta | Mean Target Delta |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | +1.00 | +0 | +2 | +1.00 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | +0.61 | -1 | +4 | +0.63 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 142 | +0.17 | -1 | +2 | +0.17 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | +1.00 | +0 | +2 | +1.00 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | +0.18 | +0 | +2 | +0.18 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 142 | +0.08 | -2 | +2 | +0.08 |

## 4. Dataset Preservation & Human Review Status
- **Preserved Rows:** All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and the 6 annotator/adjudication disagreement items.
- **No Unchecked Filtering:** Zero rows discarded or altered.
- **Interpretive Guardrail:** Token count differences reflect subword vocabulary segmentation, not grammatical correctness or semantic validity.

## 5. Artifacts Generated
- Results CSV: `D:\hindi-lexical-sensitivity\outputs\tokenization\tokenization_results.csv` (400 rows)
- Metadata JSON: `D:\hindi-lexical-sensitivity\outputs\tokenization\run_metadata.json`
- Summary Report: `D:\hindi-lexical-sensitivity\outputs\tokenization\summary.md`
