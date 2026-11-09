# AetherGovern v2.0.0 — Operations

**Version:** 2.0.0-draft
**Date:** 2026-11-09
**Status:** Operational Specification (v2.0.0)
**Supersedes:** v0.1.0 (hypothesis only)
**Depends on:** `01_entities.md`
**Reference:** AetherGovern v0.1.0, DOI [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)

---

## Purpose

This document defines the operations of AetherGovern v2.0.0. Each operation is specified as:

- **Signature** (inputs, outputs, preconditions, postconditions)
- **Algorithm** (step-by-step)
- **Errors** (failure modes)
- **Invariants** (which invariants from `03_invariants.md` are preserved)

The operations are derived from the five-layer architecture of v0.1.0, but they are specified here as **executable functions** rather than as architectural concepts.

> **Methodological note.** v0.1.0 described the five layers conceptually. v2.0.0 specifies **seven operations** that implement the layers: `grant`, `delegate`, `revoke`, `check`, `apply_policy`, `escalate`, `rotate_key`. Each operation is testable; the test design is the subject of `05_test_design.md`.

---

## Overview

| # | Operation | Layer | Purpose |
|:-:|---|---|---|
| 1 | `grant` | Authorization | Issue a root delegation certificate |
| 2 | `delegate` | Authorization | Issue a child delegation certificate |
| 3 | `revoke` | Revocation | Withdraw a certificate |
| 4 | `check` | Authorization | Verify an authority chain at a frontier |
| 5 | `apply_policy` | Policy | Evaluate an action against a policy |
| 6 | `escalate` | Dispute Resolution | Escalate an unresolved conflict |
| 7 | `rotate_key` | Authorization | Replace an agent's public key |

---

## Operation 1 — `grant`

Issue a root delegation certificate from a recognized root to a subject.

### Signature

```python
def grant(
    root: Agent,
    subject: Agent,
    scope: Scope,
    expiry: str,
    root_private_key: bytes,
) -> DelegationCertificate
```

Preconditions

· root.status == AgentStatus.ACTIVE
· root is a recognized root of authority (in the root registry).
· subject.status == AgentStatus.ACTIVE
· expiry is in the future (relative to the current logical time).
· scope is non-empty.

Postconditions

· A new DelegationCertificate is created.
· certificate.issuer == root.agent_id
· certificate.subject == subject.agent_id
· certificate.parent_ref is None (root certificate)
· certificate.signature verifies against root.public_key
· The certificate is added to the key registry under subject.agent_id.

Algorithm

1. Validate preconditions.
2. Construct canonical certificate fields (issuer, subject, scope, constraints, expiry, parent_ref=None).
3. Compute certificate_id = SHA-256(canonical fields).
4. Sign certificate_id with root_private_key → signature.
5. Construct DelegationCertificate with all fields.
6. Register in key registry.
7. Return the certificate.

Errors

Error Condition
RootNotRecognizedError root is not in the root registry.
AgentInactiveError root.status != ACTIVE or subject.status != ACTIVE.
ExpiryInPastError expiry is in the past.
EmptyScopeError scope is empty.

Invariants Preserved

· I4.2 — Root recognition: the first certificate is issued by a recognized root.
· I4.4 — Signature covers content: the signature is over certificate_id.
· I1.3 — Registration completeness: both agents must be active.

Reference

· v0.1.0, Section 5.3 (Authority Delegation), "root of authority".

---

Operation 2 — delegate

Issue a child delegation certificate from an issuer to a subject, attenuating the issuer's scope.

Signature

```python
def delegate(
    issuer: Agent,
    subject: Agent,
    scope: Scope,
    expiry: str,
    parent_certificate: DelegationCertificate,
    issuer_private_key: bytes,
) -> DelegationCertificate
```

Preconditions

