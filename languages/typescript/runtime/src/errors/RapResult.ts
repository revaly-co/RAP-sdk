import { RapError } from './RapError';

/**
 * The discriminated-union result option of runtime-tdd §3: the same three-class
 * taxonomy, delivered as a value instead of a throw. Discriminate on `ok`, then on
 * `failure.kind` — and keep a default branch on the kind switch (the taxonomy is fixed
 * by contract, but defensive handling mirrors the open-verdict rule everywhere else in
 * this SDK).
 */
export type RapResult<T> =
    | { readonly ok: true; readonly value: T }
    | { readonly ok: false; readonly failure: RapError };

/**
 * Runs an SDK call and folds the three typed failure classes into a {@link RapResult}.
 * Only {@link RapError} is captured: caller cancellations (AbortError), request
 * validation errors and other programming errors rethrow unchanged — they are not
 * payment outcomes.
 *
 * ```ts
 * const result = await toRapResult(() => client.charge(request));
 * if (!result.ok) {
 *     switch (result.failure.kind) { ... }
 * }
 * ```
 */
export async function toRapResult<T>(operation: Promise<T> | (() => Promise<T>)): Promise<RapResult<T>> {
    try {
        const value = await (typeof operation === 'function' ? operation() : operation);
        return { ok: true, value };
    } catch (failure) {
        if (failure instanceof RapError) {
            return { ok: false, failure };
        }
        throw failure;
    }
}
