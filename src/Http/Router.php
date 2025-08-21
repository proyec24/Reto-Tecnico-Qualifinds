<?php
declare(strict_types=1);

namespace App\Http;

use App\Exception\HttpException;

final class Router
{
    /** @var array<array{method:string, pattern:string, regex: string, vars: string[], handler: callable}> */
    private array $routes = [];

    public function get(string $pattern, callable $handler): void
    {
        $this->add('GET', $pattern, $handler);
    }

    private function add(string $method, string $pattern, callable $handler): void
    {
        // Convierte /joke/{category} a regex con captura
        $vars = [];
        $regex = preg_replace_callback('#\{([a-zA-Z_][a-zA-Z0-9_]*)\}#', function ($m) use (&$vars) {
            $vars[] = $m[1];
            return '([^/]+)';
        }, $pattern);
        $regex = '#^' . $regex . '$#';

        $this->routes[] = compact('method', 'pattern', 'regex', 'vars', 'handler');
    }

    public function dispatch(Request $request): Response
    {
        if ($request->method !== 'GET') {
            throw HttpException::methodNotAllowed('Only GET is supported.');
        }

        foreach ($this->routes as $r) {
            if ($r['method'] === $request->method && preg_match($r['regex'], $request->path, $m)) {
                array_shift($m);
                $params = array_combine($r['vars'], array_map('urldecode', $m)) ?: [];
                return ($r['handler'])(...[$request, $params]);
            }
        }
        throw HttpException::notFound('Route not found.');
    }
}
