# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Instructor reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (instructor document, not present in this repository)
- Live connectivity: **not demonstrated**

The sample file declares itself as:

```text
sample_kind              : instructor_approved_fallback_fixture
access_mode              : approved_sample
is_live_bloomberg_output : false
```

Its values are illustrative teaching values reused from `data/sample/prices.csv`.
They are not certified Bloomberg historical observations.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier | Yahoo symbol (TD08) |
|---|---|---|---|
| Instrument | AAPL | AAPL US Equity | AAPL |
| Benchmark | SP500 | SPX Index | ^GSPC |

The canonical tickers `AAPL` and `SP500` are the only identifiers that reach `src/analytics.py`.
`AAPL US Equity` and `SPX Index` stay at the provider boundary.

## Inspected inputs

### Instrument - AAPL US Equity

| Item | Observed value |
|---|---|
| role | `instrument` |
| canonical_ticker | `AAPL` |
| provider_identifier | `AAPL US Equity` |
| observations | 21 |
| first observation_date | 2026-09-01 |
| last observation_date | 2026-09-30 |
| missing values | none |

### Benchmark - SPX Index

| Item | Observed value |
|---|---|
| role | `benchmark` |
| canonical_ticker | `SP500` |
| provider_identifier | `SPX Index` |
| observations | 21 |
| first observation_date | 2026-09-01 |
| last observation_date | 2026-09-30 |
| missing values | none (`volume_value` is always `0`, see notes) |

## Field mapping

The keys below are **teaching wrapper keys** defined by the approved sample.

```text
teaching wrapper key
!=
Bloomberg LIVE field mnemonic
```

No Bloomberg LIVE field name was observed in this session, so none is documented here.

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key, ISO text `YYYY-MM-DD`, keep as `str` |
| ticker | application mapping from `canonical_ticker` | `AAPL` or `SP500`, never the Bloomberg identifier |
| open | `open_value` | teaching wrapper key, convert to `float` |
| high | `high_value` | teaching wrapper key, convert to `float` |
| low | `low_value` | teaching wrapper key, convert to `float` |
| close | `close_value` | teaching wrapper key, convert to `float` |
| volume | `volume_value` | teaching wrapper key, convert to `int` |

## Target canonical row

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

- **Access mode:** APPROVED_SAMPLE (live connectivity not demonstrated)
- **Instrument identifier:** `AAPL US Equity` -> canonical `AAPL`
- **Benchmark identifier:** `SPX Index` -> canonical `SP500`
- **Date representation:** ISO text `YYYY-MM-DD` in `observation_date`, already in MarketPulse format
- **Input structure:** one JSON object with a `series` list; each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list of daily rows
- **Missing fields:** none in the sample; both series contain 21 observations on the same dates
- **Special normalization notes:**
  - JSON numbers may be integers (`248`, `6600`): always cast `open/high/low/close` to `float` and `volume` to `int`
  - `SPX Index` has `volume_value = 0` on every row: an index has no traded volume, so keep `0` and do not treat it as missing data
  - use `canonical_ticker` for the `ticker` field, never `provider_identifier`
  - keep TD07 `align_series()` to align instrument and benchmark on common dates
- **Expected canonical reference:** `data/sample/bloomberg_reference_expected.json`

## Validation

```text
[x] access mode is explicit
[x] instrument mapping is documented
[x] benchmark mapping is documented
[x] field source is identifiable
[x] canonical tickers remain AAPL and SP500
[x] no LIVE field name was invented
[x] APPROVED_SAMPLE wrapper keys are labelled as teaching keys
[x] missing fields are documented honestly
[x] no credential appears
[x] TD10 handoff is present
```
