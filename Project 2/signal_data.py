"""Lab 16/17 admission gate: exact prior-day vintage, never current-data fallback."""
import csv
from datetime import date, timedelta
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def cpi_signal(decision_date, root=ROOT):
    decision = date.fromisoformat(decision_date)
    vintage = decision - timedelta(days=1)
    name = f'CPIAUCSL-vintage-{vintage.isoformat()}.csv'
    records = json.loads((root / 'sources/cpi-manifest.json').read_text())
    record = next((r for r in records if Path(r['file']).name == name), None)
    if record is None:
        raise ValueError(f'No retained CPI vintage for {vintage}. Stop: do not substitute current data.')
    raw = (root / record['file']).read_bytes()
    if sha256(raw).hexdigest() != record['sha256']:
        raise ValueError('CPI snapshot hash mismatch; stop.')
    rows = list(csv.reader(raw.decode('utf-8-sig').splitlines()))
    values = {}
    for row in rows[1:]:
        stamp = date.fromisoformat(row[0])
        if stamp > vintage:
            raise ValueError('CPI observation after the requested vintage; stop.')
        if row[1] in ('', '.'):
            continue
        value = float(row[1])
        if not isfinite(value) or value <= 0 or stamp in values:
            raise ValueError('Invalid or duplicate CPI value; stop.')
        values[stamp] = value
    if not values:
        raise ValueError('Empty CPI vintage; stop.')
    latest = max(values)
    prior = latest.replace(year=latest.year - 1)
    if prior not in values:
        raise ValueError('Missing year-ago CPI in the same vintage; stop.')
    return {'decision_date': decision_date, 'vintage_date': vintage.isoformat(),
            'observation_date': latest.isoformat(), 'prior_observation_date': prior.isoformat(),
            'level': values[latest], 'prior_level': values[prior],
            'year_over_year': values[latest] / values[prior] - 1,
            'url': record['url'], 'downloaded_utc': record['downloaded_utc'],
            'sha256': record['sha256'], 'file': record['file'],
            'interpretation': 'Trailing inflation; using it as expected inflation is a proposed proxy, not a forecast.'}


def verify_prices(decision_date, root=ROOT):
    """Reject a historical allocation date before the retained price download."""
    decision = date.fromisoformat(decision_date)
    metadata = json.loads((root / 'sources/Prices.json').read_text())
    for source in metadata['sources']:
        if date.fromisoformat(source['downloaded_at_utc'][:10]) >= decision:
            raise ValueError('Saved price download was not available before this decision day; stop.')
        raw = (root / 'sources/yahoo' / (source['ticker'] + '.json')).read_bytes()
        if sha256(raw).hexdigest() != source['sha256']:
            raise ValueError('Price source hash mismatch; stop.')
    with (root / 'prices.csv').open(newline='') as handle:
        rows = list(csv.reader(handle))
    if rows[0] != metadata['columns'] or len(rows) - 1 != len(metadata['rows']):
        raise ValueError('Price CSV differs from retained source metadata; stop.')
    for actual, expected in zip(rows[1:], metadata['rows']):
        if actual[0] != expected[0] or any(abs(float(a) - b) > 1e-9 for a, b in zip(actual[1:], expected[1:])):
            raise ValueError('Price CSV differs from retained source metadata; stop.')
    return {'download_date': max(s['downloaded_at_utc'][:10] for s in metadata['sources']),
            'last_price_month': rows[-1][0][:7], 'sha256': sha256((root / 'prices.csv').read_bytes()).hexdigest()}
