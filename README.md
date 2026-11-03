# Hindi Lexical Sensitivity Research System

## Research objective

Study how contextual lexical contrasts, synonym substitutions, and realistic spelling errors in Hindi Devanagari affect subword tokenization and pretrained masked-language-model behavior.

## Research principles

- Preserve the original dataset.
- Never silently modify human annotations.
- Keep processed data and experiment outputs separate.
- Record experiment configurations and software versions.
- Do not interpret language-model scores as direct measures of grammatical correctness.
- Do not report results until experiments have actually run.

## Setup & Installation

### 1. Python Environment Setup
Recommended: Python 3.10 to 3.12.

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> **Note on PyTorch**: If your teammate has an NVIDIA GPU and wants CUDA acceleration, install CUDA-enabled PyTorch first from [pytorch.org](https://pytorch.org) (e.g. `pip install torch --index-url https://download.pytorch.org/whl/cu121`), then run `pip install -r requirements.txt`.

### 2. Verify Installation
Run the test suite to ensure all components and models work as expected:
```bash
pytest
```

### 3. Step-by-Step Research Notebooks (ML Workflow)
The complete end-to-end research methodology is organized as clean, publication-grade Jupyter Notebooks in [`notebooks/`](notebooks/):

1. **[`01_dataset_curation_and_validation.ipynb`](notebooks/01_dataset_curation_and_validation.ipynb)**: Cryptographic SHA-256 verification, Devanagari script integrity (`U+0900`–`U+097F`), orthographic error taxonomy, and non-destructive human review preservation.
2. **[`02_subword_tokenization_and_alignment.ipynb`](notebooks/02_subword_tokenization_and_alignment.ipynb)**: SentencePiece BPE (XLM-RoBERTa) vs WordPiece (MuRIL), character offset alignment, and the Devanagari subword collapse under spelling errors.
3. **[`03_mlm_pseudo_log_likelihood_scoring.ipynb`](notebooks/03_mlm_pseudo_log_likelihood_scoring.ipynb)**: Masked language model Pseudo-Log-Likelihood (PLL) derivation, length normalization ($\text{MeanLogP}$), and 8 GB RAM memory-safe batching.
4. **[`04_tokenization_vs_model_plausibility.ipynb`](notebooks/04_tokenization_vs_model_plausibility.ipynb)**: Non-parametric Spearman correlation with Benjamini–Hochberg FDR control and cross-model concordance (74.5% directional agreement).
5. **[`05_explainability_attention_vs_integrated_gradients.ipynb`](notebooks/05_explainability_attention_vs_integrated_gradients.ipynb)**: Multi-Head Attention Rollup vs Integrated Gradients (IG), Devanagari attribution heatmaps, and continuous-discrete domain mismatch.
6. **[`06_explanation_stability_and_faithfulness.ipynb`](notebooks/06_explanation_stability_and_faithfulness.ipynb)**: Resolution of the Stage 6 Masked-Target Artifact (Visible-Target Scoring), Top-$k$ vs Bottom-$k$ erasure interventions, and testing the orthogonality of Stability and Faithfulness ($p > 0.05$).
7. **[`07_paper_synthesis_and_dashboard_integration.ipynb`](notebooks/07_paper_synthesis_and_dashboard_integration.ipynb)**: Master publication figures, practical guidelines for Devanagari NLP, and production data packaging for the React dashboard.

See [`notebooks/README.md`](notebooks/README.md) for full execution guidelines.

### 4. Interactive Dashboard (Optional)
The project includes a React/Vite visualization dashboard:
```bash
cd dashboard
npm install
npm run dev
```

