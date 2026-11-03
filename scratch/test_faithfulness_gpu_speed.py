import sys
import os
import time
import torch
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.data.tokenization_experiment import load_dataset_rows
from src.analysis.hindi_faithfulness import (
    load_hindi_mlm_model_and_tokenizer,
    evaluate_pair_faithfulness,
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Device:", device)

dataset_path = Path("data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv")
rows = load_dataset_rows(dataset_path)
spelling_rows = [r for r in rows if r.get("track") == "REALISTIC_SPELLING_ERROR"]
print(f"Total spelling rows: {len(spelling_rows)}")

model_name = "google/muril-base-cased"
model, tokenizer = load_hindi_mlm_model_and_tokenizer(model_name=model_name, device=device)

# Warmup
evaluate_pair_faithfulness(spelling_rows[0], model, tokenizer, device, model_name, fractions=[0.10, 0.20, 0.30], n_steps=20)

t0 = time.time()
n_test = 5
for r in spelling_rows[1:1+n_test]:
    elig, recs, stab = evaluate_pair_faithfulness(r, model, tokenizer, device, model_name, fractions=[0.10, 0.20, 0.30], n_steps=20)

t1 = time.time()
print(f"Time for {n_test} pairs: {t1-t0:.2f}s ({ (t1-t0)/n_test:.3f} s/pair)")
