# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source: data/sample/bloomberg_reference_sample.json

Live connectivity: not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

Teaching wrapper keys (not Bloomberg field mnemonics):

| MarketPulse field | Source field | Status |
|---|---|---|
| date | observation_date | available |
| ticker | application mapping | AAPL or SP500 |
| open | open_value | available |
| high | high_value | available |
| low | low_value | available |
| close | close_value | available |
| volume | volume_value | available (0 for SPX Index) |

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: YYYY-MM-DD string
- Input structure: JSON with series array, each with observations
- Missing fields: none (volume is 0 for index but field exists)
- Special normalization notes: provider_identifier must be mapped back to canonical ticker (AAPL, SP500)
- Expected canonical reference: data/sample/bloomberg_reference_expected.json