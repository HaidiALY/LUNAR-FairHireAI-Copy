#!/usr/bin/env bash
set -euo pipefail
python3 audit_dataset.py recruitment_data.csv
python3 -m unittest -v test_fairhireai.py
python3 fairhireai.py recruitment_data.csv --adapter fixture --sampling random --limit 20 --repeats 2 --seed 594 --db offline_control.sqlite --out results_offline_control
python3 view_results.py results_offline_control
python3 fairhireai.py recruitment_data.csv --adapter injected --sampling random --limit 20 --repeats 2 --seed 594 --db offline_injected.sqlite --out results_offline_injected
python3 view_results.py results_offline_injected
printf '\nOffline tests complete. Open the generated report.html files.\n'
