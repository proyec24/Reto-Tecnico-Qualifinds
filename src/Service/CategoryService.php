<?php
declare(strict_types=1);

namespace App\Service;

final class CategoryService
{
    /** @var string[]|null */
    private ?array $cache = null;

    public function __construct(private readonly ChuckClient $client) {}

    /** @return string[] */
    public function all(): array
    {
        if ($this->cache !== null) return $this->cache;
        $cats = $this->client->categories();
        sort($cats, SORT_NATURAL | SORT_FLAG_CASE);
        return $this->cache = $cats;
    }

    public function exists(string $category): bool
    {
        $catLower = strtolower($category);
        foreach ($this->all() as $c) {
            if (strtolower($c) === $catLower) return true;
        }
        return false;
    }
}
