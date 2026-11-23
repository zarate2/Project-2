"""Lab 15: extended Lab 14 engine. Run: python3 portfolio.py

Standard library only. Returns, volatilities and weights are decimal fractions.
All inputs below are course training values, not market estimates.
"""

SLEEVES = [
    {"name": "Treasury bills", "return": .035, "volatility": .005, "reserve": True},
    {"name": "Treasury 10-year note", "return": .043, "volatility": .070, "reserve": True},
    {"name": "Investment-grade bond fund", "return": .050, "volatility": .060, "reserve": False},
    {"name": "Global equity index fund", "return": .080, "volatility": .160, "reserve": False},
]
CORRELATIONS = [
    [1.00, .10, .05, .00],
    [.10, 1.00, .80, -.10],
    [.05, .80, 1.00, .25],
    [.00, -.10, .25, 1.00],
]
CPI_ESTIMATE = .025  # Labelled course estimate, not an observed inflation rate.
REAL_RETURN_TARGET = .040
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_TARGET  # Course additive convention.
BENCHMARK_WEIGHTS = [0.0, 0.0, .40, .60]

from math import fsum, isclose, isfinite, sqrt
import sys


def validate_inputs(sleeves, correlations):
    """Reject malformed, nonfinite, out-of-range or asymmetric inputs."""
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must be square with one row per sleeve.")
    for sleeve in sleeves:
        if not isfinite(sleeve["return"]):
            raise ValueError("Expected returns must be finite.")
        if not isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Volatilities must be finite and positive for inverse volatility.")
    for i in range(n):
        for j in range(n):
            rho = correlations[i][j]
            if not isfinite(rho) or not -1 <= rho <= 1:
                raise ValueError(f"Correlation [{i}][{j}] = {rho} is outside -1 to 1 or nonfinite.")
            if not isclose(rho, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table is not symmetric at [{i}][{j}] and [{j}][{i}].")
        if not isclose(correlations[i][i], 1, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Every diagonal correlation must equal 1.")


def covariance_matrix(sleeves, correlations):
    validate_inputs(sleeves, correlations)
    return [[correlations[i][j] * a["volatility"] * b["volatility"]
             for j, b in enumerate(sleeves)] for i, a in enumerate(sleeves)]


def validate_weights(weights, count):
    if len(weights) != count or not all(isfinite(w) and w >= 0 for w in weights):
        raise ValueError("Provide one finite, nonnegative weight per sleeve.")
    if not isclose(fsum(weights), 1, rel_tol=0, abs_tol=1e-12):
        raise ValueError("Portfolio weights must sum to 1 (100%).")


def equal_weights(sleeves):
    if not sleeves:
        raise ValueError("At least one sleeve is required.")
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    if not sleeves or any(not isfinite(s["volatility"]) or s["volatility"] <= 0 for s in sleeves):
        raise ValueError("Inverse volatility requires positive, finite volatilities.")
    inverse = [1 / sleeve["volatility"] for sleeve in sleeves]
    total = fsum(inverse)
    return [value / total for value in inverse]


def expected_return(weights, sleeves):
    validate_weights(weights, len(sleeves))
    return fsum(w * sleeve["return"] for w, sleeve in zip(weights, sleeves))


def portfolio_variance(weights, covariance):
    validate_weights(weights, len(covariance))
    n = len(weights)
    if any(len(row) != n for row in covariance):
        raise ValueError("Covariance matrix must be square.")
    # All i,j pairs include the two symmetric cross terms for each asset pair.
    variance = fsum(weights[i] * weights[j] * covariance[i][j]
                    for i in range(n) for j in range(n))
    if not isfinite(variance) or variance < -1e-12:
        raise ValueError("Portfolio variance is invalid; check the covariance inputs.")
    return max(0.0, variance)  # Only absorbs tiny floating-point roundoff.


def portfolio_volatility(weights, covariance):
    return sqrt(portfolio_variance(weights, covariance))


def reserve_weight(weights, sleeves):
    validate_weights(weights, len(sleeves))
    return fsum(w for w, sleeve in zip(weights, sleeves) if sleeve["reserve"])


def meets_objective(value, objective):
    if not isfinite(objective):
        raise ValueError("Objective return must be finite.")
    return value >= objective


def baseline_weights(sleeves):
    return {"Benchmark": list(BENCHMARK_WEIGHTS), "Equal weight": equal_weights(sleeves),
            "Inverse volatility": inverse_volatility_weights(sleeves)}


def evaluate(weights, sleeves, covariance, objective):
    result = expected_return(weights, sleeves)
    return {"weights": list(weights), "return": result,
            "volatility": portfolio_volatility(weights, covariance),
            "reserve": reserve_weight(weights, sleeves),
            "meets_objective": meets_objective(result, objective)}


def calculate_baselines(sleeves=None, correlations=None, objective=None):
    sleeves = SLEEVES if sleeves is None else sleeves
    correlations = CORRELATIONS if correlations is None else correlations
    objective = OBJECTIVE_RETURN if objective is None else objective
    covariance = covariance_matrix(sleeves, correlations)
    return {name: evaluate(weights, sleeves, covariance, objective)
            for name, weights in baseline_weights(sleeves).items()}


def search_lowest_risk(sleeves, correlations, objective, reserve_minimum):
    """Exhaust every long-only 5-percentage-point mix; return a result or None.

    Inputs and outputs use decimal fractions. Equal-risk ties keep the first
    mix in ascending weight order. Constraints use a 1e-12 rounding tolerance.
    """
    covariance = covariance_matrix(sleeves, correlations)
    if not 3 <= len(sleeves) <= 6:
        raise ValueError("The lab requires three to six assets.")
    if not isfinite(objective):
        raise ValueError("Objective return must be finite.")
    if not isfinite(reserve_minimum) or not 0 <= reserve_minimum <= 1:
        raise ValueError("Reserve minimum must be between 0 and 1.")

    def allocations(remaining, count):
        # Twenty units represent 100%; each unit is five percentage points.
        if count == 1:
            yield [remaining / 20]
        else:
            for units in range(remaining + 1):
                for tail in allocations(remaining - units, count - 1):
                    yield [units / 20] + tail

    best = None
    for weights in allocations(20, len(sleeves)):
        if expected_return(weights, sleeves) + 1e-12 < objective:
            continue
        if reserve_weight(weights, sleeves) + 1e-12 < reserve_minimum:
            continue
        result = evaluate(weights, sleeves, covariance, objective)
        if best is None or result["volatility"] < best["volatility"] - 1e-12:
            best = result
    return best


def estimate_from_csv(source, last_36=False):
    """Estimate annual inputs from monthly adjusted price levels.

    source is a path or a text file-like object. Use arithmetic monthly means
    times 12, sample standard deviations times sqrt(12), and Pearson sample
    correlations on aligned monthly returns. Last 36 means 36 RETURNS, which
    require 37 price levels. Reject gaps instead of silently filling prices.
    """
    import csv
    from datetime import date
    from pathlib import Path
    from statistics import mean, stdev

    if hasattr(source, "read"):
        rows = list(csv.reader(source))
    else:
        with Path(source).open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
    if not rows or not 4 <= len(rows[0]) <= 7:
        raise ValueError("CSV needs a date column followed by three to six tickers.")
    tickers = [cell.strip().upper() for cell in rows[0][1:]]
    if any(not name for name in tickers) or len(set(tickers)) != len(tickers):
        raise ValueError("Ticker headers must be nonempty and unique.")
    dates, prices = [], []
    previous_month = None
    for line, row in enumerate(rows[1:], start=2):
        if len(row) != len(tickers) + 1:
            raise ValueError(f"CSV row {line} has missing or extra columns.")
        try:
            stamp = date.fromisoformat(row[0].strip())
            values = [float(cell) for cell in row[1:]]
        except ValueError as error:
            raise ValueError(f"CSV row {line}: use YYYY-MM-DD and numeric prices.") from error
        month = stamp.year * 12 + stamp.month
        if previous_month is not None and month != previous_month + 1:
            raise ValueError("Dates must be consecutive monthly observations, oldest first.")
        if any(not isfinite(value) or value <= 0 for value in values):
            raise ValueError(f"CSV row {line}: prices must be finite and positive.")
        previous_month = month
        dates.append(stamp.isoformat())
        prices.append(values)
    minimum = 37 if last_36 else 3
    if len(prices) < minimum:
        raise ValueError(f"This estimate needs at least {minimum} monthly price levels.")
    monthly = [[new / old - 1 for new, old in zip(prices[t], prices[t - 1])]
               for t in range(1, len(prices))]
    return_dates = dates[1:]
    if last_36:
        monthly, return_dates = monthly[-36:], return_dates[-36:]
    columns = list(zip(*monthly))
    means = [mean(values) for values in columns]
    deviations = [stdev(values) for values in columns]
    if any(value <= 1e-15 for value in deviations):
        raise ValueError("Each asset needs nonzero return variation to estimate correlation.")
    correlations = []
    for i, left in enumerate(columns):
        row = []
        for j, right in enumerate(columns):
            covariance = fsum((a - means[i]) * (b - means[j])
                              for a, b in zip(left, right)) / (len(monthly) - 1)
            rho = covariance / (deviations[i] * deviations[j])
            row.append(1.0 if i == j else max(-1.0, min(1.0, rho)))
        correlations.append(row)
    sleeves = [{"name": name, "return": means[i] * 12,
                "volatility": deviations[i] * sqrt(12),
                "reserve": name in {"BIL", "IEF"}}
               for i, name in enumerate(tickers)]
    validate_inputs(sleeves, correlations)
    return {"sleeves": sleeves, "correlations": correlations,
            "observations": len(monthly), "first_return_month": return_dates[0],
            "last_return_month": return_dates[-1]}


def main():
    results = calculate_baselines()
    print("Meridian baselines — course training inputs; annual return and volatility")
    print(f"Objective: {OBJECTIVE_RETURN:.2%}; CPI estimate: {CPI_ESTIMATE:.1%}")
    print("Weight order: " + " / ".join(s["name"] for s in SLEEVES))
    for name, row in results.items():
        print(f"\n{name}")
        print("  Weights: " + " / ".join(f"{w:.1%}" for w in row["weights"]))
        print(f"  Expected return: {row['return']:.2%}")
        print(f"  Volatility: {row['volatility']:.2%}")
        print(f"  Reserve-eligible: {row['reserve']:.1%}")
        print(f"  Meets {OBJECTIVE_RETURN:.1%} objective: {'yes' if row['meets_objective'] else 'no'}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
