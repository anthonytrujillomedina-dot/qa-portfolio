import http from 'k6/http';
import { check, sleep } from 'k6';
import { Trend, Rate } from 'k6/metrics';

// Métricas personalizadas
const getDuration = new Trend('get_duration');
const postDuration = new Trend('post_duration');
const errorRate = new Rate('error_rate');

// Load test contra JSONPlaceholder (API REST pública)
// Objetivo: medir comportamiento bajo carga real con peticiones GET y POST
export const options = {
  stages: [
    { duration: '30s', target: 10 }, // subir a 10 usuarios en 30s
    { duration: '1m',  target: 10 }, // mantener 10 usuarios por 1 minuto
    { duration: '20s', target: 0  }, // bajar a 0 usuarios
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% de requests deben responder en < 2s
    error_rate: ['rate<0.05'],         // menos del 5% de errores
  },
};

const BASE_URL = 'https://jsonplaceholder.typicode.com';

export default function () {
  // 1. GET: obtener lista de posts
  const getPosts = http.get(`${BASE_URL}/posts`);

  check(getPosts, {
    'GET /posts status 200': (r) => r.status === 200,
    'GET /posts devuelve array': (r) => JSON.parse(r.body).length > 0,
  });

  getDuration.add(getPosts.timings.duration);
  errorRate.add(getPosts.status !== 200);

  sleep(1);

  // 2. GET: obtener un post específico
  const getPost = http.get(`${BASE_URL}/posts/1`);

  check(getPost, {
    'GET /posts/1 status 200': (r) => r.status === 200,
    'GET /posts/1 tiene título': (r) => JSON.parse(r.body).title !== undefined,
  });

  errorRate.add(getPost.status !== 200);

  sleep(1);

  // 3. POST: crear un nuevo post
  const payload = JSON.stringify({
    title: 'Test de carga K6',
    body: 'Probando rendimiento con K6',
    userId: 1,
  });

  const params = { headers: { 'Content-Type': 'application/json' } };
  const createPost = http.post(`${BASE_URL}/posts`, payload, params);

  check(createPost, {
    'POST /posts status 201': (r) => r.status === 201,
    'POST /posts devuelve id': (r) => JSON.parse(r.body).id !== undefined,
  });

  postDuration.add(createPost.timings.duration);
  errorRate.add(createPost.status !== 201);

  sleep(1);
}
