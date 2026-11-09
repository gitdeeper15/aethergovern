"""
AetherGovern — Accountability records (Layer 3, v2.0.0).

Implements:
    - create_record: create an accountability record for an admitted action
    - compute_record_id: content-addressed id
    - verify_hash_link: verify the hash-link to the previous record
    - query_by_action: find all records for an action
    - canonical_record_bytes: serialization for signing

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0,
    docs/specification/02_operations.md and docs/specification/03_invariants.md.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List

from aethergovern.models import (
    AccountabilityRecord,
    Action,
)


# =============================================================================
# canonical_record_bytes
# =============================================================================

def canonical_record_bytes(record: AccountabilityRecord) -> bytes:
    """
    Serialize an accountability record to canonical bytes (excluding signature).
    """
    canonical = {
        "action_ref": record.action_ref,
        "authority_chain_ref": record.authority_chain_ref,
        "admitted_at": record.admitted_at,
        "admitted_by": record.admitted_by,
        "prev_record_hash": record.prev_record_hash,
    }
    return json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_record_id(record: AccountabilityRecord) -> str:
    """Compute the content-addressed record id."""
    return hashlib.sha256(canonical_record_bytes(record)).hexdigest()


# =============================================================================
# Time helpers
# =============================================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# =============================================================================
# create_record
# =============================================================================

def create_record(
    action: Action,
    authority_chain_ref: str,
    admitted_by: str,
    prev_record_hash: str,
) -> AccountabilityRecord:
    """
    Create an accountability record for an admitted action.

    Preconditions:
        - action.action_id is non-empty
        - authority_chain_ref is non-empty
        - admitted_by is non-empty
        - prev_record_hash is a 64-char hex string (or "0"*64 for the first)

    Postconditions:
        - record.action_ref == action.action_id
        - record.authority_chain_ref == authority_chain_ref
        - record.admitted_by == admitted_by
        - record.prev_record_hash == prev_record_hash
        - record.record_id == compute_record_id(record)

    Note: the record is created unsigned; signing is the caller's
    responsibility (via `accountability.sign`).
    """
    if not action.action_id:
        raise ValueError("action.action_id is empty")
    if not authority_chain_ref:
        raise ValueError("authority_chain_ref is empty")
    if not admitted_by:
        raise ValueError("admitted_by is empty")
    if len(prev_record_hash) != 64:
        raise ValueError(
            f"prev_record_hash must be 64 hex chars, got {len(prev_record_hash)}"
        )

    record = AccountabilityRecord(
        record_id="",  # placeholder
        action_ref=action.action_id,
        authority_chain_ref=authority_chain_ref,
        admitted_at=_now_iso(),
        admitted_by=admitted_by,
        prev_record_hash=prev_record_hash,
        signature=b"",
    )
    record_id = compute_record_id(record)
    return AccountabilityRecord(
        record_id=record_id,
        action_ref=action.action_id,
        authority_chain_ref=authority_chain_ref,
        admitted_at=record.admitted_at,
        admitted_by=admitted_by,
        prev_record_hash=prev_record_hash,
        signature=b"",
    )


# =============================================================================
# verify_hash_link
# =============================================================================

def verify_hash_link(
    record: AccountabilityRecord,
    previous: AccountabilityRecord,
) -> bool:
    """
    Verify that `record.prev_record_hash` equals `previous.record_id`.

    Invariants:
        I10.2 — Hash-link integrity.
    """
    return record.prev_record_hash == previous.record_id


# =============================================================================
# query_by_action
# =============================================================================

def query_by_action(
    records: List[AccountabilityRecord],
    action_id: str,
) -> List[AccountabilityRecord]:
    """
    Find all accountability records for a given action.

    Invariants:
        I10.3 — Attribution completeness: every admitted action must have
        at least one record; this function returns all records for the action.
    """
    return [r for r in records if r.action_ref == action_id]
