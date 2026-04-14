"""
Pytest configuration — shared fixtures and hooks for the QA portfolio suite.
"""

import sys
import pytest
import allure
import requests

sys.path.insert(0, ".")

from pages.saucedemo_page import SaucedemoPage


# --- API fixtures ---

@pytest.fixture(scope="session")
def api_base_url():
    """URL base de la API REST usada en los tests de rendimiento y funcionales."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api_session(api_base_url):
    """Sesión HTTP reutilizable con headers JSON preconfigurados."""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    session.base_url = api_base_url
    yield session
    session.close()


@pytest.fixture
def existing_post(api_session):
    """Crea un post antes del test y lo elimina al finalizar (setup/teardown)."""
    payload = {
        "title": "Post de prueba",
        "body": "Creado por fixture de Pytest",
        "userId": 1,
    }
    response = api_session.post(f"{api_session.base_url}/posts", json=payload)
    post = response.json()

    yield post

    api_session.delete(f"{api_session.base_url}/posts/{post['id']}")


@pytest.fixture
def saucedemo(page):
    """Return a SaucedemoPage already logged in as standard_user.

    Used by cart and checkout tests that require an authenticated session.
    Equivalent to a beforeEach that handles the login precondition.
    """
    login = SaucedemoPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    return login


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
