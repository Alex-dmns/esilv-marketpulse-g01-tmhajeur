from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers import bloomberg_provider
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

DEFAULT_PROVIDER = "bloomberg"

YAHOO_PERIOD = "1mo"
YAHOO_INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


# Local CSV path, kept to validate analytics if a provider is unavailable.
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


def fetch_yahoo_asset_prices(asset):
    ticker = asset["ticker"]
    return fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[ticker],
        canonical_ticker=ticker,
        period=YAHOO_PERIOD,
        interval=YAHOO_INTERVAL,
    )


# Every provider returns canonical rows; only the label and source differ.
def fetch_market_prices(provider, instrument, benchmark):
    if provider == "bloomberg":
        label = f"Bloomberg stage ({bloomberg_provider.ACCESS_MODE})"
        instrument_prices = bloomberg_provider.fetch_bloomberg_prices(instrument["ticker"])
        benchmark_prices = bloomberg_provider.fetch_bloomberg_prices(benchmark["ticker"])
    elif provider == "yahoo":
        label = "Yahoo Finance via yfinance"
        instrument_prices = fetch_yahoo_asset_prices(instrument)
        benchmark_prices = fetch_yahoo_asset_prices(benchmark)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    return label, instrument_prices, benchmark_prices


# Shared application result, consumed by the terminal (TD10) and Dash (TD11).
def build_market_snapshot(provider=DEFAULT_PROVIDER):
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    provider_label, instrument_prices, benchmark_prices = fetch_market_prices(
        provider,
        instrument,
        benchmark,
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": provider_label,
        "access_mode": bloomberg_provider.ACCESS_MODE if provider == "bloomberg" else "LIVE",
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return,
            benchmark_return,
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['ticker']} - {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()
    print("Common observations")
    print(f"Count      : {len(instrument_base_100)}")
    print(f"First date : {instrument_base_100[0]['date']}")
    print(f"Last date  : {instrument_base_100[-1]['date']}")
    print()
    print(f"Instrument return : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return  : {snapshot['benchmark_return']:.2f}%")
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )
    print()
    print("Base 100")
    print(f"{instrument['ticker']:<6}: {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']:<6}: {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()
