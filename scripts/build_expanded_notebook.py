"""
Script: build_expanded_notebook.py
Purpose: Generates and executes the teacher-ready Jupyter notebook:
         notebooks/expanded_experimental_results.ipynb
         using verified outputs from results/runs/scaleup_rerun/
"""

import os
import sys
import nbformat as nbf
from nbclient import NotebookClient

def create_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.12.0"
        }
    }

    cells = []

    # -------------------------------------------------------------
    # TITLE & HEADER
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""# Beyond Tokenization: Investigating Model Behaviour, Explanation Stability, and Faithfulness under Lexical Perturbations in Devanagari Hindi
## Comprehensive Teacher-Facing Notebook for Expanded Scale-Up Experiments

**Authors**: Anonymous Author(s)  
**Academic Status**: Under Review for Publication  
**Authoritative Run Source**: `results/runs/scaleup_rerun/`  
**Target Audience**: Teachers, Advisors, Research Evaluators, and Students in NLP / Computational Linguistics  

---

### Executive Overview & Pedagogical Roadmap

This Jupyter Notebook presents the empirical results, statistical analyses, and linguistic findings of the expanded **Hindi Lexical Sensitivity** scale-up study. The notebook is structured to facilitate evaluation by instructors and researchers, allowing verification of every table, figure, and correlation directly from frozen dataset files and precomputed experimental outputs.

#### Core Pedagogical Sections:
1. **Section 1: Research Overview** — Problem statement, 5 Research Questions (RQ1–RQ5), frozen model checkpoints, and experimental pipeline.
2. **Section 2: Dataset & Experimental Cohorts** — Distinction of the 4 cohorts (Primary $N=1,679$, Template $N=1,957$, Auxiliary $N=12$, Historical Pilot $N=200$).
3. **Section 3: Tokenization and Fragmentation** — Subword segmentation dynamics, matra/ligature disruptions, and the Devanagari subword collapse (Table 1; Figures 2 & 3).
4. **Section 4: Pseudo-Log-Likelihood (PLL) Scoring** — Length-normalized plausibility shifts ($\Delta \\text{MeanLogP}$), preference rates, and track comparisons (Table 2; Figure 1).
5. **Section 5: Cross-Model Comparison** — Concordance, directional agreement, and Spearman rank correlations between MuRIL and XLM-RoBERTa (Table 3; Figures 4 & 5).
6. **Section 6: Explanation Stability** — Resolving the Stage 6 Masked-Target Artifact via the Stage 7 Visible-Target Protocol; Attention vs. Integrated Gradients (Table 4; Figure 6).
7. **Section 7: Explanation Faithfulness via Context Erasure** — Causal feature erasure ($f \in \\{0.10, 0.20, 0.30\\}$), faithfulness gaps, and win rates (Table 5; Figure 7).
8. **Section 8: Stability–Faithfulness Relationship** — Testing the core hypothesis of metric orthogonality ($p > 0.05$) across 1,005 spelling pairs (Table 6; Figure 8).
9. **Section 9: Template Sensitivity Analysis** — Syntactic frame invariance across 278 template frames ($N=1,957$).
10. **Section 10: Auxiliary Multiword Probe** — Fine-grained 4-category analysis of multiword ripples and token alignment edge cases ($N=12$).
11. **Section 11: Overall Findings and Limitations** — Pedagogical synthesis of findings and methodological limitations.
"""))

    # -------------------------------------------------------------
    # SETUP CODE CELL
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_code_cell("""# Environment Setup & Working Directory Normalization
import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from IPython.display import display, Image, HTML

# Ensure working directory is the project root
if os.path.basename(os.getcwd()) == 'notebooks':
    os.chdir('..')

print("=" * 70)
print(f"Working Directory : {os.getcwd()}")
print(f"Python Executable : {sys.executable}")
print(f"Pandas Version    : {pd.__version__}")
print(f"Scipy Version     : {stats.__file__}")
print("=" * 70)

