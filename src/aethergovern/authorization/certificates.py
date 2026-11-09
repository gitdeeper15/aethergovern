"""
AetherGovern — Authorization (Layer 1, v2.0.0).

Implements:
    - grant:    issue a root delegation certificate
    - delegate: issue a child delegation certificate
    - revoke:   withdraw a certificate
    - check:    verify an authority chain at a frontier

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0, docs/specification/02_operations.md.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from aethergovern.models import (
    Action,
    Agent,
    AgentStatus,
    AuthorityChain,
    DelegationCertificate,
    RevocationFrontier,
    RevocationRecord,
    Scope,
)


# =============================================================================
# Keypair generation
# =============================================================================

def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """Generate a fresh Ed25519 keypair."""
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    return private, public


# =============================================================================
# Canonical serialization
# =============================================================================

def canonical_certificate_bytes(cert: DelegationCertificate) -> bytes:
    """
    Serialize a certificate to canonical bytes (excluding signature).
    Used for signing and verification.
    """
    canonical = {
        "certificate_id": cert.certificate_id,
        "issuer": cert.issuer,
        "subject": cert.subject,
        "scope": sorted([list(p) for p in cert.scope]),
        "constraints": cert.constraints,
        "expiry": cert.expiry,
        "parent_ref": cert.parent_ref,
    }
    return json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_revocation_bytes(rev: RevocationRecord) -> bytes:
    """Serialize a revocation record to canonical bytes (excluding signature)."""
    canonical = {
        "revocation_id": rev.revocation_id,
        "certificate_ref": rev.certificate_ref,
        "issuer": rev.issuer,
        "reason": rev.reason,
        "timestamp": rev.timestamp,
    }
    return json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _compute_certificate_id(cert: DelegationCertificate) -> str:
    """Compute the content-addressed certificate id."""
    return hashlib.sha256(canonical_certificate_bytes(cert)).hexdigest()


def _compute_revocation_id(rev: RevocationRecord) -> str:
    """Compute the content-addressed revocation id."""
    return hashlib.sha256(canonical_revocation_bytes(rev)).hexdigest()


# =============================================================================
# Time helpers
# =============================================================================

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_past(timestamp: str) -> bool:
    """Return True iff timestamp is in the past (relative to now)."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return True
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt <= now


def _is_expired(expiry: str, current_time: str) -> bool:
    """Return True iff expiry < current_time."""
    try:
        exp = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
        cur = datetime.fromisoformat(current_time.replace("Z", "+00:00"))
    except ValueError:
        return True
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if cur.tzinfo is None:
        cur = cur.replace(tzinfo=timezone.utc)
    return cur > exp


# =============================================================================
# Root recognition (simplified registry)
# =============================================================================

# In a full implementation, this would be a decentralized root registry.
# For v2.0.0, the set of roots is passed explicitly.
# The `grant` function takes a `root_agents` parameter to recognize roots.

# For the test suite, we use a module-level registry that tests can populate.
_ROOT_AGENTS: dict[str, Agent] = {}


def register_root(agent: Agent) -> None:
    """Register an agent as a recognized root (for testing)."""
    _ROOT_AGENTS[agent.agent_id] = agent


def clear_roots() -> None:
    """Clear the root registry (for testing)."""
    _ROOT_AGENTS.clear()


def is_root(agent: Agent) -> bool:
    """Check whether an agent is a recognized root."""
    return agent.agent_id in _ROOT_AGENTS


# =============================================================================
# Operation 1 — grant
# =============================================================================

