#!/usr/bin/env python3
"""
Experiment 2 — Exposure Window (M2, M3).

Measures:
    M2: Exposure count — number of nodes that still admit actions
        citing a revoked authority after the revocation is issued.
    M3: Exposure duration — time from revocation issue to its receipt
        at each honest node (median, 99th percentile).

Simulation:
    - N nodes, with 1 root
    - Root grants a certificate to a subject
    - Subject performs actions continuously
    - Root revokes the certificate at a known time
    - We measure how long each node takes to see the revocation
    - M2 = number of nodes that never see the revocation
    - M3 = distribution of receipt times

Usage:
    python experiments/exposure_window/run.py

Output:
    experiments/exposure_window/results.json
"""

import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethergovern.models import RevocationFrontier
from aethergovern.authorization.certificates import (
    clear_roots,
    grant,
    revoke,
    is_root,
)
from aethergovern.simulation.node import create_cluster, Node
from aethergovern.simulation.network import Network


def run_config(n_nodes: int, seed: int = 42, max_rounds: int = 100) -> dict:
    """Run one configuration: N nodes, one revocation, measure exposure."""
    clear_roots()
    nodes = create_cluster(n_nodes, n_roots=1, seed=seed)
    root = nodes[0]
    subject = nodes[1] if n_nodes > 1 else nodes[0]

    # Grant a certificate
    cert = root.grant(
        subject=subject,
        scope=frozenset([("commit", "branch/main")]),
        expiry="2027-01-01T00:00:00Z",
    )

    # Track when each node receives the revocation
    revocation_time = 0.0  # logical time of revocation issue
    receipt_times = {n.node_id: None for n in nodes}

    # Issue the revocation at root
    record = root.revoke_certificate(cert, "test revocation")

    # At the moment of revocation, the root itself has it
    receipt_times[root.node_id] = revocation_time

    # Build a network: each round, nodes gossip their frontier to k peers
    net = Network(min_latency=0.01, max_latency=0.05, drop_probability=0.0, seed=seed)
    current_time = 0.0

    # Each round, gossip the root's frontier to all other nodes
    for round_idx in range(max_rounds):
        # Root sends its frontier to all peers
        for peer in nodes:
            if peer.node_id == root.node_id:
                continue
            net.send(
                sender=root.node_id,
                recipient=peer.node_id,
                payload=("revocation", record),
                send_time=current_time,
            )

        # Deliver
        def on_delivery(sender, recipient, payload):
            kind, data = payload
            if kind != "revocation":
                return
            target = next((n for n in nodes if n.node_id == recipient), None)
            if target is None:
                return
            if receipt_times[target.node_id] is None:
                receipt_times[target.node_id] = current_time
            # Merge into target's frontier
            if data.certificate_ref not in target.frontier.revocations:
                target.frontier = RevocationFrontier(
                    frontier_id="merged",
                    revocations=target.frontier.revocations | {data.certificate_ref},
                    created_at=target.frontier.created_at,
                )

        net.deliver_until(current_time, on_delivery=on_delivery)
        current_time += 0.1

        # Check if all nodes have seen the revocation
        if all(t is not None for t in receipt_times.values()):
            break

    # M2: number of nodes that did NOT receive the revocation
    m2_count = sum(1 for t in receipt_times.values() if t is None)

    # M3: distribution of receipt times (excluding root)
    times = [t for nid, t in receipt_times.items() if nid != root.node_id and t is not None]
    if times:
        m3_median = statistics.median(times)
        m3_p99 = sorted(times)[int(0.99 * len(times))] if len(times) > 1 else times[0]
    else:
        m3_median = None
        m3_p99 = None

    clear_roots()

    return {
        "n_nodes": n_nodes,
        "m2_exposure_count": m2_count,
        "m3_receipt_times": times,
        "m3_median_ms": (m3_median * 1000) if m3_median is not None else None,
        "m3_p99_ms": (m3_p99 * 1000) if m3_p99 is not None else None,
        "rounds_run": round_idx + 1,
    }


def main():
    results = {
        "experiment": "exposure_window",
        "description": "Exposure count (M2) and duration (M3) after revocation",
        "source": "docs/specification/05_test_design.md",
        "runs": [],
    }

    configs = [10, 50, 100, 250, 500]

    for n_nodes in configs:
        print(f"Running n_nodes={n_nodes}...", end=" ", flush=True)
        result = run_config(n_nodes, seed=42)
        results["runs"].append(result)
        print(f"M2={result['m2_exposure_count']}, M3 median={result['m3_median_ms']} ms")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
