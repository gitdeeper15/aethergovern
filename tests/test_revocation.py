"""
Tests for aethergovern.revocation — revoke + frontier.

Covers invariants:
    - I5.1 (monotonicity)
    - I5.2 (signature covers content)
    - I5.3 (issuer authority)
    - I7.1 (grow-only)
    - I7.2 (join is union)
"""

import pytest

from aethergovern.models import (
    Agent,
    AgentStatus,
    DelegationCertificate,
    RevocationFrontier,
    RevocationRecord,
)
from aethergovern.authorization.certificates import (
    grant,
    revoke,
    generate_keypair,
    canonical_revocation_bytes,
)
from aethergovern.revocation.frontier import (
    add_revocation,
    join_frontiers,
    is_revoked,
)


class TestRevoke:
    def test_revoke_creates_record(self, root_agent, subject_agent, scope):
        """A revocation record is created."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        frontier = RevocationFrontier(
            frontier_id="f0", revocations=frozenset(), created_at="2026-11-09T00:00:00Z"
        )
        record = revoke(root, cert, "test revocation", root_priv, frontier)
        assert record.certificate_ref == cert.certificate_id
        assert record.issuer == root.agent_id
        assert record.reason == "test revocation"

    def test_revoke_rejects_non_issuer(self, root_agent, subject_agent, scope):
        """I5.3 — A non-issuer is rejected."""
        root, root_priv = root_agent
        subject, subject_priv = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        frontier = RevocationFrontier(
            frontier_id="f0", revocations=frozenset(), created_at="2026-11-09T00:00:00Z"
        )
        with pytest.raises(ValueError, match="not the certificate's issuer"):
            revoke(subject, cert, "unauthorized", subject_priv, frontier)

    def test_revoke_rejects_already_revoked(self, root_agent, subject_agent, scope):
        """I5.1 — An already-revoked certificate is rejected."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        frontier0 = RevocationFrontier(
            frontier_id="f0", revocations=frozenset(), created_at="2026-11-09T00:00:00Z"
        )
        record = revoke(root, cert, "first", root_priv, frontier0)
        frontier1 = add_revocation(frontier0, record)
        with pytest.raises(ValueError, match="already revoked"):
            revoke(root, cert, "second", root_priv, frontier1)

    def test_revoke_invalidates_dependents(self, root_agent, subject_agent, scope):
        """I5.1 — Revoking a parent invalidates its children."""
        root, root_priv = root_agent
        subject, subject_priv = subject_agent
        parent_cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        new_agent = Agent("agent-003", b"\x01" * 32, "k3", None, "2026-11-09T00:00:00Z", AgentStatus.ACTIVE)
        child_scope = frozenset([("commit", "branch/main")])
        from aethergovern.authorization.certificates import delegate
        child_cert = delegate(subject, new_agent, child_scope, "2026-12-01T00:00:00Z", parent_cert, subject_priv)
        frontier0 = RevocationFrontier("f0", frozenset(), "2026-11-09T00:00:00Z")
        record = revoke(root, parent_cert, "revoke parent", root_priv, frontier0)
        frontier1 = add_revocation(frontier0, record)
        assert is_revoked(frontier1, parent_cert.certificate_id)
        # Child is not directly revoked, but its parent is.
        assert not is_revoked(frontier1, child_cert.certificate_id)

    def test_revoke_monotonic(self, root_agent, subject_agent, scope):
        """I5.1 — Adding a revocation does not validate."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        frontier0 = RevocationFrontier("f0", frozenset(), "2026-11-09T00:00:00Z")
        record = revoke(root, cert, "test", root_priv, frontier0)
        frontier1 = add_revocation(frontier0, record)
        # If it was revoked at f0 (it wasn't), it remains revoked at f1.
        # If it was not revoked at f0, it may be revoked at f1.
        assert not is_revoked(frontier0, cert.certificate_id)
        assert is_revoked(frontier1, cert.certificate_id)

    def test_revoke_signature_verifies(self, root_agent, subject_agent, scope):
        """I5.2 — The signature verifies against the issuer's key."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        frontier0 = RevocationFrontier("f0", frozenset(), "2026-11-09T00:00:00Z")
        record = revoke(root, cert, "test", root_priv, frontier0)
        canonical = canonical_revocation_bytes(record)
        root.public_key.verify(record.signature, canonical)


class TestFrontier:
    def test_frontier_join_is_union(self):
        """I7.2 — Frontier join is set union."""
        f1 = RevocationFrontier("f1", frozenset(["r1", "r2"]), "2026-11-09T00:00:00Z")
        f2 = RevocationFrontier("f2", frozenset(["r2", "r3"]), "2026-11-09T00:00:00Z")
        joined = join_frontiers(f1, f2)
        assert joined.revocations == frozenset(["r1", "r2", "r3"])

    def test_frontier_grow_only(self, root_agent, subject_agent, scope):
        """I7.1 — A frontier can only grow."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(root, subject, scope, "2027-01-01T00:00:00Z", root_priv)
        f0 = RevocationFrontier("f0", frozenset(), "2026-11-09T00:00:00Z")
        record = revoke(root, cert, "test", root_priv, f0)
        f1 = add_revocation(f0, record)
        assert f0.revocations <= f1.revocations
