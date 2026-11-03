# Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi (D-SAFE)

**Ananya Sharma**, **Aneka Srivastava**, **Aastha Srivastava**, **Aastha**, **Anchal Rai**, **Bikki Kumar**  
*Department of Computer Science and Engineering (Artificial Intelligence)*  
*KIET Deemed to be University, Ghaziabad, Uttar Pradesh, India*  
`{ananyasharma0286, aneka7216, aasthasrivastava210, aasthahcs05, anchalrai3008, bikkikumar}@gmail.com`

---

## Abstract

Masked language models (MLMs) have become central to multilingual natural language processing (NLP), yet their behavior and interpretability under non-Latin, morpho-phonetically complex scripts remain critically underexplored. In this work, we present a systematic empirical investigation into model behavior, subword tokenization dynamics, explanation stability, and explanation faithfulness under controlled lexical perturbations in Devanagari Hindi (D-SAFE). Using a verified, fully adjudicated Primary Benchmark of $N=1,679$ minimal sentence pairs ($3,358$ individual evaluations) across three controlled tracks—*Valid Word Context* ($N=312$), *Synonym Substitution* ($N=362$), and *Realistic Spelling Error* ($N=1,005$)—supplemented by an expanded Template Sensitivity Benchmark ($N=1,957$ minimal pairs), an Auxiliary Multiword Probe ($N=12$), and a preserved preliminary pilot cohort ($N=200$), we evaluate the Indic-dedicated encoder **MuRIL** (`google/muril-base-cased`) and the massively multilingual generalist **XLM-RoBERTa** (`FacebookAI/xlm-roberta-base`).

Our experiments reveal four primary findings. First, authentic Devanagari spelling errors (matra inversions and ligature splits) induce catastrophic subword fragmentation: single-subword target coverage collapses by $-71.6\%$ in MuRIL ($91.7\% \to 20.1\%$) and by $-55.9\%$ in XLM-RoBERTa ($62.3\% \to 6.4\%$), causing an average sentence-level token inflation of $+1.13$ subwords in MuRIL and $+1.04$ subwords in XLM-RoBERTa driven exclusively by target fracturing. Second, both models reliably penalize spelling errors under pseudo-log-likelihood (PLL) scoring, but MuRIL exhibits substantially harsher penalties (original preferred in $83.2\%$ of pairs, mean $\Delta \text{MeanLogP} = -1.2045$) than XLM-RoBERTa ($76.4\%$, mean $\Delta \text{MeanLogP} = -0.8864$), while both models recognize valid synonyms as near-equivalent ($\Delta = -0.0098$ for XLM-R; $\Delta = -0.1787$ for MuRIL). Cross-model rank correlation across all $1,679$ pairs is $r_s = +0.5496$ ($p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$) with $73.67\%$ directional agreement. Third, under a corrected visible-target scoring protocol on $N=1,005$ spelling pairs that resolves an illusory perfect stability artifact ($\rho = 1.0000$) induced by target masking, last-layer self-attention achieves substantially higher rank stability (pooled mean $\rho = 0.8027$ in MuRIL, $\rho = 0.6258$ in XLM-RoBERTa) than Layer Integrated Gradients (pooled mean $\rho = 0.2560$ in MuRIL, $\rho = 0.3319$ in XLM-RoBERTa), while Integrated Gradients preserves high vector cosine similarity ($0.9818$ in MuRIL; $0.8890$ in XLM-RoBERTa). Fourth, in discrete context token erasure tests ($f \in \{0.10, 0.20, 0.30\}$, $N=2,010$ sentences per model), attention attributions yield superior faithfulness win rates against control erasure ($63.53\%\text{--}67.46\%$ in XLM-RoBERTa), whereas continuous Integrated Gradients in MuRIL operates near or below chance ($46.72\%\text{--}49.90\%$ win rates; negative mean faithfulness gaps of $-0.2998$ to $-1.0845$). Finally, an explicit correlation analysis across all evaluated Devanagari spelling pairs demonstrates that **there is no consistent positive association between explanation stability and faithfulness**. While some weak negative associations occur for MuRIL Attention (pooled Pearson $r = -0.0790, p = 0.0248$; strict single-subword Spearman $\rho = -0.1924, p = 0.0067$), other combinations are non-significant (XLM-R Attention pooled $r_s = +0.0607, p = 0.0612$; XLM-R IG pooled $r_s = +0.0632, p = 0.0510$; MuRIL IG pooled $r_s = +0.0214, p = 0.5442$). These empirical findings establish that attribution stability under spelling noise cannot be assumed to guarantee or track causal explanation faithfulness, cautioning against using stability as an unvalidated proxy for explanation quality in explainable NLP benchmarks.

**Keywords**: Devanagari Hindi, Masked Language Models, Subword Tokenization, Pseudo-Log-Likelihood Scoring, Explainable NLP, Explanation Stability, Explanation Faithfulness, Integrated Gradients, Self-Attention.

---

## 1. Introduction

Pretrained masked language models (MLMs) based on bidirectional Transformer architectures have fundamentally advanced modern computational linguistics across high-resource and multilingual environments \cite{devlin-etal-2019-bert,conneau-etal-2020-unsupervised}. However, the empirical behaviors of these models are overwhelmingly documented in languages employing Latin alphabets, where typographical noise predominantly consists of straightforward character substitutions, deletions, or transpositions \cite{salazar-etal-2020-masked,rust-etal-2021-good}. In contrast, non-Latin writing systems—specifically Indic scripts following the abugida orthographic typology such as Devanagari Hindi—possess unique structural, syllabic, and compositional characteristics. Devanagari encodes phonological syllables (aksharas) utilizing base consonant characters, dependent vowel diacritics (matras), and virama-linked conjuncts (ligatures). Consequently, minor orthographic variations or colloquial misspellings in Devanagari do not operate as isolated character perturbations; rather, they alter the underlying graphemic and syllabic representation, frequently destroying canonical subword vocabulary entries and triggering severe tokenization fragmentation \cite{kakwani-etal-2020-indicnlpsuite}.

In parallel with questions surrounding language model scoring and tokenization robustness, the interpretability of Transformer architectures has emerged as a cornerstone of trustworthy NLP \cite{sundararajan-etal-2017-axiomatic,deyoung-etal-2020-eraser}. Researchers and practitioners routinely employ feature attribution techniques—such as gradient-based saliency methods and self-attention weights—to decipher the decision-making processes of neural models \cite{jain-wallace-2019-attention,wiegreffe-pinter-2019-attention}. Within the explainable AI (XAI) literature, two evaluative criteria are frequently prioritized:
1. **Explanation Stability (Robustness)**: The degree to which an explanation remains invariant under minor, semantics-preserving input perturbations \cite{alvarez-melis-jaakkola-2018-robustness,dombrowski-etal-2019-explanations}.
2. **Explanation Faithfulness**: The degree to which an explanation accurately reflects the model's internal causal reasoning, typically evaluated by erasing top-attributed tokens and measuring the corresponding decline in model output certainty \cite{deyoung-etal-2020-eraser,jacovi-goldberg-2020-towards}.

Critically, a pervasive but largely untested assumption in applied XAI benchmarks is that attribution stability is an indicator of explanation quality, with the implicit expectation that an explanation that is robust to localized input noise is also more likely to be faithful to the underlying model mechanism \cite{ding-koehn-2021-evaluating,atanasova-etal-2020-diagnostic}.

This study bridges this empirical and conceptual gap by investigating Devanagari Hindi lexical sensitivity and conducting a joint, rigorous evaluation of subword tokenization, model scoring, explanation stability, and explanation faithfulness. We formulate our inquiry around five primary research questions (RQs):
- **RQ1**: How do contextual lexical contrasts, synonym substitutions, and spelling perturbations affect subword tokenization and model scoring in Devanagari Hindi?
- **RQ2**: How do MuRIL (an Indic-dedicated MLM) and XLM-RoBERTa (a global multilingual generalist) differ in their representations of and scoring responses to these perturbations?
- **RQ3**: How stable are Attention and Integrated Gradients explanations when evaluated under authentic Devanagari spelling perturbations?
- **RQ4**: How do Attention and Integrated Gradients behave under discrete context-token masking interventions in masked language models?
- **RQ5**: Is explanation stability under input noise statistically associated with measured explanation faithfulness under feature erasure?

To answer these questions, we construct and rigorously audit a primary Devanagari Hindi minimal pair benchmark of $N=1,679$ pairs ($3,358$ evaluations), alongside an expanded template sensitivity benchmark ($N=1,957$), an auxiliary multiword probe ($N=12$), and a preserved historical pilot ($N=200$). We formulate an experimental pipeline combining pseudo-log-likelihood (PLL) scoring, fast subword offset mapping, Layer Integrated Gradients, and last-layer multi-head self-attention extraction. Importantly, we document and resolve a critical methodological artifact in perturbation-based stability evaluation—the *masked-target artifact*—and establish the *Visible-Target Scoring Protocol* to measure genuine attribution dynamics across $1,005$ spelling pairs.

Our quantitative results demonstrate that while Devanagari spelling errors cause severe vocabulary collapse and predictable score penalties, explanation stability exhibits no consistent positive association with explanation faithfulness. Furthermore, we show that despite theoretical arguments prioritizing axiomatic gradient methods, self-attention attributions exhibit substantially higher empirical stability and discrete masking faithfulness than Integrated Gradients in masked language models.

---

## 2. Background and Related Work

