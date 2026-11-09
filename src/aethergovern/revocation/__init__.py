"""AetherGovern — Revocation module (Layer 4)."""

from aethergovern.revocation.frontier import (
    add_revocation,
    join_frontiers,
    is_revoked,
    compute_frontier_id,
)

__all__ = [
    "add_revocation",
    "join_frontiers",
    "is_revoked",
    "compute_frontier_id",
]
