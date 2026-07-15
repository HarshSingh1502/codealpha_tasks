# Netflix EDA

Exploratory Data Analysis of the public [Netflix titles dataset](https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-20) — 7,800+ movies and TV shows with ratings, genres, countries, and catalog growth insights.

## Features

- Modular Python package (`src/`)
- Automated EDA pipeline with 12 visualizations
- Genre breakdown, duration analysis, and description word cloud
- Jupyter notebook for interactive exploration
- JSON summary report output

## Project Structure

```
netflix-eda/
├── data/
│   ├── raw/                  # netflix_titles.csv
│   └── processed/            # netflix_cleaned.csv (generated)
├── docs/                     # Documentation assets
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
├── reports/
│   ├── figures/              # Generated charts (gitignored)
│   └── eda_summary.json      # Generated summary (gitignored)
├── scripts/
│   └── download_netflix_data.py
├── src/
│   ├── config.py             # Paths and constants
│   ├── load_data.py          # Load & preprocess data
│   ├── eda_utils.py          # Analysis helpers
│   └── visualizations.py     # Plotting functions
├── run_eda.py                  # Main pipeline entry point
├── requirements.txt
└── README.md
```

## Setup

```bash
# Clone or download this repo, then:
python -m pip install -r requirements.txt

# Download dataset (skip if data/raw/netflix_titles.csv already exists)
python scripts/download_netflix_data.py

# Run full analysis
python run_eda.py
```

### Jupyter Notebook

```bash
python -m jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

## Modules

| Module | Description |
|--------|-------------|
| `src/config.py` | Project paths, dataset URL, filenames |
| `src/load_data.py` | CSV loading, date/duration parsing, feature engineering |
| `src/eda_utils.py` | Overview, summaries, outliers, genres, countries |
| `src/visualizations.py` | All chart generation functions |
| `run_eda.py` | Orchestrates the full pipeline |

## Output

Running `python run_eda.py` generates:

- `reports/figures/` — 12 PNG charts
- `reports/eda_summary.json` — structured analysis summary
- `data/processed/netflix_cleaned.csv` — cleaned dataset

## Upload to GitHub

```bash
cd netflix-eda
git init
git add .
git commit -m "Initial commit: Netflix EDA project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/netflix-eda.git
git push -u origin main
```

Create a new repository on [GitHub](https://github.com/new) first, then replace `YOUR_USERNAME` with your GitHub username.

## Dataset Source

Netflix titles data from [TidyTuesday (2021-04-20)](https://github.com/rfordatascience/tidytuesday/tree/master/data/2021/2021-04-20).

## Requirements

- Python 3.10+
- pandas, numpy, matplotlib, seaborn, scipy, wordcloud, jupyter

## License

MIT License — see [LICENSE](LICENSE).
