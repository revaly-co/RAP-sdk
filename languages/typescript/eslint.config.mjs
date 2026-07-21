/**
 * ESLint flat config for the HAND-WRITTEN surfaces only: runtime/src, tests, smoke
 * (ADR-SDK-028). `core/` is generator output (repo rule 1) and is NEVER linted — it is
 * globally ignored below and must stay that way; unused-code hygiene for the runtime
 * lives here precisely so the shared tsconfig never needs noUnusedLocals (which would
 * flag the generated core).
 *
 * Typed linting (typescript-eslint recommendedTypeChecked) needs the JS-API TypeScript
 * line (6.0.x), while this package pins the native tsc (typescript 7.x, no JS compiler
 * API) for `npm run typecheck` — typescript-eslint's peer range (`>=4.8.4 <6.1.0`)
 * cannot resolve against it in one npm root. The lint toolchain therefore lives in
 * ./lint with its own lockfile (same pattern as pipeline/typescript/compile-check),
 * and this config loads the plugins from there via createRequire.
 */
import { createRequire } from 'node:module';

const requireLint = createRequire(new URL('./lint/package.json', import.meta.url));
const eslintJs = requireLint('@eslint/js');
const tseslint = requireLint('typescript-eslint');

export default tseslint.config(
    {
        ignores: [
            // Generated core — never linted (repo rule 1; ADR-SDK-001).
            'core/**',
            'dist/**',
            'lint/**',
            'node_modules/**',
            // Out of the ADR-SDK-028 lint scope (runtime/src, tests, smoke).
            'eslint.config.mjs',
            'vitest.config.ts',
            'vitest.smoke.config.ts',
        ],
    },
    {
        files: ['runtime/src/**/*.ts', 'tests/**/*.ts', 'smoke/**/*.ts'],
        extends: [eslintJs.configs.recommended, ...tseslint.configs.recommendedTypeChecked],
        languageOptions: {
            parserOptions: {
                // Typed linting against the same tsconfig `npm run typecheck` uses.
                project: './tsconfig.json',
                tsconfigRootDir: import.meta.dirname,
            },
        },
        rules: {
            // Not in recommendedTypeChecked — required explicitly by ADR-SDK-028.
            '@typescript-eslint/consistent-type-imports': 'error',
        },
    },
);
