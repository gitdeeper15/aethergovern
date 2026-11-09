# AetherGovern v2.0.0 — Invariants

**Version:** 2.0.0-draft
**Date:** 2026-11-09
**Status:** Operational Specification (v2.0.0)
**Depends on:** `01_entities.md`, `02_operations.md`
**Reference:** AetherGovern v0.1.0, DOI [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)

---

## Purpose

This document collects the invariants introduced in `01_entities.md` and `02_operations.md`, states each one as a **testable property**, and assigns it to a test category. The invariants are the contract between the specification and the implementation: if the implementation violates an invariant, the test must fail.

Each invariant is stated as:

- **ID** — stable identifier (e.g., I4.1).
- **Entity / operation** — which entity or operation it constrains.
- **Statement** — the property, stated formally.
- **Rationale** — why it matters.
- **Test category** — how it will be tested (unit, property-based, integration, or simulation).
- **Failure mode** — what goes wrong if the invariant is violated.

> **Methodological note.** v0.1.0 stated the invariants informally (as conditions on chain validity and admission determinism). v2.0.0 states them as **testable properties**. Each invariant corresponds to at least one test in `tests/` (see `05_test_design.md`).

---

## Summary

| Category | Invariants | Count |
|:-:|---|:-:|
| Structural (entities) | I1.1–I1.3, I2.1–I2.4, I3.1–I3.2, I4.1–I4.5, I5.1–I5.3, I6.1–I6.4, I7.1–I7.3, I8.1–I8.4, I9.1–I9.3, I10.1–I10.4 | 35 |
| Operational (operations) | O1–O7 (one per operation) | 7 |
| Cross-cutting | X1–X5 | 5 |
| **Total** | | **47** |

---

## Structural Invariants (Entities)

### Agent (Entity 1)

**I1.1 — Key uniqueness.** No two agents may share the same `public_key`.

- **Statement:** ∀ a, b ∈ Agents: a ≠ b ⇒ a.public_key ≠ b.public_key.
- **Rationale:** Duplicate keys would make attribution ambiguous.
- **Test category:** unit.
- **Failure mode:** Two agents sign the same action; attribution is indeterminate.

**I1.2 — Status monotonicity.** Once `revoked`, an agent cannot return to `active`.

- **Statement:** ∀ agent: agent.status = revoked ⇒ agent.status cannot transition to active.
- **Rationale:** Prevents resurrection of compromised identities.
- **Test category:** unit.
- **Failure mode:** A compromised agent returns to active and performs actions.

**I1.3 — Registration completeness.** An agent cannot perform an Action unless its `status` is `active`.

- **Statement:** ∀ action, agent: action.actor = agent.agent_id ⇒ agent.status = active.
- **Rationale:** Suspended and revoked agents must not act.
- **Test category:** integration.
- **Failure mode:** A suspended agent commits a change.

---

### Action (Entity 2)

**I2.1 — Causal citation.** Every Action must cite a `frontier_ref` and a `policy_ref` that are in its causal closure.

- **Statement:** ∀ action: frontier(action.frontier_ref) ∈ closure(action) ∧ policy(action.policy_ref) ∈ closure(action).
- **Rationale:** Determinism of admission requires the cited frontier and policy to be part of the action's causal past.
- **Test category:** property-based.
- **Failure mode:** Two honest nodes evaluate the same action against different frontiers; verdicts diverge.

**I2.2 — Content addressing.** `action_id` = SHA-256 of the canonical action (excluding signature).

- **Statement:** ∀ action: action.action_id = SHA256(canonical(action)).
- **Rationale:** Tamper-evidence.
- **Test category:** unit.
- **Failure mode:** An action is altered in transit; the change is undetected.

**I2.3 — Signature covers content.** The signature is over `action_id`.

- **Statement:** ∀ action: Verify(action.signature, action.action_id, actor.public_key) = True.
- **Rationale:** Provenance.
- **Test category:** unit.
- **Failure mode:** An action is forged by a non-actor.

**I2.4 — Chain completeness.** The `authority_chain` must be non-empty and must start with a root certificate.

- **Statement:** ∀ action: len(action.authority_chain) ≥ 1 ∧ root(action.authority_chain[0]).
- **Rationale:** No action without authority.
- **Test category:** unit.
- **Failure mode:** An action with no authority chain is admitted.

---

### Resource (Entity 3)

