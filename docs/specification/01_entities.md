# AetherGovern v2.0.0 — Entities

**Version:** 2.0.0-draft
**Date:** 2026-11-09
**Status:** Operational Specification (v2.0.0)
**Supersedes:** v0.1.0 (hypothesis only)
**Reference:** AetherGovern v0.1.0, DOI [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)

---

## Purpose

This document defines the ten core entities of AetherGovern v2.0.0. These entities are the operational specification that will be implemented in `src/aethergovern/` and tested in `tests/`.

The entities are derived from the five-layer architecture of v0.1.0 (Authorization, Policy, Accountability, Revocation, Dispute Resolution), but they are specified here as **concrete, implementable data structures** rather than as architectural concepts.

> **Methodological note.** v0.1.0 described the five layers as a hypothesis. v2.0.0 converts them into **testable entities** with explicit fields, operations, and invariants. The invariants are the subject of `03_invariants.md`; the operations are the subject of `02_operations.md`.

---

## Overview

| # | Entity | Layer | Purpose |
|:-:|---|---|---|
| 1 | Agent | Authorization | The actor: identity, key, record |
| 2 | Action | Authorization | The operation: commit, merge, delete, deploy, rotate_key |
| 3 | Resource | Authorization | The target: branch, path, key |
| 4 | DelegationCertificate | Authorization | The signed grant of scope from issuer to subject |
| 5 | RevocationRecord | Revocation | The signed withdrawal of a certificate |
| 6 | Policy | Policy | The rule that governs authorization |
| 7 | RevocationFrontier | Revocation | The set of revocation records an actor has seen |
| 8 | AuthorityChain | Authorization | The sequence of certificates from root to agent |
| 9 | Dispute | Dispute Resolution | The conflict between two authority claims |
| 10 | AccountabilityRecord | Accountability | The after-the-fact trace of an admitted action |

---

## Entity 1 — Agent

An **Agent** is an autonomous software actor, identified by a key, that proposes changes.

### Fields

| Field | Type | Description |
|---|---|---|
| `agent_id` | `str` | Stable identifier (e.g., `"agent-001"`). |
| `public_key` | `bytes` | Ed25519 public key (32 bytes). |
| `key_id` | `str` | Identifier for the public key (for lookup). |
| `role` | `Optional[str]` | Optional role label (e.g., `"reviewer"`, `"maintainer"`). |
| `registered_at` | `str` | ISO-8601 timestamp of registration. |
| `status` | `AgentStatus` | `active`, `suspended`, `revoked`. |

### Relations

- An Agent **issues** zero or more `DelegationCertificate`s.
- An Agent **receives** zero or more `DelegationCertificate`s.
- An Agent **performs** zero or more `Action`s.
- An Agent **has** one `public_key` registered in the key registry.

### Invariants

- **I1.1 — Key uniqueness:** No two agents may share the same `public_key`.
- **I1.2 — Status monotonicity:** Once `revoked`, an agent cannot return to `active`.
- **I1.3 — Registration completeness:** An agent cannot perform an `Action` unless its `status` is `active`.

### Python (illustrative)

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class AgentStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

@dataclass(frozen=True)
class Agent:
    agent_id: str
    public_key: bytes
    key_id: str
    role: Optional[str]
    registered_at: str
    status: AgentStatus
```

Reference

· v0.1.0, Section 5.1 (Layer 1 — Authorization), "Agent identity".

---

Entity 2 — Action

An Action is an operation by an agent on a resource.

Fields

Field Type Description
action_id str Content-addressed identifier (SHA-256).
kind ActionKind commit, merge, delete, deploy, rotate_key.
actor str agent_id of the actor.
resource str resource_id of the target.
payload dict Action-specific data (e.g., diff hash, key bytes).
timestamp str ISO-8601 timestamp (actor-reported).
frontier_ref str Hash of the RevocationFrontier cited by the actor.
policy_ref str Hash of the Policy version cited by the actor.
authority_chain List[str] List of certificate_ids from root to actor.
signature bytes Actor's signature over the canonical action (excluding signature).

Relations

· An Action is performed by one Agent.
· An Action targets one Resource.
· An Action cites one RevocationFrontier and one Policy.
· An Action presents one AuthorityChain.
· An Action produces one AccountabilityRecord (after admission).

Invariants

· I2.1 — Causal citation: Every Action must cite a frontier_ref and a policy_ref that are in its causal closure.
· I2.2 — Content addressing: action_id = SHA-256 of the canonical action (excluding signature).
· I2.3 — Signature covers content: The signature is over action_id.
· I2.4 — Chain completeness: The authority_chain must be non-empty and must start with a root certificate.

Python (illustrative)

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class ActionKind(str, Enum):
    COMMIT = "commit"
    MERGE = "merge"
    DELETE = "delete"
    DEPLOY = "deploy"
    ROTATE_KEY = "rotate_key"

@dataclass(frozen=True)
class Action:
    action_id: str
    kind: ActionKind
    actor: str
    resource: str
    payload: Dict
    timestamp: str
    frontier_ref: str
    policy_ref: str
    authority_chain: List[str]
    signature: bytes
```

