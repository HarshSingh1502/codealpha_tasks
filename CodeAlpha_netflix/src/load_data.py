"""Data loading and preprocessing for the Netflix titles dataset."""

import re
from pathlib import Path

import pandas as pd

from src.config import NETFLIX_DATASET_FILE, PROCESSED_DATA_DIR, RAW_DATA_DIR


def _parse_duration(value: str | float) -> tuple[float | None, str | None]:
    """Extract numeric duration and unit (minutes or seasons) from the raw string."""
    if pd.isna(value):
        return None, None
    text = str(value).strip()
    if "min" in text:
        match = re.search(r"(\d+)", text)
        return (float(match.group(1)) if match else None), "minutes"
    if "Season" in text:
        match = re.search(r"(\d+)", text)
        return (float(match.group(1)) if match else None), "seasons"
    return None, None


def preprocess_netflix(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the raw Netflix titles dataset."""
    out = df.copy()
    out["date_added"] = pd.to_datetime(out["date_added"], errors="coerce")
    parsed = out["duration"].apply(_parse_duration)
    out["duration_value"] = parsed.apply(lambda x: x[0])
    out["duration_unit"] = parsed.apply(lambda x: x[1])
    out["primary_country"] = out["country"].str.split(",").str[0].str.strip()
    out["primary_genre"] = out["listed_in"].str.split(",").str[0].str.strip()
    return out


def load_netflix_data(filename: str = NETFLIX_DATASET_FILE) -> pd.DataFrame:
    """Load and preprocess the Netflix titles dataset."""
    path = RAW_DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run `python scripts/download_netflix_data.py` first."
        )
    df = pd.read_csv(path)
    return preprocess_netflix(df)


def save_processed(df: pd.DataFrame, filename: str = "netflix_cleaned.csv") -> Path:
    """Save a processed dataframe to the processed data directory."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = PROCESSED_DATA_DIR / filename
    df.to_csv(path, index=False)
    return path