· issuer.status == AgentStatus.ACTIVE
· subject.status == AgentStatus.ACTIVE
· parent_certificate.subject == issuer.agent_id (issuer must be the parent's subject).
· parent_certificate is not expired.
· parent_certificate is not revoked at the issuer's current frontier.
· scope ⊆ parent_certificate.scope (attenuation).
· expiry <= parent_certificate.expiry (child expires no later than parent).

Postconditions

· A new DelegationCertificate is created.
· certificate.parent_ref == parent_certificate.certificate_id
· certificate.scope ⊆ parent_certificate.scope
· certificate.signature verifies against issuer.public_key

Algorithm

1. Validate preconditions.
2. Construct canonical certificate fields (issuer, subject, scope, constraints, expiry, parent_ref=parent_certificate.certificate_id).
3. Compute certificate_id = SHA-256(canonical fields).
4. Sign certificate_id with issuer_private_key → signature.
5. Construct DelegationCertificate.
6. Return the certificate.

Errors

Error Condition
NotParentSubjectError parent_certificate.subject != issuer.agent_id.
ParentExpiredError parent_certificate.expiry < now.
ParentRevokedError parent_certificate is in issuer.frontier.revocations.
AttenuationViolationError scope ⊄ parent_certificate.scope.
ExpiryExceedsParentError expiry > parent_certificate.expiry.

Invariants Preserved

· I4.1 — Attenuation: scope(c) ⊆ scope(parent_ref).
· I4.3 — Expiry: child expires no later than parent.
· I4.5 — No cycle: parent_ref prevents cycles.

Reference

· v0.1.0, Section 5.3 (Authority Delegation), "condition (b) scope attenuates".

---

Operation 3 — revoke

Withdraw a delegation certificate by issuing a revocation record.

Signature

```python
def revoke(
    issuer: Agent,
    certificate: DelegationCertificate,
    reason: str,
    issuer_private_key: bytes,
) -> RevocationRecord
```

Preconditions

· issuer.status == AgentStatus.ACTIVE
· issuer.agent_id is the certificate's issuer or an ancestor in the certificate's chain.
· certificate is not already revoked at the issuer's frontier.

Postconditions

· A new RevocationRecord is created.
· record.certificate_ref == certificate.certificate_id
· record.signature verifies against issuer.public_key
· The record is added to the issuer's frontier.
· All certificates whose parent chain includes certificate become invalid at the issuer's frontier.

Algorithm

1. Validate preconditions.
2. Construct canonical revocation fields (certificate_ref, issuer, reason, timestamp).
3. Compute revocation_id = SHA-256(canonical fields).
4. Sign revocation_id with issuer_private_key → signature.
5. Construct RevocationRecord.
6. Add to issuer's frontier.
7. Return the record.

Errors

Error Condition
NotAuthorizedToRevokeError issuer.agent_id is not the certificate's issuer or an ancestor.
AlreadyRevokedError certificate is already in issuer.frontier.revocations.

Invariants Preserved

· I5.1 — Monotonicity: adding a revocation can only invalidate.
· I5.2 — Signature covers content: the signature is over revocation_id.
· I5.3 — Issuer authority: the issuer must be the certificate's issuer or an ancestor.

Reference

· v0.1.0, Section 5.3.2 (Revocation and its exposure window).

---

Operation 4 — check

Verify an authority chain at a specified revocation frontier.

Signature

```python
def check(
    action: Action,
    chain: AuthorityChain,
    frontier: RevocationFrontier,
    current_time: str,
) -> CheckResult
```

Preconditions

· action.frontier_ref == frontier.frontier_id (the action cites the frontier being checked).
· action.authority_chain == chain.certificates (the action presents this chain).
· current_time is the logical time of the checking node.

Postconditions

· result.valid is True iff all five conditions of chain validity hold:
  · (a) every signature verifies
  · (b) scope attenuates: scope(c_{i+1}) ⊆ scope(c_i)
  · (c) no certificate has expired at current_time
  · (d) no certificate in the chain appears in frontier.revocations
  · (e) the first certificate's issuer is a recognized root

Algorithm

1. Validate preconditions.
2. For each certificate in chain.certificates:
   · Load certificate from registry.
   · Verify signature (condition a).
   · If not first: check scope(c) ⊆ scope(prev) (condition b).
   · Check current_time < certificate.expiry (condition c).
   · Check certificate.certificate_id ∉ frontier.revocations (condition d).
3. Check first certificate's issuer is a recognized root (condition e).
4. Return CheckResult(valid=True) if all pass, else CheckResult(valid=False, reason=...).

Errors

None. The operation always returns a CheckResult (valid or invalid).

Invariants Preserved

· I2.1 — Causal citation: the action cites the frontier being checked.
· I8.1 — Attenuation preserved: every certificate's scope is checked.
· I8.2 — Root recognized: the first certificate's issuer is checked.
· I8.4 — Contiguity: each certificate's issuer is the previous certificate's subject.

Reference

· v0.1.0, Section 5.3.1 (Causal-authority admission).

---

Operation 5 — apply_policy

Evaluate an action against a policy.

Signature

```python
def apply_policy(
    action: Action,
    policy: Policy,
) -> PolicyVerdict
```

Preconditions

· policy.status == PolicyStatus.ENFORCED
· policy.effective_from <= action.timestamp
· action.policy_ref == policy_hash(policy) (the action cites this policy version).

Postconditions

· verdict.decision ∈ {ALLOW, DENY, QUARANTINE}
· verdict.policy_id == policy.policy_id
· verdict.policy_version == policy.version
· The verdict is deterministic: same (action, policy) always gives the same verdict.

Algorithm

1. Validate preconditions.
2. For each rule in policy.rules:
   · Check if rule.action_kind == action.kind.
   · Check if action.resource matches rule.resource_pattern.
   · If match: return PolicyVerdict(decision=rule.verdict).
3. If no rule matches: return PolicyVerdict(decision=DENY) (default deny).

Errors

Error Condition
PolicyNotEnforcedError policy.status != ENFORCED.
PolicyNotEffectiveError policy.effective_from > action.timestamp.
PolicyRefMismatchError action.policy_ref != policy_hash(policy).

Invariants Preserved

· I6.1 — Version monotonicity: the policy version is cited in the verdict.
· I6.2 — Approval completeness: the policy must be approved before enforcement.
· I6.3 — Effective date: the policy must be effective at action time.

Reference

· v0.1.0, Section 5.2 (The Policy Lifecycle), "enforcement".

---

Operation 6 — escalate

Escalate an unresolved dispute to human review.

Signature

```python
def escalate(
    dispute: Dispute,
    reason: str,
    escalation_target: str,
) -> Dispute
```

Preconditions

· dispute.resolution == DisputeResolution.PENDING or ESCALATED (cannot escalate a resolved dispute).
· escalation_target is a non-empty human-review identifier.

Postconditions

· dispute.resolution == DisputeResolution.ESCALATED
· dispute.escalation_record is non-empty and contains reason and escalation_target.

Algorithm

1. Validate preconditions.
2. Construct escalation_record = {reason, escalation_target, timestamp}.
3. Return new Dispute with resolution=ESCALATED and escalation_record.

Errors

Error Condition
DisputeAlreadyResolvedError dispute.resolution == RESOLVED_BY_RULE.
EmptyEscalationTargetError escalation_target == "".

Invariants Preserved

· I9.2 — Escalation completeness: escalation_record must be non-empty.
· I9.3 — No silent resolution: the dispute is explicitly escalated.

Reference

· v0.1.0, Section 5.1 (Layer 5 — Dispute Resolution), "escalate".

---

Operation 7 — rotate_key

Replace an agent's public key with a new one.

Signature

```python
def rotate_key(
    agent: Agent,
    new_public_key: bytes,
    new_key_id: str,
    old_private_key: bytes,
) -> Agent
```

Preconditions

· agent.status == AgentStatus.ACTIVE
· new_public_key is not already registered to another agent.
· old_private_key verifies against agent.public_key (proof of ownership).

Postconditions

· The agent's public_key is replaced with new_public_key.
· The agent's key_id is replaced with new_key_id.
· All existing delegation certificates issued by the agent remain valid (the agent's identity is unchanged).
· A KeyRotationRecord is added to the key registry for audit.

Algorithm

1. Validate preconditions.
2. Verify old_private_key against agent.public_key (proof of ownership).
3. Construct a KeyRotationRecord (old_key, new_key, timestamp, signature).
4. Update key registry.
5. Return new Agent with updated public_key and key_id.

Errors

Error Condition
AgentInactiveError agent.status != ACTIVE.
KeyAlreadyRegisteredError new_public_key is already registered.
OwnershipProofError old_private_key does not verify against agent.public_key.

Invariants Preserved

· I1.1 — Key uniqueness: new_public_key must not be registered elsewhere.
· I1.2 — Status monotonicity: rotation does not change the agent's status.

Reference

· v0.1.0, Section 5.1 (Layer 1 — Authorization), "rotate keys".

---

Summary

# Operation Inputs Outputs Errors Invariants
1 grant 5 1 4 3
2 delegate 6 1 5 3
3 revoke 4 1 2 3
4 check 4 1 0 4
5 apply_policy 2 1 3 3
6 escalate 3 1 2 2
7 rotate_key 4 1 3 2

Total: 7 operations, 28 inputs, 7 outputs, 19 errors, 20 invariants preserved.

---

Limitations of This Document

· The operations are specifications, not implementations. No code is claimed.
· The signatures are proposals; they may be revised as the implementation and tests reveal gaps.
· The error types are proposals; the exact exception hierarchy will be fixed in the implementation.
· The invariants preserved are claimed; they will be tested in tests/ (see 05_test_design.md).

---

End of Operations (v2.0.0-draft).