Reference

· v0.1.0, Section 5.1 (Layer 1 — Authorization), "action, resource, scope".

---

Entity 3 — Resource

A Resource is the target of an action.

Fields

Field Type Description
resource_id str Stable identifier (e.g., "branch/main", "path/src/a.py").
kind ResourceKind branch, path, key.
owner str agent_id of the resource owner (for key resources).
metadata dict Optional metadata.

Relations

· A Resource is targeted by zero or more Actions.
· A Resource is scoped by zero or more DelegationCertificates.

Invariants

· I3.1 — Identifier stability: A resource's resource_id cannot change after creation.
· I3.2 — Kind immutability: A resource's kind cannot change after creation.

Python (illustrative)

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class ResourceKind(str, Enum):
    BRANCH = "branch"
    PATH = "path"
    KEY = "key"

@dataclass(frozen=True)
class Resource:
    resource_id: str
    kind: ResourceKind
    owner: str
    metadata: Dict
```

Reference

· v0.1.0, Section 5.1 (Layer 1 — Authorization), "resource".

---

Entity 4 — DelegationCertificate

A DelegationCertificate is a signed grant of scope from an issuer to a subject.

Fields

Field Type Description
certificate_id str Content-addressed identifier (SHA-256).
issuer str agent_id of the issuer.
subject str agent_id of the subject.
scope Scope Set of (action_kind, resource_id) pairs.
constraints dict Optional constraints (e.g., time window, rate limit).
expiry str ISO-8601 timestamp after which the certificate is invalid.
parent_ref Optional[str] certificate_id of the parent certificate, or None for root.
signature bytes Issuer's signature over the canonical certificate (excluding signature).

Relations

· A DelegationCertificate is issued by one Agent.
· A DelegationCertificate is issued to one Agent.
· A DelegationCertificate may have one parent certificate.
· A DelegationCertificate may be revoked by one RevocationRecord.
· A DelegationCertificate scopes zero or more Resources.

Invariants

· I4.1 — Attenuation: scope(c) ⊆ scope(parent_ref) for every non-root certificate.
· I4.2 — Root recognition: The first certificate in a chain must be issued by a recognized root.
· I4.3 — Expiry: A certificate is invalid after its expiry timestamp.
· I4.4 — Signature covers content: The signature is over certificate_id.
· I4.5 — No cycle: The parent chain cannot form a cycle.

Python (illustrative)

```python
from dataclasses import dataclass
from typing import Dict, FrozenSet, Optional, Tuple

Scope = FrozenSet[Tuple[str, str]]  # (action_kind, resource_id)

@dataclass(frozen=True)
class DelegationCertificate:
    certificate_id: str
    issuer: str
    subject: str
    scope: Scope
    constraints: Dict
    expiry: str
    parent_ref: Optional[str]
    signature: bytes
```

Reference

· v0.1.0, Section 5.3 (Authority Delegation), "Delegation certificate".

---

Entity 5 — RevocationRecord

A RevocationRecord is a signed withdrawal of a certificate.

Fields

Field Type Description
revocation_id str Content-addressed identifier (SHA-256).
certificate_ref str certificate_id of the revoked certificate.
issuer str agent_id of the revoking agent.
reason str Human-readable reason (e.g., "key compromise").
timestamp str ISO-8601 timestamp of revocation.
signature bytes Issuer's signature over the canonical record.

Relations

· A RevocationRecord revokes one DelegationCertificate.
· A RevocationRecord is issued by one Agent.
· A RevocationRecord is part of zero or more RevocationFrontiers.

Invariants

· I5.1 — Monotonicity: Adding a RevocationRecord to a frontier can only invalidate certificates, never validate them.
· I5.2 — Signature covers content: The signature is over revocation_id.
· I5.3 — Issuer authority: The issuer must be the same as (or an ancestor of) the certificate's issuer.

Python (illustrative)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class RevocationRecord:
    revocation_id: str
    certificate_ref: str
    issuer: str
    reason: str
    timestamp: str
    signature: bytes
```

