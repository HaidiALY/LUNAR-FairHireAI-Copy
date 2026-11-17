"""Create a standalone, dependency-free HTML viewer from actual CSV run outputs."""
import argparse
import csv
import html
import json
from pathlib import Path

def load(path):
    with path.open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def generate(result_dir):
    folder=Path(result_dir)
    summary=load(folder/'summary.csv')
    pairs=load(folder/'pairs.csv')
    evals=load(folder/'evaluations.csv')
    metadata_path=folder/'run_metadata.json'
    metadata=json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path.exists() else {}
    if not summary or not pairs or not evals:
        raise ValueError('Empty results: execute fairhireai.py first')
    adapters=set()
    statuses={}
    for r in evals:
        statuses[r['status']]=statuses.get(r['status'],0)+1
        if r.get('raw_response'):
            try:
                raw=json.loads(r['raw_response'])
                adapters.add('deterministic test' if 'fixture' in raw.get('explanation','').lower() or 'synthetic injected' in raw.get('explanation','').lower() else 'other')
            except (ValueError,TypeError):pass
    # Explicitly label the output according to run provenance in the database if available.
    disclaimer='Outputs are from a selected evaluator. Deterministic or injected fixtures are NOT live LLM findings.'
    adapter=metadata.get('adapter','unknown (legacy export)')
    if adapter.startswith(('rule_based_fixture','injected_fault_fixture')):
        disclaimer='OFFLINE SIMULATION. These results verify the software behavior; they are not an experiment with a real generative model.'
    elif adapter.startswith('openai_responses::'):
        disclaimer=('LIVE OPENAI API OBSERVATIONS. Scores were returned by the selected external model. '
                    'Conclusions are restricted to this model, this small synthetic sample, prompts and run date. '
                    'A score difference alone does not establish unlawful discrimination; zero differences do not prove universal fairness.')
    api_calls=load(folder/'api_calls.csv') if (folder/'api_calls.csv').exists() else []
    audit=load(folder/'scoring_audit.csv') if (folder/'scoring_audit.csv').exists() else []
    def esc(v):return html.escape('' if v is None else str(v))
    def table(rows,columns,max_rows=50):
        heads=''.join(f'<th>{esc(c)}</th>' for c in columns)
        body=''.join('<tr>'+''.join(f'<td>{esc(r.get(c,""))}</td>' for c in columns)+'</tr>' for r in rows[:max_rows])
        return f'<div class="scroll"><table><thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table></div>'
    cards=''.join(f'<article><small>{esc(r["strategy"])}</small><h2>{esc(r["eligible"])} pairs</h2><p>Agreement: {esc(r["agreement_rate"])} · Mean |gap|: {esc(r["mean_absolute_score_gap"])} · Flags: {esc(r["flagged"])}</p></article>' for r in summary)
    provenance=(f'<p><b>Dataset SHA-256:</b> <code>{esc(metadata.get("dataset_checksum","missing"))}</code><br>'
                f'<b>Code SHA-256:</b> <code>{esc(metadata.get("source_sha256","missing"))}</code><br>'
                f'<b>Protocol version:</b> {esc(metadata.get("protocol_version","legacy"))} · '
                f'<b>Planned evaluations:</b> {esc(metadata.get("planned_evaluations","unknown"))}</p>')
    usage_section=''
    if api_calls:
        token_total=sum(int(r['total_tokens']) for r in api_calls if r.get('total_tokens') not in ('',None))
        success=sum(bool(r.get('response_id')) for r in api_calls)
        usage_section=(f'<section><h2>Live provider evidence</h2><p>{success} recorded response IDs; '
                       f'{token_total:,} total API tokens recorded (where reported). '
                       'Usage is not a dollar charge estimate.</p>'+table(api_calls,
                       ['pair_id','strategy','repeat','variant','resolved_model','response_id','total_tokens','response_status','latency_s'],30)+'</section>')
    audit_section=''
    if audit:
        compared=[r for r in audit if r.get('rubric_arithmetic_match') in ('True','False')]
        discrepant=[r for r in compared if r['rubric_arithmetic_match']=='False']
        audit_section=(f'<section><h2>Independent scoring arithmetic audit (V2)</h2>'
            f'<p><b>{len(discrepant)} of {len(compared)}</b> interpretable raw scores differ from the '
            'documented fixed rubric. This is an <b>audit only</b>: scores and recommendations were '
            'not corrected or changed, and audit discrepancies do not automatically exclude a comparison. '
            'See scoring_audit.csv for all records, including invalid model responses.</p>'+
            table(audit,['pair_id','strategy','repeat','variant','status',
                'reference_rubric_score','original_model_returned_score',
                'difference_model_minus_reference','rubric_arithmetic_match','model_response_error'],25)+
            '</section>')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FairHireAI — Local Run Evidence</title>
<style>body{{font:15px/1.5 system-ui,Arial;background:#f5f7fb;color:#1c2d37;max-width:1120px;margin:auto;padding:26px}}h1{{color:#123f4d}}header,article,section{{background:white;padding:22px;border-radius:12px;box-shadow:0 2px 9px #183c4c12;margin-bottom:20px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}}.cards article{{margin:0}}small{{color:#407663;font-weight:700}}h2{{margin:6px 0}}.note{{border-left:5px solid #c07b28;background:#fff8e8;padding:15px}}table{{border-collapse:collapse;width:100%;min-width:650px}}th,td{{padding:8px 10px;border-bottom:1px solid #e7e8ed;text-align:left;white-space:normal;max-width:340px;font-size:13px;vertical-align:top}}th{{background:#e7f0ed;position:sticky;top:0}}.scroll{{overflow:auto;max-height:450px}}code{{background:#eee;padding:2px 5px}}footer{{color:#596a71}}</style></head><body>
<header><small>GRAD 695 · Applied Project · Executed result viewer</small><h1>FairHireAI — Paired Recruitment-Cue Audit</h1><p><b>Adapter:</b> {esc(adapter)} · <b>Run:</b> {esc(metadata.get('run_id','unavailable'))} · <b>Seed:</b> {esc(metadata.get('seed','unavailable'))}</p><p>Built from local CSV output in <code>{esc(folder)}</code>. {len(evals):,} candidate-level evaluations, {len(pairs):,} paired comparisons.</p><div class="note"><b>Research integrity:</b> {esc(disclaimer)}</div>{provenance}</header>
<div class="cards">{cards}</div><section><h2>Strategy summary</h2>{table(summary,['strategy','eligible','incomplete','agreement_rate','mean_absolute_score_gap','flagged'])}</section>
<section><h2>Matched comparisons (first 50 rows)</h2>{table(pairs,['pair_id','strategy','repeat','complete','score_gap','agree','baseline_recommendation','altered_recommendation'])}</section>
<section><h2>Exact model / fixture outputs (first 25 rows)</h2><p>These are unmodified returned scores, explanations, and failures. See evaluations.csv for all raw records.</p>{table(evals,['pair_id','strategy','repeat','variant','score','recommendation','explanation','status','error','attempts'],25)}</section>{audit_section}{usage_section}
<footer>Read-only HTML generated by view_results.py. Source of truth: CSV and SQLite output, not this viewer.</footer></body></html>'''
    target=folder/'report.html'
    target.write_text(page,encoding='utf-8')
    print(f'Created: {target.resolve()}')
    print('Open report.html in a browser. The label states whether the run used live API or offline adapters.')
    return target

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results_dir',nargs='?',default='results')
    generate(p.parse_args().results_dir)