# Display settings for clear teacher evaluation
pd.set_option('display.max_columns', 25)
pd.set_option('display.max_rows', 50)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: f'{x:.4f}' if isinstance(x, float) else str(x))
"""))

    # -------------------------------------------------------------
    # SECTION 1: RESEARCH OVERVIEW
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 1: Research Overview

### 1.1 Research Objective
The goal of this research is to systematically investigate how lexical perturbations in **Devanagari Hindi** affect:
1. **Subword tokenization dynamics** across differing tokenization algorithms (WordPiece vs. SentencePiece BPE).
2. **Model plausibility scoring** under bidirectional pseudo-log-likelihood (PLL).
3. **Explanation stability** under authentic orthographic noise.
4. **Explanation faithfulness** under discrete causal feature erasure.
5. The empirical relationship between **stability** and **faithfulness**.

### 1.2 The Five Core Research Questions (RQs)
As formalized in the research manuscript, this study addresses five specific questions:
- **RQ1**: How do contextual lexical contrasts, synonym substitutions, and spelling perturbations affect subword tokenization and model scoring in Devanagari Hindi?
- **RQ2**: How do MuRIL (an Indic-dedicated MLM) and XLM-RoBERTa (a global multilingual generalist) differ in their representations of and scoring responses to these perturbations?
- **RQ3**: How stable are Attention and Integrated Gradients explanations when evaluated under authentic Devanagari spelling perturbations?
- **RQ4**: How do Attention and Integrated Gradients behave under discrete context-token masking interventions in masked language models?
- **RQ5**: Is explanation stability under input noise statistically associated with measured explanation faithfulness under feature erasure?

### 1.3 Pretrained Models (Strictly Frozen Pretrained MLMs)
We evaluate two widely used transformer architectures without fine-tuning or retraining:
1. **MuRIL (`google/muril-base-cased`)**:
   - 12 layers, 12 heads, 768 hidden dimensions (~236M parameters).
   - Pretrained on 17 Indic languages + English using a 197,285-token **WordPiece** vocabulary.
2. **XLM-RoBERTa (`FacebookAI/xlm-roberta-base`)**:
   - 12 layers, 12 heads, 768 hidden dimensions (~278M parameters).
   - Pretrained on 2.5TB Common Crawl across 100+ languages using a 250,002-token **SentencePiece BPE** vocabulary.

> **Methodological Note on Frozen Models**: Both models are evaluated strictly as frozen masked language models. No fine-tuning or parameter updates were applied, isolating the intrinsic linguistic and representational behaviors instilled during pretraining.

### 1.4 Experimental Pipeline
```
[Minimal Sentence Pairs]
           │
           ├───────────────────────────────┐
           ▼                               ▼
 [Subword Tokenization]          [Pseudo-Log-Likelihood]
 - WordPiece vs. BPE             - Length-Normalized MeanLogP
 - Target Fragmentation          - Signed Plausibility Shifts
           │                               │
           └───────────────┬───────────────┘
                           ▼
          [Feature Attribution Analysis]
          - Last-Layer Multi-Head Attention
          - Layer Integrated Gradients (20 steps)
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
 [Visible-Target Stability]      [Context Erasure Faithfulness]
 - Spearman Rank (ρ)             - Top-k vs. Bottom-k vs. Random-k
 - Cosine Similarity             - Erasure budgets: 10%, 20%, 30%
           │                               │
           └───────────────┬───────────────┘
                           ▼
          [Joint Stability-Faithfulness Evaluation]
          - Spearman & Pearson Correlation Matrix
          - Stability vs. Faithfulness (RQ5)
```
"""))

    # -------------------------------------------------------------
    # SECTION 2: DATASET & EXPERIMENTAL COHORTS
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 2: Dataset and Experimental Cohorts

### 2.1 The Four Distinct Cohorts
To prevent data contamination and ensure clear scientific interpretation, the research project partitions data into four distinct cohorts:

1. **Primary Benchmark ($N = 1,679$ minimal pairs / $3,358$ evaluations)**:
   - Gold-standard, fully audited minimal sentence pairs across three controlled tracks.
   - Evaluated across all nine computational stages (Tokenization, PLL Scoring, Stability, Faithfulness, Correlations).
2. **Secondary Template Sensitivity Benchmark ($N = 1,957$ minimal pairs / $3,914$ evaluations)**:
   - Incorporates the primary benchmark plus 278 template frames (`VALID_WORD_CONTEXT`: 312, `SYNONYM_SUBSTITUTION`: 385, `REALISTIC_SPELLING_ERROR`: 1,260).
   - Designed to evaluate whether plausibility shifts are invariant across different syntactic templates.
   - **Crucial Note**: The template sensitivity benchmark is an extension of the primary benchmark, **not** an independent statistical sample.
3. **Auxiliary Multiword Probe ($N = 12$ minimal pairs / $24$ evaluations)**:
   - Curated to investigate multiword lexical substitutions and alignment edge cases.
   - Classified under a fine-grained 4-category taxonomy (6 agreement, 1 postposition, 1 light verb, 4 ambiguity).
4. **Historical Preliminary Pilot ($N = 200$ minimal pairs / $400$ evaluations)**:
   - The initial exploratory pilot preserved in `results/runs/historical_pilot_200/` for archival tracking.

Let us load the authoritative dataset CSV files and inspect their actual distributions.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load and verify the dataset files
primary_df = pd.read_csv('data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv')
template_df = pd.read_csv('data/final/TEMPLATE_SENSITIVITY_BENCHMARK.csv')
auxiliary_df = pd.read_csv('data/final/AUXILIARY_MULTIWORD_PROBE.csv')

print(f"Primary Benchmark Rows   : {len(primary_df):,}")
print(f"Template Benchmark Rows  : {len(template_df):,}")
print(f"Auxiliary Probe Rows     : {len(auxiliary_df):,}")

# Primary Benchmark Track Distribution
track_dist = primary_df['track'].value_counts().reset_index()
track_dist.columns = ['Experimental Track', 'Pair Count (N)']
track_dist['Percentage (%)'] = (track_dist['Pair Count (N)'] / len(primary_df) * 100).round(2)
track_dist['Model Evaluations (2x)'] = track_dist['Pair Count (N)'] * 2

print("\\n=== PRIMARY BENCHMARK TRACK BREAKDOWN (N=1,679) ===")
display(track_dist)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display sample minimal pairs from each track of the Primary Benchmark
sample_pairs = []
for track in ['VALID_WORD_CONTEXT', 'SYNONYM_SUBSTITUTION', 'REALISTIC_SPELLING_ERROR']:
    row = primary_df[primary_df['track'] == track].iloc[0]
    sample_pairs.append({
        'Track': track,
        'Pair ID': row['pair_id'],
        'Original Sentence (Canonical)': row['original_sentence'],
        'Contrast Sentence (Perturbed)': row['contrast_sentence'],
        'Target Orig': row['target_original'],
        'Target Cont': row['target_contrast']
    })

