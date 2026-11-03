"""Script to test and validate notebook code cell execution."""

from __future__ import annotations

import json
from pathlib import Path
import sys

# Ensure UTF-8 output on Windows consoles to support Devanagari and SentencePiece tokens
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "scripts" / "lib") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "lib"))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"


def test_notebook(nb_path: Path) -> None:
    print(f"\n==========================================")
    print(f"Testing execution of: {nb_path.name}")
    print(f"==========================================")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    # Clean namespace for the notebook
    nb_ns: dict = {
        "__file__": str(nb_path),
        "__name__": "__main__",
    }

    code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
    for idx, cell in enumerate(code_cells, 1):
        code_str = "".join(cell["source"])
        # Skip interactive plt.show() blocking
        code_str = code_str.replace("plt.show()", "# plt.show()")
        try:
            exec(code_str, nb_ns)
            print(f"  [Cell {idx}/{len(code_cells)}] PASS")
        except Exception as e:
            print(f"  [Cell {idx}/{len(code_cells)}] FAIL: {e}")
            raise e

    print(f" {nb_path.name}: ALL CODE CELLS EXECUTED SUCCESSFULLY!")


def main() -> None:
    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    for nb in notebooks:
        test_notebook(nb)
    print("\n\n ALL NOTEBOOKS VERIFIED AND EXECUTE WITHOUT ERRORS!")


if __name__ == "__main__":
    main()
