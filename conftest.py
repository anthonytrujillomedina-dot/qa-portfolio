"""
Pytest configuration — shared fixtures and hooks for the QA portfolio suite.
"""

import sys
import pytest
import allure

sys.path.insert(0, ".")

from pages.saucedemo_page import SaucedemoPage


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
