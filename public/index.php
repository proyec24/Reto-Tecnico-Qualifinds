<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';

use App\Bootstrap;
use App\Http\Request;

$kernel = new Bootstrap();
$router = $kernel->router();

$request = Request::fromGlobals();

try {
    $response = $router->dispatch($request);
} catch (Throwable $e) {
    $response = $kernel->handleException($e);
}

$response->send();
