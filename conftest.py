import sys
import pytest
sys.path.insert(0, ".")

from pages.saucedemo_page import SaucademoPage


@pytest.fixture
def saucedemo(page):
    
    """
    Fixture que entrega un SaucademoPage ya logueado.
    Se ejecuta automáticamente antes de cada test que la pida.
    """
    
    login = SaucademoPage(page)
    login.navigate()
    login.login_exitoso("standard_user", "secret_sauce")
    return login


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook que se ejecuta despues de cada test.
    Si el test fallo, toma un screenshot y lo adjunta al reporte HTML.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot = page.screenshot()
            report.extras = getattr(report, "extras", [])
            report.extras.append(pytest.html.extras.image(screenshot, mime_type="image/png"))
