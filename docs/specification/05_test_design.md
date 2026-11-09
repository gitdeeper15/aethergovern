# AetherGovern v2.0.0 — Test Design

**Version:** 2.0.0-draft
**Date:** 2026-11-09
**Status:** Operational Specification (v2.0.0)
**Depends on:** `01_entities.md`, `02_operations.md`, `03_invariants.md`, `04_interfaces.md`
**Reference:** AetherGovern v0.1.0, DOI [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)

---

## Purpose

This document designs the test suite for AetherGovern v2.0.0. It specifies:

- **What** is tested (invariants from `03_invariants.md`, operations from `02_operations.md`, interfaces from `04_interfaces.md`).
- **How** it is tested (unit, property-based, integration, simulation).
- **Which tools** are used (pytest, Hypothesis).
- **The success criteria** for each test.

The test suite is the operational counterpart of the invariants: if the implementation violates an invariant, at least one test must fail.

> **Methodological note.** v0.1.0 had no tests (it was a hypothesis). v2.0.0 designs the tests **before** writing the implementation, so that the implementation is driven by the specification rather than the reverse. This is the "test-first" discipline applied to the operational specification.

---

## Test Categories

| Category | Tool | Scope | Count |
|---|---|---|:-:|
| **Unit** | pytest | Individual operations and entities | ~60 |
| **Property-based** | Hypothesis | Invariants over generated inputs | ~20 |
| **Integration** | pytest | Interfaces between dimensions | ~15 |
| **Simulation** | pytest + custom harness | End-to-end behavior under network conditions | ~12 |
| **Total** | | | **~107** |

The exact count (107) is a **proposal**, not a commitment. The tests will be counted precisely after implementation. If the specification reveals that fewer tests are needed (or more), the count will be revised — this is the discipline of not assuming "107" as a target.

---

## Unit Tests (~60)

### Entities (10 tests)

| # | Test | What it verifies | Invariant |
|:-:|---|---|:-:|
| 1 | `test_agent_creation` | An Agent can be created with valid fields. | — |
| 2 | `test_agent_key_unique` | Two agents cannot share a public key. | I1.1 |
| 3 | `test_agent_status_monotonic` | A revoked agent cannot return to active. | I1.2 |
| 4 | `test_action_content_addressing` | An action's id is the SHA-256 of its content. | I2.2 |
| 5 | `test_action_signature` | An action's signature verifies against the actor's key. | I2.3 |
| 6 | `test_action_chain_completeness` | An action with an empty chain is rejected. | I2.4 |
| 7 | `test_resource_id_stable` | A resource's id cannot be changed. | I3.1 |
| 8 | `test_resource_kind_immutable` | A resource's kind cannot be changed. | I3.2 |
| 9 | `test_certificate_signature` | A certificate's signature verifies against the issuer's key. | I4.4 |
| 10 | `test_frontier_join_is_union` | Frontier join is set union. | I7.2 |

### Operations (50 tests, 7 operations)

