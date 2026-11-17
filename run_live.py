"""Safely launch an actual paid OpenAI evaluation without exposing the key in the terminal."""
import argparse
import getpass
import os
from pathlib import Path
from datetime import datetime, timezone
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description='Real OpenAI FairHireAI pilot; charges API credits')
    parser.add_argument('--csv', default='recruitment_data.csv')
    parser.add_argument('--model', default='gpt-4.1-mini')
    parser.add_argument('--limit', type=int, default=2, help='Start at 2 candidate PAIRS')
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--seed', type=int, default=594)
    parser.add_argument('--db', default='live_openai.sqlite')
    parser.add_argument('--out', default='results_live_openai')
    parser.add_argument('--dry-run', action='store_true', help='Print plan without API calls')
    parser.add_argument('--allow-large-run', action='store_true', help='Explicitly approve >20 pairs')
    args = parser.parse_args()
    if args.limit < 1 or args.repeats < 1 or args.limit > 1500 or args.repeats > 10:
        parser.error('Use 1–1500 pairs and 1–10 repeats')
    if args.limit > 20 and not args.allow_large_run:
        parser.error('More than 20 pairs requires --allow-large-run')
    if not Path(args.csv).exists():
        parser.error(f'Missing dataset: {args.csv}')
    planned = args.limit * 2 * 2 * args.repeats
    print(f'\nLIVE EXPERIMENT PLAN: {args.limit} pairs × 2 demographic codes × 2 prompts × {args.repeats} repeat(s) = {planned} PAID API calls (before retries).')
    print(f'Model: {args.model}. Data: {args.csv}. This is NOT a real employer hiring decision.')
    print(f'Maximum API attempts if every call is retried: {planned * 3} (normally fewer).')
    print('Real model responses, errors and token usage will be recorded; no deterministic fallback will be used.')
    if args.dry_run:
        print('DRY RUN COMPLETE: no API requests or charges.\n')
        return
    answer=input('Type LIVE to confirm paid API calls: ').strip()
    if answer!='LIVE':
        print('Cancelled; no API requests sent')
        return
    # Unique evidence destinations: never overwrite another experiment's reports.
    tag=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    if args.db=='live_openai.sqlite': args.db=f'live_openai_{tag}.sqlite'
    if args.out=='results_live_openai': args.out=f'results_live_openai_{tag}'
    if Path(args.db).exists() or Path(args.out).exists():
        parser.error('Output already exists. Choose fresh --db and --out paths; do not overwrite evidence.')
    key=os.environ.get('OPENAI_API_KEY')
    if not key:
        print('\nSECURE API-KEY ENTRY — DO THIS ONLY AT THE PROMPT BELOW:')
        print('1. Use a NEW key after revoking any key that was exposed in chat or terminal.')
        print('2. When the prompt below appears, paste your key once and press Return.')
        print('3. The key will NOT be displayed. Do NOT type it at the later % shell prompt.')
        print('4. Pause your video/screen recording while entering the key.\n')
        key=getpass.getpass('NEW OPENAI API KEY (hidden, press Return after pasting): ').strip()
    if not key:
        print('No key provided; no API requests sent');sys.exit(2)
    env=os.environ.copy()
    env['OPENAI_API_KEY']=key
    command=[sys.executable, 'fairhireai.py', args.csv, '--adapter', 'openai',
             '--model', args.model, '--limit',str(args.limit), '--repeats',str(args.repeats),
             '--seed',str(args.seed),'--sampling','random', '--db',args.db,'--out',args.out]
    del key
    print('\nExecuting real model experiment; responses may be missing if the API returns an error.\n')
    result=subprocess.run(command,env=env,check=False)
    if result.returncode==0:
        viewer=subprocess.run([sys.executable,'view_results.py',args.out],check=False)
        if viewer.returncode==0:
            report_path=(Path(args.out)/'report.html').resolve()
            print('\nLIVE RESULT REPORT: '+str(report_path))
            print('On Mac, you may open it with: open '+str(report_path))
            if sys.platform=='darwin':
                try:
                    subprocess.run(['open',str(report_path)],check=False)
                except OSError:
                    pass
        print('Next check: python3 inspect_live_run.py (summarizes response IDs, successes and missing cases).')
        print('NEVER paste your API key when the terminal returns to the % or $ shell prompt.')
    else:
        print('Execution failed; review output, API billing and credentials. No offline results were substituted.')
        sys.exit(result.returncode)


if __name__=='__main__':
    main()
