"""URL-driven web scraper with site presets and generic fallback."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

import config
from export import export_csv, export_json
from extractors import extract_items, next_page_url
from page_fetcher import fetch_page
from presets import SitePreset, detect_preset


@dataclass
class ScrapeResult:
    url: str
    preset: str
    records: list[dict[str, Any]]
    pages_scraped: int


def scrape_url(
    url: str,
    *,
    preset_name: str | None = None,
    max_pages: int | None = None,
    force_stealth: bool = False,
) -> ScrapeResult:
    preset = detect_preset(url, preset_name)
    limit = max_pages if max_pages is not None else config.MAX_PAGES
    all_records: list[dict[str, Any]] = []
    current_url = url
    pages_scraped = 0

    while current_url and pages_scraped < limit:
        print(f"[{preset.name}] Fetching page {pages_scraped + 1}: {current_url}")
        page = fetch_page(
            current_url,
            use_stealth=force_stealth or preset.use_stealth,
            wait_selector=preset.wait_selector,
        )
        base_url = f"{urlparse(current_url).scheme}://{urlparse(current_url).netloc}"
        records = extract_items(page, preset, base_url)
        print(f"  Found {len(records)} items")
        all_records.extend(records)
        pages_scraped += 1

        if pages_scraped >= limit:
            break

        current_url = next_page_url(page, preset, current_url)
        if current_url:
            time.sleep(config.REQUEST_DELAY)

    # Global dedupe across pages
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for record in all_records:
        key = str(record.get("product_url") or record.get("asin") or record.get("title"))
        if key not in seen:
            seen.add(key)
            unique.append(record)

    return ScrapeResult(
        url=url,
        preset=preset.name,
        records=unique,
        pages_scraped=pages_scraped,
    )


def save_result(result: ScrapeResult, output_dir: str | None = None) -> tuple[str, str]:
    out = __import__("pathlib").Path(output_dir or config.OUTPUT_DIR)
    slug = urlparse(result.url).netloc.replace(".", "_") or "scrape"
    json_path = out / f"{slug}_{result.preset}.json"
    csv_path = out / f"{slug}_{result.preset}.csv"
    export_json(result.records, json_path)
    export_csv(result.records, csv_path)
    return str(json_path), str(csv_path)
