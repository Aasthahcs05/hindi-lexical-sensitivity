import csv
import sys
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
AUDIT = ROOT / "audit_dataset_2000"

def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

primary = {r["pair_id"]: r for r in load_csv(FINAL / "PRIMARY_BENCHMARK_ADJUDICATED.csv")}
template = {r["pair_id"]: r for r in load_csv(FINAL / "TEMPLATE_SENSITIVITY_BENCHMARK.csv")}
aux = {r["pair_id"]: r for r in load_csv(FINAL / "AUXILIARY_MULTIWORD_PROBE.csv")}
adj_log = {r["pair_id"]: r for r in load_csv(FINAL / "ADJUDICATION_LOG.csv")}

accepted_2000 = {r["pair_id"]: r for r in load_csv(AUDIT / "DATASET_2000_ACCEPTED.csv")}
review_2000 = {r["pair_id"]: r for r in load_csv(AUDIT / "DATASET_2000_REVIEW_REQUIRED.csv")}
rejected_2000 = {r["pair_id"]: r for r in load_csv(AUDIT / "DATASET_2000_REJECTED.csv")}

print(f"ACCEPTED: {len(accepted_2000)}")
print(f"REVIEW: {len(review_2000)}")
print(f"REJECTED: {len(rejected_2000)}")
total_2000 = len(accepted_2000) + len(review_2000) + len(rejected_2000)
print(f"Total rows in audit sets: {total_2000}")

all_ids = set(accepted_2000.keys()) | set(review_2000.keys()) | set(rejected_2000.keys())
print(f"Unique IDs: {len(all_ids)}")

rev_in_primary = [pid for pid in review_2000 if pid in primary]
rev_in_template = [pid for pid in review_2000 if pid in template]
rev_in_aux = [pid for pid in review_2000 if pid in aux]
rev_in_adj = [pid for pid in review_2000 if pid in adj_log]

print("\n--- 309 REVIEW ROWS BREAKDOWN ---")
print(f"In Primary: {len(rev_in_primary)} -> {rev_in_primary}")
print(f"In Template: {len(rev_in_template)}")
print(f"In Aux: {len(rev_in_aux)} -> {rev_in_aux}")
print(f"In Adjudication Log: {len(rev_in_adj)} -> {rev_in_adj}")

rev_in_none = [pid for pid in review_2000 if pid not in primary and pid not in template and pid not in aux]
print(f"In None of the experiment sets: {len(rev_in_none)}")

issues_counter = Counter()
for pid in rev_in_none:
    issues_counter[review_2000[pid].get("audit_issues", "unknown")] += 1

print("\nIssues for rows in NONE of the experiment sets:")
for issue, count in issues_counter.most_common():
    print(f"  {issue}: {count}")

print("\nDetails of 16 review rows in NONE of the experiment sets:")
for pid in sorted(rev_in_none):
    r = review_2000[pid]
    in_adj = pid in adj_log
    adj_dec = adj_log[pid]["decision"] if in_adj else "NOT_IN_ADJ_LOG"
    adj_reason = adj_log[pid]["reason"] if in_adj else ""
    print(f"  {pid}: track={r['track']}, issue={r['audit_issues']}, adj={adj_dec}, reason={adj_reason}")

# Check template breakdown
tmpl_only = [pid for pid in template if pid not in primary]
print(f"\nIn Template but not Primary: {len(tmpl_only)}")
tmpl_only_in_rev = [pid for pid in tmpl_only if pid in review_2000]
print(f"  Of which are in 309 review: {len(tmpl_only_in_rev)}")
tmpl_only_in_acc = [pid for pid in tmpl_only if pid in accepted_2000]
print(f"  Of which are in 1676 accepted: {len(tmpl_only_in_acc)}")

# Check primary breakdown
prim_not_in_acc = [pid for pid in primary if pid not in accepted_2000]
print(f"\nIn Primary but not Accepted 1676: {len(prim_not_in_acc)} -> {prim_not_in_acc}")
