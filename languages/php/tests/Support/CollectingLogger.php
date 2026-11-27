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

    /**
     * Every message and context value flattened into one haystack string. json_encode renders
     * a Throwable as {} and other objects by their public properties only, so the context is
     * also walked and each value rendered as a handler might print it (see render()).
     */
    public function flattened(): string
    {
        $chunks = [];
        foreach ($this->records as $record) {
            $chunks[] = $record['message'];
            $chunks[] = json_encode($record['context']) ?: '';
            $chunks[] = self::render($record['context'], 0);
        }

        return implode("\n", $chunks);
    }

    /**
     * A context value as text. A Throwable (the PSR-3 'exception' key, or nested anywhere) gives
     * its class and message, then the same for each previous one, its trace string, and every
     * trace argument in full, since the trace string cuts string arguments to 15 bytes. An
     * object gives its class, its string form when it has one, and its JSON form.
     */
    private static function render(mixed $value, int $depth): string
    {
        if ($depth > 8) {
            return '';
        }
        if ($value instanceof \Throwable) {
            $chunks = [];
            for ($e = $value; $e !== null; $e = $e->getPrevious()) {
                $chunks[] = get_class($e) . ': ' . $e->getMessage();
                $chunks[] = $e->getTraceAsString();
                foreach ($e->getTrace() as $frame) {
                    foreach ($frame['args'] ?? [] as $argument) {
                        $chunks[] = self::render($argument, $depth + 1);
                    }
                }
            }

            return implode("\n", $chunks);
        }
        if (is_array($value)) {
            $chunks = [];
            foreach ($value as $key => $item) {
                $chunks[] = $key . '=' . self::render($item, $depth + 1);
            }

            return implode("\n", $chunks);
        }
        if (is_object($value)) {
            $text = $value instanceof \Stringable ? (string) $value : '';

            return get_class($value) . ' ' . $text . ' ' . (json_encode($value) ?: '');
        }

        return is_scalar($value) ? (string) $value : '';
    }
}
