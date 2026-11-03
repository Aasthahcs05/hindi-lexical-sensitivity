import json

nb_path = 'hindi-lexical-sensitivity/notebooks/expanded_experimental_results.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update Cell 0 Roadmap item 8
cell0_src = ''.join(nb['cells'][0]['source'])
cell0_src = cell0_src.replace(
    'Testing the core hypothesis of metric orthogonality ($p > 0.05$) across 1,005 spelling pairs (Table 6; Figure 8).',
    'Evaluating whether explanation stability predicts faithfulness across 1,005 spelling pairs (Table 6; Figure 8).'
)
nb['cells'][0]['source'] = [line + '\n' for line in cell0_src.split('\n')][:-1]

# Update Cell 29 title
cell29_src = ''.join(nb['cells'][29]['source'])
cell29_src = cell29_src.replace('Testing the Orthogonality Hypothesis', 'Evaluating the Relationship Between Stability and Faithfulness')
nb['cells'][29]['source'] = [line + '\n' for line in cell29_src.split('\n')][:-1]

# Update Cell 30 code
cell30_src = ''.join(nb['cells'][30]['source'])
old_code = """                # Statistical interpretation
                if sp_p > 0.05:
                    interp = "Non-Significant (p > 0.05)"
                elif sp_r < 0:
                    interp = "Weak Inverse Rank (rs < 0)"
                else:
                    interp = "Significant Positive (p <= 0.05)"""

new_code = """                # Statistical interpretation
                if sp_p <= 0.05 and sp_r < 0:
                    interp = f"Weak Inverse Rank (rs={sp_r:.4f}, p={sp_p:.4f})"
                elif pe_p <= 0.05 and pe_r < 0:
                    interp = f"Weak Inverse Linear (r={pe_r:.4f}, p={pe_p:.4f})"
                elif pe_p <= 0.05 and pe_r > 0:
                    interp = f"Weak Positive Linear (r={pe_r:.4f}, p={pe_p:.4f})"
                elif sp_p <= 0.05 and sp_r > 0:
                    interp = f"Significant Positive Rank (rs={sp_r:.4f}, p={sp_p:.4f})"
                else:
                    interp = "Non-Significant (p > 0.05)""""

if old_code in cell30_src:
    cell30_src = cell30_src.replace(old_code, new_code)
    nb['cells'][30]['source'] = [line + '\n' for line in cell30_src.split('\n')][:-1]
    print("Updated Cell 30 code.")
else:
    print("Warning: old_code not found in Cell 30.")

# Update Cell 32 markdown
cell32_new = """### 8.2 Statistical Interpretation & Core Conclusion
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
   - We do not claim that these empirical findings prove mathematical independence, establish causation, or rule out all sample-size limitations across all neural network architectures. Rather, within these evaluated models and benchmark, **stability to spelling perturbations cannot serve as a reliable empirical proxy for causal explanation faithfulness**."""

nb['cells'][32]['source'] = [line + '\n' for line in cell32_new.split('\n')]
print("Updated Cell 32 markdown.")

# Update Cell 40 markdown
cell40_src = ''.join(nb['cells'][40]['source'])
cell40_src = cell40_src.replace(
    '5. **Stability–Faithfulness Decoupling**: Across 1,005 spelling pairs, explanation stability does **not** predict explanation faithfulness ($p > 0.05$ across all conditions). Evaluating explanation methods solely on robustness risks selecting stably unfaithful rationales.',
    '5. **No Consistent Positive Stability–Faithfulness Association**: Across 1,005 Devanagari spelling pairs, there is no consistent positive association between explanation stability and faithfulness. Some weak negative associations occur for MuRIL Attention (pooled Pearson $r = -0.0790, p = 0.0248$; strict single-subword Spearman $\\rho = -0.1924, p = 0.0067$), while other combinations are non-significant. Robustness to spelling perturbations cannot be assumed to guarantee or predict causal explanation faithfulness.'
)
cell40_src = cell40_src.replace(
    'While $N=1,005$ spelling pairs provides ample power to detect weak effect sizes, future work should explore whether specialized architectural constraints can couple stability and faithfulness.',
    'While $N=1,005$ spelling pairs provides ample statistical power to evaluate small effect sizes, the results reflect empirical observations on the evaluated models and benchmark rather than an exhaustive proof across all deep learning architectures.'
)
nb['cells'][40]['source'] = [line + '\n' for line in cell40_src.split('\n')][:-1]
print("Updated Cell 40 markdown.")

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('Notebook successfully updated and saved!')
