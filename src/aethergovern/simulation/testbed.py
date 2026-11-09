"""
AetherGovern — Simulated P2P testbed.

Orchestrates nodes and a network to reproduce the evaluation metrics
from v0.1.0:
    - M1: Unauthorized-action admission rate
    - M2: Exposure count
    - M3: Exposure duration
    - M9: Convergence preservation

Reference:
    Baladi, S. (2026). AetherGovern v2.0.0,
    docs/specification/05_test_design.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from aethergovern.models import (
    Action,
    ActionKind,
    RevocationFrontier,
)
from aethergovern.simulation.network import (
    Network,
    PartitionEvent,
    PartitionSchedule,
)
from aethergovern.simulation.node import Node, create_cluster


@dataclass
class TestbedConfig:
    """Configuration for a single testbed run."""
    n_nodes: int = 10
    n_roots: int = 1
    seed: int = 42
    network_latency_min: float = 0.01
    network_latency_max: float = 0.05
    network_drop_probability: float = 0.0
    partition_events: List[PartitionEvent] = field(default_factory=list)


class Testbed:
    """A simulated P2P testbed for AetherGovern."""

    def __init__(self, config: TestbedConfig):
        self.config = config
        self.nodes: List[Node] = create_cluster(
            n=config.n_nodes,
            n_roots=config.n_roots,
            seed=config.seed,
        )
        self.network = Network(
            min_latency=config.network_latency_min,
            max_latency=config.network_latency_max,
            drop_probability=config.network_drop_probability,
            seed=config.seed,
        )
        self.schedule = PartitionSchedule(config.partition_events)
        self.current_time: float = 0.0
        self.round: int = 0

    def run_round(self) -> int:
        """Run one gossip round: each node sends its frontier to its peers."""
        self.schedule.apply_until(self.current_time, self.network)
        exchanges = 0
        for node in self.nodes:
            for peer in self.nodes:
                if peer.node_id == node.node_id:
                    continue
                if self.network._partition_blocks(node.node_id, peer.node_id):
                    continue
                self.network.send(
                    sender=node.node_id,
                    recipient=peer.node_id,
                    payload=("frontier", node.frontier),
                    send_time=self.current_time,
                )
                exchanges += 1
        self.network.deliver_until(
            self.current_time,
            on_delivery=self._on_delivery,
        )
        self.current_time += 0.1
        self.round += 1
        return exchanges

    def _on_delivery(self, sender: str, recipient: str, payload) -> None:
        kind, data = payload
        if kind == "frontier":
            target = self._find_node(recipient)
            if target is not None:
                # Merge frontiers
                joined = target.frontier.revocations | data.revocations
                target.frontier = RevocationFrontier(
                    frontier_id="joined",
                    revocations=joined,
                    created_at=target.frontier.created_at,
                )
                target.deltas_seen += 1

    def _find_node(self, node_id: str) -> Optional[Node]:
        for n in self.nodes:
            if n.node_id == node_id:
                return n
        return None

    def converged_fraction(self) -> float:
        """Fraction of nodes with the same frontier as the global union."""
        if not self.nodes:
            return 0.0
        global_set = set()
        for n in self.nodes:
            global_set |= n.frontier.revocations
        n_converged = sum(1 for n in self.nodes if n.frontier.revocations == global_set)
        return n_converged / len(self.nodes)

    def measure_exposure_window(self, expiry: str = "2027-01-01T00:00:00Z") -> Dict:
        """
        Measure the exposure window after a revocation.

        M2: number of nodes that still admit actions citing the revoked
            authority after the revocation is issued.
        """
        root = self.nodes[0]
        subject = self.nodes[1]
        cert = root.grant(subject, frozenset([("commit", "branch/main")]), expiry)
        record = root.revoke_certificate(cert, "test revocation")

        # Count nodes that have the revocation
        n_with_revocation = sum(
            1 for n in self.nodes if n.is_revoked(cert.certificate_id)
        )
        return {
            "n_nodes": len(self.nodes),
            "n_with_revocation": n_with_revocation,
            "exposure_fraction": 1.0 - (n_with_revocation / len(self.nodes)),
            "certificate_id": cert.certificate_id,
        }

    def summary(self) -> Dict:
        return {
            "n_nodes": len(self.nodes),
            "rounds_run": self.round,
            "current_time": self.current_time,
            "converged_fraction": self.converged_fraction(),
            "network_stats": self.network.stats(),
        }
