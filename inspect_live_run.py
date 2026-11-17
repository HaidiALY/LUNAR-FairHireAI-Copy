"""Inspect local OpenAI evidence; does NOT send any API calls."""
import argparse
import csv
import json
from pathlib import Path

def rows(path):
    if not path.exists():
        return []
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))

def newest():
    folders=[p for p in Path('.').glob('results_live_openai_*/') if (p/'run_metadata.json').exists()]
    if not folders:
        raise SystemExit('No live results in this folder yet. Run python3 run_live.py --limit 2 --repeats 1')
    return max(folders,key=lambda p:p.name)

def main():
    p=argparse.ArgumentParser(description='Check whether a LIVE API run actually completed')
    p.add_argument('results_folder', nargs='?', help='Default: newest results_live_openai_... folder')
    a=p.parse_args()
    folder=Path(a.results_folder) if a.results_folder else newest()
    metadata=json.loads((folder/'run_metadata.json').read_text(encoding='utf-8'))
    evaluations=rows(folder/'evaluations.csv')
    calls=rows(folder/'api_calls.csv')
    summary=rows(folder/'summary.csv')
    audit=rows(folder/'scoring_audit.csv')
    status_ok=[r for r in evaluations if r.get('status')=='ok']
    missing=[r for r in evaluations if r.get('status')!='ok']
    response_ids={r['response_id'] for r in calls if r.get('response_id')}
    print('Results folder:',folder.resolve())
    print('Evaluator:',metadata.get('adapter'))
    if not str(metadata.get('adapter','')).startswith('openai_responses::'):
        raise SystemExit('NOT A LIVE API RUN: provenance is not openai_responses')
    print('Planned individual model evaluations:',metadata.get('planned_evaluations'))
    print('Successful parsed evaluations:',len(status_ok))
    print('Incomplete/failed evaluations:',len(missing))
    print('Provider response IDs recorded:',len(response_ids))
    for s in summary:
        print(f"  {s['strategy']}: eligible paired comparisons={s['eligible']}; incomplete={s['incomplete']}; "+
              f"recommendation agreement={s['agreement_rate']}; mean absolute score gap={s['mean_absolute_score_gap']}")
    compared=[r for r in audit if r.get('rubric_arithmetic_match') in ('True','False')]
    mismatches=[r for r in compared if r.get('rubric_arithmetic_match')=='False']
    if audit:
        print('V2 scoring arithmetic audit (unmodified original model scores):',
              len(mismatches),'mismatches among',len(compared),'interpretable outputs')
        print('Note: audit-only mismatches are NOT silently corrected or excluded.')
    if missing:
        print('WARNING: Some model calls failed or returned invalid output. Check evaluations.csv and attempts.csv.')
    if not response_ids:
        print('WARNING: No provider response IDs. Do not claim verified live model results without checking the logs.')
    print('Inspect the exact responses in evaluations.csv and provider records in api_calls.csv')
    report=folder/'report.html'
    if report.exists(): print('Report:',report.resolve())
    print('A small experiment does NOT prove or disprove general model fairness.')

if __name__=='__main__':
    main()