sample_df = pd.DataFrame(sample_pairs)
print("=== SAMPLE MINIMAL SENTENCE PAIRS BY TRACK ===")
display(sample_df)
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 2.2 Complete 2,000-Row Candidate Reconciliation
Every row in the original 2,000-row candidate spreadsheet was tracked and adjudicated with zero unresolved items:
- **Primary Adjudicated Benchmark**: 1,679 pairs
- **Template Sensitivity Only**: 278 pairs
- **Auxiliary Multiword Probe**: 12 pairs
- **Excluded / Discarded**: 31 pairs (annotator rejection / formatting invalidity)
$$\\text{Total Reconciled} = 1,679 + 278 + 12 + 31 = 2,000 \\text{ rows}$$
"""))

    # -------------------------------------------------------------
    # SECTION 3: TOKENIZATION & FRAGMENTATION
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 3: Tokenization and Fragmentation (RQ1 & RQ2)

### 3.1 Linguistic Theory: Devanagari Akshara Structure vs. Subword Segmenters
Devanagari is an **abugida** (alphasyllabary). Words are constructed from syllabic units called **aksharas**, comprising base consonants, dependent vowel diacritics (*matras*), viramas (*halants*), and conjuncts (*samyuktaksharas*).

Standard subword tokenizers (Byte-Pair Encoding and WordPiece) operate on statistical character n-gram frequencies. When a user introduces a Devanagari typo—such as inverting a long *dirgha* matra for a short *hrasva* matra (`पानी` $\\to$ `पानि`) or omitting a halant (`आवश्यक` $\\to$ `आवशयक`)—the underlying Unicode sequence breaks across syllabic boundaries. The tokenizer loses its canonical vocabulary match and fractures the word into multiple fine-grained subwords or isolated codepoints. We term this phenomenon the **Devanagari Subword Collapse**.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load authoritative tokenization summary (Table 1)
tok_summary = pd.read_csv('results/runs/scaleup_rerun/dashboard_data/tokenization_summary.csv')

# Calculate Single-Subword Collapse Delta
tok_summary['single_subword_collapse_pct'] = (
    tok_summary['pct_single_subword_cont_target'] - tok_summary['pct_single_subword_orig_target']
).round(1)

# Format table for display
display_tok = tok_summary.copy()
display_tok.columns = [
    'Model Checkpoint', 'Track', 'Pair Count', 'Mean Orig Tokens', 'Mean Cont Tokens',
    'Token Delta (Δ)', 'Length Ratio', 'Mean Orig Target Subwords', 'Mean Cont Target Subwords',
    'Single Orig Target (%)', 'Single Cont Target (%)', 'Single Collapse (Δ%)'
]

print("=== TABLE 1: SUBWORD TOKENIZATION DYNAMICS (N=1,679 PRIMARY PAIRS) ===")
display(display_tok)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 2: Sentence Token Delta vs. MeanLogP Plausibility Shift
print("Figure 2: Sentence Token Length Changes vs. Plausibility Shifts")
display(Image(filename='results/runs/scaleup_rerun/figures/fig2_token_delta_vs_meanlp.png', width=750))
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 3: Target Token Delta vs. MeanLogP Plausibility Shift
print("Figure 3: Target Subword Changes vs. Plausibility Shifts")
display(Image(filename='results/runs/scaleup_rerun/figures/fig3_target_token_delta_vs_meanlp.png', width=750))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 3.2 Key Tokenization Observations
1. **Catastrophic Fragmentation in Spelling Errors**:
   - In `REALISTIC_SPELLING_ERROR` ($N=1,005$), introducing authentic Devanagari spelling errors causes single-subword target coverage to collapse by **$-71.6\\%$** in MuRIL ($91.7\\% \\to 20.1\\%$) and by **$-55.9\\%$** in XLM-RoBERTa ($62.3\\% \\to 6.4\\%$).
   - This fragmentation induces an average sentence-level token inflation of **$+1.13$ subwords in MuRIL** and **$+1.04$ subwords in XLM-RoBERTa**, driven exclusively by target fracturing.
2. **Tokenizer Efficiency Advantage**:
   - Across all tracks, MuRIL's Indic-dedicated WordPiece vocabulary encodes Hindi sentences with **$7.9\\%$ to $12.2\\%$ fewer subwords** than XLM-RoBERTa's massively multilingual SentencePiece vocabulary.
3. **Subword Robustness on Synonyms**:
   - In `SYNONYM_SUBSTITUTION` ($N=362$), 98.6% of canonical targets tokenize into a single subword in MuRIL, and 92.8% remain single subwords after substitution (a modest $-5.8\\%$ change).
"""))

    # -------------------------------------------------------------
    # SECTION 4: PSEUDO-LOG-LIKELIHOOD (PLL) SCORING
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 4: Pseudo-Log-Likelihood (PLL) Scoring (RQ1 & RQ2)

### 4.1 Scoring Formulation
Bidirectional masked language models cannot directly compute joint sequence probabilities $P(W)$. Following Salazar et al. (2020), we compute the **Pseudo-Log-Likelihood (PLL)** via iterative masking:
$$\\text{PLL}(W) = \\sum_{t=1}^{|W|} \\log P(w_t \\mid W_{\\setminus t}; \\Theta)$$

To avoid length bias caused by token inflation, we apply length normalization:
$$\\text{MeanLogP}(W) = \\frac{\\text{PLL}(W)}{|W_{\\text{scorable}}|}$$

The signed plausibility shift is:
$$\\Delta \\text{MeanLogP} = \\text{MeanLogP}(W_{\\text{cont}}) - \\text{MeanLogP}(W_{\\text{orig}})$$
- $\\Delta \\text{MeanLogP} < 0$: The original sentence is preferred (canonical preference).
- $\\Delta \\text{MeanLogP} > 0$: The contrast sentence is preferred.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load descriptive statistics (Table 2)
desc_stats = pd.read_csv('results/runs/scaleup_rerun/analysis/descriptive_statistics.csv')

# Filter to scorable primary benchmark rows (include_rejected == True)
table2_df = desc_stats[desc_stats['include_rejected'] == True][[
    'model_name', 'track', 'n_pairs', 'delta_meanlp_mean', 'delta_meanlp_median',
    'delta_meanlp_std', 'delta_meanlp_iqr', 'delta_meanlp_min', 'delta_meanlp_max',
    'delta_meanlp_n_negative'
]].copy()

