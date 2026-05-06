import pandas as pd
import numpy as np


def clean_dataframe(df: pd.DataFrame, options: dict) -> tuple[pd.DataFrame, list]:
    """
    Clean a dataframe based on user-selected options.
    Returns (cleaned_df, list of changes made).
    """
    changes = []
    original_rows = len(df)
    original_cols = len(df.columns)

    # 1. Standardize column headers
    if options.get("standardize_headers"):
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(r"[\s]+", "_", regex=True)
            .str.replace(r"[^\w]", "", regex=True)
        )
        changes.append("✅ Column headers standardized to snake_case")

    # 2. Strip whitespace from string columns
    if options.get("strip_whitespace"):
        str_cols = df.select_dtypes(include="object").columns
        df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())
        changes.append(f"✅ Stripped whitespace from {len(str_cols)} text column(s)")

    # 3. Drop fully empty columns
    if options.get("drop_empty_cols"):
        before = len(df.columns)
        df.dropna(axis=1, how="all", inplace=True)
        dropped = before - len(df.columns)
        if dropped:
            changes.append(f"✅ Dropped {dropped} fully empty column(s)")

    # 4. Fill missing numeric values
    fill_numeric = options.get("fill_numeric", "mean")
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        missing = df[col].isnull().sum()
        if missing > 0:
            if fill_numeric == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif fill_numeric == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif fill_numeric == "zero":
                df[col].fillna(0, inplace=True)
            changes.append(f"✅ Filled {missing} missing value(s) in '{col}' with {fill_numeric}")

    # 5. Fill missing categorical values
    fill_cat = options.get("fill_categorical", "mode")
    cat_cols = df.select_dtypes(include="object").columns
    for col in cat_cols:
        missing = df[col].isnull().sum()
        if missing > 0:
            if fill_cat == "mode":
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col].fillna(mode_val[0], inplace=True)
            elif fill_cat == "unknown":
                df[col].fillna("Unknown", inplace=True)
            changes.append(f"✅ Filled {missing} missing value(s) in '{col}' with {fill_cat}")

    # 6. Remove duplicate rows
    if options.get("drop_duplicates"):
        before = len(df)
        df.drop_duplicates(inplace=True)
        dropped = before - len(df)
        if dropped:
            changes.append(f"✅ Removed {dropped} duplicate row(s)")

    # 7. Remove outliers using IQR (numeric cols only)
    if options.get("remove_outliers"):
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            before = len(df)
            df = df[~((df[col] < (Q1 - 3.0 * IQR)) | (df[col] > (Q3 + 3.0 * IQR)))]
            removed = before - len(df)
            if removed:
                changes.append(f"✅ Removed {removed} outlier(s) from '{col}' using IQR")

    if not changes:
        changes.append("ℹ️ No changes made — data looks clean already!")

    return df, changes