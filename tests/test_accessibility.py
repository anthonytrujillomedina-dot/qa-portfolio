import allure
import pytest
from axe_playwright_python.sync_playwright import Axe

axe = Axe()


@allure.feature("Accesibilidad")
class TestAccessibility:

    @allure.story("Saucedemo")
    @allure.title("Página de login no tiene violaciones de accesibilidad críticas")
    def test_login_page_accessibility(self, page):
        page.goto("https://www.saucedemo.com")
        results = axe.run(page)

        violations = [v for v in results.response["violations"] if v["impact"] in ("critical", "serious")]

        if violations:
            report = "\n".join(
                f"[{v['impact'].upper()}] {v['id']}: {v['description']}"
                for v in violations
            )
            allure.attach(report, name="Violaciones de accesibilidad", attachment_type=allure.attachment_type.TEXT)

        assert len(violations) == 0, f"Se encontraron {len(violations)} violaciones críticas:\n{report}"

    @pytest.mark.xfail(
        reason="Bug conocido en Saucedemo: el dropdown de ordenamiento no tiene etiqueta accesible (select-name)"
    )
    @allure.story("Saucedemo")
    @allure.title("Página de inventario no tiene violaciones de accesibilidad críticas")
    def test_inventory_page_accessibility(self, page):
        page.goto("https://www.saucedemo.com")
        page.fill("#user-name", "standard_user")
        page.fill("#password", "secret_sauce")
        page.click("#login-button")
        page.wait_for_url("**/inventory.html")

        results = axe.run(page)

        violations = [v for v in results.response["violations"] if v["impact"] in ("critical", "serious")]

        if violations:
            report = "\n".join(
                f"[{v['impact'].upper()}] {v['id']}: {v['description']}"
                for v in violations
            )
            allure.attach(report, name="Violaciones de accesibilidad", attachment_type=allure.attachment_type.TEXT)

        assert len(violations) == 0, f"Se encontraron {len(violations)} violaciones críticas:\n{report}"

    @allure.story("Wikipedia")
    @allure.title("Página principal de Wikipedia no tiene violaciones críticas")
    def test_wikipedia_accessibility(self, page):
        page.goto("https://www.wikipedia.org")
        results = axe.run(page)

        violations = [v for v in results.response["violations"] if v["impact"] in ("critical", "serious")]

        if violations:
            report = "\n".join(
                f"[{v['impact'].upper()}] {v['id']}: {v['description']}"
                for v in violations
            )
            allure.attach(report, name="Violaciones de accesibilidad", attachment_type=allure.attachment_type.TEXT)

        assert len(violations) == 0, f"Se encontraron {len(violations)} violaciones críticas:\n{report}"
