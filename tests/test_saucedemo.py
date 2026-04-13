"""
Test suite for Saucedemo — login and cart flows.

Organized into two feature classes:
- TestLogin: successful and failed authentication scenarios.
- TestCart:  add-to-cart and full checkout scenarios.
"""

import pytest
import allure
from pages.saucedemo_page import SaucedemoPage


@allure.feature("Login")
class TestLogin:

    @allure.title("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_success(self, page):
        with allure.step("Navigate to Saucedemo"):
            login = SaucedemoPage(page)
            login.navigate()

        with allure.step("Enter valid credentials"):
            login.login("standard_user", "secret_sauce")

        with allure.step("Verify redirect to products page"):
            assert "inventory" in page.url

    @allure.title("Failed login with wrong password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_failure(self, page):
        with allure.step("Navigate to Saucedemo"):
            login = SaucedemoPage(page)
            login.navigate()

        with allure.step("Enter invalid credentials"):
            login.login("standard_user", "wrong_password")

        with allure.step("Verify error message is displayed"):
            assert "Epic sadface" in login.error_message().inner_text()


@allure.feature("Cart")
class TestCart:

    @allure.title("Add a product to the cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_to_cart(self, saucedemo):
        with allure.step("Add Sauce Labs Backpack to cart"):
            saucedemo.add_to_cart(
                product_id="sauce-labs-backpack",
                name="Sauce Labs Backpack",
                expected_price="$29.99"
            )

        with allure.step("Verify cart badge shows 1 item"):
            assert saucedemo.page.locator("[data-test='shopping-cart-badge']").inner_text() == "1"

    @allure.title("Full flow: add to cart and complete checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_checkout_complete(self, saucedemo):
        with allure.step("Add Sauce Labs Backpack to cart"):
            saucedemo.add_to_cart(
                product_id="sauce-labs-backpack",
                name="Sauce Labs Backpack",
                expected_price="$29.99"
            )

        with allure.step("Go to cart and verify product"):
            saucedemo.go_to_cart()
            assert saucedemo.cart_product_name() == "Sauce Labs Backpack"

        with allure.step("Fill in checkout information"):
            saucedemo.click_checkout()
            saucedemo.fill_checkout_info("Tony", "QA", "12345")

        with allure.step("Finish order and verify confirmation"):
            saucedemo.finish_order()
            assert saucedemo.order_confirmation() == "Thank you for your order!"
