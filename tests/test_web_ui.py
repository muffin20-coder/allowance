from __future__ import annotations

import contextlib
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Iterator

import pytest


@contextlib.contextmanager
def serve_web(root: Path) -> Iterator[str]:
    """Run a lightweight HTTP server for the static web UI."""

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, directory=str(root), **kwargs)

        def log_message(self, *args, **kwargs) -> None:  # type: ignore[override]
            # Silence request logging during tests for cleaner output.
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as httpd:
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{port}/index.html"
        finally:
            httpd.shutdown()
            thread.join()


@pytest.fixture(scope="session")
def playwright_page():
    sync_api = pytest.importorskip(
        "playwright.sync_api", reason="Playwright is required for web UI tests."
    )
    with sync_api.sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def test_web_ui_memo_persists_and_totals_update(playwright_page) -> None:
    web_root = Path(__file__).resolve().parents[1] / "allowance" / "web"
    with serve_web(web_root) as url:
        page = playwright_page
        page.goto(url)
        # Start from a clean state so the seeded data is reproducible.
        page.evaluate("localStorage.clear()")
        page.reload()

        unique_desc = "테스트 거래 항목"
        memo_text = "테스트 메모"
        page.select_option("#tx-type", "expense")
        page.fill("#tx-desc", unique_desc)
        page.fill("#tx-amt", "2000")
        page.fill("#tx-date", "2024-05-03")
        page.click('button[type="submit"]')

        # Edit the memo cell within the printable table.
        row = page.locator("tbody tr").filter(has_text=unique_desc).first
        row.wait_for()
        memo_cell = row.locator("td").nth(5)
        memo_cell.click()
        page.keyboard.type(memo_text)
        page.keyboard.press("Tab")

        page.reload()

        # Memo should persist after reload.
        persisted_row = page.locator("tbody tr").filter(has_text=unique_desc).first
        memo_value = persisted_row.locator("td").nth(5).inner_text().strip()
        assert memo_value == memo_text

        # Footer totals should reflect one income (₩10,000) and two expenses (₩4,500 + ₩2,000).
        footer_cells = page.locator("tfoot td")
        assert footer_cells.nth(2).inner_text().strip() == "₩10,000"
        assert footer_cells.nth(3).inner_text().strip() == "₩6,500"
        assert footer_cells.nth(4).inner_text().strip() == "₩3,500"
