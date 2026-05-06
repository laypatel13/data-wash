import pandas as pd
import numpy as np


def analyze_dataframe(df: pd.DataFrame) -> dict:
    """
    Generate analysis summary for a dataframe.
    Returns a dict of stats used by the template.
    """
    analysis = {}

    # Basic shape
    analysis["rows"] = df.shape[0]
    analysis["cols"] = df.shape[1]
    analysis["total_missing"] = int(df.isnull().sum().sum())
    analysis["total_duplicates"] = int(df.duplicated().sum())
    analysis["memory_kb"] = round(df.memory_usage(deep=True).sum() / 1024, 2)

    # Column-level info
    col_info = []
    for col in df.columns:
        col_info.append({
            "name": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "missing_pct": round(df[col].isnull().mean() * 100, 1),
            "unique": int(df[col].nunique()),
        })
    analysis["columns"] = col_info

    # Numeric summary
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