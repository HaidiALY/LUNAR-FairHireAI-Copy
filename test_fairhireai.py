import csv,json,tempfile,unittest
from pathlib import Path
from fairhireai import FIELDS, load_candidates,make_pairs,validate_pair,prompt,parse_response,RuleBasedDemo,run,analyze,export
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.csv=Path(self.tmp.name)/'candidates.csv'
        with self.csv.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=[*FIELDS,'Gender','HiringDecision']);w.writeheader()
            for i in range(4):w.writerow(dict(zip([*FIELDS,'Gender','HiringDecision'],['29','2','5','2','12','80','90','70','1',str(i%2),'1'])))
    def test_csv(self):self.assertEqual(len(load_candidates(self.csv)),4)
    def test_pairs(self):self.assertTrue(all(validate_pair(p['baseline'],p['altered']) for p in make_pairs(load_candidates(self.csv))))
    def test_reject_changed_skill(self):
        p=make_pairs(load_candidates(self.csv))[0];p['altered']['SkillScore']='0';self.assertFalse(validate_pair(p['baseline'],p['altered']))
    def test_output_hidden(self):self.assertNotIn('HiringDecision',prompt(load_candidates(self.csv)[0],'baseline','job','rubric'))
    def test_parser_rejects_bad(self):
        with self.assertRaises(ValueError):parse_response('{"score":101,"recommendation":"Hire","explanation":"ok"}')
    def test_reject_personal_fields(self):
        with self.csv.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=[*FIELDS,'Gender','Email']);w.writeheader();w.writerow({**{k:'1' for k in FIELDS},'Gender':'0','Email':'x@y.org'})
        with self.assertRaises(ValueError):load_candidates(self.csv)
    def test_full_run(self):
        db=Path(self.tmp.name)/'results.sqlite';rid=run(self.csv,db,RuleBasedDemo(),limit=4,repeats=2)
        sums,detail=analyze(db,rid)
        self.assertEqual(len(detail),16);self.assertEqual(sums[0]['eligible'],8)
        self.assertTrue(all(s['agreement_rate']==1 for s in sums))
        export(db,rid,Path(self.tmp.name)/'out');self.assertTrue((Path(self.tmp.name)/'out'/'evaluations.csv').exists())
    def test_missing_responses_excluded(self):
        class Bad:
            name='bad_fixture'
            def evaluate(self,profile,text):return 'not-json'
        db=Path(self.tmp.name)/'bad.sqlite';rid=run(self.csv,db,Bad(),limit=1,repeats=1)
        s,_=analyze(db,rid);self.assertTrue(all(x['eligible']==0 and x['incomplete']==1 and x['agreement_rate'] is None for x in s))
    def test_order_seed_repeatability(self):
        d1=Path(self.tmp.name)/'one.sqlite';d2=Path(self.tmp.name)/'two.sqlite'
        a=run(self.csv,d1,RuleBasedDemo(),limit=2);b=run(self.csv,d2,RuleBasedDemo(),limit=2)
        import sqlite3
        def positions(d):return sqlite3.connect(d).execute('SELECT pair_id,strategy,repeat,variant,position FROM evaluations ORDER BY pair_id,strategy,repeat,variant').fetchall()
        self.assertEqual(positions(d1),positions(d2))
if __name__=='__main__':unittest.main(verbosity=2)

class ExtendedTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.path=Path(self.t.name)/'sample.csv'
        with self.path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=[*FIELDS,'Gender']);w.writeheader()
            for i in range(12):
                w.writerow(dict(zip([*FIELDS,'Gender'],['31','3','6','1','10',str(55+i),'75','65','0',str(i%2)])))
    def test_seeded_random_selection_reproducible(self):
        from fairhireai import run,RuleBasedDemo
        from pathlib import Path
        import sqlite3
        def ids(name):
            d=Path(self.t.name)/name
            run(self.path,d,RuleBasedDemo(),limit=5,repeats=1,sampling='random',seed=594)
            with sqlite3.connect(d) as c:
                return c.execute('select distinct pair_id from evaluations order by pair_id').fetchall()
        self.assertEqual(ids('x.db'),ids('y.db'))
        self.assertEqual(len(ids('z.db')),5)
    def test_documented_scoring_rubric(self):
        from fairhireai import RuleBasedDemo
        profile={k:'0' for k in [*FIELDS,'Gender']}
        profile.update({'SkillScore':'90','InterviewScore':'80','ExperienceYears':'5'})
        value=json.loads(RuleBasedDemo().evaluate(profile,'test'))
        self.assertEqual(value['score'],78)  # 0.4*90 + 0.4*80 + 2*5
        self.assertEqual(value['recommendation'],'Hire')
        profile['Gender']='1'
        self.assertEqual(json.loads(RuleBasedDemo().evaluate(profile,'test'))['score'],78)
    def test_injected_fault_is_detected(self):
        from fairhireai import run,analyze,InjectedFaultDemo
        d=Path(self.t.name)/'fault.db'
        rid=run(self.path,d,InjectedFaultDemo(),limit=4,repeats=1)
        result,_=analyze(d,rid)
        self.assertTrue(all(row['mean_absolute_score_gap']>0 for row in result))
    def test_viewer_generates_html(self):
        from fairhireai import run,export,RuleBasedDemo
        from view_results import generate
        d=Path(self.t.name)/'viewer.db';out=Path(self.t.name)/'results'
        rid=run(self.path,d,RuleBasedDemo(),limit=3,repeats=1)
        export(d,rid,out)
        self.assertIn('FairHireAI',generate(out).read_text())
