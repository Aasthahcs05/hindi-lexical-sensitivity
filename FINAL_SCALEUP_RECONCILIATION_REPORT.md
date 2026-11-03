# FINAL SCALE-UP RECONCILIATION AUDIT: CONSISTENCY, MEMBERSHIP, AND STATISTICAL VERIFICATION

**Project Title:** Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi  
**Phase:** Phase 2 — Final Reconciliation Audit Before Scale-Up Approval  
**Auditor:** Antigravity Research Assistant (Independent Verification Mode)  
**Date:** November 2026  
**Status:** Complete Forensic Reconciliation — Awaiting Human Approval (No models executed, no existing candidate files overwritten)

---

## Executive Summary

Before approving any dataset for the main scale-up experiment, this audit provides a final mathematical, structural, and linguistic reconciliation across all dataset counts, candidate memberships, flagged edge cases, and statistical power claims.

### Master Numbers at a Glance

```
Raw Expanded Dataset:                          2,000 Pairs (100.0%)
 ├── Candidate 1 (Strict Accepted Benchmark):  1,676 Pairs ( 83.8%)  <-- RECOMMENDED PRIMARY
 ├── Candidate 2 (Accepted with Templates):    1,954 Pairs ( 97.7%)  <-- SENSITIVITY CANDIDATE
 ├── Candidate 3 (Accepted without Templates): 1,676 Pairs ( 83.8%)  <-- IDENTICAL TO CANDIDATE 1
 ├── Candidate 4 (Multi-Word Agreement Group):    12 Pairs (  0.6%)  <-- AUXILIARY PROBE
 ├── Candidate 5 (Original Benchmark N=199):     199 Pairs ( 10.0%)  <-- HISTORICAL CONTINUITY
 └── Candidate 6 (Newly Added Accepted):       1,487 Pairs ( 74.4%)  <-- COHORT GENERALIZATION
```

---

## 1. Reconciliation of Original Benchmark Counts

The project documentation references five related but distinct sample counts regarding the original benchmark and the expanded dataset. This section provides the exact mathematical reconciliation.

### 1.1 The Five Benchmark Counts Explained

| Metric / Count | Value | Exact Definition & Provenance |
|---|---|---|
| **Original Raw Benchmark** | **200** | The total row count in `hindi_lexical_sensitivity_cleaned.xlsx` (and Rows 1–200 in the new dataset). Contains all original minimal pairs, including unadjudicated and rejected items. |
| **Historical Accepted Benchmark** | **199** | The historical working subset used in `RESEARCH_PROJECT_HANDOVER.md`. Filtered strictly on `final_status == 'accept'`, which dropped exactly 1 pair (`HC_0178`). Formatted as **Candidate 5**. |
| **Strictly Accepted Original Examples** | **189** | The subset of the original 200 pairs that survived the new, comprehensive quality audit. Excludes `HC_0178` plus **10 additional historical pairs** that fail strict minimal-pair, punctuation, or deduplication standards. |
| **Newly Added Accepted Examples** | **1,487** | The subset of newly authored pairs (Rows 201–2000) that passed strict acceptance criteria. Formatted as **Candidate 6**. |
| **Recommended Primary Dataset** | **1,676** | The sum of strictly accepted original pairs ($189$) and strictly accepted new pairs ($1,487$):  $$\text{Candidate 1} = 189 + 1,487 = \mathbf{1,676}$$ |

### 1.2 Mathematical Proof of the 10-Example Discrepancy (Candidate 5 + Candidate 6 = 1,686 vs. Candidate 1 = 1,676)
A key question is: *Why does Candidate 5 ($199$) plus Candidate 6 ($1,487$) equal $1,686$, which is $10$ more than Candidate 1 ($1,676$)?*

