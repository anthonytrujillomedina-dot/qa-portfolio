from pages.wikipedia_page import WikipediaPage

def test_navegacion_wikipedia(page):
    wiki = WikipediaPage(page)
    wiki.navigate()
    assert "Wikipedia" in wiki.obtener_titulo_resultado()

def test_busqueda_wikipedia(page):
    wiki = WikipediaPage(page)
    wiki.navigate()
    wiki.search("Playwright")
    assert "Playwright" in wiki.obtener_titulo_resultado()
