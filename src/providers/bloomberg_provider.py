import json
from pathlib import Path

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

SAMPLE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "sample" / "bloomberg_reference_sample.json"


def fetch_bloomberg_prices(canonical_ticker, mode="APPROVED_SAMPLE"):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]

    if mode == "APPROVED_SAMPLE":
        with open(SAMPLE_PATH) as f:
            data = json.load(f)

        for series in data["series"]:
            if series["canonical_ticker"] == canonical_ticker:
                raw_observations = series["observations"]
                break
        else:
            raise ValueError(f"No series found for {canonical_ticker}")

        return normalize_bloomberg_history(raw_observations, canonical_ticker)

    raise ValueError(f"Mode {mode} not implemented")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []
    for obs in raw_data:
        rows.append({
            "date": obs["observation_date"],
            "ticker": canonical_ticker,
            "open": float(obs["open_value"]),
            "high": float(obs["high_value"]),
            "low": float(obs["low_value"]),
            "close": float(obs["close_value"]),
            "volume": int(obs["volume_value"]),
        })
    return rows