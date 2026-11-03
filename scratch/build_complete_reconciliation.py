import csv
import sys
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
AUDIT = ROOT / "audit_dataset_2000"
ORIGINAL_CSV = Path(r"C:\Users\Friends\Downloads\hindi_lexical_sensitivity_cleaned - Sheet1 (1).csv")

# 1. Load Original CSV
with open(ORIGINAL_CSV, "r", encoding="utf-8") as f:
    orig_rows = list(csv.DictReader(f))

print(f"Original CSV loaded: {len(orig_rows)} rows")

# 2. Load Audit sets
acc_rows = {r["pair_id"]: r for r in csv.DictReader(open(AUDIT / "DATASET_2000_ACCEPTED.csv", encoding="utf-8"))}
rev_rows = {r["pair_id"]: r for r in csv.DictReader(open(AUDIT / "DATASET_2000_REVIEW_REQUIRED.csv", encoding="utf-8"))}
rej_rows = {r["pair_id"]: r for r in csv.DictReader(open(AUDIT / "DATASET_2000_REJECTED.csv", encoding="utf-8"))}

print(f"Audit Accepted: {len(acc_rows)}, Review: {len(rev_rows)}, Rejected: {len(rej_rows)}")

# 3. Load Frozen sets
prim_rows = {r["pair_id"]: r for r in csv.DictReader(open(FINAL / "PRIMARY_BENCHMARK_ADJUDICATED.csv", encoding="utf-8"))}
tmpl_rows = {r["pair_id"]: r for r in csv.DictReader(open(FINAL / "TEMPLATE_SENSITIVITY_BENCHMARK.csv", encoding="utf-8"))}
aux_rows = {r["pair_id"]: r for r in csv.DictReader(open(FINAL / "AUXILIARY_MULTIWORD_PROBE.csv", encoding="utf-8"))}
adj_rows = {r["pair_id"]: r for r in csv.DictReader(open(FINAL / "ADJUDICATION_LOG.csv", encoding="utf-8"))}

print(f"Frozen Primary: {len(prim_rows)}, Template: {len(tmpl_rows)}, Aux: {len(aux_rows)}, AdjLog: {len(adj_rows)}")

reconciliation_rows = []

