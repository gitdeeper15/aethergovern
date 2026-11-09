"""
Tests for aethergovern.dispute — escalate.

Covers invariants:
    - I9.2 (escalation completeness)
    - I9.3 (no silent resolution)
"""

import pytest

from aethergovern.models import (
    AuthorityChain,
    Dispute,
    DisputeResolution,
    Scope,
)
from aethergovern.dispute.resolution import (
    escalate,
    resolve_by_rule,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def chain_a():
    """A sample authority chain."""
    return AuthorityChain(
        chain_id="chain-a",
        certificates=["cert-a-1", "cert-a-2"],
        leaf_agent="agent-a",
        leaf_scope=frozenset([("commit", "branch/main")]),
    )


@pytest.fixture
def chain_b():
    """A second sample authority chain."""
    return AuthorityChain(
        chain_id="chain-b",
        certificates=["cert-b-1", "cert-b-2"],
        leaf_agent="agent-b",
        leaf_scope=frozenset([("commit", "branch/main")]),
    )


@pytest.fixture
def pending_dispute(chain_a, chain_b):
    """A pending dispute between two chains."""
    return Dispute(
        dispute_id="dispute-001",
        claim_a=chain_a,
        claim_b=chain_b,
        precedence_rule=None,
        resolution=DisputeResolution.PENDING,
        escalation_record=None,
        created_at="2026-11-09T00:00:00Z",
    )


@pytest.fixture
def resolved_dispute(chain_a, chain_b):
    """A dispute resolved by rule."""
    return Dispute(
        dispute_id="dispute-002",
        claim_a=chain_a,
        claim_b=chain_b,
        precedence_rule="more_restrictive",
        resolution=DisputeResolution.RESOLVED_BY_RULE,
        escalation_record=None,
        created_at="2026-11-09T00:00:00Z",
    )


# =============================================================================
# escalate tests
# =============================================================================

class TestEscalate:
    def test_escalate_pending_dispute(self, pending_dispute):
        """A pending dispute can be escalated."""
        result = escalate(pending_dispute, reason="needs human review", escalation_target="human-review-001")
        assert result.resolution == DisputeResolution.ESCALATED
        assert result.escalation_record is not None

    def test_escalate_rejects_resolved(self, resolved_dispute):
        """I9.3 — A resolved dispute cannot be escalated."""
        with pytest.raises(ValueError, match="already resolved"):
            escalate(resolved_dispute, reason="cannot", escalation_target="human-review-001")

    def test_escalate_rejects_empty_target(self, pending_dispute):
        """I9.2 — An empty escalation target is rejected."""
        with pytest.raises(ValueError, match="empty escalation target"):
            escalate(pending_dispute, reason="needs review", escalation_target="")

    def test_escalate_records_reason(self, pending_dispute):
        """I9.2 — The escalation record contains the reason."""
        result = escalate(pending_dispute, reason="needs human review", escalation_target="human-review-001")
        assert result.escalation_record["reason"] == "needs human review"

    def test_escalate_records_target(self, pending_dispute):
        """I9.2 — The escalation record contains the target."""
        result = escalate(pending_dispute, reason="needs human review", escalation_target="human-review-001")
        assert result.escalation_record["escalation_target"] == "human-review-001"


# =============================================================================
# resolve_by_rule tests
# =============================================================================

class TestResolveByRule:
    def test_resolve_by_rule_deterministic(self, pending_dispute):
        """I9.1 — resolve_by_rule is deterministic."""
        r1 = resolve_by_rule(pending_dispute, rule="more_restrictive")
        r2 = resolve_by_rule(pending_dispute, rule="more_restrictive")
        assert r1.resolution == r2.resolution
        assert r1.precedence_rule == r2.precedence_rule

    def test_resolve_by_rule_rejects_already_resolved(self, resolved_dispute):
        """A resolved dispute cannot be resolved again."""
        with pytest.raises(ValueError, match="already resolved"):
            resolve_by_rule(resolved_dispute, rule="later_expiry")
