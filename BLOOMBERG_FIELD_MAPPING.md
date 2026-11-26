## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| `date` | `observation_date` | Mapped from approved sample teaching wrapper key (`YYYY-MM-DD`) |
| `ticker` | `canonical_ticker` (series-level mapping) | Preserves `AAPL` and `SP500` instead of `AAPL US Equity` and `SPX Index` |
| `open` | `open_value` | Mapped from approved sample teaching wrapper key (cast to `float`) |
| `high` | `high_value` | Mapped from approved sample teaching wrapper key (cast to `float`) |
| `low` | `low_value` | Mapped from approved sample teaching wrapper key (cast to `float`) |
| `close` | `close_value` | Mapped from approved sample teaching wrapper key (cast to `float`) |
| `volume` | `volume_value` | Mapped from approved sample teaching wrapper key (cast to `int`; `0` for `SP500`) |