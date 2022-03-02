import os
from pathlib import Path

import environ
import pytest
from playwright.sync_api import sync_playwright

# from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager

# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
env = environ.Env(
    LOGIN_USERNAME=str,
    LOGIN_PASSWORD=str,
)
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


@pytest.mark.django_db
def test_playwright_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/deets/test-1")
        browser.close()


@pytest.mark.django_db
def test_login():
    pass
    # webdriver/chrome isn't working on debian_local
    # driver.get("http://www.google.com")
    # assert "Google" in driver.title


@pytest.mark.django_db
def test_playwright_login2():
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/login/")
        assert page.inner_text("h2") == "Login"
        page.fill("input[name=username]", env("LOGIN_USERNAME"))
        page.fill("input[name=password]", env("LOGIN_PASSWORD"))
        page.click("input[value=Login]")
        assert page.inner_text("a[class=main__link]") == "test 1"
        # need a more specific selector here
        browser.close()
