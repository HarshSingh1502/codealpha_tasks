"""Web UI for the universal scraper."""

from __future__ import annotations

from io import BytesIO

from flask import Flask, jsonify, render_template, request, send_file

from export import export_excel_bytes
from presets import available_preset_names
from scraper import scrape_url

app = Flask(__name__)


@app.get("/")
def index():
    return render_template(
        "index.html",
        presets=available_preset_names(),
    )


@app.post("/api/scrape")
def api_scrape():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL."}), 400
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    preset = data.get("preset") or None
    if preset == "auto":
        preset = None

    max_pages = data.get("max_pages", 1)
    try:
        max_pages = max(1, min(int(max_pages), 10))
    except (TypeError, ValueError):
        max_pages = 1

    force_stealth = bool(data.get("stealth"))

    try:
        result = scrape_url(
            url,
            preset_name=preset,
            max_pages=max_pages,
            force_stealth=force_stealth,
        )
    except Exception as exc:
        message = str(exc)
        if "playwright" in message.lower() or "browser" in message.lower():
            message += " Run `scrapling install` in your terminal first."
        return jsonify({"error": message}), 500

    return jsonify(
        {
            "url": result.url,
            "preset": result.preset,
            "pages_scraped": result.pages_scraped,
            "count": len(result.records),
            "items": result.records,
        }
    )


@app.post("/api/export/excel")
def api_export_excel():
    data = request.get_json(silent=True) or {}
    items = data.get("items")
    if not isinstance(items, list):
        return jsonify({"error": "No items to export."}), 400

    filename = (data.get("filename") or "scrape_results").strip()
    if not filename.endswith(".xlsx"):
        filename = f"{filename}.xlsx"

    excel_data = export_excel_bytes(items)
    return send_file(
        BytesIO(excel_data),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=filename,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