**I3.1 — Identifier stability.** A resource's `resource_id` cannot change after creation.

- **Statement:** ∀ resource: resource.resource_id is immutable.
- **Rationale:** References to resources must remain valid.
- **Test category:** unit.
- **Failure mode:** A reference to a resource points to a different resource.

**I3.2 — Kind immutability.** A resource's `kind` cannot change after creation.

- **Statement:** ∀ resource: resource.kind is immutable.
- **Rationale:** Authorization scopes are keyed on resource kind.
- **Test category:** unit.
- **Failure mode:** A branch is reinterpreted as a path; scope checks are bypassed.

---

### DelegationCertificate (Entity 4)

**I4.1 — Attenuation.** `scope(c) ⊆ scope(parent_ref)` for every non-root certificate.

- **Statement:** ∀ c ∈ Certificates, c.parent_ref ≠ None ⇒ scope(c) ⊆ scope(parent_ref).
- **Rationale:** No agent can grant more than it holds.
- **Test category:** property-based.
- **Failure mode:** A delegate escalates its own scope.

**I4.2 — Root recognition.** The first certificate in a chain must be issued by a recognized root.

- **Statement:** ∀ chain: root(chain.certificates[0].issuer) = True.
- **Rationale:** Trust anchoring.
- **Test category:** integration.
- **Failure mode:** An unrecognized agent acts as a root.

**I4.3 — Expiry.** A certificate is invalid after its `expiry` timestamp.

- **Statement:** ∀ c, t: t > c.expiry ⇒ Valid(c, t) = False.
- **Rationale:** Time-bounded grants.
- **Test category:** unit.
- **Failure mode:** An expired certificate is used to perform an action.

**I4.4 — Signature covers content.** The signature is over `certificate_id`.

- **Statement:** ∀ c: Verify(c.signature, c.certificate_id, c.issuer.public_key) = True.
- **Rationale:** Provenance.
- **Test category:** unit.
- **Failure mode:** A certificate is forged.

**I4.5 — No cycle.** The parent chain cannot form a cycle.

- **Statement:** ∀ c: c ∉ ancestors(c).
- **Rationale:** Termination of chain verification.
- **Test category:** property-based.
- **Failure mode:** Chain verification loops indefinitely.

---

### RevocationRecord (Entity 5)

**I5.1 — Monotonicity.** Adding a RevocationRecord to a frontier can only invalidate certificates, never validate them.

