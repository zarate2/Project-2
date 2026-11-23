"""Run: python3 -m streamlit run app.py"""
from datetime import date
import json
import streamlit as st
import model
from run import stress_rows

st.set_page_config(page_title='Project 2 | U.S. Portfolio', page_icon='📊', layout='wide')
st.caption(model.ANNOUNCEMENT)
st.title('U.S. stock and bond portfolio')
config = model.load_config()
st.caption(f"Version {config['version']} · seven-year horizon · no scheduled withdrawals · proposed November 23 decision")
st.write('Find the lowest-volatility portfolio that meets a Treasury-relative return target, using U.S. stocks, Treasury securities and investment-grade corporate bonds.')
with st.sidebar:
    st.header('Portfolio assumptions')
    if st.button('Reset to saved assumptions'):
        st.session_state.clear()
        st.rerun()
    config['decision_date'] = st.date_input('Proposed decision date', date.fromisoformat(config['decision_date']), key='decision_date').isoformat()
    st.caption('Retained information set: November 23, 2026, using data downloaded November 22. Other dates stop the calculation.')
    config['return_premium'] = st.number_input('Target above Treasury rate (percentage points)', 0.0, 20.0, config['return_premium']*100, .5, key='return_premium') / 100
    config['window_months'] = st.selectbox('Estimation window (months)', [36, 60, 120], index=[36,60,120].index(config['window_months']), key='window_months')
    config['equity_return_shift'] = st.number_input('VTI expected return shift (percentage points)', -50.0, 50.0, config['equity_return_shift']*100, .5, key='equity_return_shift') / 100
    config['additional_annual_cost'] = st.number_input('Additional annual cost (%)', 0.0, 5.0, config['additional_annual_cost']*100, .25, key='additional_annual_cost') / 100
    config['volatility_limit'] = st.number_input('Annual volatility limit (%)', 0.0, 100.0, config['volatility_limit']*100, 1.0, key='volatility_limit_v021') / 100
    config['equity_weight_limit'] = st.number_input('Maximum U.S. equity allocation (%)', 0.0, 100.0, config['equity_weight_limit']*100, 5.0, key='equity_weight_limit') / 100
    st.caption('100% means no separate equity cap; the volatility limit still applies. The 60% equity weight belongs to the comparison benchmark.')
    st.info('Controls recalculate immediately. For your required AI-off experiment, publish the prediction before entering the changed value. Downloads preserve this session; defaults stay unchanged.')

try:
    result = model.calculate(config)
except (ValueError, OSError, KeyError) as exc:
    st.error(f'STOP: {exc}')
    st.stop()

mix = result['portfolios']['Constrained portfolio']
if mix is None:
    st.warning(result['decision'])
else:
    st.info(result['decision'])
tabs = st.tabs(['Portfolio & mandate', 'Treasury signal', 'Stress tests', 'How to use & limits'])
with tabs[0]:
    cols = st.columns(4)
    cols[0].metric('Treasury reference rate', f"{result['signal']['rate']:.2%}")
    cols[1].metric('Net annual return target', f"{result['net_return_target']:.2%}")
    cols[2].metric('Annual volatility limit', f"{config['volatility_limit']:.2%}")
    if mix is None:
        ceiling = result['best_within_risk']
        cols[3].metric('Best net estimate within limits', 'None' if ceiling is None else f"{ceiling['net_return']:.2%}")
        st.error('Calculation completed: no feasible portfolio. No allocation is selected.')
        st.write('The best net estimate is the highest among the tested five-point allocations that satisfy the risk limits. It is a diagnostic, not an approved portfolio. The app keeps your rules unchanged.')
    else:
        cols[3].metric('Selected net return estimate', f"{mix['net_return']:.2%}")
        st.write(f"Selected annual volatility: **{mix['volatility']:.2%}**. Estimates are not guaranteed returns or maximum losses.")
        st.bar_chart({'Asset': config['tickers'], 'Weight': [w*100 for w in mix['weights']]}, x='Asset', y='Weight', y_label='Allocation (%)')
    st.subheader('Same assumptions, four portfolios')
    st.dataframe(model.table_rows(result), hide_index=True, width='stretch')
    if mix is not None:
        st.dataframe([{'Rule': k, 'Result': v} for k,v in mix['rules'].items()], hide_index=True, width='stretch')
    st.caption('BIL: Treasury bills · IEF: Treasury bonds/notes · LQD: investment-grade corporate bonds · VTI: broad U.S. equities. Benchmark: 60% VTI, 20% IEF, 20% LQD.')
    st.warning('Capital deployment remains unapproved. Personal review, independent performance evaluation, costs, liquidity and implementation evidence are incomplete.')
    st.download_button('Save current scenario JSON', json.dumps(result, indent=2), 'project2-scenario.json', 'application/json')

with tabs[1]:
    signal = result['signal']
    st.subheader('Treasury yield available before the proposed decision')
    st.metric('Three-month Treasury yield', f"{signal['rate']:.2%}")
    st.write(f"Observation: **{signal['observation_date']}** · ALFRED vintage: **{signal['vintage_date']}** · proposed decision: **{signal['decision_date']}**")
    st.code(f"{signal['rate']:.2%} + {config['return_premium']*100:.2f} percentage points = {result['net_return_target']:.2%} net annual target")
    st.write('DGS3MO is a three-month Treasury constant-maturity yield quoted on an investment basis. A prior-day snapshot prevents a later observation from entering this decision. The premium is a policy choice, not an estimated equity risk premium.')
    st.markdown(f"[Retained ALFRED source]({signal['url']}) · [Series definition]({signal['definition_url']})")
    st.caption(f"Retrieved {signal['downloaded_utc']} · SHA-256 {signal['sha256']}")
    st.warning('This short-term yield is not locked in for seven years. Reinvestment rates can change. Missing snapshots, future observations, stale rates or failed hashes stop the model.')

with tabs[2]:
    scenarios = model.stress_suite(config)
    st.subheader('What changes the decision?')
    st.dataframe(stress_rows({'scenarios': scenarios}), hide_index=True, width='stretch')
    st.write('Each scenario changes one dimension from your current settings. With the default 4-point premium, the target stress uses 5 points. A shorter estimation window changes return, volatility and correlation estimates together; it is not a historical strategy backtest.')
    st.caption('The cost/premium stresses add one percentage point up to a 100% validation bound; the equity-cap stress tightens to at most 25%. At a bound the relevant stress may be unchanged.')
    st.download_button('Save stress results JSON', json.dumps(scenarios, indent=2), 'project2-stresses.json', 'application/json')

with tabs[3]:
    st.subheader('Read the result before changing a control')
    st.markdown('1. Compare the target, risk limit and pass/fail reasons.\n2. Save the starting scenario.\n3. For practice, inspect the already-displayed stress cases.\n4. For the required experiment, close AI and commit your own prediction to GitHub before changing the chosen input.\n5. Save the after result separately and explain what changed.\n6. Use Reset to saved assumptions to restore the baseline.')
    st.write('The default model estimates returns from the latest 60 monthly returns. The retained history has 120 monthly returns, and 36/120-month alternatives are available. Selecting a window after seeing its outcome does not validate predictive ability.')
    st.write('There are no scheduled withdrawals or reserve requirements. The seven-year horizon is a planning assumption; the model does not promise or simulate a seven-year realized outcome. Additional annual cost is a provisional 0.25% beyond expenses embedded in adjusted prices.')
    st.write('Rebalancing, turnover, executable liquidity and out-of-sample performance require further evidence. The previous global-equity/CPI/payout version is archived. Its allocation and NVDA persona exhibit are not evidence for this revised strategy.')
