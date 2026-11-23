"""Validate the retained information set; no network access or silent fallback."""
import csv
from datetime import date, datetime, timedelta
from hashlib import sha256
import io
import json
from math import isfinite
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent


def checked_bytes(record, root):
    raw = (root / record['file']).read_bytes()
    if sha256(raw).hexdigest() != record['sha256']:
        raise ValueError('Source hash mismatch; stop: ' + record['file'])
    return raw


def read_market(decision_date, window_months, root=ROOT):
    decision = date.fromisoformat(decision_date)
    meta = json.loads((root / 'sources/market/manifest.json').read_text())
    if decision_date != meta['decision_date']:
        raise ValueError('No retained information set for this decision date; use ' + meta['decision_date'])
    csv_raw = (root / meta['price_csv']).read_bytes()
    if sha256(csv_raw).hexdigest() != meta['price_csv_sha256']:
        raise ValueError('Price CSV hash mismatch; stop.')
    rows = list(csv.reader(csv_raw.decode().splitlines()))
    if rows[0] != ['Date', *meta['tickers']] or len(rows) != meta['levels'] + 1:
        raise ValueError('Invalid price table shape or ticker order.')
    expected_months = [row[0] for row in rows[1:]]
    for col, source in enumerate(meta['sources'], 1):
        if source['ticker'] != meta['tickers'][col - 1]:
            raise ValueError('Raw source order differs from price table.')
        if datetime.fromisoformat(source['downloaded_utc']).date() >= decision:
            raise ValueError('Price download is not available before the decision day.')
        raw = json.loads(checked_bytes(source, root))['chart']['result'][0]
        if raw['meta']['symbol'] != source['ticker'] or raw['meta']['currency'] != 'USD':
            raise ValueError('Unexpected price symbol or currency.')
        stamps = raw['timestamp']
        prices = raw['indicators']['adjclose'][0]['adjclose']
        if len(stamps) != len(prices) or len(prices) != len(expected_months):
            raise ValueError('Raw price coverage mismatch.')
        months = [datetime.fromtimestamp(t, ZoneInfo(raw['meta']['exchangeTimezoneName'])).strftime('%Y-%m-01') for t in stamps]
        if months != expected_months:
            raise ValueError('Raw price months differ from table.')
        for row, value in zip(rows[1:], prices):
            if value is None or not isfinite(value) or value <= 0 or float(row[col]) != value:
                raise ValueError('Raw adjusted price differs from table.')
    last_month = date.fromisoformat(rows[-1][0])
    if (last_month.year, last_month.month) >= (decision.year, decision.month):
        raise ValueError('Price bar is not a completed month before the decision.')
    if len(rows) - 1 < window_months + 1:
        raise ValueError('Insufficient price levels for the requested return window.')
    # Validate the complete calendar, not only the selected estimation window.
    month_numbers = [date.fromisoformat(r[0]).year * 12 + date.fromisoformat(r[0]).month for r in rows[1:]]
    if any(b != a + 1 for a, b in zip(month_numbers, month_numbers[1:])):
        raise ValueError('Price months must be consecutive; no row dropping or filling.')
    rf = meta['risk_free']
    if rf['vintage_date'] != (decision - timedelta(days=1)).isoformat():
        raise ValueError('Missing exact prior-day Treasury vintage; no fallback.')
    if datetime.fromisoformat(rf['downloaded_utc']).date() >= decision:
        raise ValueError('Treasury snapshot was not retrieved before the decision day.')
    rate_rows = list(csv.reader(checked_bytes(rf, root).decode('utf-8-sig').splitlines()))
    if rate_rows[0] != ['observation_date', 'DGS3MO_' + rf['vintage_date'].replace('-', '')]:
        raise ValueError('Treasury CSV header does not identify the retained vintage.')
    values = {}
    for row in rate_rows[1:]:
        stamp = date.fromisoformat(row[0])
        if stamp > date.fromisoformat(rf['vintage_date']):
            raise ValueError('Treasury observation is after its vintage.')
        if row[1] in ('', '.'):
            continue
        value = float(row[1])
        if not isfinite(value) or stamp in values:
            raise ValueError('Invalid or duplicate Treasury observation.')
        values[stamp] = value
    if not values:
        raise ValueError('Empty Treasury vintage.')
    latest = max(values)
    if (decision - latest).days > 7:
        raise ValueError('Treasury observation is more than seven days old; stop.')
    signal = {**rf, 'observation_date': latest.isoformat(), 'rate_percent': values[latest],
              'rate': values[latest] / 100, 'decision_date': decision_date}
    selected = io.StringIO()
    writer = csv.writer(selected)
    writer.writerow(rows[0])
    writer.writerows(rows[-(window_months + 1):])
    selected.seek(0)
    return selected, signal, {'first_month': rows[1][0], 'last_month': rows[-1][0],
                             'available_returns': len(rows) - 2, 'window_months': window_months,
                             'retrieved_date': max(s['downloaded_utc'][:10] for s in meta['sources']),
                             'manifest': 'sources/market/manifest.json', 'csv_sha256': meta['price_csv_sha256']}
