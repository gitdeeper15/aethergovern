"""
Tests for aethergovern.authorization — grant, delegate, check.

Fixtures are provided by conftest.py (root_agent, subject_agent, scope).
"""

import pytest

from aethergovern.models import (
    Agent,
    AgentStatus,
    DelegationCertificate,
)
from aethergovern.authorization.certificates import (
    grant,
    delegate,
    canonical_certificate_bytes,
)


class TestGrant:
    def test_grant_creates_root_certificate(self, root_agent, subject_agent, scope):
        """A root certificate is created with parent_ref=None."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(
            root=root,
            subject=subject,
            scope=scope,
            expiry="2027-01-01T00:00:00Z",
            root_private_key=root_priv,
        )
        assert cert.issuer == "root-001"
        assert cert.subject == "agent-002"
        assert cert.parent_ref is None
        assert cert.scope == scope

    def test_grant_rejects_unrecognized_root(self, subject_agent, scope):
        """I4.2 — A non-root issuer is rejected."""
        subject, _ = subject_agent
        # A fake root that is not in the registry
        fake_priv, fake_pub = generate_keypair()
        fake_root = Agent(
            agent_id="fake-root",
            public_key=fake_pub,
            key_id="fake-key",
            role="maintainer",
            registered_at="2026-11-09T00:00:00Z",
            status=AgentStatus.ACTIVE,
        )
        with pytest.raises(ValueError, match="not a recognized root"):
            grant(
                root=fake_root,
                subject=subject,
                scope=scope,
                expiry="2027-01-01T00:00:00Z",
                root_private_key=fake_priv,
            )

    def test_grant_rejects_inactive_agent(self, root_agent, scope):
        """I1.3 — An inactive agent cannot be granted."""
        root, root_priv = root_agent
        inactive = Agent(
            agent_id="inactive-001",
            public_key=b"\x00" * 32,
            key_id="inactive-key",
            role=None,
            registered_at="2026-11-09T00:00:00Z",
            status=AgentStatus.SUSPENDED,
        )
        with pytest.raises(ValueError, match="not active"):
            grant(
                root=root,
                subject=inactive,
                scope=scope,
                expiry="2027-01-01T00:00:00Z",
                root_private_key=root_priv,
            )

    def test_grant_rejects_past_expiry(self, root_agent, subject_agent, scope):
        """I4.3 — An expiry in the past is rejected."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        with pytest.raises(ValueError, match="past"):
            grant(
                root=root,
                subject=subject,
                scope=scope,
                expiry="2020-01-01T00:00:00Z",
                root_private_key=root_priv,
            )

    def test_grant_rejects_empty_scope(self, root_agent, subject_agent):
        """An empty scope is rejected."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        with pytest.raises(ValueError, match="empty scope"):
            grant(
                root=root,
                subject=subject,
                scope=frozenset(),
                expiry="2027-01-01T00:00:00Z",
                root_private_key=root_priv,
            )

    def test_grant_signature_verifies(self, root_agent, subject_agent, scope):
        """I4.4 — The signature verifies against the root's key."""
        root, root_priv = root_agent
        subject, _ = subject_agent
        cert = grant(
            root=root,
            subject=subject,
            scope=scope,
            expiry="2027-01-01T00:00:00Z",
            root_private_key=root_priv,
        )
        canonical = canonical_certificate_bytes(cert)
        root.public_key.verify(cert.signature, canonical)


class TestDelegate:
    def test_delegate_creates_child_certificate(self, root_agent, subject_agent, scope):
        """A child certificate is created with parent_ref set."""
        root, root_priv = root_agent
        subject, subject_priv = subject_agent

        parent_cert = grant(
            root=root,
            subject=subject,
            scope=scope,
            expiry="2027-01-01T00:00:00Z",
            root_private_key=root_priv,
        )

        new_agent = Agent(
            agent_id="agent-003",
            public_key=b"\x01" * 32,
            key_id="new-key",
            role=None,
            registered_at="2026-11-09T00:00:00Z",
            status=AgentStatus.ACTIVE,
        )
        child_scope = frozenset([("commit", "branch/main")])

        child_cert = delegate(
            issuer=subject,
            subject=new_agent,
            scope=child_scope,
            expiry="2026-12-01T00:00:00Z",
            parent_certificate=parent_cert,
            issuer_private_key=subject_priv,
        )
        assert child_cert.parent_ref == parent_cert.certificate_id
        assert child_cert.issuer == "agent-002"
        assert child_cert.subject == "agent-003"

    def test_delegate_rejects_scope_escalation(self, root_agent, subject_agent, scope):
        """I4.1 — A scope larger than the parent's is rejected."""
        root, root_priv = root_agent
        subject, subject_priv = subject_agent

        parent_cert = grant(
            root=root,
            subject=subject,
            scope=scope,
            expiry="2027-01-01T00:00:00Z",
            root_private_key=root_priv,
        )

        new_agent = Agent(
            agent_id="agent-003",
            public_key=b"\x01" * 32,
            key_id="new-key",
            role=None,
            registered_at="2026-11-09T00:00:00Z",
            status=AgentStatus.ACTIVE,
        )
        larger_scope = frozenset([
            ("commit", "branch/main"),
            ("merge", "branch/main"),
            ("delete", "branch/main"),
        ])

        with pytest.raises(ValueError, match="not a subset"):
            delegate(
                issuer=subject,
                subject=new_agent,
                scope=larger_scope,
                expiry="2026-12-01T00:00:00Z",
                parent_certificate=parent_cert,
                issuer_private_key=subject_priv,
            )


# Import needed for the fake keypair in test_grant_rejects_unrecognized_root
from aethergovern.authorization.certificates import generate_keypair
