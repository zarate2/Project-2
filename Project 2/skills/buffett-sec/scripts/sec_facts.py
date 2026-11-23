"""Keyless SEC annual facts and literal-number memo auditing; stdlib only."""
from __future__ import annotations

import argparse
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
    "liabilities": ["Liabilities"],
}
FLOW_KEYS = ("revenue", "net_income", "operating_cash_flow", "capital_spending")
LABELS = {key: key.replace("_", " ").title() for key in TAGS}
LABELS.update(roe="ROE", owner_earnings="Owner Earnings", liabilities_to_equity="Liabilities / Equity")
METRICS = list(TAGS) + ["roe", "owner_earnings", "liabilities_to_equity"]


def validate_ticker(ticker):
    ticker = ticker.strip().upper()
    if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,14}", ticker):
        raise ValueError("Enter a valid SEC ticker, such as COST or JPM.")
    return ticker


def download_json(url, user_agent):
    if not re.fullmatch(r"[^\r\n]+\s+[^\s@]+@[^\s@]+\.[^\s@]+", user_agent or ""):
        raise ValueError("SEC User-Agent must contain your name and real email.")
    # Sequential requests, well below SEC's request limit. curl verifies TLS.
    time.sleep(0.15)
    result = subprocess.run(
        ["curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "60",
         "--retry", "2", "--retry-delay", "2", "--user-agent", user_agent, url],
        capture_output=True, check=True,
    )
    raw = result.stdout
    payload = json.loads(raw)
    evidence = {"url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                "sha256": hashlib.sha256(raw).hexdigest()}
    return payload, raw, evidence


def fetch_company(ticker, user_agent, source_dir=None):
    ticker = validate_ticker(ticker)
    listing, raw_tickers, ticker_source = download_json(TICKERS_URL, user_agent)
    match = next((v for v in listing.values() if v["ticker"].upper() == ticker), None)
    if match is None:
        raise ValueError(f"{ticker} was not found in SEC's ticker map.")
    cik = int(match["cik_str"])
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    facts, raw_facts, fact_source = download_json(url, user_agent)
    if int(facts["cik"]) != cik:
        raise ValueError("Company facts CIK does not match the ticker lookup.")
    packet = analyze(facts, ticker)
    packet["sources"] = [ticker_source, fact_source]
    if source_dir:
        source_dir = Path(source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        for filename, raw, evidence in [
            (f"{ticker}-tickers.json", raw_tickers, ticker_source),
            (f"{ticker}-companyfacts.json", raw_facts, fact_source),
        ]:
            (source_dir / filename).write_bytes(raw)
            evidence["file"] = filename
        (source_dir / f"{ticker}-manifest.json").write_text(json.dumps(packet["sources"], indent=2) + "\n")
    return packet


def annual(fact):
    """Allow calendar and 52/53-week years, never quarters or year-to-date flows."""
    if fact.get("form") != "10-K" or not fact.get("start") or not fact.get("end"):
        return False
    days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days + 1
    return 350 <= days <= 380


def observations(facts, tag):
    return facts.get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", [])


def select_fact(facts, key, fiscal_end):
    # Priority is applied separately for each year. The latest filing wins within a tag.
    for tag in TAGS[key]:
        candidates = [f for f in observations(facts, tag)
                      if f.get("form") == "10-K" and f.get("end") == fiscal_end
                      and (annual(f) if key in FLOW_KEYS else not f.get("start"))]
        if candidates:
            latest = max(candidates, key=lambda f: (f.get("filed", ""), f.get("accn", ""), f.get("start", "")))
            return {"value": latest["val"], "tag": tag,
                    **{k: latest.get(k) for k in ("start", "end", "filed", "accn", "form")}}
    return {"value": None, "tag": "not found", "searched_tags": TAGS[key]}


def year_row(facts, fiscal_end):
    """Turn annual facts into one row; None is missing, never an estimated zero."""
    row = {"fiscal_year_end": fiscal_end}
    row.update({key: select_fact(facts, key, fiscal_end) for key in TAGS})
    income, equity = row["net_income"]["value"], row["equity"]["value"]
    cash, capex = row["operating_cash_flow"]["value"], row["capital_spending"]["value"]
    liabilities = row["liabilities"]["value"]
    row["roe"] = {"value": income / equity if income is not None and equity is not None and equity > 0 else None,
                  "tag": "NetIncomeLoss / StockholdersEquity"}
    row["owner_earnings"] = {"value": cash - capex if cash is not None and capex is not None else None,
                             "tag": f'{row["operating_cash_flow"]["tag"]} - {row["capital_spending"]["tag"]}'}
    row["liabilities_to_equity"] = {
        "value": liabilities / equity if liabilities is not None and equity is not None and equity > 0 else None,
        "tag": "Liabilities / StockholdersEquity"}
    return row


def checks(rows):
    def every(key, predicate):
        values = [row[key]["value"] for row in rows]
        if len(values) != 5 or any(v is None for v in values):
            return "not known"
        return "pass" if all(predicate(v) for v in values) else "fail"
    growth = "not known"
    if len(rows) == 5 and rows[0]["owner_earnings"]["value"] is not None and rows[-1]["owner_earnings"]["value"] is not None:
        growth = "pass" if rows[-1]["owner_earnings"]["value"] > rows[0]["owner_earnings"]["value"] else "fail"
    return {"ROE at least 15% every year": every("roe", lambda v: v >= .15),
            "Owner earnings positive every year": every("owner_earnings", lambda v: v > 0),
            "Owner earnings grew, first year to last": growth}


def analyze(facts, ticker):
    # SEC's fy is the filing year, not necessarily the year a comparative fact measures.
    ends = sorted({f["end"] for key in FLOW_KEYS for tag in TAGS[key]
                   for f in observations(facts, tag) if annual(f)})[-5:]
    if not ends:
        raise ValueError("No annual USD 10-K periods found for the required flow tags.")
    rows = [year_row(facts, end) for end in ends]
    return {"ticker": validate_ticker(ticker), "company": facts.get("entityName", ticker),
            "cik": facts.get("cik"), "rows": rows, "checks": checks(rows)}


def display_value(key, value):
    if value is None:
        return "not known" if key in ("roe", "liabilities_to_equity") else "not found"
    if key == "roe":
        return f"{value * 100:.1f}%"
    if key == "liabilities_to_equity":
        return f"{value:.2f}"
    return f"{value / 1_000_000:,.6f}".rstrip("0").rstrip(".")


def table_rows(packet):
    return [{"Fiscal year end": row["fiscal_year_end"],
             **{LABELS[k]: display_value(k, row[k]["value"]) for k in METRICS}}
            for row in packet["rows"]]


def render_report(packet):
    table = table_rows(packet)
    columns = list(table[0])
    lines = [f'# {packet["ticker"]} — {packet["company"]}', "",
             "SEC EDGAR · 10-K only · monetary values in USD millions · ROE as percent.",
             "Owner earnings = operating cash flow minus total capital spending. Ratios use year-end equity.", "",
             "| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    lines += ["| " + " | ".join(row.values()) + " |" for row in table]
    lines += ["", "## Computed checks", ""] + [f"- {k}: **{v}**" for k, v in packet["checks"].items()]
    lines += ["", "## XBRL tags and filing provenance", "",
              "| Fiscal year end | Metric | Value | Tag / formula | Period start | Filed | Accession |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    for row in packet["rows"]:
        for key in METRICS:
            fact = row[key]
            tag = fact["tag"]
            if fact.get("searched_tags"):
                tag += "; searched " + ", ".join(fact["searched_tags"])
            lines.append(f'| {row["fiscal_year_end"]} | {LABELS[key]} | {display_value(key, fact["value"])} | {tag} | {fact.get("start") or "—"} | {fact.get("filed") or "—"} | {fact.get("accn") or "—"} |')
    for source in packet.get("sources", []):
        lines += ["", f'Source: {source["url"]} · retrieved {source["retrieved_utc"]} · SHA-256 `{source["sha256"]}`']
    return "\n".join(lines) + "\n"


NUMBER = re.compile(r"\d{4}-\d{2}-\d{2}|(?<!\d)[−+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][+-]?\d+)?\s*%?")


def number_key(token):
    token = token.strip().replace("−", "-")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", token):
        return ("date", token)
    percent = token.endswith("%")
    return ("percent" if percent else "number", Decimal(token.rstrip("% ").replace(",", "")))


def unsupported_numbers(memo, packet):
    # Whitelist only values/dates/threshold printed in the table and checks, not accession fragments.
    allowed = {number_key("15%"), number_key("10")}
    for row in table_rows(packet):
        for cell in row.values():
            allowed.update(number_key(m.group()) for m in NUMBER.finditer(cell))
    return [{"number": m.group().strip(), "line": memo.count("\n", 0, m.start()) + 1,
             "context": memo.splitlines()[memo.count("\n", 0, m.start())]}
            for m in NUMBER.finditer(memo) if number_key(m.group()) not in allowed]


def packet_digest(packet):
    return hashlib.sha256(json.dumps({k: packet[k] for k in ("ticker", "rows", "checks")}, sort_keys=True).encode()).hexdigest()


def save_packet(packet, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f'{packet["ticker"]}-facts.json').write_text(json.dumps(packet, indent=2) + "\n")
    report = render_report(packet)
    (output_dir / f'{packet["ticker"]}-facts.md').write_text(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker")
    parser.add_argument("--user-agent", default=os.environ.get("SEC_USER_AGENT", ""))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--source-dir", type=Path, default=Path("sources"))
    parser.add_argument("--audit-memo", type=Path)
    args = parser.parse_args()
    ticker = validate_ticker(args.ticker)
    if args.audit_memo:
        packet = json.loads((args.output_dir / f"{ticker}-facts.json").read_text())
        bad = unsupported_numbers(args.audit_memo.read_text(), packet)
        print(json.dumps({"unsupported_numbers": bad}, indent=2))
        if bad:
            raise SystemExit(1)
        args.audit_memo.with_suffix(".meta.json").write_text(json.dumps({"facts_sha256": packet_digest(packet)}, indent=2) + "\n")
    else:
        packet = fetch_company(ticker, args.user_agent, args.source_dir)
        print(save_packet(packet, args.output_dir))


if __name__ == "__main__":
    main()
