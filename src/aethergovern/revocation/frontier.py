"""
AetherGovern — Revocation frontier (Layer 4, v2.0.0).

The frontier tracks **revoked certificate ids**, not revocation record ids.
This is because `check` and `is_revoked` operate on certificate ids.

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0, docs/specification/02_operations.md,
    Operation 3 (revoke) and docs/specification/03_invariants.md (I5, I7).
"""

from __future__ import annotations

import hashlib
from typing import FrozenSet

from aethergovern.models import (
    RevocationFrontier,
    RevocationRecord,
)


def compute_frontier_id(certificate_ids: FrozenSet[str]) -> str:
    """Compute the content-addressed frontier id from sorted certificate ids."""
    sorted_ids = sorted(certificate_ids)
    canonical = "\n".join(sorted_ids).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def add_revocation(
    frontier: RevocationFrontier,
    record: RevocationRecord,
) -> RevocationFrontier:
    """
    Add a revocation record to a frontier.

    The frontier tracks the **certificate id** referenced by the record,
    not the record's own revocation_id.

    Invariants:
        I7.1 — Grow-only: the new frontier contains the old one.
    """
    new_set = frontier.revocations | {record.certificate_ref}
    return RevocationFrontier(
        frontier_id=compute_frontier_id(new_set),
        revocations=new_set,
        created_at=frontier.created_at,
    )


def join_frontiers(
    f1: RevocationFrontier,
    f2: RevocationFrontier,
) -> RevocationFrontier:
    """Join two frontiers (set union of revoked certificate ids)."""
    joined = f1.revocations | f2.revocations
    created_at = min(f1.created_at, f2.created_at)
    return RevocationFrontier(
        frontier_id=compute_frontier_id(joined),
        revocations=joined,
        created_at=created_at,
    )


def is_revoked(
    frontier: RevocationFrontier,
    certificate_id: str,
) -> bool:
    """
    Check whether a certificate is revoked at a frontier.

    Direct check only. Transitive revocation (a parent revoked ⇒ children
    invalid) is handled by the `check` operation.
    """
    return certificate_id in frontier.revocations
