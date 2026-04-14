# K6 Performance Tests

Pruebas de rendimiento contra [Saucedemo](https://www.saucedemo.com) usando [K6](https://k6.io).

## Requisitos

- [K6](https://k6.io/docs/get-started/installation/) instalado

## Archivos

| Archivo | Descripción |
|---|---|
| `smoke_test.js` | 1 usuario, 1 iteración — verifica que el sitio responde |
| `load_test.js` | Rampa de 10 usuarios — mide comportamiento bajo carga |

## Cómo ejecutar

### Smoke test
```bash
k6 run k6/smoke_test.js
```

### Load test
```bash
k6 run k6/load_test.js
```

## Thresholds (criterios de paso)

- 95% de requests deben responder en menos de **2 segundos**
- Tasa de errores menor al **5%**
