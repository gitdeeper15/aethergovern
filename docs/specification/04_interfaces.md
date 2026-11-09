# AetherGovern v2.0.0 — Interfaces

**Version:** 2.0.0-draft
**Date:** 2026-11-09
**Status:** Operational Specification (v2.0.0)
**Depends on:** `01_entities.md`, `02_operations.md`, `03_invariants.md`
**Reference:** AetherGovern v0.1.0, DOI [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)

---

## Purpose

This document defines the four interfaces between AetherGovern and the existing Aether dimensions:

| # | Dimension | System | Interface purpose |
|:-:|---|---|---|
| 1 | Storage | AetherGit | Read changeset log; append governance records |
| 2 | Integration | AetherFlow | Admission hook; authorization verdicts |
| 3 | Verification | AetherProof | Designate governed specification changes |
| 4 | Decentralization | AetherMesh | Delta replication; determinism-compatible predicate |

Each interface is specified as:

- **Direction** (AetherGovern → other, other → AetherGovern, bidirectional)
- **Data exchanged** (types and fields)
- **Coupling level** (low, medium, high)
- **Invariants** (which invariants from `03_invariants.md` depend on the interface)
- **Failure modes** (what goes wrong if the interface is violated)

> **Methodological note.** v0.1.0 specified the interfaces at the level of requirements (Section 6). v2.0.0 specifies them as **concrete protocols** with message formats, error handling, and invariant dependencies. The interfaces are testable: each has a corresponding integration test (see `05_test_design.md`).

---

## Overview

| Interface | Direction | Coupling | Invariants |
|:-:|---|:-:|:-:|
| **AetherGit** | Bidirectional | Low-medium | I2.1, I2.2, I10.2 |
| **AetherFlow** | AetherGovern → Flow | Medium | I2.1, I2.4, X1 |
| **AetherProof** | Bidirectional | Medium | I6.2, X4 |
| **AetherMesh** | Bidirectional | High | I5.1, I7.1, I7.2, X1, X2 |

---

## Interface 1 — AetherGit (Storage)

### Direction

Bidirectional. AetherGovern **reads** the changeset log; AetherGovern **writes** governance records as ordinary changesets.

### Data Exchanged

#### From AetherGit to AetherGovern

| Field | Type | Description |
|---|---|---|
| `changeset_id` | `str` | Content-addressed changeset identifier. |
| `parent_ids` | `List[str]` | Parent changeset identifiers. |
| `author` | `str` | `agent_id` of the changeset author. |
| `timestamp` | `str` | ISO-8601 timestamp. |
| `content_hash` | `str` | SHA-256 of the changeset content. |
| `governance_headers` | `dict` | Optional governance fields (authority_chain_ref, policy_ref, frontier_ref). |

#### From AetherGovern to AetherGit

| Field | Type | Description |
|---|---|---|
| `record_type` | `str` | `"delegation_certificate"`, `"revocation_record"`, `"policy_approval"`, `"accountability_record"`. |
| `record_body` | `dict` | Canonical record fields. |
| `record_hash` | `str` | SHA-256 of `record_body`. |
| `signature` | `bytes` | Issuer's signature over `record_hash`. |

### Message Formats

**Read request:**
```json
{
  "type": "read_changeset",
  "changeset_id": "...",
  "include_governance_headers": true
}
```

Read response:

```json
{
  "type": "changeset",
  "changeset_id": "...",
  "parent_ids": ["...", "..."],
  "author": "...",
  "timestamp": "...",
  "content_hash": "...",
  "governance_headers": {
    "authority_chain_ref": "...",
    "policy_ref": "...",
    "frontier_ref": "..."
  }
}
```

Write request:

```json
{
  "type": "write_governance_record",
  "record_type": "revocation_record",
  "record_body": { ... },
  "record_hash": "...",
  "signature": "..."
}
```

Coupling

Low-medium. AetherGovern requires only:

· An append-only changeset log with parent pointers.
· Fields for authority and policy references.
· Append-only governance records.

AetherGovern does not require changes to AetherGit's core data structures.

Invariants Dependent on This Interface

· I2.1 — Causal citation: The frontier_ref and policy_ref are stored in the changeset's governance headers.
· I2.2 — Content addressing: The changeset_id is the content hash.
· I10.2 — Hash-link integrity: The prev_record_hash of an accountability record matches the previous record's changeset_id.

Failure Modes

Failure Consequence
AetherGit does not store governance_headers I2.1 cannot be verified; determinism fails.
AetherGit reorders changesets prev_record_hash chain breaks; I10.2 violated.
AetherGit rejects governance records Revocations and certificates cannot be recorded.

