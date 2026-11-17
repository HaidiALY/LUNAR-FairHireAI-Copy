# FairHire AI — Configuration Management

**Project:** FairHire AI: Counterfactual Fairness Testing for AI-Assisted Recruitment  
**Student:** Haidi Aly Fahmy  
**Course:** Software Quality Assurance / Software Testing  
**Code Name:** LUNAR

## Project Overview

FairHire AI is my project for testing fairness and consistency in AI-assisted recruitment. The application compares how a Large Language Model evaluates candidates with the same qualifications but different demographic characteristics.

The goal is to identify whether changes in characteristics such as gender or nationality affect the model's scores or hiring recommendations. The application generates candidate pairs, processes model evaluations, compares the results, and produces reports to help identify potential inconsistencies.

For this Configuration Management assignment, I used Git and GitHub to organize the project files, track changes, and manage different versions of the application.

## Configuration Management

The repository contains the main application code, test files, datasets, and project documentation.

**Application files**
- `fairhireai.py`
- `run_live.py`
- `view_results.py`
- `inspect_live_run.py`
- `open_latest_report.py`
- `audit_dataset.py`

**Testing files**
- `test_fairhireai.py`
- `test_protocol_v2.py`
- `test_research_guardrails.py`
- `test_live_api_mock.py`

**Datasets**
- `recruitment_data.csv`
- `sample_candidates.csv`

**Project documentation and configuration**
- `RESEARCH_PROTOCOL_AND_GUARDRAILS.md`
- `CHANGELOG_PROTOCOL_V2.md`
- `requirements.txt`
- `.gitignore`
- `.github/workflows/tests.yml`

**Configuration Management documentation**
- `CM_PLAN.md`
- `CM_CHANGE_RECORD.md`
- `CM_VERIFICATION.txt`

## Version Control with Git and GitHub

I used Git and GitHub to manage changes to the project and maintain a history of the files.

The Configuration Management exercise includes:
- Creating and maintaining a Git repository.
- Tracking changes through commits.
- Using a separate branch for documentation updates.
- Merging changes into the main branch.
- Using Git tags to identify a project version.
- Configuring GitHub Actions for automated testing.

The Git history created for this exercise demonstrates these configuration management operations separately from the application's earlier development.

## Testing and Verification

The application includes automated tests to verify candidate-pair generation, evaluation processing, scoring rules, and research safeguards.

I ran the following commands to verify the application:

```bash
python3 -m unittest discover -v -p 'test*.py'
python3 audit_dataset.py recruitment_data.csv
python3 run_live.py --dry-run --limit 2 --repeats 1
```

All 29 automated tests passed.

The dataset audit and dry-run commands provide additional checks without requiring new live API requests.

## Project Results

As part of my FairHire AI project demonstration, I also conducted a live experiment using GPT-4.1-mini.

The experiment included 20 candidate pairs, two evaluation strategies, and two repetitions, resulting in 160 model evaluations.

The baseline strategy achieved 80% recommendation agreement, compared with 82.5% for the fairness-aware strategy. These results helped identify differences in the model's behavior, although they are not sufficient to establish overall model fairness.

## Conclusion

This exercise helped me apply Configuration Management concepts to my existing FairHire AI project. Using Git and GitHub allows me to organize source code, maintain version history, manage changes, and keep track of the tests and configurations associated with the application.