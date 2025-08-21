<?php
declare(strict_types=1);

namespace App\Controller;

use App\Exception\HttpException;
use App\Http\JsonResponse;
use App\Http\Request;
use App\Service\CategoryService;
use App\Service\ChuckClient;

final class JokeController
{
    public function __construct(
        private readonly ChuckClient $client,
        private readonly CategoryService $categories
    ) {}

    public function show(Request $req, array $params): JsonResponse
    {
        $category = (string)($params['category'] ?? '');

        if ($category === '' || !$this->categories->exists($category)) {
            throw HttpException::badRequest('Invalid category. See valid_categories for options.');
        }

        $joke = $this->client->randomByCategory($category);

        return new JsonResponse([
            'id'       => (string)($joke['id'] ?? ''),
            'url'      => (string)($joke['url'] ?? ''),
            'category' => $category,
            'value'    => (string)($joke['value'] ?? '')
        ]);
    }
}