**`grant` (6 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 11 | `test_grant_creates_root_certificate` | A root certificate is created with `parent_ref=None`. |
| 12 | `test_grant_rejects_unrecognized_root` | A non-root issuer is rejected. |
| 13 | `test_grant_rejects_inactive_agent` | An inactive agent cannot be granted. |
| 14 | `test_grant_rejects_past_expiry` | An expiry in the past is rejected. |
| 15 | `test_grant_rejects_empty_scope` | An empty scope is rejected. |
| 16 | `test_grant_signature_verifies` | The signature verifies against the root's key. |

**`delegate` (8 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 17 | `test_delegate_creates_child_certificate` | A child certificate is created with `parent_ref` set. |
| 18 | `test_delegate_rejects_non_parent_subject` | An issuer that is not the parent's subject is rejected. |
| 19 | `test_delegate_rejects_expired_parent` | An expired parent is rejected. |
| 20 | `test_delegate_rejects_revoked_parent` | A revoked parent is rejected. |
| 21 | `test_delegate_rejects_scope_escalation` | A scope larger than the parent's is rejected. |
| 22 | `test_delegate_rejects_expiry_beyond_parent` | A child expiring later than its parent is rejected. |
| 23 | `test_delegate_preserves_attenuation` | The child's scope ⊆ the parent's scope. |
| 24 | `test_delegate_signature_verifies` | The signature verifies against the issuer's key. |

**`revoke` (6 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 25 | `test_revoke_creates_record` | A revocation record is created. |
| 26 | `test_revoke_rejects_non_issuer` | A non-issuer (and non-ancestor) is rejected. |
| 27 | `test_revoke_rejects_already_revoked` | An already-revoked certificate is rejected. |
| 28 | `test_revoke_invalidates_dependents` | Revoking a parent invalidates its children. |
| 29 | `test_revoke_monotonic` | Adding a revocation does not validate. |
| 30 | `test_revoke_signature_verifies` | The signature verifies against the issuer's key. |

**`check` (10 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 31 | `test_check_valid_chain` | A valid chain at a frontier returns `valid=True`. |
| 32 | `test_check_expired_certificate` | An expired certificate returns `valid=False`. |
| 33 | `test_check_revoked_certificate` | A revoked certificate returns `valid=False`. |
| 34 | `test_check_scope_escalation` | A chain with scope escalation returns `valid=False`. |
| 35 | `test_check_unknown_root` | A chain with an unknown root returns `valid=False`. |
| 36 | `test_check_broken_contiguity` | A chain with broken contiguity returns `valid=False`. |
| 37 | `test_check_action_frontier_mismatch` | An action citing a different frontier returns `valid=False`. |
| 38 | `test_check_action_chain_mismatch` | An action presenting a different chain returns `valid=False`. |
| 39 | `test_check_deterministic` | The same input always gives the same output. |
| 40 | `test_check_ignores_local_state` | The check does not depend on local clock. |

**`apply_policy` (8 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 41 | `test_apply_policy_allow` | A matching rule returns `allow`. |
| 42 | `test_apply_policy_deny` | A matching deny rule returns `deny`. |
| 43 | `test_apply_policy_quarantine` | A matching quarantine rule returns `quarantine`. |
| 44 | `test_apply_policy_default_deny` | No matching rule returns `deny`. |
| 45 | `test_apply_policy_rejects_unenforced` | An unenforced policy is rejected. |
| 46 | `test_apply_policy_rejects_ineffective` | A policy not yet effective is rejected. |
| 47 | `test_apply_policy_rejects_mismatch` | An action citing a different policy is rejected. |
| 48 | `test_apply_policy_deterministic` | The same input always gives the same verdict. |

**`escalate` (5 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 49 | `test_escalate_pending_dispute` | A pending dispute can be escalated. |
| 50 | `test_escalate_rejects_resolved` | A resolved dispute cannot be escalated. |
| 51 | `test_escalate_rejects_empty_target` | An empty escalation target is rejected. |
| 52 | `test_escalate_records_reason` | The escalation record contains the reason. |
| 53 | `test_escalate_records_target` | The escalation record contains the target. |

**`rotate_key` (7 tests)**

| # | Test | What it verifies |
|:-:|---|---|
| 54 | `test_rotate_key_updates_public_key` | The agent's public key is replaced. |
| 55 | `test_rotate_key_rejects_inactive_agent` | An inactive agent cannot rotate. |
| 56 | `test_rotate_key_rejects_duplicate_key` | A key already registered is rejected. |
| 57 | `test_rotate_key_requires_ownership_proof` | The old private key must verify. |
| 58 | `test_rotate_key_preserves_certificates` | Existing certificates remain valid. |
| 59 | `test_rotate_key_creates_audit_record` | A key rotation record is created. |
| 60 | `test_rotate_key_preserves_status` | The agent's status is unchanged. |

---

## Property-Based Tests (~20)

Using **Hypothesis**, these tests generate random inputs and verify that the invariants hold for all of them.

| # | Test | Property |
|:-:|---|---|
| 61 | `test_attenuation_random` | For random chains, I4.1 holds. |
| 62 | `test_monotonicity_random` | For random frontiers, I5.1 holds. |
| 63 | `test_join_associativity` | Frontier join is associative. |
| 64 | `test_join_commutativity` | Frontier join is commutative. |
| 65 | `test_join_idempotence` | Frontier join is idempotent. |
| 66 | `test_scope_intersection` | The leaf scope is the intersection of all scopes. |
| 67 | `test_no_cycle_in_chains` | Random chains have no cycle. |
| 68 | `test_no_cycle_in_policies` | Random policies have no cycle. |
| 69 | `test_determinism_random` | Random actions give the same verdict at honest nodes. |
| 70 | `test_content_addressing_random` | Random actions have content-addressed ids. |
| 71 | `test_signature_integrity_random` | Random actions have verifiable signatures. |
| 72 | `test_chain_contiguity_random` | Random chains are contiguous. |
| 73 | `test_expiry_monotonic` | Child certificates expire no later than parents. |
| 74 | `test_frontier_grow_only` | Frontiers only grow. |
| 75 | `test_policy_version_monotonic` | Policy versions only increase. |
| 76 | `test_dispute_determinism` | Random disputes resolve deterministically. |
| 77 | `test_attribution_completeness` | Every admitted action has a record. |
| 78 | `test_hash_link_integrity` | Random record chains are intact. |
| 79 | `test_authority_evidence_separation` | Authority records ≠ evidence records. |
| 80 | `test_root_set_common_knowledge` | All honest nodes agree on the root set. |

---

## Integration Tests (~15)

These tests verify that the four interfaces from `04_interfaces.md` work correctly.

### AetherGit (3 tests)

| # | Test | What it verifies |
|:-:|---|---|
| 81 | `test_git_stores_governance_headers` | Governance headers are stored and retrieved. |
| 82 | `test_git_preserves_hash_links` | The `prev_record_hash` chain is intact. |
| 83 | `test_git_rejects_invalid_records` | Invalid governance records are rejected. |

### AetherFlow (4 tests)

| # | Test | What it verifies |
|:-:|---|---|
| 84 | `test_flow_requests_authorization` | AetherFlow requests a verdict before admission. |
| 85 | `test_flow_honors_verdict` | AetherFlow honors the verdict. |
| 86 | `test_flow_preserves_causal_refs` | AetherFlow does not strip `frontier_ref` or `policy_ref`. |
| 87 | `test_flow_deterministic` | AetherFlow does not add local state. |

### AetherProof (4 tests)

| # | Test | What it verifies |
|:-:|---|---|
| 88 | `test_proof_designates_governed_changes` | Governed specification changes are designated. |
| 89 | `test_proof_respects_approval_chain` | Unapproved changes are rejected. |
| 90 | `test_proof_separates_authority_and_evidence` | Authority ≠ evidence. |
| 91 | `test_proof_no_circularity` | Policies verified by AetherProof do not feed back into governance. |

### AetherMesh (4 tests)

| # | Test | What it verifies |
|:-:|---|---|
| 92 | `test_mesh_replicates_governance_deltas` | Governance deltas replicate as ordinary deltas. |
| 93 | `test_mesh_join_is_union` | Frontier join is set union. |
| 94 | `test_mesh_admission_predicate_deterministic` | The admission predicate satisfies A6. |
| 95 | `test_mesh_preserves_governance_metadata` | Governance metadata survives replication. |

---

## Simulation Tests (~12)

These tests run the simulator under network conditions and verify end-to-end behavior.

| # | Test | What it verifies |
|:-:|---|---|
| 96 | `test_sim_convergence` | Honest nodes converge on the same admitted set. |
| 97 | `test_sim_exposure_window` | The exposure window after revocation is finite. |
| 98 | `test_sim_partition_healing` | Partitions heal; frontiers converge. |
| 99 | `test_sim_revocation_propagation` | Revocations propagate via gossip. |
| 100 | `test_sim_no_divergence` | No divergence under deterministic admission. |
| 101 | `test_sim_chain_verification_cost` | Chain verification cost is linear in chain length. |
| 102 | `test_sim_attribution_recovery` | Attribution can be recovered from records. |
| 103 | `test_sim_dispute_resolution` | Disputes resolve or escalate deterministically. |
| 104 | `test_sim_key_rotation` | Key rotation does not break existing certificates. |
| 105 | `test_sim_policy_consistency` | Policies can be checked for consistency. |
| 106 | `test_sim_hybrid_causal_eventual` | Hybrid causal/eventual validity is tested (Q9). |
| 107 | `test_sim_scenario_classes` | The scenario classes of Section 7.3 are exercised. |

---

## Test Design Principles

1. **Test-first.** Tests are designed before the implementation, from the specification.
2. **Invariant-driven.** Every test maps to an invariant from `03_invariants.md`.
3. **Deterministic.** All tests are deterministic (seeds fixed, no wall-clock dependence).
4. **Reproducible.** Any test failure can be reproduced with the same seed.
5. **No over-specification.** Tests verify the specification, not implementation details.

---

## Success Criteria

A test passes if:

- The actual behavior matches the expected behavior.
- The invariant it tests holds.
- The test is deterministic and reproducible.

A test fails if:

- The actual behavior differs from the expected behavior.
- The invariant it tests is violated.
- The test is non-deterministic.

**The test suite is complete if every invariant from `03_invariants.md` is covered by at least one test.**

---

## Limitations of This Document

- The test count (~107) is a **proposal**; it will be revised after implementation.
- Some invariants are **hard** to test exhaustively; they are tested with property-based testing.
- Some invariants are **not testable** without simulation; they are tested in the simulation suite.
- The test design is **not a substitute** for the specification; it is a complement.

---

**End of Test Design (v2.0.0-draft).**
