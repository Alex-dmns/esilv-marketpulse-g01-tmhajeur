from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.yahoo_provider import (
    fetch_yahoo_prices,
    YAHOO_SYMBOLS,
)


def main():
    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Yahoo Finance via yfinance")
    print()

    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["AAPL"],
        canonical_ticker="AAPL",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS["SP500"],
        canonical_ticker="SP500",
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_perf = calculate_relative_performance(
        instrument_return, benchmark_return
    )
    instrument_base100 = calculate_base_100(aligned_instrument)
    benchmark_base100 = calculate_base_100(aligned_benchmark)

    print("Market configuration")
    print("Instrument : AAPL - Apple Inc.")
    print("Benchmark  : SP500 - S&P 500")
    print("Period     : 1 month")
    print("Interval   : Daily")
    print()
    print(f"Instrument return : {instrument_return:.2f}%")
    print(f"Benchmark return  : {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(f"AAPL vs SP500 : {relative_perf:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"AAPL  : {instrument_base100[0]['value']:.2f} -> {instrument_base100[-1]['value']:.2f}")
    print(f"SP500 : {benchmark_base100[0]['value']:.2f} -> {benchmark_base100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()