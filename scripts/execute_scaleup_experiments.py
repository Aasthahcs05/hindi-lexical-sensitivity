"""Master Execution Script: Scale-Up Experiment Execution (N=1,679).

Preserves existing research methodology, frozen models (MuRIL, XLM-R),
tokenization procedures, PLL calculations, attention & Integrated Gradients procedures,
and explanation stability & faithfulness metrics.

Execution sequence:
1. Primary Benchmark (data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv, N=1,679):
   - Stage 2: Tokenization Experiment
   - Stage 3: Pretrained Model PLL Scoring (CUDA)
   - Stage 4: Combined Statistical Analysis & Figures 1-5
   - Stage 6: Explanation Stability on Spelling Errors (N=1,005, CUDA)
   - Stage 7: Visible-Target Faithfulness Evaluation (N=1,005, CUDA)
   - Stage 8: Dashboard Data Preparation & Synthesis
   - Figures 6, 7, 8: Publication-quality figures
2. Secondary Benchmark (data/final/TEMPLATE_SENSITIVITY_BENCHMARK.csv, N=1,957):
   - Stage 2 Tokenization & Stage 3 PLL Scoring & Combined Analysis
3. Auxiliary Multiword Probe (data/final/AUXILIARY_MULTIWORD_PROBE.csv, N=12):
   - Stage 2 Tokenization & Stage 3 PLL Scoring
4. Synchronization of primary scale-up outputs into outputs/ for manuscript and document builds.
"""

from __future__ import annotations

import csv
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from src.data.tokenization_experiment import run_tokenization_experiment
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