table2_df['pct_original_preferred'] = (table2_df['delta_meanlp_n_negative'] / table2_df['n_pairs'] * 100).round(1)

table2_df.columns = [
    'Model Checkpoint', 'Track Scope', 'N Pairs', 'Mean Δ MeanLogP', 'Median Δ',
    'SD', 'IQR', 'Min Δ', 'Max Δ', 'Original Preferred (N)', 'Original Preferred (%)'
]

print("=== TABLE 2: MODEL PLAUSIBILITY SHIFTS (N=1,679 PRIMARY PAIRS) ===")
display(table2_df)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 1: Plausibility Shifts by Track
print("Figure 1: Distribution of Length-Normalized Pseudo-Log-Likelihood Deltas")
display(Image(filename='results/runs/scaleup_rerun/figures/fig1_delta_meanlp_by_track.png', width=750))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 4.2 Key Scoring Observations
1. **Harsher Spelling Penalties in MuRIL**:
   - In `REALISTIC_SPELLING_ERROR` ($N=1,005$), MuRIL penalizes spelling errors substantially more decisively than XLM-RoBERTa:
     - **MuRIL**: Original preferred in **$83.2\\%$** of pairs (836/1,005); Mean $\\Delta = -1.2045$, Median $= -0.8892$.
     - **XLM-RoBERTa**: Original preferred in **$76.4\\%$** of pairs (768/1,005); Mean $\\Delta = -0.8864$, Median $= -0.7752$.
2. **Contextual Sensitivity**:
   - Both models strongly reject contextual semantic mismatches (`VALID_WORD_CONTEXT`, $N=312$): MuRIL prefers the original in **$94.2\\%$** of pairs (mean $\\Delta = -1.8470$), while XLM-RoBERTa prefers the original in **$82.7\\%$** (mean $\\Delta = -1.0831$).
3. **Synonym Interchangeability**:
   - In `SYNONYM_SUBSTITUTION` ($N=362$), XLM-RoBERTa treats synonyms as near-interchangeable (mean $\\Delta = -0.0098$, 50.6% preference). MuRIL displays a modest negative shift (mean $\\Delta = -0.1787$, 58.8% preference), reflecting frequency distributions in its Indic training corpus.
4. **Non-Causal Guardrail**:
   - These plausibility deltas represent probabilistic language model scores under bidirectional conditioning, not direct causal claims about human grammatical acceptability.
"""))

    # -------------------------------------------------------------
    # SECTION 5: CROSS-MODEL COMPARISON
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 5: Cross-Model Comparison (RQ2)

### 5.1 Measuring Concordance across Architectures
Because MuRIL and XLM-RoBERTa utilize entirely different subword vocabularies and tokenization algorithms, their raw PLL sums cannot be directly cross-compared. Cross-model concordance is evaluated using:
1. **Directional Sign Agreement**: Percentage of pairs where both models agree on the preference direction ($\text{sgn}(\\Delta_{\\text{XLM}}) == \\text{sgn}(\\Delta_{\\text{MuRIL}})$).
2. **Spearman Rank Correlation ($r_s$)**: Rank correlation of within-model signed deltas ($\Delta \\text{MeanLogP}$), with Fisher $z$-transformed 95% confidence intervals.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load cross-model comparison results (Table 3)
model_comp = pd.read_csv('results/runs/scaleup_rerun/analysis/model_comparison.csv')

display_mc = model_comp[[
    'track_scope', 'n_pairs', 'direction_both_negative', 'direction_both_positive',
    'direction_xlm_neg_muril_pos', 'direction_xlm_pos_muril_neg',
    'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value', 'ci_95_lo', 'ci_95_hi'
]].copy()

display_mc['direction_agreement_rate'] = (display_mc['direction_agreement_rate'] * 100).round(2)
display_mc['ci_95'] = display_mc.apply(lambda r: f"[{r['ci_95_lo']:.4f}, {r['ci_95_hi']:.4f}]", axis=1)

display_mc = display_mc.drop(columns=['ci_95_lo', 'ci_95_hi'])
display_mc.columns = [
    'Track Scope', 'N Pairs', 'Both Neg (Orig)', 'Both Pos (Cont)',
    'XLM Neg / MuRIL Pos', 'XLM Pos / MuRIL Neg', 'Agreement Rate (%)',
    'Spearman rs', 'p-value', '95% CI'
]

print("=== TABLE 3: CROSS-MODEL CONCORDANCE (N=1,679 PRIMARY PAIRS) ===")
display(display_mc)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 4: Cross-Model Plausibility Scatter
print("Figure 4: Cross-Model Scatter Plot of Delta MeanLogP")
display(Image(filename='results/runs/scaleup_rerun/figures/fig4_model_comparison_scatter.png', width=750))
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 5: Directional Agreement Proportions
print("Figure 5: Directional Agreement Proportions Across Tracks")
display(Image(filename='results/runs/scaleup_rerun/figures/fig5_direction_agreement.png', width=650))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 5.2 Key Cross-Model Observations
1. **Global Concordance on Prominent Contrasts**:
   - Across all 1,679 pairs, the two architectures exhibit **$73.67\\%$ directional agreement** and a statistically significant rank correlation of **$r_s = +0.5496$** ($p < 10^{-15}$, 95% CI $[0.5153, 0.5821]$).
   - Concordance is highest in `VALID_WORD_CONTEXT` ($84.62\\%$ agreement, $r_s = +0.4590$) and `REALISTIC_SPELLING_ERROR` ($75.12\\%$ agreement, $r_s = +0.5513$).
2. **Decoupling on Synonyms**:
   - In `SYNONYM_SUBSTITUTION` ($N=362$), directional agreement drops to **$60.22\\%$** and rank correlation weakens to **$r_s = +0.2271$** ($p = 1.3 \\times 10^{-5}$).
   - This indicates that when semantic truth conditions are preserved, the models' scoring preferences reflect independent pretraining corpus frequencies rather than shared linguistic structures.
"""))

    # -------------------------------------------------------------
    # SECTION 6: EXPLANATION STABILITY
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 6: Explanation Stability (RQ3)

