# Web Scraper

Universal web scraper with a browser UI. Paste a product listing URL and get structured data (title, price, rating, images, links).

## Setup

```bash
pip install -r requirements.txt
scrapling install   # required for Amazon, eBay, and other protected sites
```

## Run the web app

```bash
python app.py
```

Open http://127.0.0.1:5000

Results can be downloaded as **JSON** or **Excel (.xlsx)** from the web UI.

## Run from the command line

```bash
python run.py --url "https://books.toscrape.com"
python run.py --url "https://www.amazon.com/s?k=phones" --stealth
```

## Supported sites

- Amazon (search/category pages)
- eBay
- books.toscrape.com
- Generic fallback for other e-commerce sites
