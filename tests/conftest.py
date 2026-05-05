import pytest
import os
from playwright.sync_api import sync_playwright

# Определяем, запущены ли тесты в CI среде
IS_CI = os.environ.get('CI') == 'true'

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # В CI запускаем headless, локально - можно с GUI
        browser = p.chromium.launch(headless=IS_CI)
        yield browser
        browser.close()

@pytest.fixture
def context(browser):
    context = browser.new_context()
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()