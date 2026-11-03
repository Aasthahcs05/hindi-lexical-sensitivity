# Hindi Lexical Sensitivity — Research Notebook Suite

This directory contains the complete, step-by-step Jupyter Notebook suite for the **Hindi Lexical Sensitivity & Explainability Research Project**.

Each notebook is designed as a self-contained, publication-grade research stage following modern ML/NLP engineering standards, complete with mathematical derivations, Devanagari script linguistics, interactive demonstrations, and empirical validations.

---

## Notebook Index & Learning Progression

| # | Notebook | Research Stage | Primary Focus & Methods |
|---|---|---|---|
| **01** | [01_dataset_curation_and_validation.ipynb](01_dataset_curation_and_validation.ipynb) | Stage 1: Data Engineering | Cryptographic SHA-256 validation, Devanagari Unicode integrity (`U+0900`–`U+097F`), orthographic taxonomy, and non-destructive human review preservation. |
| **02** | [02_subword_tokenization_and_alignment.ipynb](02_subword_tokenization_and_alignment.ipynb) | Stage 2: Subword Tokenization | SentencePiece BPE (XLM-RoBERTa) vs WordPiece (MuRIL), character offset alignment, and the **Devanagari Subword Collapse** under spelling errors. |
| **03** | [03_mlm_pseudo_log_likelihood_scoring.ipynb](03_mlm_pseudo_log_likelihood_scoring.ipynb) | Stage 3: Model Scoring | Bidirectional Pseudo-Log-Likelihood (PLL) derivation, length normalization ($	ext{MeanLogP}$), cross-model guardrails, and 8 GB RAM memory-safe batching. |
| **04** | [04_tokenization_vs_model_plausibility.ipynb](04_tokenization_vs_model_plausibility.ipynb) | Stage 4: Combined Statistics | Tidy dataset merging, non-parametric Spearman correlations with Benjamini-Hochberg FDR control, and cross-model concordance (74.5% sign agreement). |
| **05** | [05_explainability_attention_vs_integrated_gradients.ipynb](05_explainability_attention_vs_integrated_gradients.ipynb) | Stage 5: Explainability | Multi-Head Attention Rollup vs Integrated Gradients (IG), Devanagari word-level aggregation, and the continuous-discrete embedding mismatch. |
| **06** | [06_explanation_stability_and_faithfulness.ipynb](06_explanation_stability_and_faithfulness.ipynb) | Stages 6 & 7: Core Scientific Study | Resolution of the Stage 6 Masked-Target Artifact (Visible-Target Scoring), Top-$k$ vs Bottom-$k$ erasure interventions, and testing the **orthogonality of Stability and Faithfulness** ($p > 0.05$). |
| **07** | [07_paper_synthesis_and_dashboard_integration.ipynb](07_paper_synthesis_and_dashboard_integration.ipynb) | Stage 8: Synthesis & Deployment | Master publication figure generation, practical guidelines for Devanagari NLP, and data packaging for the interactive React/Vite dashboard. |

---

## Environment & Execution Guidelines

### 1. Environment Setup
Activate the project's virtual environment:
```bash
# On Windows:
.venv\Scripts\activate

# On Linux / macOS:
source .venv/bin/activate
```

Verify that all dependencies and editable project packages are present:
```bash
python -c "import torch, transformers, pandas, matplotlib; print('Environment verified!')"
```

### 2. Fast Execution vs. Live Retraining
Every notebook is engineered to:
- **Execute instantly**: Load verified precomputed results from `outputs/` so all statistical figures, correlation tables, and audit logs render in seconds without needing hours of CPU compute.
- **Run interactively**: Provide standalone live functions and sample sentence demonstrations so you can test custom Hindi sentences on live models.

### 3. Hardware Requirements
- **RAM**: 8 GB minimum (memory management with explicit garbage collection is implemented throughout).
- **Compute**: PyTorch CPU-only or CUDA GPU.
- **OS**: Windows 11, Linux, or macOS.

---

## Scientific Principles & Guardrails
1. **Preserve the Original Data**: Human annotations and rejected rows are strictly retained and transparently tagged.
2. **Never Compare Raw PLL Across Vocabularies**: Always use within-model signed differences ($\Delta$) and length-normalized $	ext{MeanLogP}$.
3. **Correlation $
eq$ Causation**: Subword fragmentation and likelihood penalties are co-effects of vocabulary coverage, not mechanical determinants.
4. **Stability $
eq$ Faithfulness**: Explanation stability under Devanagari spelling noise is orthogonal to attribution faithfulness.
