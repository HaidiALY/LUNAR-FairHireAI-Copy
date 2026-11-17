# VIDEO 1 — CODE WALKTHROUGH (8–9 minutes, must be <10)

**Purpose:** explain the actual Python code and how the project is verified. Use VS Code and a terminal; no need to spend API credits while recording this video.

| Timing | What to SHOW | Suggested EXPLANATION |
| --- | --- | --- |
| 0:00–0:40 | VS Code folder and `fairhireai.py` | 'FairHireAI audits whether an LLM recruitment-support evaluation changes when only the coded demographic cue changes. We study the model rather than presuppose the outcome.' |
| 0:40–1:25 | `recruitment_data.csv`, `audit_dataset.py` | 'This is the original 1,500-row Kaggle synthetic dataset. I verify the schema, SHA-256 and missing and duplicate counts. I never send the source hiring outcome to the model.' Run `python3 audit_dataset.py recruitment_data.csv`. |
| 1:25–2:15 | `load_candidates()`, `make_pairs()`, `validate_pair()` | 'Input guardrails reject invalid numeric fields and direct identifiers. Each pair changes Gender 0 vs 1 and preserves nine other input fields exactly.' |
| 2:15–3:15 | `prompt()`, `reference_rubric_score()` | 'V1 exposed a mismatch: thresholds were enforced by the parser but omitted from the prompt. V2 states the exact same score formula and Hire/Interview/Reject thresholds in both strategies. Fairness-aware adds one separate instruction. The arithmetic reference is audit-only, never a replacement for model scores.' Show P00961 inputs giving reference score 58. |
| 3:15–4:30 | `OpenAIAdapter.__init__`, `_schema()`, `evaluate()` | 'This is the REAL OpenAI Responses API HTTP request, with strict JSON output schema, no local score substitution, model/response ID and token usage logging. The API key is read from the environment and securely entered by `run_live.py`; I will never display it.' |
| 4:30–5:35 | `run_live.py`, `connect()`, `run()` | 'The launcher prints the cost plan and requires confirmation. The engine randomizes trials with seed 594, records prompts and response attempts in SQLite, and preserves protocol and source checksums.' |
| 5:35–6:30 | `parse_response()`, `analyze()`, `export()` | 'The parser rejects a score/label mismatch without rescore or relabel. Eligible matched responses are compared by score gap and recommendation agreement. The new `scoring_audit.csv` flags arithmetic mistakes without altering the real outputs.' |
| 6:30–7:30 | `test_protocol_v2.py`, other tests | Run `python3 -m unittest discover -v -p 'test*.py'`. State: 'These 29 automated offline and mocked-API tests verify the software; they do not constitute live LLM fairness findings.' |
| 7:30–8:40 | `view_results.py`, `inspect_live_run.py` | Show how the HTML report, API metadata and arithmetic audit distinguish live evidence from mock tests. State that the old V1 pilot remains separately preserved and V2 results must be analyzed on their own. |

**Security:** pause the video during secret entry; ideally do not need any paid API requests in the code video. All tests use no paid API credentials.

**Do not say:** 'We made the model fair', 'The software corrects model scores', 'All responses will pass', or 'A difference proves discrimination'.
