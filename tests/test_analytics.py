import pytest

from analytics import align_series, calculate_base_100, calculate_period_return
from providers.bloomberg_provider import fetch_raw_bloomberg_history, normalize_bloomberg_history


def row(date, ticker, close):
    return {"date": date, "ticker": ticker, "close": close}


def test_align_series_keeps_only_common_dates_in_order():
    instrument = [
        row("2026-09-03", "AAPL", 103.0),
        row("2026-09-01", "AAPL", 101.0),
        row("2026-09-02", "AAPL", 102.0),
    ]
    benchmark = [
        row("2026-09-01", "SP500", 6600.0),
        row("2026-09-03", "SP500", 6620.0),
        row("2026-09-04", "SP500", 6630.0),
    ]

    aligned_instrument, aligned_benchmark = align_series(instrument, benchmark)

    assert [r["date"] for r in aligned_instrument] == ["2026-09-01", "2026-09-03"]
    assert [r["date"] for r in aligned_benchmark] == ["2026-09-01", "2026-09-03"]


def test_period_return_known_value():
    prices = [row("2026-09-01", "AAPL", 250.0), row("2026-09-30", "AAPL", 266.2)]

    assert calculate_period_return(prices) == pytest.approx(6.48)


def test_base_100_starts_at_100_and_matches_period_return():
    prices = [
        row("2026-09-01", "AAPL", 250.0),
        row("2026-09-02", "AAPL", 255.0),
        row("2026-09-30", "AAPL", 266.2),
    ]

    base_100 = calculate_base_100(prices)

    assert base_100[0]["value"] == pytest.approx(100.0)
    assert base_100[-1]["value"] == pytest.approx(100 + calculate_period_return(prices))
    assert prices[0]["close"] == 250.0  # original rows are not modified


def test_bloomberg_normalization_uses_canonical_ticker_and_types():
    raw = fetch_raw_bloomberg_history("SPX Index")

    rows = normalize_bloomberg_history(raw, "SP500")

    assert len(rows) == 21
    assert {r["ticker"] for r in rows} == {"SP500"}
    assert set(rows[0]) == {"date", "ticker", "open", "high", "low", "close", "volume"}
    assert isinstance(rows[0]["close"], float)
    assert isinstance(rows[0]["volume"], int)
