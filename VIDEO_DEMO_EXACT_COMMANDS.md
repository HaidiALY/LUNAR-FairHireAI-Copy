# What to put on the recording screen: exact commands and narration checkpoints

## Recording 1 — CODE WALKTHROUGH (aim ~8 minutes, <10)
1. (0:00–0:40) Open `fairhireai.py` in VS Code, say: "FairHireAI measures sensitivity of a recruitment-support model to a coded demographic cue. It is research, not an actual hiring system."
2. (0:40–1:20) Open `recruitment_data.csv` / `audit_dataset.py`; run `python3 audit_dataset.py recruitment_data.csv`; explain original Kaggle 1,500 structured records.
3. (1:20–2:25) Show `load_candidates()`, `make_pairs()`, `validate_pair()`: strict numeric data and exact one-field differences; original hiring outcome omitted.
4. (2:25–3:20) Show `prompt()`; explain two planned strategies and fixed shared scoring rubric. No favorable result is hard-coded into live mode.
5. (3:20–4:40) Show `OpenAIAdapter._schema()` and `evaluate()` and endpoint `https://api.openai.com/v1/responses`. Explain that `OPENAI_API_KEY` comes from a secure environment variable inserted by `run_live.py`; NEVER show a key.
6. (4:40–5:35) Show `connect()`, `run()`: seeded ordering, retry handling, attempt logs, SQLite evidence, hashes and timestamps.
7. (5:35–6:25) Show `parse_response()`, `analyze()`, `export()`: invalid outputs excluded, paired gaps and recommendation agreement, CSV exports.
8. (6:25–7:30) Run `python3 -m unittest discover -v -p 'test*.py'`. Explain local/software and MOCK-API tests vs paid external testing.
9. (7:30–8:20) Show `view_results.py` and `inspect_live_run.py`; explain research integrity of output labeling.

## Recording 2 — LIVE PROJECT DEMO (aim ~8 minutes, <10)
1. (0:00–0:45) Introduce two research questions: does changing code 0 to 1 affect the score or recommendation; does fairness-aware prompting change sensitivity?
2. (0:45–1:35) Run `python3 audit_dataset.py recruitment_data.csv` and show 1,500 Kaggle synthetic candidate records.
3. (1:35–2:15) Run 23 software tests `python3 -m unittest discover -v -p 'test*.py'`.
4. (2:15–2:55) Run no-charge plan `python3 run_live.py --dry-run --limit 2 --repeats 1`; explain 8 planned model requests.
5. (2:55–4:10) Show already completed real run, or execute `python3 run_live.py --limit 2 --repeats 1 --model gpt-4.1-mini`; type LIVE, PAUSE recording while pasting NEW key only at hidden prompt, resume afterwards. Do not claim successful API work unless it returned actual model responses.
6. (4:10–5:45) Run `python3 open_latest_report.py`, show report provenance/model/eligible/incomplete, explain paired comparisons.
7. (5:45–6:40) Run `python3 inspect_live_run.py`, show `api_calls.csv` response IDs/token usage, `evaluations.csv` raw scores/explanations, `attempts.csv` errors.
8. (6:40–7:50) Read actual results on screen without making up scores. Zero gap only means no observed difference in tested conditions; nonzero gap indicates observed sensitivity. No universal fairness or legal claim follows.
9. (7:50–8:30) Explain safeguards and future scaling to 20 pairs × two variants × two strategies × 2 repeats = 160 paid calls.

## Demo tips
- Turn off notification popups before screen recording.
- Never reveal an API key. Do not type one after a terminal `%` or `$` shell prompt.
- If API billing returns an error, describe the failure and inspect logged evidence rather than silently using fixture scores.
- Open `.sqlite` files in a database viewer, not the VS Code plain-text editor. `report.html` is the easiest visual demonstration.
