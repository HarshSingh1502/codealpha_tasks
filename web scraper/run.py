#!/usr/bin/env python3
"""
Universal web scraper — pass any URL and get structured data.

Examples:
  python run.py --url "https://books.toscrape.com"
  python run.py --url "https://www.amazon.com/s?k=phones"
  python run.py --url "https://www.ebay.com/sch/i.html?_nkw=phones" --max-pages 2
  python run.py --url "https://example.com" --preset generic
"""

from __future__ import annotations

import argparse
import json
import sys

from presets import available_preset_names
from scraper import save_result, scrape_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape product listings and structured data from any website URL.",
    )
    parser.add_argument(
        "--url",
        "-u",
        required=True,
        help="Page URL to scrape (search results, category page, etc.)",
    )
    parser.add_argument(
        "--preset",
        "-p",
        choices=available_preset_names(),
        help="Force a site preset instead of auto-detecting from the URL",
    )
    parser.add_argument(
        "--max-pages",
        "-m",
        type=int,
        default=None,
        help="Maximum pages to follow via pagination (default: 5)",
    )
    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Always use browser-based stealth fetching (needed for Amazon, eBay, etc.)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output",
        help="Output directory for JSON and CSV files",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=5,
        help="Number of records to print as a preview (default: 5, 0 to skip)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        result = scrape_url(
            args.url,
            preset_name=args.preset,
            max_pages=args.max_pages,
            force_stealth=args.stealth,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if "playwright" in str(exc).lower() or "browser" in str(exc).lower():
            print(
                "\nTip: Run `scrapling install` first for browser-based sites like Amazon.",
                file=sys.stderr,
            )
        return 1

    json_path, csv_path = save_result(result, args.output)

    print(f"\nDone — scraped {len(result.records)} items from {result.pages_scraped} page(s)")
    print(f"Preset: {result.preset}")
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")

    if args.preview and result.records:
        print(f"\nPreview ({min(args.preview, len(result.records))} items):")
        for item in result.records[: args.preview]:
            print(json.dumps(item, ensure_ascii=False))

    if not result.records:
        print(
            "\nNo items found. Try --stealth for JavaScript-heavy sites, "
            "or check if the URL is a listing/search page.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
