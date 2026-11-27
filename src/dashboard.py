"""MarketPulse Dash dashboard (TD11).

Presentation only: every value comes from build_market_snapshot().
No provider call and no analytical formula belongs in this file.
"""

from dash import Dash, dcc, html
import plotly.graph_objects as go

from main import build_market_snapshot


# ── data: snapshot only ───────────────────────────────
snapshot = build_market_snapshot()

provider = snapshot["provider"]
access_mode = snapshot["access_mode"]
lookback = snapshot["lookback"]
interval = snapshot["interval"]

instrument = snapshot["instrument"]
benchmark = snapshot["benchmark"]

instrument_return = snapshot["instrument_return"]
benchmark_return = snapshot["benchmark_return"]
relative_performance = snapshot["relative_performance"]

instrument_base_100 = snapshot["instrument_base_100"]
benchmark_base_100 = snapshot["benchmark_base_100"]


# ── theme (OPTIONAL styling polish) ───────────────────
BG = "#0a0a0a"
CARD = "#121212"
BORDER = "#262626"
WHITE = "#ededed"
LIGHT = "#bdbdbd"
MID = "#6b6b6b"
GREEN = "#3ddc97"
RED = "#ff5c5c"
FONT = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"

CARD_STYLE = {
    "backgroundColor": CARD,
    "border": f"1px solid {BORDER}",
    "borderRadius": "10px",
    "padding": "14px 16px",
}


# ── local layout helpers (formatting only) ────────────
def card(title, children, **style):
    return html.Div(
        style={**CARD_STYLE, **style},
        children=[
            html.Div(title, style={"fontSize": "12px", "color": MID, "marginBottom": "8px"}),
            *children,
        ],
    )


def context_line(label, value):
    return html.Div(
        style={"display": "flex", "justifyContent": "space-between", "gap": "16px",
               "fontSize": "13px", "padding": "4px 0"},
        children=[
            html.Span(label, style={"color": MID}),
            html.Span(value, style={"color": WHITE, "textAlign": "right"}),
        ],
    )


def indicator(title, value, suffix):
    color = GREEN if value >= 0 else RED
    return card(title, [
        html.Div(f"{value:+.2f}{suffix}", style={"fontSize": "28px", "color": color}),
    ])


def base_100_trace(series, name, color, dash):
    return go.Scatter(
        x=[row["date"] for row in series],
        y=[row["value"] for row in series],
        mode="lines",
        name=name,
        line=dict(color=color, width=2, dash=dash),
    )


# ── context ───────────────────────────────────────────
context = card("Comparison context", [
    context_line("Provider", provider),
    context_line("Access mode", access_mode),
    context_line("Instrument", f"{instrument['ticker']} - {instrument['name']}"),
    context_line("Benchmark", f"{benchmark['ticker']} - {benchmark['name']}"),
    context_line("Lookback", lookback),
    context_line("Interval", interval),
])


# ── three performance indicators ──────────────────────
performance = html.Div(
    style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "14px"},
    children=[
        indicator(f"Instrument return ({instrument['ticker']})", instrument_return, "%"),
        indicator(f"Benchmark return ({benchmark['ticker']})", benchmark_return, "%"),
        indicator("Relative performance", relative_performance, " pts"),
    ],
)


# ── base-100 chart: both series ───────────────────────
figure = go.Figure()
figure.add_trace(base_100_trace(instrument_base_100, instrument["ticker"], WHITE, "solid"))
figure.add_trace(base_100_trace(benchmark_base_100, benchmark["ticker"], MID, "dot"))
figure.update_layout(
    title="Instrument vs Benchmark - Base 100",
    xaxis_title="Date",
    yaxis_title="Base 100",
    plot_bgcolor=CARD,
    paper_bgcolor=CARD,
    font=dict(family=FONT, color=LIGHT, size=11),
    xaxis=dict(showgrid=False, linecolor=BORDER),
    yaxis=dict(gridcolor=BORDER, zeroline=False),
    legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"),
    hovermode="x unified",
    margin=dict(l=50, r=20, t=60, b=40),
)


# ── app ───────────────────────────────────────────────
app = Dash(__name__, title="MarketPulse")
app.index_string = app.index_string.replace(
    "<head>", f"<head><style>html, body {{ margin: 0; background: {BG}; }}</style>"
)

app.layout = html.Div(
    style={"backgroundColor": BG, "color": WHITE, "fontFamily": FONT, "minHeight": "100vh",
           "padding": "24px 16px", "boxSizing": "border-box"},
    children=[
        html.Div(
            style={"maxWidth": "1100px", "margin": "0 auto", "display": "flex",
                   "flexDirection": "column", "gap": "14px"},
            children=[
                html.H1("MarketPulse", style={"margin": "0", "fontSize": "24px"}),
                html.P("Instrument vs Benchmark market comparison",
                       style={"margin": "0", "color": MID, "fontSize": "13px"}),
                context,
                performance,
                html.Div(style={**CARD_STYLE, "padding": "6px"}, children=[dcc.Graph(figure=figure)]),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=False)