### 6.1 The Stage 6 Masked-Target Artifact vs. Stage 7 Visible-Target Protocol
A critical methodological insight documented in this project is the **Masked-Target Artifact**:
- In early stability evaluations (Stage 6), the target word was masked with `[MASK]` in both original and contrast sentences.
- Because spelling perturbations resided exclusively inside the target word, masking the target caused both input sequences to become byte-identical ($X_{\\text{orig}} \\equiv X_{\\text{cont}}$).
- This generated an illusory, trivial stability score of $\\rho = 1.0000$ and $\\text{Cosine} = 1.0000$ with zero variance.

To resolve this artifact, we formulated the **Visible-Target Scoring Protocol** in Stage 7:
1. Target words remain **fully visible** in the input text during attribution computation.
2. The target prediction score is defined as the mean unnormalized logit of the actual target subwords:
   $$S(X; Y_{\\text{target}}) = \\frac{1}{|T|} \\sum_{j \\in T} \\text{Logit}(p_j, y_j)$$
3. Attributions are computed across aligned context tokens while the model processes the actual spelling error.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load explanation stability summary (Table 4)
stab_summary = pd.read_csv('results/runs/scaleup_rerun/dashboard_data/stability_summary.csv')

display_stab = stab_summary[[
    'model_name', 'method', 'subset', 'pair_count',
    'stage6_masked_target_stability_rho', 'stage6_masked_target_cosine',
    'visible_target_stability_rho_mean', 'visible_target_stability_rho_median',
    'visible_target_cosine_mean', 'visible_target_cosine_median'
]].copy()

display_stab.columns = [
    'Model Checkpoint', 'Method', 'Subset', 'Pair Count (N)',
    'Stage 6 Masked ρ', 'Stage 6 Masked Cosine',
    'Visible Mean ρ', 'Visible Median ρ',
    'Visible Mean Cosine', 'Visible Median Cosine'
]

print("=== TABLE 4: VISIBLE-TARGET EXPLANATION STABILITY (N=1,005 SPELLING PAIRS) ===")
display(display_stab)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 6: Explanation Stability Comparison
print("Figure 6: Visible-Target Explanation Stability under Devanagari Spelling Noise")
display(Image(filename='results/runs/scaleup_rerun/figures/fig6_explanation_stability.png', width=800))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 6.2 Key Stability Observations
1. **Attention Rank Stability Superiority**:
   - Under authentic spelling noise, last-layer multi-head self-attention achieves **$1.9\\times$ to $3.1\\times$ higher rank stability** than Integrated Gradients:
     - **MuRIL**: Pooled Mean $\\rho = 0.8027$ (Attention) vs. $0.2560$ (IG).
     - **XLM-RoBERTa**: Pooled Mean $\\rho = 0.6258$ (Attention) vs. $0.3319$ (IG).
2. **Dissociation between Rank and Vector Stability in IG**:
   - While Integrated Gradients exhibits low rank stability ($\rho \\approx 0.26\\text{--}0.33$), its **Cosine Similarity remains exceptionally high** ($0.8890$ to $0.9818$).
   - **Geometric Interpretation**: The gradient attribution vector preserves its global orientation in high-dimensional embedding space, but the relative ranking of individual context tokens fluctuates under localized orthographic noise.
"""))

    # -------------------------------------------------------------
    # SECTION 7: FAITHFULNESS VIA CONTEXT ERASURE
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 7: Faithfulness and Context Erasure (RQ4)

### 7.1 Causal Feature Erasure Protocol
Following the ERASER benchmark (DeYoung et al., 2020), explanation faithfulness is evaluated by measuring model score degradation when attributed context tokens are erased.

For each sentence ($N=2,010$ sentences per model across 1,005 spelling pairs), context tokens are ranked by attribution score. We evaluate three masking interventions at fractions $f \\in \\{0.10, 0.20, 0.30\\}$:
- **Top-$k$ Erasure**: Masking the top $k = \\lceil f \\cdot |C| \\rceil$ tokens with `[MASK]`.
- **Bottom-$k$ Erasure (Control)**: Masking the $k$ lowest-attributed tokens.
- **Random-$k$ Erasure**: Masking $k$ random tokens (averaged over 5 independent trials).

We evaluate:
1. **Faithfulness Gap**: $\\Delta S_{\\text{top}} - \\Delta S_{\\text{bottom}} = S_{\\text{bottom}} - S_{\\text{top}}$ (positive indicates that top tokens degrade target logit more than control tokens).
2. **Win Rate vs. Bottom Control**: Percentage of sentences where $\\Delta S_{\\text{top}} > \\Delta S_{\\text{bottom}}$.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load faithfulness summary (Table 5)
faith_summary = pd.read_csv('results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv')

display_faith = faith_summary[[
    'model_name', 'method', 'subset', 'fraction', 'n_evaluated_sentences',
    'top_k_logit_drop_mean', 'bottom_k_logit_drop_mean', 'random_k_logit_drop_mean',
    'faithfulness_gap_mean', 'faithfulness_gap_median',
    'win_rate_vs_bottom', 'win_rate_vs_random'
]].copy()

display_faith['win_rate_vs_bottom'] = (display_faith['win_rate_vs_bottom'] * 100).round(2)
display_faith['win_rate_vs_random'] = (display_faith['win_rate_vs_random'] * 100).round(2)

display_faith.columns = [
    'Model Checkpoint', 'Method', 'Subset', 'Fraction (f)', 'N Sentences',
    'Mean Top Drop', 'Mean Bottom Drop', 'Mean Random Drop',
    'Mean Faith Gap', 'Median Faith Gap',
    'Win Rate vs Bottom (%)', 'Win Rate vs Random (%)'
]

print("=== TABLE 5: FAITHFULNESS UNDER CONTEXT ERASURE (N=2,010 SENTENCES / MODEL) ===")
display(display_faith)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 7: Faithfulness Interventions Trajectory
print("Figure 7: Context Erasure Faithfulness across Intervention Fractions")
display(Image(filename='results/runs/scaleup_rerun/figures/fig7_faithfulness_interventions.png', width=800))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 7.2 Key Faithfulness Observations
1. **Attention Outperforms Integrated Gradients in XLM-RoBERTa**:
   - In discrete masking tests on XLM-RoBERTa, self-attention attributions consistently achieve positive Faithfulness Gaps ($+2.44$ to $+3.81$) and win rates of **$63.53\\%\\text{--}67.46\\%$** against bottom control erasure.
2. **Integrated Gradients Operates Near or Below Chance in MuRIL**:
   - In MuRIL, Integrated Gradients achieves win rates of only **$46.72\\%\\text{--}49.90\\%$** (worse than or equal to random chance), yielding negative mean faithfulness gaps across all fractions ($-0.30$ to $-1.08$).
3. **Continuous Path Integrals vs. Discrete MLM Heads**:
   - **Theoretical Explanation**: Integrated Gradients accumulates gradients along a continuous straight-line path in embedding space:
     $$\\gamma(\\alpha) = x' + \\alpha(x - x'), \\quad \\alpha \\in [0, 1]$$
     This path traverses off-manifold embedding regions. In contrast, discrete token erasure in MLMs creates an abrupt contextual shift that aligns more closely with last-layer attention routing mechanisms.
"""))

    # -------------------------------------------------------------
    # SECTION 8: STABILITY-FAITHFULNESS RELATIONSHIP
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 8: Stability–Faithfulness Relationship (RQ5)

