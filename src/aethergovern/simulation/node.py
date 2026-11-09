"""
AetherGovern — Simulated node.

A Node bundles:
    - A local authority registry
    - A revocation frontier
    - A keypair (for signing)
    - A reference to the shared key registry

The Node is the unit of simulation.

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0,
    docs/specification/04_interfaces.md.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from aethergovern.models import (
    Agent,
    AgentStatus,
    DelegationCertificate,
    RevocationFrontier,
    RevocationRecord,
)
from aethergovern.authorization.certificates import (
    generate_keypair,
    grant,
    revoke,
    is_root,
    register_root,
)
from aethergovern.revocation.frontier import (
    add_revocation,
    is_revoked,
)


@dataclass
class Node:
    """
    A simulated AetherGovern node.

    Attributes:
        node_id:         Unique identifier.
        agent:           The agent this node represents.
        private_key:     This node's signing key.
        registry:        Shared certificate registry (cert_id -> cert).
        frontier:        Local revocation frontier.
        deltas_seen:     Number of deltas this node has processed.
        grants_issued:   Number of certificates issued.
        revocations:     Number of revocations issued.
    """
    node_id: str
    agent: Agent
    private_key: object  # Ed25519PrivateKey
    registry: Dict[str, DelegationCertificate] = field(default_factory=dict)
    frontier: RevocationFrontier = field(
        default_factory=lambda: RevocationFrontier(
            frontier_id="f0", revocations=frozenset(), created_at="2026-11-09T00:00:00Z"
        )
    )
    deltas_seen: int = 0
    grants_issued: int = 0
    revocations: int = 0

    def grant(
        self,
        subject: Node,
        scope: frozenset,
        expiry: str,
    ) -> DelegationCertificate:
        """Issue a root certificate (only if this node's agent is a root)."""
        cert = grant(
            root=self.agent,
            subject=subject.agent,
            scope=scope,
            expiry=expiry,
            root_private_key=self.private_key,
        )
        self.registry[cert.certificate_id] = cert
        self.grants_issued += 1
        return cert

    def revoke_certificate(
        self,
        certificate: DelegationCertificate,
        reason: str,
    ) -> RevocationRecord:
        """Revoke a certificate."""
        record = revoke(
            issuer=self.agent,
            certificate=certificate,
            reason=reason,
            issuer_private_key=self.private_key,
            frontier=self.frontier,
        )
        self.frontier = add_revocation(self.frontier, record)
        self.revocations += 1
        return record

    def is_revoked(self, certificate_id: str) -> bool:
        return is_revoked(self.frontier, certificate_id)

    def summary(self) -> Dict:
        return {
            "node_id": self.node_id,
            "agent_id": self.agent.agent_id,
            "frontier_size": len(self.frontier.revocations),
            "registry_size": len(self.registry),
            "grants_issued": self.grants_issued,
            "revocations": self.revocations,
        }


def create_cluster(
    n: int,
    n_roots: int = 1,
    seed: Optional[int] = None,
) -> List[Node]:
    """
    Create n nodes, with `n_roots` recognized roots.

    Each node has a unique agent and keypair. The first `n_roots` nodes
    are registered as roots.
    """
    rng = random.Random(seed)
    nodes: List[Node] = []

    for i in range(n):
        node_id = f"node-{i:03d}"
        agent_id = f"agent-{i:03d}"
        priv, pub = generate_keypair()
        agent = Agent(
            agent_id=agent_id,
            public_key=pub,
            key_id=f"key-{i}",
            role="root" if i < n_roots else "agent",
            registered_at="2026-11-09T00:00:00Z",
            status=AgentStatus.ACTIVE,
        )
        nodes.append(Node(node_id=node_id, agent=agent, private_key=priv))

    # Register the first n_roots as roots
    for i in range(n_roots):
        register_root(nodes[i].agent)

    return nodes
