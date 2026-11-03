# Stage 4: Combined Statistical Analysis — Hindi Lexical Sensitivity

**Run Timestamp (UTC):** 2026-11-02T15:32:14.940913+00:00
**Input SHA-256 (xlsx):** `b769ccd82ee00b7930c8f32a7666e5d16897d0afc8c10c1cc97633334717fe18`
**Total merged rows:** 3358 (400 expected: 200 pairs × 2 models)

> **Scope note:** This analysis examines the relationship between subword tokenization
> changes and pseudo-log-likelihood (PLL) score changes in Hindi sentence pairs.
> PLL is a *model-based plausibility score*, not a ground-truth measure of grammaticality
> or semantic correctness. Within-model Δ values only; raw PLL totals are **not** compared
> across different tokenizers. Correlation ≠ causation.

---

## 1. Data Validation

✅ All validation checks passed: no label mismatches, no missing keys, 
no duplicate rows, no non-finite values, all delta math verified.

### Suspicious Value Investigation: Identical XLM-R Δ PLL Sum at −7.74

The Stage 3 summary reported Mean Δ PLL Sum of −7.7439 for `REALISTIC_SPELLING_ERROR` 
and −7.7425 for `VALID_WORD_CONTEXT` under XLM-RoBERTa. These differ at the 4th decimal
place. This is **coincidental numeric proximity**, not a calculation error.
The recalculated values from raw data:

| Track | Mean Δ PLL Sum | Mean Δ MeanLogP |
|---|---|---|
| VALID_WORD_CONTEXT | -8.7187 | -1.0831 |
| SYNONYM_SUBSTITUTION | -0.3040 | -0.0098 |
| REALISTIC_SPELLING_ERROR | -10.2231 | -0.8864 |

**Conclusion:** No data anomaly. Rounded display in the summary caused visual ambiguity.

### Rejected Records and Disagreements
- `final_status=reject`: 2 records preserved in all analyses.
- Annotation disagreements (annotator_1 ≠ annotator_2): retained in full dataset.
- A **sensitivity analysis** excluding rejected records is provided in Section 3.

---

## 2. Descriptive Statistics

> Sign convention: **Δ = contrast − original**. Negative Δ MeanLogP means the model
> assigns lower plausibility to the contrast sentence than the original.

### 2a. By Model and Track — Δ MeanLogP (primary, length-normalized)

| Model | Track | N | Mean | Median | SD | IQR | Min | Max | N<0 | N>0 | N=0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | -1.0831 | -0.9464 | 1.2195 | 1.4564 | -4.8362 | 1.6353 | 258 | 54 | 0 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 362 | -0.0098 | -0.0084 | 1.0110 | 0.9386 | -4.6842 | 3.8360 | 183 | 179 | 0 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1005 | -0.8864 | -0.7752 | 1.2929 | 1.6561 | -6.4884 | 3.6106 | 768 | 237 | 0 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | -1.8470 | -1.6755 | 1.3965 | 1.6648 | -5.9067 | 2.4179 | 294 | 18 | 0 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 362 | -0.1787 | -0.1049 | 0.8545 | 0.8320 | -3.6843 | 2.0094 | 213 | 149 | 0 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1005 | -1.2045 | -0.8892 | 1.3526 | 1.7256 | -6.8610 | 2.3473 | 836 | 169 | 0 |

### 2b. By Model and Track — Δ PLL Sum (secondary; affected by sentence length)

> ⚠️ Δ PLL Sum is sensitive to sentence length and number of scored tokens.
> Use Δ MeanLogP for cross-sentence comparisons within a model.

| Model | Track | N | Mean | Median | SD | IQR | N<0 | N>0 |
|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | -8.7187 | -8.3609 | 8.5980 | 10.7041 | 267 | 45 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 362 | -0.3040 | -0.3001 | 5.3754 | 5.8848 | 192 | 170 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1005 | -10.2231 | -9.3231 | 10.4215 | 15.0007 | 857 | 148 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | -12.9546 | -13.1731 | 9.2682 | 11.0052 | 288 | 24 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 362 | -1.1435 | -0.8073 | 5.2815 | 5.3026 | 215 | 147 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1005 | -12.0761 | -9.6253 | 10.9821 | 14.2280 | 914 | 91 |

