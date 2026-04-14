# QA Automation Portfolio

Portafolio de automatización de pruebas que cubre las tres capas principales del testing: **UI end-to-end**, **API REST** y **rendimiento**.

🔗 **[Ver reporte Allure en vivo](https://anthonytrujillomedina-dot.github.io/qa-portfolio/)**

![CI Status](https://github.com/anthonytrujillomedina-dot/qa-portfolio/actions/workflows/tests.yml/badge.svg)

---

## Tecnologías

| Capa | Herramienta |
|---|---|
| UI E2E | Playwright + Pytest |
| API REST | Pytest + Requests |
| Performance | K6 |
| Reportes | Allure (GitHub Pages) |
| CI/CD | GitHub Actions |

---

## Estructura del proyecto

```
qa-portfolio/
├── pages/                        # Page Object Model
│   ├── saucedemo_page.py
│   └── wikipedia_page.py
├── tests/
│   ├── test_saucedemo.py         # Tests E2E — login, carrito, checkout
│   ├── test_saucedemo_parametrize.py  # Tests parametrizados con múltiples usuarios
│   ├── test_wikipedia.py         # Tests E2E — búsqueda y navegación
│   └── test_api.py               # Tests de API REST con fixtures y parametrize
├── k6/
│   ├── smoke_test.js             # 1 usuario — verifica que el sitio responde
│   └── load_test.js              # Rampa de 10 usuarios con thresholds
├── conftest.py                   # Fixtures compartidas
├── pytest.ini                    # Configuración de Pytest
└── .github/workflows/tests.yml   # Pipeline CI/CD
```

---

## Tests de UI — Saucedemo

Pruebas end-to-end sobre [saucedemo.com](https://www.saucedemo.com) usando el patrón **Page Object Model**.

**Casos cubiertos:**
- Login con credenciales válidas e inválidas
- Agregar y eliminar productos del carrito
- Flujo completo de checkout
- Ordenamiento de productos
- Tests parametrizados con múltiples tipos de usuario

---

## Tests de API — JSONPlaceholder

Pruebas funcionales sobre la API REST de [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com).

**Casos cubiertos:**
- `GET /posts` — lista completa con validación de estructura
- `GET /posts/{id}` — parametrizado con 5 IDs distintos
- `GET /posts/9999` — manejo de recurso no encontrado (404)
- `POST /posts` — creación con distintos payloads
- `PUT /posts/{id}` — actualización completa
- `DELETE /posts/{id}` — eliminación con fixture de setup/teardown

---

## Tests de Performance — K6

Pruebas de carga sobre la API REST usando [K6](https://k6.io).

**Smoke test** — verifica que el sitio responde correctamente con 1 usuario.

**Load test** — rampa de carga con thresholds:
- 10 usuarios simultáneos durante 1 minuto
- p(95) de respuesta < 2 segundos
- Tasa de errores < 5%

---

## Cómo ejecutar localmente

### Requisitos
- Python 3.12+
- K6

### Instalar dependencias
```bash
pip install -r requirements.txt
playwright install chromium
```

### Correr tests de UI y API
```bash
pytest --alluredir=allure-results
```

### Correr tests de K6
```bash
# Smoke test
k6 run k6/smoke_test.js

# Load test con reporte HTML
$env:K6_WEB_DASHBOARD="true"; $env:K6_WEB_DASHBOARD_EXPORT="k6/reports/load_report.html"; k6 run k6/load_test.js
```

---

## CI/CD

El pipeline se ejecuta automáticamente en cada push a `main` y tiene dos jobs:

1. **test** — corre todos los tests de Playwright y Pytest, publica el reporte en Allure
2. **performance** — instala K6, corre smoke y load test, sube el reporte HTML como artifact
