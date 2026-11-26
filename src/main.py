from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "CSV sample data"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# CSV values arrive as text: convert numeric fields before analytics.
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


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def display_configuration():
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print(f"Provider : {PROVIDER_LABEL}")


# Same display logic for the instrument and the benchmark.
def display_market_summary(title, asset, period_return):
    print(title)
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Period return : {period_return:.2f}%")


def display_base_100(asset, base_100):
    first_value = base_100[0]["value"]
    last_value = base_100[-1]["value"]
    print(f"{asset['ticker']:<6}: {first_value:.2f} -> {last_value:.2f}")


def main():
    instruments = load_instruments()
    prices = [normalize_price_row(row) for row in load_prices()]

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    display_configuration()
    print()
    display_market_summary("Instrument", instrument, instrument_return)
    print()
    display_market_summary("Benchmark", benchmark, benchmark_return)
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
    )
    print()
    print("Base 100")
    display_base_100(instrument, instrument_base_100)
    display_base_100(benchmark, benchmark_base_100)


if __name__ == "__main__":
    main()
