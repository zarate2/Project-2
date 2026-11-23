"""Retained Labs 18/19 research; independent of the portfolio allocation weights."""
import json
from pathlib import Path
import panel

ROOT = Path(__file__).resolve().parent


def investor_review():
    packet = panel.from_snapshot('NVDA')
    digest = panel.digest(packet)
    memos = {}
    for investor, name in panel.INVESTORS.items():
        path = ROOT / 'research/memos' / f'NVDA-{investor}-memo.md'
        text = path.read_text()
        meta = json.loads(path.with_suffix('.meta.json').read_text())
        flags = panel.unsupported_numbers(text, packet)
        bound = meta.get('packet_sha256') == digest
        memos[name] = {'text': text, 'bound_to_packet': bound, 'unsupported_numbers': flags,
                       'verdict': panel.verdict_from_memo(text) if bound and not flags else 'Needs review'}
    return {'packet': packet, 'memos': memos,
            'scope': 'Supplementary November 19 research on a VT holding; not an October 30 signal, price valuation or allocation rule.'}
