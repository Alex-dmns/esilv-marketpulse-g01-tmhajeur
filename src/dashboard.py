from pathlib import Path
from datetime import date
import statistics
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dash import Dash, dcc, html
import plotly.graph_objects as go
from main import build_market_snapshot

# ── data (snapshot only) ──────────────────────────────
snapshot = build_market_snapshot()

provider = snapshot["provider"]
access_mode = snapshot["access_mode"]
lookback = snapshot["lookback"]
interval = snapshot["interval"]
inst_ticker = snapshot["instrument"]["ticker"]
inst_name = snapshot["instrument"]["name"]
bench_ticker = snapshot["benchmark"]["ticker"]
bench_name = snapshot["benchmark"]["name"]
inst_return = snapshot["instrument_return"]
bench_return = snapshot["benchmark_return"]
relative_perf = snapshot["relative_performance"]

dates = [r["date"] for r in snapshot["instrument_base_100"]]
inst = [r["value"] for r in snapshot["instrument_base_100"]]
bench = [r["value"] for r in snapshot["benchmark_base_100"]]


def daily_returns(values):
    return [(values[i] / values[i - 1] - 1) * 100 for i in range(1, len(values))]


inst_daily = daily_returns(inst)
bench_daily = daily_returns(bench)
inst_vol = statistics.stdev(inst_daily)
bench_vol = statistics.stdev(bench_daily)

up_days = sum(1 for v in inst_daily if v > 0)
down_days = sum(1 for v in inst_daily if v < 0)
outperf_days = sum(1 for a, b in zip(inst_daily, bench_daily) if a > b)
underperf_days = sum(1 for a, b in zip(inst_daily, bench_daily) if a < b)
n_days = len(inst_daily)
outperf_pct = outperf_days / n_days * 100
ratio = [a / b for a, b in zip(inst, bench)]

# ── theme ─────────────────────────────────────────────
BG = "#0a0a0a"
CARD = "#121212"
BORDER = "#262626"
WHITE = "#ededed"
LIGHT = "#bdbdbd"
MID = "#6b6b6b"
DARK = "#2a2a2a"
GREEN = "#3ddc97"
RED = "#ff5c5c"
FONT = "'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace"


def signed(v, suffix="%"):
    return f"{v:+.2f}{suffix}"


def arrow(v):
    color = GREEN if v >= 0 else RED
    return html.Span(f"{'↑' if v >= 0 else '↓'} {abs(v):.2f}%", style={"color": color, "fontSize": "11px"})


def pills(labels, active):
    return html.Div(style={"display": "flex", "gap": "4px"}, children=[
        html.Span(label, style={
            "fontSize": "11px", "padding": "3px 9px", "borderRadius": "6px",
            "border": f"1px solid {LIGHT if label == active else BORDER}",
            "color": WHITE if label == active else LIGHT,
        })
        for label in labels
    ])


def icons():
    return html.Div(style={"display": "flex", "gap": "12px", "color": MID, "fontSize": "13px"},
                    children=[html.Span("⤓"), html.Span("···")])


def card(title, body, right=None, **style):
    base = {
        "backgroundColor": CARD, "border": f"1px solid {BORDER}", "borderRadius": "10px",
        "padding": "14px 16px", "display": "flex", "flexDirection": "column", "minHeight": "0",
    }
    base.update(style)
    header = html.Div(
        style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "12px"},
        children=[html.Span(title, style={"fontSize": "14px", "color": WHITE}), right],
    )
    return html.Div(style=base, children=[header, *body])


def graph(fig, **style):
    return dcc.Graph(figure=fig, config={"displayModeBar": False, "responsive": True},
                     style={"flex": "1", "minHeight": "0", **style})


def base_layout(**kw):
    layout = dict(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=MID, size=10),
        margin=dict(l=8, r=8, t=4, b=22),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=BORDER, tickfont=dict(color=LIGHT)),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=MID)),
        showlegend=False,
        hoverlabel=dict(bgcolor="#1c1c1c", bordercolor=BORDER, font=dict(family=FONT, color=WHITE, size=11)),
    )
    layout.update(kw)
    return layout


