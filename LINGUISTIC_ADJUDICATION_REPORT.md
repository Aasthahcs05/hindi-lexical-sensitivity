# LINGUISTIC ADJUDICATION REPORT: EDGE CASES AND SUBGROUP ANALYSIS

**Project Title:** Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi  
**Phase:** Phase 2 — Final Dataset Adjudication and Scale-Up Readiness  
**Auditor:** Antigravity Research Assistant (Independent Verification Mode)  
**Date:** November 2026  

---

## Executive Summary

This report delivers a forensic linguistic adjudication of all edge cases flagged during the quality audit of the 2,000-example Hindi dataset. Specifically, it resolves:
1. **The 12 Non-Minimal Cases:** Disentangling true multi-word grammatical gender concord shifts from automated string replacement collisions.
2. **The 6 Real-Word Spelling Cases:** Analyzing whether typos forming valid dictionary words belong in the spelling track or the contextual substitution track.
3. **The 4 Multi-Word Verb Phrase Targets:** Evaluating multi-token targets against MLM single-token logit scoring requirements.
4. **The 7 Interrogative Sentences:** Assessing punctuation consistency (`?` vs. `।`).

---

## Part 1: The 12 Non-Minimal / Multi-Word Cases

A primary assumption of minimal-pair perturbation benchmarks is that **exactly one lexical item changes between the original and contrast sentences**, preserving all surrounding context tokens.

The audit flagged 12 cases where replacing `target_original` with `target_contrast` did not yield `contrast_sentence`. Forensic analysis reveals that these divide into **two distinct categories**:

### 1.1 Category A: 4 Substring Collisions & Duplicate Word Occurrences (Actually Single-Word Replacements)
In these 4 cases, **only one word was actually changed**. They were flagged purely due to automated string-matching ambiguities:

| Pair ID | Track | Original Sentence | Contrast Sentence | Target Change | Root Cause / Forensic Explanation |
|---|---|---|---|---|---|
| **`HC_1060`** | `VALID_WORD_CONTEXT` | `डॉक्टर ने मरीज की जाँच की।` | `डॉक्टर ने मरीज की जाँच जी।` | `की` $\to$ `जी` | Word `की` occurs twice (genitive postposition and light verb). Only the sentence-final verb was replaced. |
| **`HC_1067`** | `VALID_WORD_CONTEXT` | `राहुल ने खिड़की बंद की।` | `राहुल ने खिड़की बंद सी।` | `की` $\to$ `सी` | `की` occurs as a substring inside `खिड़की`. Only the sentence-final verb `की` was replaced. |
| **`HC_1081`** | `VALID_WORD_CONTEXT` | `दर्जी ने कपड़े की सिलाई की।` | `दर्जी ने कपड़े की सिलाई पी।` | `की` $\to$ `पी` | `की` occurs twice (`कपड़े की`, `सिलाई की`). Only the final verb `की` was replaced. |
| **`HC_1190`** | `REALISTIC_SPELLING_ERROR` | `विद्यार्थी ने अपने उत्तर में उत्तर शब्द लिखा।` | `विद्यार्थी ने अपने उत्तर में उतर शब्द लिखा।` | `उत्तर` $\to$ `उतर` | `उत्तर` occurs twice. Only the second occurrence was replaced with the misspelled `उतर`. |

- **Adjudication Verdict:** These 4 pairs are **genuine single-word perturbations**. However, because the target token occurs twice in the sentence, automated character-offset alignment (`align_target_word`) in MLM attribution scripts marks them as `status: "ambiguous"`. They are retained in `REVIEW` to prevent pipeline crashes during gradient attribution.

### 1.2 Category B: 8 True Multi-Word Rewrites (Gender Agreement & Collocation Shifts)
In these 8 pairs within `SYNONYM_SUBSTITUTION`, substituting a synonym required altering adjacent words to preserve grammatical correctness:

