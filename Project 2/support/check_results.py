"""Independent tests of the revised Treasury-relative portfolio screen."""
from copy import deepcopy
from datetime import datetime, timezone, date
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.parse import unquote

import numpy as np
from streamlit.testing.v1 import AppTest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import model
import run
from market_data import read_market


class ProjectChecks(unittest.TestCase):
    def test_independent_estimates_grid_and_diagnostic(self):
        prices=np.genfromtxt(ROOT/'sources/market/prices.csv',delimiter=',',skip_header=1)[:,1:]
        all_returns=prices[1:]/prices[:-1]-1
        grid=np.array([[a,b,c,20-a-b-c] for a in range(21) for b in range(21-a) for c in range(21-a-b)])/20
        self.assertEqual(len(grid),1771)
        for scenario in model.stress_suite().values():
            c=scenario['config']; monthly=all_returns[-c['window_months']:]
            means=monthly.mean(axis=0)*12; means[3]+=c['equity_return_shift']
            cov=np.cov(monthly.T)*12
            np.testing.assert_allclose([s['return'] for s in scenario['estimate']['sleeves']],means)
            net=grid@means-c['additional_annual_cost']
            vol=np.sqrt(np.einsum('ij,jk,ik->i',grid,cov,grid))
            risk=(vol<=c['volatility_limit']+1e-12)&(grid[:,3]<=c['equity_weight_limit']+1e-12)
            eligible=risk&(net>=scenario['net_return_target']-1e-12)
            actual=scenario['portfolios']['Constrained portfolio']
            if eligible.any():
                np.testing.assert_allclose(actual['weights'],grid[eligible][vol[eligible].argmin()])
            else:
                self.assertIsNone(actual)
                self.assertIn('REJECT',scenario['decision'])
            diagnostic=scenario['best_within_risk']
            if risk.any():
                self.assertAlmostEqual(diagnostic['net_return'],float(net[risk].max()))
            else:
                self.assertIsNone(diagnostic)
            for row in scenario['portfolios'].values():
                if row is not None:
                    w=np.array(row['weights'])
                    self.assertAlmostEqual(row['net_return'],float(w@means-c['additional_annual_cost']))
                    self.assertAlmostEqual(row['volatility'],float(np.sqrt(w@cov@w)))
                    self.assertNotIn('reserve',row)

    def test_known_treasury_units_and_baseline_rules(self):
        result=model.calculate()
        self.assertEqual(result['signal']['observation_date'],'2026-11-19')
        self.assertEqual(result['signal']['vintage_date'],'2026-11-22')
        self.assertAlmostEqual(result['signal']['rate'],.0434)
        self.assertAlmostEqual(result['net_return_target'],.0834)
        self.assertEqual(result['portfolios']['Constrained portfolio']['weights'],[.35,0.0,0.0,.65])
        benchmark=result['portfolios']['60/40 benchmark']
        self.assertEqual(benchmark['weights'],[0,.2,.2,.6])
        self.assertEqual(len(benchmark['failed_rules']),1)
        self.assertEqual(result['config']['scheduled_withdrawals'],False)
        self.assertNotIn('reserve_floor',result['config'])
        self.assertEqual(result['estimate']['observations'],60)
        self.assertEqual(result['price_source']['available_returns'],120)
        for row in result['portfolios'].values():
            if row:
                self.assertTrue(row['deployment_verdict'].startswith('FAIL'))

    def test_stress_changes_do_not_relax_limits(self):
        cases=model.stress_suite();base=cases['Base']
        target=cases['Target: premium plus 1 percentage point']
        self.assertAlmostEqual(target['net_return_target']-base['net_return_target'],.01)
        costs=cases['Cost: plus 1 percentage point']
        for name in ['Equal weight','Inverse volatility','60/40 benchmark']:
            self.assertAlmostEqual(base['portfolios'][name]['net_return']-costs['portfolios'][name]['net_return'],.01)
        window=cases['Window: 36 months']
        self.assertEqual(window['estimate']['observations'],36)
        self.assertIsNotNone(window['portfolios']['Constrained portfolio'])
        self.assertEqual(base['config']['volatility_limit'],.12)
        self.assertEqual(base['config']['return_premium'],.04)
        self.assertIsNotNone(base['portfolios']['Constrained portfolio'])

    def test_information_gates_and_tampering(self):
        with self.assertRaisesRegex(ValueError,'No retained information set'):
            read_market('2026-11-22',60)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            shutil.copytree(ROOT/'sources/market',root/'sources/market')
            mp=root/'sources/market/manifest.json';original=json.loads(mp.read_text())
            rawpath=root/original['sources'][0]['file'];raw=rawpath.read_bytes()
            rawpath.write_bytes(raw+b' ')
            with self.assertRaisesRegex(ValueError,'hash mismatch'):
                read_market('2026-11-23',60,root)
            rawpath.write_bytes(raw)
            changed=deepcopy(original);changed['risk_free']['vintage_date']='2026-11-21'
            mp.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'prior-day'):
                read_market('2026-11-23',60,root)
            changed=deepcopy(original);changed['sources'][0]['downloaded_utc']='2026-11-23T12:00:00+00:00'
            mp.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'not available'):
                read_market('2026-11-23',60,root)
            changed=deepcopy(original);rate=root/changed['risk_free']['file']
            rate.write_text(rate.read_text()+'2026-11-24,4.3\n')
            changed['risk_free']['sha256']=sha256(rate.read_bytes()).hexdigest()
            mp.write_text(json.dumps(changed))
            with self.assertRaisesRegex(ValueError,'after its vintage'):
                read_market('2026-11-23',60,root)

    def test_invalid_policy_inputs(self):
        for key,value in [('return_premium',float('nan')),('additional_annual_cost',-.01),('volatility_limit',1.1),('equity_return_shift',float('inf')),('window_months',121),('scheduled_withdrawals',True)]:
            with self.assertRaises(ValueError):
                model.calculate(dict(model.load_config(),**{key:value}))

    def test_app_controls_reset_and_unavailable_date(self):
        app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric][:3],['4.34%','8.34%','12.00%'])
        self.assertTrue(any('PILOT' in x.value for x in app.info))
        self.assertEqual(app.metric[3].value,'8.61%')
        app.selectbox[0].set_value(36).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[3].value,'8.44%')
        next(b for b in app.button if b.label=='Reset to saved assumptions').click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value,60)
        self.assertTrue(any('PILOT' in x.value for x in app.info))
        app.date_input[0].set_value(date(2026,11,22)).run()
        self.assertFalse(app.exception)
        self.assertIn('No retained information set',app.error[0].value)
        self.assertFalse(app.metric)

    def test_saved_output_and_documents(self):
        report=run.build_report()
        self.assertEqual(json.loads((ROOT/'outputs/results.json').read_text()),report)
        self.assertEqual((ROOT/'outputs/visible-output.md').read_text(),run.render(report))
        for p in [ROOT/'README.md',ROOT/'CHANGELOG.md',*sorted((ROOT/'docs').glob('*.md'))]:
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                if '://' not in link and not link.startswith('#'):
                    self.assertTrue((p.parent/unquote(link.split('#')[0])).exists(),f'{p}: {link}')
        memo=(ROOT/'docs/decision-memo.md').read_text()
        self.assertIn(report['scenarios']['Base']['decision'],memo)
        self.assertIn('8.34%',memo)
        self.assertIn('4.34%',memo)

    def test_isolated_readme_run(self):
        with tempfile.TemporaryDirectory(prefix='project2-v02-cold-') as temp:
            folder=Path(temp)/'project'
            shutil.copytree(ROOT,folder,ignore=shutil.ignore_patterns('.venv','__pycache__','.git','history'))
            started=time.perf_counter()
            proc=subprocess.run(['python3','run.py'],cwd=folder,text=True,capture_output=True,timeout=30)
            self.assertEqual(proc.returncode,0,proc.stderr)
            hashes={}
            for name in ['results.json','visible-output.md']:
                raw=(folder/'outputs'/name).read_bytes()
                self.assertEqual(raw,(ROOT/'outputs'/name).read_bytes())
                hashes[name]=sha256(raw).hexdigest()
            record={'version':model.load_config()['version'],'performed_by':'Codex automated isolated local run; not a partner or fresh dependency install','run_utc':datetime.now(timezone.utc).isoformat(),'command':'python3 run.py','elapsed_seconds':round(time.perf_counter()-started,4),'exit_code':proc.returncode,'first_failure':None,'output_hashes':hashes}
            (ROOT/'outputs/cold-run.json').write_text(json.dumps(record,indent=2)+'\n')
            (ROOT/'outputs/cold-run.txt').write_text(proc.stdout+proc.stderr)


if __name__=='__main__':
    log=StringIO()
    result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProjectChecks))
    (ROOT/'outputs/Verification.txt').write_text(log.getvalue())
    print(log.getvalue())
    sys.exit(0 if result.wasSuccessful() else 1)
