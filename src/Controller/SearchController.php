<?php
declare(strict_types=1);

namespace App\Controller;

use App\Exception\HttpException;
use App\Http\JsonResponse;
use App\Http\Request;
use App\Service\ChuckClient;

final class SearchController
{
    public function __construct(private readonly ChuckClient $client) {}

    public function index(Request $req): JsonResponse
    {
        $q = trim((string)($req->query('query') ?? ''));
        if ($q === '') {
            throw HttpException::badRequest('Missing or empty "query" parameter.');
        }

        $payload = $this->client->search($q);
        $results = [];

        foreach ($payload['result'] ?? [] as $it) {
            $results[] = [
                'id'       => (string)($it['id'] ?? ''),
                'url'      => (string)($it['url'] ?? ''),
                'category' => isset($it['categories'][0]) ? (string)$it['categories'][0] : null,
                'value'    => (string)($it['value'] ?? '')
            ];
        }

        return new JsonResponse([
            'total'   => (int)($payload['total'] ?? count($results)),
            'results' => $results
        ]);
    }
}
