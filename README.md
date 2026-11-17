# FairHire AI — Configuration Management Exercise

**Project:** FairHire AI: Counterfactual Fairness Testing for AI-Assisted Recruitment  
**Student:** Haidi Aly Fahmy  
**Course:** Software Quality Assurance / Software Testing  
**Implementation:** FairHire AI Live Protocol V2 (actual code from the project demo)

This repository contains the actual FairHire AI application, **not an invented demonstration application**. It generates controlled counterfactual candidate pairs, evaluates their model outputs, validates scores and recommendation formats, and exports audit results. It is a research/test application, not a hiring platform.

## Configuration items under version control

- **Application:** `fairhireai.py`, `run_live.py`, `view_results.py`, `inspect_live_run.py`, `open_latest_report.py`, `audit_dataset.py`
- **Tests:** `test_fairhireai.py`, `test_protocol_v2.py`, `test_research_guardrails.py`, `test_live_api_mock.py`
- **Input:** `recruitment_data.csv` (Kaggle-derived experimental dataset), `sample_candidates.csv`
- **Protocol and requirements:** `RESEARCH_PROTOCOL_AND_GUARDRAILS.md`, `CHANGELOG_PROTOCOL_V2.md`, instructions and demo walkthroughs
- **Configuration metadata:** `requirements.txt`, `.gitignore`, `.github/workflows/tests.yml`
- **CM records:** `CM_PLAN.md`, `CM_CHANGE_RECORD.md`, `CM_VERIFICATION.txt`

## Run the tests (offline; no API key)

```bash
python3 -m unittest discover -v -p 'test*.py'
python3 audit_dataset.py recruitment_data.csv
python3 run_live.py --dry-run --limit 2 --repeats 1
```

Python 3.10+ standard library only. The dry run does not contact the live API.

## Example version control operations

The ZIP includes an actual **local Git repository** and its development history for this **CM exercise only**. These commits were generated while preparing the assignment, **not** during the original November 16 experimental run. They are not evidence of prior code development. They show a source baseline, a separate CM documentation branch, a merge, and an annotated exercise tag.

```bash
git log --oneline --graph --all --decorate
git branch -a
git tag -n
git status
```

To connect to a GitHub repository that **you** create:

```bash
git remote add origin https://github.com/YOUR_USERNAME/FairHireAI_CM.git
git push -u origin main
git push origin --tags
```

A GitHub pull request and remote workflow run are **not** included: those require an actual GitHub remote. Do not claim either has already occurred.

## Documentation

Read `CM_PLAN.md` for configuration identification, baselining, change requests, build/verification, and auditing; and `CM_CHANGE_RECORD.md` for the example exercised here. The original `START_HERE_EXACT_STEPS.md` describes the full V2 app and optional live runs.
