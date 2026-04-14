import http from 'k6/http';
import { check, sleep } from 'k6';

// Smoke test: 1 usuario, 1 iteración
// Objetivo: verificar que el sitio responde correctamente
export const options = {
  vus: 1,
  iterations: 1,
};

const BASE_URL = 'https://www.saucedemo.com';

export default function () {
  // 1. Cargar la página principal
  const res = http.get(BASE_URL);

  check(res, {
    'status es 200': (r) => r.status === 200,
    'página carga en menos de 2s': (r) => r.timings.duration < 2000,
    'contiene referencia a la app': (r) => r.body.includes('Swag Labs'),
  });

  sleep(1);
}
