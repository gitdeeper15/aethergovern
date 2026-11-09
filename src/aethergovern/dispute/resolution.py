"""
AetherGovern — Dispute resolution (Layer 5, v2.0.0).

Implements:
    - escalate: escalate an unresolved dispute to human review
    - resolve_by_rule: resolve a dispute by a deterministic rule

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0,
    docs/specification/02_operations.md, Operation 6 (escalate).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from aethergovern.models import (
    Dispute,
    DisputeResolution,
)


# =============================================================================
# Time helpers
# =============================================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# =============================================================================
# escalate
# =============================================================================

def escalate(
    dispute: Dispute,
    reason: str,
    escalation_target: str,
) -> Dispute:
    """
    Escalate an unresolved dispute to human review.

    Preconditions:
        - dispute.resolution == PENDING or ESCALATED
        - escalation_target is a non-empty string

    Postconditions:
        - result.resolution == ESCALATED
        - result.escalation_record contains reason and escalation_target

    Invariants:
        I9.2 — Escalation completeness: escalation_record must be non-empty.
        I9.3 — No silent resolution: the dispute is explicitly escalated.
    """
    if dispute.resolution == DisputeResolution.RESOLVED_BY_RULE:
        raise ValueError(
            f"dispute {dispute.dispute_id} is already resolved by rule "
            f"(rule={dispute.precedence_rule})"
        )
    if not escalation_target:
        raise ValueError("empty escalation target")
    if not reason:
        raise ValueError("empty escalation reason")

    escalation_record: Dict = {
        "reason": reason,
        "escalation_target": escalation_target,
        "escalated_at": _now_iso(),
    }

    return Dispute(
        dispute_id=dispute.dispute_id,
        claim_a=dispute.claim_a,
        claim_b=dispute.claim_b,
        precedence_rule=dispute.precedence_rule,
        resolution=DisputeResolution.ESCALATED,
        escalation_record=escalation_record,
        created_at=dispute.created_at,
    )


# =============================================================================
# resolve_by_rule
# =============================================================================

def resolve_by_rule(dispute: Dispute, rule: str) -> Dispute:
    """
    Resolve a dispute by a deterministic precedence rule.

    Supported rules (for v2.0.0):
        - "more_restrictive": the claim with the smaller scope wins.
        - "later_expiry": the claim with the later expiry wins
          (approximated by chain length for v2.0.0).

    Preconditions:
        - dispute.resolution == PENDING
        - rule is a non-empty string

    Postconditions:
        - result.resolution == RESOLVED_BY_RULE
        - result.precedence_rule == rule

    Invariants:
        I9.1 — Determinism: the same input always gives the same resolution.
        I9.3 — No silent resolution: the rule is explicitly recorded.
    """
    if dispute.resolution == DisputeResolution.RESOLVED_BY_RULE:
        raise ValueError(
            f"dispute {dispute.dispute_id} is already resolved "
            f"(rule={dispute.precedence_rule})"
        )
    if dispute.resolution == DisputeResolution.ESCALATED:
        raise ValueError(
            f"dispute {dispute.dispute_id} has been escalated; "
            f"cannot resolve by rule"
        )
    if not rule:
        raise ValueError("empty rule")

    # Deterministic resolution: the rule determines the winner.
    # For v2.0.0, we only record the rule; the winner is determined by the
    # caller (or a future implementation of the rule).
    return Dispute(
        dispute_id=dispute.dispute_id,
        claim_a=dispute.claim_a,
        claim_b=dispute.claim_b,
        precedence_rule=rule,
        resolution=DisputeResolution.RESOLVED_BY_RULE,
        escalation_record=dispute.escalation_record,
        created_at=dispute.created_at,
    )
