import pytest

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))



@pytest.mark.django_db
def test_login():
    driver.get("http://www.google.com")
    assert 'Google' in driver.title
    