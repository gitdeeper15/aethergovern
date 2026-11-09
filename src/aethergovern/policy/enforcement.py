"""
AetherGovern — Policy enforcement (Layer 2, v2.0.0).

Implements:
    - policy_hash: content-addressed hash of a policy
    - apply_policy: evaluate an action against a policy

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0, docs/specification/02_operations.md,
    Operation 5 (apply_policy).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import List

from aethergovern.models import (
    Action,
    Policy,
    PolicyStatus,
    PolicyVerdict,
    Rule,
)


# =============================================================================
# policy_hash
# =============================================================================

def policy_hash(policy: Policy) -> str:
    """
    Compute the content-addressed hash of a policy.

    The hash covers all fields that affect the verdict:
        policy_id, version, rules, approval_chain, status,
        created_at, effective_from, supersedes.
    """
    canonical = {
        "policy_id": policy.policy_id,
        "version": policy.version,
        "rules": [
            {
                "action_kind": r.action_kind,
                "resource_pattern": r.resource_pattern,
                "verdict": r.verdict.value,
            }
            for r in policy.rules
        ],
        "approval_chain": sorted(policy.approval_chain),
        "status": policy.status.value,
        "created_at": policy.created_at,
        "effective_from": policy.effective_from,
        "supersedes": policy.supersedes,
    }
    return hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


# =============================================================================
# Time helpers
# =============================================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(timestamp: str) -> datetime:
    dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _is_effective(effective_from: str, at: str) -> bool:
    """Return True iff effective_from <= at."""
    try:
        return _parse_iso(effective_from) <= _parse_iso(at)
    except ValueError:
        return False


# =============================================================================
# Rule matching
# =============================================================================

def _matches_rule(rule: Rule, action: Action) -> bool:
    """
    Check whether a rule matches an action.

    Matching is on:
        - action kind (exact string match)
        - resource pattern (glob-like: "branch/main" matches "branch/main",
          "branch/*" matches "branch/main", "*" matches anything)
    """
    if rule.action_kind != action.kind.value:
        return False

    pattern = rule.resource_pattern
    resource = action.resource

    # Simple pattern matching: "*" matches anything, "prefix/*" matches prefix/,
    # otherwise exact match.
    if pattern == "*":
        return True
    if pattern.endswith("/*"):
        prefix = pattern[:-2]
        return resource == prefix or resource.startswith(prefix + "/")
    return resource == pattern


# =============================================================================
# apply_policy
# =============================================================================

def apply_policy(action: Action, policy: Policy) -> PolicyVerdict:
    """
    Evaluate an action against a policy.

    Preconditions:
        - policy.status == ENFORCED
        - policy.effective_from <= action.timestamp
        - action.policy_ref == policy_hash(policy)

    Returns:
        PolicyVerdict (ALLOW, DENY, or QUARANTINE).

    Raises:
        ValueError if preconditions are violated.
    """
    # I6.2 — approval completeness
    if policy.status != PolicyStatus.ENFORCED:
        raise ValueError(
            f"policy {policy.policy_id} is not enforced "
            f"(status={policy.status.value})"
        )

    # I6.3 — effective date
    if not _is_effective(policy.effective_from, action.timestamp):
        raise ValueError(
            f"policy {policy.policy_id} is not yet effective "
            f"(effective_from={policy.effective_from}, action_at={action.timestamp})"
        )

    # I6.1 — version monotonicity (the action must cite this policy version)
    expected_hash = policy_hash(policy)
    if action.policy_ref != expected_hash:
        raise ValueError(
            f"action's policy_ref does not match policy hash "
            f"(expected={expected_hash[:16]}..., got={action.policy_ref[:16]}...)"
        )

    # Evaluate rules in order; first match wins.
    for rule in policy.rules:
        if _matches_rule(rule, action):
            return rule.verdict

    # Default deny (no rule matched).
    return PolicyVerdict.DENY