Reference

· v0.1.0, Section 5.3.2 (Revocation and its exposure window), "Revocation set".

---

Entity 6 — Policy

A Policy is a rule that governs authorization.

Fields

Field Type Description
policy_id str Stable identifier (e.g., "policy-001").
version int Monotonically increasing version.
rules List[Rule] List of authorization rules.
approval_chain List[str] agent_ids that approved the policy.
status PolicyStatus proposed, approved, enforced, revoked.
created_at str ISO-8601 timestamp.
effective_from str ISO-8601 timestamp.
supersedes Optional[str] policy_id of the previous policy, or None.

Relations

· A Policy is approved by one or more Agents.
· A Policy is cited by zero or more Actions.
· A Policy may supersede one previous Policy.

Invariants

· I6.1 — Version monotonicity: A policy's version cannot decrease.
· I6.2 — Approval completeness: A policy cannot be enforced unless its approval_chain is non-empty.
· I6.3 — Effective date: A policy cannot be enforced before its effective_from timestamp.
· I6.4 — Supersession chain: The supersedes chain cannot form a cycle.

Python (illustrative)

```python
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

class PolicyStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    ENFORCED = "enforced"
    REVOKED = "revoked"

@dataclass(frozen=True)
class Rule:
    action_kind: str
    resource_pattern: str
    verdict: str  # "allow", "deny", "quarantine"

@dataclass(frozen=True)
class Policy:
    policy_id: str
    version: int
    rules: List[Rule]
    approval_chain: List[str]
    status: PolicyStatus
    created_at: str
    effective_from: str
    supersedes: Optional[str]
```

Reference

· v0.1.0, Section 5.2 (The Policy Lifecycle).

---

Entity 7 — RevocationFrontier

A RevocationFrontier is the set of revocation records an actor has seen.

Fields

Field Type Description
frontier_id str Content-addressed identifier (SHA-256 of sorted revocation_ids).
revocations FrozenSet[str] Set of revocation_ids.
created_at str ISO-8601 timestamp.

Relations

· A RevocationFrontier contains zero or more RevocationRecords.
· A RevocationFrontier is cited by zero or more Actions.

Invariants

· I7.1 — Grow-only: A frontier can only grow (revocations can be added, never removed).
· I7.2 — Join is union: frontier_a ⊔ frontier_b = frontier_a.revocations ∪ frontier_b.revocations.
· I7.3 — Content addressing: frontier_id = SHA-256 of sorted revocation_ids.

Python (illustrative)

```python
from dataclasses import dataclass
from typing import FrozenSet

@dataclass(frozen=True)
class RevocationFrontier:
    frontier_id: str
    revocations: FrozenSet[str]
    created_at: str
```

Reference

· v0.1.0, Section 5.3.1 (Causal-authority admission), "revocation frontier F".

---

Entity 8 — AuthorityChain

An AuthorityChain is a sequence of delegation certificates from a root to an agent.

Fields

Field Type Description
chain_id str Content-addressed identifier (SHA-256 of certificate_ids).
certificates List[str] Ordered list of certificate_ids, from root to leaf.
leaf_agent str agent_id of the leaf (the agent whose authority is being proven).
leaf_scope Scope Effective scope of the chain (intersection of all scopes).

Relations

· An AuthorityChain contains one or more DelegationCertificates.
· An AuthorityChain is presented by one Action.
· An AuthorityChain is rooted at one root certificate.

Invariants

· I8.1 — Attenuation preserved: The effective leaf_scope must be a subset of every certificate's scope in the chain.
· I8.2 — Root recognized: The first certificate must be issued by a recognized root.
· I8.3 — No cycle: The chain cannot contain a cycle.
· I8.4 — Contiguity: Each certificate's issuer must be the previous certificate's subject.

