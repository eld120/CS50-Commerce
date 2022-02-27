import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.django_db
def test_login():

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/deets/test-1")
        browser.close()
