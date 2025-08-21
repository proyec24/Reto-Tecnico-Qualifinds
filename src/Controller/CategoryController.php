<?php
declare(strict_types=1);

namespace App\Controller;

use App\Http\JsonResponse;
use App\Http\Request;
use App\Service\CategoryService;

final class CategoryController
{
    public function __construct(private readonly CategoryService $categories) {}

    public function index(Request $req): JsonResponse
    {
        return new JsonResponse($this->categories->all());
    }
}
