# Hindi Lexical Sensitivity - Tokenization Experiment Summary

**Run Timestamp (UTC):** 2026-11-02T17:28:52.680303+00:00
**Input Dataset:** `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\data\final\AUXILIARY_MULTIWORD_PROBE.csv`
**Dataset SHA-256:** `208aabab0056f8287297d8800462c703afc7506f0d3e5fd5e7ff08fc23cf096e`
**Input Data Rows:** 12 (799 empty trailing rows ignored)
**Total Evaluations:** 24 rows (2 models x 12 sentence pairs)

## 1. Models Evaluated
- **`FacebookAI/xlm-roberta-base`**: Fast Tokenizer=`True`, Vocab Size=`250002`, Class=`XLMRobertaTokenizer`
- **`google/muril-base-cased`**: Fast Tokenizer=`True`, Vocab Size=`197258`, Class=`BertTokenizer`

## 2. Alignment Outcomes

| Model | Original Unique | Original Ambiguous | Original Missing | Contrast Unique | Contrast Ambiguous | Contrast Missing |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | 8 | 4 | 0 | 12 | 0 | 0 |
| `google/muril-base-cased` | 8 | 4 | 0 | 12 | 0 | 0 |

## 3. Token Count Distribution Across Tracks (Signed Delta: Contrast - Original)

| Model | Track | Count | Mean Inclusive Delta | Min Inclusive Delta | Max Inclusive Delta | Mean Target Delta |
|---|---|---|---|---|---|---|
| `FacebookAI/xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | +0.00 | +0 | +0 | +0.00 |
| `FacebookAI/xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | +1.00 | +0 | +2 | +0.62 |
| `FacebookAI/xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | +0.00 | +0 | +0 | +0.00 |
| `google/muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | +0.00 | +0 | +0 | +0.00 |
| `google/muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | +0.50 | +0 | +3 | +0.25 |
| `google/muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | +0.00 | +0 | +0 | +0.00 |

## 4. Dataset Preservation & Human Review Status
- **Preserved Rows:** All 200 non-empty rows, including the 1 rejected item (`final_status=reject`) and the 6 annotator/adjudication disagreement items.
- **No Unchecked Filtering:** Zero rows discarded or altered.
- **Interpretive Guardrail:** Token count differences reflect subword vocabulary segmentation, not grammatical correctness or semantic validity.

## 5. Artifacts Generated
- Results CSV: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\tokenization\tokenization_results.csv` (24 rows)
- Metadata JSON: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\tokenization\run_metadata.json`
- Summary Report: `C:\Users\Friends\Downloads\hindi-lexical-sensitivity (3)\hindi-lexical-sensitivity\results\runs\scaleup_rerun\auxiliary_probe\tokenization\summary.md`
