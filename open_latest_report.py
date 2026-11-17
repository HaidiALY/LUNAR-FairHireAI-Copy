"""Open the most recent actual HTML report. No timestamp typing needed."""
from pathlib import Path
import webbrowser
folders=[p for p in Path('.').glob('results_live_openai_*/') if (p/'report.html').exists()]
if not folders:
    raise SystemExit('No live report yet. Execute python3 run_live.py --limit 2 --repeats 1 first.')
folder=max(folders,key=lambda p:p.name)
report=(folder/'report.html').resolve()
print('Opening your actual report:',report)
webbrowser.open(report.as_uri())