Python (illustrative)

```python
from dataclasses import dataclass
from typing import List, FrozenSet, Tuple

Scope = FrozenSet[Tuple[str, str]]

@dataclass(frozen=True)
class AuthorityChain:
    chain_id: str
    certificates: List[str]
    leaf_agent: str
    leaf_scope: Scope
```

Reference

· v0.1.0, Section 5.3 (Authority Delegation), "chain validity at frontier F".

---

Entity 9 — Dispute

A Dispute is the conflict between two authority claims.

Fields

Field Type Description
dispute_id str Content-addressed identifier (SHA-256).
claim_a AuthorityChain First authority claim.
claim_b AuthorityChain Second authority claim.
precedence_rule Optional[str] Deterministic rule applied ("more_restrictive", "later_expiry", "root_depth").
resolution DisputeResolution pending, resolved_by_rule, escalated.
escalation_record Optional[dict] Escalation details (if unresolved).
created_at str ISO-8601 timestamp.

Relations

· A Dispute involves two AuthorityChains.
· A Dispute may be resolved by one precedence rule.
· A Dispute may be escalated to human review.

Invariants

· I9.1 — Determinism: If precedence_rule is applied, the resolution must be deterministic.
· I9.2 — Escalation completeness: If resolution = escalated, escalation_record must be non-empty.
· I9.3 — No silent resolution: A dispute cannot be resolved_by_rule if no rule applies.

Python (illustrative)

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict

class DisputeResolution(str, Enum):
    PENDING = "pending"
    RESOLVED_BY_RULE = "resolved_by_rule"
    ESCALATED = "escalated"

@dataclass(frozen=True)
class Dispute:
    dispute_id: str
    claim_a: "AuthorityChain"
    claim_b: "AuthorityChain"
    precedence_rule: Optional[str]
    resolution: DisputeResolution
    escalation_record: Optional[Dict]
    created_at: str
```

Reference

· v0.1.0, Section 5.1 (Layer 5 — Dispute Resolution).

---

Entity 10 — AccountabilityRecord

An AccountabilityRecord is the after-the-fact trace of an admitted action.

Fields

Field Type Description
record_id str Content-addressed identifier (SHA-256).
action_ref str action_id of the admitted action.
authority_chain_ref str chain_id of the authority chain presented.
admitted_at str ISO-8601 timestamp of admission.
admitted_by str agent_id of the admitting node.
prev_record_hash str Hash of the previous record (hash-linked log).
signature bytes Admitting node's signature over the canonical record.

Relations

· An AccountabilityRecord traces one Action.
· An AccountabilityRecord references one AuthorityChain.
· An AccountabilityRecord links to one previous AccountabilityRecord.

Invariants

· I10.1 — Immutability: Once created, an AccountabilityRecord cannot be modified.
· I10.2 — Hash-link integrity: prev_record_hash must match the previous record's record_id.
· I10.3 — Attribution completeness: Every admitted Action must have exactly one AccountabilityRecord.
· I10.4 — Signature covers content: The signature is over record_id.

Python (illustrative)

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class AccountabilityRecord:
    record_id: str
    action_ref: str
    authority_chain_ref: str
    admitted_at: str
    admitted_by: str
    prev_record_hash: str
    signature: bytes
```

Reference

· v0.1.0, Section 5.1 (Layer 3 — Accountability), "Action record; chain of authority; signature; hash link".

---

Summary

# Entity Fields Relations Invariants
1 Agent 6 4 3
2 Action 10 5 4
3 Resource 4 2 2
4 DelegationCertificate 8 5 5
5 RevocationRecord 6 3 3
6 Policy 8 3 4
7 RevocationFrontier 3 2 3
8 AuthorityChain 4 3 4
9 Dispute 7 3 3
10 AccountabilityRecord 7 3 4

Total: 10 entities, 63 fields, 33 relations, 35 invariants.

---

Limitations of This Document

· The entities are operational specifications, not implementations. No code is claimed.
· The fields are proposals; they may be revised as the implementation and tests reveal gaps.
· The invariants are testable properties; they will be tested in tests/ (see 05_test_design.md).
· The relations are conceptual; the exact cardinality (one-to-one, one-to-many) will be fixed in the implementation.

---

End of Entities (v2.0.0-draft).