# ── main chart: candles built from consecutive base-100 closes ──
opens = [inst[0]] + inst[:-1]
main_fig = go.Figure()
main_fig.add_trace(go.Candlestick(
    x=dates, open=opens, close=inst,
    high=[max(o, c) for o, c in zip(opens, inst)],
    low=[min(o, c) for o, c in zip(opens, inst)],
    increasing=dict(line=dict(color=WHITE, width=1), fillcolor=WHITE),
    decreasing=dict(line=dict(color=LIGHT, width=1), fillcolor=CARD),
    name=inst_ticker,
))
main_fig.add_trace(go.Scatter(
    x=dates, y=bench, mode="lines", name=bench_ticker,
    line=dict(color=MID, width=1.2, dash="dot"),
    hovertemplate=f"{bench_ticker} %{{y:.2f}}<extra></extra>",
))
main_fig.add_hline(y=inst[-1], line=dict(color=LIGHT, width=1, dash="dot"))
main_fig.add_annotation(
    x=1, xref="paper", y=inst[-1], text=f"{inst[-1]:.2f}", showarrow=False, xanchor="left",
    font=dict(color="#0a0a0a", size=10, family=FONT), bgcolor=WHITE, borderpad=3,
)
peak = inst.index(max(inst))
main_fig.add_annotation(
    x=dates[peak], y=inst[peak], text=f"{inst[peak]:.2f}", showarrow=True, arrowcolor=MID,
    ax=-30, ay=-18, font=dict(color=LIGHT, size=10, family=FONT),
)
main_fig.update_layout(**base_layout(
    margin=dict(l=8, r=58, t=10, b=24),
    xaxis=dict(showgrid=False, zeroline=False, linecolor=BORDER, rangeslider=dict(visible=False),
               tickfont=dict(color=LIGHT), rangebreaks=[dict(bounds=["sat", "mon"])]),
    yaxis=dict(side="right", showgrid=False, zeroline=False, tickfont=dict(color=LIGHT), tickformat=".2f"),
    hovermode="x unified",
))

# ── daily return map (heatmap of squares) ─────────────
ROWS = 7
span = max(abs(v) for v in inst_daily + bench_daily) or 1


def bucket(v):
    return min(ROWS - 1, int((v + span) / (2 * span) * ROWS))


z = [[0] * n_days for _ in range(ROWS)]
for d in range(n_days):
    z[bucket(bench_daily[d])][d] = 1
    z[bucket(inst_daily[d])][d] = 2
heat_fig = go.Figure(go.Heatmap(
    z=z, x=dates[1:], zmin=0, zmax=2, xgap=5, ygap=5, showscale=False, hoverinfo="skip",
    colorscale=[[0, DARK], [0.33, DARK], [0.34, MID], [0.66, MID], [0.67, WHITE], [1, WHITE]],
))
heat_fig.update_layout(**base_layout(
    xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=LIGHT), nticks=6, tickformat="%b %d"),
    yaxis=dict(visible=False),
))

# ── return split donut ───────────────────────────────
donut_fig = go.Figure(go.Pie(
    values=[outperf_days, underperf_days, n_days - outperf_days - underperf_days],
    hole=0.8, sort=False, direction="clockwise", textinfo="none", hoverinfo="skip",
    marker=dict(
        colors=[WHITE, MID, DARK],
        pattern=dict(shape=["", "/", ""], fgcolor=LIGHT, bgcolor=DARK, size=4),
        line=dict(color=CARD, width=3),
    ),
))
donut_fig.update_layout(**base_layout(margin=dict(l=0, r=0, t=0, b=0)))
donut_fig.add_annotation(text=f"{outperf_pct:.0f} %", showarrow=False, y=0.56,
                         font=dict(size=26, color=WHITE, family=FONT))
donut_fig.add_annotation(text="Outperf.", showarrow=False, y=0.4, font=dict(size=11, color=MID, family=FONT))

# ── weekly returns (hatched vs solid bars) ───────────
weeks = {}
for i, d in enumerate(dates):
    weeks.setdefault(date.fromisoformat(d).isocalendar()[1], []).append(i)
week_labels, inst_weekly, bench_weekly = [], [], []
prev = 0
for idx in weeks.values():
    last = idx[-1]
    week_labels.append(date.fromisoformat(dates[idx[0]]).strftime("%b %d"))
    inst_weekly.append((inst[last] / inst[prev] - 1) * 100)
    bench_weekly.append((bench[last] / bench[prev] - 1) * 100)
    prev = last

