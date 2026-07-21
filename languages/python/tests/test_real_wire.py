"""The real urllib3 wire against local socket servers: single-shot semantics
(ADR-SDK-004 — no hidden retries, no redirect re-POST) and the §2 taxonomy rows
that only a real socket can produce. No external network is touched except the
RFC 6761 ``.invalid`` DNS probe.
"""

from __future__ import annotations

import re
import socket
import struct
import threading
import time

import pytest
import urllib3.exceptions

from conftest import payment_request
from revaly_sdk import RapOutcomeUnknown, RapTransientFailure


class _SocketServer:
    """A per-connection handler server on an ephemeral loopback port."""

    def __init__(self, handler) -> None:
        self._handler = handler
        self._stop = threading.Event()
        self.hits = 0
        self.request_lines: list = []
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._srv.bind(("127.0.0.1", 0))
        self._srv.listen(8)
        self.port = self._srv.getsockname()[1]
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self._srv.settimeout(0.2)
                conn, _ = self._srv.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            self.hits += 1
            threading.Thread(target=self._dispatch, args=(conn,), daemon=True).start()

    def _dispatch(self, conn) -> None:
        try:
            head = _recv_full_request(conn)
            if head:
                self.request_lines.append(head.split(b"\r\n", 1)[0].decode(errors="replace"))
            self._handler(conn, head)
        except OSError:
            pass
        finally:
            try:
                conn.close()
            except OSError:
                pass

    def stop(self) -> None:
        self._stop.set()
        self._srv.close()


def _recv_full_request(conn) -> bytes:
    conn.settimeout(3)
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            return data
        data += chunk
    head, _, rest = data.partition(b"\r\n\r\n")
    match = re.search(rb"content-length:\s*(\d+)", head, re.I)
    want = int(match.group(1)) if match else 0
    while len(rest) < want:
        chunk = conn.recv(4096)
        if not chunk:
            break
        rest += chunk
    return head


def _respond(conn, payload: bytes) -> None:
    conn.sendall(payload)
    try:
        conn.shutdown(socket.SHUT_WR)
        conn.settimeout(1)
        while conn.recv(4096):
            pass
    except OSError:
        pass


@pytest.fixture
def server_factory():
    servers = []

    def start(handler) -> _SocketServer:
        server = _SocketServer(handler)
        servers.append(server)
        return server

    yield start
    for server in servers:
        server.stop()


def _real_client(port: int, **kwargs):
    from conftest import SYNTHETIC_API_KEY
    from revaly_sdk import RapClient

    return RapClient(SYNTHETIC_API_KEY, base_url=f"http://127.0.0.1:{port}", **kwargs)


def test_307_on_post_is_not_followed_and_not_resubmitted(server_factory):
    # urllib3's DEFAULT follows a 307 and re-sends the payment body (probed) —
    # a silent resubmission. The transport's retries=False turns the 3xx into a
    # plain response: OutcomeUnknown, exactly ONE server hit.
    def handler(conn, head):
        _respond(
            conn,
            b"HTTP/1.1 307 Temporary Redirect\r\nLocation: /target\r\n"
            b"Content-Length: 0\r\nConnection: close\r\n\r\n",
        )

    server = server_factory(handler)
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        _real_client(server.port).charge(payment_request())
    assert exc_info.value.status == 307
    assert server.hits == 1
    assert server.request_lines == ["POST /payments HTTP/1.1"]


def test_connection_reset_mid_body_is_outcome_unknown_single_shot(server_factory):
    # The body materializes INSIDE the transport request, so a mid-body reset
    # classifies there (urllib3 surfaces it at read() time — probed).
    def handler(conn, head):
        conn.sendall(
            b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
            b"Content-Length: 1000\r\n\r\n" + b"x" * 10
        )
        time.sleep(0.1)
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))

    server = server_factory(handler)
    with pytest.raises(RapOutcomeUnknown):
        _real_client(server.port).charge(payment_request())
    assert server.hits == 1


def test_deadline_after_send_is_outcome_unknown(server_factory):
    # §1: overall-deadline expiry AFTER send is OutcomeUnknown, never
    # TransientFailure.
    def handler(conn, head):
        time.sleep(3)

    server = server_factory(handler)
    started = time.monotonic()
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        _real_client(server.port, overall_deadline=0.5).charge(payment_request())
    assert time.monotonic() - started < 2.5
    assert isinstance(exc_info.value.__cause__, urllib3.exceptions.ReadTimeoutError)
    assert server.hits == 1


def test_tls_failure_bypasses_the_core_flatten_path(server_factory):
    # The core's rest.py collapses SSL failures into ApiException(status=0);
    # the runtime transport replaces that path and types it (conservatively
    # OutcomeUnknown — generic TLS errors carry no phase proof in urllib3).
    def handler(conn, head):
        _respond(conn, b"NOT TLS AT ALL\r\n\r\n")

    server = server_factory(handler)
    from conftest import SYNTHETIC_API_KEY
    from revaly_sdk import RapClient

    client = RapClient(SYNTHETIC_API_KEY, base_url=f"https://127.0.0.1:{server.port}")
    with pytest.raises(RapOutcomeUnknown) as exc_info:
        client.charge(payment_request())
    assert isinstance(exc_info.value.__cause__, urllib3.exceptions.SSLError)


def test_connection_refused_is_transient_failure():
    # Bind-then-close guarantees nothing is listening on the port.
    probe = socket.socket()
    probe.bind(("127.0.0.1", 0))
    refused_port = probe.getsockname()[1]
    probe.close()

    with pytest.raises(RapTransientFailure) as exc_info:
        _real_client(refused_port).charge(payment_request())
    assert isinstance(exc_info.value.__cause__, urllib3.exceptions.NewConnectionError)


def test_dns_failure_is_transient_failure():
    # RFC 6761: .invalid never resolves.
    from conftest import SYNTHETIC_API_KEY
    from revaly_sdk import RapClient

    client = RapClient(SYNTHETIC_API_KEY, base_url="http://rap-sdk-probe.invalid")
    with pytest.raises(RapTransientFailure) as exc_info:
        client.charge(payment_request())
    assert isinstance(exc_info.value.__cause__, urllib3.exceptions.NewConnectionError)


def test_connect_phase_timeout_is_transient_failure_when_provable():
    # Non-routable TEST-NET-ish target: the connect phase can time out or be
    # refused depending on the network — both are provably never-sent →
    # TransientFailure. If some environment actually routes the address, the
    # probe is inconclusive and skips rather than weakening the assertion.
    from conftest import SYNTHETIC_API_KEY
    from revaly_sdk import RapClient, RapError

    client = RapClient(
        SYNTHETIC_API_KEY,
        base_url="http://10.255.255.1:81",
        connect_timeout=0.4,
        overall_deadline=2.0,
    )
    try:
        client.charge(payment_request())
    except RapTransientFailure as failure:
        assert isinstance(failure.__cause__, urllib3.exceptions.ConnectTimeoutError)
        return
    except RapError:
        pytest.skip("environment routed the non-routable probe address")
    pytest.skip("environment accepted the non-routable probe address")
