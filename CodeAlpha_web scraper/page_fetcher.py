"""Fetch pages with automatic stealth fallback for protected sites."""

from __future__ import annotations

from scrapling.engines.toolbelt.custom import Response
from scrapling.fetchers import Fetcher, StealthyFetcher


def fetch_page(
    url: str,
    *,
    use_stealth: bool = False,
    wait_selector: str | None = None,
    timeout: int = 60_000,
) -> Response:
    """Fetch a URL. Uses a real browser when stealth is requested or HTTP fails."""
    if not use_stealth:
        try:
            response = Fetcher.get(url, timeout=30)
            if response.status >= 400:
                raise RuntimeError(f"HTTP {response.status}")
            return response
        except Exception:
            use_stealth = True

    kwargs: dict = {
        "headless": True,
        "network_idle": True,
        "timeout": timeout,
        "disable_resources": True,
    }
    if wait_selector:
        kwargs["wait_selector"] = wait_selector
        kwargs["wait_selector_state"] = "attached"

    return StealthyFetcher.fetch(url, **kwargs)
