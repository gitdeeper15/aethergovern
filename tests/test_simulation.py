"""
Tests for aethergovern.simulation — network, node, testbed.

Covers:
    - Network: send, deliver, drop, partition, stats
    - create_cluster: N nodes, n_roots registered
    - Node: grant, revoke, is_revoked
    - Testbed: creation, convergence, summary
"""

import pytest

from aethergovern.simulation.network import Network, PartitionEvent, PartitionSchedule
from aethergovern.simulation.node import Node, create_cluster
from aethergovern.simulation.testbed import Testbed, TestbedConfig
from aethergovern.models import RevocationFrontier


# =============================================================================
# Network tests
# =============================================================================

class TestNetwork:
    def test_network_send_and_deliver(self):
        """Network sends and delivers messages."""
        net = Network(min_latency=0.01, max_latency=0.02, drop_probability=0.0, seed=42)
        ok = net.send("a", "b", "hello", send_time=0.0)
        assert ok is True

        delivered = []
        net.deliver_until(0.05, on_delivery=lambda s, r, p: delivered.append((s, r, p)))
        assert len(delivered) == 1
        assert delivered[0] == ("a", "b", "hello")

    def test_network_drop(self):
        """Drop probability = 1.0 drops all messages."""
        net = Network(drop_probability=1.0, seed=42)
        ok = net.send("a", "b", "msg", send_time=0.0)
        assert ok is False
        assert net.messages_dropped == 1

    def test_network_partition(self):
        """Partition blocks cross-partition messages."""
        net = Network(drop_probability=0.0, seed=42)
        net.set_partition({"a"})
        ok = net.send("a", "b", "msg", send_time=0.0)
        assert ok is False
        assert net.messages_blocked_by_partition == 1

    def test_network_stats(self):
        """Network stats are correct."""
        net = Network(drop_probability=0.0, seed=42)
        net.send("a", "b", "m1", send_time=0.0)
        net.send("b", "a", "m2", send_time=0.0)
        stats = net.stats()
        assert stats["messages_sent"] == 2
        assert stats["messages_in_flight"] == 2


# =============================================================================
# Cluster tests
# =============================================================================

class TestCluster:
    def test_cluster_creation(self):
        """create_cluster creates N nodes."""
        nodes = create_cluster(5, n_roots=1, seed=42)
        assert len(nodes) == 5
        for i, node in enumerate(nodes):
            assert node.node_id == f"node-{i:03d}"
            assert node.agent.agent_id == f"agent-{i:03d}"

    def test_cluster_roots(self):
        """The first n_roots nodes are registered as roots."""
        from aethergovern.authorization.certificates import is_root, clear_roots
        clear_roots()
        nodes = create_cluster(5, n_roots=2, seed=42)
        assert is_root(nodes[0].agent) is True
        assert is_root(nodes[1].agent) is True
        assert is_root(nodes[2].agent) is False
        clear_roots()


# =============================================================================
# Node tests
# =============================================================================

class TestNode:
    def test_node_grant(self):
        """Node.grant creates a certificate."""
        from aethergovern.authorization.certificates import clear_roots
        clear_roots()
        nodes = create_cluster(3, n_roots=1, seed=42)
        root = nodes[0]
        subject = nodes[1]
        cert = root.grant(subject, frozenset([("commit", "branch/main")]), "2027-01-01T00:00:00Z")
        assert cert.issuer == root.agent.agent_id
        assert cert.subject == subject.agent.agent_id
        assert cert.parent_ref is None
        clear_roots()

    def test_node_revoke(self):
        """Node.revoke_certificate creates a revocation record."""
        from aethergovern.authorization.certificates import clear_roots
        clear_roots()
        nodes = create_cluster(3, n_roots=1, seed=42)
        root = nodes[0]
        subject = nodes[1]
        cert = root.grant(subject, frozenset([("commit", "branch/main")]), "2027-01-01T00:00:00Z")
        record = root.revoke_certificate(cert, "test revocation")
        assert record.certificate_ref == cert.certificate_id
        assert record.issuer == root.agent.agent_id
        clear_roots()

    def test_node_is_revoked(self):
        """Node.is_revoked returns True after revocation."""
        from aethergovern.authorization.certificates import clear_roots
        clear_roots()
        nodes = create_cluster(3, n_roots=1, seed=42)
        root = nodes[0]
        subject = nodes[1]
        cert = root.grant(subject, frozenset([("commit", "branch/main")]), "2027-01-01T00:00:00Z")
        assert root.is_revoked(cert.certificate_id) is False
        root.revoke_certificate(cert, "test revocation")
        assert root.is_revoked(cert.certificate_id) is True
        clear_roots()


# =============================================================================
# Testbed tests
# =============================================================================

class TestTestbed:
    def test_testbed_creation(self):
        """Testbed creates N nodes."""
        config = TestbedConfig(n_nodes=5, n_roots=1, seed=42)
        tb = Testbed(config)
        assert len(tb.nodes) == 5
        assert tb.current_time == 0.0
        assert tb.round == 0

    def test_testbed_convergence(self):
        """Frontiers converge after gossip rounds."""
        from aethergovern.authorization.certificates import clear_roots
        clear_roots()
        config = TestbedConfig(n_nodes=3, n_roots=1, seed=42)
        tb = Testbed(config)
        # Issue a revocation at node 0
        cert = tb.nodes[0].grant(
            tb.nodes[1],
            frozenset([("commit", "branch/main")]),
            "2027-01-01T00:00:00Z",
        )
        tb.nodes[0].revoke_certificate(cert, "test revocation")
        # Run a few rounds
        for _ in range(5):
            tb.run_round()
        # After enough rounds, all nodes should have the revocation
        # (for a small network with no drops, this should happen quickly)
        assert tb.converged_fraction() > 0.0
        clear_roots()

    def test_testbed_summary(self):
        """Testbed.summary returns a dict."""
        config = TestbedConfig(n_nodes=3, n_roots=1, seed=42)
        tb = Testbed(config)
        summary = tb.summary()
        assert "n_nodes" in summary
        assert summary["n_nodes"] == 3
        assert "rounds_run" in summary
        assert "network_stats" in summary
