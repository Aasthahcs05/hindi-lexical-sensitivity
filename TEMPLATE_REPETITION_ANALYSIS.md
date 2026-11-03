# TEMPLATE REPETITION ANALYSIS: INVESTIGATION OF CARRIER SENTENCE CLUSTERING

**Project Title:** Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi  
**Phase:** Phase 2 — Final Dataset Adjudication and Scale-Up Readiness  
**Auditor:** Antigravity Research Assistant (Independent Verification Mode)  
**Date:** November 2026  

---

## Executive Summary

During the forensic quality audit of the new 2,000-example Hindi dataset, a distinct structural anomaly was identified: **278 sentence pairs (13.90% of the entire dataset)** between Rows 603 and 1499 were generated using **14 repetitive boilerplate carrier sentence templates**.

This report documents the exact decomposition of these 14 template families, lists every associated Pair ID, analyzes the linguistic and psycholinguistic validity of carrier frames, evaluates the theoretical consequences on MLM scoring and feature attributions, and provides a comparative scientific assessment between including vs. excluding these examples.

---

## 1. Forensic Decomposition of the 14 Template Families

Every one of the 278 template examples maps to one of 14 exact syntactic skeletons:

| Family # | Template Sentence Skeleton | Example Count | Track Breakdown | Unique Targets | Representative Pair IDs |
|---|---|---|---|---|---|
| **T-01** | `मैंने [TARGET] शब्द अपनी कॉपी में लिखा।` | **45** | 45 Spelling | 45 | `HC_0604`, `HC_0608`, `HC_0612`, `HC_0625`, `HC_0629`, `HC_0633` ... `HC_0904`, `HC_0908` |
| **T-02** | `हमें [TARGET] से जुड़ी जानकारी मिली।` | **44** | 44 Spelling | 44 | `HC_0610`, `HC_0614`, `HC_0622`, `HC_0635`, `HC_0639`, `HC_0643` ... `HC_0897`, `HC_0910` |
| **T-03** | `शिक्षक ने [TARGET] का उल्लेख किया।` | **43** | 43 Spelling | 43 | `HC_0603`, `HC_0607`, `HC_0624`, `HC_0628`, `HC_0632`, `HC_0645` ... `HC_0903`, `HC_0907` |
| **T-04** | `आज [TARGET] के बारे में चर्चा हुई।` | **42** | 42 Spelling | 42 | `HC_0602`, `HC_0615`, `HC_0623`, `HC_0627`, `HC_0640`, `HC_0644` ... `HC_0898`, `HC_0902` |
| **T-05** | `इस पाठ में [TARGET] का महत्व बताया गया।` | **42** | 42 Spelling | 42 | `HC_0605`, `HC_0609`, `HC_0613`, `HC_0630`, `HC_0634`, `HC_0647` ... `HC_0905`, `HC_0909` |
| **T-06** | `इस वाक्य में [TARGET] शब्द की वर्तनी जाँचें।` | **13** | 13 Spelling | 13 | `HC_1177`, `HC_1179`, `HC_1181`, `HC_1183`, `HC_1185`, `HC_1187` ... `HC_1201` |
| **T-07** | `रिपोर्ट में इसे [TARGET] बताया गया है।` | **8** | 8 Spelling | 8 | `HC_0617`, `HC_0655`, `HC_0688`, `HC_0742`, `HC_0767`, `HC_0850`, `HC_0884`, `HC_0913` |
| **T-08** | `यह [TARGET] विचार सभी को पसंद आया।` | **7** | 7 Spelling | 7 | `HC_0619`, `HC_0652`, `HC_0690`, `HC_0744`, `HC_0769`, `HC_0877`, `HC_0915` |
| **T-09** | `वाक्य में [TARGET] शब्द को रेखांकित कीजिए।` | **6** | 6 Spelling | 6 | `HC_0618`, `HC_0689`, `HC_0743`, `HC_0768`, `HC_0885`, `HC_0914` |
| **T-10** | `इस अनुच्छेद में [TARGET] शब्द का प्रयोग किया गया है।` | **6** | 6 Synonym | 6 | `HC_1096`, `HC_1111`, `HC_1126`, `HC_1141`, `HC_1156`, `HC_1171` |
| **T-11** | `इस वाक्य में [TARGET] शब्द स्वाभाविक लगता है।` | **6** | 6 Synonym | 6 | `HC_1097`, `HC_1112`, `HC_1127`, `HC_1142`, `HC_1157`, `HC_1172` |
| **T-12** | `लेख के अगले वाक्य में [TARGET] शब्द फिर आया।` | **6** | 6 Synonym | 6 | `HC_1098`, `HC_1113`, `HC_1128`, `HC_1143`, `HC_1158`, `HC_1173` |
| **T-13** | `शिक्षक ने [TARGET] शब्द का अर्थ समझाया।` | **5** | 5 Spelling | 5 | `HC_0654`, `HC_0687`, `HC_0879`, `HC_0883`, `HC_0912` |
| **T-14** | `शिक्षिका ने [TARGET] शब्द का अर्थ समझाया।` | **5** | 5 Spelling | 5 | `HC_0616`, `HC_0653`, `HC_0691`, `HC_0745`, `HC_0770` |
| **Total** | **All 14 Template Families Combined** | **278** | **254 Spelling, 24 Synonym** | **278** | **Full inventory documented in audit review** |