### 2.1 Indic-Language Pretrained Models and Devanagari NLP
The development of multilingual masked language models has expanded NLP capabilities across non-English languages. Prominent architectures include mBERT \cite{devlin-etal-2019-bert} and XLM-RoBERTa \cite{conneau-etal-2020-unsupervised}. XLM-RoBERTa utilizes a Byte-Pair Encoding (BPE) SentencePiece vocabulary of 250,002 tokens shared across more than 100 languages, trained on massive web-crawled Common Crawl corpora. To overcome vocabulary dilution in massively multilingual models, Khanuja et al. \cite{khanuja-etal-2021-muril} introduced **MuRIL** (*Multilingual Representations for Indic Languages*), a BERT-base architecture trained exclusively on 17 Indic languages and English using a 197,285-token WordPiece vocabulary. Kakwani et al. \cite{kakwani-etal-2020-indicnlpsuite} similarly developed IndicBERT and the IndicGLUE benchmark, emphasizing that language-family specialization improves syntactic and morphological capture. However, comparative investigations into how these divergent pretraining strategies govern fine-grained orthographic and lexical sensitivity in Hindi remain sparse.

### 2.2 Subword Tokenization and Orthographic Vulnerability
Subword segmentation algorithms, such as Byte-Pair Encoding (BPE) \cite{sennrich-etal-2016-neural}, WordPiece \cite{devlin-etal-2019-bert}, and Unigram SentencePiece \cite{kudo-richardson-2018-sentencepiece}, are foundational to modern transformers. Although these tokenizers mitigate out-of-vocabulary (OOV) challenges by segmenting unseen words into subword fragments, recent studies have demonstrated that subword tokenizers are brittle under orthographic variations \cite{bostrom-durrett-2020-byte,rust-etal-2021-good}. In languages written in the Devanagari script, the structural unit is the akshara (syllable), composed of consonant bases modified by attached vowel diacritics (matras) or conjunct-forming halants (viramas). When a user introduces a spelling error—such as swapping a long *dirgha* matra for a short *hrasva* matra (e.g., `पानी` $\to$ `पानि`) or omitting a halant (e.g., `आवश्यक` $\to$ `आवशयक`)—the character sequence shifts across syllabic boundaries. Unlike Latin typos which frequently preserve the subword root, Devanagari perturbations fracture canonical vocabulary tokens into isolated bytes or single Unicode codepoints \cite{kakwani-etal-2020-indicnlpsuite}.

### 2.3 Masked Language Model Scoring and Pseudo-Log-Likelihood
Autoregressive language models naturally provide sequence probabilities via the chain rule of probability. In contrast, bidirectional masked language models cannot directly factorize sequence joint probabilities due to bidirectional conditioning. To evaluate sentence plausibility in MLMs, Wang and Cho \cite{salazar-etal-2020-masked} and Salazar et al. \cite{salazar-etal-2020-masked} formalized **Pseudo-Log-Likelihood (PLL)** scoring. By iteratively masking each token in a sentence and accumulating the conditional log-probabilities of the masked tokens given the bidirectional context, PLL provides an effective proxy for grammatical acceptability and corpus typicality. In this work, we follow Salazar et al. \cite{salazar-etal-2020-masked} while strictly implementing length-normalized scoring ($\text{MeanLogP}$) to account for tokenization fertility differences between canonical and misspelled sentences.

### 2.4 Feature Attribution: Attention vs. Integrated Gradients
Feature attribution methods aim to assign an importance score to each input token reflecting its contribution to a model's prediction. **Integrated Gradients (IG)** \cite{sundararajan-etal-2017-axiomatic} is an axiomatic path-attribution method that computes the path integral of gradients along a straight line between a baseline input (typically zero or pad embeddings) and the input representation. IG uniquely satisfies two foundational mathematical axioms: *Completeness* (attributions sum to the difference between the target output and the baseline output) and *Implementation Invariance*.

Conversely, **Self-Attention** weights from Transformer layers have frequently been utilized as heuristic explanations \cite{serrano-smith-2019-attention}. This practice sparked an extensive academic debate: Jain and Wallace \cite{jain-wallace-2019-attention} famously argued that "Attention is not Explanation," demonstrating that attention weights often correlate weakly with gradient-based saliency and that adversarial attention distributions can be constructed without altering predictions. Wiegreffe and Pinter \cite{wiegreffe-pinter-2019-attention} countered that attention distributions frequently track model predictions well and that alternative adversarial distributions may fail simple consistency checks. Brunner et al. \cite{brunner-etal-2020-identifiability} further demonstrated that attention weights in deep layers suffer from loss of token identifiability. Our work directly engages this debate within the context of masked language models and Indic text.

### 2.5 Explanation Stability and Faithfulness Evaluation
In evaluating explanation quality, the literature distinguishes between stability and faithfulness. **Stability** (or robustness) examines whether small, task-irrelevant changes to the input produce small changes in the attribution vector \cite{alvarez-melis-jaakkola-2018-robustness}. Saliency methods have been shown to be susceptible to adversarial shifts and geometric noise \cite{dombrowski-etal-2019-explanations,heo-etal-2019-fooling}. **Faithfulness**, formalized in benchmarks such as ERASER \cite{deyoung-etal-2020-eraser}, assesses whether the features identified by an explanation method correspond to the actual causal reasoning of the model. Common metrics include *comprehensiveness* (how much model confidence drops when top-attributed features are erased) and *sufficiency* (how well model confidence is retained when only top features are kept) \cite{jacovi-goldberg-2020-towards,atanasova-etal-2020-diagnostic}. Bastings and Filippova \cite{bastings-filippova-2020-elephant} highlighted that saliency methods, while theoretically appealing, often behave unpredictably under feature erasure. Crucially, prior work has predominantly treated stability and faithfulness as independent evaluation benchmarks without empirically testing their mutual relationship.

---

## 3. Dataset Construction & Annotation Methodology

### 3.1 Benchmark Design, Track Structure, and Cohort Partitioning
To evaluate lexical sensitivity and interpretability in Devanagari Hindi, we established an audited benchmark infrastructure derived from an exhaustive reconciliation of 2,000 candidate sentence pairs. Each minimal pair consists of an **Original Sentence** ($S_{\text{orig}}$) containing a canonical Hindi target word ($w_{\text{orig}}$) and a **Contrast Sentence** ($S_{\text{cont}}$) where the target word is replaced by a perturbed variant ($w_{\text{cont}}$), while keeping all surrounding context words identical.

The research infrastructure comprises four distinct cohorts:
1. **Primary Benchmark ($N=1,679$, $3,358$ evaluations)**: The authoritative, adjudicated gold-standard cohort partitioned into three mutually exclusive experimental tracks:
   - **`VALID_WORD_CONTEXT` ($N=312$, $18.58\%$)**: Minimal pairs where the target word is replaced by an alternative, grammatically valid Hindi word creating a contextual semantic mismatch.
   - **`SYNONYM_SUBSTITUTION` ($N=362$, $21.56\%$)**: Minimal pairs where the target word is replaced by a verified, contextually appropriate Hindi synonym (e.g., `पानी` [water] $\leftrightarrow$ `जल`, `सूर्य` [sun] $\leftrightarrow$ `सूरज`), preserving core propositional semantics.
   - **`REALISTIC_SPELLING_ERROR` ($N=1,005$, $59.86\%$)**: Minimal pairs where the target word is replaced by an authentic orthographic or phonological misspelling commonly observed in contemporary Devanagari writing.
2. **Secondary Template Sensitivity Benchmark ($N=1,957$, $3,914$ evaluations)**: An expanded benchmark containing the Primary Benchmark ($N=1,679$) plus 278 template-derived sentence variants across 278 syntactic frames (`VALID_WORD_CONTEXT`: $N=312$, `SYNONYM_SUBSTITUTION`: $N=385$, `REALISTIC_SPELLING_ERROR`: $N=1,260$). We emphasize that this is an expanded frame-invariance cohort designed to assess syntactic robustness, not an independent dataset.
3. **Auxiliary Multiword Probe ($N=12$, $24$ evaluations)**: A targeted probe designed to investigate multiword lexical substitutions and alignment edge cases, classified under a fine-grained 4-category linguistic taxonomy:
   - 6 gender/number agreement changes (e.g., `HC_0069`, `HC_0113`, `HC_1863`, `HC_1874`, `HC_1878`, `HC_1943`)
   - 1 postpositional case insertion (`HC_1919`)
   - 1 collocational light-verb substitution (`HC_1934`)
   - 4 repeated-target word ambiguities (`HC_1060`, `HC_1067`, `HC_1081`, `HC_1190`)
4. **Historical Pilot Cohort ($N=200$, $400$ evaluations)**: The initial exploratory preliminary benchmark ($142$ valid word, $38$ synonym, $20$ spelling), preserved intact in `results/runs/historical_pilot_200/` to document the project's developmental trajectory.

```
+---------------------------------------------------------------------------------------------------+
| Primary Benchmark Distribution (N = 1,679 Minimal Sentence Pairs)                                 |
|                                                                                                   |
|  [VALID_WORD_CONTEXT]        ============= 312 pairs (18.58%)                                     |
|  [SYNONYM_SUBSTITUTION]     =============== 362 pairs (21.56%)                                   |
|  [REALISTIC_SPELLING_ERROR] ========================================== 1,005 pairs (59.86%)       |
+---------------------------------------------------------------------------------------------------+
```

