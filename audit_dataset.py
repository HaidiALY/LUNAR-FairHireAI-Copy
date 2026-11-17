"""Inspect the authentic Kaggle recruitment_data.csv without fabricating dataset claims."""
import csv,collections,hashlib,json,sys
from pathlib import Path
from fairhireai import load_candidates, FIELDS
p=Path(sys.argv[1] if len(sys.argv)>1 else "recruitment_data.csv")
if not p.exists(): raise SystemExit("Missing recruitment_data.csv. Download it from the official Kaggle link in README.md and copy it into this folder.")
with p.open(newline="",encoding="utf-8-sig") as f:
    reader=csv.DictReader(f); headers=reader.fieldnames; rows=list(reader)
records=load_candidates(p)
print(json.dumps({"file":str(p),"rows":len(rows),"columns":headers,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"blank_cells":sum(not str(v or "").strip() for row in rows for v in row.values()),"exact_duplicates":len(rows)-len({tuple(sorted(r.items())) for r in rows}),"gender_counts":dict(collections.Counter(row["Gender"] for row in rows)),"hiring_decision_counts":dict(collections.Counter(row.get("HiringDecision","UNAVAILABLE") for row in rows)),"validated_profiles":len(records),"notice":"HiringDecision is excluded from model prompts. Group codes 0/1 are not assumed to be gender labels."},indent=2))
