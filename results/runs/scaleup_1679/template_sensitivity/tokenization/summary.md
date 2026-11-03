# Hindi Lexical Sensitivity - Tokenization Experiment Summary

**Run Timestamp (UTC):** 2026-11-02T15:55:20.850086+00:00
**Input Dataset:** `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\data\final\TEMPLATE_SENSITIVITY_BENCHMARK.csv`
**Dataset SHA-256:** `b88160d39d1f7133391ff3aceff1faa2f157310833490e3765ae635c17e0155a`
**Input Data Rows:** 1957 (799 empty trailing rows ignored)
**Total Evaluations:** 3914 rows (2 models x 1957 sentence pairs)

## 1. Models Evaluated
- **`FacebookAI/xlm-roberta-base`**: Fast Tokenizer=`True`, Vocab Size=`250002`, Class=`XLMRobertaTokenizer`
- **`google/muril-base-cased`**: Fast Tokenizer=`True`, Vocab Size=`197258`, Class=`BertTokenizer`

## 2. Alignment Outcomes

| Model | Original Unique | Original Ambiguous | Original Missing | Contrast Unique | Contrast Ambiguous | Contrast Missing |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | 1957 | 0 | 0 | 1957 | 0 | 0 |
| `google/muril-base-cased` | 1957 | 0 | 0 | 1957 | 0 | 0 |

## 3. Token Count Distribution Across Tracks (Signed Delta: Contrast - Original)

| Model | Track | Count | Mean Inclusive Delta | Min Inclusive Delta | Max Inclusive Delta | Mean Target Delta |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1260 | +1.12 | -4 | +3 | +1.12 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 385 | +0.19 | -2 | +4 | +0.19 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | +0.22 | -1 | +2 | +0.22 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1260 | +1.16 | -2 | +4 | +1.16 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 385 | +0.09 | -2 | +3 | +0.09 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | +0.11 | -2 | +2 | +0.11 |

## 4. Dataset Preservation & Human Review Status
- **Preserved Rows:** All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and the 6 annotator/adjudication disagreement items.
- **No Unchecked Filtering:** Zero rows discarded or altered.
- **Interpretive Guardrail:** Token count differences reflect subword vocabulary segmentation, not grammatical correctness or semantic validity.

## 5. Artifacts Generated
- Results CSV: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\tokenization\tokenization_results.csv` (3914 rows)
- Metadata JSON: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\tokenization\run_metadata.json`
- Summary Report: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_1679\template_sensitivity\tokenization\summary.md`
