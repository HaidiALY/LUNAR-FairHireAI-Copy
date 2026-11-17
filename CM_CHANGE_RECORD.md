# CM Exercise Change Record

## CR-CM-001 — Introduce configuration-management documentation and CI

**Status:** Implemented locally for the class exercise (not a GitHub PR).  
**Reason:** The professor's CM exercise requires evidence of basic files, commits, branching/merging and optional advanced automation.  
**Affected configuration items:** README, CM plan, change record, GitHub Actions YAML.  
**Application behavior:** Existing Python implementation and prompt/protocol logic were preserved.  
**Procedure:** Create a local source-code baseline on `main`; create `feature/cm-documentation`; add documentation and an offline test workflow; merge into `main`; tag `cm-exercise-v1.0`.  
**Acceptance criteria:** 29 offline tests pass; dataset audit works; dry-run does not make API calls.  
**Limitations:** Local demonstration only; no GitHub remote, pull request, required review or hosted CI run has been made.

## Actual research-protocol change (reference, NOT recreated)

`CHANGELOG_PROTOCOL_V2.md` describes the V1-to-V2 prompt specification update, including explicit scoring formula and thresholds. This CM exercise does not claim to recreate the user's historical V1→V2 commits or live API calls.
