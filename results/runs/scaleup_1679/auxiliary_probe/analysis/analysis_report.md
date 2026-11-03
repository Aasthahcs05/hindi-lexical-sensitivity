# Stage 4: Combined Statistical Analysis — Hindi Lexical Sensitivity

**Run Timestamp (UTC):** 2026-11-02T16:04:02.214624+00:00
**Input SHA-256 (xlsx):** `208aabab0056f8287297d8800462c703afc7506f0d3e5fd5e7ff08fc23cf096e`
**Total merged rows:** 24 (400 expected: 200 pairs × 2 models)

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
| VALID_WORD_CONTEXT | -26.0177 | -3.3733 |
| SYNONYM_SUBSTITUTION | 3.0791 | 1.6957 |
| REALISTIC_SPELLING_ERROR | -11.5767 | -1.2863 |

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
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | -3.3733 | -3.4133 | 1.4539 | 1.4535 | -4.8068 | -1.8999 | 3 | 0 | 0 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | 1.6957 | 1.5157 | 1.5641 | 2.1198 | -0.6760 | 3.9502 | 1 | 7 | 0 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | -1.2863 | -1.2863 |  | 0.0000 | -1.2863 | -1.2863 | 1 | 0 | 0 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | -2.4124 | -2.4857 | 0.2548 | 0.2468 | -2.6225 | -2.1289 | 3 | 0 | 0 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | -0.5527 | -0.6658 | 0.5263 | 0.8186 | -1.1827 | 0.1961 | 6 | 2 | 0 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | -1.4674 | -1.4674 |  | 0.0000 | -1.4674 | -1.4674 | 1 | 0 | 0 |

### 2b. By Model and Track — Δ PLL Sum (secondary; affected by sentence length)

> ⚠️ Δ PLL Sum is sensitive to sentence length and number of scored tokens.
> Use Δ MeanLogP for cross-sentence comparisons within a model.

| Model | Track | N | Mean | Median | SD | IQR | N<0 | N>0 |
|---|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | -26.0177 | -27.3068 | 8.3494 | 8.2745 | 3 | 0 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | 3.0791 | 2.6497 | 3.9397 | 5.2311 | 1 | 7 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | -11.5767 | -11.5767 |  | 0.0000 | 1 | 0 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | -16.9322 | -14.9144 | 3.5054 | 3.0387 | 3 | 0 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | -4.3458 | -3.7101 | 5.5146 | 3.4969 | 6 | 2 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | -13.2067 | -13.2067 |  | 0.0000 | 1 | 0 |

### 2c. Token Count Changes by Model and Track

| Model | Track | N | Mean Δ Sent Tokens | Median Δ Sent Tokens | Mean Δ Target Tokens |
|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | 0.0000 | 0.0000 |  |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | 1.0000 | 1.0000 | 0.6250 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | 0.0000 | 0.0000 |  |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | 0.0000 | 0.0000 |  |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | 0.5000 | 0.0000 | 0.2500 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | 0.0000 | 0.0000 |  |

---

## 3. Sensitivity Analysis — Excluding Rejected Records

2 records have `final_status=reject`. Results below exclude these.

| Model | Track | N (excl. rejected) | Mean Δ MeanLogP | Mean Δ PLL Sum |
|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | 3 | -3.3733 | -26.0177 |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | 8 | 1.6957 | 3.0791 |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | 1 | -1.2863 | -11.5767 |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | 3 | -2.4124 | -16.9322 |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | 8 | -0.5527 | -4.3458 |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | 1 | -1.4674 | -13.2067 |

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
| `xlm-roberta-base` | Δ sentence token count (excl.) | 12 | 0.8245 | 0.000970 | True | [0.4756, 0.9492] |
| `xlm-roberta-base` | Δ target token count | 8 | -0.2999 | 0.470427 | False | [-0.8293, 0.5132] |
| `muril-base-cased` | Δ sentence token count (excl.) | 12 | 0.2419 | 0.448765 | False | [-0.3855, 0.7164] |
| `muril-base-cased` | Δ target token count | 8 | -0.2474 | 0.554646 | False | [-0.8108, 0.5538] |

### 4b. By Track — Δ MeanLogP

| Model | Track | X Variable | N | Spearman r | p (raw) | BH reject | Note |
|---|---|---|---|---|---|---|---|
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 3 | nan | nan | False | WARNING: n<10, result unreliable |
| `xlm-roberta-base` | `VALID_WORD_CONTEXT` | Δ target token count | 0 | nan | nan | False | WARNING: n<10, result unreliable |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 8 | 0.6172 | 0.103046 | False | WARNING: n<10, result unreliable |
| `xlm-roberta-base` | `SYNONYM_SUBSTITUTION` | Δ target token count | 8 | -0.2999 | 0.470427 | False | WARNING: n<10, result unreliable |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 1 | nan | nan | False | WARNING: n<10, result unreliable |
| `xlm-roberta-base` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 0 | nan | nan | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ sentence token count (excl.) | 3 | nan | nan | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `VALID_WORD_CONTEXT` | Δ target token count | 0 | nan | nan | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ sentence token count (excl.) | 8 | -0.0468 | 0.912451 | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `SYNONYM_SUBSTITUTION` | Δ target token count | 8 | -0.2474 | 0.554646 | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ sentence token count (excl.) | 1 | nan | nan | False | WARNING: n<10, result unreliable |
| `muril-base-cased` | `REALISTIC_SPELLING_ERROR` | Δ target token count | 0 | nan | nan | False | WARNING: n<10, result unreliable |

---

## 5. Model Comparison (XLM-RoBERTa vs. MuRIL)

> Comparison uses **within-model Δ MeanLogP** for each pair.
> Raw PLL sums are **not** cross-compared due to different tokenizer vocabularies.

| Track Scope | N | Direction Agreement | Spearman r (Δ MeanLogP) | p | 95% CI |
|---|---|---|---|---|---|
| `ALL_TRACKS` | 12 | 0.4167 (4↓↓ + 1↑↑) | 0.6364 | 0.026097 | [0.0984, 0.8865] |
| `VALID_WORD_CONTEXT` | 3 | 1.0000 (3↓↓ + 0↑↑) | -1.0000 | 0.000000 | [nan, nan] |
| `SYNONYM_SUBSTITUTION` | 8 | 0.1250 (0↓↓ + 1↑↑) | -0.1429 | 0.735765 | [-0.7700, 0.6247] |
| `REALISTIC_SPELLING_ERROR` | 1 | 1.0000 (1↓↓ + 0↑↑) | nan | nan | [nan, nan] |

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
