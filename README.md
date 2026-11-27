# ESILV MarketPulse - Team G01 Tmahjeur

[![Course: MESIFI472326](https://img.shields.io/badge/course-MESIFI472326-1f6feb.svg)](#)
[![ESILV A4](https://img.shields.io/badge/ESILV-A4-111827.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)](https://www.python.org/)

**MarketPulse** compares one financial instrument with its benchmark over the same period, then shows the result in the terminal and in a Dash dashboard.

> Is the instrument outperforming or underperforming its benchmark over the same period and frequency?

## Market configuration

| Item | Value |
|---|---|
| Instrument | AAPL - Apple Inc. |
| Benchmark | SP500 - S&P 500 |
| Lookback | 1 month |
| Interval | Daily |

Computed indicators:

- period return of the instrument and of the benchmark;
- relative performance (instrument minus benchmark, in percentage points);
- base-100 series for both, plotted on one chart.

## Provider and access mode

The final release uses:

```text
Provider    : Bloomberg stage
Access mode : APPROVED_SAMPLE
Source      : data/sample/bloomberg_reference_sample.json
```

`APPROVED_SAMPLE` uses the instructor-approved fallback fixture.
**It is not live Bloomberg data and does not prove live Bloomberg connectivity.**

Field mapping: [docs/BLOOMBERG_FIELD_MAPPING.md](docs/BLOOMBERG_FIELD_MAPPING.md)

Other providers are still available through `build_market_snapshot(provider)` in `src/main.py`:

| Provider | Value | Access mode |
|---|---|---|
| Bloomberg stage (default) | `"bloomberg"` | APPROVED_SAMPLE |
| Yahoo Finance via yfinance | `"yahoo"` | LIVE, requires internet access |
| Local CSV | `"csv"` | LOCAL_SAMPLE |

## Installation

Requirements: Python 3.x and `pip`.

```bash
git clone https://github.com/Alex-dmns/esilv-marketpulse-g01-tmhajeur.git
cd esilv-marketpulse-g01-tmhajeur
python -m pip install -r requirements.txt
```

Direct dependencies (`requirements.txt`):

```text
yfinance
dash
plotly
```

## Run

From the repository root.

Terminal:

```bash
python src/main.py
```

Dashboard:

```bash
python src/dashboard.py
```

Then open the local URL displayed by Dash (by default <http://127.0.0.1:8050>). Stop the server with `Ctrl+C`.

## Environment constraints

- The default Bloomberg stage runs offline from the approved sample file. No Bloomberg terminal or credential is needed.
- No live Bloomberg environment was available, so no Bloomberg connector is installed or imported.
- The Yahoo path needs internet access. `yfinance` is a community library, not the official Yahoo Finance API.
- On Windows, use `python` (or `py`) in PowerShell. On Linux / macOS, `python3` may be required.

## Architecture

```text
src/
├── main.py                  build_market_snapshot(...) + terminal output
├── analytics.py             alignment, period return, base 100, relative performance
├── dashboard.py             Dash presentation of the same snapshot
└── providers/
    ├── __init__.py
    ├── yahoo_provider.py    Yahoo -> canonical rows (AAPL, ^GSPC -> SP500)
    └── bloomberg_provider.py  Bloomberg stage -> canonical rows (AAPL US Equity, SPX Index)
```

```text
provider -> canonical rows -> analytics.py -> build_market_snapshot() -> terminal / Dash
```

Provider identifiers (`^GSPC`, `AAPL US Equity`, `SPX Index`) stay inside `src/providers/`.
`analytics.py` only receives the canonical tickers `AAPL` and `SP500`.

## Evidence

Checkpoint evidence is stored per student under:

```text
evidence/checkpoint-a/<github-username>/
evidence/checkpoint-b/<github-username>/
evidence/checkpoint-c/<github-username>/
```

Lab reports are stored under `rendu_tp/<student>/`.

## Team

See [TEAM.md](TEAM.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

No password, API key, access token or Bloomberg credential is committed to this repository.

---

**Course:** MESIFI472326 - Python, Git, Linux · **School:** ESILV - A4