week_fig = go.Figure()
week_fig.add_trace(go.Bar(
    x=week_labels, y=bench_weekly, name=bench_ticker,
    marker=dict(color=CARD, line=dict(color=LIGHT, width=1), pattern=dict(shape="/", fgcolor=LIGHT, size=5)),
    hovertemplate=f"{bench_ticker} %{{y:.2f}}%<extra></extra>",
))
week_fig.add_trace(go.Bar(
    x=week_labels, y=inst_weekly, name=inst_ticker, marker=dict(color="#dcdcdc", line=dict(width=0)),
    hovertemplate=f"{inst_ticker} %{{y:.2f}}%<extra></extra>",
))
week_fig.update_layout(**base_layout(
    barmode="group", bargap=0.35, bargroupgap=0.12,
    margin=dict(l=36, r=8, t=4, b=22),
    yaxis=dict(showgrid=False, zeroline=True, zerolinecolor=BORDER, ticksuffix="%", tickfont=dict(color=MID)),
))

# ── relative strength area ───────────────────────────
rs_fig = go.Figure()
rs_fig.add_trace(go.Scatter(x=dates, y=[1] * len(dates), mode="lines",
                            line=dict(color=MID, width=1, dash="dot"), hoverinfo="skip"))
rs_fig.add_trace(go.Scatter(
    x=dates, y=ratio, mode="lines", fill="tonexty", fillcolor="rgba(150,150,150,0.45)",
    line=dict(color=LIGHT, width=1.5, shape="spline"),
    hovertemplate=f"{inst_ticker}/{bench_ticker} %{{y:.4f}}<extra></extra>",
))
rs_fig.update_layout(**base_layout(
    margin=dict(l=8, r=44, t=4, b=22), hovermode="x unified",
    xaxis=dict(showgrid=False, zeroline=False, linecolor=BORDER, tickfont=dict(color=LIGHT), tickformat="%d %b"),
    yaxis=dict(side="right", showgrid=False, zeroline=False, tickformat=".3f", tickfont=dict(color=MID)),
))


# ── small html pieces ────────────────────────────────
def stat(label, value, sub=None, color=WHITE):
    return html.Div([
        html.Div(label, style={"fontSize": "11px", "color": MID, "marginBottom": "6px"}),
        html.Div(value, style={"fontSize": "21px", "color": color}),
        html.Div(sub, style={"marginTop": "4px"}) if sub is not None else None,
    ])


def waffle():
    cells = []
    max_move = max(abs(v) for v in inst_daily) or 1
    for v in inst_daily:
        lit = max(1, round(abs(v) / max_move * 6))
        col = [html.Div(style={
            "width": "100%", "aspectRatio": "1", "borderRadius": "2px",
            "backgroundColor": (WHITE if v >= 0 else MID) if row >= 6 - lit else DARK,
        }) for row in range(6)]
        cells.append(html.Div(col, style={"display": "flex", "flexDirection": "column", "gap": "3px", "flex": "1"}))
    return html.Div(cells, style={"display": "flex", "gap": "3px", "marginTop": "14px"})


def legend_item(swatch, label, value):
    return html.Div(style={"display": "flex", "alignItems": "center", "gap": "6px"}, children=[
        html.Span(style={"width": "8px", "height": "8px", "backgroundColor": swatch, "display": "inline-block"}),
        html.Span(label, style={"color": WHITE, "fontSize": "11px"}),
        html.Span(value, style={"color": MID, "fontSize": "11px"}),
    ])


def stripes(share, label, color):
    return html.Div(style={
        "flex": f"{max(share, 6)}", "borderLeft": f"2px solid {LIGHT}", "paddingLeft": "10px",
        "display": "flex", "flexDirection": "column",
    }, children=[
        html.Div(label, style={"fontSize": "11px", "color": MID}),
        html.Div(f"{share:.0f} %", style={"fontSize": "26px", "color": WHITE, "margin": "4px 0 10px"}),
        html.Div(style={
            "flex": "1", "minHeight": "60px",
            "background": f"repeating-linear-gradient(90deg, {color} 0 1px, transparent 1px 4px)",
        }),
    ])


vol_total = inst_vol + bench_vol
inst_vol_share = inst_vol / vol_total * 100
bench_vol_share = bench_vol / vol_total * 100

