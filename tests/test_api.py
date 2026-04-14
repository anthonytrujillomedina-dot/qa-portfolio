import pytest
import allure


@allure.feature("API Posts")
class TestGetPosts:

    @allure.story("Listar posts")
    @allure.title("GET /posts retorna 100 posts")
    def test_get_all_posts(self, api_session):
        response = api_session.get(f"{api_session.base_url}/posts")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json; charset=utf-8"
        assert len(response.json()) == 100

    @allure.story("Obtener post específico")
    @allure.title("GET /posts/1 retorna el post correcto")
    def test_get_single_post(self, api_session):
        response = api_session.get(f"{api_session.base_url}/posts/1")
        body = response.json()

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 2
        assert body["id"] == 1
        assert "title" in body
        assert "body" in body
        assert body["userId"] == 1

    @allure.story("Post no encontrado")
    @allure.title("GET /posts/9999 retorna 404")
    def test_get_nonexistent_post(self, api_session):
        response = api_session.get(f"{api_session.base_url}/posts/9999")

        assert response.status_code == 404

    @pytest.mark.parametrize("post_id", [1, 25, 50, 75, 100])
    @allure.story("Obtener post específico")
    @allure.title("GET /posts/{post_id} retorna estructura válida")
    def test_get_post_structure(self, api_session, post_id):
        response = api_session.get(f"{api_session.base_url}/posts/{post_id}")
        body = response.json()

        assert response.status_code == 200
        assert body["id"] == post_id
        assert isinstance(body["title"], str) and len(body["title"]) > 0
        assert isinstance(body["body"], str) and len(body["body"]) > 0
        assert isinstance(body["userId"], int)


@allure.feature("API Posts")
class TestCreatePost:

    @allure.story("Crear post")
    @allure.title("POST /posts crea un recurso y retorna 201")
    def test_create_post(self, api_session):
        payload = {
            "title": "QA Portfolio Test",
            "body": "Prueba de API con Pytest y requests",
            "userId": 1,
        }

        response = api_session.post(f"{api_session.base_url}/posts", json=payload)
        body = response.json()

        assert response.status_code == 201
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert "id" in body

    @pytest.mark.parametrize("payload,expected_status", [
        ({"title": "Solo título", "userId": 1}, 201),
        ({"body": "Solo body", "userId": 1}, 201),
        ({}, 201),
    ])
    @allure.story("Crear post con distintos payloads")
    @allure.title("POST /posts maneja distintos payloads correctamente")
    def test_create_post_variants(self, api_session, payload, expected_status):
        response = api_session.post(f"{api_session.base_url}/posts", json=payload)

        assert response.status_code == expected_status
        assert "id" in response.json()


@allure.feature("API Posts")
class TestUpdatePost:

    @allure.story("Actualizar post")
    @allure.title("PUT /posts/1 actualiza el recurso completo")
    def test_update_post(self, api_session):
        payload = {
            "id": 1,
            "title": "Título actualizado",
            "body": "Contenido actualizado",
            "userId": 1,
        }

        response = api_session.put(f"{api_session.base_url}/posts/1", json=payload)
        body = response.json()

        assert response.status_code == 200
        assert body["title"] == payload["title"]

    @allure.story("Eliminar post")
    @allure.title("DELETE /posts/{id} elimina el recurso")
    def test_delete_post(self, api_session, existing_post):
        response = api_session.delete(
            f"{api_session.base_url}/posts/{existing_post['id']}"
        )

        assert response.status_code == 200
