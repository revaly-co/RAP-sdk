"""The central allowlist scrubber (ADR-SDK-020): only known-safe fields pass;
everything else scrubs; schema evolution fails safe."""

from __future__ import annotations

import json

from revaly_sdk import REDACTED, SCRUBBED, scrub_headers, scrub_json, scrub_value


def test_allowlisted_fields_pass_verbatim():
    scrubbed = json.loads(
        scrub_json(
            '{"transactionId": "txn_1", "merchantTransactionId": "mtx_1", "code": "not_processed",'
            ' "error": "boom", "currency": "USD", "transactionStatus": 1}'
        )
    )
    assert scrubbed == {
        "transactionId": "txn_1",
        "merchantTransactionId": "mtx_1",
        "code": "not_processed",
        "error": "boom",
        "currency": "USD",
        "transactionStatus": 1,
    }


def test_unknown_fields_scrub_fail_safe():
    scrubbed = json.loads(scrub_json('{"amount": 2500, "shinyNewField": "secret"}'))
    assert scrubbed == {"amount": SCRUBBED, "shinyNewField": SCRUBBED}


def test_card_fields_scrub():
    scrubbed = json.loads(
        scrub_json(
            '{"paymentMethod": {"creditCard": {"number": "4111111111111111",'
            ' "cardVerificationCode": "123"}, "firstName": "Synthetic"}}'
        )
    )
    card = scrubbed["paymentMethod"]["creditCard"]
    assert card["number"] == SCRUBBED
    assert card["cardVerificationCode"] == SCRUBBED
    assert scrubbed["paymentMethod"]["firstName"] == SCRUBBED


def test_structure_is_preserved():
    scrubbed = json.loads(scrub_json('{"a": {"b": [1, 2]}, "code": "x"}'))
    assert isinstance(scrubbed["a"], dict)
    assert isinstance(scrubbed["a"]["b"], list)
    assert scrubbed["code"] == "x"


def test_array_scalars_keep_parent_key_status():
    scrubbed = json.loads(scrub_json('{"attempts": [1, 2], "pans": ["4111"]}'))
    assert scrubbed["attempts"] == [1, 2]
    assert scrubbed["pans"] == [SCRUBBED]


def test_case_insensitive_field_match():
    scrubbed = json.loads(scrub_json('{"MerchantTransactionID": "mtx_1"}'))
    assert scrubbed["MerchantTransactionID"] == "mtx_1"


def test_non_json_input_never_leaks():
    assert scrub_json("PAN=4111111111111111") == "[unparseable:scrubbed]"


def test_empty_input_is_empty():
    assert scrub_json(None) == ""
    assert scrub_json("   ") == ""


def test_scrub_value_uses_model_to_json():
    from revaly_sdk_core.models.stored_credential import StoredCredential

    scrubbed = scrub_value(StoredCredential(reason_type="recurring"))
    assert json.loads(scrubbed) == {"reasonType": SCRUBBED}


def test_scrub_value_survives_unserializable_input():
    assert scrub_value(object()) == SCRUBBED


def test_headers_allowlist_and_redaction():
    scrubbed = scrub_headers(
        {
            "Authorization": "ApiKey sk_synthetic_secret",
            "User-Agent": "revaly-sdk-python/0.0.0",
            "X-Correlation-ID": "corr-1",
            "Content-Type": "application/json",
            "X-Internal-Routing": "edge-7",
        }
    )
    assert scrubbed["Authorization"] == REDACTED
    assert "sk_synthetic_secret" not in json.dumps(scrubbed)
    assert scrubbed["User-Agent"] == "revaly-sdk-python/0.0.0"
    assert scrubbed["X-Correlation-ID"] == "corr-1"
    assert scrubbed["X-Internal-Routing"] == REDACTED


def test_headers_multi_value_join():
    scrubbed = scrub_headers({"api-supported-versions": ["2.0", "2.1"], "User-Agent": ["a/1", "b/2"]})
    assert scrubbed["api-supported-versions"] == "2.0, 2.1"
    assert scrubbed["User-Agent"] == "a/1 b/2"


def test_headers_sorted_by_name():
    scrubbed = scrub_headers({"b-header": "1", "A-Header": "2"})
    assert list(scrubbed.keys()) == ["A-Header", "b-header"]
