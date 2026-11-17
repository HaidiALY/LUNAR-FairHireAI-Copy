# VIDEO 2 — REAL PROJECT DEMONSTRATION (8–9 minutes, must be <10)

**Purpose:** run the working application, display authentic model responses, report missing cases and arithmetic discrepancies, and explain exactly what the research can and cannot establish. The result values below are **not pre-specified**; read them from YOUR executed V2 report.

1. **00:00–00:45 — Introduction.** 'My project investigates whether changing only a coded demographic attribute changes GPT recruitment-support scores/recommendations and whether an explicit fairness-aware prompt affects differences. It is not used to make actual hiring decisions.'
2. **00:45–01:35 — Dataset.** Show `recruitment_data.csv`, run `python3 audit_dataset.py recruitment_data.csv`. Explain 1,500 synthetic records, nine professional/context attributes unchanged, and the source `HiringDecision` excluded.
3. **01:35–02:15 — Software checks.** Run `python3 -m unittest discover -v -p 'test*.py'` and show 29/29 local and mocked-API tests, not real model experiments.
4. **02:15–03:05 — Method and preflight.** Show `CHANGELOG_PROTOCOL_V2.md`. Explain V1's two invalid responses and transparent V2 clarification; no thresholds changed, no bias imposed. Run `python3 run_live.py --dry-run --limit 2 --repeats 1`. Explain 8 planned requests, no charges for dry-run.
5. **03:05–04:15 — Real OpenAI run.** Execute `python3 run_live.py --limit 2 --repeats 1 --model gpt-4.1-mini`. Type `LIVE`. STOP/PAUSE screen recording before private API key prompt. Resume only after entry. The run may take time; you may instead show saved evidence from YOUR new V2 run for a smooth video. Never show or speak the key.
6. **04:15–05:30 — Inspect success and missingness.** Run `python3 inspect_live_run.py`; note the *actual* provider response IDs, successful parsed evaluations, failed/incomplete cases, and eligible comparisons. If missing, explain the status honestly, not as a fabricated result. Run `python3 open_latest_report.py`.
7. **05:30–06:45 — Report and CSV proof.** Show HTML `report.html`, especially the LIVE provider provenance line and V2 protocol version, then `evaluations.csv`, `api_calls.csv`, `attempts.csv` and `scoring_audit.csv`. Explain arithmetic reference versus unmodified score and any observed mismatch.
8. **06:45–07:55 — Findings.** Read your *actual* agreement rates and score gaps in baseline/fairness-aware strategies. A nonzero score gap is observed cue sensitivity under these conditions, but possible causes include arithmetic errors and model variability; no gap is observed consistency under these limited conditions. Neither proves universal fairness/discrimination.
9. **07:55–08:45 — Conclusions.** Explain guardrails, versioning, transparency about the V1 correction, and future 20-pair/2-repeat experiment. The larger run schedules 160 paid requests before retries: `python3 run_live.py --limit 20 --repeats 2 --seed 594 --model gpt-4.1-mini`. Run it separately, only if the revised small pilot works and spending is acceptable.

## Real outputs to keep visible

`report.html`, `run_metadata.json` (shows V2), `evaluations.csv` (original model text), `api_calls.csv` (real response IDs), `attempts.csv` (retries/errors), `summary.csv` and `pairs.csv` (only eligible comparisons), `scoring_audit.csv` (arithmetic discrepancies recorded, not corrected).

Upload the YouTube video as Unlisted; paste the resulting URL into `SUBMISSION_VIDEO_2_LINK.txt`. No videos/links are pre-made in this package.