summary = (
    f"{inst_ticker} returned {signed(inst_return)} over {lookback} "
    f"against {signed(bench_return)} for {bench_ticker}, "
    f"i.e. {signed(relative_perf, ' pts')} of relative performance. "
    f"It beat the benchmark on {outperf_days} of {n_days} sessions."
)

# ── app ───────────────────────────────────────────────
app = Dash(__name__, title="MarketPulse")
app.index_string = app.index_string.replace(
    "<head>",
    "<head><style>"
    f"html, body {{ margin: 0; padding: 0; background: {BG}; }}"
    "@media (max-width: 1100px) {"
    " .mp-grid { grid-template-columns: minmax(0, 1fr) !important;"
    " grid-template-rows: none !important; grid-auto-rows: minmax(300px, auto); }"
    " .mp-grid > * { grid-column: auto !important; } }"
    "</style>",
    1,
)

app.layout = html.Div(
    style={
        "backgroundColor": BG, "minHeight": "100vh", "fontFamily": FONT, "color": WHITE,
        "padding": "14px", "boxSizing": "border-box", "display": "flex", "flexDirection": "column", "gap": "12px",
    },
    children=[
        # nav
        html.Div(style={"display": "flex", "alignItems": "center", "gap": "12px 28px", "padding": "4px 6px", "flexWrap": "wrap"}, children=[
            html.Span("✳ MarketPulse", style={"fontSize": "20px", "color": WHITE}),
            html.Div(style={
                "display": "flex", "justifyContent": "space-between", "alignItems": "center",
                "border": f"1px solid {BORDER}", "borderRadius": "8px", "padding": "7px 12px",
                "width": "300px", "color": MID, "fontSize": "12px",
            }, children=[html.Span(f"⌕  {inst_ticker} vs {bench_ticker}"),
                         html.Span("/", style={"border": f"1px solid {BORDER}", "borderRadius": "4px", "padding": "0 6px"})]),
            html.Span("Overview", style={"color": WHITE, "fontSize": "12px"}),
            html.Span("Base 100", style={"color": LIGHT, "fontSize": "12px"}),
            html.Span("Returns", style={"color": LIGHT, "fontSize": "12px"}),
            html.Div(style={"marginLeft": "auto", "textAlign": "right"}, children=[
                html.Div(provider, style={"fontSize": "12px", "color": WHITE}),
                html.Div(f"mode {access_mode} · {interval}", style={"fontSize": "10px", "color": MID}),
            ]),
        ]),

        # grid
        html.Div(
            className="mp-grid",
            style={
                "display": "grid", "gap": "12px", "flex": "1",
                "gridTemplateColumns": "minmax(0, 1.1fr) minmax(0, 1fr) minmax(0, 0.95fr)",
                "gridTemplateRows": "minmax(340px, 1.3fr) minmax(260px, 1fr) minmax(300px, 1.1fr)",
            },
            children=[
                # main chart
                card(
                    html.Span([
                        html.Span(inst_ticker, style={"color": WHITE}),
                        html.Span(f"  {inst_name}", style={"color": MID, "fontSize": "11px"}),
                        html.Span("   Base 100", style={"color": WHITE, "fontSize": "12px"}),
                        html.Span(f" / {bench_ticker}", style={"color": MID, "fontSize": "12px"}),
                    ]),
                    [graph(main_fig),
                     html.Div("log / auto", style={"textAlign": "right", "fontSize": "11px", "color": LIGHT})],
                    right=html.Div(style={"display": "flex", "gap": "16px", "alignItems": "center"},
                                   children=[pills(["1D", "7D", "1M", "1Y", "All"], "1M"), icons()]),
                    gridColumn="1 / 3",
                ),

                # returns (portfolio-style)
                card("Returns", [
                    html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr 1fr", "gap": "10px"}, children=[
                        stat(inst_ticker, f"{inst[-1]:.2f}", arrow(inst_return)),
                        stat(bench_ticker, f"{bench[-1]:.2f}", arrow(bench_return)),
                        stat("Relative", signed(relative_perf, ""), arrow(relative_perf)),
                    ]),
                    waffle(),
                    html.Div(style={"display": "flex", "gap": "16px", "marginTop": "12px", "flexWrap": "wrap"}, children=[
                        legend_item(WHITE, "Up", str(up_days)),
                        legend_item(MID, "Down", str(down_days)),
                        legend_item(DARK, "Max", signed(max(inst_daily))),
                        legend_item(DARK, "Min", signed(min(inst_daily))),
                    ]),
                ], right=icons()),

                # heatmap
                card("Daily Return Map", [
                    graph(heat_fig),
                    html.Div(style={"display": "flex", "gap": "16px", "marginTop": "6px"}, children=[
                        legend_item(WHITE, inst_ticker, ""),
                        legend_item(MID, bench_ticker, ""),
                    ]),
                ], right=pills(["1D", "7D", "1M", "All"], "1M")),

                # volatility split (holders-style)
                card("Volatility Split", [
                    html.Div(style={"display": "flex", "flex": "1", "gap": "6px"}, children=[
                        stripes(inst_vol_share, inst_ticker, WHITE),
                        stripes(bench_vol_share, bench_ticker, MID),
                    ]),
                    html.Div(style={"display": "flex", "gap": "18px", "marginTop": "10px", "fontSize": "11px"}, children=[
                        html.Span([html.Span(f"{inst_ticker} σ ", style={"color": WHITE}),
                                   html.Span(f"{inst_vol:.2f}%", style={"color": MID})]),
                        html.Span([html.Span(f"{bench_ticker} σ ", style={"color": WHITE}),
                                   html.Span(f"{bench_vol:.2f}%", style={"color": MID})]),
                    ]),
                ], right=html.Span("daily σ", style={"fontSize": "11px", "color": LIGHT})),

                # donut (unlocks-style)
                card("Session Split", [
                    html.Div(style={"display": "flex", "flex": "1", "alignItems": "center", "gap": "14px"}, children=[
                        graph(donut_fig, height="100%"),
                        html.Div(style={"display": "flex", "flexDirection": "column", "gap": "14px", "flexShrink": "0"}, children=[
                            legend_item(WHITE, "Outperf.", f"{outperf_days}"),
                            legend_item(LIGHT, "Underperf.", f"{underperf_days}"),
                            legend_item(DARK, "Equal", f"{n_days - outperf_days - underperf_days}"),
                            legend_item(DARK, "Sessions", f"{n_days}"),
                        ]),
                    ]),
                ], right=html.Span(f"{inst_ticker} vs {bench_ticker}", style={"fontSize": "11px", "color": LIGHT})),

                # weekly bars (buys/sells-style)
                card("Weekly Returns", [
                    html.Div(style={"display": "flex", "gap": "26px", "marginBottom": "8px"}, children=[
                        stat("Obs", str(len(dates))),
                        stat(f"{inst_ticker}", signed(inst_return)),
                        stat(f"{bench_ticker}", signed(bench_return)),
                        stat("Spread", signed(relative_perf, ""), color=GREEN if relative_perf >= 0 else RED),
                    ]),
                    graph(week_fig),
                ], right=pills(["1D", "7D", "1M", "1Y", "All"], "1M")),

                # relative strength (long/short-style)
                card("Relative Strength", [graph(rs_fig)],
                     right=html.Span(f"{inst_ticker} / {bench_ticker}", style={"fontSize": "11px", "color": LIGHT})),

                # notes (assistant-style)
                card("Snapshot Notes", [
                    html.Div(style={"display": "flex", "flexDirection": "column", "gap": "14px", "flex": "1",
                                    "justifyContent": "center"}, children=[
                        html.Div(style={
                            "alignSelf": "flex-end", "backgroundColor": "#1e1e1e", "borderRadius": "8px",
                            "padding": "12px 14px", "fontSize": "12px", "color": LIGHT, "maxWidth": "80%",
                        }, children=[html.Div(f"{inst_ticker} vs {bench_ticker} — {lookback}"),
                                     html.Div(dates[-1], style={"textAlign": "right", "color": MID, "fontSize": "10px", "marginTop": "6px"})]),
                        html.Div(style={
                            "alignSelf": "flex-start", "backgroundColor": "#e6e6e6", "borderRadius": "8px",
                            "padding": "12px 14px", "fontSize": "12px", "color": "#111", "maxWidth": "88%", "lineHeight": "1.5",
                        }, children=[html.Div(summary),
                                     html.Div(provider, style={"color": "#777", "fontSize": "10px", "marginTop": "6px"})]),
                    ]),
                ], right=icons()),
            ],
        ),
    ],
)

if __name__ == "__main__":
    app.run(debug=False)
