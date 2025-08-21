<?php
declare(strict_types=1);

namespace App;

use App\Exception\HttpException;
use App\Exception\UpstreamException;
use App\Http\JsonResponse;
use App\Http\Router;
use App\Service\CategoryService;
use App\Service\ChuckClient;

final class Bootstrap
{
    private Router $router;
    private ChuckClient $client;
    private CategoryService $categoryService;

    public function __construct()
    {
        $this->client = new ChuckClient(
            baseUrl: 'https://api.chucknorris.io',
            timeoutSeconds: 5
        );

        $this->categoryService = new CategoryService($this->client);

        $this->router = new Router();
        $this->mountRoutes();
    }

    private function mountRoutes(): void
    {
        $cat = new \App\Controller\CategoryController($this->categoryService);
        $joke = new \App\Controller\JokeController($this->client, $this->categoryService);
        $search = new \App\Controller\SearchController($this->client);

        $this->router->get('/', fn() => new JsonResponse(['endpoints' => [
            'GET /categories', 'GET /joke/{category}', 'GET /search?query=term'
        ]]));

        $this->router->get('/categories', [$cat, 'index']);
        $this->router->get('/joke/{category}', [$joke, 'show']);
        $this->router->get('/search', [$search, 'index']);
    }

    public function router(): Router
    {
        return $this->router;
    }

    public function handleException(\Throwable $e): JsonResponse
    {
        // Normalizamos errores a JSON limpio
        if ($e instanceof HttpException) {
            return new JsonResponse([
                'error' => $e->getTitle(),
                'message' => $e->getMessage(),
            ], $e->getCode());
        }

        if ($e instanceof UpstreamException) {
            return new JsonResponse([
                'error' => 'Bad Gateway',
                'message' => $e->getMessage(),
            ], 502);
        }

        return new JsonResponse([
            'error' => 'Internal Server Error',
            'message' => 'Unexpected error.',
        ], 500);
    }
}
