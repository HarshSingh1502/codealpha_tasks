"""Visualization helpers for EDA reports."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.config import FIGURES_DIR

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.0)
plt.rcParams["figure.dpi"] = 120


def _save_fig(name: str) -> Path:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / name
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    return path


def plot_missing_values(df: pd.DataFrame, filename: str = "01_missing_values.png") -> Path:
    """Bar chart of missing value percentages."""
    missing_pct = df.isnull().mean().sort_values(ascending=False) * 100
    missing_pct = missing_pct[missing_pct > 0]
    if missing_pct.empty:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No missing values", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    fig, ax = plt.subplots(figsize=(10, max(4, len(missing_pct) * 0.4)))
    missing_pct.plot(kind="barh", ax=ax, color="#4C72B0")
    ax.set_xlabel("Missing (%)")
    ax.set_title("Missing Values by Column")
    return _save_fig(filename)


def plot_distributions(df: pd.DataFrame, filename: str = "02_distributions.png") -> Path:
    """Histograms for numeric columns."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "No numeric columns", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    n = len(numeric_cols)
    cols = 2
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
    axes = axes.flatten() if n > 1 else [axes]

    for ax, col in zip(axes, numeric_cols):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color="#55A868")
        ax.set_title(f"Distribution: {col}")

    for ax in axes[len(numeric_cols) :]:
        ax.axis("off")

    fig.suptitle("Numeric Feature Distributions", y=1.02, fontsize=14)
    return _save_fig(filename)


def plot_correlation_heatmap(df: pd.DataFrame, filename: str = "03_correlation_heatmap.png") -> Path:
    """Correlation heatmap for numeric features."""
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Need 2+ numeric columns", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    fig, ax = plt.subplots(figsize=(10, 8))
    corr = numeric.corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax, square=True)
    ax.set_title("Correlation Heatmap")
    return _save_fig(filename)


def plot_categorical_counts(
    df: pd.DataFrame,
    column: str,
    filename: str | None = None,
    top_n: int = 10,
) -> Path:
    """Bar chart of top categories for a column."""
    fname = filename or f"04_{column}_counts.png"
    counts = df[column].value_counts().head(top_n)

    fig, ax = plt.subplots(figsize=(10, max(4, len(counts) * 0.35)))
    counts.plot(kind="barh", ax=ax, color="#C44E52")
    ax.set_xlabel("Count")
    ax.set_title(f"Top {top_n}: {column}")
    return _save_fig(fname)


def plot_counts_over_time(
    df: pd.DataFrame,
    date_col: str = "date_added",
    filename: str = "05_titles_added_over_time.png",
) -> Path:
    """Line chart of title counts aggregated over time."""
    if date_col not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Date column missing", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    monthly = df.dropna(subset=[date_col]).groupby(pd.Grouper(key=date_col, freq="ME")).size()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly.index, monthly.values, color="#E50914", linewidth=1.8)
    ax.fill_between(monthly.index, monthly.values, alpha=0.12, color="#E50914")
    ax.set_xlabel("Date")
    ax.set_ylabel("Titles Added")
    ax.set_title("Netflix Titles Added Over Time")
    return _save_fig(filename)


def plot_type_split(df: pd.DataFrame, filename: str = "05b_type_split.png") -> Path:
    """Pie chart of Movie vs TV Show distribution."""
    if "type" not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Type column missing", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    counts = df["type"].value_counts()
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", colors=["#E50914", "#221F1F"], startangle=90)
    ax.set_title("Movies vs TV Shows")
    return _save_fig(filename)


def plot_boxplots_by_category(
    df: pd.DataFrame,
    numeric_col: str,
    category_col: str,
    filename: str | None = None,
) -> Path:
    """Boxplot of a numeric variable grouped by category."""
    fname = filename or f"06_{numeric_col}_by_{category_col}.png"
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(
        data=df,
        x=category_col,
        y=numeric_col,
        hue=category_col,
        ax=ax,
        palette="pastel",
        legend=False,
    )
    ax.set_title(f"{numeric_col} by {category_col}")
    plt.xticks(rotation=30, ha="right")
    return _save_fig(fname)


def plot_genre_breakdown(
    genre_counts: pd.Series,
    filename: str = "07_genre_breakdown.png",
    top_n: int = 15,
) -> Path:
    """Horizontal bar chart of top genres."""
    counts = genre_counts.head(top_n)
    fig, ax = plt.subplots(figsize=(11, max(5, len(counts) * 0.35)))
    counts.sort_values().plot(kind="barh", ax=ax, color="#B81D24")
    ax.set_xlabel("Number of Titles")
    ax.set_title(f"Top {top_n} Netflix Genres")
    return _save_fig(filename)


def plot_duration_analysis(df: pd.DataFrame, filename: str = "08_duration_analysis.png") -> Path:
    """Compare movie runtimes (minutes) vs TV show season counts."""
    movies = df[(df["type"] == "Movie") & (df["duration_unit"] == "minutes")]["duration_value"].dropna()
    shows = df[(df["type"] == "TV Show") & (df["duration_unit"] == "seasons")]["duration_value"].dropna()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    if not movies.empty:
        sns.histplot(movies, kde=True, ax=axes[0], color="#E50914", bins=30)
        axes[0].axvline(movies.median(), color="black", linestyle="--", label=f"Median: {movies.median():.0f} min")
        axes[0].legend()
    axes[0].set_title("Movie Runtime (minutes)")
    axes[0].set_xlabel("Minutes")

    if not shows.empty:
        sns.histplot(shows, kde=True, ax=axes[1], color="#221F1F", bins=range(1, int(shows.max()) + 2))
        axes[1].axvline(shows.median(), color="black", linestyle="--", label=f"Median: {shows.median():.0f} seasons")
        axes[1].legend()
    axes[1].set_title("TV Show Seasons")
    axes[1].set_xlabel("Seasons")

    fig.suptitle("Duration Analysis: Movies vs TV Shows", y=1.02, fontsize=14)
    return _save_fig(filename)


def plot_description_wordcloud(df: pd.DataFrame, filename: str = "09_description_wordcloud.png") -> Path:
    """Word cloud from title descriptions."""
    from wordcloud import STOPWORDS, WordCloud

    if "description" not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, "Description column missing", ha="center", va="center", fontsize=14)
        ax.axis("off")
        return _save_fig(filename)

    text = " ".join(df["description"].dropna().astype(str))
    extra_stop = {"one", "two", "new", "find", "life", "world", "year", "years", "way", "man", "woman"}
    stopwords = set(STOPWORDS) | extra_stop

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="#141414",
        colormap="Reds",
        stopwords=stopwords,
        max_words=150,
        collocations=False,
    ).generate(text)

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title("Most Common Words in Netflix Descriptions", color="white", pad=12)
    fig.patch.set_facecolor("#141414")
    return _save_fig(filename)
