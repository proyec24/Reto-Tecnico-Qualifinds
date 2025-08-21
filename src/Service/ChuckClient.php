<?php
declare(strict_types=1);

namespace App\Service;

use App\Exception\UpstreamException;

final class ChuckClient
{
    public function __construct(
        private readonly string $baseUrl,
        private readonly int $timeoutSeconds = 5
    ) {}

    /** @return array<mixed> */
    public function get(string $path, array $query = []): array
    {
        $url = rtrim($this->baseUrl, '/') . $path;
        if ($query) {
            $url .= '?' . http_build_query($query);
        }

        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_CONNECTTIMEOUT => $this->timeoutSeconds,
            CURLOPT_TIMEOUT => $this->timeoutSeconds,
            CURLOPT_HTTPHEADER => ['Accept: application/json'],
            CURLOPT_USERAGENT => 'ChuckNorris-Backend-Exercise/1.0'
        ]);

        $body = curl_exec($ch);
        $errno = curl_errno($ch);
        $error = curl_error($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($errno !== 0) {
            throw new UpstreamException("Network error: $error");
        }
        if ($status < 200 || $status >= 300) {
            throw new UpstreamException("Upstream HTTP $status");
        }

        $decoded = json_decode((string)$body, true);
        if (!is_array($decoded)) {
            throw new UpstreamException('Invalid JSON from upstream');
        }
        return $decoded;
    }

    /** @return string[] */
    public function categories(): array
    {
        $data = $this->get('/jokes/categories');
        return array_values(array_map('strval', $data));
    }

    /** @return array{id:string,url:string,value:string,categories?:array} */
    public function randomByCategory(string $category): array
    {
        /** @var array{id:string,url:string,value:string,categories?:array} */
        return $this->get('/jokes/random', ['category' => $category]);
    }

    /** @return array{total:int,result:array<int,array>} */
    public function search(string $term): array
    {
        /** @var array{total:int,result:array<int,array>} */
        return $this->get('/jokes/search', ['query' => $term]);
    }
}
