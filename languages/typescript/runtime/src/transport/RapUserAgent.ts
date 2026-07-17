import { SDK_VERSION } from '../version';

/**
 * Builds the adoption-telemetry User-Agent per the ADR-SDK-005 normative grammar:
 * `revaly-sdk-typescript/<semver> (node <major.minor>; <os>)`. The exact string is a
 * contract with platform dashboards; it carries only the coarse tokens below — no
 * hostnames, no distro fingerprints. A merchant token may be APPENDED after the SDK
 * token (`userAgentSuffix`); the SDK prefix stays first and intact — it can never be
 * replaced or suppressed (enforced at transport level, where the core cannot bypass it).
 */

/** The fixed lowercase language token (ADR-SDK-005 grammar). */
export const PRODUCT_NAME = 'revaly-sdk-typescript';

/** The full header value, e.g. `revaly-sdk-typescript/1.2.0 (node 24.11; linux)`. */
export function userAgentValue(merchantSuffix?: string): string {
    let value = `${PRODUCT_NAME}/${SDK_VERSION} (${runtimeToken()}; ${osToken()})`;
    const suffix = merchantSuffix?.trim();
    if (suffix) {
        value += ` ${suffix}`;
    }
    return value;
}

/** Coarse runtime token: `node <major.minor>` on Node.js, `js` elsewhere. */
export function runtimeToken(): string {
    const nodeVersion = globalThis.process?.versions?.node;
    if (typeof nodeVersion === 'string') {
        const [major, minor] = nodeVersion.split('.');
        return `node ${major}.${minor ?? '0'}`;
    }
    return 'js';
}

/** Coarse platform token: `linux` / `windows` / `darwin` / `other`. */
export function osToken(): string {
    switch (globalThis.process?.platform) {
        case 'win32':
            return 'windows';
        case 'linux':
            return 'linux';
        case 'darwin':
            return 'darwin';
        default:
            return 'other';
    }
}