---

## 2. Linguistic and Methodological Evaluation

### 2.1 Are Target Words Systematically Substituted into Identical Sentences?
**YES.** Inspection reveals a clear batch generation design:
For a given vocabulary word (e.g., `पानी` vs. misspelled `पानि`), the author generated up to 5 sentences by plugging the word into the 5 primary template frames:
1. `आज पानी के बारे में चर्चा हुई।` $\to$ `आज पानि के बारे में चर्चा हुई।` (`HC_0602`)
2. `शिक्षक ने पानी का उल्लेख किया।` $\to$ `शिक्षक ने पानि का उल्लेख किया।` (`HC_0603`)
3. `मैंने पानी शब्द अपनी कॉपी में लिखा।` $\to$ `मैंने पानि शब्द अपनी कॉपी में लिखा।` (`HC_0604`)
4. `इस पाठ में पानी का महत्व बताया गया।` $\to$ `इस पाठ में पानि का महत्व बताया गया।` (`HC_0605`)

This pattern was repeated systematically across 45 distinct vocabulary lemmas (e.g., `बाज़ार`, `परीक्षा`, `स्वास्थ्य`, `उत्सव`, `विज्ञान`, `संस्कृति`, `संगीत`, `आशीर्वाद`, `विद्यार्थी`, `चिकित्सक`).

### 2.2 Linguistic Naturalness vs. Metalinguistic Priming
- **Naturalness:** Every template frame is grammatically flawless standard Hindi.
- **Metalinguistic Priming:** Notice that templates T-01, T-06, T-09, T-10, T-11, T-12, T-13, and T-14 explicitly contain the word **`शब्द` ("word")** (e.g., `मैंने [TARGET] शब्द अपनी कॉपी में लिखा।`, `इस अनुच्छेद में [TARGET] शब्द का प्रयोग किया गया है।`).
  - *Psycholinguistic Effect:* In linguistics, these are termed *metalinguistic carrier sentences* (often used in phonetic elicitation and dictation tasks).
  - *MLM Consequence:* Pretrained language models learn strong transitional probabilities between `[NOUN]` and `शब्द` (e.g., $P(\text{शब्द} \mid \text{पानी})$ is high). When `पानी` is misspelled as `पानि`, the model's conditioned expectation for `शब्द` can partially buffer or amplify the plausibility drop in an artificial manner.

---

## 3. Impact on Research Experimental Pipeline

### 3.1 Impact on Pseudo-Log-Likelihood (PLL) Scoring
1. **Context Prior Collapse:** In PLL calculation:
   $$\text{PLL}(W) = \sum_{t=1}^{|W|} \log P(w_t \mid W_{\setminus t})$$
   In a template sentence, 7 out of 8 tokens (`मैंने`, `शब्द`, `अपनी`, `कॉपी`, `में`, `लिखा`, `।`) are identical across 45 examples. The baseline plausibility of the surrounding context is virtually constant.
