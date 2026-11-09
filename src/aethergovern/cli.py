"""
AetherGovern — Command-line interface (v2.0.0).

Usage:
    python -m aethergovern.cli info
    python -m aethergovern.cli verify
"""

from __future__ import annotations

import sys

from aethergovern.__version__ import (
    __version__,
    __author__,
    __email__,
    __doi__,
    __license__,
    __paper_version__,
    __record_id__,
)


def cmd_info(args) -> int:
    """Print version, DOI, and record information."""
    print("=" * 60)
    print(f"AetherGovern v{__version__}")
    print("=" * 60)
    print(f"Author:          {__author__}")
    print(f"Email:           {__email__}")
    print(f"License:         {__license__}")
    print(f"Paper version:   {__paper_version__}")
    print(f"Record ID:       {__record_id__}")
    print(f"DOI:             {__doi__}")
    print(f"DOI URL:         https://doi.org/{__doi__}")
    print()
    print("AetherGovern is the fifth functional dimension of the Aether family:")
    print("  AetherGit    (storage)          — 10.5281/zenodo.23966896")
    print("  AetherFlow   (integration)      — 10.5281/zenodo.23979129")
    print("  AetherProof  (verification)     — 10.5281/zenodo.24013124")
    print("  AetherMesh   (decentralization) — 10.5281/zenodo.24053492")
    print("  AetherGovern (governance)       — 10.5281/zenodo.24054524")
    print()
    print("Status: Architectural Hypothesis Under Investigation (v0.1.0).")
    print("        No real-world deployment. Theorems P1–P2 are proof sketches.")
    print("=" * 60)
    return 0


def cmd_verify(args) -> int:
    """Run a quick self-check."""
    print("=" * 60)
    print(f"AetherGovern v{__version__} — self-check")
    print("=" * 60)

    ok = True

    # 1. Ed25519 signature
    print("[1/3] Ed25519 signature verification")
    from aethergovern.authorization.certificates import generate_keypair
    priv, pub = generate_keypair()
    msg = b"test message"
    sig = priv.sign(msg)
    try:
        pub.verify(sig, msg)
        print("      ✅ Valid signature verified")
    except Exception:
        print("      ❌ Signature verification failed")
        ok = False

    # 2. Frontier join
    print("[2/3] Revocation frontier join")
    from aethergovern.models import RevocationFrontier
    from aethergovern.revocation.frontier import join_frontiers
    f1 = RevocationFrontier("f1", frozenset(["r1", "r2"]), "2026-11-09T00:00:00Z")
    f2 = RevocationFrontier("f2", frozenset(["r2", "r3"]), "2026-11-09T00:00:00Z")
    joined = join_frontiers(f1, f2)
    if joined.revocations == frozenset(["r1", "r2", "r3"]):
        print(f"      ✅ Frontier join: {sorted(joined.revocations)}")
    else:
        print(f"      ❌ Frontier join failed: {joined.revocations}")
        ok = False

    # 3. Policy evaluation
    print("[3/3] Policy evaluation")
    from aethergovern.models import (
        Action, ActionKind, Policy, PolicyStatus, PolicyVerdict, Rule
    )
    from aethergovern.policy.enforcement import apply_policy, policy_hash
    policy = Policy(
        policy_id="p1", version=1,
        rules=[Rule("commit", "branch/main", PolicyVerdict.ALLOW)],
        approval_chain=["agent-1"],
        status=PolicyStatus.ENFORCED,
        created_at="2026-11-01T00:00:00Z",
        effective_from="2026-11-01T00:00:00Z",
    )
    action = Action(
        action_id="a"*64, kind=ActionKind.COMMIT, actor="agent-1",
        resource="branch/main", payload={},
        timestamp="2026-11-09T00:00:00Z",
        frontier_ref="f"*64, policy_ref=policy_hash(policy),
        authority_chain=["c"*64], signature=b"\x00"*64,
    )
    verdict = apply_policy(action, policy)
    if verdict == PolicyVerdict.ALLOW:
        print(f"      ✅ Policy verdict: {verdict.value}")
    else:
        print(f"      ❌ Policy verdict: {verdict.value}")
        ok = False

    print("=" * 60)
    if ok:
        print("      ✅ All checks passed")
        return 0
    else:
        print("      ❌ Some checks failed")
        return 1


def main(argv=None) -> int:
    """Main entry point."""
    import argparse
    parser = argparse.ArgumentParser(
        prog="aethergovern",
        description=f"AetherGovern v{__version__} — falsification-first governance",
    )
    parser.add_argument("--version", action="version", version=f"aethergovern {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="Print version and record info")
    p_info.set_defaults(func=cmd_info)

    p_verify = sub.add_parser("verify", help="Run a self-check")
    p_verify.set_defaults(func=cmd_verify)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