Reference

· v0.1.0, Section 6.1 (Interface with AetherGit).

---

Interface 2 — AetherFlow (Integration)

Direction

AetherGovern → AetherFlow (admission hook); AetherFlow → AetherGovern (authorization verdict request).

Data Exchanged

From AetherGovern to AetherFlow

Field Type Description
action_id str Identifier of the action being admitted.
verdict str "allow", "deny", "quarantine".
reason str Human-readable explanation.
authority_chain_ref str Reference to the verified authority chain.

From AetherFlow to AetherGovern

Field Type Description
action Action The action to be authorized (see 01_entities.md, Entity 2).
requested_at str ISO-8601 timestamp of the request.

Message Formats

Authorization request (Flow → Govern):

```json
{
  "type": "authorization_request",
  "action": {
    "action_id": "...",
    "kind": "merge",
    "actor": "agent-001",
    "resource": "branch/main",
    "payload": { ... },
    "timestamp": "...",
    "frontier_ref": "...",
    "policy_ref": "...",
    "authority_chain": ["cert-001", "cert-002"],
    "signature": "..."
  },
  "requested_at": "..."
}
```

Authorization verdict (Govern → Flow):

```json
{
  "type": "authorization_verdict",
  "action_id": "...",
  "verdict": "allow",
  "reason": "authority chain valid at cited frontier",
  "authority_chain_ref": "..."
}
```

Coupling

Medium. AetherFlow requires:

· An admission hook before verification is scheduled.
· A rule for who may initiate or approve remediation actions.

AetherGovern requires:

· A message-based protocol (any format) for submitting actions and receiving verdicts.

Invariants Dependent on This Interface

· I2.1 — Causal citation: The action must cite a frontier and policy; AetherFlow must not strip these fields.
· I2.4 — Chain completeness: The authority chain must be non-empty.
· X1 — Determinism (A6): The verdict must be a pure function of the action and its causal closure; AetherFlow must not add local state.

Failure Modes

Failure Consequence
AetherFlow strips frontier_ref I2.1 cannot be verified.
AetherFlow adds local time to the request X1 (determinism) fails; honest nodes diverge.
AetherFlow ignores the verdict Unauthorized actions are admitted.

Reference

· v0.1.0, Section 6.2 (Interface with AetherFlow).

---

Interface 3 — AetherProof (Verification)

Direction

Bidirectional. AetherGovern designates which specification changes and evidence acceptances are governed actions; AetherProof provides proof obligations that can be consulted by semantic predicates.

Data Exchanged

From AetherGovern to AetherProof

Field Type Description
governed_action_kinds List[str] Which action kinds are subject to governance.
policy_documents List[Policy] Policies that can be treated as specifications.

From AetherProof to AetherGovern

Field Type Description
specification_changes List[Change] Changes to specifications, each with a governed flag.
evidence_acceptances List[Acceptance] Acceptances of proof evidence, each with a governed flag.

Message Formats

Governed-action designation (Govern → Proof):

```json
{
  "type": "governed_action_designation",
  "governed_action_kinds": ["specification_change", "evidence_acceptance"],
  "policy_documents": [ ... ]
}
```

Specification change query (Proof → Govern):

```json
{
  "type": "specification_change",
  "change_id": "...",
  "author": "agent-001",
  "governed": true
}
```

Coupling

Medium. AetherGovern requires:

· A designation of which specification changes and evidence acceptances are governed actions.

AetherProof requires:

· A statement of who may change a specification.
· Policy documents that can be checked for consistency.

Invariants Dependent on This Interface

· I6.2 — Approval completeness: A policy cannot be enforced without an approval chain; AetherProof must respect this.
· X4 — Authority–evidence separation: Authority records ≠ evidence records; AetherProof must not treat proof evidence as authority.

Failure Modes

Failure Consequence
AetherProof treats proof evidence as authority X4 violated; category error.
AetherProof allows unapproved specification changes I6.2 violated.
Circularity (policies verified by AetherProof) Trust anchoring becomes circular.

Reference

· v0.1.0, Section 6.3 (Interface with AetherProof).

---

Interface 4 — AetherMesh (Decentralization)

Direction

Bidirectional. AetherGovern uses AetherMesh's gossip to replicate governance records; AetherMesh accepts an additional authorization predicate in its admission pipeline.

Data Exchanged

From AetherGovern to AetherMesh

