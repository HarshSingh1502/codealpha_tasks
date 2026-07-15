# 🌐 Web Scraper

A Python-based web scraping application that extracts product and webpage information from a user-provided URL. The project uses **BeautifulSoup** and **Requests** to collect structured data from websites and export it into CSV format for further analysis.

## Features

- Modular Python project structure (`src/`)
- Accepts website URL as user input
- Extracts product information from webpages
- Cleans and organizes scraped data
- Exports data to CSV format
- Jupyter Notebook for testing and experimentation
- Automatic JSON summary report generation
- Easy-to-extend scraping functions

## Project Structure

```
web-scraper/
├── data/
│   ├── raw/                     # Raw HTML files (optional)
│   └── processed/               # Generated CSV files
├── docs/                        # Project documentation
├── notebooks/
│   └── 01_web_scraping.ipynb
├── reports/
│   ├── output/                  # Scraped datasets
│   └── scraping_summary.json    # Generated summary
├── scripts/
│   └── sample_scraper.py
├── src/
│   ├── config.py                # Project configuration
│   ├── scraper.py               # Main scraping functions
│   ├── parser.py                # HTML parsing utilities
│   ├── exporter.py              # Export CSV/JSON
│   └── utils.py                 # Helper functions
├── main.py                      # Main application
├── requirements.txt
└── README.md
```

## Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/web-scraper.git

# Navigate to project folder
cd web-scraper

# Install dependencies
python -m pip install -r requirements.txt

# Run the scraper
python main.py
```

## Jupyter Notebook

```bash
python -m jupyter notebook notebooks/01_web_scraping.ipynb
```

## Modules

| Module | Description |
|---------|-------------|
| `src/config.py` | Stores project paths and configuration settings |
| `src/scraper.py` | Sends HTTP requests and retrieves webpage content |
| `src/parser.py` | Extracts required information from HTML using BeautifulSoup |
| `src/exporter.py` | Saves scraped data into CSV and JSON formats |
| `src/utils.py` | Helper functions for cleaning and formatting data |
| `main.py` | Executes the complete web scraping workflow |

## Output

Running

```bash
python main.py
```

generates:

- `reports/output/` — Scraped CSV dataset
- `reports/scraping_summary.json` — Summary of scraping results
- `data/processed/` — Cleaned and processed data

## Sample Output

| Product Name | Price | Rating | Product Link |
|--------------|-------|--------|--------------|
| Product A | ₹999 | ⭐ 4.5 | https://example.com |
| Product B | ₹1499 | ⭐ 4.3 | https://example.com |

## Upload to GitHub

```bash
cd web-scraper
git init
git add .
git commit -m "Initial commit: Web Scraper project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/web-scraper.git
git push -u origin main
```

Create a new repository on GitHub, then replace `YOUR_USERNAME` with your GitHub username.

## Technologies Used

- Python 3.10+
- BeautifulSoup4
- Requests
- Pandas
- CSV
- JSON
- Jupyter Notebook

## Future Enhancements

- Support multiple websites
- Selenium integration for JavaScript-based websites
- Proxy and User-Agent rotation
- Multi-threaded scraping
- Export to Excel and SQL databases
- GUI using Tkinter or PyQt
- Schedule automated scraping tasks

## Disclaimer

This project is developed **for educational purposes only**. Always comply with the target website's Terms of Service and `robots.txt` file before scraping. Do not overload websites with excessive requests.

## License

MIT License — see `LICENSE`.