import pytest
from pages.saucedemo_page import SaucademoPage


# ------------------------------------------------------------------ #
#  Parametrize — Login con múltiples usuarios
#
#  En vez de escribir un test por cada caso, declaras los datos
#  y pytest genera un test por cada fila automáticamente.
#
#  Formato: @pytest.mark.parametrize("param1, param2", [
#               (valor1a, valor2a),   ← caso 1
#               (valor1b, valor2b),   ← caso 2
#           ])
# ------------------------------------------------------------------ #

@pytest.mark.parametrize("username, password, expected_message", [
    ("standard_user",   "secret_sauce", "inventory"),           # login exitoso → verifica URL
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("invalid_user",    "secret_sauce", "Username and password do not match"),
])
def test_login_multiples_usuarios(page, username, password, expected_message):
    login = SaucademoPage(page)
    login.navigate()
    login.login_exitoso(username, password)

    # Para el usuario válido verificamos la URL, para los inválidos el mensaje de error
    if username == "standard_user":
        assert expected_message in page.url
    else:
        assert expected_message in login.error_message().inner_text()


# ------------------------------------------------------------------ #
#  Parametrize — Agregar múltiples productos al carrito
#
#  El mismo flujo de add_to_cart pero con productos distintos.
# ------------------------------------------------------------------ #

@pytest.mark.parametrize("product_id, name, price", [
    ("sauce-labs-backpack",   "Sauce Labs Backpack",   "$29.99"),
    ("sauce-labs-bike-light", "Sauce Labs Bike Light", "$9.99"),
    ("sauce-labs-onesie",     "Sauce Labs Onesie",     "$7.99"),
])
def test_agregar_productos(saucedemo, product_id, name, price):
    saucedemo.add_to_cart(product_id=product_id, name=name, expected_price=price)
    assert saucedemo.page.locator("[data-test='shopping-cart-badge']").inner_text() == "1"
