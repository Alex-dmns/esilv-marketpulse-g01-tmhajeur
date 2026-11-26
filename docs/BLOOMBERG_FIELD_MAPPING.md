# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (not present in the team repository at the time of writing; mapping below is taken from the fixture's own `schema_note` and the expected canonical file)
- Live connectivity: **not demonstrated**

The fixture declares itself as:

- `sample_kind`: `instructor_approved_fallback_fixture`
- `access_mode`: `approved_sample`
- `is_live_bloomberg_output`: `false`
- `provenance`: illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg observations.

This document must not be presented as proof of LIVE Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

Provider identifier comparison:

| Canonical | CSV | Yahoo | Bloomberg |
|---|---|---|---|
| AAPL | AAPL | AAPL | AAPL US Equity |
| SP500 | SP500 | ^GSPC | SPX Index |

Provider identifiers stay at the provider boundary. `analytics.py` only receives the canonical tickers `AAPL` and `SP500`.

## Inspected inputs

| Series | `provider_identifier` | `canonical_ticker` | Observations | First date | Last date |
|---|---|---|---|---|---|
| instrument | AAPL US Equity | AAPL | 21 | 2026-09-01 | 2026-09-30 |
| benchmark | SPX Index | SP500 | 21 | 2026-09-01 | 2026-09-30 |

Input structure:

```text
{
  ...metadata...,
  "series": [
    {
      "role": "instrument" | "benchmark",
      "canonical_ticker": "...",
      "provider_identifier": "...",
      "observations": [
        { "observation_date", "open_value", "high_value",
          "low_value", "close_value", "volume_value" }
      ]
    }
  ]
}
```

## Field mapping

The source keys below are **teaching wrapper keys** defined by the approved fixture.

```text
teaching wrapper key
!=
Bloomberg LIVE field mnemonic
```

No Bloomberg field mnemonic has been observed in this session, and none is invented here.

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Teaching wrapper key. String `YYYY-MM-DD`, kept as-is. |
| ticker | application mapping (`series.canonical_ticker`) | `AAPL` or `SP500`. Never use `provider_identifier` here. |
| open | `open_value` | Teaching wrapper key. Convert to `float`. |
| high | `high_value` | Teaching wrapper key. Convert to `float`. |
| low | `low_value` | Teaching wrapper key. Convert to `float`. |
| close | `close_value` | Teaching wrapper key. Convert to `float`. |
| volume | `volume_value` | Teaching wrapper key. Convert to `int`. Always `0` for `SPX Index`. |

Target canonical row (shape only):

```python
{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592.0,
    "high": 6615.0,
    "low": 6580.0,
    "close": 6600.0,
    "volume": 0,
}
```

## TD10 handoff

- Access mode: APPROVED_SAMPLE (live connectivity not demonstrated).
- Instrument identifier: `AAPL US Equity` -> canonical `AAPL`.
- Benchmark identifier: `SPX Index` -> canonical `SP500`.
- Date representation: string `YYYY-MM-DD` in `observation_date`; no time zone, no timestamp.
- Input structure: one JSON file, `series` list, one entry per role, each with an `observations` list.
- Missing fields: none in the fixture. All six wrapper keys are present for all 42 observations.
- Special normalization notes:
  - Some prices are JSON integers (e.g. `close_value: 250`, `low_value: 248`): cast with `float()` so every price field is a `float`.
  - `volume_value` is `0` for `SPX Index` (an index has no traded volume). Keep `0`; do not treat it as missing.
  - Select series by `role` / `canonical_ticker`, not by position in the list.
  - Output rows must use `canonical_ticker`, never `provider_identifier`.
  - Expected canonical reference: `data/sample/bloomberg_reference_expected.json` (42 rows, 21 AAPL + 21 SP500) to validate the TD10 provider output.
- Analytics: TD07 `analytics.py` must be reused unchanged.

## Provider boundary

```text
bloomberg_reference_sample.json
(AAPL US Equity, SPX Index, *_value keys)
        |
        v
TD10 bloomberg_provider.py
(identifier + wrapper-key normalization)
        |
        v
canonical rows (AAPL, SP500, date/open/high/low/close/volume)
        |
        v
analytics.py (unchanged)
```

Provider-specific identifiers and wrapper keys disappear inside the TD10 provider.

## Security

No credential, session token or terminal identifier is included in this document.
