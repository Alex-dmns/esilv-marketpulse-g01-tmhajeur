from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from providers.bloomberg_provider import (
    fetch_bloomberg_prices,
    BLOOMBERG_IDENTIFIERS,
)

ACCESS_MODE = "APPROVED_SAMPLE"


def build_market_snapshot(mode=ACCESS_MODE):
    instrument_prices = fetch_bloomberg_prices("AAPL", mode=mode)
    benchmark_prices = fetch_bloomberg_prices("SP500", mode=mode)

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

    return {
        "provider": "Bloomberg stage",
        "access_mode": mode,
        "lookback": "1 month",
        "interval": "Daily",
        "instrument": "AAPL",
        "benchmark": "SP500",
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_perf,
        "instrument_base_100": instrument_base100,
        "benchmark_base_100": benchmark_base100,
    }


def main():
    snapshot = build_market_snapshot()

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print("Market configuration")
    print("Instrument : AAPL - Apple Inc.")
    print("Benchmark  : SP500 - S&P 500")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()
    print(f"Instrument return : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return  : {snapshot['benchmark_return']:.2f}%")
    print()
    print("Relative performance")
    print(f"AAPL vs SP500 : {snapshot['relative_performance']:+.2f} percentage points")
    print()
    print("Base 100")
    b100_i = snapshot["instrument_base_100"]
    b100_b = snapshot["benchmark_base_100"]
    print(f"AAPL  : {b100_i[0]['value']:.2f} -> {b100_i[-1]['value']:.2f}")
    print(f"SP500 : {b100_b[0]['value']:.2f} -> {b100_b[-1]['value']:.2f}")


if __name__ == "__main__":
    main()