"""Bloomberg-stage provider for MarketPulse.

Access mode: APPROVED_SAMPLE.
Raw input comes from the instructor-approved fallback fixture, not from a
live Bloomberg connection. Mapping source: docs/BLOOMBERG_FIELD_MAPPING.md.
"""

import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "sample" / "bloomberg_reference_sample.json"
)

# Canonical MarketPulse ticker -> Bloomberg identifier.
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


# Raw input boundary.
# In LIVE mode, only the instructor-approved acquisition would go here.
# In APPROVED_SAMPLE mode, the series is read from the fallback fixture.
def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            observations = [
                observation
                for observation in series["observations"]
                if (start_date is None or observation["observation_date"] >= start_date)
                and (end_date is None or observation["observation_date"] <= end_date)
            ]
            return {**series, "observations": observations}

    raise ValueError(f"Unsupported Bloomberg identifier: {identifier}")


# Normalization boundary: teaching wrapper keys -> canonical rows.
# observation_date/open_value/... are NOT Bloomberg field mnemonics.
def normalize_bloomberg_history(raw_data, canonical_ticker):
    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError(
            f"Series {raw_data['provider_identifier']} belongs to "
            f"{raw_data['canonical_ticker']}, not {canonical_ticker}"
        )

    return [
        {
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        }
        for observation in raw_data["observations"]
    ]


def fetch_bloomberg_prices(canonical_ticker, start_date=None, end_date=None):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier, start_date, end_date)
    rows = normalize_bloomberg_history(raw_data, canonical_ticker)

    if not rows:
        raise ValueError(f"No Bloomberg-stage data returned for {identifier}")

    return rows
