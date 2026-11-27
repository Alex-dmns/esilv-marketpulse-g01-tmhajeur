# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md`
- Live connectivity: not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | teaching wrapper key |
| ticker | application mapping | AAPL or SP500 |
| open | `open_value` | teaching wrapper key |
| high | `high_value` | teaching wrapper key |
| low | `low_value` | teaching wrapper key |
| close | `close_value` | teaching wrapper key |
| volume | `volume_value` | teaching wrapper key |

Teaching wrapper keys are not Bloomberg LIVE field mnemonics.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: text `YYYY-MM-DD`
- Input structure: JSON with a `series` list, one series per identifier, each with an `observations` list
- Missing fields: none (21 observations per series)
- Special normalization notes: convert prices to `float` and volume to `int`; SPX Index volume is always `0`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
