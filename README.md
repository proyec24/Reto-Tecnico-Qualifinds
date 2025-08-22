# Chuck Norris Backend (PHP) — Jr Backend Engineer Challenge

Backend sencillo en PHP 8 que consume la Chuck Norris API y expone endpoints propios en el puerto 5000. Incluye validación de categorías, manejo de errores y un endpoint de búsqueda (bonus).

Endpoints

Base URL (local): `http://127.0.0.1:5000`

GET /categories

Retorna la lista de categorías disponibles.

Respuesta 200

```
["animal","career","celebrity","dev","explicit","fashion","food","history","money","movie","music","political","religion","science","sport","travel"]
```

GET /joke/{category}

Retorna un chiste aleatorio de la categoría indicada.

Respuesta 200

```
{
"id": "8d7m0p3tQ_6Jk9bC0b6xVg",
"url": "https://api.chucknorris.io/jokes/8d7m0p3tQ_6Jk9bC0b6xVg",
"category": "dev",
"value": "Chuck Norris writes code that optimizes itself."
}
```

Respuesta 400 (categoría inválida)

```
{
"error": "Bad Request",
"message": "Invalid category. See valid_categories for options."
}
```

GET /search?query=term (bonus)

Busca chistes por término.

Respuesta 200

```
{
"total": 2,
"results": [
{
"id": "abc123",
"url": "https://api.chucknorris.io/jokes/abc123",
"category": "dev",
"value": "Chuck Norris can divide by zero."
},
{
"id": "def456",
"url": "https://api.chucknorris.io/jokes/def456",
"category": null,
"value": "When Chuck Norris throws exceptions, it's across the room."
}
]
}
```

## Códigos de estado

200 OK — Respuesta correcta.

400 Bad Request — Input inválido (p.ej. categoría inexistente o query vacío).

404 Not Found — Ruta inexistente.

405 Method Not Allowed — Solo se soporta GET.

502 Bad Gateway — Falla comunicando con la API pública (timeout, 4xx/5xx del upstream).

500 Internal Server Error — Error inesperado local.

## Arquitectura & Diseño

PHP puro + cURL, sin dependencias en runtime.

PSR-4 autoload con Composer.

Capas: Router mínimo → Controladores → Servicios (API externa y validación) → Excepciones → Respuestas JSON.

Validación de categoría con cache en memoria (proceso) para evitar llamadas redundantes.

Timeouts y manejo de errores de red centralizado en ChuckClient.

### Cómo correr (puerto 5000)

Prerrequisitos

PHP ≥ 8.0 (recomendado 8.1+)

Composer (para autoload)

cURL habilitado

Pasos

### 1) Instalar autoload

composer dump-autoload

### 2) Levantar el servidor embebido en 0.0.0.0:5000

php -S 127.0.0.1:5000 -t public

Probar rápido
curl http://127.0.0.1:5000/categories
curl http://127.0.0.1:5000/joke/dev
curl "http://127.0.0.1:5000/search?query=database"

## Ejemplos de uso (curl)

### Lista de categorías

curl -s http://127.0.0.1:5000/categories | jq .

### Chiste por categoría (case-insensitive)

curl -s http://127.0.0.1:5000/joke/DEV | jq .

### Búsqueda

curl -s "http://127.0.0.1:5000/search?query=cloud" | jq .

###Configuración

Valores definidos en src/Bootstrap.php:

baseUrl: https://api.chucknorris.io

timeoutSeconds: 5