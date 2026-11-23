"""Reproduce the revised portfolio screen using retained inputs only."""
import json
from pathlib import Path
import model
ROOT = Path(__file__).resolve().parent


def build_report():
    return {'version': model.load_config()['version'], 'review_date': '2026-11-22', 'scenarios': model.stress_suite()}


def stress_rows(report):
    rows = []
    for name, result in report['scenarios'].items():
        row = result['portfolios']['Constrained portfolio']
        rows.append({'Scenario': name, 'BIL / IEF / LQD / VTI': 'No feasible allocation' if row is None else ' / '.join(f'{w:.0%}' for w in row['weights']),
                     'Net proxy': '—' if row is None else f"{row['net_return']:.2%}",
                     'Volatility': '—' if row is None else f"{row['volatility']:.2%}", 'Status': result['status']})
    return rows


def allocation_range(report):
    feasible = [r['portfolios']['Constrained portfolio']['weights'] for r in report['scenarios'].values()
                if r['portfolios']['Constrained portfolio'] is not None]
    if not feasible:
        return 'No feasible tested allocation'
    return '; '.join(f"{t}: {min(w[i] for w in feasible):.0%}–{max(w[i] for w in feasible):.0%}"
                     for i,t in enumerate(model.load_config()['tickers']))


def render(report):
    base = report['scenarios']['Base']; c=base['config']; s=base['signal']; prices=base['price_source']
    sections = [model.ANNOUNCEMENT, '# Project 2 — version ' + report['version'], base['decision'],
        f"Calculated {report['review_date']} for the proposed decision date {c['decision_date']}. "
        f"Prices retrieved {prices['retrieved_date']}, through completed month {prices['last_month'][:7]}. No live feed is used.",
        '## Mandate and information set',
        f"Seven-year planning horizon; no scheduled withdrawals or payout reserve. Universe BIL / IEF / LQD / VTI. "
        f"Benchmark: 60% VTI, 20% IEF, 20% LQD. Fully invested, long-only. "
        f"Annualized volatility ceiling {c['volatility_limit']:.2%}; equity cap {c['equity_weight_limit']:.0%} "
        '(100% means no separate equity restriction beyond long-only and the volatility ceiling).',
        f"Three-month Treasury reference: {s['rate']:.2%}, observation {s['observation_date']}, "
        f"ALFRED vintage {s['vintage_date']}, downloaded {s['downloaded_utc']}. "
        f"Return premium {c['return_premium']*100:.2f} percentage points gives a {base['net_return_target']:.2%} annual net screen. "
        f"Additional annual cost {c['additional_annual_cost']:.2%}; estimation uses {c['window_months']} monthly returns.",
        'The Treasury rate is a short-term reference, not a rate locked in for seven years. Returns are annualized arithmetic estimates, not a seven-year compound forecast. '
        'The return premium and risk ceiling are policy choices, not guaranteed outcomes. The cost estimate remains provisional.',
        '## Comparisons', model.markdown_table(model.table_rows(base)),
        '## Sensitivities', model.markdown_table(stress_rows(report)),
        '**Research range across feasible scenarios:** ' + allocation_range(report) + '. '
        'The range is not a menu of independently combinable weights and grants no capital authorization.',
        '## Decision conditions',
        'Stop if no allocation is feasible, a required source or vintage is unavailable, integrity fails, or inputs are invalid. '
        'Do not substitute another date or relax the risk limit. Monitor estimated net return versus the Treasury-relative target, '
        'volatility, allocation drift, costs and source eligibility at each review. Annual rebalancing is a proposed convention, not an implemented trading simulation.',
        'These estimates use one information set and are not an out-of-sample strategy evaluation. Ten years of retained prices allow additional outcome checks, '
        'but this screen has not validated a seven-year realized return, actual transaction costs, liquidity or turnover. '
        'Adoption requires that evidence and review; otherwise retain paper research only or reject an infeasible scenario.',
        'The previous inflation/global-equity/payout version is archived in history/before-mandate-v0.2.zip. '
        'The old NVDA persona research is retained as historical material and does not drive this screen.',
        'Human AI-off prediction, prior GitHub commit, independent user run, ownership confirmation, videos/transcripts and submission remain pending.',
        'Sources: sources/market/manifest.json. Full results: outputs/results.json. Reproduce with python3 run.py.']
    return '\n\n'.join(sections) + '\n'


def main():
    report=build_report(); text=render(report); (ROOT/'outputs').mkdir(exist_ok=True)
    (ROOT/'outputs/results.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'outputs/visible-output.md').write_text(text)
    print(text)


if __name__ == '__main__':
    main()
