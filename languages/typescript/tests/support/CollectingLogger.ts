import type { RapLogger } from '../../runtime/src/index';

export interface LogLine {
    readonly level: 'error' | 'warn' | 'info' | 'debug';
    readonly message: string;
    readonly context: Record<string, unknown> | undefined;
}

/**
 * Captures every log line the runtime emits, for the ADR-SDK-020 log-capture
 * assertions: the full material (messages AND context values, all levels) is scanned
 * for sensitive content.
 */
export class CollectingLogger implements RapLogger {
    readonly lines: LogLine[] = [];

    error(message: string, context?: Record<string, unknown>): void {
        this.lines.push({ level: 'error', message, context });
    }

    warn(message: string, context?: Record<string, unknown>): void {
        this.lines.push({ level: 'warn', message, context });
    }

    info(message: string, context?: Record<string, unknown>): void {
        this.lines.push({ level: 'info', message, context });
    }

    debug(message: string, context?: Record<string, unknown>): void {
        this.lines.push({ level: 'debug', message, context });
    }

    /** Everything logged, flattened to one scannable string (messages + context values). */
    all(): string {
        return this.lines.map((line) => `${line.level} ${line.message} ${JSON.stringify(line.context)}`).join('\n');
    }

    ofLevel(level: LogLine['level']): LogLine[] {
        return this.lines.filter((line) => line.level === level);
    }
}
