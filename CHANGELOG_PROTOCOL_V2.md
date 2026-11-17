# FairHireAI V1 → V2 — Transparent protocol amendment

Date: 2026-11-16. Project: GRAD 695 Applied Project.

## Evidence that motivated the change (original user-performed V1 live pilot)

The first reported successful API-contact pilot returned 8 provider response IDs, 6 valid parsed evaluations and 2 invalid evaluations. Both invalid outputs were for candidate pair P00961 under the baseline strategy, with Gender-coded A/B variants. They returned scores 81 and 76, both with recommendation `Interview`, violating the pre-existing thresholds that a score >=75 means `Hire`. Their text also included arithmetic mistakes. The exact registered formula gives **58** for SkillScore=19, InterviewScore=86 and ExperienceYears=8. These are observations from the user's V1 logs, **not results recreated in this ZIP**.

## Corrected specification mismatch

- **V1:** Both prompts said 'SkillScore 40%, InterviewScore 40%, ExperienceYears 20%' without spelling out exact arithmetic, inputs' 0–100 scales, rounding or the recommendation thresholds. The parser enforced thresholds that the prompt omitted.
- **V2:** Both baseline and fairness-aware prompts now include **the same explicit formula** `round(0.4 * SkillScore + 0.4 * InterviewScore + 2 * min(ExperienceYears, 10))`, the score scale, and `Hire >= 75`, `Interview 50–74`, `Reject < 50`. Both use the same job/context, same candidate data and schema. The fairness-aware prompt continues to add its one separate demographic instruction. Scoring weights and thresholds were **not changed**.
- **V2 addition:** A reference arithmetic score is stored alongside each evaluation and exported to `scoring_audit.csv` solely for transparent comparison with the *raw original model score*. This does not replace scores, change recommendation labels, alter validation status or remove arithmetic discrepancies from paired metrics.
- **Preserved:** CSV data and hash; Gender-code paired design; sampling seed 594; randomized requests; API adapter; parse guardrails; versioned result metadata; raw responses/errors; threshold-based rejection; no fixture fallback.
- **Provenance:** V2 records an updated `protocol_version` and `source_sha256` for new runs. All V1 data remains in its original location; no V1 run is overwritten or retrospectively described as V2.

## Consequence for interpretation

Report V1 as a **pilot with identified specification ambiguity**, and V2 as an **amended protocol**. Do not directly pool V1 and V2 comparison rates as if identical experimental conditions. V2 may still show incomplete outputs and mathematical discrepancies; those are legitimate findings, not automatic grounds for changing the code. This is a measurement of model response sensitivity under controlled conditions, not proof of legally actionable discrimination or universal fairness.