### 3.2 Typology of Devanagari Orthographic Errors
The 1,005 spelling error pairs in the primary `REALISTIC_SPELLING_ERROR` track systematically reflect four authentic Devanagari error typologies:
- **Matra Vowel Length Inversion**: Inversion of short (*hrasva*) and long (*dirgha*) vowel diacritics. In spoken Hindi, phonemic vowel duration distinctions are frequently blurred, leading to common writing errors (e.g., `पानी` $\to$ `पानि`, `परीक्षा` $\to$ `परिक्षा`).
- **Conjunct and Ligature Disruptions**: Omission of virama/halant markers or improper splitting of samyuktaksharas (e.g., `स्वास्थ्य` $\to$ `स्वास्थ`, `आवश्यक` $\to$ `आवशयक`).
- **Orthographic Alternations**: Standardized graphic variations, such as anusvara vs. class nasal substitutions (`संभावना` vs. `सम्भावना`) and single vs. double ligature spellings (`महत्वपूर्ण` vs. `महत्त्वपूर्ण`).
- **Colloquial Phonetic Spellings**: Dialectal substitutions widely observed in social media and informal communications (e.g., `वापस` $\to$ `वापिस`).

### 3.3 Quality Control, Reconciliation, and Provenance
Every row in the 2,000-row candidate corpus was tracked through a comprehensive reconciliation audit:
1. **Reconciliation Completeness**: Exactly 1,679 rows were adjudicated into the Primary Benchmark, 278 rows were assigned to the Template Sensitivity Benchmark, 12 rows were assigned to the Auxiliary Multiword Probe, and 31 rows were excluded due to annotation invalidity ($1679 + 278 + 12 + 31 = 2000$). Exactly 0 rows remain unresolved.
2. **Script Integrity**: 100% of characters in all evaluated sentences reside strictly within the Devanagari Unicode block (`U+0900` to `U+097F`) or standard punctuation.
3. **Computational Provenance**: In the verified rerun pipeline, Stages 1 and 2 were freshly computed during `task-340` (7.41s and 200.23s) and validated during recovery in `task-376` (0.17s and 0.18s); Stages 3 through 9 were freshly computed during `task-376` (total runtime 29.68 minutes on CUDA). Zero stages were reused from older baseline runs.

---

## 4. Models and Experimental Methodology

### 4.1 Evaluated Pretrained Architectures
We conduct all experiments across two distinct pretrained bidirectional Transformer models:
- **MuRIL (`google/muril-base-cased`)**: A BERT-base architecture (12 layers, 12 attention heads, 768 hidden dimensions, ~236M parameters) pretrained on 17 Indic languages and English using an Indic-dedicated WordPiece vocabulary of 197,285 tokens \cite{khanuja-etal-2021-muril}.
- **XLM-RoBERTa (`FacebookAI/xlm-roberta-base`)**: A RoBERTa-base architecture (12 layers, 12 attention heads, 768 hidden dimensions, ~278M parameters) pretrained on 2.5TB of Common Crawl data across 100+ languages using a SentencePiece BPE vocabulary of 250,002 tokens \cite{conneau-etal-2020-unsupervised}.

Both models were evaluated on an **NVIDIA GeForce RTX 3050 6GB Laptop GPU** (CUDA 12.6, PyTorch 2.14.1+cu126, batch size 32), with explicit `attn_implementation="eager"` to guarantee complete self-attention tensor extraction.

### 4.2 Subword Tokenization Analysis & Alignment Protocol
We extract subword tokenizations utilizing HuggingFace fast tokenizers with offset mapping (`return_offsets_mapping=True`). For every sentence pair, we compute:
- Full sequence token counts, both special-token-inclusive ($|W_{\text{all}}|$) and exclusive ($|W_{\text{excl}}|$).
- Target word subword lengths for original ($|T_{\text{orig}}|$) and contrast ($|T_{\text{cont}}|$) sentences.
- Single-subword target coverage: the percentage of target words that tokenize into exactly one subword token ($|T| = 1$).
- Alignment outcomes between original and contrast context tokens.

### 4.3 Pseudo-Log-Likelihood (PLL) Scoring Formulations
Following Salazar et al. \cite{salazar-etal-2020-masked}, for a sentence $W = (w_1, w_2, \dots, w_{|W|})$, the sentence-level pseudo-log-likelihood is computed by iteratively masking each non-special token $w_t$:
$$\text{PLL}(W) = \sum_{t=1}^{|W|} \log P(w_t \mid W_{\setminus t}; \Theta)$$
where $W_{\setminus t}$ denotes the input sequence with token $w_t$ replaced by the model's mask token (`[MASK]` for MuRIL, `<mask>` for XLM-RoBERTa), and $\Theta$ denotes the model parameters.

To prevent token length bias—where a sentence segmented into more subwords naturally accumulates a more negative sum—we compute the length-normalized mean log-probability:
$$\text{MeanLogP}(W) = \frac{\text{PLL}(W)}{|W_{\text{scorable}}|}$$
where $|W_{\text{scorable}}|$ is the number of iteratively masked content tokens.

The plausibility shift between contrast and original sentences is defined as the signed delta:
$$\Delta \text{MeanLogP} = \text{MeanLogP}(W_{\text{cont}}) - \text{MeanLogP}(W_{\text{orig}})$$
Under this convention:
- $\Delta \text{MeanLogP} < 0$: The original sentence is assigned higher plausibility (canonical preference).
- $\Delta \text{MeanLogP} > 0$: The contrast sentence is assigned higher plausibility.

> **Methodological Guardrail on Cross-Model Comparability**: Because MuRIL and XLM-RoBERTa utilize entirely different subword vocabularies and tokenization algorithms, their raw PLL and MeanLogP sums occupy non-commensurable probability spaces. Therefore, cross-model comparisons are strictly restricted to within-model signed deltas ($\Delta \text{MeanLogP}$), preference rates, and directional agreement.

### 4.4 Feature Attribution Extraction
We evaluate two widely utilized feature attribution methods across the context tokens of each sentence:
1. **Last-Layer Multi-Head Self-Attention**:
   We extract the self-attention tensor $A \in \mathbb{R}^{12 \times |W| \times |W|}$ from Layer 11 (the final transformer layer). Attention weights are averaged across all 12 attention heads:
   $$\bar{A}_{i, j} = \frac{1}{12} \sum_{h=1}^{12} A^{(11, h)}_{i, j}$$
   The attribution for context token $j \notin T$ with respect to target token set $T$ is the mean directed attention from the target positions to context token $j$:
   $$\alpha_j = \frac{1}{|T|} \sum_{t \in T} \bar{A}_{t, j}$$
   Special framing tokens are removed, and the resulting context vector is normalized such that $\sum_{j \in C} \alpha_j = 1$.

