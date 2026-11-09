from __future__ import annotations

import subprocess
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import expect


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


@pytest.fixture(scope="module")
def vite_url():
    process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", "4178", "--strictPort"],
        cwd=FRONTEND,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    url = "http://127.0.0.1:4178/"
    try:
        for _ in range(80):
            if process.poll() is not None:
                raise RuntimeError("Vite exited before becoming ready.")
            try:
                with urllib.request.urlopen(url, timeout=1):
                    break
            except Exception:
                time.sleep(0.25)
        else:
            raise RuntimeError("Vite did not become ready within 20 seconds.")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def test_store_koko_theme_and_workspace_tabs(page, vite_url):
    def mock_api(route):
        path = route.request.url.split("?", 1)[0]
        if path.endswith("/health"):
            payload = {"database": "ok"}
        elif path.endswith("/security/status"):
            payload = {"pin_configured": False}
        elif path.endswith("/dashboard"):
            payload = {"revenue": 0, "net_profit": 0, "receivables": 0, "low_stock_count": 0}
        elif "/reports/" in path:
            payload = {"count": 0, "total": 0, "documents": []}
        elif path.endswith("/backups"):
            payload = []
        else:
            payload = []
        route.fulfill(status=200, content_type="application/json", body=__import__("json").dumps(payload))

    page.route("**/api/**", mock_api)
    page.goto(vite_url)
    expect(page.locator(".sidebar nav button").first).to_be_visible()

    launcher = page.locator("#koko-theme-launcher")
    expect(launcher).to_be_visible()
    launcher.click()
    panel = page.locator("#koko-theme-panel")
    panel.locator("#kt-theme").select_option("dark")
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "dark")
    expect(panel).to_have_attribute("aria-hidden", "false")
    expect(launcher).to_have_attribute("aria-expanded", "true")
    assert page.locator("html").evaluate(
        "(el) => getComputedStyle(el).getPropertyValue('--koko-bg').trim() === '#101923'"
    )
    page.keyboard.press("Escape")
    expect(panel).to_be_hidden()
    expect(launcher).to_have_attribute("aria-expanded", "false")
    page.reload()
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "dark")

    page.get_by_role("button", name="کالاها", exact=True).click()
    expect(page).to_have_url(vite_url.rstrip("/") + "/products")
    expect(page.locator("#koko-workspace-tabs .koko-tab.active")).to_contain_text("کالاها")
    page.get_by_role("button", name="بستن کالاها").click()
    expect(page).to_have_url(vite_url)
    expect(page.locator("#koko-workspace-tabs .koko-tab.active")).to_contain_text("داشبورد")

    page.locator("#koko-theme-launcher").click()
    page.locator("#kt-reset").click()
    expect(page.locator("html")).to_have_attribute("data-koko-theme", "pastel")
    page.set_viewport_size({"width": 390, "height": 844})
    assert page.locator("body").evaluate("(el) => el.scrollWidth <= window.innerWidth")

    toggle = page.get_by_role("button", name="☰ منو")
    expect(toggle).to_be_visible()
    toggle.click()
    expect(page.locator("#store-sidebar")).to_have_class("sidebar is-open")
    page.get_by_role("button", name="مشتریان", exact=True).click()
    expect(page.locator("#store-sidebar")).not_to_have_class("is-open")
