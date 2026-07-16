package co.revaly.sdk.transport;

import java.util.Locale;

/**
 * Builds the adoption-telemetry User-Agent per the ADR-SDK-005 normative grammar: {@code
 * revaly-sdk-java/<semver> (OpenJDK <feature>; <os>)}. The exact string is a contract with platform
 * dashboards; it carries only the coarse tokens below — no hostnames, no distro fingerprints.
 */
public final class RapUserAgent {

    /** The fixed lowercase language token (ADR-SDK-005 grammar). */
    public static final String PRODUCT_NAME = "revaly-sdk-java";

    /** The package semver, no {@code v} prefix (stage 5 stamps release versions). */
    public static final String SEMVER = resolveSemver();

    /**
     * Coarse runtime identifier, e.g. {@code OpenJDK 21} (the ADR's example token for java — the
     * feature release only, vendor-agnostic by convention).
     */
    public static final String RUNTIME_VERSION = "OpenJDK " + Runtime.version().feature();

    /** Coarse platform token: {@code linux} / {@code windows} / {@code darwin} / {@code other}. */
    public static final String OS = resolveOs();

    /** The full header value, e.g. {@code revaly-sdk-java/1.2.0 (OpenJDK 21; linux)}. */
    public static final String VALUE =
            PRODUCT_NAME + "/" + SEMVER + " (" + RUNTIME_VERSION + "; " + OS + ")";

    private RapUserAgent() {}

    private static String resolveSemver() {
        // Implementation-Version is stamped into the jar manifest at release (stage 5);
        // classes-dir runs (tests, IDEs) fall back to the placeholder.
        String version =
                RapUserAgent.class.getPackage() == null
                        ? null
                        : RapUserAgent.class.getPackage().getImplementationVersion();
        if (version == null || version.trim().isEmpty()) {
            return "0.0.0";
        }
        // Strip build metadata (+sha) — the ADR grammar carries the bare semver.
        int plus = version.indexOf('+');
        return plus > 0 ? version.substring(0, plus) : version;
    }

    private static String resolveOs() {
        String name = System.getProperty("os.name", "").toLowerCase(Locale.ROOT);
        if (name.contains("win")) {
            return "windows";
        }
        if (name.contains("linux")) {
            return "linux";
        }
        if (name.contains("mac") || name.contains("darwin")) {
            return "darwin";
        }
        return "other";
    }
}
