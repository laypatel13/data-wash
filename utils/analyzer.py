import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ── Theme constants matching the app ──
BG         = "rgba(0,0,0,0)"
CARD_BG    = "#1c1c1c"
BORDER     = "#2a2a2a"
TEXT_1     = "#e8e8e8"
TEXT_2     = "#aaaaaa"
TEXT_3     = "#666666"
GRID       = "#222222"
FONT_FMLY  = "Copperplate, Copperplate Gothic Light, Georgia, serif"

# accent colors matching your badges
BLUE       = "#6ab0f5"
GREEN      = "#7ec98a"
ORANGE     = "#f5a623"
RED        = "#e05252"
GREY       = "#555555"

MARGIN     = dict(t=16, b=16, l=16, r=16)


def _base_layout(height=260):
    return dict(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family=FONT_FMLY, color=TEXT_2, size=10),
        margin=MARGIN,
        height=height,
        legend=dict(
            font=dict(family=FONT_FMLY, color=TEXT_2, size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER,
            borderwidth=1,
        ),
        xaxis=dict(
            gridcolor=GRID,
            linecolor=BORDER,
            tickcolor=BORDER,
            color=TEXT_3,
            tickfont=dict(family=FONT_FMLY, size=9),
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=GRID,
            linecolor=BORDER,
            tickcolor=BORDER,
            color=TEXT_3,
            tickfont=dict(family=FONT_FMLY, size=9),
            showgrid=True,
            zeroline=False,
        ),
    )


def analyze_dataframe(df: pd.DataFrame) -> dict:
    analysis = {}

    # ── Basic stats ──
    analysis["rows"]             = df.shape[0]
    analysis["cols"]             = df.shape[1]
    analysis["total_missing"]    = int(df.isnull().sum().sum())
    analysis["total_duplicates"] = int(df.duplicated().sum())
    analysis["memory_kb"]        = round(df.memory_usage(deep=True).sum() / 1024, 2)

    total_cells = df.shape[0] * df.shape[1]
    analysis["missing_pct"] = round(
        (analysis["total_missing"] / total_cells * 100) if total_cells > 0 else 0, 1
    )

    # ── Column breakdown ──
    col_info = []
    for col in df.columns:
        missing = int(df[col].isnull().sum())
        col_info.append({
            "name":        col,
            "dtype":       str(df[col].dtype),
            "missing":     missing,
            "missing_pct": round(missing / len(df) * 100, 1) if len(df) > 0 else 0,
            "unique":      int(df[col].nunique()),
        })
    analysis["columns"] = col_info

    # ── Numeric summary ──
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        desc = num_df.describe().round(2)
        analysis["numeric_summary"] = desc.to_html(
            classes="table table-dark table-bordered table-sm",
            border=0
        )
    else:
        analysis["numeric_summary"] = None

    # ────────────────────────────────────────
    # CHART 1 — Donut: data types breakdown
    # ────────────────────────────────────────
    dtype_counts = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        if "int" in dtype or "float" in dtype:
            dtype_counts["Numeric"]  = dtype_counts.get("Numeric", 0) + 1
        elif "object" in dtype or "string" in dtype:
            dtype_counts["Text"]     = dtype_counts.get("Text", 0) + 1
        elif "datetime" in dtype:
            dtype_counts["DateTime"] = dtype_counts.get("DateTime", 0) + 1
        elif "bool" in dtype:
            dtype_counts["Boolean"]  = dtype_counts.get("Boolean", 0) + 1
        else:
            dtype_counts["Other"]    = dtype_counts.get("Other", 0) + 1

    pie_colors = [BLUE, GREEN, ORANGE, RED, GREY]

    pie_fig = go.Figure(data=[go.Pie(
        labels=list(dtype_counts.keys()),
        values=list(dtype_counts.values()),
        hole=0.6,
        marker=dict(
            colors=pie_colors[:len(dtype_counts)],
            line=dict(color="#111111", width=2),
        ),
        textfont=dict(family=FONT_FMLY, color=TEXT_1, size=9),
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>%{value} columns<br>%{percent}<extra></extra>",
    )])

    layout = _base_layout(260)
    layout.pop("xaxis", None)
    layout.pop("yaxis", None)
    layout["showlegend"] = True
    layout["legend"]["orientation"] = "v"
    pie_fig.update_layout(**layout)
    analysis["pie_chart"] = pie_fig.to_json()

    # ────────────────────────────────────────
    # CHART 2 — Bar: missing values per column
    # ────────────────────────────────────────
    missing_series = df.isnull().sum()
    missing_series = missing_series[missing_series > 0].sort_values(ascending=False)

    if not missing_series.empty:
        bar_colors = [
            RED if v / len(df) > 0.3
            else ORANGE if v / len(df) > 0.1
            else BLUE
            for v in missing_series.values
        ]

        bar_fig = go.Figure(data=[go.Bar(
            x=list(missing_series.index),
            y=list(missing_series.values),
            marker=dict(
                color=bar_colors,
                line=dict(width=0),
                opacity=0.9,
            ),
            hovertemplate="<b>%{x}</b><br>Missing: %{y}<extra></extra>",
        )])

        layout = _base_layout(260)
        layout["xaxis"]["title"] = dict(text="Column", font=dict(size=9, color=TEXT_3))
        layout["yaxis"]["title"] = dict(text="Missing Count", font=dict(size=9, color=TEXT_3))
        layout["showlegend"] = False
        layout["bargap"] = 0.3
        bar_fig.update_layout(**layout)
        analysis["bar_chart"] = bar_fig.to_json()
    else:
        analysis["bar_chart"] = None

    # ────────────────────────────────────────
    # CHART 3 — Histogram: first numeric col
    # ────────────────────────────────────────
    if not num_df.empty:
        col_name = num_df.columns[0]
        col_data = num_df[col_name].dropna()

        hist_fig = go.Figure(data=[go.Histogram(
            x=col_data,
            nbinsx=20,
            marker=dict(
                color=GREEN,
                line=dict(color="#111111", width=1),
                opacity=0.85,
            ),
            hovertemplate="Range: %{x}<br>Count: %{y}<extra></extra>",
        )])

        layout = _base_layout(260)
        layout["xaxis"]["title"] = dict(text=col_name, font=dict(size=9, color=TEXT_3))
        layout["yaxis"]["title"] = dict(text="Count", font=dict(size=9, color=TEXT_3))
        layout["showlegend"] = False
        layout["bargap"] = 0.05
        hist_fig.update_layout(**layout)
        analysis["hist_chart"] = hist_fig.to_json()
        analysis["hist_col"]   = col_name
    else:
        analysis["hist_chart"] = None
        analysis["hist_col"]   = None

    return analysis