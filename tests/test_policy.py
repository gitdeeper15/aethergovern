"""
Tests for aethergovern.policy.enforcement — apply_policy.

Covers invariants:
    - I6.1 (version monotonicity)
    - I6.2 (approval completeness)
    - I6.3 (effective date)
    - X1 (determinism)
"""

import pytest

from aethergovern.models import (
    Action,
    ActionKind,
    Policy,
    PolicyStatus,
    PolicyVerdict,
    Rule,
)
from aethergovern.policy.enforcement import apply_policy, policy_hash


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def approved_policy():
    """An enforced, effective policy with a single allow rule."""
    policy = Policy(
        policy_id="policy-001",
        version=1,
        rules=[
            Rule(action_kind="commit", resource_pattern="branch/main", verdict=PolicyVerdict.ALLOW),
            Rule(action_kind="merge", resource_pattern="branch/main", verdict=PolicyVerdict.ALLOW),
            Rule(action_kind="delete", resource_pattern="branch/main", verdict=PolicyVerdict.DENY),
        ],
        approval_chain=["agent-001"],
        status=PolicyStatus.ENFORCED,
        created_at="2026-11-01T00:00:00Z",
        effective_from="2026-11-01T00:00:00Z",
        supersedes=None,
    )
    return policy


@pytest.fixture
def action_commit(approved_policy):
    """An action that cites approved_policy."""
    return Action(
        action_id="a" * 64,
        kind=ActionKind.COMMIT,
        actor="agent-001",
        resource="branch/main",
        payload={"diff": "abc"},
        timestamp="2026-11-09T00:00:00Z",
        frontier_ref="f" * 64,
        policy_ref=policy_hash(approved_policy),
        authority_chain=["c" * 64],
        signature=b"\x00" * 64,
    )


# =============================================================================
# apply_policy tests
# =============================================================================

class TestApplyPolicy:
    def test_apply_policy_allow(self, action_commit, approved_policy):
        """A matching allow rule returns ALLOW."""
        verdict = apply_policy(action_commit, approved_policy)
        assert verdict == PolicyVerdict.ALLOW

    def test_apply_policy_deny(self, approved_policy):
        """A matching deny rule returns DENY."""
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.DELETE,
            actor="agent-001",
            resource="branch/main",
            payload={"target": "src/a.py"},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref=policy_hash(approved_policy),
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        verdict = apply_policy(action, approved_policy)
        assert verdict == PolicyVerdict.DENY

    def test_apply_policy_quarantine(self):
        """A matching quarantine rule returns QUARANTINE."""
        policy = Policy(
            policy_id="policy-quarantine",
            version=1,
            rules=[Rule("deploy", "branch/*", PolicyVerdict.QUARANTINE)],
            approval_chain=["agent-001"],
            status=PolicyStatus.ENFORCED,
            created_at="2026-11-01T00:00:00Z",
            effective_from="2026-11-01T00:00:00Z",
        )
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.DEPLOY,
            actor="agent-001",
            resource="branch/main",
            payload={},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref=policy_hash(policy),
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        verdict = apply_policy(action, policy)
        assert verdict == PolicyVerdict.QUARANTINE

    def test_apply_policy_default_deny(self):
        """No matching rule returns DENY."""
        policy = Policy(
            policy_id="policy-allow-commit",
            version=1,
            rules=[Rule("commit", "branch/main", PolicyVerdict.ALLOW)],
            approval_chain=["agent-001"],
            status=PolicyStatus.ENFORCED,
            created_at="2026-11-01T00:00:00Z",
            effective_from="2026-11-01T00:00:00Z",
        )
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.ROTATE_KEY,
            actor="agent-001",
            resource="key-1",
            payload={},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref=policy_hash(policy),
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        verdict = apply_policy(action, policy)
        assert verdict == PolicyVerdict.DENY

    def test_apply_policy_rejects_unenforced(self, action_commit):
        """I6.2 — An unenforced policy is rejected."""
        policy = Policy(
            policy_id="policy-unenforced",
            version=1,
            rules=[Rule("commit", "branch/main", PolicyVerdict.ALLOW)],
            approval_chain=[],
            status=PolicyStatus.PROPOSED,
            created_at="2026-11-01T00:00:00Z",
            effective_from="2026-11-01T00:00:00Z",
        )
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.COMMIT,
            actor="agent-001",
            resource="branch/main",
            payload={},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref=policy_hash(policy),
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        with pytest.raises(ValueError, match="not enforced"):
            apply_policy(action, policy)

    def test_apply_policy_rejects_ineffective(self):
        """I6.3 — A policy not yet effective is rejected."""
        policy = Policy(
            policy_id="policy-future",
            version=1,
            rules=[Rule("commit", "branch/main", PolicyVerdict.ALLOW)],
            approval_chain=["agent-001"],
            status=PolicyStatus.ENFORCED,
            created_at="2026-11-01T00:00:00Z",
            effective_from="2027-01-01T00:00:00Z",
        )
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.COMMIT,
            actor="agent-001",
            resource="branch/main",
            payload={},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref=policy_hash(policy),
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        with pytest.raises(ValueError, match="not yet effective"):
            apply_policy(action, policy)

    def test_apply_policy_rejects_mismatch(self, approved_policy):
        """I6.1 — An action citing a different policy is rejected."""
        action = Action(
            action_id="a" * 64,
            kind=ActionKind.COMMIT,
            actor="agent-001",
            resource="branch/main",
            payload={},
            timestamp="2026-11-09T00:00:00Z",
            frontier_ref="f" * 64,
            policy_ref="different-hash",
            authority_chain=["c" * 64],
            signature=b"\x00" * 64,
        )
        with pytest.raises(ValueError, match="does not match"):
            apply_policy(action, approved_policy)

    def test_apply_policy_deterministic(self, action_commit, approved_policy):
        """X1 — The same input always gives the same verdict."""
        v1 = apply_policy(action_commit, approved_policy)
        v2 = apply_policy(action_commit, approved_policy)
        v3 = apply_policy(action_commit, approved_policy)
        assert v1 == v2 == v3