### 8.1 Evaluating the Relationship Between Stability and Faithfulness
A pervasive assumption in explainable AI is that attribution stability is an indicator of explanation quality—i.e., that a stable explanation is more likely to be faithful to the underlying model reasoning.

We test this hypothesis across all 1,005 Devanagari spelling pairs by correlating visible-target stability (Spearman $\\rho$) with the mean faithfulness gap at $f=0.20$.
"""))

    cells.append(nbf.v4.new_code_cell("""# Compute and display Table 6: Stability vs. Faithfulness Correlation Matrix
rel_df = pd.read_csv('results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv')

corr_rows = []
for model in ['FacebookAI/xlm-roberta-base', 'google/muril-base-cased']:
    for method in ['attention', 'integrated_gradients']:
        for subset in ['all_scorable', 'strict_single_subword']:
            sub = rel_df[(rel_df['model_name'] == model) & (rel_df['method'] == method) & (rel_df['subset'] == subset)]
            valid = sub.dropna(subset=['visible_target_stability_rho', 'mean_faithfulness_gap_f20'])
            
            if len(valid) > 2:
                sp_r, sp_p = stats.spearmanr(valid['visible_target_stability_rho'], valid['mean_faithfulness_gap_f20'])
                pe_r, pe_p = stats.pearsonr(valid['visible_target_stability_rho'], valid['mean_faithfulness_gap_f20'])
                
                # Statistical interpretation
                if sp_p <= 0.05 and sp_r < 0:
                    interp = f"Weak Inverse Rank (rs={sp_r:.4f}, p={sp_p:.4f})"
                elif pe_p <= 0.05 and pe_r < 0:
                    interp = f"Weak Inverse Linear (r={pe_r:.4f}, p={pe_p:.4f})"
                elif pe_p <= 0.05 and pe_r > 0:
                    interp = f"Weak Positive Linear (r={pe_r:.4f}, p={pe_p:.4f})"
                elif sp_p <= 0.05 and sp_r > 0:
                    interp = f"Significant Positive Rank (rs={sp_r:.4f}, p={sp_p:.4f})"
                else:
                    interp = "Non-Significant (p > 0.05)"
                
                corr_rows.append({
                    'Model Checkpoint': model,
                    'Explanation Method': method,
                    'Evaluated Subset': subset,
                    'Sample Size (N)': len(valid),
                    'Spearman Rank rs': round(sp_r, 4),
                    'p-value (rs)': round(sp_p, 4),
                    'Pearson Linear r': round(pe_r, 4),
                    'p-value (r)': round(pe_p, 4),
                    'Empirical Interpretation': interp
                })

table6_df = pd.DataFrame(corr_rows)
print("=== TABLE 6: CORRELATION BETWEEN STABILITY AND FAITHFULNESS (N=1,005 SPELLING PAIRS) ===")
display(table6_df)
"""))

    cells.append(nbf.v4.new_code_cell("""# Display Figure 8: Stability vs. Faithfulness Decoupling Scatter
