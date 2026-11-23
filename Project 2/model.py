"""Constrained U.S. portfolio screen using a dated Treasury reference."""
from copy import deepcopy
from math import fsum, isfinite
import json
from pathlib import Path
import portfolio as p
from market_data import read_market

ROOT = Path(__file__).resolve().parent
ANNOUNCEMENT = ('AI disclosure: OpenAI Codex assisted with implementation, testing and drafting. '
                'Student ownership confirmation is pending.\n\nFor education, not investment advice.')
DECISION = ('PILOT in paper research only, with 0% new capital authorized. Consider adoption only after '
            'the assumptions are reviewed and independent performance, costs, liquidity and implementation evidence support it.')
REJECT = 'REJECT this scenario: no feasible allocation meets the return target and risk limits; do not relax the rules automatically.'
DEPLOYMENT_GAPS = ['student and committee review', 'independent performance evaluation',
                   'observed costs, liquidity and implementation evidence']


def load_config():
    return json.loads((ROOT / 'config.json').read_text())


def validate_config(c):
    if c['tickers'] != ['BIL', 'IEF', 'LQD', 'VTI']:
        raise ValueError('Universe must be BIL, IEF, LQD, VTI; do not relabel other source data.')
    for key in ('return_premium', 'additional_annual_cost', 'volatility_limit', 'equity_weight_limit'):
        value = c[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= 1:
            raise ValueError(key + ' must be a finite decimal rate between zero and one.')
    if not isinstance(c['equity_return_shift'], (int, float)) or not isfinite(c['equity_return_shift']):
        raise ValueError('Equity return shift must be finite.')
    if isinstance(c['window_months'], bool) or not isinstance(c['window_months'], int) or not 12 <= c['window_months'] <= 120:
        raise ValueError('Estimation window must be an integer from 12 to 120 months.')
    if c['scheduled_withdrawals'] is not False or c['horizon_years'] != 7:
        raise ValueError('This mandate uses seven years and no scheduled withdrawals.')
    p.validate_weights(c['benchmark_weights'], 4)


def grid():
    for a in range(21):
        for b in range(21 - a):
            for c in range(21 - a - b):
                yield [a/20, b/20, c/20, (20-a-b-c)/20]


def evaluate(weights, sleeves, covariance, config, target):
    row = p.evaluate(weights, sleeves, covariance, target + config['additional_annual_cost'])
    row['gross_return'] = row.pop('return')
    row.pop('reserve')
    row.pop('meets_objective')
    row['net_return'] = row['gross_return'] - config['additional_annual_cost']
    rules = {
        'Fully invested and long-only': abs(fsum(weights)-1) <= 1e-12 and min(weights) >= 0,
        'Net return proxy >= Treasury rate + premium': row['net_return'] + 1e-12 >= target,
        'Annual volatility <= limit': row['volatility'] <= config['volatility_limit'] + 1e-12,
        'U.S. equity weight <= configured cap': weights[3] <= config['equity_weight_limit'] + 1e-12,
    }
    row['rules'] = {name: 'PASS' if ok else 'FAIL' for name, ok in rules.items()}
    row['failed_rules'] = [name for name, ok in rules.items() if not ok]
    row['modeled_verdict'] = 'FAIL' if row['failed_rules'] else 'PASS'
    row['deployment_verdict'] = 'FAIL — validation and review incomplete'
    return row


def calculate(config=None):
    c = deepcopy(load_config() if config is None else config)
    validate_config(c)
    prices, signal, source = read_market(c['decision_date'], c['window_months'])
    target = signal['rate'] + c['return_premium']
    estimate = p.estimate_from_csv(prices)
    if [s['name'] for s in estimate['sleeves']] != c['tickers']:
        raise ValueError('Price order does not match the mandate.')
    estimate['sleeves'][3]['return'] += c['equity_return_shift']
    sleeves = estimate['sleeves']
    covariance = p.covariance_matrix(sleeves, estimate['correlations'])
    baselines = {'Equal weight': p.equal_weights(sleeves),
                 'Inverse volatility': p.inverse_volatility_weights(sleeves),
                 '60/40 benchmark': c['benchmark_weights']}
    rows = {name: evaluate(w, sleeves, covariance, c, target) for name, w in baselines.items()}
    best = None
    best_within_risk = None
    for weights in grid():
        row = evaluate(weights, sleeves, covariance, c, target)
        risk_ok = all(ok == 'PASS' for rule, ok in row['rules'].items() if not rule.startswith('Net return'))
        if risk_ok and (best_within_risk is None or row['net_return'] > best_within_risk['net_return']):
            best_within_risk = row
        if not row['failed_rules'] and (best is None or row['volatility'] < best['volatility'] - 1e-12):
            best = row
    rows['Constrained portfolio'] = best
    return {'config': c, 'price_source': source, 'signal': signal, 'net_return_target': target,
            'estimate': estimate, 'portfolios': rows, 'best_within_risk': best_within_risk,
            'status': 'FEASIBLE' if best else 'STOP — no feasible 5-point allocation',
            'decision': DECISION if best else REJECT, 'deployment_gaps': DEPLOYMENT_GAPS}


def stress_suite(config=None):
    base = load_config() if config is None else config
    changes = {
        'Base': {},
        'Estimate: VTI minus 1 percentage point': {'equity_return_shift': base['equity_return_shift'] - .01},
        'Window: 36 months' if base['window_months'] != 36 else 'Window: 60 months': {'window_months': 36 if base['window_months'] != 36 else 60},
        'Cost: plus 1 percentage point': {'additional_annual_cost': min(1., base['additional_annual_cost'] + .01)},
        'Constraint: U.S. equity cap at most 25%': {'equity_weight_limit': min(base['equity_weight_limit'], .25)},
        'Target: premium plus 1 percentage point': {'return_premium': min(1., base['return_premium'] + .01)},
    }
    return {name: calculate(dict(base, **change)) for name, change in changes.items()}


def table_rows(result):
    records = []
    for name, row in result['portfolios'].items():
        if row is None:
            records.append({'Portfolio': name, 'Weights BIL / IEF / LQD / VTI': 'No feasible allocation',
                            'Gross': '—', 'Net proxy': '—', 'Volatility': '—',
                            'Modeled verdict': 'FAIL: infeasible', 'Deployment': 'FAIL'})
        else:
            records.append({'Portfolio': name, 'Weights BIL / IEF / LQD / VTI': ' / '.join(f'{w:.2%}' for w in row['weights']),
                            'Gross': f"{row['gross_return']:.2%}", 'Net proxy': f"{row['net_return']:.2%}",
                            'Volatility': f"{row['volatility']:.2%}",
                            'Modeled verdict': row['modeled_verdict'] + (': ' + '; '.join(row['failed_rules']) if row['failed_rules'] else ''),
                            'Deployment': row['deployment_verdict']})
    return records


def markdown_table(rows):
    headings = list(rows[0])
    lines = ['| ' + ' | '.join(headings) + ' |', '| ' + ' | '.join(['---'] * len(headings)) + ' |']
    return '\n'.join(lines + ['| ' + ' | '.join(str(row[key]) for key in headings) + ' |' for row in rows])
