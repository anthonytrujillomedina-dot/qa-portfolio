
#Inportación de Playwright 
from playwright.sync_api import Page

# Test para verificar que la página de Google
def test_google_search(page: Page):
    page.goto("https://www.google.com") # Abre el navegador de Google
    assert "Google" in page.title()     # Verifica que el título de la página contenga "Google"
