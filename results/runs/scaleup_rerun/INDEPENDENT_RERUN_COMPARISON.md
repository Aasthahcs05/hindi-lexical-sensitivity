# Independent Experiment Rerun Verification Report

**Comparison Timestamp (UTC)**: 2026-11-02T17:33:20.753190+00:00
**Baseline Run**: `results/runs/scaleup_1679/`
**Independent Rerun**: `results/runs/scaleup_rerun/`
**Overall Verification Status**: **FULL_AGREEMENT**

## 1. Executive Summary

An independent, unassisted full experiment rerun was executed using frozen pretrained MLMs (`google/muril-base-cased` and `FacebookAI/xlm-roberta-base`) on the NVIDIA RTX 3050 Laptop GPU under PyTorch 2.14.1+cu126.

| Stage | Analysis Domain | Baseline Count (N) | Rerun Count (N) | Numerical Diff (Max) | Agreement Status |
|---|---|---|---|---|---|
| Stage 1 | Primary Tokenization | 3358 | 3358 | 0.0 (exact match) | ✅ Agree |
| Stage 2 | Primary PLL Scoring (CUDA) | 3358 | 3358 | 0.000000 | ✅ Agree |
| Stage 3 | Combined Statistical Analysis | 3358 | 3358 | 0.0 | ✅ Agree |
| Stage 4 | Explanation Stability (N=1,005) | 4020 | 4020 | 0.000000 | ✅ Agree |
| Stage 5 | Faithfulness Interventions (N=1,005) | 72360 | 72360 | 0.0 | ✅ Agree |
| Stage 6 | Dashboard Data & Master Tables | 3358 | 3358 | 0.0 | ✅ Agree |
| Stage 7 | Publication Figures (Figs 1-8) | 8 figs | 8 figs | - | ✅ Agree |
| Stage 8 | Template Benchmark (N=1,957) | 3914 | 3914 | 0.0 | ✅ Agree |
| Stage 9 | Auxiliary Multiword Probe (N=12) | 24 | 24 | 0.0 | ✅ Agree |

## 2. Stage-by-Stage Verification Details

### Stage 1: Tokenization and Fragmentation
- Baseline Evaluations: 3358 (1679 unique pairs x 2 models)
- Rerun Evaluations: 3358 (1679 unique pairs x 2 models)
- Target and context token alignments match bit-for-bit with baseline run.

### Stage 2: Pseudo-Log-Likelihood Scoring
- Max absolute difference in Delta MeanLogP: `0.000000`
- Mean absolute difference across 3,358 evaluations: `0.00000000`
- All differences are within expected floating-point non-determinism bounds for GPU matrix multiplication.

### Stage 4 & 5: Explanation Stability & Faithfulness
- Evaluated Spelling Errors: exactly N=1,005 sentence pairs.
- Stability Pair Evaluations: exactly 4,020 records (1,005 pairs x 2 models x 2 methods).
- Faithfulness Interventions: exactly 72,360 records (1,005 pairs x 2 models x 2 methods x 2 sentences x 3 fractions x 3 mask types).
- Max difference in Spearman rank correlation rho: `0.000000`.

### Stages 8 & 9: Secondary Benchmarks
- Template Sensitivity: 3914 evaluations (1,957 pairs x 2 models).
- Auxiliary Probe: 24 evaluations (12 pairs x 2 models).

## 3. Hardware & Telemetry Verification
- All model weights were loaded onto `cuda:0`.
- Input tensors were verified on `cuda:0` throughout the forward passes.
- Peak VRAM during batch inference remained safely within 6 GB GPU memory capacity.
- No CPU fallbacks or device transfer failures occurred.

## 4. Final Verdict
**FULL_AGREEMENT**: The independent rerun fully confirms all results of `scaleup_1679` within numerical precision limits across all 9 computational stages.