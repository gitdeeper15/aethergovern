"""
AetherGovern — Core data models (v2.0.0).

This module defines the ten entities of AetherGovern v2.0.0:

    1. Agent                    — actor identity
    2. Action                   — operation (commit, merge, delete, deploy, rotate_key)
    3. Resource                 — target (branch, path, key)
    4. DelegationCertificate    — signed grant of scope
    5. RevocationRecord         — signed withdrawal of a certificate
    6. Policy                   — rule that governs authorization
    7. RevocationFrontier       — set of revocation records an actor has seen
    8. AuthorityChain           — sequence of certificates from root to leaf
    9. Dispute                  — conflict between two authority claims
   10. AccountabilityRecord     — after-the-fact trace of an admitted action

Reference:
    Baladi, S. (2026). AetherGovern: A Falsification-First Investigation
    of Governance in the Aether Family. Zenodo.
    https://doi.org/10.5281/zenodo.24054524

    v2.0.0 Specification, docs/specification/01_entities.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, List, Optional, Tuple


# =============================================================================
# Enums
# =============================================================================

class AgentStatus(str, Enum):
    """Status of an agent."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"


class ActionKind(str, Enum):
    """Kind of action an agent may perform."""
    COMMIT = "commit"
    MERGE = "merge"
    DELETE = "delete"
    DEPLOY = "deploy"
    ROTATE_KEY = "rotate_key"


class ResourceKind(str, Enum):
    """Kind of resource an action targets."""
    BRANCH = "branch"
    PATH = "path"
    KEY = "key"


class PolicyStatus(str, Enum):
    """Status of a policy."""
    PROPOSED = "proposed"
    APPROVED = "approved"
    ENFORCED = "enforced"
    REVOKED = "revoked"


class DisputeResolution(str, Enum):
    """Resolution status of a dispute."""
    PENDING = "pending"
    RESOLVED_BY_RULE = "resolved_by_rule"
    ESCALATED = "escalated"


class PolicyVerdict(str, Enum):
    """Verdict of a policy evaluation."""
    ALLOW = "allow"
    DENY = "deny"
    QUARANTINE = "quarantine"


# =============================================================================
# Type aliases
# =============================================================================

Scope = FrozenSet[Tuple[str, str]]
"""A scope is a frozen set of (action_kind, resource_id) pairs."""


# =============================================================================
# Entity 1 — Agent
# =============================================================================

@dataclass(frozen=True)
class Agent:
    """
    An autonomous software actor.

    Invariants:
        I1.1 — Key uniqueness (enforced by the registry, not the entity)
        I1.2 — Status monotonicity (enforced by the state machine)
        I1.3 — Registration completeness (enforced by the admission layer)
    """
    agent_id: str
    public_key: bytes
    key_id: str
    role: Optional[str]
    registered_at: str
    status: AgentStatus = AgentStatus.ACTIVE


# =============================================================================
# Entity 2 — Action
# =============================================================================

@dataclass(frozen=True)
class Action:
    """
    An operation by an agent on a resource.

    Invariants:
        I2.1 — Causal citation (enforced by the admission layer)
        I2.2 — Content addressing (enforced by the constructor)
        I2.3 — Signature covers content (enforced by the signature layer)
        I2.4 — Chain completeness (enforced by the admission layer)
    """
    action_id: str
    kind: ActionKind
    actor: str
    resource: str
    payload: Dict
    timestamp: str
    frontier_ref: str
    policy_ref: str
    authority_chain: List[str]
    signature: bytes = b""


# =============================================================================
# Entity 3 — Resource
# =============================================================================

@dataclass(frozen=True)
class Resource:
    """
    The target of an action.

    Invariants:
        I3.1 — Identifier stability (enforced by frozen dataclass)
        I3.2 — Kind immutability (enforced by frozen dataclass)
    """
    resource_id: str
    kind: ResourceKind
    owner: str
    metadata: Dict = field(default_factory=dict)


# =============================================================================
# Entity 4 — DelegationCertificate
# =============================================================================

@dataclass(frozen=True)
class DelegationCertificate:
    """
    A signed grant of scope from an issuer to a subject.

    Invariants:
        I4.1 — Attenuation (enforced by the delegate operation)
        I4.2 — Root recognition (enforced by the check operation)
        I4.3 — Expiry (enforced by the check operation)
        I4.4 — Signature covers content (enforced by the signature layer)
        I4.5 — No cycle (enforced by the parent_ref chain)
    """
    certificate_id: str
    issuer: str
    subject: str
    scope: Scope
    constraints: Dict
    expiry: str
    parent_ref: Optional[str]
    signature: bytes = b""