- **The Reason:** Candidate 5 represents the **historical** accepted benchmark ($N=199$), which was accepted in early pilot work before rigorous automated checks were applied.
- However, our strict quality audit revealed that **10 of those 199 historical pairs fail modern publication-grade criteria** (3 contain fatal technical flaws like Japanese punctuation or duplication, and 7 contain linguistic multi-word shifts, phrase targets, or question marks).
- In Candidate 1, those 10 flawed historical pairs were removed ($199 - 10 = 189$).
- Therefore:
  $$\text{Candidate 5 } (199) + \text{Candidate 6 } (1,487) = 1,686$$
  $$\text{Candidate 1 } = (199 - 10) + 1,487 = 189 + 1,487 = \mathbf{1,676}$$
  $$\text{Difference} = 1,686 - 1,676 = \mathbf{10 \text{ examples}}.$$

### 1.3 Complete Inventory of All 11 Original Benchmark Exclusions from Candidate 1

The table below lists every single original benchmark pair excluded from Candidate 1, along with its specific failure mode and classification:

| Pair ID | Raw Row | Track | Sentence (Original $\to$ Contrast) | Stated Target | Audit Status | Specific Reason for Exclusion from Candidate 1 |
|---|---|---|---|---|---|---|
| **`HC_0066`** | 67 | `VALID_WORD_CONTEXT` | `उसने चाबी ताले में लगाई।` $\to$ `उसने चाबी ताले में जगाई。` | `लगाई` $\to$ `जगाई` | **`REJECT`** | **Punctuation Corruption:** Sentence ends with fullwidth Japanese period `。` (U+3002) instead of Devanagari danda `।`. |
| **`HC_0069`** | 70 | `SYNONYM_SUBSTITUTION` | `उसने बहुत मेहनत की।` $\to$ `उसने बहुत परिश्रम किया।` | `मेहनत` $\to$ `परिश्रम` | **`REVIEW`** | **Multi-Word Gender Rewrite:** `मेहनत की` (fem) $\to$ `परिश्रम किया` (masc). Two words changed; violates single-word minimal pair. |
| **`HC_0091`** | 92 | `VALID_WORD_CONTEXT` | `मेज़ पर तीन गिलास रखे हैं।` $\to$ `मेज़ पर तीन गिलास रखा है।` | `रखे हैं` $\to$ `रखा है` | **`REVIEW`** | **Multi-Word Phrase Target:** Target is a 2-word copula phrase, ineligible for single-token logit attribution. |
| **`HC_0094`** | 95 | `VALID_WORD_CONTEXT` | `अचानक बिजली चली गई।` $\to$ `अचानक बिजली चला गया।` | `चली गई` $\to$ `चला गया` | **`REVIEW`** | **Multi-Word Phrase Target:** Target is a 2-word compound verb, ineligible for single-token logit attribution. |
| **`HC_0104`** | 105 | `VALID_WORD_CONTEXT` | `बगीचे में लाल गुलाब खिला है।` $\to$ `बगीचे में लाल गुलाब खिले हैं।` | `खिला है` $\to$ `खिले हैं` | **`REVIEW`** | **Multi-Word Phrase Target:** Target is a 2-word aspectual verb, ineligible for single-token logit attribution. |
| **`HC_0112`** | 113 | `SYNONYM_SUBSTITUTION` | `कृपया अपना परिचय दीजिए।` $\to$ `कृपया अपना परिचय प्रस्तुत कीजिए।` | `दीजिए` $\to$ `प्रस्तुत कीजिए` | **`REVIEW`** | **Multi-Word Phrase Expansion:** Target expands from 1 word to 2 words (`दीजिए` $\to$ `प्रस्तुत कीजिए`). |
| **`HC_0113`** | 114 | `SYNONYM_SUBSTITUTION` | `सैनिक ने साहस दिखाया।` $\to$ `सैनिक ने वीरता दिखाई।` | `साहस` $\to$ `वीरता` | **`REVIEW`** | **Multi-Word Gender Rewrite:** `साहस दिखाया` (masc) $\to$ `वीरता दिखाई` (fem). Two words changed. |
| **`HC_0163`** | 164 | `VALID_WORD_CONTEXT` | `सीमा ने कहानी पढ़ी।` $\to$ `सीमा ने कहानी पड़ी।` | `पढ़ी` $\to$ `पड़ी` | **`REJECT`** | **Exact Duplicate Pair:** Identical duplicate of Row 4 (`HC_0003`). |
| **`HC_0169`** | 170 | `VALID_WORD_CONTEXT` | `आप कहाँ जा रहे हैं?` $\to$ `आप कहाँ जा रहे है?` | `हैं` $\to$ `है` | **`REVIEW`** | **Interrogative Punctuation:** Sentence ends in ASCII `?` rather than standard Devanagari danda `।`. |
| **`HC_0178`** | 179 | `VALID_WORD_CONTEXT` | `पिताजी ने मुझे एक सलाह दी।` $\to$ `पिताजी ने मुझे एक सलाई दी।` | `सलाह` $\to$ `सलाई` | **`REJECT`** | **Annotation Rejection:** Formally rejected by both annotators and curator (`final_status = reject`). |
| **`HC_0193`** | 194 | `SYNONYM_SUBSTITUTION` | `उसने जवाब दिया।` $\to$ `उसने उत्तर दिया।` | `जवाब` $\to$ `उत्तर` | **`REJECT`** | **Exact Duplicate Pair:** Identical duplicate of Row 76 (`HC_0075`). |

