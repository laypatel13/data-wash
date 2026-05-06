import pandas as pd
import numpy as np


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """
    Generate a full analysis summary for a dataframe.
    Returns a dict consumed by analyze.html.
    """
    analysis = {}

    # Basic shape
    analysis["rows"] = df.shape[0]
    analysis["cols"] = df.shape[1]
    analysis["total_missing"] = int(df.isnull().sum().sum())
    analysis["total_duplicates"] = int(df.duplicated().sum())
    analysis["memory_kb"] = round(df.memory_usage(deep=True).sum() / 1024, 2)

    # Missing % overall
    total_cells = df.shape[0] * df.shape[1]
    analysis["missing_pct"] = round(
        (analysis["total_missing"] / total_cells * 100) if total_cells > 0 else 0, 1
    )

    # Column-level breakdown
    col_info = []
    for col in df.columns:
        missing = int(df[col].isnull().sum())
        col_info.append({
            "name": col,
            "dtype": str(df[col].dtype),
            "missing": missing,
            "missing_pct": round(missing / len(df) * 100, 1) if len(df) > 0 else 0,
            "unique": int(df[col].nunique()),
        })
    analysis["columns"] = col_info

    # Numeric describe() as HTML table
    num_df = df.select_dtypes(include=[np.number])
    if not num_df.empty:
        desc = num_df.describe().round(2)
        analysis["numeric_summary"] = desc.to_html(
            classes="table table-dark table-bordered table-sm",
            border=0
        )
    else:
        analysis["numeric_summary"] = None

    return analysis