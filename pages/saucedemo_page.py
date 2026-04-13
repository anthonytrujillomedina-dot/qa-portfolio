from playwright.sync_api import Page


class SaucedemoPage:
    """Page Object for https://www.saucedemo.com.

    Encapsulates all locators and interactions for the Saucedemo application,
    covering login, product catalog, cart, and checkout flows.
    """

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #

    def navigate(self):
        """Open the Saucedemo home page."""
        self.page.goto(self.URL)

    # ------------------------------------------------------------------ #
    # Locators (private)
    # ------------------------------------------------------------------ #

    def _username(self):
        return self.page.locator("#user-name")

    def _password(self):
        return self.page.locator("#password")

    def error_message(self):
        """Return the error banner locator (visible after a failed login)."""
        return self.page.locator("[data-test='error']")

    # ------------------------------------------------------------------ #
    # Actions — Login
    # ------------------------------------------------------------------ #

    def login(self, username: str, password: str):
        """Fill in credentials and submit the login form."""
        self._username().fill(username)
        self._password().fill(password)
        self.page.get_by_role("button", name="Login").click()

    # ------------------------------------------------------------------ #
    # Actions — Products
    # ------------------------------------------------------------------ #

    def add_to_cart(self, product_id: str, name: str, expected_price: str):
        """Add a product to the cart after verifying its price.

        Uses .filter() to scope the price check to the specific product
        container, avoiding strict-mode violations on shared locators.
        """
        product = self.page.locator(".inventory_item").filter(
            has=self.page.get_by_text(name)
        )
        actual_price = product.locator("[data-test='inventory-item-price']").inner_text()
        if actual_price == expected_price:
            self.page.locator(f"[data-test='add-to-cart-{product_id}']").click()

    # ------------------------------------------------------------------ #
    # Actions — Cart & Checkout
    # ------------------------------------------------------------------ #

    def go_to_cart(self):
        """Click the shopping cart icon."""
        self.page.locator("[data-test='shopping-cart-link']").click()

    def cart_product_name(self):
        """Return the name of the first product in the cart."""
        return self.page.locator("[data-test='inventory-item-name']").inner_text()

    def click_checkout(self):
        """Click the Checkout button inside the cart."""
        self.page.locator("[data-test='checkout']").click()

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        """Fill the checkout step-one form and proceed to the order overview."""
        self.page.locator("[data-test='firstName']").fill(first_name)
        self.page.locator("[data-test='lastName']").fill(last_name)
        self.page.locator("[data-test='postalCode']").fill(zip_code)
        self.page.locator("[data-test='continue']").click()

    def finish_order(self):
        """Click Finish to complete the purchase."""
        self.page.locator("[data-test='finish']").click()

    def order_confirmation(self):
        """Return the confirmation header text after a successful order."""
        return self.page.locator("[data-test='complete-header']").inner_text()
