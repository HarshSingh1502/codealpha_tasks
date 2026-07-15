"""Netflix EDA — exploratory data analysis package."""

from src.eda_utils import (
    categorical_summary,
    correlation_matrix,
    dataset_overview,
    duration_summary,
    numeric_summary,
    outlier_summary,
    top_countries,
    top_genres,
)
from src.load_data import load_netflix_data, preprocess_netflix, save_processed

__all__ = [
    "categorical_summary",
    "correlation_matrix",
    "dataset_overview",
    "duration_summary",
    "load_netflix_data",
    "numeric_summary",
    "outlier_summary",
    "preprocess_netflix",
    "save_processed",
    "top_countries",
    "top_genres",
]
