<?php

declare(strict_types=1);

namespace Revaly\Sdk\Tests\Support;

use Psr\Log\AbstractLogger;

/** PSR-3 logger capturing every record for log-capture assertions (ADR-SDK-020). */
final class CollectingLogger extends AbstractLogger
{
    /** @var list<array{level: string, message: string, context: array<mixed>}> */
    public array $records = [];

    public function log($level, string|\Stringable $message, array $context = []): void
    {
        $this->records[] = [
            'level' => (string) $level,
            'message' => (string) $message,
            'context' => $context,
        ];
    }

    /** @return list<array{level: string, message: string, context: array<mixed>}> */
    public function atLevel(string $level): array
    {
        return array_values(array_filter($this->records, fn (array $r): bool => $r['level'] === $level));
    }

    /** Every message and context value flattened into one haystack string. */
    public function flattened(): string
    {
        $chunks = [];
        foreach ($this->records as $record) {
            $chunks[] = $record['message'];
            $chunks[] = json_encode($record['context']) ?: '';
        }

        return implode("\n", $chunks);
    }
}
