"""Shared, deterministic Lab 19 evidence and checks. Models write the memos."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re

import sec_facts as sec

ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / "skills/cathie-wood-sec/policy.json"
INVESTORS = {"buffett": "Warren Buffett", "cathie-wood": "Cathie Wood", "burry": "Michael Burry"}
VERDICTS = ("Own the business", "Watch it", "Pass")


def read_policy():
    policy = json.loads(POLICY_PATH.read_text())
    for key in ("growth_threshold", "rd_threshold"):
        if not isinstance(policy[key], (float, int)) or not 0 <= policy[key] <= 1:
            raise ValueError(f"{key} must be a decimal rate between zero and one.")
    return policy


def compare(value, threshold, minimum=True):
    if value is None:
        return "not known"
    meets = value >= threshold if minimum else value <= threshold
    return "pass" if meets or math.isclose(value, threshold, rel_tol=0, abs_tol=1e-12) else "fail"


def revenue_cagr(rows):
    if len(rows) != 5:
        return None
    first, last = rows[0]["revenue"]["value"], rows[-1]["revenue"]["value"]
    if first is None or last is None or first <= 0 or last < 0:
        return None
    return (last / first) ** (1 / 4) - 1


def cathie_checks(rows, policy):
    """Compare code-computed growth and latest R&D intensity; missing stays unknown."""
    growth = revenue_cagr(rows)
    rd_ratio = rows[-1]["rd_to_revenue"]["value"] if rows else None
    return {
        f'Revenue CAGR at least {policy["growth_threshold"] * 100:g}%, first to last': compare(growth, policy["growth_threshold"]),
        f'Latest R&D / revenue at least {policy["rd_threshold"] * 100:g}%': compare(rd_ratio, policy["rd_threshold"]),
    }


def burry_checks(rows):
    pairs = [(row["operating_cash_flow"]["value"], row["net_income"]["value"]) for row in rows]
    cash_check = "not known"
    if len(pairs) == 5 and all(cash is not None and income is not None for cash, income in pairs):
        cash_check = "pass" if all(cash >= income for cash, income in pairs) else "fail"
    ratio = rows[-1]["liabilities_to_equity"]["value"] if rows else None
    return {"Operating cash flow at least net income every year": cash_check,
            "Latest liabilities / equity no more than 2": compare(ratio, 2, minimum=False)}


def add_panel(packet, policy=None):
    policy = dict(read_policy() if policy is None else policy)
    packet = dict(packet)
    rows = packet["rows"]
    packet["policy"] = policy
    packet["revenue_cagr"] = revenue_cagr(rows)
    packet["panel"] = {"buffett": sec.checks(rows), "cathie-wood": cathie_checks(rows, policy), "burry": burry_checks(rows)}
    return packet


def from_snapshot(ticker, source_dir=ROOT / "sources", policy=None):
    ticker = sec.validate_ticker(ticker)
    source_dir = Path(source_dir)
    raw = (source_dir / f"{ticker}-companyfacts.json").read_bytes()
    manifest = json.loads((source_dir / f"{ticker}-manifest.json").read_text())
    fact_record = next(s for s in manifest if "companyfacts" in s["url"])
    if hashlib.sha256(raw).hexdigest() != fact_record["sha256"]:
        raise ValueError("Retained SEC company-facts hash mismatch.")
    facts = json.loads(raw)
    packet = sec.analyze(facts, ticker)
    packet["sources"] = manifest
    return add_panel(packet, policy)


def fetch_panel(ticker, user_agent, source_dir=ROOT / "sources", policy=None):
    return add_panel(sec.fetch_company(ticker, user_agent, source_dir), policy)


def digest(packet):
    content = {key: packet[key] for key in ("ticker", "rows", "policy", "panel", "revenue_cagr")}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()


def panel_rows(packet):
    return [{"Investor": INVESTORS[key], "Check": check, "Result": result}
            for key, checks in packet["panel"].items() for check, result in checks.items()]


def pct(value):
    return "not known" if value is None else f"{value:.2%}"


def evidence_text(packet):
    # This part of the report is the memo's numeric whitelist. Provenance IDs are excluded.
    rows = sec.table_rows(packet)
    cols = list(rows[0])
    lines = [f'# {packet["ticker"]} — {packet["company"]}', "",
             "SEC EDGAR: 10-K only; five fiscal years. Monetary values in USD millions.",
             "ROE uses year-end equity; owner earnings = operating cash flow minus total capital spending.", "",
             "| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    lines += ["| " + " | ".join(r.values()) + " |" for r in rows]
    lines += ["", f'Revenue CAGR, first year to last: **{pct(packet["revenue_cagr"])}**.',
              "Formula: (last revenue / first revenue)^(1/4) - 1, with a five-year window.", "",
              "## Panel checks", "", "| Investor | Check | Result |", "| --- | --- | --- |"]
    lines += [f'| {r["Investor"]} | {r["Check"]} | {r["Result"]} |' for r in panel_rows(packet)]
    lines += ["", "## Cash-versus-income detail", "", "| Fiscal year end | OCF at least net income |", "| --- | --- |"]
    for row in packet["rows"]:
        cash, income = row["operating_cash_flow"]["value"], row["net_income"]["value"]
        state = "not known" if cash is None or income is None else "pass" if cash >= income else "fail"
        lines.append(f'| {row["fiscal_year_end"]} | {state} |')
    return "\n".join(lines) + "\n"


def render_report(packet):
    provenance = sec.render_report(packet).split("## XBRL tags and filing provenance", 1)[1]
    return evidence_text(packet) + "\n## XBRL tags and filing provenance" + provenance


def unsupported_numbers(memo, packet):
    allowed = {sec.number_key(m.group()) for m in sec.NUMBER.finditer(evidence_text(packet))}
    return [{"number": m.group().strip(), "line": memo.count("\n", 0, m.start()) + 1,
             "context": memo.splitlines()[memo.count("\n", 0, m.start())]}
            for m in sec.NUMBER.finditer(memo) if sec.number_key(m.group()) not in allowed]


def verdict_from_memo(memo):
    heading = memo.splitlines()[0] if memo else ""
    verdict = heading.rsplit(" — ", 1)[-1]
    return verdict if verdict in VERDICTS else None


def save_packet(packet, output_dir=ROOT / "outputs", suffix="panel"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f'{packet["ticker"]}-{suffix}'
    (output_dir / f"{stem}.json").write_text(json.dumps(packet, indent=2) + "\n")
    (output_dir / f"{stem}.md").write_text(render_report(packet))


def audit_memos(packet, output_dir=ROOT / "outputs"):
    output_dir = Path(output_dir)
    audits = {}
    for investor in INVESTORS:
        path = output_dir / f'{packet["ticker"]}-{investor}-memo.md'
        if not path.exists():
            audits[investor] = {"error": "memo not found"}
            continue
        memo = path.read_text()
        verdict = verdict_from_memo(memo)
        bad = unsupported_numbers(memo, packet)
        audits[investor] = {"verdict": verdict, "unsupported_numbers": bad}
        if not bad and verdict:
            path.with_suffix(".meta.json").write_text(json.dumps({"packet_sha256": digest(packet), "verdict": verdict}, indent=2) + "\n")
    (output_dir / f'{packet["ticker"]}-memo-audit.json').write_text(json.dumps(audits, indent=2) + "\n")
    return audits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--snapshot", action="store_true")
    parser.add_argument("--audit-memos", action="store_true")
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT", ""))
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    parser.add_argument("--source-dir", type=Path, default=ROOT / "sources")
    args = parser.parse_args()
    ticker = sec.validate_ticker(args.ticker)
    if args.audit_memos:
        packet = json.loads((args.output_dir / f"{ticker}-panel.json").read_text())
        if packet["policy"] != read_policy():
            raise SystemExit("Recompute the panel after changing the skill's policy before auditing memos.")
        audits = audit_memos(packet, args.output_dir)
        print(json.dumps(audits, indent=2))
        raise SystemExit(0 if all(a.get("verdict") and not a.get("unsupported_numbers") for a in audits.values()) else 1)
    packet = from_snapshot(ticker, args.source_dir) if args.snapshot else fetch_panel(ticker, args.user_agent, args.source_dir)
    save_packet(packet, args.output_dir)
    print(render_report(packet))


if __name__ == "__main__":
    main()
