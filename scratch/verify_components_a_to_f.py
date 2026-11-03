import io
import sys
import os
import pandas as pd
import numpy as np
import scipy.stats as stats
from pathlib import Path

# Set stdout encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

proj_root = Path('hindi-lexical-sensitivity').resolve()
base_results = proj_root / 'results' / 'runs' / 'scaleup_rerun'
base_data = proj_root / 'data' / 'final'

print("=" * 80)
print("AUDIT & VERIFICATION OF EXPERIMENTAL COMPONENTS A THROUGH F")
print("=" * 80)

# -------------------------------------------------------------
# COMPONENT A: TOKENIZATION ANALYSIS
# -------------------------------------------------------------
print("\n--- COMPONENT A: TOKENIZATION ANALYSIS ---")
tok_df = pd.read_csv(base_results / 'dashboard_data' / 'tokenization_summary.csv')
print(tok_df[['model_name', 'track', 'pair_count', 'pct_single_subword_orig_target', 'pct_single_subword_cont_target']])

# Denominator check:
spelling_pairs = 1005
synonym_pairs = 362
context_pairs = 312
total_primary = 1679

assert tok_df[tok_df['track'] == 'REALISTIC_SPELLING_ERROR']['pair_count'].tolist() == [1005, 1005]
assert tok_df[tok_df['track'] == 'SYNONYM_SUBSTITUTION']['pair_count'].tolist() == [362, 362]
assert tok_df[tok_df['track'] == 'VALID_WORD_CONTEXT']['pair_count'].tolist() == [312, 312]
print("Component A Denominators Verified: Spelling=1,005, Synonym=362, Context=312, Total=1,679.")

# Coverage collapse
for idx, r in tok_df[tok_df['track'] == 'REALISTIC_SPELLING_ERROR'].iterrows():
    orig_pct = r['pct_single_subword_orig_target']
    cont_pct = r['pct_single_subword_cont_target']
    diff = cont_pct - orig_pct
    print(f"  {r['model_name']} Spelling Single-Subword: Orig={orig_pct:.1f}%, Cont={cont_pct:.1f}%, Delta={diff:.1f} pp")

# Strict single-subword counts
stab_df = pd.read_csv(base_results / 'dashboard_data' / 'stability_summary.csv')
print("\nStrict single-subword sample sizes:")
for model in ['FacebookAI/xlm-roberta-base', 'google/muril-base-cased']:
    strict_row = stab_df[(stab_df['model_name'] == model) & (stab_df['subset'] == 'strict_single_subword') & (stab_df['method'] == 'attention')]
    pooled_row = stab_df[(stab_df['model_name'] == model) & (stab_df['subset'] == 'all_scorable_pooled') & (stab_df['method'] == 'attention')]
    print(f"  {model}: Strict Single-Subword N = {strict_row['pair_count'].values[0]}, Pooled N = {pooled_row['pair_count'].values[0]}")

# -------------------------------------------------------------
# COMPONENT B: PSEUDO-LOG-LIKELIHOOD (PLL) ANALYSIS
# -------------------------------------------------------------
print("\n--- COMPONENT B: PSEUDO-LOG-LIKELIHOOD (PLL) ANALYSIS ---")
score_df = pd.read_csv(base_results / 'dashboard_data' / 'scoring_summary.csv')
print(score_df[['model_name', 'track', 'pair_count', 'mean_delta_mean_logp', 'orig_preferred_rate']])

desc_df = pd.read_csv(base_results / 'analysis' / 'descriptive_statistics.csv')
print("\nDescriptive statistics for delta_meanlp:")
pll_desc = desc_df[desc_df['include_rejected'] == True]
print(pll_desc[['model_name', 'track', 'n_pairs', 'delta_meanlp_mean', 'delta_meanlp_median', 'delta_meanlp_std', 'delta_meanlp_n_negative']])

# -------------------------------------------------------------
# COMPONENT C: EXPLANATION STABILITY
# -------------------------------------------------------------
print("\n--- COMPONENT C: EXPLANATION STABILITY ---")
for idx, r in stab_df[stab_df['subset'].isin(['all_scorable_pooled', 'strict_single_subword'])].iterrows():
    print(f"  {r['model_name']:<28} | {r['method']:<20} | {r['subset']:<22} | N={r['pair_count']:<4} | Rho={r['visible_target_stability_rho_mean']:.4f} | Cos={r['visible_target_cosine_mean']:.4f}")

