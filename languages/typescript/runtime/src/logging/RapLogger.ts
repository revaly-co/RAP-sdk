/**
 * The runtime's pluggable logging abstraction (runtime-tdd §6): console-compatible, so
 * `console` itself, pino/winston adapters, or any `{ warn, info, debug }` object plugs
 * in directly. Every line the runtime emits through this interface is VALUES-FREE at
 * info/warn level — operation, status, class and correlation id only; debug level
 * carries allowlist-scrubbed payloads (ADR-SDK-020). No logger configured = silent.
 */
export interface RapLogger {
    error?(message: string, context?: Record<string, unknown>): void;
    warn?(message: string, context?: Record<string, unknown>): void;
    info?(message: string, context?: Record<string, unknown>): void;
    debug?(message: string, context?: Record<string, unknown>): void;
}

/** @internal a never-throwing view over the configured logger */
export function loggerOrSilent(logger: RapLogger | undefined): Required<RapLogger> {
    const call = (level: keyof RapLogger) => (message: string, context?: Record<string, unknown>) => {
        try {
            logger?.[level]?.(message, context);
        } catch {
            // A throwing logger must never change payment control flow (runtime-tdd §6).
        }
    };
    return { error: call('error'), warn: call('warn'), info: call('info'), debug: call('debug') };
}
