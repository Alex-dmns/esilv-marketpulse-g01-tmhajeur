from pathlib import Path
import json


SAMPLE_FIXTURE_PATH = Path("data/sample/bloomberg_reference_sample.json")

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(
    identifier,
    start_date=None,
    end_date=None,
    access_mode="APPROVED_SAMPLE",
):
    if access_mode != "APPROVED_SAMPLE":
        raise ValueError(
            f"Unsupported Bloomberg access mode: {access_mode}"
        )

    with open(SAMPLE_FIXTURE_PATH, encoding="utf-8") as file:
        payload = json.load(file)

    for series in payload.get("series", []):
        if series.get("provider_identifier") == identifier:
            return series.get("observations", [])

    raise ValueError(
        f"No Bloomberg sample data found for {identifier}"
    )


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for observation in raw_data:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_bloomberg_prices(
    canonical_ticker,
    access_mode="APPROVED_SAMPLE",
):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(
            f"Unsupported canonical ticker for Bloomberg: {canonical_ticker}"
        )

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_observations = fetch_raw_bloomberg_history(
        identifier=identifier,
        access_mode=access_mode,
    )
    return normalize_bloomberg_history(
        raw_data=raw_observations,
        canonical_ticker=canonical_ticker,
    )