print("Figure 8: Visible-Target Stability vs. Faithfulness Decoupling")
display(Image(filename='results/runs/scaleup_rerun/figures/fig8_stability_vs_faithfulness.png', width=800))
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 8.2 Statistical Interpretation & Core Conclusion
1. **Absence of a Consistent Positive Association**:
   - In the preliminary pilot ($N=20$), the absence of correlation was preliminary and limited by sample size. In this expanded scale-up benchmark ($N=953$ and $N=808$ scorable pairs), we evaluate stability–faithfulness relationships with substantially greater statistical resolution.
   - Importantly, **not all stability–faithfulness correlations are non-significant**:
     - **MuRIL Attention (Pooled, $N=808$)**: Pearson linear correlation is weakly negative and statistically significant ($r = -0.0790, p = 0.0248$), while Spearman rank correlation is non-significant ($r_s = -0.0442, p = 0.2099$).
     - **MuRIL Attention (Strict Single-Subword, $N=197$)**: Spearman rank correlation is weakly negative and statistically significant ($r_s = -0.1924, p = 0.0067$), while Pearson linear correlation is $r = -0.1129, p = 0.1141$.
     - **XLM-RoBERTa Attention (Strict Single-Subword, $N=52$)**: Pearson linear correlation is weakly positive ($r = +0.2949, p = 0.0338$), while Spearman rank correlation remains non-significant ($r_s = +0.2472, p = 0.0773$).
     - **Other Conditions**: XLM-RoBERTa Attention pooled ($r_s = +0.0607, p = 0.0612$), XLM-RoBERTa IG pooled ($r_s = +0.0632, p = 0.0510$), XLM-RoBERTa IG strict ($r_s = +0.1647, p = 0.2434$), MuRIL IG pooled ($r_s = +0.0214, p = 0.5442$), and MuRIL IG strict ($r_s = +0.0344, p = 0.6316$) all exhibit non-significant associations ($p > 0.05$).
2. **Proper Scientific Nuance**:
   - The appropriate overall conclusion is that **there is no consistent positive association between explanation stability and faithfulness**.
   - Some weak negative associations occur for MuRIL Attention, while other combinations are non-significant.
   - We do not claim that these empirical findings prove mathematical independence, establish causation, or rule out all sample-size limitations across all neural network architectures. Rather, within these evaluated models and benchmark, **stability to spelling perturbations cannot serve as a reliable empirical proxy for causal explanation faithfulness**.
"""))

    # -------------------------------------------------------------
    # SECTION 9: TEMPLATE SENSITIVITY ANALYSIS
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 9: Template Sensitivity Analysis

### 9.1 Purpose of the Template Benchmark ($N=1,957$)
To verify that our empirical findings are not idiosyncratic artifacts of specific sentence contexts, we evaluated the Secondary Template Sensitivity Benchmark ($N=1,957$ minimal pairs across 278 template frames).

> **Pedagogical Reminder**: The template sensitivity benchmark contains the primary pairs plus template-generated sentence frames. It evaluates frame invariance and is analyzed separately from the primary benchmark.
"""))

    cells.append(nbf.v4.new_code_cell("""# Load Template Sensitivity descriptive statistics and model comparison
tmpl_desc = pd.read_csv('results/runs/scaleup_rerun/template_sensitivity/analysis/descriptive_statistics.csv')
tmpl_comp = pd.read_csv('results/runs/scaleup_rerun/template_sensitivity/analysis/model_comparison.csv')

# Format descriptive table
tmpl_desc_display = tmpl_desc[tmpl_desc['include_rejected'] == True][[
    'model_name', 'track', 'n_pairs', 'delta_meanlp_mean', 'delta_meanlp_median',
    'delta_meanlp_std', 'delta_meanlp_n_negative'
]].copy()
tmpl_desc_display['pct_orig_preferred'] = (tmpl_desc_display['delta_meanlp_n_negative'] / tmpl_desc_display['n_pairs'] * 100).round(1)
tmpl_desc_display.columns = ['Model Checkpoint', 'Track', 'N Pairs', 'Mean Δ', 'Median Δ', 'SD', 'Orig Preferred (N)', 'Orig Preferred (%)']

print("=== TEMPLATE SENSITIVITY: DESCRIPTIVE STATISTICS (N=1,957 PAIRS) ===")
display(tmpl_desc_display)

# Format model comparison table
tmpl_comp_display = tmpl_comp[[
    'track_scope', 'n_pairs', 'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value', 'ci_95_lo', 'ci_95_hi'
]].copy()
tmpl_comp_display['direction_agreement_rate'] = (tmpl_comp_display['direction_agreement_rate'] * 100).round(2)
tmpl_comp_display['95% CI'] = tmpl_comp_display.apply(lambda r: f"[{r['ci_95_lo']:.4f}, {r['ci_95_hi']:.4f}]", axis=1)
tmpl_comp_display = tmpl_comp_display.drop(columns=['ci_95_lo', 'ci_95_hi'])
tmpl_comp_display.columns = ['Track Scope', 'N Pairs', 'Agreement Rate (%)', 'Spearman rs', 'p-value', '95% CI']

print("\\n=== TEMPLATE SENSITIVITY: CROSS-MODEL COMPARISON (N=1,957 PAIRS) ===")
display(tmpl_comp_display)
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 9.2 Template Benchmark Takeaways
- On `REALISTIC_SPELLING_ERROR` ($N=1,260$): MuRIL prefers the original in $81.9\\%$ of pairs (mean $\\Delta = -1.0778$), and XLM-RoBERTa prefers the original in $70.8\\%$ (mean $\\Delta = -0.6941$).
- On `SYNONYM_SUBSTITUTION` ($N=385$): XLM-RoBERTa exhibits an average delta of just $\\Delta = -0.0026$, replicating synonym interchangeability.
- Global directional agreement across all 1,957 template pairs is **$71.28\\%$** with Spearman **$r_s = +0.5344$** ($p < 10^{-15}$), tightly mirroring primary benchmark results ($73.67\\%, r_s = +0.5496$).
"""))

    # -------------------------------------------------------------
    # SECTION 10: AUXILIARY MULTIWORD PROBE
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 10: Auxiliary Multiword Probe ($N=12$)

