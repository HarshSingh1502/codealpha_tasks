"""Site-specific scraping presets keyed by hostname patterns."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import urljoin, urlparse

from scrapling.parser import Selector


@dataclass
class SitePreset:
    name: str
    item_selector: str
    fields: dict[str, str | Callable[[Selector, str], str | None]]
    next_page_selector: str | None = None
    wait_selector: str | None = None
    use_stealth: bool = False


def _text(el: Selector | None) -> str | None:
    if not el:
        return None
    value = el.get_all_text(strip=True)
    return str(value).strip() if value else None


def _attr(el: Selector | None, name: str) -> str | None:
    if not el:
        return None
    return el.attrib.get(name)


def _first_price(text: str | None) -> str | None:
    if not text:
        return None
    match = re.search(r"[\$£€₹]\s*[\d,]+(?:\.\d{2})?|[\d,]+(?:\.\d{2})?\s*[\$£€₹]", text)
    return match.group(0).strip() if match else None


def _amazon_title(item: Selector, base_url: str) -> str | None:
    for sel in ("h2 a span", "h2 span", ".a-text-normal"):
        title = _text(item.css(sel).first)
        if title:
            return title
    return None


def _amazon_link(item: Selector, base_url: str) -> str | None:
    for sel in ("h2 a", "a.a-link-normal.s-no-outline", "a.a-link-normal"):
        href = _attr(item.css(sel).first, "href")
        if href:
            return urljoin(base_url, href)
    asin = _amazon_asin(item, base_url)
    if asin:
        return f"https://www.amazon.com/dp/{asin}"
    return None


def _amazon_price(item: Selector, base_url: str) -> str | None:
    for sel in (".a-price .a-offscreen", ".a-price-whole", ".a-color-price"):
        price = _text(item.css(sel).first)
        if price:
            return price
    return _first_price(item.get())


def _amazon_rating(item: Selector, base_url: str) -> str | None:
    return _text(item.css(".a-icon-alt").first)


def _amazon_image(item: Selector, base_url: str) -> str | None:
    return _attr(item.css("img.s-image").first, "src") or _attr(item.css("img").first, "src")


def _amazon_asin(item: Selector, base_url: str) -> str | None:
    return item.attrib.get("data-asin") or _attr(item, "data-asin")


def _books_title(item: Selector, base_url: str) -> str | None:
    return _attr(item.css("h3 a").first, "title") or _text(item.css("h3 a").first)


def _books_link(item: Selector, base_url: str) -> str | None:
    href = _attr(item.css("h3 a").first, "href")
    return urljoin(base_url, href) if href else None


def _books_price(item: Selector, base_url: str) -> str | None:
    return _text(item.css("p.price_color").first)


def _books_rating(item: Selector, base_url: str) -> str | None:
    star = item.css("p.star-rating")
    if not star:
        return None
    classes = star[0].attrib.get("class", "").split()
    for cls in classes:
        if cls != "star-rating":
            return cls
    return None


def _books_availability(item: Selector, base_url: str) -> str | None:
    return _text(item.css("p.instock.availability").first)


def _generic_title(item: Selector, base_url: str) -> str | None:
    for sel in ("h1 a", "h2 a", "h3 a", "h4 a", "h1", "h2", "h3", ".title", "[class*='title'] a"):
        title = _text(item.css(sel).first) or _attr(item.css(sel).first, "title")
        if title and len(title) > 2:
            return title
    link = item.css("a[href]").first
    return _text(link) or _attr(link, "title")


def _generic_link(item: Selector, base_url: str) -> str | None:
    for sel in ("h1 a", "h2 a", "h3 a", "a[href]"):
        href = _attr(item.css(sel).first, "href")
        if href and not href.startswith(("#", "javascript:")):
            return urljoin(base_url, href)
    return None


def _generic_price(item: Selector, base_url: str) -> str | None:
    for sel in (
        ".price",
        "[class*='price']",
        "[data-price]",
        "span.a-price",
        ".a-color-price",
    ):
        price = _text(item.css(sel).first) or _attr(item.css(sel).first, "data-price")
        if price:
            found = _first_price(price)
            if found:
                return found
    return _first_price(item.get())


def _generic_image(item: Selector, base_url: str) -> str | None:
    for sel in ("img[src]", "img[data-src]", "picture img"):
        img = item.css(sel).first
        src = _attr(img, "src") or _attr(img, "data-src")
        if src and not src.startswith("data:"):
            return urljoin(base_url, src)
    return None


PRESETS: list[tuple[re.Pattern[str], SitePreset]] = [
    (
        re.compile(r"(^|\.)amazon\.", re.I),
        SitePreset(
            name="amazon",
            item_selector='[data-component-type="s-search-result"], div.s-result-item[data-asin]:not([data-asin=""])',
            fields={
                "title": _amazon_title,
                "price": _amazon_price,
                "rating": _amazon_rating,
                "image_url": _amazon_image,
                "product_url": _amazon_link,
                "asin": _amazon_asin,
            },
            next_page_selector="a.s-pagination-next",
            wait_selector='[data-component-type="s-search-result"]',
            use_stealth=True,
        ),
    ),
    (
        re.compile(r"(^|\.)ebay\.", re.I),
        SitePreset(
            name="ebay",
            item_selector="li.s-item",
            fields={
                "title": lambda item, base: _text(item.css(".s-item__title").first),
                "price": lambda item, base: _text(item.css(".s-item__price").first),
                "product_url": lambda item, base: urljoin(
                    base, _attr(item.css(".s-item__link").first, "href") or ""
                )
                or None,
                "image_url": lambda item, base: _attr(item.css(".s-item__image-img").first, "src"),
            },
            next_page_selector="a.pagination__next",
            use_stealth=True,
        ),
    ),
    (
        re.compile(r"books\.toscrape\.com", re.I),
        SitePreset(
            name="books_toscrape",
            item_selector="article.product_pod",
            fields={
                "title": _books_title,
                "price": _books_price,
                "rating": _books_rating,
                "availability": _books_availability,
                "product_url": _books_link,
            },
            next_page_selector="li.next a",
        ),
    ),
]

GENERIC_PRESET = SitePreset(
    name="generic",
    item_selector=(
        "article, li.product, div.product, [class*='product-card'], "
        "[class*='product-item'], [data-product], [itemtype*='Product']"
    ),
    fields={
        "title": _generic_title,
        "price": _generic_price,
        "product_url": _generic_link,
        "image_url": _generic_image,
    },
    next_page_selector="a[rel='next'], li.next a, a.next, .pagination a.next",
)


def detect_preset(url: str, forced: str | None = None) -> SitePreset:
    if forced:
        for _, preset in PRESETS:
            if preset.name == forced:
                return preset
        if forced == "generic":
            return GENERIC_PRESET
        raise ValueError(f"Unknown preset: {forced}. Available: {available_preset_names()}")

    host = urlparse(url).netloc
    for pattern, preset in PRESETS:
        if pattern.search(host):
            return preset
    return GENERIC_PRESET


def available_preset_names() -> list[str]:
    return [preset.name for _, preset in PRESETS] + ["generic"]