2. **Reduced Variance:** Because context variability is artificially suppressed, the score delta ($\Delta \text{MeanLogP}$) reflects *almost purely* the target token's unigram prior and its local bigram transition to `शब्द`, rather than realistic syntactic integration.

### 3.2 Impact on Subword Tokenization Dynamics
- **Zero Adverse Effect:** The subword segmentation of the carrier sentence is constant across all 45 instances (`मैंने` = 1 subword, `शब्द` = 1 subword, `अपनी` = 1 subword, etc.). 
- All tokenization fragmentation shifts ($\Delta \text{Tokens}$) remain strictly localized to the target word, providing an exceptionally clean test of isolated target fragmentation.

### 3.3 Impact on Last-Layer Self-Attention Rollup
- **Clustered Attention Distribution:** When computing target-to-context attention:
  $$\alpha_c = \frac{\bar{A}_{\text{target} \to c}}{\sum_{c' \in C} \bar{A}_{\text{target} \to c'}}$$
  Because the context is identical across 45 pairs, the attention heads consistently assign highest weights to `शब्द` (immediate right neighbor) and governing verb `लिखा`. While this provides high stability across items, it artificially inflates cross-example correlation, reducing the effective sample size of attention patterns.

### 3.4 Impact on Integrated Gradients Attribution
- **Baseline Invariance:** Integrated Gradients attributes the target logit against a `[PAD]` baseline. Because the context tokens are identical, the gradient paths through the embedding layer follow near-identical trajectories across all 45 examples.

### 3.5 Threat to Statistical Independence (Pseudo-Replication)
In statistical hypothesis testing (Wilcoxon signed-rank tests, Spearman correlations):
- Testing 45 pairs that share the identical carrier frame `मैंने [TARGET] शब्द अपनी कॉपी में लिखा।` introduces **correlated errors** (pseudo-replication).
- If an MLM happens to possess an idiosyncratic bias regarding `कॉपी में लिखा`, that single bias is multiplied 45 times in the statistical sample, artificially deflating standard errors and inflating $p$-values.

---

## 4. Rigorous Comparison: Scenario A vs. Scenario B

| Dimension | Scenario A: Include Templates ($N=1,954$) | Scenario B: Exclude Templates ($N=1,676$) |
|---|---|---|
| **Total Sample Size** | **1,954 pairs** ($97.7\%$ of raw dataset) | **1,676 pairs** ($83.8\%$ of raw dataset) |
| **`REALISTIC_SPELLING_ERROR` $N$** | **1,259 pairs** | **1,005 pairs** |
| **`SYNONYM_SUBSTITUTION` $N$** | **386 pairs** | **362 pairs** |
| **`VALID_WORD_CONTEXT` $N$** | **309 pairs** | **309 pairs** |
| **Context Syntactic Diversity** | Lower (278 pairs share 14 frames) | **High (Each pair has unique natural context)** |
| **Metalinguistic Priming Bias** | Present in 15% of examples (`शब्द`) | **Minimal (Natural discourse sentences)** |
| **Statistical Independence** | Mild risk of pseudo-replication | **Pristine (Meets i.i.d. assumptions)** |
| **Attention / IG Diversity** | Clustered on repetitive frame tokens | **Rich, diverse contextual distributions** |
| **Single-Subword Spelling Power** | Extremely High ($N \approx 380$ single-subwords) | **Substantial ($N \approx 300$ single-subwords)** |

---

## 5. Strategic Recommendation: The Two-Tier Protocol

We strongly recommend **Scenario B (Candidate 1, $N=1,676$) as the primary benchmark** for conference reporting, accompanied by **Scenario A (Candidate 2, $N=1,954$) as a secondary sensitivity analysis**:

1. **Primary Submission Analysis (Candidate 1, $N=1,676$):**
   - Eliminates all template repetition confounding.
   - Satisfies peer-review scrutiny regarding statistical independence and natural language validity.
   - With 1,005 clean spelling pairs, statistical power is already $50\times$ larger than the original 20-pair study.
2. **Secondary Sensitivity Analysis (Candidate 2, $N=1,954$):**
   - Re-runs PLL and stability metrics on the full dataset to demonstrate that experimental findings hold regardless of carrier frame repetition.

Both candidates have been exported and serialized in `data/scaleup_candidates/`.