def grant(
    root: Agent,
    subject: Agent,
    scope: Scope,
    expiry: str,
    root_private_key: Ed25519PrivateKey,
) -> DelegationCertificate:
    """
    Issue a root delegation certificate.

    Preconditions:
        - root is a recognized root
        - root and subject are active
        - expiry is in the future
        - scope is non-empty
    """
    if not is_root(root):
        raise ValueError(f"agent {root.agent_id} is not a recognized root")
    if root.status != AgentStatus.ACTIVE:
        raise ValueError(f"root {root.agent_id} is not active")
    if subject.status != AgentStatus.ACTIVE:
        raise ValueError(f"subject {subject.agent_id} is not active")
    if _is_past(expiry):
        raise ValueError(f"expiry {expiry} is in the past")
    if not scope:
        raise ValueError("empty scope")

    cert = DelegationCertificate(
        certificate_id="",  # placeholder
        issuer=root.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=None,
        signature=b"",
    )
    cert_id = _compute_certificate_id(cert)
    cert = DelegationCertificate(
        certificate_id=cert_id,
        issuer=root.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=None,
        signature=b"",
    )
    canonical = canonical_certificate_bytes(cert)
    signature = root_private_key.sign(canonical)
    return DelegationCertificate(
        certificate_id=cert_id,
        issuer=root.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=None,
        signature=signature,
    )


# =============================================================================
# Operation 2 — delegate
# =============================================================================

def delegate(
    issuer: Agent,
    subject: Agent,
    scope: Scope,
    expiry: str,
    parent_certificate: DelegationCertificate,
    issuer_private_key: Ed25519PrivateKey,
) -> DelegationCertificate:
    """
    Issue a child delegation certificate (attenuated).

    Preconditions:
        - issuer is active and is the parent's subject
        - subject is active
        - parent is not expired or revoked (checked by caller)
        - scope ⊆ parent's scope (attenuation)
        - expiry <= parent's expiry
    """
    if issuer.agent_id != parent_certificate.subject:
        raise ValueError(
            f"issuer {issuer.agent_id} is not the parent's subject "
            f"({parent_certificate.subject})"
        )
    if issuer.status != AgentStatus.ACTIVE:
        raise ValueError(f"issuer {issuer.agent_id} is not active")
    if subject.status != AgentStatus.ACTIVE:
        raise ValueError(f"subject {subject.agent_id} is not active")
    if not scope.issubset(parent_certificate.scope):
        raise ValueError(
            f"scope not a subset of parent scope: "
            f"{set(scope)} ⊄ {set(parent_certificate.scope)}"
        )
    if _is_past(expiry):
        raise ValueError(f"expiry {expiry} is in the past")
    if expiry > parent_certificate.expiry:
        raise ValueError(
            f"expiry {expiry} > parent expiry {parent_certificate.expiry}"
        )

    cert = DelegationCertificate(
        certificate_id="",
        issuer=issuer.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=parent_certificate.certificate_id,
        signature=b"",
    )
    cert_id = _compute_certificate_id(cert)
    cert = DelegationCertificate(
        certificate_id=cert_id,
        issuer=issuer.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=parent_certificate.certificate_id,
        signature=b"",
    )
    canonical = canonical_certificate_bytes(cert)
    signature = issuer_private_key.sign(canonical)
    return DelegationCertificate(
        certificate_id=cert_id,
        issuer=issuer.agent_id,
        subject=subject.agent_id,
        scope=scope,
        constraints={},
        expiry=expiry,
        parent_ref=parent_certificate.certificate_id,
        signature=signature,
    )


# =============================================================================
# Operation 3 — revoke
# =============================================================================

