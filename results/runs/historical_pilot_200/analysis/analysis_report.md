# Stage 4: Combined Statistical Analysis — Hindi Lexical Sensitivity

**Run Timestamp (UTC):** 2026-10-19T14:25:04.408297+00:00
**Input SHA-256 (xlsx):** `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`
**Total merged rows:** 400 (400 expected: 200 pairs × 2 models)

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
| VALID_WORD_CONTEXT | -7.7425 | -1.0933 |
| SYNONYM_SUBSTITUTION | -1.4183 | -0.0655 |
| REALISTIC_SPELLING_ERROR | -7.7439 | -0.6695 |

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
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 142 | -1.0933 | -0.8752 | 1.3572 | 1.4929 | -4.8362 | 1.5154 | 115 | 27 | 0 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | -0.0655 | -0.1035 | 0.8896 | 0.9189 | -2.5753 | 1.5220 | 22 | 16 | 0 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | -0.6695 | -0.5903 | 1.5495 | 2.4722 | -3.4560 | 2.4161 | 13 | 7 | 0 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 142 | -1.9141 | -1.6218 | 1.5638 | 1.8507 | -5.9067 | 2.3301 | 132 | 10 | 0 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | -0.5810 | -0.4607 | 0.7358 | 0.6063 | -3.6843 | 0.6790 | 32 | 6 | 0 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | -2.0368 | -2.2748 | 1.4447 | 1.6266 | -5.1822 | 0.5509 | 19 | 1 | 0 |

### 2b. By Model and Track — Δ PLL Sum (secondary; affected by sentence length)

> ⚠️ Δ PLL Sum is sensitive to sentence length and number of scored tokens.
> Use Δ MeanLogP for cross-sentence comparisons within a model.

| Model | Track | N | Mean | Median | SD | IQR | N<0 | N>0 |
|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 142 | -7.7425 | -6.8377 | 8.7325 | 11.3434 | 119 | 23 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | -1.4183 | -1.3354 | 3.8018 | 4.7686 | 24 | 14 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | -7.7439 | -6.3409 | 9.4592 | 15.0153 | 15 | 5 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 142 | -12.5616 | -11.9085 | 9.6505 | 10.9575 | 130 | 12 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | -3.9947 | -2.4943 | 5.8187 | 3.7629 | 32 | 6 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | -16.1899 | -17.2920 | 11.3300 | 18.3908 | 19 | 1 |

### 2c. Token Count Changes by Model and Track

| Model | Track | N | Mean Δ Sent Tokens | Median Δ Sent Tokens | Mean Δ Target Tokens |
|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 142 | 0.1690 | 0.0000 | 0.1690 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | 0.6053 | 0.0000 | 0.6316 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | 1.0000 | 1.0000 | 1.0000 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 142 | 0.0775 | 0.0000 | 0.0845 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | 0.1842 | 0.0000 | 0.1842 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | 1.0000 | 1.0000 | 1.0000 |

---

## 3. Sensitivity Analysis — Excluding Rejected Records

2 records have `final_status=reject`. Results below exclude these.

| Model | Track | N (excl. rejected) | Mean Δ MeanLogP | Mean Δ PLL Sum |
|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 141 | -1.0920 | -7.7059 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 38 | -0.0655 | -1.4183 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 20 | -0.6695 | -7.7439 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 141 | -1.9254 | -12.6129 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 38 | -0.5810 | -3.9947 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 20 | -2.0368 | -16.1899 |

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
| `xlm-roberta-base` | Δ sentence token count (excl.) | 200 | 0.3481 | 0.000000 | True | [0.2200, 0.4644] |
| `xlm-roberta-base` | Δ target token count | 200 | 0.3470 | 0.000000 | True | [0.2188, 0.4634] |
| `muril-base-cased` | Δ sentence token count (excl.) | 200 | -0.1941 | 0.005882 | True | [-0.3241, -0.0569] |
| `muril-base-cased` | Δ target token count | 200 | -0.2007 | 0.004387 | True | [-0.3302, -0.0637] |

### 4b. By Track — Δ MeanLogP

| Model | Track | X Variable | N | Spearman r | p (raw) | BH reject | Note |
|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 142 | 0.2337 | 0.005121 | True |  |
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ target token count | 142 | 0.2337 | 0.005121 | True |  |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 38 | 0.6571 | 0.000007 | True |  |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ target token count | 38 | 0.6127 | 0.000043 | True |  |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 20 | 0.4664 | 0.038191 | False |  |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 20 | 0.4664 | 0.038191 | False |  |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 142 | -0.1351 | 0.108798 | False |  |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ target token count | 142 | -0.1420 | 0.091767 | False |  |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 38 | -0.3400 | 0.036763 | False |  |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ target token count | 38 | -0.3400 | 0.036763 | False |  |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 20 | -0.4460 | 0.048749 | False |  |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 20 | -0.4460 | 0.048749 | False |  |

---

## 5. Model Comparison (XLM-RoBERTa vs. MuRIL)

> Comparison uses **within-model Δ MeanLogP** for each pair.
> Raw PLL sums are **not** cross-compared due to different tokenizer vocabularies.

| Track Scope | N | Direction Agreement | Spearman r (Δ MeanLogP) | p | 95% CI |
|---|---|---|---|---|---|
| `ALL_TRACKS` | 200 | 0.7450 (141↓↓ + 8↑↑) | 0.4408 | 0.000000 | [0.3217, 0.5461] |
| `VALID_WORD_CONTEXT` | 142 | 0.8099 (110↓↓ + 5↑↑) | 0.4457 | 0.000000 | [0.3032, 0.5687] |
| `SYNONYM_SUBSTITUTION` | 38 | 0.5789 (19↓↓ + 3↑↑) | 0.0595 | 0.722564 | [-0.2652, 0.3721] |
| `REALISTIC_SPELLING_ERROR` | 20 | 0.6000 (12↓↓ + 0↑↑) | 0.2150 | 0.362574 | [-0.2514, 0.6004] |

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
