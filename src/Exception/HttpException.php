<?php
declare(strict_types=1);

namespace App\Exception;

final class HttpException extends \RuntimeException
{
    private string $title;

    private function __construct(int $status, string $title, string $message)
    {
        parent::__construct($message, $status);
        $this->title = $title;
    }

    public function getTitle(): string { return $this->title; }

    public static function badRequest(string $msg): self   { return new self(400, 'Bad Request', $msg); }
    public static function notFound(string $msg): self     { return new self(404, 'Not Found', $msg); }
    public static function methodNotAllowed(string $msg): self { return new self(405, 'Method Not Allowed', $msg); }
}