### 10.1 Fine-Grained 4-Category Taxonomy
The Auxiliary Multiword Probe comprises 12 carefully adjudicated edge-case minimal pairs that test multiword ripple effects and token alignment ambiguities:
1. **Gender/Number Agreement Changes ($N=6$)**: Lexical substitution triggers grammatical agreement ripples in surrounding adjectives or verbs.
2. **Postpositional Insertion ($N=1$)**: Case marker insertion alters sentence syntactic geometry.
3. **Collocational Light-Verb Change ($N=1$)**: Synonym substitution triggers collocational change in light verb.
4. **Repeated-Target Ambiguities ($N=4$)**: Target word appears multiple times in the sentence, creating token attribution alignment ambiguities.
"""))

    cells.append(nbf.v4.new_code_cell("""# Display all 12 rows of the Auxiliary Multiword Probe
aux_rows = auxiliary_df[[
    'pair_id', 'track', 'original_sentence', 'contrast_sentence',
    'target_original', 'target_contrast', 'probe_phenomenon', 'linguistic_explanation'
]].copy()

aux_rows.columns = [
    'Pair ID', 'Track', 'Original Sentence', 'Contrast Sentence',
    'Target Orig', 'Target Cont', 'Fine-Grained Phenomenon', 'Linguistic Explanation'
]

print("=== ALL 12 AUXILIARY MULTIWORD PROBE EXAMPLES ===")
display(aux_rows)
"""))

    cells.append(nbf.v4.new_code_cell("""# Load Auxiliary Probe model comparison and descriptive statistics
aux_comp = pd.read_csv('results/runs/scaleup_rerun/auxiliary_probe/analysis/model_comparison.csv')
aux_desc = pd.read_csv('results/runs/scaleup_rerun/auxiliary_probe/analysis/descriptive_statistics.csv')

print("=== AUXILIARY PROBE: CROSS-MODEL COMPARISON ===")
display(aux_comp[['track_scope', 'n_pairs', 'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value']])

print("\\n=== AUXILIARY PROBE: DESCRIPTIVE STATISTICS ===")
display(aux_desc[aux_desc['include_rejected'] == True][['model_name', 'track', 'n_pairs', 'delta_meanlp_mean', 'delta_meanlp_median', 'delta_meanlp_n_negative']])
"""))

    cells.append(nbf.v4.new_markdown_cell("""### 10.2 Auxiliary Probe Takeaways
- The auxiliary probe confirms that multiword ripple effects (such as grammatical agreement cascades) challenge standard single-word alignment assumptions.
- Cross-model directional agreement is lower ($41.67\\%$) on this probe, reflecting the models' divergent handling of multi-word perturbations and repeated-token alignment ambiguities.
"""))

    # -------------------------------------------------------------
    # SECTION 11: OVERALL FINDINGS & LIMITATIONS
    # -------------------------------------------------------------
    cells.append(nbf.v4.new_markdown_cell("""## Section 11: Overall Findings and Limitations

### 11.1 Major Scientific Findings
1. **Devanagari Subword Collapse**: Authentic spelling errors cause massive subword fragmentation (single-subword target coverage collapses by $-71.6\\%$ in MuRIL and $-55.9\\%$ in XLM-RoBERTa), driving token inflation exclusively at the target locus.
2. **Differential Model Scoring**: MuRIL penalizes spelling errors more decisively ($83.2\\%$ preference rate, mean $\\Delta = -1.2045$) than XLM-RoBERTa ($76.4\\%$, mean $\\Delta = -0.8864$), while both recognize valid synonyms as near-interchangeable.
3. **Attention Rank Stability Advantage**: Resolving the masked-target artifact reveals that last-layer self-attention achieves $1.9\\times$ to $3.1\\times$ higher rank stability than Integrated Gradients, while Integrated Gradients preserves high vector cosine similarity.
4. **Discrete Masking Faithfulness**: Attention explanations exhibit higher win rates ($63.5\\%\\text{--}67.5\\%$) under discrete token erasure than Integrated Gradients, whose continuous path integrals do not match discrete MLM prediction heads.
5. **No Consistent Positive Stability–Faithfulness Association**: Across 1,005 Devanagari spelling pairs, there is no consistent positive association between explanation stability and faithfulness. Some weak negative associations occur for MuRIL Attention (pooled Pearson $r = -0.0790, p = 0.0248$; strict single-subword Spearman $\\rho = -0.1924, p = 0.0067$), while other combinations are non-significant. Evaluating explanation methods solely on robustness risks selecting stably unfaithful rationales.

---

### 11.2 Documented Research Limitations
To preserve academic rigor, the research documents five explicit limitations:
1. **Sample Size & Power Resolution**: While $N=1,005$ spelling pairs provides ample statistical power to evaluate small effect sizes, the results reflect empirical observations on the evaluated models and benchmark rather than an exhaustive proof across all deep learning architectures.
2. **Out-of-Distribution (OOD) Syntactic Shock from Masking**: Context token erasure introduces unnatural syntactic voids that elevate global perplexity alongside causal feature removal.
3. **Multi-Subword Target Logit Aggregation**: Averaging unnormalized logits across target subwords assumes uniform weighting among constituent fragments.
4. **Non-Causal Nature of Attention**: Attention weights are routing coefficients rather than formal causal explanations; their empirical success reflects architectural alignment with discrete transformer layers.
5. **Pretrained Checkpoint Scope**: Evaluations were conducted on base-scale bidirectional MLMs. Extrapolating these conclusions to decoder-only generative LLMs remains an open question for future work.

---
*Teacher-facing notebook compiled and verified from `results/runs/scaleup_rerun/`.*
"""))

    nb.cells = cells
    return nb

def main():
    print("Building expanded experimental results notebook...")
    nb = create_notebook()
    
    out_path = os.path.join('notebooks', 'expanded_experimental_results.ipynb')
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook written to: {out_path}")
    
    print("Executing notebook to render all outputs...")
    client = NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': '.'}})
    client.execute()
    
    with open(out_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Notebook successfully executed and saved with rendered outputs: {out_path}")

if __name__ == '__main__':
    main()