| Pair ID | Original Sentence | Contrast Sentence | Changed Tokens | Linguistic Mechanism / Grammatical Justification |
|---|---|---|---|---|
| **`HC_0069`** | `उसने बहुत मेहनत की।` | `उसने बहुत परिश्रम किया।` | `मेहनत की` $\to$ `परिश्रम किया` | **Gender Concord:** `मेहनत` is feminine (taking `की`), whereas `परिश्रम` is masculine (requiring `किया`). |
| **`HC_0113`** | `सैनिक ने साहस दिखाया।` | `सैनिक ने वीरता दिखाई।` | `साहस दिखाया` $\to$ `वीरता दिखाई` | **Gender Concord:** `साहस` is masculine (taking `दिखाया`), whereas `वीरता` is feminine (requiring `दिखाई`). |
| **`HC_1863`** | `अपनी आँख खोलो।` | `अपने नेत्र खोलो।` | `अपनी आँख` $\to$ `अपने नेत्र` | **Number/Gender Concord:** `आँख` is feminine singular (taking `अपनी`), whereas `नेत्र` is masculine plural (requiring `अपने`). |
| **`HC_1874`** | `यात्रा लंबी है।` | `सफर लंबा है।` | `यात्रा लंबी` $\to$ `सफर लंबा` | **Gender Concord:** `यात्रा` is feminine (taking adjective `लंबी`), whereas `सफर` is masculine (requiring `लंबा`). |
| **`HC_1878`** | `दुनिया बड़ी है।` | `संसार बड़ा है।` | `दुनिया बड़ी` $\to$ `संसार बड़ा` | **Gender Concord:** `दुनिया` is feminine (taking `बड़ी`), whereas `संसार` is masculine (requiring `बड़ा`). |
| **`HC_1919`** | `दूर जाओ।` | `फासले पर जाओ।` | `दूर` $\to$ `फासले पर` | **Postposition Addition:** `दूर` is an adverb; substituting noun `फासले` requires locative postposition `पर`. |
| **`HC_1934`** | `भोजन करो।` | `खाना खाओ।` | `भोजन करो` $\to$ `खाना खाओ` | **Collocation/Verb Shift:** Collocation with `भोजन` is `करना`, whereas collocation with `खाना` is `खाना` (`खाओ`). |
| **`HC_1943`** | `युद्ध बुरा है।` | `लड़ाई बुरी है।` | `युद्ध बुरा` $\to$ `लड़ाई बुरी` | **Gender Concord:** `युद्ध` is masculine (taking `बुरा`), whereas `लड़ाई` is feminine (requiring `बुरी`). |

- **Adjudication Verdict:** These 8 pairs represent **flawless, natural Hindi grammar**, but they violate the strict single-word minimal-pair constraint. Including them in single-word tokenization and PLL analyses introduces token count shifts outside the target word.
- **Action Taken:** Extracted into **Candidate 4 (`scaleup_candidate_4_multiword_agreement.csv`)** as a specialized subgroup for studying model sensitivity to grammatical gender concord.

---

## Part 2: The 6 Spelling Errors Forming Real Hindi Words

In 6 pairs within `REALISTIC_SPELLING_ERROR`, the orthographic variation forms an existing entry in the Hindi lexicon:

| Pair ID | Original Sentence | Contrast Sentence | Target Word Change | Linguistic & Semantic Nature | Recommended Adjudication |
|---|---|---|---|---|---|
| **`HC_1552`** | `उसने नया गृह प्रवेश किया।` | `उसने नया ग्रह प्रवेश किया।` | `गृह` (home) $\to$ `ग्रह` (planet) | Orthographic typo (`ृ` vs `्र`) forming a real word. `ग्रह प्रवेश` is semantically incongruent. | Reclassify to `VALID_WORD_CONTEXT` |
| **`HC_1619`** | `पृथ्वी एक ग्रह है।` | `पृथ्वी एक गृह है।` | `ग्रह` (planet) $\to$ `गृह` (home) | Inverse of `HC_1552`. `पृथ्वी एक गृह है` ("Earth is a home") is grammatically valid but contextually anomalous. | Reclassify to `VALID_WORD_CONTEXT` (Duplicate of `HC_1973` in raw set) |
| **`HC_1689`** | `आज का दिन अच्छा है।` | `आज का दीन अच्छा है।` | `दिन` (day) $\to$ `दीन` (poor / humble) | Short `ि` vs long `ी` matra confusion. `दीन` is an archaic adjective. | Reclassify to `VALID_WORD_CONTEXT` |
| **`HC_1725`** | `हमें हार नहीं माननी चाहिए।` | `हमें हर नहीं माननी चाहिए।` | `हार` (defeat) $\to$ `हर` (every) | Missing aa-matra (`ा`). `हर नहीं माननी` is ungrammatical Hindi. | **Retain in `REALISTIC_SPELLING_ERROR`** |
| **`HC_1730`** | `पिता जी काम पर गए हैं।` | `पीता जी काम पर गए हैं।` | `पिता` (father) $\to$ `पीता` (drinks) | Short `ि` vs long `ी` matra confusion. `पीता` is a verb form, creating an ungrammatical sentence. | **Retain in `REALISTIC_SPELLING_ERROR`** |
| **`HC_1747`** | `अपना लक्ष्य निर्धारित करें।` | `अपना लक्ष निर्धारित करें।` | `लक्ष्य` (goal) $\to$ `लक्ष` (lakh / 100,000) | Missing conjunct ya (`्य`). `लक्ष` is a valid numeral noun, but ungrammatical in this slot. | **Retain in `REALISTIC_SPELLING_ERROR`** |

### Adjudication Guidelines:
- If substituting the word yields a **grammatically valid sentence testing contextual plausibility** (e.g., `दिन` $\to$ `दीन`, `गृह` $\to$ `ग्रह`), it should be classified as **`VALID_WORD_CONTEXT`**.
- If substituting the word yields an **ungrammatical string** even though the token appears in a dictionary (e.g., `हार` $\to$ `हर` in `हमें हर नहीं माननी चाहिए`), the model treats it as an ungrammatical syntactic crash; hence, it functions as a **`REALISTIC_SPELLING_ERROR`**.

---

## Part 3: The 4 Multi-Word Target Phrases

Four rows in the original benchmark subset (`HC_0091`, `HC_0094`, `HC_0104`, `HC_0112`) define `target_original` as a multi-word compound:
- `HC_0091`: `रखे हैं` $\to$ `रखा है` (plural vs singular copula phrase)
- `HC_0094`: `चली गई` $\to$ `चला गया` (feminine vs masculine compound verb)
- `HC_0104`: `खिला है` $\to$ `खिले हैं` (singular vs plural aspectual verb)
- `HC_0112`: `दीजिए` $\to$ `प्रस्तुत कीजिए` (honorific verb phrase expansion)

- **Linguistic Quality:** Excellent natural Hindi minimal pairs.
- **Pipeline Challenge:** In Stage 5/6/7 explanation extraction, MLM prediction targets are evaluated on single subwords. Multi-word phrases require custom average logit pooling.
- **Adjudication Verdict:** Excluded from the strict single-word Candidate 1; suitable for sentence-level PLL evaluation.

---

## Part 4: The 7 Interrogative Sentences

Seven sentences in the dataset end with an ASCII question mark `?` rather than a Devanagari danda `।`:
- `HC_0169`: `आप कहाँ जा रहे हैं?`
- `HC_0477`: `इस कमरे की चौड़ाई कितनी है?`
- `HC_0489`: `इसका मूल्य कितना है?`
- `HC_1522`: `आज की तिथि क्या है?`
- `HC_1543`: `आपकी आयु क्या है?`
- `HC_1688`: `घड़ी में क्या बजा है?`
- `HC_1987`: `इस समस्या का मूल क्या है?`

- **Linguistic Verdict:** Authentic, natural Hindi questions. In Devanagari, question marks are standardly borrowed from Latin punctuation for interrogatives.
- **Tokenization Check:** Both MuRIL (`?` = token ID 136) and XLM-RoBERTa (`?` = token ID 705) cleanly tokenize `?` as a single punctuation subword without corrupting surrounding words.
- **Adjudication Verdict:** These 7 sentences are fully valid and can be safely admitted into the benchmark.
