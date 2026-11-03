import io
import sys
import os
import json
import time
import contextlib
from pathlib import Path

# Set UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

proj_root = Path('hindi-lexical-sensitivity').resolve()
os.chdir(proj_root)

if str(proj_root) not in sys.path:
    sys.path.insert(0, str(proj_root))
if str(proj_root / 'scripts' / 'lib') not in sys.path:
    sys.path.insert(0, str(proj_root / 'scripts' / 'lib'))

import openpyxl

notebook_order = [
    "01_dataset_curation_and_validation.ipynb",
    "02_subword_tokenization_and_alignment.ipynb",
    "03_mlm_pseudo_log_likelihood_scoring.ipynb",
    "04_tokenization_vs_model_plausibility.ipynb",
    "05_explainability_attention_vs_integrated_gradients.ipynb",
    "06_explanation_stability_and_faithfulness.ipynb",
    "07_paper_synthesis_and_dashboard_integration.ipynb",
    "expanded_experimental_results.ipynb"
]

print("=" * 80)
print("SEQUENTIAL CLEAN-KERNEL EXECUTION TEST OF ALL 8 NOTEBOOKS")
print("=" * 80)

execution_results = []

for nb_name in notebook_order:
    nb_path = proj_root / "notebooks" / nb_name
    print(f"\n--- Executing: {nb_name} ---")
    
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    total_code = len(code_cells)
    
    # Fresh isolated namespace for each notebook (clean kernel)
    clean_ns = {
        "__name__": "__main__",
        "__file__": str(nb_path),
    }
    
    start_t = time.time()
    failed_cell = None
    failed_error = None
    passed_count = 0
    
    for c_idx, cell in enumerate(code_cells, 1):
        source = "".join(cell["source"])
        # Prevent blocking interactive plot display
        source = source.replace("plt.show()", "# plt.show()")
        
        # Capture stdout/stderr in memory
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
                exec(source, clean_ns)
            passed_count += 1
        except Exception as e:
            failed_cell = c_idx
            failed_error = f"{type(e).__name__}: {e}"
            break
            
    elapsed = time.time() - start_t
    status = "FULL CLEAN-KERNEL PASS" if failed_cell is None else f"FAILED at cell {failed_cell}"
    
    execution_results.append({
        "notebook": nb_name,
        "total_cells": len(nb["cells"]),
        "code_cells": total_code,
        "passed_cells": passed_count,
        "status": status,
        "elapsed_seconds": round(elapsed, 2),
        "error": failed_error
    })
    print(f"  Result: {status} ({passed_count}/{total_code} code cells) in {elapsed:.2f}s")
    if failed_error:
        print(f"    Error details: {failed_error}")

print("\n" + "=" * 80)
print("SUMMARY TABLE OF NOTEBOOK EXECUTION VERIFICATION")
print("=" * 80)
print(f"{'Notebook':<50} | {'Status':<25} | {'Passed/Total':<12} | {'Time (s)':<8}")
print("-" * 105)
for r in execution_results:
    print(f"{r['notebook']:<50} | {r['status']:<25} | {str(r['passed_cells'])+'/'+str(r['code_cells']):<12} | {r['elapsed_seconds']:<8}")

all_pass = all(r["status"] == "FULL CLEAN-KERNEL PASS" for r in execution_results)
print("\nOVERALL SUITE STATUS:", "100% CLEAN-KERNEL PASS" if all_pass else "FAILURES DETECTED")

