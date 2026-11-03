import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
FINAL = ROOT / "data" / "final"
AUDIT = ROOT / "audit_dataset_2000"

acc = set(r['pair_id'] for r in csv.DictReader(open(AUDIT / 'DATASET_2000_ACCEPTED.csv', encoding='utf-8')))
rev = set(r['pair_id'] for r in csv.DictReader(open(AUDIT / 'DATASET_2000_REVIEW_REQUIRED.csv', encoding='utf-8')))
rej = set(r['pair_id'] for r in csv.DictReader(open(AUDIT / 'DATASET_2000_REJECTED.csv', encoding='utf-8')))

for r in csv.DictReader(open(FINAL / 'ADJUDICATION_LOG.csv', encoding='utf-8')):
    pid = r['pair_id']
    origin = 'ACCEPTED' if pid in acc else ('REVIEW' if pid in rev else ('REJECTED' if pid in rej else 'UNKNOWN'))
    print(f"{pid}: origin={origin}, dec={r['decision']}, ret={r['retained_or_excluded']}")
