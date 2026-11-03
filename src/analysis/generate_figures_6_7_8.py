"""Generate publication-quality Figures 6, 7, and 8 for the Hindi Lexical Sensitivity study.

Figure 6: Explanation stability (Spearman rho and Cosine similarity) comparing Attention vs. IG.
Figure 7: Faithfulness interventions (Faithfulness Gap and Win Rate vs Bottom-k) across fractions.
Figure 8: Decoupling of explanation stability and explanation faithfulness (scatter with OLS).
"""

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def _spearman_rho(x: list[float], y: list[float]) -> tuple[float, float]:
    """Compute Spearman rank correlation and approximate two-sided p-value."""
    n = len(x)
    if n < 3:
        return 0.0, 1.0

    def _rank(vals: list[float]) -> list[float]:
        sorted_pairs = sorted(enumerate(vals), key=lambda it: it[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and math.isclose(sorted_pairs[j][1], sorted_pairs[j + 1][1], rel_tol=1e-9, abs_tol=1e-9):
                j += 1
            avg_rank = (i + j + 2) / 2.0
            for k in range(i, j + 1):
                ranks[sorted_pairs[k][0]] = avg_rank
            i = j + 1
        return ranks

    rx = _rank(x)
    ry = _rank(y)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rho = 1.0 - (6.0 * d2) / (n * (n * n - 1))
    rho = max(-1.0, min(1.0, rho))

    if abs(abs(rho) - 1.0) < 1e-9:
        p_val = 0.0
    else:
        t_stat = rho * math.sqrt((n - 2) / max(1e-12, 1.0 - rho * rho))
        from scipy import stats
        p_val = 2.0 * (1.0 - stats.t.cdf(abs(t_stat), df=n - 2))

    return rho, p_val


def generate_figures_6_7_8(
    dashboard_dir: Path | str,
    output_figures_dir: Path | str,
) -> list[str]:
    """Generate high-resolution PNGs for Figures 6, 7, and 8."""
    dash_path = Path(dashboard_dir)
    out_dir = Path(output_figures_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "DejaVu Sans", "Helvetica"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 15,
        "figure.dpi": 300,
    })

    created: list[str] = []

    # ─────────────────────────────────────────────────────────────
    # FIGURE 6: Explanation Stability
    # ─────────────────────────────────────────────────────────────
    stab_csv = dash_path / "stability_summary.csv"
    if stab_csv.exists():
        with open(stab_csv, "r", encoding="utf-8") as f:
            stab_rows = list(csv.DictReader(f))

        # Filter to pooled scorable subset
        pooled_rows = [r for r in stab_rows if r.get("subset") == "all_scorable_pooled"]
        if not pooled_rows:
            pooled_rows = stab_rows

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300)

        models = ["FacebookAI/xlm-roberta-base", "google/muril-base-cased"]
        model_labels = ["XLM-RoBERTa", "MuRIL"]
        x = np.arange(len(models))
        width = 0.35

        attn_rhos = []
        ig_rhos = []
        attn_coss = []
        ig_coss = []

        for m in models:
            r_attn = next((r for r in pooled_rows if r["model_name"] == m and r["method"] == "attention"), None)
            r_ig = next((r for r in pooled_rows if r["model_name"] == m and r["method"] == "integrated_gradients"), None)

            attn_rhos.append(float(r_attn["visible_target_stability_rho_mean"]) if r_attn else 0.0)
            ig_rhos.append(float(r_ig["visible_target_stability_rho_mean"]) if r_ig else 0.0)

            attn_coss.append(float(r_attn["visible_target_cosine_mean"]) if r_attn else 0.0)
            ig_coss.append(float(r_ig["visible_target_cosine_mean"]) if r_ig else 0.0)

        # Panel (a): Rank Stability (Spearman rho)
        rects1 = ax1.bar(x - width / 2, attn_rhos, width, label="Self-Attention", color="#1976D2", alpha=0.9, edgecolor="black", linewidth=0.8)
        rects2 = ax1.bar(x + width / 2, ig_rhos, width, label="Integrated Gradients", color="#E64A19", alpha=0.9, edgecolor="black", linewidth=0.8)

        ax1.set_ylabel("Rank Stability (Mean Spearman ρ)")
        ax1.set_title("(a) Rank Stability under Spelling Noise", fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(model_labels, fontweight="bold")
        ax1.set_ylim(0, 1.05)
        ax1.legend(loc="upper right", framealpha=0.9)
        ax1.grid(True, linestyle="--", alpha=0.5, axis="y")

        # Value labels
        for rect in rects1:
            h = rect.get_height()
            ax1.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
        for rect in rects2:
            h = rect.get_height()
            ax1.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

        # Panel (b): Directional Stability (Cosine Similarity)
        rects3 = ax2.bar(x - width / 2, attn_coss, width, label="Self-Attention", color="#1976D2", alpha=0.9, edgecolor="black", linewidth=0.8)
        rects4 = ax2.bar(x + width / 2, ig_coss, width, label="Integrated Gradients", color="#E64A19", alpha=0.9, edgecolor="black", linewidth=0.8)

        ax2.set_ylabel("Directional Stability (Mean Cosine Sim)")
        ax2.set_title("(b) Vector Directional Stability", fontweight="bold")
        ax2.set_xticks(x)
        ax2.set_xticklabels(model_labels, fontweight="bold")
        ax2.set_ylim(0.7, 1.02)
        ax2.legend(loc="lower right", framealpha=0.9)
        ax2.grid(True, linestyle="--", alpha=0.5, axis="y")

        for rect in rects3:
            h = rect.get_height()
            ax2.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
        for rect in rects4:
            h = rect.get_height()
            ax2.annotate(f"{h:.3f}", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

        fig.suptitle("Visible-Target Explanation Stability under Devanagari Spelling Perturbations", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        fig6_path = out_dir / "fig6_explanation_stability.png"
        fig.savefig(fig6_path, bbox_inches="tight")
        plt.close(fig)
        created.append(str(fig6_path))

    # ─────────────────────────────────────────────────────────────
    # FIGURE 7: Faithfulness Interventions
    # ─────────────────────────────────────────────────────────────
    faith_csv = dash_path / "faithfulness_summary.csv"
    if faith_csv.exists():
        with open(faith_csv, "r", encoding="utf-8") as f:
            faith_rows = list(csv.DictReader(f))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.0), dpi=300)

        fractions = [0.10, 0.20, 0.30]
        frac_labels = ["10%", "20%", "30%"]

        models = [
            ("FacebookAI/xlm-roberta-base", "XLM-RoBERTa", "#1565C0", "#E65100"),
            ("google/muril-base-cased", "MuRIL", "#42A5F5", "#FF8A65"),
        ]

        markers = {"attention": "o", "integrated_gradients": "s"}
        linestyles = {"attention": "-", "integrated_gradients": "--"}

        for m_id, m_label, c_attn, c_ig in models:
            m_rows = [r for r in faith_rows if r["model_name"] == m_id and r.get("subset") in ("all_scorable_pooled", "pooled", None)]
            if not m_rows:
                m_rows = [r for r in faith_rows if r["model_name"] == m_id]

            # Attention gaps & win rates
            attn_gaps = []
            attn_wins = []
            for frac in fractions:
                r = next((x for x in m_rows if x["method"] == "attention" and math.isclose(float(x["fraction"]), frac, rel_tol=1e-3)), None)
                attn_gaps.append(float(r["faithfulness_gap_mean"]) if r else 0.0)
                attn_wins.append(float(r["win_rate_vs_bottom"]) * 100.0 if r else 0.0)

            # IG gaps & win rates
            ig_gaps = []
            ig_wins = []
            for frac in fractions:
                r = next((x for x in m_rows if x["method"] == "integrated_gradients" and math.isclose(float(x["fraction"]), frac, rel_tol=1e-3)), None)
                ig_gaps.append(float(r["faithfulness_gap_mean"]) if r else 0.0)
                ig_wins.append(float(r["win_rate_vs_bottom"]) * 100.0 if r else 0.0)

            # Panel (a): Faithfulness Gap
            ax1.plot(frac_labels, attn_gaps, marker=markers["attention"], linestyle=linestyles["attention"], color=c_attn, linewidth=2.0, markersize=7, label=f"{m_label} (Attention)")
            ax1.plot(frac_labels, ig_gaps, marker=markers["integrated_gradients"], linestyle=linestyles["integrated_gradients"], color=c_ig, linewidth=2.0, markersize=7, label=f"{m_label} (IG)")

            # Panel (b): Win Rate
            ax2.plot(frac_labels, attn_wins, marker=markers["attention"], linestyle=linestyles["attention"], color=c_attn, linewidth=2.0, markersize=7, label=f"{m_label} (Attention)")
            ax2.plot(frac_labels, ig_wins, marker=markers["integrated_gradients"], linestyle=linestyles["integrated_gradients"], color=c_ig, linewidth=2.0, markersize=7, label=f"{m_label} (IG)")

        ax1.axhline(0, color="black", linestyle=":", linewidth=1.0, alpha=0.7)
        ax1.set_xlabel("Context Erasure Fraction (f)")
        ax1.set_ylabel("Mean Faithfulness Gap (ΔS_top − ΔS_bottom)")
        ax1.set_title("(a) Context Erasure Faithfulness Gap", fontweight="bold")
        ax1.grid(True, linestyle="--", alpha=0.5)
        ax1.legend(loc="best", framealpha=0.9, fontsize=9)

        ax2.axhline(50.0, color="gray", linestyle=":", linewidth=1.0, label="Chance Level (50%)")
        ax2.set_xlabel("Context Erasure Fraction (f)")
        ax2.set_ylabel("Win Rate vs. Bottom-k Control (%)")
        ax2.set_title("(b) Intervention Win Rate vs. Bottom Control", fontweight="bold")
        ax2.set_ylim(20, 100)
        ax2.grid(True, linestyle="--", alpha=0.5)
        ax2.legend(loc="best", framealpha=0.9, fontsize=9)

        fig.suptitle("Explanation Faithfulness under Context Token Erasure Interventions", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        fig7_path = out_dir / "fig7_faithfulness_interventions.png"
        fig.savefig(fig7_path, bbox_inches="tight")
        plt.close(fig)
        created.append(str(fig7_path))

    # ─────────────────────────────────────────────────────────────
    # FIGURE 8: Stability vs. Faithfulness Decoupling
    # ─────────────────────────────────────────────────────────────
    rel_csv = dash_path / "stability_faithfulness_relationship.csv"
    if rel_csv.exists():
        with open(rel_csv, "r", encoding="utf-8") as f:
            rel_rows = list(csv.DictReader(f))

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

        configs = [
            ("FacebookAI/xlm-roberta-base", "XLM-RoBERTa", ax1),
            ("google/muril-base-cased", "MuRIL", ax2),
        ]

        method_styles = {
            "attention": {"color": "#1976D2", "label": "Self-Attention", "marker": "o"},
            "integrated_gradients": {"color": "#E64A19", "label": "Integrated Gradients", "marker": "s"},
        }

        for m_id, m_label, ax in configs:
            m_rows = [r for r in rel_rows if r["model_name"] == m_id]

            for method, style in method_styles.items():
                cur_rows = [
                    r for r in m_rows
                    if r["method"] == method
                    and r.get("visible_target_stability_rho")
                    and r.get("mean_faithfulness_gap_f20")
                ]
                xs = [float(r["visible_target_stability_rho"]) for r in cur_rows]
                ys = [float(r["mean_faithfulness_gap_f20"]) for r in cur_rows]

                if xs and ys:
                    ax.scatter(xs, ys, color=style["color"], marker=style["marker"], alpha=0.45, s=24, edgecolors="none")

                    rho, p_val = _spearman_rho(xs, ys)

                    # Trend line
                    x_arr = np.array(xs)
                    y_arr = np.array(ys)
                    if len(xs) > 1 and np.var(x_arr) > 1e-9:
                        slope, intercept = np.polyfit(x_arr, y_arr, 1)
                        x_line = np.linspace(min(xs), max(xs), 50)
                        y_line = slope * x_line + intercept
                        p_str = f"p={p_val:.3f}" if p_val >= 0.001 else "p<0.001"
                        ax.plot(x_line, y_line, color=style["color"], linewidth=1.8, label=f"{style['label']} (r_s={rho:+.3f}, {p_str})")
                    else:
                        ax.plot([], [], color=style["color"], label=f"{style['label']} (r_s={rho:+.3f})")

            ax.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
            ax.set_xlabel("Visible-Target Explanation Stability (Spearman ρ)")
            ax.set_ylabel("Mean Faithfulness Gap at f=0.20")
            ax.set_title(f"{m_label}", fontweight="bold")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend(loc="upper left", framealpha=0.9, fontsize=9)

        fig.suptitle("Decoupling of Explanation Stability and Faithfulness under Devanagari Perturbations", fontsize=14, fontweight="bold")
        fig.tight_layout(rect=[0, 0, 1, 0.95])
        fig8_path = out_dir / "fig8_stability_vs_faithfulness.png"
        fig.savefig(fig8_path, bbox_inches="tight")
        plt.close(fig)
        created.append(str(fig8_path))

    return created
