# Reproducibility Guide & Experimental Configuration

This document specifies the exact software dependencies, hardware environment, random seeds, hyperparameter configurations, dataset hashes, and mathematical definitions necessary to reproduce every experimental result presented in *"Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi"*.

---

## 1. Computing Environment & Dependency Versions

All scale-up experiments were executed on an NVIDIA GPU workstation with CUDA acceleration and batching:

- **Operating System**: Windows 11 Enterprise / Pro (x86_64)
- **GPU Accelerator**: NVIDIA GeForce RTX 3050 6GB Laptop GPU
- **CUDA Version**: 12.6
- **Host Memory**: 8 GB RAM
- **Python Version**: Python 3.12+ / 3.13
- **Key Python Packages**:
  - `torch == 2.14.1+cu126`
  - `transformers == 4.57.6`
  - `tokenizers == 0.22.2`
  - `captum == 0.9.0`
  - `scipy == 1.16.0 / 1.18.1`
  - `numpy >= 1.26.0`
  - `pandas >= 2.2.0`
  - `openpyxl == 3.1.5`
  - `matplotlib == 3.11.2`
  - `python-docx == 1.2.0`
  - `reportlab == 5.1.0`

---

## 2. Dataset Specifications & Integrity Verification

The experimental pipeline utilizes four distinct frozen datasets derived from an audited reconciliation of 2,000 raw candidate rows:

1. **Primary Benchmark (`data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv`)**:
   - **Row Count**: Exactly 1,679 minimal sentence pairs ($3,358$ individual evaluations).
   - **Track Breakdown**:
     - `VALID_WORD_CONTEXT`: 312 pairs (18.58%)
     - `SYNONYM_SUBSTITUTION`: 362 pairs (21.56%)
     - `REALISTIC_SPELLING_ERROR`: 1,005 pairs (59.86%)
   - **Quality**: Triple-annotated and adjudicated gold standard. 100% Devanagari script integrity.

2. **Template Sensitivity Benchmark (`data/final/TEMPLATE_SENSITIVITY_BENCHMARK.csv`)**:
   - **Row Count**: Exactly 1,957 minimal sentence pairs ($3,914$ evaluations).
   - **Track Breakdown**:
     - `VALID_WORD_CONTEXT`: 312 pairs
     - `SYNONYM_SUBSTITUTION`: 385 pairs
     - `REALISTIC_SPELLING_ERROR`: 1,260 pairs
   - **Purpose**: Evaluates frame-level syntactic sensitivity across 278 template frames.

3. **Auxiliary Multiword Probe (`data/final/AUXILIARY_MULTIWORD_PROBE.csv`)**:
   - **Row Count**: Exactly 12 minimal sentence pairs ($24$ evaluations).
   - **Linguistic Taxonomy**:
     - 6 gender/number agreement changes
     - 1 postpositional insertion
     - 1 collocational light-verb change
     - 4 repeated-target ambiguities
   - **Purpose**: Evaluates multiword ripple effects and token alignment edge cases.

4. **Historical Pilot Cohort (`results/runs/historical_pilot_200/`)**:
   - **Row Count**: Exactly 200 minimal sentence pairs ($400$ evaluations).
   - **Purpose**: Retained intact for archival provenance and historical pilot comparisons.

---

## 3. Pretrained Model Checkpoints & Tokenizer Settings

| Parameter | XLM-RoBERTa (`FacebookAI/xlm-roberta-base`) | MuRIL (`google/muril-base-cased`) |
|---|---|---|
| **Architecture** | RoBERTa-base (Bidirectional Encoder) | BERT-base (Bidirectional Encoder) |
| **Number of Layers** | 12 | 12 |
| **Attention Heads** | 12 | 12 |
| **Hidden Dimension** | 768 | 768 |
| **Total Parameters** | ~278 Million | ~236 Million |
| **Vocabulary Size** | 250,002 | 197,285 |
| **Tokenizer Type** | SentencePiece BPE (Unigram) | WordPiece |
| **Language Coverage** | 100+ languages (global crawl) | 17 Indic languages + English |
| **Mask Token** | `<mask>` (ID: 250001) | `[MASK]` (ID: 103) |
| **Pad Token** | `<pad>` (ID: 1) | `[PAD]` (ID: 0) |
| **BOS / EOS Tokens** | `<s>` / `</s>` | `[CLS]` / `[SEP]` |
| **Attention Implementation** | `attn_implementation="eager"` | `attn_implementation="eager"` |

---

## 4. Scoring Formulations & Protocols

### Pseudo-Log-Likelihood (PLL)
For a sentence $W = (w_1, w_2, \dots, w_{|W|})$, the PLL is computed via iterative single-token masking across all non-special tokens:
$$\text{PLL}(W) = \sum_{t=1}^{|W|} \log P(w_t \mid W_{\setminus t}; \Theta)$$
where $W_{\setminus t}$ denotes the sequence with token $w_t$ replaced by the model's mask token.