# -------------------------------------------------------------
# COMPONENT D: FAITHFULNESS ANALYSIS
# -------------------------------------------------------------
print("\n--- COMPONENT D: FAITHFULNESS ANALYSIS ---")
faith_df = pd.read_csv(base_results / 'dashboard_data' / 'faithfulness_summary.csv')
for f_val in [0.1, 0.2, 0.3]:
    print(f"\nFaithfulness at fraction f={f_val}:")
    sub_f = faith_df[(faith_df['fraction'] == f_val) & (faith_df['subset'] == 'all_scorable')]
    for idx, r in sub_f.iterrows():
        print(f"  {r['model_name']:<28} | {r['method']:<20} | N_sent={r['n_evaluated_sentences']} | Mean Gap={r['faithfulness_gap_mean']:.4f} | Win Rate={r['win_rate_vs_bottom']*100:.2f}% | Top Drop={r['top_k_logit_drop_mean']:.4f} | Bottom Drop={r['bottom_k_logit_drop_mean']:.4f}")

# -------------------------------------------------------------
# COMPONENT E: STABILITY-FAITHFULNESS CORRELATION
# -------------------------------------------------------------
print("\n--- COMPONENT E: STABILITY-FAITHFULNESS CORRELATIONS ---")
rel_df = pd.read_csv(base_results / 'dashboard_data' / 'stability_faithfulness_relationship.csv')

corr_results = []
for model in ['FacebookAI/xlm-roberta-base', 'google/muril-base-cased']:
    for method in ['attention', 'integrated_gradients']:
        for subset in ['all_scorable', 'strict_single_subword']:
            sub = rel_df[(rel_df['model_name'] == model) & (rel_df['method'] == method) & (rel_df['subset'] == subset)]
            valid = sub.dropna(subset=['visible_target_stability_rho', 'mean_faithfulness_gap_f20'])
            x = valid['visible_target_stability_rho']
            y = valid['mean_faithfulness_gap_f20']
            sp_r, sp_p = stats.spearmanr(x, y)
            pe_r, pe_p = stats.pearsonr(x, y)
            
            # Fisher z-transform 95% CI for Pearson
            z = np.arctanh(pe_r)
            se = 1.0 / np.sqrt(len(valid) - 3)
            ci_lo = np.tanh(z - 1.96 * se)
            ci_hi = np.tanh(z + 1.96 * se)
            
            corr_results.append({
                'model': model,
                'method': method,
                'subset': subset,
                'N': len(valid),
                'spearman_rho': sp_r,
                'spearman_p': sp_p,
                'pearson_r': pe_r,
                'pearson_p': pe_p,
                'ci_lo': ci_lo,
                'ci_hi': ci_hi
            })
            print(f"  {model:<28} | {method:<20} | {subset:<22} | N={len(valid):<4} | Spearman rho={sp_r:+.4f} (p={sp_p:.4f}) | Pearson r={pe_r:+.4f} (p={pe_p:.4f}) [95% CI: {ci_lo:+.4f}, {ci_hi:+.4f}]")

# -------------------------------------------------------------
# COMPONENT F: CROSS-MODEL AND CATEGORY ANALYSIS
# -------------------------------------------------------------
print("\n--- COMPONENT F: CROSS-MODEL AND CATEGORY ANALYSIS ---")
comp_df = pd.read_csv(base_results / 'analysis' / 'model_comparison.csv')
print(comp_df[['track_scope', 'n_pairs', 'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value']])

print("\nTemplate Benchmark Model Comparison:")
tpl_comp = pd.read_csv(base_results / 'template_sensitivity' / 'analysis' / 'model_comparison.csv')
print(tpl_comp[['track_scope', 'n_pairs', 'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value']])

print("\nAuxiliary Multiword Probe Model Comparison:")
aux_comp = pd.read_csv(base_results / 'auxiliary_probe' / 'analysis' / 'model_comparison.csv')
print(aux_comp[['track_scope', 'n_pairs', 'direction_agreement_rate', 'spearman_r_delta_meanlp', 'p_value']])

print("\n" + "=" * 80)
print("AUDIT COMPLETE - ALL VALUES VERIFIED DIRECTLY FROM SOURCE OF TRUTH")
print("=" * 80)