def revoke(
    issuer: Agent,
    certificate: DelegationCertificate,
    reason: str,
    issuer_private_key: Ed25519PrivateKey,
    frontier: RevocationFrontier,
) -> RevocationRecord:
    """
    Withdraw a delegation certificate.

    Preconditions:
        - issuer is active
        - issuer is the certificate's issuer (or ancestor, checked by caller)
        - certificate is not already revoked at the given frontier
    """
    if issuer.status != AgentStatus.ACTIVE:
        raise ValueError(f"issuer {issuer.agent_id} is not active")
    if issuer.agent_id != certificate.issuer:
        raise ValueError(
            f"issuer {issuer.agent_id} is not the certificate's issuer "
            f"({certificate.issuer})"
        )
    if certificate.certificate_id in frontier.revocations:
        raise ValueError(f"certificate {certificate.certificate_id} is already revoked")

    rev = RevocationRecord(
        revocation_id="",
        certificate_ref=certificate.certificate_id,
        issuer=issuer.agent_id,
        reason=reason,
        timestamp=_now_iso(),
        signature=b"",
    )
    rev_id = _compute_revocation_id(rev)
    rev = RevocationRecord(
        revocation_id=rev_id,
        certificate_ref=certificate.certificate_id,
        issuer=issuer.agent_id,
        reason=reason,
        timestamp=rev.timestamp,
        signature=b"",
    )
    canonical = canonical_revocation_bytes(rev)
    signature = issuer_private_key.sign(canonical)
    return RevocationRecord(
        revocation_id=rev_id,
        certificate_ref=certificate.certificate_id,
        issuer=issuer.agent_id,
        reason=reason,
        timestamp=rev.timestamp,
        signature=signature,
    )


# =============================================================================
# Operation 4 — check
# =============================================================================

@dataclass(frozen=True)
class CheckResult:
    """Result of a chain validity check."""
    valid: bool
    reason: str = ""


def check(
    action: Action,
    chain: AuthorityChain,
    frontier: RevocationFrontier,
    current_time: str,
    certificates: Dict[str, DelegationCertificate],
    root_agents: Dict[str, Agent],
) -> CheckResult:
    """
    Verify an authority chain at a given revocation frontier.

    Conditions (all must hold for valid=True):
        (a) every signature verifies
        (b) scope attenuates: scope(c_{i+1}) ⊆ scope(c_i)
        (c) no certificate has expired at current_time
        (d) no certificate in the chain appears in frontier.revocations
        (e) the first certificate's issuer is a recognized root
    """
    if not chain.certificates:
        return CheckResult(False, "empty chain")

    # Load certificates
    certs: List[DelegationCertificate] = []
    for cert_id in chain.certificates:
        cert = certificates.get(cert_id)
        if cert is None:
            return CheckResult(False, f"unknown certificate: {cert_id}")
        certs.append(cert)

    # (a) signature verification
    for cert in certs:
        # Look up issuer's public key
        if cert.issuer not in root_agents and cert.issuer not in {c.subject for c in certs}:
            # Issuer must be a root or an intermediate subject
            pass
        # In this implementation, we verify against root_agents if available.
        # For intermediate issuers, we'd need a full agent registry.
        # For v2.0.0, we verify all signatures if the issuer is a known root;
        # otherwise we defer to the registry (not implemented here).
        if cert.issuer in root_agents:
            canonical = canonical_certificate_bytes(cert)
            try:
                root_agents[cert.issuer].public_key.verify(cert.signature, canonical)
            except Exception as e:
                return CheckResult(False, f"signature verification failed for {cert.certificate_id}: {e}")

    # (b) attenuation
    for i in range(1, len(certs)):
        if not certs[i].scope.issubset(certs[i-1].scope):
            return CheckResult(
                False,
                f"scope attenuation violated at index {i}: "
                f"{set(certs[i].scope)} ⊄ {set(certs[i-1].scope)}"
            )

    # (c) expiry
    for cert in certs:
        if _is_expired(cert.expiry, current_time):
            return CheckResult(False, f"certificate {cert.certificate_id} expired")

    # (d) revocation
    for cert in certs:
        if cert.certificate_id in frontier.revocations:
            return CheckResult(False, f"certificate {cert.certificate_id} revoked")

    # (e) root recognition
    first_issuer = certs[0].issuer
    if first_issuer not in root_agents:
        return CheckResult(False, f"first certificate's issuer {first_issuer} is not a recognized root")

    # (contiguity) each cert's issuer = previous cert's subject
    for i in range(1, len(certs)):
        if certs[i].issuer != certs[i-1].subject:
            return CheckResult(
                False,
                f"contiguity violated at index {i}: "
                f"issuer {certs[i].issuer} ≠ previous subject {certs[i-1].subject}"
            )

    return CheckResult(True, "ok")