for r in orig_rows:
    pid = r["pair_id"]
    track = r["track"]
    
    # Audit status
    if pid in acc_rows:
        audit_status = "ACCEPT"
        audit_issue = ""
        audit_reason = "Passed comprehensive automated quality audit as pristine minimal pair"
    elif pid in rev_rows:
        audit_status = "REVIEW"
        audit_issue = rev_rows[pid].get("audit_issues", "")
        audit_reason = rev_rows[pid].get("audit_reason", "")
    elif pid in rej_rows:
        audit_status = "REJECT"
        audit_issue = rej_rows[pid].get("audit_issues", "")
        audit_reason = rej_rows[pid].get("audit_reason", "")
    else:
        audit_status = "UNKNOWN"
        audit_issue = ""
        audit_reason = ""
        
    in_primary = pid in prim_rows
    in_template = pid in tmpl_rows
    in_auxiliary = pid in aux_rows
    in_adj_log = pid in adj_rows
    
    # Determine final adjudication status & decision & reason
    adj_entry = adj_rows.get(pid, {})
    adj_decision = adj_entry.get("decision", "")
    adj_log_reason = adj_entry.get("reason", "")
    
    # Final status categorization
    if in_primary:
        if pid in ["HC_1552", "HC_1619", "HC_1689"]:
            final_adjudication_status = "ADJUDICATED_RECLASSIFIED_PRIMARY"
            inclusion_decision = "INCLUDED_PRIMARY"
            decision_reason = (
                f"Adjudicated from review: {adj_log_reason} "
                f"Reclassified to VALID_WORD_CONTEXT and included in primary benchmark."
            )
            note = f"Reclassified from REALISTIC_SPELLING_ERROR to VALID_WORD_CONTEXT; Adjudication decision: {adj_decision}"
        else:
            final_adjudication_status = "ACCEPTED_PRIMARY"
            inclusion_decision = "INCLUDED_PRIMARY"
            decision_reason = "Clean minimal pair accepted by audit; included in primary scale-up benchmark."
            note = "Standard primary benchmark member."
    elif in_auxiliary:
        final_adjudication_status = "SEGREGATED_TO_AUXILIARY_PROBE"
        inclusion_decision = "INCLUDED_AUXILIARY_ONLY"
        decision_reason = f"Segregated to auxiliary multiword probe: {adj_log_reason or audit_reason}"
        note = f"Non-minimal/multiword perturbation or repeated target ambiguity; Adjudication decision: {adj_decision}"
    elif in_template:
        final_adjudication_status = "INCLUDED_IN_TEMPLATE_BENCHMARK"
        inclusion_decision = "INCLUDED_TEMPLATE_ONLY"
        decision_reason = (
            "Boilerplate carrier frame; excluded from primary benchmark to prevent syntactic collapse, "
            "retained in secondary template-sensitivity benchmark."
        )
        note = f"Template carrier frame ({audit_issue})"
    else:
        # Excluded from all experiment datasets
        if audit_status == "REJECT":
            final_adjudication_status = "REJECTED_AUDIT"
            inclusion_decision = "EXCLUDED"
            decision_reason = f"Rejected in Phase 1 audit: {audit_reason or audit_issue}"
            note = f"Technical/structural defect ({audit_issue})"
        elif in_adj_log:
            final_adjudication_status = f"ADJUDICATED_{adj_decision}"
            inclusion_decision = "EXCLUDED"
            decision_reason = f"Adjudicated exclusion: {adj_log_reason}"
            note = f"Excluded by adjudication decision: {adj_decision}"
        elif "interrogative_sentence" in audit_issue:
            final_adjudication_status = "EXCLUDED_PUNCTUATION_INCONSISTENCY"
            inclusion_decision = "EXCLUDED"
            decision_reason = "Sentence ends with question mark '?' rather than Devanagari danda '।'; excluded for punctuation consistency."
            note = "Interrogative sentence (? punctuation)"
        elif "multi_word_target_phrase" in audit_issue:
            final_adjudication_status = "EXCLUDED_MULTI_WORD_TARGET_PHRASE"
            inclusion_decision = "EXCLUDED"
            decision_reason = "Target perturbation is a multi-word phrase; ineligible for single-token MLM logit attribution."
            note = f"Multi-word target phrase: {audit_issue}"
        elif "ambiguous_target_alignment" in audit_issue:
            final_adjudication_status = "EXCLUDED_AMBIGUOUS_TARGET_ALIGNMENT"
            inclusion_decision = "EXCLUDED"
            decision_reason = "Target word occurs multiple times in sentence; creates token attribution ambiguity during explanation extraction."
            note = "Repeated target word in sentence"
        else:
            final_adjudication_status = "EXCLUDED_REVIEW_UNRESOLVED"
            inclusion_decision = "EXCLUDED"
            decision_reason = f"Excluded from benchmark: {audit_reason or audit_issue}"
            note = f"Review required: {audit_issue}"

    reconciliation_rows.append({
        "pair_id": pid,
        "original_category": track,
        "original_audit_status": audit_status,
        "in_primary": in_primary,
        "in_template_sensitivity": in_template,
        "in_auxiliary_probe": in_auxiliary,
        "in_adjudication_log": in_adj_log,
        "final_adjudication_status": final_adjudication_status,
        "inclusion_decision": inclusion_decision,
        "decision_reason": decision_reason,
        "duplicate_or_ambiguity_note": note,
    })

print(f"Generated {len(reconciliation_rows)} reconciliation rows.")

# Verify counts
inc_counts = Counter(r["inclusion_decision"] for r in reconciliation_rows)
print("\nInclusion Decision Counts:")
for k, v in inc_counts.items():
    print(f"  {k}: {v}")

status_counts = Counter(r["final_adjudication_status"] for r in reconciliation_rows)
print("\nFinal Adjudication Status Counts:")
for k, v in status_counts.items():
    print(f"  {k}: {v}")

# Write to COMPLETE_2000_ROW_RECONCILIATION.csv
out_path = FINAL / "COMPLETE_2000_ROW_RECONCILIATION.csv"
fields = [
    "pair_id",
    "original_category",
    "original_audit_status",
    "in_primary",
    "in_template_sensitivity",
    "in_auxiliary_probe",
    "in_adjudication_log",
    "final_adjudication_status",
    "inclusion_decision",
    "decision_reason",
    "duplicate_or_ambiguity_note",
]
with open(out_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(reconciliation_rows)

print(f"\nSuccessfully wrote: {out_path} ({out_path.stat().st_size} bytes)")