# =============================================================================
# Entity 5 — RevocationRecord
# =============================================================================

@dataclass(frozen=True)
class RevocationRecord:
    """
    A signed withdrawal of a certificate.

    Invariants:
        I5.1 — Monotonicity (enforced by the frontier)
        I5.2 — Signature covers content (enforced by the signature layer)
        I5.3 — Issuer authority (enforced by the revoke operation)
    """
    revocation_id: str
    certificate_ref: str
    issuer: str
    reason: str
    timestamp: str
    signature: bytes = b""


# =============================================================================
# Entity 6 — Policy
# =============================================================================

@dataclass(frozen=True)
class Rule:
    """A single policy rule."""
    action_kind: str
    resource_pattern: str
    verdict: PolicyVerdict


@dataclass(frozen=True)
class Policy:
    """
    A rule that governs authorization.

    Invariants:
        I6.1 — Version monotonicity (enforced by the policy registry)
        I6.2 — Approval completeness (enforced by the apply_policy operation)
        I6.3 — Effective date (enforced by the apply_policy operation)
        I6.4 — Supersession chain (enforced by the policy registry)
    """
    policy_id: str
    version: int
    rules: List[Rule]
    approval_chain: List[str]
    status: PolicyStatus
    created_at: str
    effective_from: str
    supersedes: Optional[str] = None


# =============================================================================
# Entity 7 — RevocationFrontier
# =============================================================================

@dataclass(frozen=True)
class RevocationFrontier:
    """
    The set of revocation records an actor has seen.

    Invariants:
        I7.1 — Grow-only (enforced by the frontier operations)
        I7.2 — Join is union (enforced by the join method)
        I7.3 — Content addressing (enforced by the constructor)
    """
    frontier_id: str
    revocations: FrozenSet[str]
    created_at: str

    def join(self, other: "RevocationFrontier") -> "RevocationFrontier":
        """Join two frontiers: set union of revocations."""
        return RevocationFrontier(
            frontier_id=f"{self.frontier_id}+{other.frontier_id}",
            revocations=self.revocations | other.revocations,
            created_at=self.created_at,
        )

    def __le__(self, other: "RevocationFrontier") -> bool:
        """Partial order: self ≤ other iff self.revocations ⊆ other.revocations."""
        return self.revocations <= other.revocations


# =============================================================================
# Entity 8 — AuthorityChain
# =============================================================================

@dataclass(frozen=True)
class AuthorityChain:
    """
    A sequence of delegation certificates from a root to a leaf agent.

    Invariants:
        I8.1 — Attenuation preserved (enforced by the check operation)
        I8.2 — Root recognized (enforced by the check operation)
        I8.3 — No cycle (enforced by the certificate chain)
        I8.4 — Contiguity (enforced by the check operation)
    """
    chain_id: str
    certificates: List[str]
    leaf_agent: str
    leaf_scope: Scope


# =============================================================================
# Entity 9 — Dispute
# =============================================================================

@dataclass(frozen=True)
class Dispute:
    """
    A conflict between two authority claims.

    Invariants:
        I9.1 — Determinism (enforced by the escalate operation)
        I9.2 — Escalation completeness (enforced by the escalate operation)
        I9.3 — No silent resolution (enforced by the escalate operation)
    """
    dispute_id: str
    claim_a: AuthorityChain
    claim_b: AuthorityChain
    precedence_rule: Optional[str]
    resolution: DisputeResolution
    escalation_record: Optional[Dict] = None
    created_at: str = ""


# =============================================================================
# Entity 10 — AccountabilityRecord
# =============================================================================

@dataclass(frozen=True)
class AccountabilityRecord:
    """
    The after-the-fact trace of an admitted action.

    Invariants:
        I10.1 — Immutability (enforced by frozen dataclass)
        I10.2 — Hash-link integrity (enforced by the record chain)
        I10.3 — Attribution completeness (enforced by the admission layer)
        I10.4 — Signature covers content (enforced by the signature layer)
    """
    record_id: str
    action_ref: str
    authority_chain_ref: str
    admitted_at: str
    admitted_by: str
    prev_record_hash: str
    signature: bytes = b""