- **Statement:** ∀ c, F, F': F ⊆ F' ⇒ Valid(c, F') ⇒ Valid(c, F).
- **Rationale:** Revocation is monotone; it cannot be undone by adding records.
- **Test category:** property-based.
- **Failure mode:** Adding a revocation makes a previously invalid certificate valid.

**I5.2 — Signature covers content.** The signature is over `revocation_id`.

- **Statement:** ∀ r: Verify(r.signature, r.revocation_id, r.issuer.public_key) = True.
- **Rationale:** Provenance.
- **Test category:** unit.
- **Failure mode:** A revocation is forged.

**I5.3 — Issuer authority.** The issuer must be the same as (or an ancestor of) the certificate's issuer.

- **Statement:** ∀ r: r.issuer ∈ ancestors(r.certificate_ref.issuer) ∪ {r.certificate_ref.issuer}.
- **Rationale:** Only the grantor (or an ancestor) can revoke.
- **Test category:** integration.
- **Failure mode:** An arbitrary agent revokes another's certificate.

---

### Policy (Entity 6)

**I6.1 — Version monotonicity.** A policy's version cannot decrease.

- **Statement:** ∀ p, p': p' supersedes p ⇒ p'.version > p.version.
- **Rationale:** Determinism of policy enforcement.
- **Test category:** unit.
- **Failure mode:** A policy is rolled back silently.

**I6.2 — Approval completeness.** A policy cannot be `enforced` unless its `approval_chain` is non-empty.

- **Statement:** ∀ p: p.status = enforced ⇒ len(p.approval_chain) ≥ 1.
- **Rationale:** Policies must be approved.
- **Test category:** unit.
- **Failure mode:** An unapproved policy is enforced.

**I6.3 — Effective date.** A policy cannot be `enforced` before its `effective_from` timestamp.

- **Statement:** ∀ p, t: p.status = enforced ∧ t < p.effective_from ⇒ Enforcement(p, t) = False.
- **Rationale:** Time-bounded enforcement.
- **Test category:** unit.
- **Failure mode:** A policy is enforced before its effective date.

**I6.4 — Supersession chain.** The `supersedes` chain cannot form a cycle.

- **Statement:** ∀ p: p ∉ ancestors(p).
- **Rationale:** Termination of policy lookup.
- **Test category:** property-based.
- **Failure mode:** Policy lookup loops indefinitely.

---

### RevocationFrontier (Entity 7)

**I7.1 — Grow-only.** A frontier can only grow (revocations can be added, never removed).

- **Statement:** ∀ F, F': F ⊆ F' or F' ⊆ F (no removal).
- **Rationale:** Revocation is monotone.
- **Test category:** property-based.
- **Failure mode:** A revocation is removed from a frontier.

**I7.2 — Join is union.** `frontier_a ⊔ frontier_b = frontier_a.revocations ∪ frontier_b.revocations`.

- **Statement:** ∀ F1, F2: Join(F1, F2) = F1 ∪ F2.
- **Rationale:** Frontier is a join-semilattice.
- **Test category:** unit.
- **Failure mode:** Join is not commutative or associative.

**I7.3 — Content addressing.** `frontier_id` = SHA-256 of sorted `revocation_id`s.

- **Statement:** ∀ F: F.frontier_id = SHA256(sorted(F.revocations)).
- **Rationale:** Tamper-evidence.
- **Test category:** unit.
- **Failure mode:** A frontier is altered without detection.

---

### AuthorityChain (Entity 8)

**I8.1 — Attenuation preserved.** The effective `leaf_scope` must be a subset of every certificate's scope in the chain.

- **Statement:** ∀ chain, c ∈ chain: chain.leaf_scope ⊆ scope(c).
- **Rationale:** The effective scope is the intersection of all scopes.
- **Test category:** property-based.
- **Failure mode:** The effective scope is larger than some certificate's scope.

**I8.2 — Root recognized.** The first certificate must be issued by a recognized root.

- **Statement:** ∀ chain: root(chain.certificates[0].issuer) = True.
- **Rationale:** Trust anchoring.
- **Test category:** integration.
- **Failure mode:** An unrecognized chain is accepted.

**I8.3 — No cycle.** The chain cannot contain a cycle.

- **Statement:** ∀ chain: no self-reference in chain.certificates.
- **Rationale:** Termination.
- **Test category:** property-based.
- **Failure mode:** Chain traversal loops.

**I8.4 — Contiguity.** Each certificate's issuer must be the previous certificate's subject.

- **Statement:** ∀ i ∈ [1, len(chain)-1]: chain.certificates[i].issuer = chain.certificates[i-1].subject.
- **Rationale:** Chain integrity.
- **Test category:** unit.
- **Failure mode:** A certificate is inserted out of order.

---

### Dispute (Entity 9)

**I9.1 — Determinism.** If `precedence_rule` is applied, the resolution must be deterministic.

- **Statement:** ∀ dispute, same inputs ⇒ same resolution.
- **Rationale:** Predictable dispute outcomes.
- **Test category:** property-based.
- **Failure mode:** Two nodes resolve the same dispute differently.

**I9.2 — Escalation completeness.** If `resolution = escalated`, `escalation_record` must be non-empty.

- **Statement:** ∀ dispute: resolution = escalated ⇒ escalation_record ≠ ∅.
- **Rationale:** Escalation must be traceable.
- **Test category:** unit.
- **Failure mode:** A dispute is marked escalated with no record.

**I9.3 — No silent resolution.** A dispute cannot be `resolved_by_rule` if no rule applies.

- **Statement:** ∀ dispute: resolution = resolved_by_rule ⇒ precedence_rule ≠ None.
- **Rationale:** No arbitrary resolution.
- **Test category:** unit.
- **Failure mode:** A dispute is resolved without a rule.

---

### AccountabilityRecord (Entity 10)

**I10.1 — Immutability.** Once created, an AccountabilityRecord cannot be modified.

- **Statement:** ∀ r: r is immutable after creation.
- **Rationale:** Audit trail integrity.
- **Test category:** unit.
- **Failure mode:** An audit record is altered.

**I10.2 — Hash-link integrity.** `prev_record_hash` must match the previous record's `record_id`.

- **Statement:** ∀ r: r.prev_record_hash = previous(r).record_id.
- **Rationale:** Chain integrity.
- **Test category:** integration.
- **Failure mode:** A record is removed from the chain.

**I10.3 — Attribution completeness.** Every admitted Action must have exactly one AccountabilityRecord.

- **Statement:** ∀ action admitted: count(records for action) = 1.
- **Rationale:** Every action must be traceable.
- **Test category:** integration.
- **Failure mode:** An action is admitted with no record (or with duplicates).

**I10.4 — Signature covers content.** The signature is over `record_id`.

- **Statement:** ∀ r: Verify(r.signature, r.record_id, r.admitted_by.public_key) = True.
- **Rationale:** Provenance of admission.
- **Test category:** unit.
- **Failure mode:** A record is forged.

---

## Operational Invariants (Operations)

**O1 — `grant` preserves I4.2, I4.4, I1.3.**
**O2 — `delegate` preserves I4.1, I4.3, I4.5.**
**O3 — `revoke` preserves I5.1, I5.2, I5.3.**
**O4 — `check` preserves I2.1, I8.1, I8.2, I8.4.**
**O5 — `apply_policy` preserves I6.1, I6.2, I6.3.**
**O6 — `escalate` preserves I9.2, I9.3.**
**O7 — `rotate_key` preserves I1.1, I1.2.**

Each operational invariant is a **claim** that the corresponding operation, when implemented, will not violate the stated structural invariants. The claim is tested in `tests/` (see `05_test_design.md`).

---

## Cross-Cutting Invariants

**X1 — Determinism (A6).** The admission predicate is a pure function of the action and its causal closure.

- **Statement:** ∀ action, nodes n1, n2 with same causal closure: verdict(n1, action) = verdict(n2, action).
- **Rationale:** Convergence (from AetherMesh's A6).
- **Test category:** property-based.
- **Failure mode:** Honest nodes diverge.

**X2 — Monotonic revocation.** Revocation is monotone; adding revocations can only invalidate.

- **Statement:** ∀ action, F, F': F ⊆ F' ⇒ Valid(action, F') ⇒ Valid(action, F).
- **Rationale:** Consistency of revocation across nodes.
- **Test category:** property-based.
- **Failure mode:** A revocation is "undone" by receiving more records.

**X3 — Attribution completeness.** Every admitted action is traceable to a chain.

- **Statement:** ∀ action admitted: ∃ record r: r.action_ref = action.action_id.
- **Rationale:** Accountability.
- **Test category:** integration.
- **Failure mode:** An action is admitted with no trace.

**X4 — Authority–evidence separation.** Authority records ≠ evidence records.

- **Statement:** ∀ r: r is either an authority record or an evidence record, not both.
- **Rationale:** Separation of concerns (from v0.1.0, Section 5.5).
- **Test category:** unit.
- **Failure mode:** Evidence is used as authority (category error).

**X5 — No root ambiguity.** The set of roots is fixed and known to all honest nodes.

- **Statement:** ∀ nodes n1, n2: roots(n1) = roots(n2).
- **Rationale:** Trust anchoring.
- **Test category:** integration.
- **Failure mode:** Two nodes disagree on who is a root.

---

## Summary

| ID range | Count | Category |
|:-:|:-:|---|
| I1.1–I1.3 | 3 | Agent |
| I2.1–I2.4 | 4 | Action |
| I3.1–I3.2 | 2 | Resource |
| I4.1–I4.5 | 5 | DelegationCertificate |
| I5.1–I5.3 | 3 | RevocationRecord |
| I6.1–I6.4 | 4 | Policy |
| I7.1–I7.3 | 3 | RevocationFrontier |
| I8.1–I8.4 | 4 | AuthorityChain |
| I9.1–I9.3 | 3 | Dispute |
| I10.1–I10.4 | 4 | AccountabilityRecord |
| O1–O7 | 7 | Operational |
| X1–X5 | 5 | Cross-cutting |
| **Total** | **47** | |

---

## Limitations of This Document

- The invariants are **claims**; they will be tested in `tests/` (see `05_test_design.md`).
- Some invariants are **hard** to test exhaustively (e.g., I4.5, I8.3, X1); they will be tested with **property-based testing** (Hypothesis).
- Some invariants are **not testable** without a distributed setting (e.g., X1, X2, X5); they will be tested in **simulation**.
- The list is **not exhaustive**; additional invariants may be discovered during implementation.

---

**End of Invariants (v2.0.0-draft).**
