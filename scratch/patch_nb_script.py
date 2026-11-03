with open('hindi-lexical-sensitivity/scripts/build_expanded_notebook.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 6. Update Section 8.2 markdown
old_sec82 = '''### 8.2 Statistical Interpretation & Core Conclusion
1. **Decoupling across High Statistical Power**:
   - In the preliminary pilot ($N=20$), the absence of correlation could theoretically be attributed to low statistical power. In this expanded benchmark ($N=953$ and $N=808$ scorable pairs), statistical power is overwhelming for detecting weak effect sizes ($|r| \\\\ge 0.10$).
   - Across all evaluated configurations, **explanation stability does not predict explanation faithfulness**:
     - **XLM-RoBERTa Attention (Pooled)**: $r_s = +0.0607, p = 0.0612$ (Non-significant).
     - **XLM-RoBERTa IG (Pooled)**: $r_s = +0.0632, p = 0.0510$ (Non-significant).
     - **MuRIL Attention (Pooled)**: $r_s = -0.0442, p = 0.2099$ (Non-significant).
     - **MuRIL IG (Pooled)**: $r_s = +0.0214, p = 0.5442$ (Non-significant).
2. **Proper Statistical Nuance**:
   - We do not claim that a non-significant result constitutes mathematical proof of zero correlation across all deep learning architectures. Rather, within these evaluated models and benchmark, **stability to input noise cannot serve as a reliable empirical proxy for causal explanation faithfulness**.'''

new_sec82 = '''### 8.2 Statistical Interpretation & Core Conclusion
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
   - We do not claim that these empirical findings prove mathematical independence, establish causation, or rule out all sample-size limitations across all neural network architectures. Rather, within these evaluated models and benchmark, **stability to spelling perturbations cannot serve as a reliable empirical proxy for causal explanation faithfulness**.'''

if old_sec82 in text:
    text = text.replace(old_sec82, new_sec82)
    print('Updated Section 8.2 markdown successfully!')
else:
    print('Warning: old_sec82 still not found!')

with open('hindi-lexical-sensitivity/scripts/build_expanded_notebook.py', 'w', encoding='utf-8') as f:
    f.write(text)
