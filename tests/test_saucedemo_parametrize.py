"""
Parametrized test suite for Saucedemo.

Demonstrates pytest.mark.parametrize to run the same test logic
against multiple data sets without duplicating test functions.
"""

import pytest
from pages.saucedemo_page import SaucedemoPage


@pytest.mark.parametrize("username, password, expected", [
    ("standard_user",   "secret_sauce", "inventory"),
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("invalid_user",    "secret_sauce", "Username and password do not match"),
])
def test_login_multiple_users(page, username, password, expected):
    """Verify login behavior for valid, locked-out, and invalid users."""
    login = SaucedemoPage(page)
    login.navigate()
    login.login(username, password)

    if username == "standard_user":
        assert expected in page.url
    else:
        assert expected in login.error_message().inner_text()


@pytest.mark.parametrize("product_id, name, price", [
    ("sauce-labs-backpack",   "Sauce Labs Backpack",   "$29.99"),
    ("sauce-labs-bike-light", "Sauce Labs Bike Light", "$9.99"),
    ("sauce-labs-onesie",     "Sauce Labs Onesie",     "$7.99"),
])
def test_add_multiple_products(saucedemo, product_id, name, price):
    """Verify each product can be added to the cart individually."""
    saucedemo.add_to_cart(product_id=product_id, name=name, expected_price=price)
    assert saucedemo.page.locator("[data-test='shopping-cart-badge']").inner_text() == "1"