### Length-Normalized MeanLogP
To control for sentence length variations:
$$\text{MeanLogP}(W) = \frac{\text{PLL}(W)}{|W_{\text{scorable}}|}$$
where $|W_{\text{scorable}}|$ is the number of scored tokens (excluding special framing tokens).

### Signed Delta Convention
$$\Delta \text{MeanLogP} = \text{MeanLogP}(W_{\text{contrast}}) - \text{MeanLogP}(W_{\text{original}})$$
- $\Delta \text{MeanLogP} < 0$: The original sentence is assigned higher plausibility by the model.
- $\Delta \text{MeanLogP} > 0$: The contrast sentence is assigned higher plausibility.

---

## 5. Explainability Framework & Protocols

### Last-Layer Self-Attention Attribution
- **Extracted Layer**: Layer 11 (the 12th and final transformer layer).
- **Head Aggregation**: Arithmetic mean across all 12 attention heads:
  $$A_{i,j} = \frac{1}{12} \sum_{h=1}^{12} A^{(11, h)}_{i,j}$$
- **Context Importance Vector**: Mean attention weight directed from the target position(s) $T$ to each context token $j \notin T$:
  $$\alpha_j = \frac{1}{|T|} \sum_{t \in T} A_{t, j}$$
  Special tokens (`[CLS]`, `[SEP]`, `<s>`, `</s>`, padding) are excluded and attributions are normalized to sum to 1 over context tokens.

### Layer Integrated Gradients (Captum)
- **Target Layer**: Word embedding layer (`embeddings.word_embeddings`).
- **Baseline**: Zero vector in embedding space ($x' = \mathbf{0}$).
- **Approximation**: Gauss-Legendre quadrature with $m = 50$ interpolation steps.
- **Attribution Calculation**:
  $$\text{IG}_i(x) = (x_i - x'_i) \times \int_{0}^1 \frac{\partial F(x' + \alpha(x - x'))}{\partial x_i} d\alpha$$
  Subword scalar importance is obtained via the Euclidean $L_2$-norm over the embedding dimension ($d=768$), followed by context-level normalization.

### Visible-Target Protocol vs. Masked-Target Artifact
- **Stage 6 Artifact**: When the target token was masked with `[MASK]` in both original and contrast inputs, the inputs became identical ($X_{\text{orig}} \equiv X_{\text{cont}}$), yielding $\rho = 1.000$ trivially.
- **Stage 7 Visible-Target Protocol**: Target tokens remain visible in the input sequence. The target score is defined as the mean unnormalized logit of target subwords:
  $$S(X; Y_{\text{target}}) = \frac{1}{|T|} \sum_{j \in T} \text{Logit}(p_j, y_j)$$
  Attribution stability is evaluated across aligned context tokens between original and contrast sentences.

---

## 6. Faithfulness Evaluation Protocol

### Discrete Token Erasure
Context tokens are ranked by importance:
- **Top-$k$ Erasure**: Mask the top $k = \lceil f \cdot |C| \rceil$ tokens with `[MASK]`.
- **Bottom-$k$ Erasure (Control)**: Mask the bottom $k$ tokens.
- **Random-$k$ Erasure**: Mask $k$ tokens selected uniformly at random (averaged over 5 runs).
- **Fractions Evaluated**: $f \in \{0.10, 0.20, 0.30\}$.
- **Evaluated Cohort**: All $N=2,010$ sentences ($1,005$ original $+ 1,005$ contrast) across the primary spelling track.

### Metrics
1. **Target Logit Drop**:
   $$\Delta S_{\text{intervention}} = S(X; Y) - S(X_{\text{masked}}; Y)$$
2. **Faithfulness Gap**:
   $$\text{Faithfulness Gap} = \Delta S_{\text{top}} - \Delta S_{\text{bottom}}$$
3. **Win Rate vs. Bottom Control**:
   $$\text{Win Rate} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\Delta S_{\text{top}, i} > \Delta S_{\text{bottom}, i})$$

---

## 7. Statistical Testing & Significance Thresholds

- **Rank Correlation**: Spearman rank correlation ($r_s$) computed using `scipy.stats.spearmanr`.
- **Linear Correlation**: Pearson correlation ($r$) computed using `scipy.stats.pearsonr`.
- **Significance Level**: $\alpha = 0.05$.
- **Multiple Hypothesis Testing Correction**: Benjamini–Hochberg False Discovery Rate (FDR) applied across exploratory tokenization-scoring correlation batches.
- **Confidence Intervals**: 95% Fisher $z$-transformed confidence intervals for correlation coefficients.

---

## 8. Authoritative Run Directory

All verified results, CSVs, figures, and manifests for the expanded experiments are located in:
`results/runs/scaleup_rerun/`

Document and artifact generation:
```bash
python scripts/build_paper_documents.py
python scripts/build_excel_workbook.py
```
generates `paper/research_paper.docx`, `paper/research_paper.pdf`, and `paper/expanded_experimental_results.xlsx`, mirroring them to `research_paper/`.
