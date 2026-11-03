import json
import os
import sys
import io
import contextlib
import base64
from pathlib import Path
import pandas as pd
from IPython.display import Image, display

proj_root = Path('hindi-lexical-sensitivity').resolve()
os.chdir(proj_root)
sys.path.insert(0, str(proj_root))
sys.path.insert(0, str(proj_root / 'scripts' / 'lib'))

nb_path = proj_root / 'notebooks' / 'expanded_experimental_results.ipynb'

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Global execution namespace
nb_ns = {
    '__name__': '__main__',
    '__file__': str(nb_path),
}

code_cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
print(f"Executing {len(code_cells)} code cells in {nb_path.name}...")

exec_count = 1
for c_idx, cell in enumerate(code_cells, 1):
    src = ''.join(cell['source'])
    cell['execution_count'] = exec_count
    outputs = []
    
    # Custom display handler to capture display(...) calls
    def custom_display(*objs):
        for obj in objs:
            if isinstance(obj, pd.DataFrame):
                # Text and HTML representation
                outputs.append({
                    "data": {
                        "text/html": [obj.to_html()],
                        "text/plain": [obj.to_string()]
                    },
                    "execution_count": exec_count,
                    "metadata": {},
                    "output_type": "execute_result"
                })
            elif isinstance(obj, Image):
                # Image display
                img_path = obj.filename
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as img_f:
                        b64_data = base64.b64encode(img_f.read()).decode('utf-8')
                    outputs.append({
                        "data": {
                            "image/png": b64_data,
                            "text/plain": [f"<IPython.core.display.Image object>"]
                        },
                        "metadata": {},
                        "output_type": "display_data"
                    })
            else:
                outputs.append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [str(obj) + "\n"]
                })

    nb_ns['display'] = custom_display
    
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(src, nb_ns)
            
        stdout_str = stdout_buf.getvalue()
        stderr_str = stderr_buf.getvalue()
        
        if stdout_str:
            outputs.append({
                "name": "stdout",
                "output_type": "stream",
                "text": stdout_str.splitlines(keepends=True)
            })
        if stderr_str:
            outputs.append({
                "name": "stderr",
                "output_type": "stream",
                "text": stderr_str.splitlines(keepends=True)
            })
        print(f"  Cell {c_idx}/{len(code_cells)} executed successfully.")
    except Exception as e:
        print(f"  Cell {c_idx}/{len(code_cells)} FAILED: {type(e).__name__}: {e}")
        import traceback
        tb = traceback.format_exc()
        outputs.append({
            "ename": type(e).__name__,
            "evalue": str(e),
            "output_type": "error",
            "traceback": tb.splitlines(keepends=True)
        })
        cell['outputs'] = outputs
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        raise e
        
    cell['outputs'] = outputs
    exec_count += 1

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"All code cells executed and saved to {nb_path} with 0 errors!")

