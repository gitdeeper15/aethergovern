#!/usr/bin/env python3
"""
Experiment 1 — Authorization Correctness (M1).

Measures the unauthorized-action admission rate:
    M1 = (number of actions by unauthorized agents that are admitted)
         / (total number of unauthorized actions attempted)

Simulation:
    - N nodes, with 1 root
    - Each node issues a certificate to a subject
    - The root revokes some certificates
    - Subjects attempt actions that cite their certificates
    - The check() operation is applied at each node's frontier
    - M1 = number of actions admitted despite revocation / total

Usage:
    python experiments/authorization_correctness/run.py

Output:
    experiments/authorization_correctness/results.json
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethergovern.models import (
    Action,
    ActionKind,
    RevocationFrontier,
)
from aethergovern.authorization.certificates import (
    grant,
    revoke,
    check,
    clear_roots,
    register_root,
    canonical_certificate_bytes,
)
from aethergovern.simulation.node import create_cluster
from aethergovern.simulation.testbed import Testbed, TestbedConfig


def build_action(
    cert,
    actor: str,
    resource: str = "branch/main",
    action_id: str = "a" * 64,
) -> Action:
    """Build an action that cites a certificate."""
    return Action(
        action_id=action_id,
        kind=ActionKind.COMMIT,
        actor=actor,
        resource=resource,
        payload={"diff": "abc"},
        timestamp="2026-11-09T00:00:00Z",
        frontier_ref="f" * 64,
        policy_ref="p" * 64,
        authority_chain=[cert.certificate_id],
        signature=b"\x00" * 64,
    )


def run_config(n_nodes: int, n_revocations: int, seed: int = 42) -> dict:
    """Run one configuration: N nodes, R revocations."""
    clear_roots()
    nodes = create_cluster(n_nodes, n_roots=1, seed=seed)
    root = nodes[0]

    # Grant a certificate to each non-root node
    certs = []
    for i in range(1, n_nodes):
        subject = nodes[i]
        cert = root.grant(
            subject=subject,
            scope=frozenset([("commit", "branch/main")]),
            expiry="2027-01-01T00:00:00Z",
        )
        certs.append(cert)

    # Register certificates in the testbed's registry
    registry = {}
    for cert in certs:
        registry[cert.certificate_id] = cert

    # Revoke some certificates
    n_revoked = min(n_revocations, len(certs))
    revoked_certs = certs[:n_revoked]
    frontier = RevocationFrontier(
        frontier_id="f0", revocations=frozenset(), created_at="2026-11-09T00:00:00Z"
    )
    for cert in revoked_certs:
        record = revoke(
            issuer=root.agent,
            certificate=cert,
            reason="test revocation",
            issuer_private_key=root.private_key,
            frontier=frontier,
        )
        frontier = RevocationFrontier(
            frontier_id="f1",
            revocations=frontier.revocations | {record.certificate_ref},
            created_at=frontier.created_at,
        )

    # Now check each action
    root_agents = {root.agent.agent_id: root.agent}
    total_unauthorized = 0
    admitted_unauthorized = 0

    for i, cert in enumerate(certs):
        # Build an action citing this certificate
        action = build_action(cert, actor=cert.subject)

        # Count it as unauthorized if the certificate is revoked at the frontier
        is_unauthorized = cert.certificate_id in frontier.revocations
        if is_unauthorized:
            total_unauthorized += 1

        # Run check
        from aethergovern.models import AuthorityChain
        chain = AuthorityChain(
            chain_id=f"chain-{i}",
            certificates=[cert.certificate_id],
            leaf_agent=cert.subject,
            leaf_scope=cert.scope,
        )
        result = check(
            action=action,
            chain=chain,
            frontier=frontier,
            current_time="2026-11-09T00:00:00Z",
            certificates=registry,
            root_agents=root_agents,
        )

        if result.valid and is_unauthorized:
            admitted_unauthorized += 1

    clear_roots()

    m1 = admitted_unauthorized / total_unauthorized if total_unauthorized else 0.0
    return {
        "n_nodes": n_nodes,
        "n_revocations": n_revoked,
        "total_unauthorized": total_unauthorized,
        "admitted_unauthorized": admitted_unauthorized,
        "m1_unauthorized_admission_rate": m1,
    }


def main():
    results = {
        "experiment": "authorization_correctness",
        "description": "Unauthorized-action admission rate (M1)",
        "source": "docs/specification/05_test_design.md",
        "runs": [],
    }

    configs = [
        (10, 2),
        (50, 5),
        (100, 10),
        (250, 20),
        (500, 50),
    ]

    for n_nodes, n_revocations in configs:
        print(f"Running n_nodes={n_nodes}, n_revocations={n_revocations}...", end=" ", flush=True)
        result = run_config(n_nodes, n_revocations, seed=42)
        results["runs"].append(result)
        print(f"M1={result['m1_unauthorized_admission_rate']:.4f}")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
