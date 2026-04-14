import requests
import allure

BASE_URL = "https://jsonplaceholder.typicode.com"


@allure.feature("API Posts")
class TestGetPosts:

    @allure.story("Listar posts")
    @allure.title("GET /posts retorna 100 posts")
    def test_get_all_posts(self):
        response = requests.get(f"{BASE_URL}/posts")

        assert response.status_code == 200
        assert len(response.json()) == 100

    @allure.story("Obtener post específico")
    @allure.title("GET /posts/1 retorna el post correcto")
    def test_get_single_post(self):
        response = requests.get(f"{BASE_URL}/posts/1")
        body = response.json()

        assert response.status_code == 200
        assert body["id"] == 1
        assert "title" in body
        assert "body" in body
        assert body["userId"] == 1

    @allure.story("Post no encontrado")
    @allure.title("GET /posts/9999 retorna 404")
    def test_get_nonexistent_post(self):
        response = requests.get(f"{BASE_URL}/posts/9999")

        assert response.status_code == 404


@allure.feature("API Posts")
class TestCreatePost:

    @allure.story("Crear post")
    @allure.title("POST /posts crea un recurso y retorna 201")
    def test_create_post(self):
        payload = {
            "title": "QA Portfolio Test",
            "body": "Prueba de API con Pytest y requests",
            "userId": 1,
        }

        response = requests.post(f"{BASE_URL}/posts", json=payload)
        body = response.json()

        assert response.status_code == 201
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert "id" in body


@allure.feature("API Posts")
class TestUpdatePost:

    @allure.story("Actualizar post")
    @allure.title("PUT /posts/1 actualiza el recurso completo")
    def test_update_post(self):
        payload = {
            "id": 1,
            "title": "Título actualizado",
            "body": "Contenido actualizado",
            "userId": 1,
        }

        response = requests.put(f"{BASE_URL}/posts/1", json=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["title"] == payload["title"]

    @allure.story("Eliminar post")
    @allure.title("DELETE /posts/1 elimina el recurso")
    def test_delete_post(self):
        response = requests.delete(f"{BASE_URL}/posts/1")

        assert response.status_code == 200
