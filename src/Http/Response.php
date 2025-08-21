<?php
declare(strict_types=1);

namespace App\Http;

class Response
{
    public function __construct(
        protected string $body,
        protected int $status = 200,
        protected array $headers = []
    ) {}

    public function send(): void
    {
        http_response_code($this->status);
        foreach ($this->headers as $k => $v) {
            header($k . ': ' . $v);
        }
        echo $this->body;
    }
}
