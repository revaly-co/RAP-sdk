package co.revaly.sdk;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

import co.revaly.sdk.errors.PermanentRejectionException;
import co.revaly.sdk.reconcile.RapReconcileVerdict;
import co.revaly.sdk.reconcile.RapTransactionOutcome;
import co.revaly.sdk.reconcile.ReconcilePolicy;
import co.revaly.sdk.testing.RapMockTransport;
import java.time.Duration;
import org.junit.jupiter.api.Test;

/** The failover-contract §3 reconciliation procedure — both V1 verdicts and the loop bounds. */
class ReconcileTests {

    private static ReconcilePolicy quickPolicy(int maxAttempts) {
        return new ReconcilePolicy(maxAttempts, Duration.ofSeconds(10), Duration.ofMillis(1));
    }

    @Test
    void foundApprovedMeansNoFailover() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).thenFoundApproved();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict verdict = client.reconcile(TestClient.MTX, quickPolicy(3));

        RapReconcileVerdict.Found found = (RapReconcileVerdict.Found) verdict;
        assertEquals(RapTransactionOutcome.APPROVED, found.getOutcome());
        assertNotNull(found.getTransaction());
        assertEquals(TestClient.MTX, found.getTransaction().getMerchantTransactionId());
        assertNotNull(found.getCorrelationId());
    }

    @Test
    void foundDeclinedIsTerminal() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).thenFoundDeclined();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        assertEquals(RapTransactionOutcome.DECLINED, found.getOutcome());
    }

    @Test
    void notFoundYetCarriesAttemptsElapsedStatusAndCorrelation() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).notFoundYet();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict verdict = client.reconcile(TestClient.MTX, quickPolicy(3));

        RapReconcileVerdict.NotFoundYet notFound = (RapReconcileVerdict.NotFoundYet) verdict;
        assertEquals(3, notFound.getAttempts());
        assertEquals(404, notFound.getLastHttpStatus());
        assertNotNull(notFound.getCorrelationId());
        assertTrue(notFound.getElapsed().toNanos() > 0);
    }

    @Test
    void notFoundThenFoundResolvesWithinOneCall() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).notFoundYet(2).thenFoundApproved();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(5));
        assertEquals(RapTransactionOutcome.APPROVED, found.getOutcome());
        assertEquals(3, mock.getRequests().size());
    }

    @Test
    void pendingIntentIsFoundPending() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).pending();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        assertEquals(RapTransactionOutcome.PENDING, found.getOutcome());
        assertNotNull(found.getPending());
        assertEquals(TestClient.MTX, found.getPending().getMerchantTransactionId());
        assertNull(found.getTransaction());
        assertEquals(
                1,
                mock.getRequests().size(),
                "pending returns immediately; re-poll is the caller's");
    }

    @Test
    void pendingThenTerminalAcrossTwoCalls() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).pending().thenFoundApproved();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found first =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(1));
        assertEquals(RapTransactionOutcome.PENDING, first.getOutcome());

        RapReconcileVerdict.Found second =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(1));
        assertEquals(RapTransactionOutcome.APPROVED, second.getOutcome());
    }

    @Test
    void degradedReadKeepsPollingWithinBudget() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).returnsServerError().thenFoundApproved();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        assertEquals(RapTransactionOutcome.APPROVED, found.getOutcome());
        assertEquals(2, mock.getRequests().size());
    }

    @Test
    void transportFailureOnTheReadKeepsPolling() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).throwsConnectionRefused().thenFoundApproved();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        assertEquals(RapTransactionOutcome.APPROVED, found.getOutcome());
    }

    @Test
    void rejectedReadEscapesInsteadOfPolling() {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).returnsPermanentRejection(401);
        RapClient client = TestClient.client(mock);

        assertThrows(
                PermanentRejectionException.class,
                () -> client.reconcile(TestClient.MTX, quickPolicy(5)));
        assertEquals(1, mock.getRequests().size(), "polling never fixes a rejected read");
    }

    @Test
    void groupedEnvelopeIsFoundButUnmapped() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).returnsTransactionGroup();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        // A sighting is a sighting: never keep polling past a visible record, and never
        // guess an outcome for a shape this SDK version cannot map.
        assertEquals(RapTransactionOutcome.UNKNOWN, found.getOutcome());
    }

    @Test
    void unmappedTransactionStatusIsFoundUnknown() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).returnsUnmappedStatus(99);
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict.Found found =
                (RapReconcileVerdict.Found) client.reconcile(TestClient.MTX, quickPolicy(3));
        assertEquals(RapTransactionOutcome.UNKNOWN, found.getOutcome());
        assertNotNull(found.getTransaction(), "the raw record still binds");
    }

    @Test
    void budgetBoundsTheLoopEvenWithAttemptsRemaining() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).notFoundYet();
        RapClient client = TestClient.client(mock);

        ReconcilePolicy policy =
                new ReconcilePolicy(100, Duration.ofMillis(30), Duration.ofMillis(200));
        RapReconcileVerdict.NotFoundYet notFound =
                (RapReconcileVerdict.NotFoundYet) client.reconcile(TestClient.MTX, policy);
        assertEquals(1, notFound.getAttempts(), "elapsed+delay >= budget stops the loop");
    }

    @Test
    void policyBoundsAreExplicitAndValidated() {
        assertThrows(
                IllegalArgumentException.class,
                () -> new ReconcilePolicy(0, Duration.ofSeconds(1), Duration.ZERO));
        assertThrows(
                IllegalArgumentException.class,
                () -> new ReconcilePolicy(1, Duration.ZERO, Duration.ZERO));
        assertThrows(
                IllegalArgumentException.class,
                () -> new ReconcilePolicy(1, Duration.ofSeconds(1), Duration.ofMillis(-1)));
    }

    @Test
    void builderRequiresEveryBoundExplicitly() {
        // The builder ships no defaults (SC-261): every bound a constructor requires must
        // be set, and build() rejects the omissions with the constructors' own validation.
        assertThrows(IllegalArgumentException.class, () -> ReconcilePolicy.builder().build());
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .overallBudget(Duration.ofSeconds(10))
                                .initialDelay(Duration.ofMillis(1))
                                .build());
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .maxAttempts(3)
                                .initialDelay(Duration.ofMillis(1))
                                .build());
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .maxAttempts(3)
                                .overallBudget(Duration.ofSeconds(10))
                                .build());
    }

    @Test
    void builderRejectsInvalidBoundsExactlyLikeTheConstructors() {
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .maxAttempts(0)
                                .overallBudget(Duration.ofSeconds(1))
                                .initialDelay(Duration.ZERO)
                                .build());
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .maxAttempts(1)
                                .overallBudget(Duration.ZERO)
                                .initialDelay(Duration.ZERO)
                                .build());
        assertThrows(
                IllegalArgumentException.class,
                () ->
                        ReconcilePolicy.builder()
                                .maxAttempts(1)
                                .overallBudget(Duration.ofSeconds(1))
                                .initialDelay(Duration.ofMillis(-1))
                                .build());
    }

    @Test
    void builderMatchesConstructorSemantics() {
        ReconcilePolicy built =
                ReconcilePolicy.builder()
                        .maxAttempts(6)
                        .overallBudget(Duration.ofSeconds(30))
                        .initialDelay(Duration.ofSeconds(1))
                        .build();
        assertEquals(6, built.getMaxAttempts());
        assertEquals(Duration.ofSeconds(30), built.getOverallBudget());
        assertEquals(Duration.ofSeconds(1), built.getInitialDelay());
        assertNull(built.getMaxDelay(), "unset maxDelay stays uncapped — the 3-arg ctor semantics");

        ReconcilePolicy capped =
                ReconcilePolicy.builder()
                        .maxAttempts(6)
                        .overallBudget(Duration.ofSeconds(30))
                        .initialDelay(Duration.ofSeconds(1))
                        .maxDelay(Duration.ofSeconds(5))
                        .build();
        assertEquals(Duration.ofSeconds(5), capped.getMaxDelay());
    }

    @Test
    void verdictBranchingAlwaysCarriesADefault() throws Exception {
        RapMockTransport mock = new RapMockTransport();
        mock.reconcile(TestClient.MTX).notFoundYet();
        RapClient client = TestClient.client(mock);

        RapReconcileVerdict verdict = client.reconcile(TestClient.MTX, quickPolicy(1));

        // The quickstart branching shape: instanceof chain WITH a default branch —
        // verdict types are open for extension (SafeToFailover arrives with P-2).
        if (verdict instanceof RapReconcileVerdict.Found) {
            fail("scripted NotFoundYet");
        } else if (verdict instanceof RapReconcileVerdict.NotFoundYet) {
            assertEquals(1, ((RapReconcileVerdict.NotFoundYet) verdict).getAttempts());
        } else {
            fail("default branch must exist for future verdicts — never remove it");
        }
    }
}
