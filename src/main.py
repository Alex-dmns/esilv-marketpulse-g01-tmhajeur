from pathlib import Path
import csv
import json
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices

DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "Yahoo Finance via yfinance"
YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }

def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Yahoo path: provider symbols stay at the provider boundary,
    # rows keep the canonical tickers (AAPL, SP500).
    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )
    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_perf = calculate_relative_performance(instrument_return, benchmark_return)

    instrument_base100 = calculate_base_100(aligned_instrument)
    benchmark_base100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(PROVIDER_LABEL)
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print(
        f"Common dates : {len(aligned_instrument)} "
        f"({aligned_instrument[0]['date']} -> {aligned_instrument[-1]['date']})"
    )
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Period return : {instrument_return:.2f}%")
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Period return : {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : {relative_perf:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument['ticker']}  : {instrument_base100[0]['value']:.2f} -> {instrument_base100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base100[0]['value']:.2f} -> {benchmark_base100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()



