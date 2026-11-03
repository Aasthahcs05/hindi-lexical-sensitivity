# Hindi Masked Language Modeling: Masking Demonstration & Pipeline Reference

This document illustrates exactly **where, why, and how masking is performed** across the project's models and evaluation pipelines using real examples from the dataset with `google/muril-base-cased` (Mask Token: `[MASK]`, ID: `103`).

---

## 1. Summary of Masking Locations in the Codebase

| Pipeline / Task | Source File | Function / Section | Masking Objective |
| :--- | :--- | :--- | :--- |
| **Pseudo-Log-Likelihood (PLL) Scoring** | [`src/models/pll_scoring.py`](file:///d:/hindi-lexical-sensitivity/src/models/pll_scoring.py#L160-L175) | `compute_sentence_pll()` | Iteratively mask each content token one-by-one to compute the sequence probability $\sum_i \log P(w_i \mid W_{\setminus i})$. |
| **Target Explanation & Attribution** | [`src/explanations/hindi_explanations.py`](file:///d:/hindi-lexical-sensitivity/src/explanations/hindi_explanations.py#L223-L226) | `prepare_masked_target_input()` | Mask only the target Hindi word so the model generates logits, attention query weights, and gradients for that position. |
| **Integrated Gradients Baseline** | [`src/explanations/hindi_explanations.py`](file:///d:/hindi-lexical-sensitivity/src/explanations/hindi_explanations.py#L321) | `compute_integrated_gradients()` | Create an uninformative baseline reference where the target is `[MASK]` and context tokens are `[PAD]`. |
| **Faithfulness & Erasure Tests** | [`src/analysis/hindi_faithfulness.py`](file:///d:/hindi-lexical-sensitivity/src/analysis/hindi_faithfulness.py#L427-L474) | `evaluate_faithfulness()` | Mask top-k or non-top-k context tokens to measure model prediction degradation (Comprehensiveness & Sufficiency). |
| **Counterfactual Stability** | [`src/analysis/explanation_stability.py`](file:///d:/hindi-lexical-sensitivity/src/analysis/explanation_stability.py#L515-L520) | `compute_pair_stability()` | Mask target tokens across paired minimal-contrast sentences to measure representation sensitivity. |

---

## 2. Concrete Example 1: Target Word Masking (Attributions & Explanations)

Taken from pair **`HC_0001`** (`VALID_WORD_CONTEXT` track):
* **Original sentence:** `राम और सीता साथ हैं।` (Target: `और`, Token ID: `1123`)
* **Contrast sentence:** `राम ओर सीता साथ हैं।` (Target: `ओर`, Token ID: `2838`)

### Step-by-Step Masking Process
```
Original Tokens:  [CLS]  राम    और    सीता   साथ   हैं    ।   [SEP]
Token IDs:        [101,  2729,  1123, 10243, 2372, 1058, 126, 102]
                                 ▲ Target pos = 2

Masked Sequence:  [CLS]  राम   [MASK]  सीता   साथ   हैं    ।   [SEP]
Masked IDs:       [101,  2729,   103, 10243, 2372, 1058, 126, 102]
```

### Contrast Sentence Masking
```
Contrast Tokens:  [CLS]  राम    ओर    सीता   साथ   हैं    ।   [SEP]
Token IDs:        [101,  2729,  2838, 10243, 2372, 1058, 126, 102]
                                 ▲ Target pos = 2

Masked Sequence:  [CLS]  राम   [MASK]  सीता   साथ   हैं    ।   [SEP]
Masked IDs:       [101,  2729,   103, 10243, 2372, 1058, 126, 102]
```

> **Notice:** Both sentences produce identical masked input representations at the input layer. The model's logits at the `[MASK]` position reveal how much the context expects `और` (logit = 39.62) versus `ओर` (logit = 31.87), giving a $\Delta\text{logit} = -7.75$.

---

## 3. Concrete Example 2: Pseudo-Log-Likelihood (PLL) Scoring Masking

For full sentence probability estimation (`compute_sentence_pll`), every token except special tokens (`[CLS]`, `[SEP]`, `[PAD]`) is masked in individual forward passes:

Sentence: `राम और सीता साथ हैं।`

| Step | Masked Position | Token Evaluated | Model Input Sequence with Mask | Target ID | Logit / Log-Prob |
| :---: | :---: | :---: | :--- | :---: | :---: |
| **1** | Pos 1 | `राम` | `[CLS]` **`[MASK]`** `और सीता साथ हैं । [SEP]` | 2729 | $\log P(\text{राम} \mid \text{context})$ |
| **2** | Pos 2 | `और` | `[CLS] राम` **`[MASK]`** `सीता साथ हैं । [SEP]` | 1123 | $\log P(\text{और} \mid \text{context})$ |
| **3** | Pos 3 | `सीता` | `[CLS] राम और` **`[MASK]`** `साथ हैं । [SEP]` | 10243 | $\log P(\text{सीता} \mid \text{context})$ |
| **4** | Pos 4 | `साथ` | `[CLS] राम और सीता` **`[MASK]`** `हैं । [SEP]` | 2372 | $\log P(\text{साथ} \mid \text{context})$ |
| **5** | Pos 5 | `हैं` | `[CLS] राम और सीता साथ` **`[MASK]`** `। [SEP]` | 1058 | $\log P(\text{हैं} \mid \text{context})$ |
| **6** | Pos 6 | `।` | `[CLS] राम और सीता साथ हैं` **`[MASK]`** `[SEP]` | 126 | $\log P(\text{।} \mid \text{context})$ |

$$\text{PLL}(\text{Sentence}) = \sum_{i=1}^{6} \log P(w_i \mid W_{\setminus i})$$

---

## 4. Concrete Example 3: Faithfulness & Perturbation Masking

In [`src/analysis/hindi_faithfulness.py`](file:///d:/hindi-lexical-sensitivity/src/analysis/hindi_faithfulness.py), masking is used to evaluate whether explanation attributions are faithful to the model's actual reasoning:

### Comprehensiveness (Erasing Most Important Tokens)
If attribution ranks `सीता` (Pos 3) as the most important context token for predicting `और`:
```
Original Context:      [CLS]  राम    [MASK]   सीता   साथ   हैं   ।  [SEP]
Intervened Sequence:   [CLS]  राम    [MASK]  [MASK]  साथ   हैं   ।  [SEP]
                                                ▲ erased
```
*Evaluates:* How much does the target prediction drop when key explanatory evidence is masked out?

### Sufficiency (Retaining Only Important Tokens)
Retaining only `सीता` while masking out all other context words:
```
Intervened Sequence:   [CLS] [MASK]  [MASK]   सीता  [MASK] [MASK] ।  [SEP]
```
*Evaluates:* Can the model still predict `और` using only the top attributed token?

---

## 5. Tensor Code Implementation Snippet

```python
# Direct extraction from src/explanations/hindi_explanations.py
mask_token_id = getattr(tokenizer, "mask_token_id", 103)
masked_input_ids = input_ids.clone()
masked_input_ids[0, target_pos] = mask_token_id

outputs = model(input_ids=masked_input_ids, attention_mask=attention_mask)
logits = outputs.logits  # shape: (1, seq_len, vocab_size)
target_logit = logits[0, target_pos, target_token_id].item()
```
