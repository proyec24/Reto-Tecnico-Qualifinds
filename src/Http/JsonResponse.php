<?php
declare(strict_types=1);

namespace App\Http;

final class JsonResponse extends Response
{
    public function __construct(array $data, int $status = 200, array $headers = [])
    {
        $body = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        parent::__construct($body === false ? '{}' : $body, $status, $headers + [
            'Content-Type' => 'application/json; charset=utf-8'
        ]);
    }
}
