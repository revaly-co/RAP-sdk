import { defineConfig } from 'vitest/config';

// Stage-4 contract smoke runner (ADR-SDK-024): a SEPARATE vitest config so the
// live suite can never leak into the stage-3 unit run (`npm test` includes
// tests/** only). Long timeouts: reconcile scenarios carry caller-bounded
// polling budgets.
export default defineConfig({
    test: {
        environment: 'node',
        include: ['smoke/**/*.smoke.ts'],
        testTimeout: 90_000,
        hookTimeout: 30_000,
    },
});
