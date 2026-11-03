# Stage 5 — Hindi Lexical Sensitivity Explanation Pilot Summary

- **Model**: `google/muril-base-cased` (BertForMaskedLM)
- **Input Dataset**: `data\raw\hindi_lexical_sensitivity_cleaned.xlsx` (SHA-256: `f9a5af81e21624de47ead7feabba412149939c1eb9934f8fc2b8d452a232cd44`)
- **Timestamp (UTC)**: `2026-10-19T15:17:03.579206+00:00`
- **Prediction Target**: `scalar_mlm_target_token_logit_at_masked_position`
- **Explanation Methods**: Self-Attention (mean across heads at final layer), LayerIntegratedGradients (embedding layer)
- **Pilot Size**: 12 pairs (9 eligible, 3 ineligible)
- **IG Steps**: 20 | **Baseline**: `pad_with_target_masked`

## Evaluated Sentence Pairs

| Pair ID | Track | Contrast Label | Eligibility | Target (Orig / Cont) | Orig Logit | Cont Logit | Delta Logit |
|---|---|---|---|---|---|---|---|
| HC_0016 | VALID_WORD_CONTEXT | contextual_substitution_error | ineligible | तोड़ा / मोड़ा |  |  |  |
| HC_0001 | VALID_WORD_CONTEXT | contextual_substitution_error | eligible | और / ओर | 39.6236 | 31.8743 | -7.7493 |
| HC_0002 | VALID_WORD_CONTEXT | contextual_substitution_error | eligible | ओर / और | 36.3496 | 32.31 | -4.0396 |
| HC_0003 | VALID_WORD_CONTEXT | contextual_substitution_error | eligible | पढ़ी / पड़ी | 21.9879 | 12.6278 | -9.3601 |
| HC_0074 | SYNONYM_SUBSTITUTION | meaning_preserving_variant | ineligible | शांत / सुकूनभरी |  |  |  |
| HC_0004 | SYNONYM_SUBSTITUTION | meaning_preserving_variant | eligible | स्कूल / विद्यालय | 31.5516 | 29.6657 | -1.8859 |
| HC_0009 | SYNONYM_SUBSTITUTION | meaning_preserving_variant | eligible | मित्र / दोस्त | 39.377 | 39.0204 | -0.3566 |
| HC_0010 | SYNONYM_SUBSTITUTION | meaning_preserving_variant | eligible | सूरज / सूर्य | 53.5239 | 50.1694 | -3.3545 |
| HC_0005 | REALISTIC_SPELLING_ERROR | realistic_spelling_error | ineligible | पानी / पानि |  |  |  |
| HC_0077 | REALISTIC_SPELLING_ERROR | realistic_spelling_error | eligible | परीक्षा / परिक्षा | 45.8482 | 35.4353 | -10.4129 |
| HC_0078 | REALISTIC_SPELLING_ERROR | realistic_spelling_error | eligible | स्वास्थ्य / स्वास्थ | 31.2394 | 23.8002 | -7.4393 |
| HC_0118 | REALISTIC_SPELLING_ERROR | realistic_spelling_error | eligible | महत्वपूर्ण / महत्त्वपूर्ण | 44.9339 | 42.7017 | -2.2322 |

## Key Findings and Interpretive Guardrails
1. **Unified Target**: Both Attention and Integrated Gradients explain the exact same target score: the model's unnormalized logit for the designated target word token at the masked position.
2. **Special Token Exclusion**: `[CLS]`, `[SEP]`, and `[PAD]` are excluded from reported content attributions, preventing punctuation and boundary artifacts from dominating interpretation.
3. **Ineligibility Tracking**: Target words that segment into multiple subwords under spelling errors or morphological variations are explicitly recorded as compound targets, preventing ambiguous unaggregated scalar attribution.
4. **Convergence Diagnostics**: Completeness checks via `convergence_delta` confirm that the path integral accurately reconstructs the logit difference between full context and uninformative baseline.
