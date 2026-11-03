import sys
import os
import time
import torch
from pathlib import Path

sys.path.insert(0, os.getcwd())

from src.data.tokenization_experiment import load_dataset_rows
from src.analysis.hindi_faithfulness import (
    load_hindi_mlm_model_and_tokenizer,
    prepare_visible_target_input,
    calculate_visible_target_score,
    extract_visible_target_attention,
    extract_visible_target_integrated_gradients,
    compute_k_for_fraction,
    DEFAULT_FRACTIONS,
)
import json, random, hashlib

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = "google/muril-base-cased"
model, tokenizer = load_hindi_mlm_model_and_tokenizer(model_name=model_name, device=device)

dataset_path = Path("data/final/PRIMARY_BENCHMARK_ADJUDICATED.csv")
rows = load_dataset_rows(dataset_path)
row = [r for r in rows if r.get("track") == "REALISTIC_SPELLING_ERROR"][0]

prep = prepare_visible_target_input(row["original_sentence"], row["target_original"], tokenizer, device)
input_ids = prep["input_ids"]
attention_mask = prep["attention_mask"]
target_indices = prep["target_indices"]
target_token_ids = prep["target_token_ids"]
context_indices = prep["context_indices"]

attn = extract_visible_target_attention(model, input_ids, attention_mask, target_indices, context_indices)
scores = attn["normalized_attentions"]

# Unbatched execution
mask_token_id = getattr(tokenizer, "mask_token_id", 103)
paired = sorted(zip(context_indices, scores), key=lambda x: x[1], reverse=True)
ranked_indices = [idx for idx, _ in paired]
n_context = len(context_indices)

# Prepare intervention items
items = []
for frac in DEFAULT_FRACTIONS:
    k = compute_k_for_fraction(n_context, frac)
    top_k_indices = ranked_indices[:k]
    bottom_k_indices = ranked_indices[-k:]
    seed_str = f"{row['pair_id']}_original_attention_{frac}"
    seed_val = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**31 - 1)
    rng = random.Random(seed_val)
    random_k_indices = rng.sample(context_indices, k)
    for int_type, chosen in [("top_k", top_k_indices), ("bottom_k", bottom_k_indices), ("random_k", random_k_indices)]:
        items.append((frac, k, int_type, chosen))

# Unbatched
t0 = time.time()
unbatched_results = []
for frac, k, int_type, chosen in items:
    intervened_ids = input_ids.clone()
    for idx in chosen:
        if idx not in target_indices:
            intervened_ids[0, idx] = mask_token_id
    res = calculate_visible_target_score(model, intervened_ids, attention_mask, target_indices, target_token_ids)
    unbatched_results.append(res["mean_logit"])
t_unbatched = time.time() - t0

# Batched
t0 = time.time()
batch_ids = []
for frac, k, int_type, chosen in items:
    cur_ids = input_ids.clone()
    for idx in chosen:
        if idx not in target_indices:
            cur_ids[0, idx] = mask_token_id
    batch_ids.append(cur_ids[0])

batch_ids_tensor = torch.stack(batch_ids, dim=0) # [9, seq_len]
batch_mask_tensor = attention_mask.expand(len(batch_ids), -1)

with torch.no_grad():
    out = model(input_ids=batch_ids_tensor, attention_mask=batch_mask_tensor)
    logits = out.logits
    batched_results = []
    for i in range(len(items)):
        sub_logits = [logits[i, pos, tid].item() for pos, tid in zip(target_indices, target_token_ids)]
        batched_results.append(sum(sub_logits) / len(target_indices))
t_batched = time.time() - t0

print(f"Unbatched time: {t_unbatched*1000:.2f}ms")
print(f"Batched time:   {t_batched*1000:.2f}ms (Speedup: {t_unbatched/t_batched:.2f}x)")
diffs = [abs(u - b) for u, b in zip(unbatched_results, batched_results)]
print(f"Max diff: {max(diffs):.8f}")