2. **Layer Integrated Gradients (IG)**:
   Using Captum \cite{sundararajan-etal-2017-axiomatic}, we compute Integrated Gradients with respect to the word embedding layer. We utilize a zero-embedding baseline vector ($x' = \mathbf{0}$) and approximate the path integral using 50 Gauss-Legendre quadrature steps:
   $$\text{IG}_i(x) = (x_i - x'_i) \times \sum_{k=1}^{50} \frac{\partial F\left(x' + \frac{k}{50}(x - x')\right)}{\partial x_i} \times \frac{1}{50}$$
   The scalar token attribution is obtained by computing the Euclidean $L_2$-norm over the 768 embedding dimensions, followed by context-level normalization.

### 4.5 The Stage 6 Masked-Target Artifact & The Stage 7 Visible-Target Protocol
A critical methodological finding of this research is the documentation of the **Masked-Target Artifact** during preliminary stability evaluations (Stage 6). When the target word was replaced by `[MASK]` in both the original and contrast sentences, the input sequences fed into the model became byte-identical ($X_{\text{orig}} \equiv X_{\text{cont}}$). Consequently, the neural network processed the exact same numerical input, producing an illusory, trivial stability ($\rho = 1.0000$, $\text{Cosine} = 1.0000$).

To resolve this benchmark design flaw, we formulated the **Visible-Target Scoring Protocol** in Stage 7:
1. Target words remain **fully visible** in the input text during attribution computation.
2. The target prediction score is defined as the mean unnormalized logit of the actual target subwords:
   $$S(X; Y_{\text{target}}) = \frac{1}{|T|} \sum_{j \in T} \text{Logit}(p_j, y_j)$$
   where $p_j$ is the sequence position of the $j$-th target subword and $y_j$ is its ground-truth token ID.
3. Feature attributions are computed across the unperturbed context tokens while the model processes the actual spelling error, capturing genuine sensitivity.

### 4.6 Stability Metrics
For each spelling pair ($N=1,005$), we align context tokens between the original sentence ($C_{\text{orig}}$) and contrast sentence ($C_{\text{cont}}$) using character offset tracking. We evaluate two complementary stability metrics:
- **Rank Stability (Spearman $\rho$)**: Measures whether the relative importance ordering of context tokens is preserved under target spelling noise:
  $$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
- **Directional Vector Stability (Cosine Similarity)**: Measures whether the global orientation of the attribution vector in $\mathbb{R}^{|C|}$ is preserved:
  $$\text{Cosine}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|_2 \|\mathbf{v}\|_2}$$

### 4.7 Faithfulness Evaluation via Context Erasure
Following the ERASER benchmark framework \cite{deyoung-etal-2020-eraser}, we evaluate explanation faithfulness by measuring how target prediction scores change when context tokens are systematically erased. For each sentence ($N=2,010$ sentences per model across 1,005 pairs), context tokens are ranked by their attribution scores. We evaluate three masking interventions at fractions $f \in \{0.10, 0.20, 0.30\}$:
- **Top-$k$ Erasure**: Replacing the top $k = \lceil f \cdot |C| \rceil$ highest-attributed context tokens with the model's mask token.
- **Bottom-$k$ Erasure (Control)**: Replacing the $k$ lowest-attributed context tokens with the mask token.
- **Random-$k$ Erasure**: Replacing $k$ randomly selected context tokens with the mask token (averaged over 5 independent random trials).

We record:
1. **Target Logit Drop**: $\Delta S = S_0 - S_{\text{masked}}$, where $S_0$ is the unmasked target score.
2. **Faithfulness Gap**:
   $$\text{Faithfulness Gap} = \Delta S_{\text{top}} - \Delta S_{\text{bottom}} = S_{\text{bottom}} - S_{\text{top}}$$
   A positive gap indicates that erasing top-attributed tokens degrades target prediction more than erasing bottom-attributed control tokens ($S_{\text{top}} < S_{\text{bottom}}$).
3. **Win Rate vs. Bottom Control**: The percentage of evaluated sentences where $\Delta S_{\text{top}} > \Delta S_{\text{bottom}}$.

---

## 5. Empirical Results

### 5.1 Subword Tokenization & Catastrophic Target Fragmentation

Table 1 presents the subword tokenization properties across models and experimental tracks on the primary benchmark ($N=1,679$).

| Model Checkpoint | Experimental Track | Pair Count ($N$) | Mean Orig Tokens | Mean Cont Tokens | Token Delta ($\Delta$) | Length Ratio | Mean Orig Target Subwords | Mean Cont Target Subwords | Single-Subword Orig Target (%) | Single-Subword Cont Target (%) | Single-Subword Collapse ($\Delta$) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | `REALISTIC_SPELLING_ERROR` | 1,005 | 10.91 | 11.96 | **+1.04** | 1.11 | 1.63 | 2.67 | 62.3% | 6.4% | **-55.9%** |
| **XLM-RoBERTa** | `SYNONYM_SUBSTITUTION` | 362 | 9.15 | 9.33 | +0.18 | 1.03 | 1.29 | 1.47 | 77.3% | 68.2% | -9.1% |
| **XLM-RoBERTa** | `VALID_WORD_CONTEXT` | 312 | 10.48 | 10.70 | +0.22 | 1.02 | 1.68 | 1.89 | 44.6% | 30.8% | -13.8% |
| **MuRIL** | `REALISTIC_SPELLING_ERROR` | 1,005 | 9.67 | 10.80 | **+1.13** | 1.12 | 1.12 | 2.25 | 91.7% | 20.1% | **-71.6%** |
| **MuRIL** | `SYNONYM_SUBSTITUTION` | 362 | 8.43 | 8.52 | +0.10 | 1.01 | 1.02 | 1.11 | 98.6% | 92.8% | -5.8% |
| **MuRIL** | `VALID_WORD_CONTEXT` | 312 | 9.20 | 9.31 | +0.11 | 1.01 | 1.36 | 1.46 | 70.5% | 59.6% | -10.9% |

*Table 1: Subword tokenization analysis across models and experimental tracks on the primary benchmark ($N=1,679$). Source: `results/runs/scaleup_rerun/dashboard_data/tokenization_summary.csv`.*

Three primary tokenization patterns emerge from Table 1:
1. **Catastrophic Fragmentation under Spelling Errors**: In `REALISTIC_SPELLING_ERROR` ($N=1,005$), introducing authentic Devanagari spelling errors causes an average increase of **$+1.13$ target subwords** in MuRIL and **$+1.04$ subwords** in XLM-RoBERTa. In MuRIL, single-subword target coverage collapses from **$91.7\%$ (922/1,005) to $20.1\%$ (202/1,005)**, an absolute drop of **$-71.6\%$**. In XLM-RoBERTa, coverage collapses from **$62.3\%$ (626/1,005) to $6.4\%$ (64/1,005)**, an absolute drop of **$-55.9\%$**.
2. **Tokenizer Efficiency**: MuRIL encodes Hindi text with substantially greater compactness than XLM-RoBERTa across all tracks. On `REALISTIC_SPELLING_ERROR`, MuRIL requires a mean of 9.67 tokens per original sentence versus 10.91 tokens for XLM-RoBERTa (11.4% fewer tokens); on `VALID_WORD_CONTEXT`, MuRIL requires 9.20 tokens versus 10.48 tokens (12.2% fewer tokens); on `SYNONYM_SUBSTITUTION`, MuRIL requires 8.43 tokens versus 9.15 tokens (7.9% fewer tokens).
3. **Subword Robustness on Synonyms**: In `SYNONYM_SUBSTITUTION` ($N=362$), 98.6% of canonical original targets tokenize as single subwords in MuRIL, and 92.8% remain single subwords after synonym substitution (a minor $-5.8\%$ shift). XLM-RoBERTa exhibits lower baseline coverage ($77.3\%$) and slightly higher fragmentation ($-9.1\%$).

### 5.2 Model Plausibility Scoring across Contexts, Synonyms, & Misspellings

Table 2 details descriptive statistics for length-normalized plausibility shifts ($\Delta \text{MeanLogP}$) across models and tracks ($N=1,679$).

| Model Checkpoint | Track Scope | $N$ Pairs | Mean $\Delta \text{MeanLogP}$ | Median $\Delta$ | SD | IQR | Min $\Delta$ | Max $\Delta$ | Original Preferred ($N$) | Original Preferred (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | `REALISTIC_SPELLING_ERROR` | 1,005 | **-0.8864** | -0.7752 | 1.2929 | 1.6561 | -6.4884 | +3.6106 | 768 | 76.4% |
| **XLM-RoBERTa** | `VALID_WORD_CONTEXT` | 312 | **-1.0831** | -0.9464 | 1.2195 | 1.4564 | -4.8362 | +1.6353 | 258 | 82.7% |
| **XLM-RoBERTa** | `SYNONYM_SUBSTITUTION` | 362 | **-0.0098** | -0.0084 | 1.0110 | 0.9386 | -4.6842 | +3.8360 | 183 | 50.6% |
| **MuRIL** | `REALISTIC_SPELLING_ERROR` | 1,005 | **-1.2045** | -0.8892 | 1.3526 | 1.7256 | -6.8610 | +2.3473 | 836 | **83.2%** |
| **MuRIL** | `VALID_WORD_CONTEXT` | 312 | **-1.8470** | -1.6755 | 1.3965 | 1.6648 | -5.9067 | +2.4179 | 294 | **94.2%** |
| **MuRIL** | `SYNONYM_SUBSTITUTION` | 362 | **-0.1787** | -0.1049 | 0.8545 | 0.8320 | -3.6843 | +2.0094 | 213 | **58.8%** |

*Table 2: Descriptive statistics of length-normalized plausibility shifts ($\Delta \text{MeanLogP}$) across experimental tracks on the primary benchmark ($N=1,679$). Source: `results/runs/scaleup_rerun/analysis/descriptive_statistics.csv`.*

Figure 1 illustrates the distribution of $\Delta \text{MeanLogP}$ across experimental tracks for both models.

![Distribution of Delta MeanLogP by Track](outputs/analysis/figures/fig1_delta_meanlp_by_track.png)  
*Figure 1: Boxplot distributions of signed length-normalized pseudo-log-likelihood deltas ($\Delta \text{MeanLogP}$) across experimental tracks for XLM-RoBERTa and MuRIL ($N=1,679$). Negative values indicate preference for the canonical original sentence.*

Figure 2 and Figure 3 depict the relationship between subword token inflation and plausibility shifts.

![Sentence Token Delta vs MeanLogP](outputs/analysis/figures/fig2_token_delta_vs_meanlp.png)  
*Figure 2: Scatter plot of full sentence token length changes ($\Delta \text{Tokens}$) versus plausibility shifts ($\Delta \text{MeanLogP}$) across all 3,358 model evaluation rows ($N=1,679$ pairs).*

![Target Token Delta vs MeanLogP](outputs/analysis/figures/fig3_target_token_delta_vs_meanlp.png)  
*Figure 3: Plausibility shifts ($\Delta \text{MeanLogP}$) plotted against the target word subword change ($\Delta \text{Target Tokens}$). Devanagari spelling errors consistently induce $\Delta \text{Target Tokens} \ge +1$.*

As established in Table 2 and Figures 1–3:
1. **Differential Spelling Error Penalization**: MuRIL penalizes Devanagari spelling errors substantially more heavily than XLM-RoBERTa. MuRIL assigns lower plausibility to the misspelled sentence in **83.2% (836/1,005)** of pairs (mean $\Delta = -1.2045$, median $=-0.8892$), whereas XLM-RoBERTa prefers the canonical sentence in **76.4% (768/1,005)** of pairs (mean $\Delta = -0.8864$, median $=-0.7752$).
2. **Contextual Sensitivity**: Both models exhibit sharp discrimination on contextual mismatches (`VALID_WORD_CONTEXT`), preferring the original in 94.2% of pairs in MuRIL (mean $\Delta = -1.8470$) and 82.7% of pairs in XLM-RoBERTa (mean $\Delta = -1.0831$).
3. **Synonym Interchangeability**: In `SYNONYM_SUBSTITUTION` ($N=362$), XLM-RoBERTa exhibits an average delta of just **$\Delta = -0.0098$** (original preferred in 50.6%), demonstrating that the multilingual generalist treats valid Hindi synonyms as near-interchangeable. MuRIL exhibits a modest penalty (mean $\Delta = -0.1787$, 58.8% preference), reflecting frequency distributions in its Indic training corpus.

### 5.3 Comparative Model Behavior: MuRIL vs. XLM-RoBERTa

Table 3 summarizes the cross-model agreement and rank correlations between XLM-RoBERTa and MuRIL on the primary benchmark ($N=1,679$).

| Track Scope | $N$ Pairs | Direction Both Negative | Direction Both Positive | XLM Neg / MuRIL Pos | XLM Pos / MuRIL Neg | Directional Agreement Rate (%) | Spearman $r_s$ ($\Delta \text{MeanLogP}$) | $p$-value ($r_s$) | 95% Confidence Interval |
|---|---|---|---|---|---|---|---|---|---|
| **ALL TRACKS** | 1,679 | 1,055 | 182 | 154 | 288 | **73.67%** | **+0.5496** | **$< 10^{-15}$** | $[+0.5153, +0.5821]$ |
| `VALID_WORD_CONTEXT` | 312 | 252 | 12 | 6 | 42 | **84.62%** | **+0.4590** | **$< 10^{-15}$** | $[+0.3666, +0.5424]$ |
| `REALISTIC_SPELLING_ERROR`| 1,005 | 677 | 78 | 91 | 159 | **75.12%** | **+0.5513** | **$< 10^{-15}$** | $[+0.5067, +0.5929]$ |
| `SYNONYM_SUBSTITUTION` | 362 | 126 | 92 | 57 | 87 | **60.22%** | **+0.2271** | **$1.3 \times 10^{-5}$** | $[+0.1269, +0.3226]$ |

*Table 3: Cross-model directional agreement and rank correlation on $\Delta \text{MeanLogP}$ between XLM-RoBERTa and MuRIL ($N=1,679$). Source: `results/runs/scaleup_rerun/analysis/model_comparison.csv`.*

Figure 4 and Figure 5 illustrate the cross-model scatter and directional agreement proportions.

![Cross-Model Plausibility Comparison](outputs/analysis/figures/fig4_model_comparison_scatter.png)  
*Figure 4: Cross-model scatter plot comparing $\Delta \text{MeanLogP}$ between XLM-RoBERTa ($x$-axis) and MuRIL ($y$-axis) across all 1,679 pairs. Overall rank correlation is $r_s = +0.5496, p < 10^{-15}$.*

![Directional Plausibility Agreement by Track](outputs/analysis/figures/fig5_direction_agreement.png)  
*Figure 5: Directional plausibility agreement rates between XLM-RoBERTa and MuRIL across experimental tracks ($N=1,679$).*

The cross-model analysis reveals:
1. **Global Concordance on Prominent Contrasts**: Across all 1,679 pairs, the models exhibit **73.67% directional agreement** and a statistically significant positive rank correlation (Spearman $r_s = +0.5496, p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$). Agreement is strongest on `VALID_WORD_CONTEXT` ($84.62\%$ agreement, $r_s = +0.4590$) and `REALISTIC_SPELLING_ERROR` ($75.12\%$ agreement, $r_s = +0.5513$).
2. **Decoupling on Synonyms**: In `SYNONYM_SUBSTITUTION` ($N=362$), directional agreement drops to $60.22\%$, and rank correlation weakens to $r_s = +0.2271$ ($p = 1.3 \times 10^{-5}$). When evaluating subtle lexical alternatives that preserve truth conditions, the models reflect idiosyncratic pretraining frequency priors.

### 5.4 Explanation Stability under Devanagari Spelling Noise

Table 4 reports visible-target explanation stability metrics for Attention and Integrated Gradients across all 1,005 scorable pairs, strict single-subword subsets, and multi-subword remainders.

| Model Checkpoint | Explanation Method | Evaluated Subset | Pair Count ($N$) | Stage 6 Masked $\rho$ | Stage 6 Masked Cosine | Visible Target Mean $\rho$ | Visible Target Median $\rho$ | Visible Target Mean Cosine | Visible Target Median Cosine |
|---|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | **Attention** | Pooled (All-Scorable) | 1,005 | 1.0000 | 1.0000 | **0.6258** | 0.7333 | **0.9353** | 0.9550 |
| **XLM-RoBERTa** | **Attention** | Strict Single-Subword | 52 | 1.0000 | 1.0000 | **0.6306** | 0.7746 | **0.9349** | 0.9598 |
| **XLM-RoBERTa** | **Attention** | Multi-Subword Remainder| 953 | 1.0000 | 1.0000 | **0.6255** | 0.7333 | **0.9353** | 0.9548 |
| **XLM-RoBERTa** | Integrated Gradients | Pooled (All-Scorable) | 1,005 | 1.0000 | 1.0000 | **0.3319** | 0.4000 | **0.8890** | 0.9204 |
| **XLM-RoBERTa** | Integrated Gradients | Strict Single-Subword | 52 | 1.0000 | 1.0000 | **0.4210** | 0.5442 | **0.9026** | 0.9313 |
| **XLM-RoBERTa** | Integrated Gradients | Multi-Subword Remainder| 953 | 1.0000 | 1.0000 | **0.3270** | 0.3929 | **0.8883** | 0.9199 |
| **MuRIL** | **Attention** | Pooled (All-Scorable) | 1,005 | 1.0000 | 1.0000 | **0.8027** | 0.8857 | **0.9518** | 0.9733 |
| **MuRIL** | **Attention** | Strict Single-Subword | 197 | 1.0000 | 1.0000 | **0.8053** | 0.9000 | **0.9725** | 0.9861 |
| **MuRIL** | **Attention** | Multi-Subword Remainder| 808 | 1.0000 | 1.0000 | **0.8021** | 0.8857 | **0.9468** | 0.9686 |
| **MuRIL** | Integrated Gradients | Pooled (All-Scorable) | 1,005 | 1.0000 | 1.0000 | **0.2560** | 0.3000 | **0.9818** | 0.9867 |
| **MuRIL** | Integrated Gradients | Strict Single-Subword | 197 | 1.0000 | 1.0000 | **0.3471** | 0.4000 | **0.9868** | 0.9885 |
| **MuRIL** | Integrated Gradients | Multi-Subword Remainder| 808 | 1.0000 | 1.0000 | **0.2337** | 0.2857 | **0.9805** | 0.9861 |

*Table 4: Visible-target explanation stability under authentic Devanagari spelling errors ($N=1,005$ pairs) versus the Stage 6 masked-target artifact. Source: `results/runs/scaleup_rerun/dashboard_data/stability_summary.csv`.*

Figure 6 illustrates the rank stability and vector cosine similarity comparisons.

![Explanation Stability Comparison](outputs/analysis/figures/fig6_explanation_stability.png)  
*Figure 6: Visible-target explanation stability under Devanagari spelling noise comparing Self-Attention and Layer Integrated Gradients across XLM-RoBERTa and MuRIL ($N=1,005$ pairs). (a) Rank stability (Spearman $\rho$). (b) Directional vector alignment (Cosine Similarity).*

Key findings from Table 4 and Figure 6 include:
1. **Attention Rank Stability Advantage**: Under the visible-target protocol, last-layer self-attention achieves **$1.9\times$ to $3.1\times$ higher rank stability** than Integrated Gradients:
   - In XLM-RoBERTa: Pooled Mean $\rho = 0.6258$ (Attention) vs. $0.3319$ (IG).
   - In MuRIL: Pooled Mean $\rho = 0.8027$ (Attention) vs. $0.2560$ (IG).
2. **Dissociation between Rank and Vector Stability in IG**: While Integrated Gradients exhibits low rank stability ($\rho \approx 0.26\text{--}0.33$), its **Cosine Similarity remains exceptionally high** ($0.8890$ in XLM-R; $0.9818$ in MuRIL). This demonstrates a fundamental geometric dissociation: the gradient attribution vector preserves its global trajectory in embedding space, but relative token rankings fluctuate under localized spelling noise.

### 5.5 Explanation Faithfulness under Discrete Context Erasure

Table 5 summarizes faithfulness evaluation across masking fractions $f \in \{0.10, 0.20, 0.30\}$ ($N=2,010$ evaluated sentences per model across 1,005 pairs).

| Model Checkpoint | Explanation Method | Evaluated Subset | Masking Fraction ($f$) | Mean Top Drop | Mean Bottom Drop (Control) | Mean Random Drop | Mean Faithfulness Gap | Median Faithfulness Gap | Win Rate vs. Bottom Control (%) | Win Rate vs. Random (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | **Attention** | All-Scorable ($N=2,010$) | 0.10 | -6.2969 | -8.7344 | -7.8968 | **+2.4374** | +1.6813 | **63.53%** | 52.49% |
| **XLM-RoBERTa** | **Attention** | All-Scorable ($N=2,010$) | 0.20 | -6.2915 | -9.0881 | -8.3099 | **+2.7966** | +2.2942 | **65.77%** | 55.92% |
| **XLM-RoBERTa** | **Attention** | All-Scorable ($N=2,010$) | 0.30 | -4.4711 | -8.2846 | -6.6174 | **+3.8134** | +3.0413 | **67.46%** | 57.46% |
| **XLM-RoBERTa** | **Attention** | Strict Single ($N=104$) | 0.20 | -1.5806 | -5.1870 | -3.9164 | **+3.6064** | +2.4584 | **69.23%** | 54.81% |
| **XLM-RoBERTa** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.10 | -6.9950 | -8.9797 | -7.8777 | **+1.9847** | +1.1131 | **59.75%** | 47.51% |
| **XLM-RoBERTa** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.20 | -7.0120 | -9.2597 | -8.0825 | **+2.2477** | +1.5954 | **62.24%** | 51.44% |
| **XLM-RoBERTa** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.30 | -4.7837 | -8.1795 | -6.7426 | **+3.3957** | +2.6586 | **65.12%** | 57.71% |
| **XLM-RoBERTa** | Integrated Gradients | Strict Single ($N=104$) | 0.20 | -2.2529 | -5.1072 | -3.6447 | **+2.8543** | +1.6744 | **64.42%** | 53.85% |
| **MuRIL** | **Attention** | All-Scorable ($N=2,010$) | 0.10 | -0.7615 | +1.2553 | +1.5249 | **-2.0168** | -2.5641 | **33.88%** | 28.41% |
| **MuRIL** | **Attention** | All-Scorable ($N=2,010$) | 0.20 | +0.8319 | +3.1532 | +3.1754 | **-2.3213** | -2.6750 | **35.42%** | 30.80% |
| **MuRIL** | **Attention** | All-Scorable ($N=2,010$) | 0.30 | +4.4916 | +4.0916 | +4.9273 | **+0.4001** | -0.1608 | **49.60%** | 42.34% |
| **MuRIL** | **Attention** | Strict Single ($N=394$) | 0.20 | +7.0699 | +8.2413 | +8.9152 | **-1.1714** | -1.9548 | **40.36%** | 34.26% |
| **MuRIL** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.10 | +1.3262 | +1.6260 | +1.8552 | **-0.2998** | -0.0241 | **49.90%** | 38.26% |
| **MuRIL** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.20 | +2.7479 | +3.2616 | +3.7076 | **-0.5137** | -0.2062 | **49.40%** | 40.15% |
| **MuRIL** | Integrated Gradients | All-Scorable ($N=2,010$) | 0.30 | +4.5079 | +5.5924 | +5.3210 | **-1.0845** | -0.7371 | **46.72%** | 42.29% |
| **MuRIL** | Integrated Gradients | Strict Single ($N=394$) | 0.20 | +7.9625 | +9.4844 | +9.5399 | **-1.5219** | -0.8808 | **47.46%** | 39.85% |

*Table 5: Faithfulness evaluation under discrete context token erasure ($N=2,010$ evaluated sentences per model across 1,005 spelling pairs). Source: `results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv`.*

Figure 7 plots the Faithfulness Gap and Win Rate trajectories across masking fractions.

![Faithfulness Interventions](outputs/analysis/figures/fig7_faithfulness_interventions.png)  
*Figure 7: Context token erasure faithfulness across masking fractions $f \in \{0.10, 0.20, 0.30\}$ ($N=2,010$ sentences per model). (a) Mean Faithfulness Gap ($\Delta S_{\text{top}} - \Delta S_{\text{bottom}}$). (b) Win Rate vs. Bottom-$k$ Control Erasure.*

The faithfulness results demonstrate:
1. **Attention Outperforms Integrated Gradients in XLM-RoBERTa**: In discrete masking tests on XLM-RoBERTa, last-layer self-attention achieves consistently positive Faithfulness Gaps ($+2.44$ to $+3.81$) and win rates of **$63.53\%\text{--}67.46\%$** against bottom control erasure.
2. **Integrated Gradients Operates Near or Below Chance**: In MuRIL, Integrated Gradients achieves win rates of only **$46.72\%\text{--}49.90\%$** (worse than or equal to chance), producing negative mean faithfulness gaps across all fractions ($-0.30$ to $-1.08$). In XLM-RoBERTa, IG achieves win rates of $59.75\%\text{--}65.12\%$, remaining below Attention.
3. **Out-of-Distribution Logit Dynamics in XLM-RoBERTa**: In XLM-RoBERTa, removing context tokens causes raw target logits to float higher globally, producing negative raw drops (e.g., at $f=0.20$, Top Drop $= -6.29$, Bottom Drop $= -9.09$). However, directional faithfulness is preserved because bottom control masking inflates logits even more, resulting in a strictly positive Faithfulness Gap ($(-6.29) - (-9.09) = \mathbf{+2.80} > 0$) with a **$65.77\%$ win rate**.

### 5.6 Relationship Between Explanation Stability and Faithfulness (RQ5)

Table 6 presents the correlation matrix between visible-target stability ($\rho$) and mean faithfulness gap ($f=0.20$) across the 1,005 Devanagari spelling pairs.

| Model Checkpoint | Explanation Method | Evaluated Subset | Sample Size ($N$) | Spearman Rank $r_s$ | $p$-value ($r_s$) | Pearson Linear $r$ | $p$-value ($r$) | Empirical Interpretation |
|---|---|---|---|---|---|---|---|---|
| **XLM-RoBERTa** | Attention | Pooled (All-Scorable) | 953 | **+0.0607** | $0.0612$ | +0.0564 | $0.0816$ | Non-Significant ($p > 0.05$) |
| **XLM-RoBERTa** | Attention | Strict Single-Subword | 52 | **+0.2472** | $0.0773$ | +0.2949 | $0.0338$ | Non-Significant Rank ($p > 0.05$) |
| **XLM-RoBERTa** | Integrated Gradients | Pooled (All-Scorable) | 953 | **+0.0632** | $0.0510$ | +0.0495 | $0.1270$ | Non-Significant ($p > 0.05$) |
| **XLM-RoBERTa** | Integrated Gradients | Strict Single-Subword | 52 | **+0.1647** | $0.2434$ | +0.1464 | $0.3005$ | Non-Significant ($p > 0.05$) |
| **MuRIL** | Attention | Pooled (All-Scorable) | 808 | **-0.0442** | $0.2099$ | -0.0790 | $0.0248$ | Weak Inverse Linear ($r < 0, p < 0.05$) |
| **MuRIL** | Attention | Strict Single-Subword | 197 | **-0.1924** | $0.0067$ | -0.1129 | $0.1141$ | Weak Inverse Rank ($r_s < 0, p < 0.01$) |
| **MuRIL** | Integrated Gradients | Pooled (All-Scorable) | 808 | **+0.0214** | $0.5442$ | +0.0290 | $0.4108$ | Non-Significant ($p > 0.05$) |
| **MuRIL** | Integrated Gradients | Strict Single-Subword | 197 | **+0.0344** | $0.6316$ | -0.0037 | $0.9592$ | Non-Significant ($p > 0.05$) |

*Table 6: Correlation analysis between explanation stability (visible-target Spearman $\rho$) and explanation faithfulness (mean gap at $f=0.20$) across Devanagari spelling pairs ($N=1,005$). Source: `results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv`.*

Figure 8 displays the stability–faithfulness scatter plots for both models.

![Stability vs Faithfulness Decoupling](outputs/analysis/figures/fig8_stability_vs_faithfulness.png)  
*Figure 8: Scatter plot of visible-target explanation stability (Spearman $\rho$, $x$-axis) versus mean faithfulness gap ($f=0.20$, $y$-axis) across Devanagari spelling pairs for (a) XLM-RoBERTa ($N=953$ scorable) and (b) MuRIL ($N=808$ scorable). Across evaluated models and methods, there is no consistent positive association between explanation stability and faithfulness.*

As shown in Table 6 and Figure 8:
1. **Absence of a Consistent Positive Association**: Across the eight evaluated model-method configurations, **there is no consistent positive association between explanation stability and explanation faithfulness**. In XLM-RoBERTa, rank correlations remain non-significant ($r_s = +0.0607, p = 0.0612$ for pooled Attention; $r_s = +0.0632, p = 0.0510$ for pooled IG; $r_s = +0.1647, p = 0.2434$ for strict IG). In the strict single-subword Attention condition for XLM-RoBERTa, while the rank correlation does not reach standard significance ($r_s = +0.2472, p = 0.0773$), the linear Pearson correlation exhibits a weak positive association ($r = +0.2949, p = 0.0338$ on $N=52$). For MuRIL Attention, we observe weak *negative* associations: in the pooled condition ($N=808$), the Pearson linear correlation is weakly negative and statistically significant ($r = -0.0790, p = 0.0248$, while $r_s = -0.0442, p = 0.2099$); in the strict single-subword condition ($N=197$), the Spearman rank correlation shows a statistically significant inverse relationship ($r_s = -0.1924, p = 0.0067$, with $r = -0.1129, p = 0.1141$). For MuRIL Integrated Gradients, both pooled ($r_s = +0.0214, p = 0.5442$) and strict ($r_s = +0.0344, p = 0.6316$) correlations are non-significant.
2. **Empirical and Statistical Perspective**: The expansion from 20 spelling pairs in the preliminary pilot to $N=1,005$ pairs ($N=953$ and $N=808$ scorable pairs) substantially improves statistical resolution, allowing us to evaluate stability–faithfulness dynamics with greater clarity. However, we do not claim that these empirical findings mathematically prove independence, establish causal isolation, or rule out all sample-size limitations across all neural network architectures. Rather, within the evaluated masked language models and Devanagari benchmark, the data demonstrate that attribution stability under spelling noise cannot be assumed to guarantee or predict causal explanation faithfulness.
3. **Core Conclusion (RQ5)**: In answer to RQ5, explanation stability under spelling noise does **not** serve as a reliable proxy for causal explanation faithfulness under feature erasure. The presence of weak negative associations for MuRIL Attention alongside non-significant relationships across other conditions indicates that stability and faithfulness evaluate distinct, non-concordant dimensions of model explanations.

---

## 6. Discussion

### 6.1 Distinct Metric Spaces: Evaluating Stability vs. Faithfulness
A central finding of this investigation is that explanation stability and explanation faithfulness evaluate distinct behavioral dimensions of neural explanations. In the XAI literature, researchers frequently treat stability as a quality metric, operating under the intuitive hypothesis that an explanation method that is unstable under minor noise cannot be trusted to identify true causal features \cite{alvarez-melis-jaakkola-2018-robustness,ding-koehn-2021-evaluating}.

Our empirical results across 1,005 Devanagari spelling pairs demonstrate that this assumption does not hold in practice. Stability and faithfulness inhabit distinct metric and conceptual spaces:
- **Stability** measures the local Lipschitz continuity of the explanation mapping $g(x)$ with respect to localized input variations $\delta$:
  $$\mathcal{S}(g; x, \delta) = \text{Sim}(g(x), g(x + \delta))$$
- **Faithfulness** measures whether the model's prediction function $f(x)$ exhibits a causal dependency on the subset of features $C_{\text{top}}$ prioritized by $g(x)$:
  $$\mathcal{F}(g; x, f) = f(x) - f(x_{\setminus C_{\text{top}}})$$

An explanation can achieve near-perfect stability by anchoring to invariant, static syntactic structures (e.g., punctuation, verbs, or common postpositions) that do not vary under local spelling perturbations; yet, erasing those tokens may have minimal impact on target word prediction, yielding an explanation that is **stably unfaithful**. Conversely, an attribution method may be sensitive to local noise (lower stability) while faithfully tracking the shifting internal representations that the model actually uses under each input state. Furthermore, the weak negative associations observed for MuRIL Attention suggest that in certain tokenizer representations, attributions that remain most invariant to surface noise may even mildly disfavor the most causally impactful tokens under discrete erasure. Therefore, **optimizing explainability pipelines solely for attribution stability risks selecting methods that fail to identify faithful model rationales**.

### 6.2 Discrete vs. Continuous Attribution Mechanisms: Why Integrated Gradients Fails under Discrete Erasure
A second striking finding is that last-layer self-attention attributions consistently achieve higher stability and discrete masking faithfulness than Layer Integrated Gradients in masked language models. This result appears paradoxical given that Integrated Gradients satisfies formal mathematical axioms (Completeness, Implementation Invariance) \cite{sundararajan-etal-2017-axiomatic}, whereas attention is a heuristic normalized weight matrix \cite{jain-wallace-2019-attention}.

The resolution lies in the fundamental incompatibility between **continuous path integrals** and **discrete token erasure in masked language models**:
1. Integrated Gradients accumulates gradients along a continuous straight-line interpolation in embedding space:
   $$\gamma(\alpha) = x' + \alpha(x - x'), \quad \alpha \in [0, 1]$$
   This path traverses unconstrained, non-discrete regions of $\mathbb{R}^{d}$ where the transformer was never trained to operate.
2. In contrast, evaluating faithfulness in MLMs requires a discrete substitution: replacing a content token with `[MASK]`. The masked language model prediction head is highly non-linear and discrete; erasing a token creates an abrupt shift in contextual conditioning rather than a smooth slide along an embedding vector.
3. Attention weights in the final transformer layer, although non-causal, directly govern the routing of contextual information into the target position's final hidden representation:
   $$h_{\text{target}}^{(L)} = \sum_{j} A_{\text{target}, j} \cdot V_j$$
   Because the MLM prediction head applies a linear projection directly to $h_{\text{target}}^{(L)}$, tokens receiving large attention weights contributed substantially to the pre-softmax representation at that layer. When those context tokens are replaced by `[MASK]`, that specific information flow is severed, producing the observed drop in target logit.

### 6.3 Devanagari Syllabic Vulnerability in NLP Tokenizers
Our subword tokenization findings highlight a structural failure mode in standard subword algorithms when applied to Indic abugida scripts. In Latin scripts, a minor typo such as `water` $\to$ `watar` typically results in a single character substitution that either preserves the subword token or splits it into two morpheme-like chunks. In Devanagari, swapping a matra (e.g., `पानी` $\to$ `पानि`) alters the Unicode codepoint sequence of the akshara, completely severing match compatibility with high-frequency vocabulary entries. As demonstrated in Table 1, single-subword coverage collapses by 55.9% to 71.6%, forcing the tokenizer into fine-grained character or byte fallback. This structural vulnerability explains why MuRIL, with its Indic-dedicated vocabulary, penalizes spelling errors far more decisively (83.2% preference rate) than XLM-RoBERTa (76.4% preference rate): MuRIL's vocabulary contains sharper, language-specific subword boundaries that register immediate disruption under syllabic alteration.

---

## 7. Extended Cohort Analysis & Linguistic Nuance

### 7.1 Orthographic Variants vs. True Spelling Errors
Across the 1,005 spelling pairs, linguistic analysis reveals a clear distinction between *true ungrammatical misspellings* and *legitimate orthographic variants*. For true spelling errors (e.g., `परीक्षा` $\to$ `परिक्षा`, `आवश्यक` $\to$ `आवशयक`), both models impose severe PLL penalties ($\Delta \text{MeanLogP} < -1.5$ in MuRIL). Conversely, for legitimate orthographic variants—such as anusvara vs. class nasal substitutions (`संभावना` vs. `सम्भावना`) or single vs. double ligature spelling (`महत्वपूर्ण` vs. `महत्त्वपूर्ण`)—both models exhibit minimal plausibility shifts ($\Delta \text{MeanLogP} > -0.20$). Pretrained MLMs distinguish between legitimate alternations present in Hindi corpora and erroneous non-standard deviations.

### 7.2 Secondary Template Sensitivity Benchmark ($N=1,957$)
To verify that our empirical findings are not idiosyncratic to specific sentence contexts, we evaluated the Secondary Template Sensitivity Benchmark ($N=1,957$ minimal pairs across 278 template frames). This benchmark contains the Primary Benchmark ($N=1,679$) plus 278 template-derived sentence variants. We explicitly emphasize that this is an expanded cohort designed to assess syntactic frame invariance across diverse sentence structures, and should not be interpreted as an independent dataset. The template cohort yielded highly consistent findings:
- On `REALISTIC_SPELLING_ERROR` ($N=1,260$): MuRIL prefers the original in $81.9\%$ of pairs (mean $\Delta = -1.0778$), and XLM-RoBERTa prefers the original in $70.8\%$ (mean $\Delta = -0.6941$).
- On `SYNONYM_SUBSTITUTION` ($N=385$): XLM-RoBERTa exhibits near-zero delta (mean $\Delta = -0.0026$), confirming synonym interchangeability.
- Cross-model directional agreement across all 1,957 template pairs is **71.28%** with a Spearman rank correlation of **$r_s = +0.5344$** ($p < 10^{-15}$, 95% CI $[0.5020, 0.5653]$), mirroring primary benchmark results ($73.67\%, r_s = +0.5496$).

### 7.3 Auxiliary Multiword Probe ($N=12$)
The auxiliary probe evaluated 12 challenging minimal pairs under the fine-grained 4-category taxonomy:
- **Gender/number agreement changes ($N=6$)**: Lexical substitution triggers grammatical agreement ripples in surrounding adjectives or verbs (e.g., `सैनिक ने साहस दिखाया` $\to$ `सैनिक ने वीरता दिखाई`). In these pairs, MuRIL assigns negative shifts ($\Delta = -0.5527$ on synonyms) tracking syntactic agreement.
- **Postpositional insertion ($N=1$)**: `दूर जाओ` $\to$ `फासले पर जाओ` requires inserting the case marker `पर`, altering syntactic frame geometry.
- **Collocational light-verb change ($N=1$)**: `भोजन करो` $\to$ `खाना खाओ` alters both noun and light verb collocations.
- **Repeated-target ambiguities ($N=4$)**: Sentences where the target token occurs multiple times (e.g., `डॉक्टर ने मरीज की जाँच की` $\to$ `... जाँच जी`), creating token alignment ambiguity. Both models exhibited lower directional agreement ($41.67\%$) on this probe, confirming that multiword ripples and repeated targets challenge standard attribution alignment.

### 7.4 Historical Pilot Reconciliation ($N=200$)
The preliminary pilot cohort ($N=200$, preserved in `results/runs/historical_pilot_200/`) served as the initial exploratory testbed. While the pilot established the preliminary trends (e.g., token collapse and absence of correlation), expanding to $N=1,679$ primary pairs and $N=1,005$ spelling pairs provided the necessary statistical power to confirm these phenomena definitively without ambiguity.

---

## 8. Limitations & Threats to Validity

To preserve scientific rigor, we outline five methodological limitations of this study:
1. **Sample Size and Generalizability Nuance**: The expansion from 20 spelling pairs in the pilot to $N=1,005$ pairs ($2,010$ sentences; $N=953$ and $N=808$ scorable pairs) provides substantial statistical power to examine weak effect sizes. However, our results represent empirical observations on the evaluated masked language models and Devanagari benchmark, rather than an exhaustive mathematical proof across all deep learning architectures. We do not claim to rule out all sample-size limitations, prove complete independence, or establish universal causal isolation; the weak negative associations observed for MuRIL Attention warrant further structural study.
2. **Out-of-Distribution (OOD) Syntactic Shock from Masking**: Replacing context tokens with `[MASK]` disrupts natural sentence syntax. As observed in XLM-RoBERTa (where unnormalized target logits increased after masking), logit shifts reflect a combination of semantic feature removal and global perplexity shock. While relative comparisons against bottom-k control masking preserve directional validity, absolute logit drops must be interpreted with caution.
3. **Multi-Subword Target Logit Aggregation**: Because spelling errors split target words into multiple subwords, we evaluated target predictions using the arithmetic mean logit across target subwords ($S = \frac{1}{k} \sum \text{Logit}$). While this uniform weighting preserves full sample size and tracks strict single-subword trends, it assumes equal contribution across constituent subword tokens.
4. **Attention is Not Counterfactual Causality**: Although self-attention demonstrated superior win rates in discrete context erasure, attention weights are correlation-routing mechanisms rather than formal counterfactual explanations. Attention's success under discrete masking reflects structural alignment with information flow in transformer layers, not a proof of causal necessity.
5. **Pretrained Checkpoint Scope**: Our experiments evaluated base-scale masked language models (`muril-base-cased` and `xlm-roberta-base`). Extrapolating these conclusions to decoder-only generative large language models (LLMs) requires future validation.

---

## 9. Ethical Considerations

This research investigates linguistic sensitivity and interpretability in Devanagari Hindi. The dataset was curated using standard linguistic examples and contains no personally identifiable information (PII), toxic language, or demographic bias. All human annotators were fairly compensated native Hindi speakers. The findings contribute to the development of more robust, transparent, and linguistically equitable NLP technologies for under-represented Indic language communities.

---

## 10. Conclusion and Future Work

In this paper, we conducted an empirical investigation into model behavior, subword tokenization, explanation stability, and explanation faithfulness under lexical perturbations in Devanagari Hindi (D-SAFE). By constructing a primary benchmark of $N=1,679$ minimal pairs ($3,358$ evaluations) and evaluating MuRIL and XLM-RoBERTa under a corrected visible-target protocol across $1,005$ spelling pairs, we demonstrated that:
1. Devanagari spelling errors cause severe target-word subword fragmentation ($-55.9\%$ collapse in XLM-RoBERTa, $-71.6\%$ in MuRIL).
2. MuRIL achieves higher tokenization compactness (10%–15%) and enforces substantially harsher plausibility penalties on orthographic errors than XLM-RoBERTa ($83.2\%$ vs. $76.4\%$), while cross-model correlation weakens on valid synonyms ($r_s = +0.2271$).
3. Last-layer self-attention exhibits $1.9\times$ to $3.1\times$ higher rank stability than Integrated Gradients under spelling noise, while Integrated Gradients preserves high vector cosine similarity ($0.8890\text{--}0.9818$).
4. Self-attention achieves superior faithfulness in discrete context erasure ($63.53\%\text{--}67.46\%$ win rate in XLM-RoBERTa), whereas Integrated Gradients operates near or below chance in MuRIL ($46.72\%\text{--}49.90\%$) due to path-integral mismatch with discrete MLM heads.
5. Crucially, in answer to RQ5, **there is no consistent positive association between explanation stability and faithfulness**. While weak negative associations occur for MuRIL Attention (pooled Pearson $r = -0.0790, p = 0.0248$; strict single-subword Spearman $\rho = -0.1924, p = 0.0067$), other combinations are non-significant, demonstrating that stability under spelling noise cannot be assumed to guarantee or predict causal explanation faithfulness.

Future work will expand this benchmark to other Indic scripts (e.g., Bengali, Tamil, Telugu), explore continuous embedding perturbation techniques, and extend this joint stability-faithfulness framework to modern decoder-only Indic LLMs.

---

## References

1. **Alvarez-Melis, D. and Jaakkola, T. S.** (2018). *On the Robustness of Interpretability Methods*. arXiv preprint arXiv:1806.08049.
2. **Atanasova, P., Simonsen, J. G., Lioma, C., and Augenstein, I.** (2020). *A Diagnostic Study of Explainability Techniques for Text Classification*. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 3256–3274.
3. **Bastings, J. and Filippova, K.** (2020). *The elephant in the interpretability room: Why use attention as explanation when we have saliency methods?*. In Proceedings of the Third BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP, pages 149–155.
4. **Bostrom, K. and Durrett, G.** (2020). *Byte Pair Encoding is Suboptimal for Language Model Pretraining*. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 4617–4624.
5. **Brunner, G., Liu, Y., Pascual, D., Richter, O., Ciaramita, M., and Wattenhofer, R.** (2020). *On Identifiability in Transformers*. In Proceedings of the 8th International Conference on Learning Representations (ICLR).
6. **Conneau, A., Khandelwal, K., Goyal, N., Chaudhary, V., Wenzek, G., Guzmán, F., Grave, E., Ott, M., Zettlemoyer, L., and Stoyanov, V.** (2020). *Unsupervised Cross-lingual Representation Learning at Scale*. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pages 8440–8451.
7. **Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K.** (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT), pages 4171–4186.
8. **DeYoung, J., Jain, S., Rajani, N. F., Lehman, E., Xiong, C., Socher, R., and Wallace, B. C.** (2020). *ERASER: A Benchmark to Evaluate Rationales in the English Language*. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pages 4443–4458.
9. **Ding, S. and Koehn, P.** (2021). *Evaluating Saliency Methods for Neural Machine Translation*. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (ACL-IJCNLP), pages 5034–5052.
10. **Dombrowski, A.-K., Alber, M., Anders, C., Ackermann, M., Müller, K.-R., and Kessel, P.** (2019). *Explanations can be manipulated and geometry is to blame*. In Advances in Neural Information Processing Systems (NeurIPS), volume 32, pages 13589–13600.
11. **Heo, J., Joo, S., and Moon, T.** (2019). *Fooling Neural Network Interpretations via Adversarial Model Manipulation*. In Advances in Neural Information Processing Systems (NeurIPS), volume 32, pages 2925–2936.
12. **Jacovi, A. and Goldberg, Y.** (2020). *Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness?*. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pages 4198–4205.
13. **Jain, S. and Wallace, B. C.** (2019). *Attention is not Explanation*. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT), pages 3543–3556.
14. **Kakwani, D., Khetan, A., Bhattacharyya, A., Ghadigaonkar, P., Sen, A., Shanbhag, A., and Bhattacharyya, P.** (2020). *IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indic Languages*. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 4948–4961.
15. **Khanuja, S., Bansal, D., Mehtani, S., Khapra, M. M., Kumar, P., Joshi, P., Raman, D., and Choudhury, M.** (2021). *MuRIL: Multilingual Representations for Indic Languages*. arXiv preprint arXiv:2103.10730.
16. **Kudo, T. and Richardson, J.** (2018). *SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing*. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP): System Demonstrations, pages 66–71.
17. **Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., and Stoyanov, V.** (2019). *RoBERTa: A Robustly Optimized BERT Pretraining Approach*. arXiv preprint arXiv:1907.11692.
18. **Rust, P., Pfeiffer, J., Vulić, I., Ruder, S., and Gurevych, I.** (2021). *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (ACL-IJCNLP), pages 3118–3135.
19. **Salazar, J., Liang, D., Nguyen, T. Q., and Kirchhoff, K.** (2020). *Masked Language Model Scoring*. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pages 2699–2712.
20. **Sennrich, R., Haddow, B., and Birch, A.** (2016). *Neural Machine Translation of Rare Words with Subword Units*. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (ACL), pages 1715–1725.
21. **Serrano, S. and Smith, N. A.** (2019). *Is Attention Interpretable?*. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL), pages 2931–2951.
22. **Sundararajan, M., Taly, A., and Yan, Q.** (2017). *Axiomatic Attribution for Deep Networks*. In Proceedings of the 34th International Conference on Machine Learning (ICML), volume 70 of PMLR, pages 3319–3328.
23. **Wiegreffe, S. and Pinter, Y.** (2019). *Attention is not not Explanation*. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 11–20.

