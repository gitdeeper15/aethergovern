"""
Tests for aethergovern.accountability — AccountabilityRecord.

Covers invariants:
    - I10.1 (immutability)
    - I10.2 (hash-link integrity)
    - I10.3 (attribution completeness)
    - I10.4 (signature covers content)
"""

import pytest

from aethergovern.models import (
    AccountabilityRecord,
    Action,
    ActionKind,
)
from aethergovern.accountability.records import (
    create_record,
    compute_record_id,
    verify_hash_link,
    query_by_action,
    canonical_record_bytes,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def action():
    """A sample action."""
    return Action(
        action_id="a" * 64,
        kind=ActionKind.COMMIT,
        actor="agent-001",
        resource="branch/main",
        payload={"diff": "abc"},
        timestamp="2026-11-09T00:00:00Z",
        frontier_ref="f" * 64,
        policy_ref="p" * 64,
        authority_chain=["c" * 64],
        signature=b"\x00" * 64,
    )


@pytest.fixture
def previous_record():
    """A previous record in the chain."""
    return AccountabilityRecord(
        record_id="r" * 64,
        action_ref="a" * 64,
        authority_chain_ref="c" * 64,
        admitted_at="2026-11-09T00:00:00Z",
        admitted_by="node-001",
        prev_record_hash="0" * 64,
        signature=b"\x00" * 64,
    )


# =============================================================================
# create_record tests
# =============================================================================

class TestCreateRecord:
    def test_create_record(self, action):
        """A record is created with the correct fields."""
        record = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash="0" * 64,
        )
        assert record.action_ref == action.action_id
        assert record.authority_chain_ref == "c" * 64
        assert record.admitted_by == "node-001"
        assert record.prev_record_hash == "0" * 64
        assert record.record_id == compute_record_id(record)

    def test_record_immutability(self, action):
        """I10.1 — A record is immutable after creation."""
        record = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash="0" * 64,
        )
        with pytest.raises(Exception):
            record.record_id = "different"  # frozen dataclass


# =============================================================================
# Hash-link tests
# =============================================================================

class TestHashLink:
    def test_hash_link_integrity(self, action, previous_record):
        """I10.2 — The prev_record_hash must match the previous record's id."""
        record = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash=previous_record.record_id,
        )
        assert verify_hash_link(record, previous_record) is True

    def test_record_chain(self, action):
        """A chain of records is correctly linked."""
        r1 = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash="0" * 64,
        )
        r2 = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash=r1.record_id,
        )
        assert verify_hash_link(r2, r1) is True


# =============================================================================
# Attribution tests
# =============================================================================

class TestAttribution:
    def test_attribution_completeness(self, action, previous_record):
        """I10.3 — Every admitted action has exactly one record."""
        record = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash=previous_record.record_id,
        )
        found = query_by_action([record], action.action_id)
        assert len(found) == 1
        assert found[0] == record

    def test_query_by_action_empty(self, action):
        """Querying a non-existent action returns an empty list."""
        found = query_by_action([], action.action_id)
        assert found == []


# =============================================================================
# Signature tests
# =============================================================================

class TestSignature:
    def test_signature_verifies(self, action, previous_record):
        """I10.4 — The signature covers the record id."""
        from aethergovern.authorization.certificates import generate_keypair
        priv, pub = generate_keypair()

        record = create_record(
            action=action,
            authority_chain_ref="c" * 64,
            admitted_by="node-001",
            prev_record_hash=previous_record.record_id,
        )
        canonical = canonical_record_bytes(record)
        signature = priv.sign(canonical)
        signed_record = AccountabilityRecord(
            record_id=record.record_id,
            action_ref=record.action_ref,
            authority_chain_ref=record.authority_chain_ref,
            admitted_at=record.admitted_at,
            admitted_by=record.admitted_by,
            prev_record_hash=record.prev_record_hash,
            signature=signature,
        )
        pub.verify(signed_record.signature, canonical)
