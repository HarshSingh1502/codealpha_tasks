"""Core exploratory data analysis helpers."""

from typing import Any

import numpy as np
import pandas as pd


def dataset_overview(df: pd.DataFrame) -> dict[str, Any]:
    """Return a structured overview of the dataset."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    return {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "datetime_columns": datetime_cols,
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().mean() * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1_048_576, 2),
    }


def numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Descriptive statistics for numeric columns."""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.empty:
        return pd.DataFrame()
    return numeric.describe().T.round(2)


def categorical_summary(df: pd.DataFrame, max_cardinality: int = 20) -> dict[str, pd.Series]:
    """Value counts for categorical columns with limited cardinality."""
    summaries = {}
    for col in df.select_dtypes(include=["object", "category"]).columns:
        if df[col].nunique() <= max_cardinality:
            summaries[col] = df[col].value_counts()
    return summaries


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation matrix for numeric features."""
    numeric = df.select_dtypes(include=[np.number])
    if numeric.shape[1] < 2:
        return pd.DataFrame()
    return numeric.corr().round(3)


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.Series:
    """Flag outliers using the IQR method for a numeric column."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (df[column] < lower) | (df[column] > upper)


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize outlier counts per numeric column."""
    rows = []
    for col in df.select_dtypes(include=[np.number]).columns:
        mask = detect_outliers_iqr(df, col)
        rows.append(
            {
                "column": col,
                "outlier_count": int(mask.sum()),
                "outlier_pct": round(mask.mean() * 100, 2),
            }
        )
    return pd.DataFrame(rows)


def top_countries(df: pd.DataFrame, column: str = "country", top_n: int = 10) -> pd.Series:
    """Count titles by country, splitting multi-country entries."""
    if column not in df.columns:
        return pd.Series(dtype=int)
    exploded = df[column].dropna().str.split(",").explode().str.strip()
    return exploded.value_counts().head(top_n)


def top_genres(df: pd.DataFrame, column: str = "listed_in", top_n: int = 15) -> pd.Series:
    """Count titles by genre, splitting multi-genre entries."""
    if column not in df.columns:
        return pd.Series(dtype=int)
    exploded = df[column].dropna().str.split(",").explode().str.strip()
    return exploded.value_counts().head(top_n)


def duration_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize duration stats separately for movies (minutes) and TV shows (seasons)."""
    rows = []
    for content_type, unit in [("Movie", "minutes"), ("TV Show", "seasons")]:
        subset = df[(df["type"] == content_type) & (df["duration_unit"] == unit)]
        if subset.empty:
            continue
        values = subset["duration_value"].dropna()
        rows.append(
            {
                "type": content_type,
                "unit": unit,
                "count": len(values),
                "mean": round(values.mean(), 1),
                "median": round(values.median(), 1),
                "min": values.min(),
                "max": values.max(),
            }
        )
    return pd.DataFrame(rows)
