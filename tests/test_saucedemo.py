import pytest
import allure
from pages.saucedemo_page import SaucademoPage


@allure.feature("Login")
class TestLogin:

    @allure.title("Login exitoso con usuario válido")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_exitoso(self, page):
        with allure.step("Navegar a saucedemo"):
            login = SaucademoPage(page)
            login.navigate()

        with allure.step("Ingresar credenciales válidas"):
            login.login_exitoso("standard_user", "secret_sauce")

        with allure.step("Verificar redirección a la página de productos"):
            assert "inventory" in page.url

    @allure.title("Login fallido con contraseña incorrecta")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    def test_login_error(self, page):
        with allure.step("Navegar a saucedemo"):
            login = SaucademoPage(page)
            login.navigate()

        with allure.step("Ingresar credenciales inválidas"):
            login.login_exitoso("standard_user", "error pass")

        with allure.step("Verificar mensaje de error"):
            assert "Epic sadface" in login.error_message().inner_text()


@allure.feature("Carrito")
class TestCart:

    @allure.title("Agregar producto al carrito")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_card(self, saucedemo):
        with allure.step("Agregar Sauce Labs Backpack al carrito"):
            saucedemo.add_to_cart(
                product_id="sauce-labs-backpack",
                name="Sauce Labs Backpack",
                expected_price="$29.99"
            )

        with allure.step("Verificar que el carrito muestra 1 producto"):
            assert saucedemo.page.locator("[data-test='shopping-cart-badge']").inner_text() == "1"

    @allure.title("Flujo completo: agregar al carrito y hacer checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.cart
    def test_checkout_completo(self, saucedemo):
        with allure.step("Agregar Sauce Labs Backpack al carrito"):
            saucedemo.add_to_cart(
                product_id="sauce-labs-backpack",
                name="Sauce Labs Backpack",
                expected_price="$29.99"
            )

        with allure.step("Ir al carrito y verificar producto"):
            saucedemo.go_to_cart()
            assert saucedemo.cart_product_name() == "Sauce Labs Backpack"

        with allure.step("Completar formulario de checkout"):
            saucedemo.click_checkout()
            saucedemo.fill_checkout_info("Tony", "QA", "12345")

        with allure.step("Finalizar orden y verificar confirmación"):
            saucedemo.finish_order()
            assert saucedemo.order_confirmation() == "Thank you for your order!"