Field Type Description
governance_delta GovernanceDelta A certificate, revocation, or policy approval, encoded as a delta.
authorization_predicate Callable A predicate (action, causal_closure) → bool that satisfies A6.

From AetherMesh to AetherGovern

Field Type Description
replicated_delta GovernanceDelta A governance delta received via gossip.
admission_verdict bool Whether the delta was admitted.

Message Formats

Governance delta (Govern → Mesh):

```json
{
  "type": "governance_delta",
  "delta_kind": "revocation",
  "body": {
    "revocation_id": "...",
    "certificate_ref": "...",
    "issuer": "...",
    "reason": "...",
    "timestamp": "...",
    "signature": "..."
  }
}
```

Admission verdict (Mesh → Govern):

```json
{
  "type": "admission_verdict",
  "delta_id": "...",
  "admitted": true
}
```

Coupling

High. AetherGovern requires:

· That governance records replicate as deltas.
· That the admission pipeline accept an additional authorization predicate that satisfies A6.

AetherMesh requires:

· A specified registry mechanism with delegation, rotation, and revocation (which v0.1.0 left unspecified — its T6 and Q31).

Invariants Dependent on This Interface

· I5.1 — Monotonicity: Revocations are monotone; AetherMesh's join must preserve this.
· I7.1 — Grow-only: The frontier can only grow; AetherMesh's delta-state replication must preserve this.
· I7.2 — Join is union: Frontier join is set union; AetherMesh's join must match.
· X1 — Determinism (A6): The admission predicate must be a pure function of the action and its causal closure.
· X2 — Monotonic revocation: Adding revocations cannot validate; AetherMesh must preserve this.

Failure Modes

Failure Consequence
AetherMesh's join is not union I7.2 violated; frontiers diverge.
The admission predicate is non-deterministic X1 violated; honest nodes diverge.
AetherMesh strips governance metadata Certificates and revocations cannot be replicated.
Circularity (governance depends on A6, which depends on governance) The dependency must be grounded in a root.

Reference

· v0.1.0, Section 6.4 (Interface with AetherMesh).

---

Interface Summary

Dimension Requires from it Provides to it Coupling
AetherGit Fields for authority and policy references; append-only governance records Authorship authorization verdict Low-medium
AetherFlow Admission hook before verification; role for remediation Authorization verdicts; remediation authority Medium
AetherProof Designation of governed specification changes Authority for specification change; checkable policies Medium
AetherMesh Delta replication of governance records; determinism-compatible predicate Registry with delegation, rotation, revocation High

---

Minimal vs. Full Interface

Minimal Interface

The minimal interface consists of four artifacts and one rule:

1. A DelegationCertificate record (Entity 4).
2. A RevocationRecord (Entity 5).
3. An authority_frontier_ref carried in each action (Entity 2, field frontier_ref).
4. A policy_ref carried in each action (Entity 2, field policy_ref).
5. The rule that the authorization predicate satisfies Proposition 1 (causal-authority admission).

Layers covered: 1 (Authorization) and 4 (Revocation).

F1 implication: If the minimal interface is all that is needed, the whole contribution might be a bounded extension of AetherMesh.

Full Interface

The full interface adds:

· Policy lifecycle messages (propose, approve, enforce, revoke).
· Accountability queries (query_record, query_chain).
· Dispute and escalation messages.
· The governed-specification designation for AetherProof.
· The remediation-authority rule for AetherFlow.

Layers covered: all five (Authorization, Policy, Accountability, Revocation, Dispute Resolution).

F1 implication: Harder to fold into a single dimension.

Comparison

Aspect Minimal Full
Records Delegation certificate; revocation record Plus policy, approval, accountability, dispute, escalation records
Action header frontier_ref, policy_ref Plus additional governance fields
Predicate Chain validity at cited frontier Plus policy enforcement and conflict rule
Layers covered 1, 4 All five
F1 implication Likely a bounded extension of AetherMesh Harder to fold into a single dimension

The contrast sharpens the falsification question: the case for a standalone dimension rests on the layers beyond the minimal interface (policy, accountability, dispute resolution) being separable and valuable. That is a hypothesis for which v0.1.0 has no evidence; v2.0.0 is designed to test it.

---

Limitations of This Document

· The interfaces are specifications, not implementations. No code is claimed.
· The message formats are proposals; they may be revised as the implementation and tests reveal gaps.
· The coupling ratings are qualitative; they will be measured in simulation (see 05_test_design.md).
· The minimal-vs-full distinction is a design choice; it will be tested against F1 (redundancy) in experiments/.

---

End of Interfaces (v2.0.0-draft).