$$\text{Original Raw Benchmark (200)} - 11 \text{ Exclusions} = \mathbf{189 \text{ Strictly Accepted Original Pairs in Candidate 1}}.$$

---

## 2. Verification of Candidate Dataset Membership

A byte-by-byte and ID-by-ID set comparison was conducted across all six candidate CSV files in `data/scaleup_candidates/`:

### 2.1 Candidate 1 vs. Candidate 3: Identity Verification
- **Candidate 1:** `scaleup_candidate_1_strict_accepted.csv` ($1,676$ rows)
- **Candidate 3:** `scaleup_candidate_3_accepted_excluding_templates.csv` ($1,676$ rows)
- **Finding:** **Candidate 1 and Candidate 3 are 100% IDENTICAL.**
  - Identical pair IDs in identical sequential order (`ids1 == ids3` is `True`).
  - Identical cell contents across all 18 columns for all 1,676 rows.
- **Why They Are Identical:** Candidate 1 was defined by the quality audit as the *strict accepted dataset*. Because the quality audit had already flagged the 278 template-heavy examples into `REVIEW_REQUIRED`, the strict accepted set *automatically* excluded templates. Therefore, Candidate 3 ("Accepted Excluding Templates") is redundant with Candidate 1.
- **Action:** Retain Candidate 1 as the canonical Primary Benchmark and document Candidate 3 as an alias.

### 2.2 Candidate 2 vs. Candidate 1: Set Difference Verification
- **Candidate 2:** `scaleup_candidate_2_accepted_with_templates.csv` ($1,954$ rows)
- **Candidate 1:** `scaleup_candidate_1_strict_accepted.csv` ($1,676$ rows)
- **Mathematical Difference:** $1,954 - 1,676 = \mathbf{278 \text{ rows}}$.
- **Set Difference Verification:**
  $$\text{IDs}(\text{Candidate 2}) \setminus \text{IDs}(\text{Candidate 1}) = \mathbf{\text{Exactly the 278 Template IDs}}.$$
  There are zero missing IDs, zero spurious additions, and zero unintended overlaps. Candidate 2 contains every single example in Candidate 1 plus the 278 template-heavy examples.

### 2.3 Candidate 5 vs. Candidate 6: Partition Verification
- **Candidate 5:** Original benchmark ($N=199$, IDs from `HC_0001` to `HC_0200`).
- **Candidate 6:** Newly added accepted pairs ($N=1,487$, IDs from `HC_0201` to `HC_2000`).
- **Intersection:** $\text{IDs}(\text{Candidate 5}) \cap \text{IDs}(\text{Candidate 6}) = \emptyset$ (Exactly 0 overlapping IDs).
- **Integrity:** The division between historical and newly authored cohorts is perfectly clean.

---

## 3. Forensic Reclassification of the 12 Flagged Cases

In Phase 2, 12 rows were grouped under the label `non_minimal_perturbation`. However, linguistic and programmatic analysis reveals that **they are NOT all gender-agreement changes**. 

They divide into **three fundamentally different linguistic and technical classes**:

| Pair ID | Track | Sentence (Original $\to$ Contrast) | Changed Tokens | True Linguistic / Technical Classification | Can It Be Retained in Main Experiment? |
|---|---|---|---|---|---|
| **`HC_1060`** | `VALID_WORD_CONTEXT` | `डॉक्टर ने मरीज की जाँच की।` $\to$ `...जाँच जी।` | `की` $\to$ `जी` | **Duplicate Word Collision:** Single-word change. Word `की` occurs twice; only the final light verb was replaced. | **YES for PLL**; Exclude from automated single-token attribution. |
| **`HC_1067`** | `VALID_WORD_CONTEXT` | `राहुल ने खिड़की बंद की।` $\to$ `...बंद सी।` | `की` $\to$ `सी` | **Substring Collision:** Single-word change. `की` occurs inside `खिड़की`; only the final verb `की` was replaced. | **YES for PLL & Attribution** (clean word token). |
| **`HC_1081`** | `VALID_WORD_CONTEXT` | `दर्जी ने कपड़े की सिलाई की।` $\to$ `...सिलाई पी।` | `की` $\to$ `पी` | **Duplicate Word Collision:** Single-word change. `की` occurs twice; only the final verb was replaced. | **YES for PLL**; Exclude from automated single-token attribution. |
| **`HC_1190`** | `REALISTIC_SPELLING_ERROR` | `विद्यार्थी ने अपने उत्तर में उत्तर शब्द लिखा।` $\to$ `...उतर शब्द...` | `उत्तर` $\to$ `उतर` | **Duplicate Word Collision:** Single-word change. `उत्तर` occurs twice; only the second occurrence was misspelled. | **YES for PLL**; Exclude from automated single-token attribution. |
| **`HC_0069`** | `SYNONYM_SUBSTITUTION` | `उसने बहुत मेहनत की।` $\to$ `उसने बहुत परिश्रम किया।` | `मेहनत की` $\to$ `परिश्रम किया` | **Gender Concord Rewrite:** `मेहनत` (fem) takes `की`; `परिश्रम` (masc) requires `किया`. 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_0113`** | `SYNONYM_SUBSTITUTION` | `सैनिक ने साहस दिखाया।` $\to$ `सैनिक ने वीरता दिखाई।` | `साहस दिखाया` $\to$ `वीरता दिखाई` | **Gender Concord Rewrite:** `साहस` (masc) takes `दिखाया`; `वीरता` (fem) requires `दिखाई`. 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_1863`** | `SYNONYM_SUBSTITUTION` | `अपनी आँख खोलो।` $\to$ `अपने नेत्र खोलो।` | `अपनी आँख` $\to$ `अपने नेत्र` | **Number/Gender Concord:** `अपनी आँख` (fem sg) $\to$ `अपने नेत्र` (masc pl). 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_1874`** | `SYNONYM_SUBSTITUTION` | `यात्रा लंबी है।` $\to$ `सफर लंबा है।` | `यात्रा लंबी` $\to$ `सफर लंबा` | **Gender Concord Rewrite:** `यात्रा` (fem) takes `लंबी`; `सफर` (masc) requires `लंबा`. 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_1878`** | `SYNONYM_SUBSTITUTION` | `दुनिया बड़ी है।` $\to$ `संसार बड़ा है।` | `दुनिया बड़ी` $\to$ `संसार बड़ा` | **Gender Concord Rewrite:** `दुनिया` (fem) takes `बड़ी`; `संसार` (masc) requires `बड़ा`. 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_1943`** | `SYNONYM_SUBSTITUTION` | `युद्ध बुरा है।` $\to$ `लड़ाई बुरी है।` | `युद्ध बुरा` $\to$ `लड़ाई बुरी` | **Gender Concord Rewrite:** `युद्ध` (masc) takes `बुरा`; `लड़ाई` (fem) requires `बुरी`. 2 words changed. | **NO (Separate Subgroup):** Violates single-word minimal pair. |
| **`HC_1919`** | `SYNONYM_SUBSTITUTION` | `दूर जाओ।` $\to$ `फासले पर जाओ।` | `दूर` $\to$ `फासले पर` | **Syntactic Frame / Postposition Insertion:** Adverb `दूर` replaced by noun `फासले` + postposition `पर`. | **NO (Separate Subgroup):** Sentence length changed (+1 word). |
| **`HC_1934`** | `SYNONYM_SUBSTITUTION` | `भोजन करो।` $\to$ `खाना खाओ।` | `भोजन करो` $\to$ `खाना खाओ` | **Collocation / Light-Verb Shift:** Collocation with `भोजन` is `करना`, while collocation with `खाना` is `खाना`. | **NO (Separate Subgroup):** 2 words changed. |

### Summary of Classification
- **Genuine Gender / Number Agreement Rewrites:** Exactly **6 pairs** (`HC_0069`, `HC_0113`, `HC_1863`, `HC_1874`, `HC_1878`, `HC_1943`).
- **Syntactic Frame & Collocation Shifts:** Exactly **2 pairs** (`HC_1919`, `HC_1934`).
- **Single-Word Changes with Substring / Duplicate Ambiguity:** Exactly **4 pairs** (`HC_1060`, `HC_1067`, `HC_1081`, `HC_1190`).
- **Recommendation:** Keep all 8 multi-word rewrites in **Candidate 4** as an auxiliary linguistic probe. Do not include them in the primary minimal-pair candidate.

---

## 4. Reconciliation of Spelling-Track Real-Word Ambiguities

Six pairs in `REALISTIC_SPELLING_ERROR` involve spelling variations that form existing words in Hindi dictionaries. The table below details their contextual semantics and justifies why **three are recommended for reclassification while three must remain in the spelling track**:

| Pair ID | Original Sentence | Contrast Sentence | Target Word Change | Grammaticality of Contrast Sentence | Contextual Meaning & Semantic Analysis | Recommended Adjudication Decision |
|---|---|---|---|---|---|---|
| **`HC_1552`** | `उसने नया गृह प्रवेश किया।` | `उसने नया ग्रह प्रवेश किया।` | `गृह` (home) $\to$ `ग्रह` (planet) | **Grammatical** | `गृह प्रवेश` (housewarming ceremony) is replaced by `ग्रह प्रवेश` (planetary entry). The contrast sentence is grammatically valid but contextually anomalous. | **RECLASSIFY to `VALID_WORD_CONTEXT`** |
| **`HC_1619`** | `पृथ्वी एक ग्रह है।` | `पृथ्वी एक गृह है।` | `ग्रह` (planet) $\to$ `गृह` (home) | **Grammatical** | "Earth is a planet" is replaced by "Earth is a home". Completely grammatical Hindi. Identical pair is already categorized as `VALID_WORD_CONTEXT` in Row 1974 (`HC_1973`). | **RECLASSIFY to `VALID_WORD_CONTEXT`** |
| **`HC_1689`** | `आज का दिन अच्छा है।` | `आज का दीन अच्छा है।` | `दिन` (day) $\to$ `दीन` (poor / humble) | **Grammatical** | `दीन` is an adjective/noun. `आज का दीन अच्छा है` is grammatically valid Hindi ("Today's poor person is good"), testing contextual plausibility. | **RECLASSIFY to `VALID_WORD_CONTEXT`** |
| **`HC_1725`** | `हमें हार नहीं माननी चाहिए।` | `हमें हर नहीं माननी चाहिए।` | `हार` (defeat) $\to$ `हर` (every) | **UNGRAMMATICAL** | `हर` is a determiner ("every"). In Hindi syntax, `हर` cannot stand alone as a direct object before `नहीं माननी चाहिए`. The sentence is **syntactically broken**. | **RETAIN in `REALISTIC_SPELLING_ERROR`** |
| **`HC_1730`** | `पिता जी काम पर गए हैं।` | `पीता जी काम पर गए हैं।` | `पिता` (father) $\to$ `पीता` (drinks) | **UNGRAMMATICAL** | `पीता` is an imperfective verb participle. Placing a verb in subject position before honorific `जी` yields a **syntactic crash** (`*Drinks ji has gone to work`). | **RETAIN in `REALISTIC_SPELLING_ERROR`** |
| **`HC_1747`** | `अपना लक्ष्य निर्धारित करें।` | `अपना लक्ष निर्धारित करें।` | `लक्ष्य` (goal) $\to$ `लक्ष` (100,000 / lakh) | **UNGRAMMATICAL / ARCHAIC** | In modern Hindi, `लक्ष` is only used as a numeral (100,000) or in archaic Sanskrit. In this sentence, it represents a pure orthographic typo (omitting conjunct `्य`). | **RETAIN in `REALISTIC_SPELLING_ERROR`** |

### Strategic Summary
- **Why Reclassify `HC_1552`, `HC_1619`, `HC_1689`:** Because their contrast sentences are **grammatically valid**, an MLM processes them as a competition between two real words within a context frame—the precise operational definition of `VALID_WORD_CONTEXT`.
- **Why Retain `HC_1725`, `HC_1730`, `HC_1747`:** Because their contrast sentences are **syntactically ungrammatical**, the model experiences a syntax failure. They function as authentic spelling noise.
- *Status:* No categories have been modified in the candidate files. Reclassification awaits your formal sign-off.

---

## 5. Verification and Correction of Statistical Power Claims

The previous report asserted:
> *"At $N \ge 200$, statistical power to detect small-to-moderate correlations ($r_s \ge 0.20$) at $\alpha = 0.01$ exceeds 95%."*  
> *"Projected strict single-subword spelling pairs: MuRIL $\approx 300$, XLM-RoBERTa $\approx 200$."*

**This section performs the exact statistical power calculations and qualifies the tokenizer assumptions.**

### 5.1 Exact Statistical Power Calculations (Fisher's $z$-Transformation)
Under Fisher's $z$-transformation, for sample size $N$ and population correlation $r$, the test statistic is $Z = \text{arctanh}(r) \sqrt{N - 3}$. Statistical power ($1 - \beta$) for a two-tailed test at significance levels $\alpha = 0.05$ and $\alpha = 0.01$ is computed below:

| Sample Size ($N$) | Effect Size ($r=0.15$) $\alpha=0.05$ | Effect Size ($r=0.20$) $\alpha=0.05$ | Effect Size ($r=0.25$) $\alpha=0.05$ | Effect Size ($r=0.30$) $\alpha=0.05$ | Effect Size ($r=0.20$) $\alpha=0.01$ | Effect Size ($r=0.30$) $\alpha=0.01$ | Effect Size ($r=0.40$) $\alpha=0.01$ |
|---|---|---|---|---|---|---|---|
| **$N = 4$ (Original XLM-R Strict)** | $5.3\%$ | $5.5\%$ | $5.8\%$ | $6.1\%$ | $1.2\%$ | $1.4\%$ | $1.7\%$ |
| **$N = 6$ (Original MuRIL Strict)** | $5.8\%$ | $6.4\%$ | $7.3\%$ | $8.4\%$ | $1.5\%$ | $2.2\%$ | $3.3\%$ |
| **$N = 20$ (Original Pooled Spelling)** | $9.6\%$ | $13.3\%$ | $18.4\%$ | $24.8\%$ | $4.1\%$ | $9.7\%$ | $20.4\%$ |
| **$N = 50$** | $17.9\%$ | $28.5\%$ | $41.7\%$ | $56.4\%$ | $11.8\%$ | $32.5\%$ | $62.9\%$ |
| **$N = 100$** | $31.9\%$ | $51.5\%$ | $71.1\%$ | $86.2\%$ | $28.1\%$ | $68.2\%$ | $94.5\%$ |
| **$N = 150$** | $44.9\%$ | $69.1\%$ | $87.2\%$ | $96.3\%$ | $45.3\%$ | $88.0\%$ | $99.5\%$ |
| **$N = 200$** | **$56.4\%$** | **$81.2\%$** | **$94.8\%$** | **$99.1\%$** | **$60.6\%$** | **$96.2\%$** | **$100.0\%$** |
| **$N = 300$** | **$74.0\%$** | **$93.7\%$** | **$99.3\%$** | **$100.0\%$** | **$82.1\%$** | **$99.7\%$** | **$100.0\%$** |
| **$N = 500$** | **$92.1\%$** | **$99.5\%$** | **$100.0\%$** | **$100.0\%$** | **$97.4\%$** | **$100.0\%$** | **$100.0\%$** |
| **$N = 1,005$ (Full Accepted Spelling)** | **$99.8\%$** | **$100.0\%$** | **$100.0\%$** | **$100.0\%$** | **$100.0\%$** | **$100.0\%$** | **$100.0\%$** |

### 5.2 Forensic Qualification of the Claims

1. **Correction of the Power Claim:**
   - The prior statement that *"power exceeds $95\%$ for $r \ge 0.20$ at $\alpha = 0.01$ when $N \ge 200$"* was **mathematically inaccurate**.
   - As shown in the table:
     - At $N = 200$ and $r = 0.20$, power at $\alpha = 0.01$ is **$60.6\%$** (and $81.2\%$ at $\alpha = 0.05$).
     - To achieve **$>95\%$ power** at $N = 200$, the true correlation must be **$r \ge 0.26$ at $\alpha = 0.05$**, or **$r \ge 0.30$ at $\alpha = 0.01$** ($96.2\%$).
     - At the full sample size of the accepted spelling track ($N = 1,005$), statistical power is **$99.8\%$ even for tiny effects ($r = 0.15$)** at $\alpha = 0.05$.
2. **Qualification of the Strict Single-Subword Sample Size Projection:**
   - The projection of $\approx 200–300$ strict single-subword pairs was derived by linearly applying pilot retention rates ($30\%$ in MuRIL $\implies 301$ pairs; $20\%$ in XLM-RoBERTa $\implies 201$ pairs) to the 1,005 accepted spelling pairs.
   - **Methodological Caveat:** Because word length in the new dataset is slightly higher ($5.84$ words vs. $4.97$ words in the pilot), and Devanagari subword tokenization depends on specific character n-gram frequencies in pretraining corpora, the actual retention rate may deviate.
   - **Correct Scientific Framing:** The strict single-subword sample size should be described as an *empirically projected subset of substantial scale ($N \approx 150–300$ pairs)*, rather than an exact known count, until full tokenizer inference is executed. Even at $N = 150$, power to detect $r \ge 0.30$ is **$96.3\%$**, which remains vastly superior to the pilot's $N=4$ ($6.1\%$).

---

## 6. Actionable Recommendations for Approval

### Primary Recommendation: Candidate 1 ($N = 1,676$)
We recommend adopting **Candidate 1 (`scaleup_candidate_1_strict_accepted.csv`)** as the primary dataset for scale-up experimentation.

- **Why Candidate 1:**
  1. **Strict Quality:** 100% compliant with single-word minimal-pair criteria; eliminates punctuation corruptions and duplicate pairs.
  2. **Syntactic Diversity:** Completely free from repetitive template carrier frames.
  3. **High Statistical Power:** Provides **1,005 clean spelling pairs** ($50\times$ larger than the original benchmark), providing $>99\%$ power for main spelling plausibility tests and $>90\%$ power for subword-stratified correlation analyses.

### Secondary Recommendation: Candidate 2 ($N = 1,954$) for Sensitivity
We recommend running **Candidate 2 (`scaleup_candidate_2_accepted_with_templates.csv`)** as a secondary sensitivity analysis to verify that findings obtained on Candidate 1 hold across template-heavy sentences.

### Summary of Decisions Awaiting Your Approval

Before we run model inference, please confirm:
1. **Approval of Candidate 1 ($N = 1,676$)** as the primary scale-up benchmark.
2. **Approval of Candidate 2 ($N = 1,954$)** as the secondary sensitivity check.
3. **Approval of the Reclassification of `HC_1552`, `HC_1619`, and `HC_1689`** from `REALISTIC_SPELLING_ERROR` to `VALID_WORD_CONTEXT`.
4. **Approval of Candidate 4 ($N = 12$)** as a separate multi-word agreement auxiliary probe.

*All models remain unexecuted. Standing by for your instructions.*
