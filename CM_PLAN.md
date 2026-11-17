# Configuration Management Plan — FairHire AI

## 1. Scope

The CM baseline covers the Protocol V2 FairHire AI Python software, test suites, dataset input and hash, experimental rules, and documentation. This plan controls **changes to testing software**, not any real employer hiring decisions.

## 2. Configuration identification

| CI | Tracked items | Control approach |
|---|---|---|
| CI-01 Source | `fairhireai.py`, `run_live.py`, `view_results.py`, helpers | Git commit and review |
| CI-02 Test assets | `test*.py` | Run tests before merge |
| CI-03 Dataset | `recruitment_data.csv`, `sample_candidates.csv` | Keep source file; verify hash; document replacements |
| CI-04 Experiment contract | `RESEARCH_PROTOCOL_AND_GUARDRAILS.md`, prompts in source, `CHANGELOG_PROTOCOL_V2.md` | Explicit protocol version; never pool incompatible versions |
| CI-05 Tool configuration | `requirements.txt`, `.gitignore`, workflow YAML | Git changes; workflow validation |
| CI-06 CM records | `README.md`, `CM_PLAN.md`, `CM_CHANGE_RECORD.md` | Versioned evidence |

Runtime SQLite files, timestamped result folders, caches, and secrets are **not** source configuration items. They should remain outside Git. Results are preserved separately with run metadata if used as evidence; do not rewrite them to fit code changes.

## 3. Baselines and naming

- **Source baseline:** the actual supplied Protocol V2 code with its existing prompt/guardrail logic; use exercise tag `cm-exercise-v1.0` to identify this submission package.
- **Release protocol:** V1 and V2 are experimentally different protocols. Existing `CHANGELOG_PROTOCOL_V2.md` documents the specification change. The `cm-exercise-v1.0` **Git tag is not a claim that the research protocol is V1**.
- Development is on short `feature/...` branches; `main` retains merged changes.

## 4. Change-control workflow

1. Record issue, reason, affected configuration items, risk, and proposed acceptance criteria.
2. Create `feature/<change>` branch from `main`.
3. Edit only needed files and add/update relevant tests and documentation.
4. Execute `python3 -m unittest discover -v -p 'test*.py'` and dataset audit.
5. Review diff and merge into `main` only when tests pass. A one-person project uses self-review; external GitHub PR review requires a remote.
6. Tag any approved exercise/release baseline and update changelog.
7. Keep timestamped LLM results separately with protocol metadata, hashes and original responses. Never silently substitute model outputs or merge incompatible protocol results.

## 5. Version-control and access

Git is local source history; GitHub may be added as a remote by the student. `.gitignore` prevents `.env` secrets, Python caches, SQLite outputs, and generated result directories from being added by normal bulk staging. Always inspect `git status` before committing; ignored files can be force-added, so the operator remains responsible for protecting keys and personal data.

## 6. Verification and status accounting

- Offline unit/integration/mock tests: `python3 -m unittest discover -v -p 'test*.py'`.
- Dataset audit: `python3 audit_dataset.py recruitment_data.csv`.
- Execution-plan check: `python3 run_live.py --dry-run --limit 2 --repeats 1`.
- Continuous integration: `.github/workflows/tests.yml` runs the offline tests on pushes and pull requests **after** the repository is published to GitHub; the workflow is not evidence of a remote run.
- Status accounting: `git log`, `git status`, `git show`, `git tag`, `CM_CHANGE_RECORD.md`.

## 7. Audit and recovery

Use `git show cm-exercise-v1.0` to inspect the exercise baseline and `git checkout <commit>` (preferably in a separate worktree) to reproduce source files. Audit whether tests, dataset, prompt, and protocol identifiers match the intended experiment. Restore outputs from independently retained run folders rather than Git, as outputs are intentionally ignored.