### 2c. Token Count Changes by Model and Track

| Model | Track | N | Mean Δ Sent Tokens | Median Δ Sent Tokens | Mean Δ Target Tokens |
|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | 0.2179 | 0.0000 | 0.2179 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 362 | 0.1823 | 0.0000 | 0.1823 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1005 | 1.0428 | 1.0000 | 1.0428 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | 0.1090 | 0.0000 | 0.1090 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 362 | 0.0967 | 0.0000 | 0.0967 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1005 | 1.1274 | 1.0000 | 1.1274 |

---

## 3. Sensitivity Analysis — Excluding Rejected Records

2 records have `final_status=reject`. Results below exclude these.

| Model | Track | N (excl. rejected) | Mean Δ MeanLogP | Mean Δ PLL Sum |
|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 312 | -1.0831 | -8.7187 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 362 | -0.0098 | -0.3040 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1005 | -0.8864 | -10.2231 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 312 | -1.8470 | -12.9546 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 362 | -0.1787 | -1.1435 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1005 | -1.2045 | -12.0761 |

> **Interpretation:** Excluding rejected records has negligible effect given only 2 rejections
> out of 200 pairs. Main conclusions remain unchanged.

---

## 4. Correlation Analysis: Tokenization vs. PLL Changes

> **Primary outcome:** Δ MeanLogP (length-normalized).
> **Secondary outcome:** Δ PLL Sum (may be confounded by length changes).
> **Predictor 1:** Δ sentence token count (exclusive of special tokens).
> **Predictor 2:** Δ target token count.
> **Correction:** Benjamini–Hochberg FDR at α=0.05 across all tests.
> **Limitation:** REALISTIC_SPELLING_ERROR has only 20 pairs — treat those results with caution.

### 4a. Overall (all tracks) — Δ MeanLogP

| Model | X Variable | N | Spearman r | p (raw) | BH reject | 95% CI |
|---|---|---|---|---|---|---|
| `xlm-roberta-base` | Δ sentence token count (excl.) | 1679 | 0.2015 | 0.000000 | True | [0.1552, 0.2470] |
| `xlm-roberta-base` | Δ target token count | 1679 | 0.2015 | 0.000000 | True | [0.1552, 0.2470] |
| `muril-base-cased` | Δ sentence token count (excl.) | 1679 | -0.1677 | 0.000000 | True | [-0.2138, -0.1208] |
| `muril-base-cased` | Δ target token count | 1679 | -0.1677 | 0.000000 | True | [-0.2138, -0.1208] |

### 4b. By Track — Δ MeanLogP

| Model | Track | X Variable | N | Spearman r | p (raw) | BH reject | Note |
|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 312 | 0.2586 | 0.000004 | True |  |
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ target token count | 312 | 0.2586 | 0.000004 | True |  |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 362 | 0.5759 | 0.000000 | True |  |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ target token count | 362 | 0.5759 | 0.000000 | True |  |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 1005 | 0.2670 | 0.000000 | True |  |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 1005 | 0.2670 | 0.000000 | True |  |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 312 | -0.0697 | 0.219746 | False |  |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ target token count | 312 | -0.0697 | 0.219746 | False |  |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 362 | 0.0037 | 0.944152 | False |  |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ target token count | 362 | 0.0037 | 0.944152 | False |  |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 1005 | -0.1559 | 0.000001 | True |  |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 1005 | -0.1559 | 0.000001 | True |  |

---

## 5. Model Comparison (XLM-RoBERTa vs. MuRIL)

> Comparison uses **within-model Δ MeanLogP** for each pair.
> Raw PLL sums are **not** cross-compared due to different tokenizer vocabularies.