# Target run directory
RUN_BASE = PROJECT_ROOT / "results" / "runs" / "scaleup_1679"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def log_step(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {title}")
    print("=" * 70, flush=True)


def main() -> None:
    t_start = time.time()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Starting scale-up experiment execution on {device}...")
    if device.type == "cuda":
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")

    RUN_BASE.mkdir(parents=True, exist_ok=True)
    run_log: dict[str, Any] = {
        "start_time_utc": datetime.now(timezone.utc).isoformat(),
        "device": str(device),
        "device_name": torch.cuda.get_device_name(0) if device.type == "cuda" else "CPU",
        "stages": {},
    }

    # ─────────────────────────────────────────────────────────────
    # STEP 1: PRIMARY BENCHMARK TOKENIZATION (Stage 2)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 1: Primary Benchmark Tokenization (N=1,679)")
    t0 = time.time()
    tok_dir = RUN_BASE / "tokenization"
    tok_results, tok_meta, tok_summary = run_tokenization_experiment(
        input_file=PRIMARY_CSV,
        output_dir=tok_dir,
        force=True,
    )
    t_tok = time.time() - t0
    run_log["stages"]["stage2_tokenization"] = {
        "elapsed_seconds": round(t_tok, 2),
        "total_evaluations": len(tok_results),
        "output_csv": str(tok_dir / "tokenization_results.csv"),
    }
    print(f"Tokenization completed in {t_tok:.2f}s ({len(tok_results)} evals).")

    # ─────────────────────────────────────────────────────────────
    # STEP 2: PRIMARY BENCHMARK PLL SCORING (Stage 3)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 2: Primary Benchmark PLL Scoring (N=1,679, batch_size=32)")
    t0 = time.time()
    score_dir = RUN_BASE / "scoring"
    pll_results, pll_meta, pll_summary = run_pll_scoring_experiment(
        input_file=PRIMARY_CSV,
        output_dir=score_dir,
        pilot=False,
        batch_size=32,
        force=True,
    )
    t_pll = time.time() - t0
    run_log["stages"]["stage3_pll_scoring"] = {
        "elapsed_seconds": round(t_pll, 2),
        "total_evaluations": len(pll_results),
        "output_csv": str(score_dir / "pll_scoring_results.csv"),
    }
    print(f"PLL Scoring completed in {t_pll:.2f}s ({len(pll_results)} evals).")

    # ─────────────────────────────────────────────────────────────
    # STEP 3: PRIMARY BENCHMARK COMBINED ANALYSIS (Stage 4)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 3: Primary Benchmark Combined Analysis & Figures 1-5")
    t0 = time.time()
    analysis_dir = RUN_BASE / "analysis"
    combined_rows, warnings, meta = run_analysis(
        tok_path=tok_dir / "tokenization_results.csv",
        pll_path=score_dir / "pll_scoring_results.csv",
        xlsx_path=PRIMARY_CSV,
        output_dir=analysis_dir,
    )
    t_analysis = time.time() - t0
    run_log["stages"]["stage4_combined_analysis"] = {
        "elapsed_seconds": round(t_analysis, 2),
        "merged_rows": len(combined_rows),
        "warnings_count": len(warnings),
        "figures_dir": str(analysis_dir / "figures"),
    }
    print(f"Combined analysis completed in {t_analysis:.2f}s ({len(combined_rows)} rows).")

    # ─────────────────────────────────────────────────────────────
    # STEP 4: PRIMARY EXPLANATION STABILITY (Stage 6)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 4: Primary Explanation Stability on Spelling Track (N=1,005)")
    t0 = time.time()
    stab_dir = RUN_BASE / "stability"
    s6_meta, s6_pairs, s6_summary = run_stage6_stability_experiment(
        input_file=PRIMARY_CSV,
        output_dir=stab_dir,
        track_filter="REALISTIC_SPELLING_ERROR",
        n_steps=20,
        device=device,
    )
    t_stab = time.time() - t0
    run_log["stages"]["stage6_stability"] = {
        "elapsed_seconds": round(t_stab, 2),
        "total_pair_evaluations": len(s6_pairs),
        "output_dir": str(stab_dir),
    }
    print(f"Stage 6 Stability completed in {t_stab:.2f}s ({len(s6_pairs)} pair evals).")

    # ─────────────────────────────────────────────────────────────
    # STEP 5: PRIMARY FAITHFULNESS EVALUATION (Stage 7)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 5: Primary Faithfulness Evaluation on Spelling Track (N=1,005)")
    t0 = time.time()
    faith_dir = RUN_BASE / "faithfulness"
    s7_meta, s7_pairs, s7_summary = run_stage7_faithfulness_experiment(
        input_path=PRIMARY_CSV,
        output_dir=faith_dir,
        track_filter="REALISTIC_SPELLING_ERROR",
        n_steps=20,
    )
    t_faith = time.time() - t0
    run_log["stages"]["stage7_faithfulness"] = {
        "elapsed_seconds": round(t_faith, 2),
        "total_interventions": len(s7_pairs),
        "output_dir": str(faith_dir),
    }
    print(f"Stage 7 Faithfulness completed in {t_faith:.2f}s ({len(s7_pairs)} interventions).")

    # ─────────────────────────────────────────────────────────────
    # STEP 6: PRIMARY DASHBOARD DATA PREPARATION (Stage 8)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 6: Dashboard Data Preparation & Unified Master Tables")
    t0 = time.time()
    dash_dir = RUN_BASE / "dashboard_data"
    dash_manifest = run_stage8_dashboard_data_preparation(
        input_dataset=PRIMARY_CSV,
        output_base=RUN_BASE,
        dashboard_dir=dash_dir,
    )
    t_dash = time.time() - t0
    run_log["stages"]["stage8_dashboard_data"] = {
        "elapsed_seconds": round(t_dash, 2),
        "pair_master_row_count": dash_manifest.get("pair_master_row_count"),
        "dashboard_dir": str(dash_dir),
    }
    print(f"Dashboard data preparation completed in {t_dash:.2f}s.")

    # ─────────────────────────────────────────────────────────────
    # STEP 7: GENERATE FIGURES 6, 7, AND 8
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 7: Generate Publication-Quality Figures 6, 7, and 8")
    t0 = time.time()
    figures_out = RUN_BASE / "figures"
    analysis_figs_dir = analysis_dir / "figures"
    gen_figs = generate_figures_6_7_8(
        dashboard_dir=dash_dir,
        output_figures_dir=figures_out,
    )
    # Copy Figs 6, 7, 8 to analysis_figs_dir as well
    for f_path in gen_figs:
        shutil.copy2(f_path, analysis_figs_dir / Path(f_path).name)

    # Copy Figs 1-5 from analysis_figs_dir to figures_out
    for fname in ["fig1_delta_meanlp_by_track.png", "fig2_token_delta_vs_meanlp.png", "fig3_target_token_delta_vs_meanlp.png", "fig4_model_comparison_scatter.png", "fig5_direction_agreement.png"]:
        src_f = analysis_figs_dir / fname
        if src_f.exists():
            shutil.copy2(src_f, figures_out / fname)

    t_figs = time.time() - t0
    run_log["stages"]["figures_generation"] = {
        "elapsed_seconds": round(t_figs, 2),
        "figures_generated": [Path(p).name for p in gen_figs],
        "all_figures_dir": str(figures_out),
    }
    print(f"Figures 6, 7, and 8 generated in {t_figs:.2f}s.")

    # ─────────────────────────────────────────────────────────────
    # STEP 8: SECONDARY TEMPLATE SENSITIVITY BENCHMARK (N=1,957)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 8: Secondary Template Sensitivity Benchmark (N=1,957)")
    t0 = time.time()
    tmpl_dir = RUN_BASE / "template_sensitivity"
    tmpl_tok_dir = tmpl_dir / "tokenization"
    tmpl_score_dir = tmpl_dir / "scoring"
    tmpl_analysis_dir = tmpl_dir / "analysis"

    # Tokenization on Template benchmark
    run_tokenization_experiment(input_file=TEMPLATE_CSV, output_dir=tmpl_tok_dir, force=True)
    # PLL scoring on Template benchmark
    run_pll_scoring_experiment(input_file=TEMPLATE_CSV, output_dir=tmpl_score_dir, pilot=False, batch_size=32, force=True)
    # Combined analysis on Template benchmark
    run_analysis(
        tok_path=tmpl_tok_dir / "tokenization_results.csv",
        pll_path=tmpl_score_dir / "pll_scoring_results.csv",
        xlsx_path=TEMPLATE_CSV,
        output_dir=tmpl_analysis_dir,
    )
    t_tmpl = time.time() - t0
    run_log["stages"]["secondary_template_benchmark"] = {
        "elapsed_seconds": round(t_tmpl, 2),
        "output_dir": str(tmpl_dir),
    }
    print(f"Secondary Template Sensitivity Benchmark completed in {t_tmpl:.2f}s.")

    # ─────────────────────────────────────────────────────────────
    # STEP 9: AUXILIARY MULTIWORD PROBE (N=12)
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 9: Auxiliary Multiword Probe (N=12)")
    t0 = time.time()
    aux_dir = RUN_BASE / "auxiliary_probe"
    aux_tok_dir = aux_dir / "tokenization"
    aux_score_dir = aux_dir / "scoring"
    aux_analysis_dir = aux_dir / "analysis"

    run_tokenization_experiment(input_file=AUX_CSV, output_dir=aux_tok_dir, force=True)
    run_pll_scoring_experiment(input_file=AUX_CSV, output_dir=aux_score_dir, pilot=False, batch_size=16, force=True)
    run_analysis(
        tok_path=aux_tok_dir / "tokenization_results.csv",
        pll_path=aux_score_dir / "pll_scoring_results.csv",
        xlsx_path=AUX_CSV,
        output_dir=aux_analysis_dir,
    )
    t_aux = time.time() - t0
    run_log["stages"]["auxiliary_multiword_probe"] = {
        "elapsed_seconds": round(t_aux, 2),
        "output_dir": str(aux_dir),
    }
    print(f"Auxiliary probe completed in {t_aux:.2f}s.")

    # ─────────────────────────────────────────────────────────────
    # STEP 10: SYNCHRONIZE PRIMARY SCALE-UP RESULTS TO outputs/
    # ─────────────────────────────────────────────────────────────
    log_step("STEP 10: Synchronize Primary Scale-Up Outputs to outputs/")
    # Copy tokenization
    shutil.copytree(tok_dir, OUTPUTS_DIR / "tokenization", dirs_exist_ok=True)
    # Copy scoring
    shutil.copytree(score_dir, OUTPUTS_DIR / "scoring", dirs_exist_ok=True)
    # Copy analysis
    shutil.copytree(analysis_dir, OUTPUTS_DIR / "analysis", dirs_exist_ok=True)
    # Copy stability
    shutil.copytree(stab_dir, OUTPUTS_DIR / "hindi_explanation_stability", dirs_exist_ok=True)
    # Copy faithfulness
    shutil.copytree(faith_dir, OUTPUTS_DIR / "hindi_faithfulness", dirs_exist_ok=True)
    # Copy dashboard_data
    shutil.copytree(dash_dir, OUTPUTS_DIR / "dashboard_data", dirs_exist_ok=True)
    # Copy figures to refined paper figures dir as well
    refined_figs_dir = PROJECT_ROOT / "research_paper" / "refined" / "figures"
    refined_figs_dir.mkdir(parents=True, exist_ok=True)
    for fig_file in figures_out.glob("*.png"):
        shutil.copy2(fig_file, refined_figs_dir / fig_file.name)
        shutil.copy2(fig_file, OUTPUTS_DIR / "analysis" / "figures" / fig_file.name)

    t_total = time.time() - t_start
    run_log["end_time_utc"] = datetime.now(timezone.utc).isoformat()
    run_log["total_elapsed_seconds"] = round(t_total, 2)
    run_log["total_elapsed_minutes"] = round(t_total / 60.0, 2)
    run_log["completed_successfully"] = True

    # Save run manifest
    with open(RUN_BASE / "scaleup_run_manifest.json", "w", encoding="utf-8") as f:
        json.dump(run_log, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"SCALE-UP EXPERIMENT EXECUTION COMPLETED IN {t_total / 60.0:.2f} MINUTES!")
    print(f"Canonical Run Dir: {RUN_BASE}")
    print(f"Run Manifest: {RUN_BASE / 'scaleup_run_manifest.json'}")
    print("=" * 70, flush=True)


if __name__ == "__main__":
    main()
