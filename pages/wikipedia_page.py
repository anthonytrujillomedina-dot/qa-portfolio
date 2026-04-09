from playwright.sync_api import Page

class WikipediaPage:
    # Constructor de la clase WikipediaPage
    def __init__(self, page: Page):
        self.page = page

    # Método para navegar a la página principal de Wikipedia
    def navigate(self):
        self.page.goto("https://en.wikipedia.org/wiki/Main_Page")

    # Método para realizar una búsqueda en Wikipedia
    def search(self, query: str):
        self.page.fill("#searchInput", query)
        self.page.keyboard.press("Enter")

    # Método para obtener el título del resultado de la búsqueda
    def obtener_titulo_resultado(self):
        self.page.wait_for_load_state("networkidle")
        return self.page.title()