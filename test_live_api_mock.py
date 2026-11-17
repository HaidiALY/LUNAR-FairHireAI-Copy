"""Mocked Responses API contract tests. These tests do NOT use network or paid tokens."""
import csv
import io
import json
import os
import sqlite3
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from fairhireai import FIELDS, OpenAIAdapter, ProviderRequestError, export, run


def mock_response(score=77, response_id='resp_mock_001'):
    return {
        'id':response_id, 'model':'gpt-4.1-mini-2025-04-14', 'status':'completed',
        'usage':{'input_tokens':125,'output_tokens':50,'total_tokens':175},
        'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps({
            'score':score, 'recommendation':'Hire', 'explanation':'Skills and interview evidence meet the experiment rubric.'
        })}]}]
    }


class LiveAdapterContractTests(unittest.TestCase):
    def test_no_key_fails_before_request(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaisesRegex(RuntimeError,'OPENAI_API_KEY'):
                OpenAIAdapter('gpt-4.1-mini')

    def test_responses_endpoint_payload_json_schema_and_usage(self):
        raw=io.BytesIO(json.dumps(mock_response()).encode())
        with patch.dict(os.environ,{'OPENAI_API_KEY':'fake-for-mock-only'}):
            with patch('urllib.request.urlopen',return_value=raw) as caller:
                adapter=OpenAIAdapter('gpt-4.1-mini')
                output=adapter.evaluate({'Gender':'0'},'Candidate: test')
                self.assertEqual(json.loads(output)['score'],77)
                self.assertEqual(adapter.last_metadata['total_tokens'],175)
                self.assertEqual(adapter.last_metadata['response_id'],'resp_mock_001')
                request=caller.call_args.args[0]
                payload=json.loads(request.data)
                self.assertTrue(payload['text']['format']['strict'])
                self.assertFalse(payload['store'])
                self.assertNotIn('fake-for-mock-only',json.dumps(payload))

    def test_permanent_error_cannot_be_retried_as_a_success(self):
        with patch.dict(os.environ,{'OPENAI_API_KEY':'fake-for-mock-only'}):
            with patch('urllib.request.urlopen',side_effect=urllib.error.HTTPError(
                'https://api.openai.com/v1/responses',401,'Unauthorized',{},None)):
                adapter=OpenAIAdapter('gpt-4.1-mini')
                with self.assertRaises(ProviderRequestError) as ctx:
                    adapter.evaluate({'Gender':'0'},'Candidate: test')
                self.assertFalse(ctx.exception.retryable)

    def test_live_run_stores_response_ids_and_exports_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            dataset=root/'tiny.csv'
            with dataset.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=[*FIELDS,'Gender'])
                w.writeheader(); w.writerow({k:'5' for k in FIELDS}|{'Gender':'0'})
            calls=[]
            def fake_open(request,timeout=90):
                calls.append(request)
                return io.BytesIO(json.dumps(mock_response(response_id=f'resp_mock_{len(calls)}')).encode())
            with patch.dict(os.environ,{'OPENAI_API_KEY':'fake-for-mock-only'}):
                with patch('urllib.request.urlopen',side_effect=fake_open):
                    adapter=OpenAIAdapter('gpt-4.1-mini')
                    run_id=run(dataset,root/'out.sqlite',adapter,limit=1,repeats=1)
                    export(root/'out.sqlite',run_id,root/'result')
            with sqlite3.connect(root/'out.sqlite') as con:
                self.assertEqual(con.execute('SELECT COUNT(*) FROM evaluations WHERE status="ok"').fetchone()[0],4)
                self.assertEqual(con.execute('SELECT COUNT(*) FROM api_calls WHERE response_id IS NOT NULL').fetchone()[0],4)
            self.assertTrue((root/'result'/'api_calls.csv').exists())
            from view_results import generate
            html_file=generate(root/'result')
            self.assertIn('LIVE OPENAI API OBSERVATIONS',html_file.read_text())
            self.assertEqual(len(calls),4)


if __name__=='__main__': unittest.main(verbosity=2)
