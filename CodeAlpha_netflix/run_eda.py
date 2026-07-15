"""Run the full EDA pipeline and save reports."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import REPORTS_DIR  # noqa: E402
from src.eda_utils import (  # noqa: E402
    categorical_summary,
    correlation_matrix,
    dataset_overview,
    duration_summary,
    numeric_summary,
    outlier_summary,
    top_countries,
    top_genres,
)
from src.load_data import load_netflix_data, save_processed  # noqa: E402
from src.visualizations import (  # noqa: E402
    plot_boxplots_by_category,
    plot_categorical_counts,
    plot_correlation_heatmap,
    plot_counts_over_time,
    plot_description_wordcloud,
    plot_distributions,
    plot_duration_analysis,
    plot_genre_breakdown,
    plot_missing_values,
    plot_type_split,
)


def run_eda() -> None:
    print("=" * 60)
    print("  Netflix EDA — Titles Analysis")
    print("=" * 60)

    df = load_netflix_data()
    overview = dataset_overview(df)

    print(f"\nDataset shape: {overview['shape'][0]:,} rows x {overview['shape'][1]} columns")
    print(f"Memory usage:  {overview['memory_mb']} MB")
    print(f"Duplicate rows: {overview['duplicate_rows']}")

    missing = {k: v for k, v in overview["missing_pct"].items() if v > 0}
    if missing:
        print("\nMissing values (%):")
        for col, pct in missing.items():
            print(f"  {col}: {pct}%")
    else:
        print("\nNo missing values detected.")

    print("\n--- Numeric Summary ---")
    print(numeric_summary(df).to_string())

    print("\n--- Outlier Summary (IQR) ---")
    print(outlier_summary(df).to_string(index=False))

    print("\n--- Correlation Matrix ---")
    corr = correlation_matrix(df)
    if not corr.empty:
        print(corr.to_string())

    cat_summary = categorical_summary(df)
    if cat_summary:
        print("\n--- Categorical Distributions ---")
        for col, counts in cat_summary.items():
            print(f"\n{col}:")
            print(counts.head(5).to_string())

    countries = top_countries(df)
    if not countries.empty:
        print("\n--- Top Countries ---")
        print(countries.to_string())

    genres = top_genres(df)
    if not genres.empty:
        print("\n--- Top Genres ---")
        print(genres.to_string())

    dur = duration_summary(df)
    if not dur.empty:
        print("\n--- Duration Summary ---")
        print(dur.to_string(index=False))

    print("\nGenerating figures...")
    figures = [
        plot_missing_values(df),
        plot_distributions(df),
        plot_correlation_heatmap(df),
        plot_categorical_counts(df, "type", filename="04_type_counts.png"),
        plot_categorical_counts(df, "rating", filename="04_rating_counts.png"),
        plot_categorical_counts(df, "primary_country", filename="04_country_counts.png", top_n=12),
        plot_counts_over_time(df),
        plot_type_split(df),
        plot_boxplots_by_category(df, "release_year", "type", filename="06_release_year_by_type.png"),
        plot_genre_breakdown(genres),
        plot_duration_analysis(df),
        plot_description_wordcloud(df),
    ]
    for fig_path in figures:
        print(f"  Saved: {fig_path.relative_to(PROJECT_ROOT)}")

    cleaned = df.drop_duplicates(subset=["show_id"]).copy()
    for col in ["director", "cast", "country"]:
        cleaned[col] = cleaned[col].fillna("Unknown")
    processed_path = save_processed(cleaned)
    print(f"\nProcessed data saved: {processed_path.relative_to(PROJECT_ROOT)}")

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = REPORTS_DIR / "eda_summary.json"
    report = {
        "overview": overview,
        "numeric_summary": numeric_summary(df).to_dict(),
        "outlier_summary": outlier_summary(df).to_dict(orient="records"),
        "correlation": corr.to_dict() if not corr.empty else {},
        "top_countries": countries.to_dict(),
        "top_genres": genres.to_dict(),
        "duration_summary": dur.to_dict(orient="records"),
    }
    summary_path.write_text(json.dumps(report, indent=2, default=str))
    print(f"Summary report:   {summary_path.relative_to(PROJECT_ROOT)}")

    print("\nEDA complete.")


if __name__ == "__main__":
    run_eda()
