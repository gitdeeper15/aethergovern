#!/usr/bin/env python3
"""
Experiment 3 — Attribution Accuracy (M4, M5).

Measures:
    M4: Attribution completeness — fraction of admitted actions
        for which the responsible chain can be recovered from records.
    M5: Attribution accuracy — fraction of recovered chains that match
        the ground-truth chain.

Simulation:
    - N nodes, with 1 root
    - Root grants a certificate to a subject
    - Subject performs actions
    - Each action is admitted at the subject's node, and an
      accountability record is created
    - We try to recover the chain from the records
    - M4 = number of actions with a recoverable chain / total actions
    - M5 = number of correctly recovered chains / total recoveries

Usage:
    python experiments/attribution_accuracy/run.py

Output:
    experiments/attribution_accuracy/results.json
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from aethergovern.models import (
    Action,
    ActionKind,
    AccountabilityRecord,
)
from aethergovern.authorization.certificates import (
    clear_roots,
    grant,
)
from aethergovern.accountability.records import (
    create_record,
    query_by_action,
)
from aethergovern.simulation.node import create_cluster


def run_config(n_nodes: int, n_actions_per_node: int = 5, seed: int = 42) -> dict:
    """Run one configuration: N nodes, M actions each, measure M4 and M5."""
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
        certs.append((subject, cert))

    # Simulate actions
    records: list[AccountabilityRecord] = []
    actions: list[Action] = []
    ground_truth: dict[str, str] = {}  # action_id -> true chain_ref

    prev_hash = "0" * 64
    for subject, cert in certs:
        for j in range(n_actions_per_node):
            action_id = f"{subject.agent.agent_id}-{j}"
            action = Action(
                action_id=action_id,
                kind=ActionKind.COMMIT,
                actor=subject.agent.agent_id,
                resource="branch/main",
                payload={"diff": f"diff-{j}"},
                timestamp="2026-11-09T00:00:00Z",
                frontier_ref="f" * 64,
                policy_ref="p" * 64,
                authority_chain=[cert.certificate_id],
                signature=b"\x00" * 64,
            )
            actions.append(action)
            ground_truth[action_id] = cert.certificate_id

            # Create accountability record
            record = create_record(
                action=action,
                authority_chain_ref=cert.certificate_id,
                admitted_by=subject.node_id,
                prev_record_hash=prev_hash,
            )
            records.append(record)
            prev_hash = record.record_id

    # M4: try to recover each action's chain
    m4_recovered = 0
    m5_correct = 0
    for action in actions:
        found = query_by_action(records, action.action_id)
        if len(found) >= 1:
            m4_recovered += 1
            # M5: check if recovered chain matches ground truth
            recovered_chain = found[0].authority_chain_ref
            if recovered_chain == ground_truth[action.action_id]:
                m5_correct += 1

    total_actions = len(actions)
    m4 = m4_recovered / total_actions if total_actions else 0.0
    m5 = m5_correct / m4_recovered if m4_recovered else 0.0

    clear_roots()

    return {
        "n_nodes": n_nodes,
        "n_actions_per_node": n_actions_per_node,
        "total_actions": total_actions,
        "m4_recovered": m4_recovered,
        "m4_attribution_completeness": m4,
        "m5_correct": m5_correct,
        "m5_attribution_accuracy": m5,
    }


def main():
    results = {
        "experiment": "attribution_accuracy",
        "description": "Attribution completeness (M4) and accuracy (M5)",
        "source": "docs/specification/05_test_design.md",
        "runs": [],
    }

    configs = [
        (10, 5),
        (50, 5),
        (100, 5),
        (250, 3),
        (500, 2),
    ]

    for n_nodes, n_actions in configs:
        print(f"Running n_nodes={n_nodes}, n_actions={n_actions}...", end=" ", flush=True)
        result = run_config(n_nodes, n_actions, seed=42)
        results["runs"].append(result)
        print(f"M4={result['m4_attribution_completeness']:.4f}, M5={result['m5_attribution_accuracy']:.4f}")

    out = Path(__file__).parent / "results.json"
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results written to {out}")


if __name__ == "__main__":
    main()
