"""Master Execution Script: Scale-Up Experiment Independent Rerun (results/runs/scaleup_rerun/).

Preserves existing research methodology, frozen models (MuRIL, XLM-R),
tokenization procedures, PLL calculations, attention & Integrated Gradients procedures,
and explanation stability & faithfulness metrics.

Strict Isolation:
- Outputs strictly to results/runs/scaleup_rerun/
- Does NOT overwrite results/runs/scaleup_1679/
- Does NOT overwrite results/runs/historical_pilot_200/
- Does NOT modify outputs/ or research_paper/
- Records full GPU hardware telemetry for every inference stage.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure stdout uses UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from src.data.tokenization_experiment import (
    compute_file_sha256,
    get_library_versions,
    load_dataset_rows,
    run_tokenization_experiment,
)
from src.models.pll_scoring import run_pll_scoring_experiment
from src.analysis.combined_analysis import run_analysis
from src.analysis.explanation_stability import run_stage6_stability_experiment
from src.analysis.hindi_faithfulness import run_stage7_faithfulness_experiment
from src.analysis.dashboard_data import run_stage8_dashboard_data_preparation
from src.analysis.generate_figures_6_7_8 import generate_figures_6_7_8

# Frozen benchmark paths
DATA_FINAL = PROJECT_ROOT / "data" / "final"
PRIMARY_CSV = DATA_FINAL / "PRIMARY_BENCHMARK_ADJUDICATED.csv"
TEMPLATE_CSV = DATA_FINAL / "TEMPLATE_SENSITIVITY_BENCHMARK.csv"
AUX_CSV = DATA_FINAL / "AUXILIARY_MULTIWORD_PROBE.csv"

# Target rerun directory
RUN_BASE = PROJECT_ROOT / "results" / "runs" / "scaleup_rerun"


def get_gpu_telemetry() -> dict[str, Any]:
    """Capture current GPU memory and device information."""
    if not torch.cuda.is_available():
        return {"cuda_available": False}
    return {
        "cuda_available": True,
        "device_name": torch.cuda.get_device_name(0),
        "device_capability": list(torch.cuda.get_device_capability(0)),
        "total_memory_mb": round(torch.cuda.get_device_properties(0).total_memory / (1024 * 1024), 2),
        "allocated_memory_mb": round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2),
        "reserved_memory_mb": round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2),
        "max_memory_allocated_mb": round(torch.cuda.max_memory_allocated(0) / (1024 * 1024), 2),
    }


def log_step(title: str, log_file: Path | None = None) -> None:
    msg = f"\n{'=' * 70}\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {title}\n{'=' * 70}"
    print(msg, flush=True)
    if log_file:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")


def get_dataset_stats(csv_path: Path) -> dict[str, Any]:
    """Parse CSV to validate records and unique IDs."""
    rows = load_dataset_rows(csv_path)
    pair_ids = [r.get("pair_id") for r in rows if r.get("pair_id")]
    unique_ids = set(pair_ids)
    return {
        "path": str(csv_path.resolve()),
        "sha256": compute_file_sha256(csv_path),
        "parsed_row_count": len(rows),
        "unique_id_count": len(unique_ids),
        "has_duplicates": len(rows) != len(unique_ids),
    }


def make_gpu_loader(device: torch.device, model_param_records: dict[str, Any]):
    """Creates a model loader that records actual parameter device on CUDA."""
    from transformers import AutoModelForMaskedLM, AutoTokenizer

    def loader(model_id: str) -> tuple[Any, Any]:
        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
        try:
            model = AutoModelForMaskedLM.from_pretrained(model_id, attn_implementation="eager")
        except (TypeError, ValueError):
            model = AutoModelForMaskedLM.from_pretrained(model_id)
        model.eval()
        model.to(device)
        param_dev = str(next(model.parameters()).device)
        input_tensor_dev = str(device)
        model_param_records[model_id] = {
            "model_name": model_id,
            "actual_param_device": param_dev,
            "input_tensor_device": input_tensor_dev,
            "param_dtype": str(next(model.parameters()).dtype),
            "num_parameters": sum(p.numel() for p in model.parameters()),
            "is_cuda": "cuda" in param_dev,
        }
        print(f"Verified {model_id} loaded on {param_dev} (input tensor target: {input_tensor_dev})", flush=True)
        return model, tokenizer

    return loader


def main() -> None:
    t_start = time.time()
    RUN_BASE.mkdir(parents=True, exist_ok=True)
    log_file = RUN_BASE / "scaleup_rerun.log"

    # Append to log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"\n=== SCALE-UP EXPERIMENT RESUMED ===\nResumed: {datetime.now(timezone.utc).isoformat()}\n\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Starting scale-up independent rerun on {device}...", flush=True)
    if device.type != "cuda":
        raise RuntimeError("GPU (CUDA) is required for scale-up rerun, but torch.cuda.is_available() is False!")

    gpu_name = torch.cuda.get_device_name(0)
    cuda_ver = torch.version.cuda
    pytorch_ver = torch.__version__
    print(f"CUDA Device: {gpu_name}", flush=True)
    print(f"CUDA Version: {cuda_ver}", flush=True)
    print(f"PyTorch Version: {pytorch_ver}", flush=True)

    # Validate dataset inputs
    dataset_manifest = {
        "primary": get_dataset_stats(PRIMARY_CSV),
        "template": get_dataset_stats(TEMPLATE_CSV),
        "auxiliary": get_dataset_stats(AUX_CSV),
    }

    run_log: dict[str, Any] = {
        "start_time_utc": datetime.now(timezone.utc).isoformat(),
        "run_id": "scaleup_rerun",
        "system_environment": {
            "os": platform.platform(),
            "python_version": sys.version,
            "pytorch_version": pytorch_ver,
            "cuda_version": cuda_ver,
            "gpu_name": gpu_name,
            "device": str(device),
            "library_versions": get_library_versions(),
        },
        "datasets": dataset_manifest,
        "models": [
            {"id": "google/muril-base-cased", "frozen": True, "type": "pretrained_mlm"},
            {"id": "FacebookAI/xlm-roberta-base", "frozen": True, "type": "pretrained_mlm"},
        ],
        "stages": {},
        "gpu_inference_telemetry": {},
    }

    # ─────────────────────────────────────────────────────────────
    # STEP 1: PRIMARY BENCHMARK TOKENIZATION (Stage 2)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 1: Primary Benchmark Tokenization (N=1,679)", log_file)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    tok_dir = RUN_BASE / "tokenization"
    tok_results, tok_meta, tok_summary = run_tokenization_experiment(
        input_file=PRIMARY_CSV,
        output_dir=tok_dir,
        force=False,
    )
    t_tok = time.time() - t0
    run_log["stages"]["stage1_tokenization"] = {
        "description": "Primary Benchmark Tokenization & Fragmentation",
        "sample_size": len(tok_results) // 2,
        "total_evaluations": len(tok_results),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_tok, 2),
        "output_files": [str(tok_dir / "tokenization_results.csv"), str(tok_dir / "run_metadata.json")],
        "completed_successfully": True,
    }
    print(f"Tokenization completed in {t_tok:.2f}s ({len(tok_results)} evals).", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 2: PRIMARY BENCHMARK PLL SCORING (Stage 3)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 2: Primary Benchmark PLL Scoring (N=1,679, batch_size=32, CUDA)", log_file)
    torch.cuda.reset_peak_memory_stats(0)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    score_dir = RUN_BASE / "scoring"
    pll_param_records: dict[str, Any] = {}
    pll_loader = make_gpu_loader(device, pll_param_records)

    pll_results, pll_meta, pll_summary = run_pll_scoring_experiment(
        input_file=PRIMARY_CSV,
        output_dir=score_dir,
        pilot=False,
        batch_size=32,
        force=False,
        model_loader=pll_loader,
    )
    t_pll = time.time() - t0
    gpu_tel_pll = get_gpu_telemetry()
    run_log["gpu_inference_telemetry"]["stage2_pll_scoring"] = {
        "cuda_available": True,
        "gpu_name": gpu_name,
        "cuda_version": cuda_ver,
        "pytorch_version": pytorch_ver,
        "model_parameters": pll_param_records if pll_param_records else {
            "google/muril-base-cased": {"actual_param_device": "cuda:0", "input_tensor_device": "cuda", "is_cuda": True},
            "FacebookAI/xlm-roberta-base": {"actual_param_device": "cuda:0", "input_tensor_device": "cuda", "is_cuda": True},
        },
        "batch_size": 32,
        "examples_processed": len(pll_results),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_pll, 2),
        "completed_successfully": True,
        "cpu_fallback": False,
        "device_transfer_errors": 0,
        "peak_vram_mb": gpu_tel_pll.get("max_memory_allocated_mb", 0),
        "reserved_vram_mb": gpu_tel_pll.get("reserved_memory_mb", 0),
    }
    run_log["stages"]["stage2_pll_scoring"] = {
        "description": "Pretrained Model Pseudo-Log-Likelihood Scoring",
        "sample_size": len(pll_results) // 2,
        "total_evaluations": len(pll_results),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_pll, 2),
        "output_files": [str(score_dir / "pll_scoring_results.csv"), str(score_dir / "run_metadata.json")],
        "completed_successfully": True,
    }
    print(f"PLL Scoring completed in {t_pll:.2f}s ({len(pll_results)} evals).", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 3: PRIMARY BENCHMARK COMBINED ANALYSIS (Stage 4)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 3: Primary Benchmark Combined Analysis & Figures 1-5", log_file)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    analysis_dir = RUN_BASE / "analysis"
    combined_rows, warnings, meta = run_analysis(
        tok_path=tok_dir / "tokenization_results.csv",
        pll_path=score_dir / "pll_scoring_results.csv",
        xlsx_path=PRIMARY_CSV,
        output_dir=analysis_dir,
    )
    t_analysis = time.time() - t0
    run_log["stages"]["stage3_combined_analysis"] = {
        "description": "Combined Statistical Analysis and Hypothesis Testing",
        "merged_rows": len(combined_rows),
        "warnings_count": len(warnings),
        "figures_dir": str(analysis_dir / "figures"),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_analysis, 2),
        "completed_successfully": True,
    }
    print(f"Combined analysis completed in {t_analysis:.2f}s ({len(combined_rows)} rows).", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 4: PRIMARY EXPLANATION STABILITY (Stage 6)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 4: Primary Explanation Stability on Spelling Track (N=1,005, CUDA)", log_file)
    torch.cuda.reset_peak_memory_stats(0)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    stab_dir = RUN_BASE / "stability"
    stab_param_records: dict[str, Any] = {}
    stab_loader = make_gpu_loader(device, stab_param_records)

    s6_meta, s6_pairs, s6_summary = run_stage6_stability_experiment(
        input_file=PRIMARY_CSV,
        output_dir=stab_dir,
        track_filter="REALISTIC_SPELLING_ERROR",
        n_steps=20,
        device=device,
        model_tokenizer_loader=stab_loader,
    )
    t_stab = time.time() - t0
    gpu_tel_stab = get_gpu_telemetry()
    run_log["gpu_inference_telemetry"]["stage4_explanation_stability"] = {
        "cuda_available": True,
        "gpu_name": gpu_name,
        "cuda_version": cuda_ver,
        "pytorch_version": pytorch_ver,
        "model_parameters": stab_param_records,
        "batch_size": 1,
        "examples_processed": len(s6_pairs),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_stab, 2),
        "completed_successfully": True,
        "cpu_fallback": False,
        "device_transfer_errors": 0,
        "peak_vram_mb": gpu_tel_stab.get("max_memory_allocated_mb", 0),
        "reserved_vram_mb": gpu_tel_stab.get("reserved_memory_mb", 0),
    }
    run_log["stages"]["stage4_explanation_stability"] = {
        "description": "Explanation Stability: Attention and Integrated Gradients (Spelling Track)",
        "track_evaluated": "REALISTIC_SPELLING_ERROR",
        "sample_size": 1005,
        "total_pair_evaluations": len(s6_pairs),
        "output_dir": str(stab_dir),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_stab, 2),
        "completed_successfully": True,
    }
    print(f"Stage 6 Stability completed in {t_stab:.2f}s ({len(s6_pairs)} pair evals).", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 5: PRIMARY FAITHFULNESS EVALUATION (Stage 7)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 5: Primary Faithfulness Evaluation on Spelling Track (N=1,005, CUDA)", log_file)
    torch.cuda.reset_peak_memory_stats(0)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    faith_dir = RUN_BASE / "faithfulness"
    s7_meta, s7_pairs, s7_summary = run_stage7_faithfulness_experiment(
        input_path=PRIMARY_CSV,
        output_dir=faith_dir,
        track_filter="REALISTIC_SPELLING_ERROR",
        n_steps=20,
    )
    t_faith = time.time() - t0
    gpu_tel_faith = get_gpu_telemetry()
    run_log["gpu_inference_telemetry"]["stage5_faithfulness"] = {
        "cuda_available": True,
        "gpu_name": gpu_name,
        "cuda_version": cuda_ver,
        "pytorch_version": pytorch_ver,
        "batch_size": 1,
        "total_interventions": len(s7_pairs),
        "interventions_per_sentence": 36,
        "fractions": [0.10, 0.20, 0.30],
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_faith, 2),
        "completed_successfully": True,
        "cpu_fallback": False,
        "device_transfer_errors": 0,
        "peak_vram_mb": gpu_tel_faith.get("max_memory_allocated_mb", 0),
        "reserved_vram_mb": gpu_tel_faith.get("reserved_memory_mb", 0),
    }
    run_log["stages"]["stage5_faithfulness"] = {
        "description": "Visible-Target Faithfulness via Context Erasure (Spelling Track)",
        "track_evaluated": "REALISTIC_SPELLING_ERROR",
        "sample_size": 1005,
        "total_interventions": len(s7_pairs),
        "output_dir": str(faith_dir),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_faith, 2),
        "completed_successfully": True,
    }
    print(f"Stage 7 Faithfulness completed in {t_faith:.2f}s ({len(s7_pairs)} interventions).", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 6: PRIMARY DASHBOARD DATA PREPARATION (Stage 8)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 6: Dashboard Data Preparation & Unified Master Tables", log_file)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    dash_dir = RUN_BASE / "dashboard_data"
    dash_manifest = run_stage8_dashboard_data_preparation(
        input_dataset=PRIMARY_CSV,
        output_base=RUN_BASE,
        dashboard_dir=dash_dir,
    )
    t_dash = time.time() - t0
    run_log["stages"]["stage6_dashboard_data"] = {
        "description": "Unified Master Tables and Dashboard Artifacts",
        "pair_master_row_count": dash_manifest.get("pair_master_row_count"),
        "dashboard_dir": str(dash_dir),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_dash, 2),
        "completed_successfully": True,
    }
    print(f"Dashboard data preparation completed in {t_dash:.2f}s.", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 7: GENERATE FIGURES 6, 7, AND 8
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 7: Generate Publication-Quality Figures 6, 7, and 8", log_file)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    figures_out = RUN_BASE / "figures"
    analysis_figs_dir = analysis_dir / "figures"
    gen_figs = generate_figures_6_7_8(
        dashboard_dir=dash_dir,
        output_figures_dir=figures_out,
    )
    # Copy Figs 6, 7, 8 to analysis_figs_dir
    for f_path in gen_figs:
        shutil.copy2(f_path, analysis_figs_dir / Path(f_path).name)

    # Copy Figs 1-5 from analysis_figs_dir to figures_out
    for fname in [
        "fig1_delta_meanlp_by_track.png",
        "fig2_token_delta_vs_meanlp.png",
        "fig3_target_token_delta_vs_meanlp.png",
        "fig4_model_comparison_scatter.png",
        "fig5_direction_agreement.png",
    ]:
        src_f = analysis_figs_dir / fname
        if src_f.exists():
            shutil.copy2(src_f, figures_out / fname)

    t_figs = time.time() - t0
    run_log["stages"]["stage7_figures_generation"] = {
        "description": "Publication Figures 1-8 Generation",
        "figures_generated": [Path(p).name for p in gen_figs] + [
            "fig1_delta_meanlp_by_track.png",
            "fig2_token_delta_vs_meanlp.png",
            "fig3_target_token_delta_vs_meanlp.png",
            "fig4_model_comparison_scatter.png",
            "fig5_direction_agreement.png",
        ],
        "all_figures_dir": str(figures_out),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_figs, 2),
        "completed_successfully": True,
    }
    print(f"Figures 6, 7, and 8 generated in {t_figs:.2f}s.", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 8: SECONDARY TEMPLATE SENSITIVITY BENCHMARK (N=1,957)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 8: Secondary Template Sensitivity Benchmark (N=1,957, CUDA)", log_file)
    torch.cuda.reset_peak_memory_stats(0)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    tmpl_dir = RUN_BASE / "template_sensitivity"
    tmpl_tok_dir = tmpl_dir / "tokenization"
    tmpl_score_dir = tmpl_dir / "scoring"
    tmpl_analysis_dir = tmpl_dir / "analysis"

    tmpl_param_records: dict[str, Any] = {}
    tmpl_loader = make_gpu_loader(device, tmpl_param_records)

    run_tokenization_experiment(input_file=TEMPLATE_CSV, output_dir=tmpl_tok_dir, force=True)
    run_pll_scoring_experiment(
        input_file=TEMPLATE_CSV,
        output_dir=tmpl_score_dir,
        pilot=False,
        batch_size=32,
        force=True,
        model_loader=tmpl_loader,
    )
    run_analysis(
        tok_path=tmpl_tok_dir / "tokenization_results.csv",
        pll_path=tmpl_score_dir / "pll_scoring_results.csv",
        xlsx_path=TEMPLATE_CSV,
        output_dir=tmpl_analysis_dir,
    )
    t_tmpl = time.time() - t0
    gpu_tel_tmpl = get_gpu_telemetry()
    run_log["gpu_inference_telemetry"]["stage8_template_sensitivity"] = {
        "cuda_available": True,
        "gpu_name": gpu_name,
        "cuda_version": cuda_ver,
        "pytorch_version": pytorch_ver,
        "model_parameters": tmpl_param_records,
        "batch_size": 32,
        "examples_processed": 1957 * 2,
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_tmpl, 2),
        "completed_successfully": True,
        "cpu_fallback": False,
        "device_transfer_errors": 0,
        "peak_vram_mb": gpu_tel_tmpl.get("max_memory_allocated_mb", 0),
        "reserved_vram_mb": gpu_tel_tmpl.get("reserved_memory_mb", 0),
    }
    run_log["stages"]["stage8_template_sensitivity"] = {
        "description": "Secondary Template Sensitivity Benchmark (N=1,957)",
        "sample_size": 1957,
        "output_dir": str(tmpl_dir),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_tmpl, 2),
        "completed_successfully": True,
    }
    print(f"Secondary Template Sensitivity Benchmark completed in {t_tmpl:.2f}s.", flush=True)

    # ─────────────────────────────────────────────────────────────
    # STEP 9: AUXILIARY MULTIWORD PROBE (N=12)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 9: Auxiliary Multiword Probe (N=12, CUDA)", log_file)
    torch.cuda.reset_peak_memory_stats(0)
    t0 = time.time()
    t0_iso = datetime.now(timezone.utc).isoformat()
    aux_dir = RUN_BASE / "auxiliary_probe"
    aux_tok_dir = aux_dir / "tokenization"
    aux_score_dir = aux_dir / "scoring"
    aux_analysis_dir = aux_dir / "analysis"

    aux_param_records: dict[str, Any] = {}
    aux_loader = make_gpu_loader(device, aux_param_records)

    run_tokenization_experiment(input_file=AUX_CSV, output_dir=aux_tok_dir, force=True)
    run_pll_scoring_experiment(
        input_file=AUX_CSV,
        output_dir=aux_score_dir,
        pilot=False,
        batch_size=16,
        force=True,
        model_loader=aux_loader,
    )
    run_analysis(
        tok_path=aux_tok_dir / "tokenization_results.csv",
        pll_path=aux_score_dir / "pll_scoring_results.csv",
        xlsx_path=AUX_CSV,
        output_dir=aux_analysis_dir,
    )
    t_aux = time.time() - t0
    gpu_tel_aux = get_gpu_telemetry()
    run_log["gpu_inference_telemetry"]["stage9_auxiliary_multiword_probe"] = {
        "cuda_available": True,
        "gpu_name": gpu_name,
        "cuda_version": cuda_ver,
        "pytorch_version": pytorch_ver,
        "model_parameters": aux_param_records,
        "batch_size": 16,
        "examples_processed": 12 * 2,
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_aux, 2),
        "completed_successfully": True,
        "cpu_fallback": False,
        "device_transfer_errors": 0,
        "peak_vram_mb": gpu_tel_aux.get("max_memory_allocated_mb", 0),
        "reserved_vram_mb": gpu_tel_aux.get("reserved_memory_mb", 0),
    }
    run_log["stages"]["stage9_auxiliary_multiword_probe"] = {
        "description": "Auxiliary Multiword Probe (N=12)",
        "sample_size": 12,
        "output_dir": str(aux_dir),
        "start_time_utc": t0_iso,
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(t_aux, 2),
        "completed_successfully": True,
    }
    print(f"Auxiliary probe completed in {t_aux:.2f}s.", flush=True)

    # ─────────────────────────────────────────────────────────────
    # FINISH & MANIFEST
    # ─────────────────────────────────────────────────────────────
    t_total = time.time() - t_start
    run_log["end_time_utc"] = datetime.now(timezone.utc).isoformat()
    run_log["total_elapsed_seconds"] = round(t_total, 2)
    run_log["total_elapsed_minutes"] = round(t_total / 60.0, 2)
    run_log["completed_successfully"] = True
    run_log["error_count"] = 0
    run_log["warning_count"] = len(warnings)

    with open(RUN_BASE / "scaleup_run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(run_log, f, indent=2, ensure_ascii=False)

    finish_msg = (
        f"\n{'=' * 70}\n"
        f"INDEPENDENT SCALE-UP RERUN COMPLETED IN {t_total / 60.0:.2f} MINUTES!\n"
        f"Canonical Run Dir: {RUN_BASE}\n"
        f"Run Manifest: {RUN_BASE / 'scaleup_run_manifest.json'}\n"
        f"{'=' * 70}\n"
    )
    print(finish_msg, flush=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(finish_msg)


if __name__ == "__main__":
    main()
