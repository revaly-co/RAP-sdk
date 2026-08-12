import { defineConfig } from 'vitest/config';

export default defineConfig({
    test: {
        environment: 'node',
        include: ['tests/**/*.test.ts'],
        coverage: {
            provider: 'v8',
            // Hand-written runtime only. core/ is generator output (ADR-SDK-001) — it is
            // proven by the stage-2 regeneration diff and the stage-4 contract smoke, not
            // by unit coverage, and including it would bury the runtime's number.
            include: ['runtime/src/**/*.ts'],
            reporter: ['text-summary', 'json-summary'],
            reportsDirectory: './coverage',
        },
    },
});
