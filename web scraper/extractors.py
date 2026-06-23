"""Extract structured records from fetched pages."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin

from scrapling.engines.toolbelt.custom import Response

from presets import GENERIC_PRESET, SitePreset


def _clean_record(record: dict[str, Any]) -> dict[str, Any] | None:
    cleaned = {k: v for k, v in record.items() if v not in (None, "", [])}
    if not cleaned.get("title") and not cleaned.get("product_url"):
        return None
    return cleaned


def extract_items(page: Response, preset: SitePreset, base_url: str) -> list[dict[str, Any]]:
    items = page.css(preset.item_selector)
    records: list[dict[str, Any]] = []

    for item in items:
        record: dict[str, Any] = {"source": preset.name}
        for field_name, extractor in preset.fields.items():
            if callable(extractor):
                record[field_name] = extractor(item, base_url)
            else:
                el = item.css(extractor).first
                record[field_name] = el.get().strip() if el else None
        cleaned = _clean_record(record)
        if cleaned:
            records.append(cleaned)

    if records:
        return _dedupe_records(records)

    if preset.name != "generic":
        return extract_items(page, GENERIC_PRESET, base_url)

    return _heuristic_extract(page, base_url)


def _dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for record in records:
        key = record.get("product_url") or record.get("asin") or record.get("title")
        if not key or key not in seen:
            if key:
                seen.add(str(key))
            unique.append(record)
    return unique


def _heuristic_extract(page: Response, base_url: str) -> list[dict[str, Any]]:
    """Last-resort extraction for unknown page layouts."""
    records: list[dict[str, Any]] = []
    price_pattern = re.compile(r"[\$£€₹]\s*[\d,]+(?:\.\d{2})?")

    for block in page.css("article, li, div[class], section"):
        text = str(block.get_all_text(strip=True) or "")
        if len(text) < 20 or len(text) > 4000:
            continue

        title_el = block.css("h1, h2, h3, h4, a[title], a").first
        title = str(title_el.get_all_text(strip=True)) if title_el else None
        if not title or len(title) < 3:
            continue

        price_match = price_pattern.search(text)
        link_el = block.css("a[href]").first
        href = link_el.attrib.get("href") if link_el else None
        product_url = urljoin(base_url, href) if href and not href.startswith("#") else None
        img_el = block.css("img").first
        image_url = None
        if img_el:
            image_url = img_el.attrib.get("src") or img_el.attrib.get("data-src")

        record = _clean_record(
            {
                "source": "heuristic",
                "title": title,
                "price": price_match.group(0) if price_match else None,
                "product_url": product_url,
                "image_url": image_url,
            }
        )
        if record:
            records.append(record)

    return _dedupe_records(records)[:50]


def next_page_url(page: Response, preset: SitePreset, current_url: str) -> str | None:
    if not preset.next_page_selector:
        return None
    link = page.css(preset.next_page_selector).first
    if not link:
        return None
    href = link.attrib.get("href")
    return urljoin(current_url, href) if href else None