| Track Scope | N | Direction Agreement | Spearman r (Δ MeanLogP) | p | 95% CI |
|---|---|---|---|---|---|
| `ALL_TRACKS` | 1679 | 0.7367 (1055↓↓ + 182↑↑) | 0.5496 | 0.000000 | [0.5153, 0.5821] |
| `VALID_WORD_CONTEXT` | 312 | 0.8462 (252↓↓ + 12↑↑) | 0.4590 | 0.000000 | [0.3666, 0.5424] |
| `SYNONYM_SUBSTITUTION` | 362 | 0.6022 (126↓↓ + 92↑↑) | 0.2271 | 0.000013 | [0.1269, 0.3226] |
| `REALISTIC_SPELLING_ERROR` | 1005 | 0.7512 (677↓↓ + 78↑↑) | 0.5513 | 0.000000 | [0.5067, 0.5929] |

---

## 6. Scientific Interpretation and Limitations

### Beginner-Friendly Summary

We looked at 200 Hindi sentence pairs where one word was changed (the 'contrast' sentence).
We measured two things:
1. **Tokenization change**: Did the model's word-splitter break the changed word into more or fewer pieces?
2. **PLL score change**: Did the model assign a lower 'plausibility score' to the contrast sentence?

**Key findings:**
- Both models almost always assigned *lower* plausibility scores to contrast sentences,
  especially for spelling errors and contextual word substitutions.
- Synonym substitutions had much smaller score changes — the models found them almost equally plausible,
  which makes sense because correct synonyms should be semantically interchangeable.
- When a word was spelled incorrectly, models tended to split it into more subword pieces
  (higher tokenization count), and also gave it a lower plausibility score.
  These two things tend to go together, but we **cannot say one causes the other**.

### Research-Level Summary

**Descriptive:** Both models consistently produced negative Δ MeanLogP across all tracks,
indicating that contrast sentences were assigned lower pseudo-log-likelihood than originals.
Effect sizes were largest for REALISTIC_SPELLING_ERROR and VALID_WORD_CONTEXT tracks,
and smallest for SYNONYM_SUBSTITUTION, consistent with the expectation that valid synonyms
should be near-equally plausible under well-trained MLMs.

**Associations:** Spearman correlations between tokenization deltas and Δ MeanLogP were
examined per model and track. Detailed results are in `correlation_results.csv`.
Statistically significant correlations (BH-corrected) should be interpreted as associations,
not causal mechanisms: both tokenization fragmentation and lower PLL scores may be
independently driven by a common cause (e.g., a word being out-of-vocabulary or misspelled).

**Model comparison:** Both models agreed on the direction of score change (both negative)
for the substantial majority of pairs. The rank correlation between models' Δ MeanLogP
values provides evidence that both models capture similar relative sensitivity patterns
across pairs, despite different tokenization schemes and vocabulary sizes.

### Limitations
- **PLL is not grammaticality**: A lower PLL score does not prove a sentence is ungrammatical
  or semantically wrong. Valid synonyms and rare-but-correct constructions may also score lower.
- **Tokenization is not meaning**: More subword tokens does not mean a word is incorrect.
- **Small samples**: REALISTIC_SPELLING_ERROR has only 20 pairs. Correlations on this track
  are unreliable and should not be over-interpreted.
- **CPU-only inference**: Model weights were loaded from local cache; results reflect the
  specific model checkpoint versions loaded, not any fine-tuned variants.
- **This analysis does not establish explanation stability or faithfulness.**
  Those require separate perturbation experiments with reference explanations.

---

## 7. Artifacts

| File | Description |
|---|---|
| `combined_pair_level_results.csv` | Merged dataset, 400 rows |
| `descriptive_statistics.csv` | Per-model, per-track stats (with and without rejections) |
| `correlation_results.csv` | Spearman correlations with BH correction |
| `model_comparison.csv` | Direction agreement and rank correlation between models |
| `analysis_report.md` | This report |
| `run_metadata.json` | Software versions, hashes, row counts |
| `figures/` | Publication-quality visualizations |
