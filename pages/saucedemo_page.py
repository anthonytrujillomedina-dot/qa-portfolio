from playwright.sync_api import Page

class SaucademoPage:
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        self.page.goto(self.URL)

    # --- Locators ---

    def username(self):
        return self.page.locator("#user-name")
    
    def password(self):
        return self.page.locator("#password")
    
    def error_message(self):
        return self.page.locator("[data-test='error']")
    
    # --- Acciones ---

    def login_exitoso(self, username:str ,password:str):
        self.username().fill(username)
        self.password().fill(password)
        self.page.get_by_role("button", name = "Login").click()

    def add_to_cart(self, product_id: str, name: str, expected_price: str):
        
        # Paso 1: encuentra el contenedor del producto por su nombre
        # .filter() limita la búsqueda al contenedor que tiene ese texto
        product = self.page.locator(".inventory_item").filter(
            has=self.page.get_by_text(name)
        )

        # Paso 2: lee el precio dentro de ese contenedor
        actual_price = product.locator("[data-test='inventory-item-price']").inner_text()

        # Paso 3: solo agrega al carrito si el precio coincide
        if actual_price == expected_price:
            self.page.locator(f"[data-test='add-to-cart-{product_id}']").click()

    def go_to_cart(self):
        self.page.locator("[data-test='shopping-cart-link']").click()

    def cart_product_name(self):
        return self.page.locator("[data-test='inventory-item-name']").inner_text()

    def click_checkout(self):
        self.page.locator("[data-test='checkout']").click()

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        self.page.locator("[data-test='firstName']").fill(first_name)
        self.page.locator("[data-test='lastName']").fill(last_name)
        self.page.locator("[data-test='postalCode']").fill(zip_code)
        self.page.locator("[data-test='continue']").click()

    def finish_order(self):
        self.page.locator("[data-test='finish']").click()

    def order_confirmation(self):
        return self.page.locator("[data-test='complete-header']").inner_text()




