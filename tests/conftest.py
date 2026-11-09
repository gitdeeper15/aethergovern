"""
Pytest fixtures for AetherGovern v2.0.0.

This module registers the root agents and provides shared fixtures
for the authorization, policy, revocation, and dispute tests.
"""

import pytest

from aethergovern.models import Agent, AgentStatus
from aethergovern.authorization.certificates import (
    generate_keypair,
    register_root,
    clear_roots,
)


@pytest.fixture(autouse=True)
def reset_roots():
    """Reset the root registry before each test."""
    clear_roots()
    yield
    clear_roots()


@pytest.fixture
def root_agent():
    """A recognized root agent with a valid Ed25519 keypair."""
    priv, pub = generate_keypair()
    agent = Agent(
        agent_id="root-001",
        public_key=pub,
        key_id="root-key-1",
        role="root",
        registered_at="2026-11-09T00:00:00Z",
        status=AgentStatus.ACTIVE,
    )
    register_root(agent)
    return agent, priv


@pytest.fixture
def subject_agent():
    """A subject agent with a valid Ed25519 keypair."""
    priv, pub = generate_keypair()
    return Agent(
        agent_id="agent-002",
        public_key=pub,
        key_id="agent-key-1",
        role="maintainer",
        registered_at="2026-11-09T00:00:00Z",
        status=AgentStatus.ACTIVE,
    ), priv


@pytest.fixture
def scope():
    return frozenset([("commit", "branch/main")])