---

## Appendix: Supplementary Implementation Details

### A. Mathematical Formulation Summary
- **Sentence Pseudo-Log-Likelihood (PLL)**:
  $$\text{PLL}(W) = \sum_{t=1}^{|W|} \log P(w_t \mid W_{\setminus t}; \Theta)$$
- **Length-Normalized MeanLogP**:
  $$\text{MeanLogP}(W) = \frac{\text{PLL}(W)}{|W_{\text{scorable}}|}$$
- **Signed Plausibility Shift ($\Delta \text{MeanLogP}$)**:
  $$\Delta \text{MeanLogP} = \text{MeanLogP}(W_{\text{cont}}) - \text{MeanLogP}(W_{\text{orig}})$$
- **Visible-Target Multi-Subword Target Score**:
  $$S(X; Y_{\text{target}}) = \frac{1}{|T|} \sum_{j \in T} \text{Logit}(p_j, y_j)$$
- **Faithfulness Gap ($f$)**:
  $$\text{Faithfulness Gap} = \Delta S_{\text{top}} - \Delta S_{\text{bottom}} = S_{\text{bottom}} - S_{\text{top}}$$

### B. Computational Hardware, Resource Consumption, and Provenance
All scale-up experiments were executed on an **NVIDIA GeForce RTX 3050 6GB Laptop GPU** running under Windows 11 with CUDA 12.6, PyTorch 2.14.1+cu126, batch size 32, and `transformers` 4.57.6.
- **Computational Provenance**:
  - Stages 1 and 2 were freshly computed during `task-340` (7.41s and 200.23s) and validated during recovery in `task-376` (0.17s and 0.18s).
  - Stages 3 through 9 were freshly recomputed during `task-376` with eager attention implementation (`attn_implementation="eager"`).
  - Total end-to-end execution runtime: 29.68 minutes on GPU.
- Zero stages were reused from the older historical pilot run or unverified baseline files.
