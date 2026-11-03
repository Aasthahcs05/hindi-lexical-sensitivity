"""Dump notebook 2 code cells to a UTF-8 text file for inspection."""
import json
from pathlib import Path

nb_path = Path("notebooks/02_subword_tokenization_and_alignment.ipynb")
out_path = Path("scripts/_nb2_cells_dump.txt")

nb = json.load(open(nb_path, encoding="utf-8"))

with open(out_path, "w", encoding="utf-8") as out:
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            out.write(f"=== CODE CELL {i} ===\n")
            out.write(src)
            out.write("\n\n")

print(f"Dumped to {out_path}")
