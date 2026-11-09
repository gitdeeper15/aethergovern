# AetherOrchestrate — Architectural Hypothesis Under Investigation

**Status:** Architectural Hypothesis — Under Investigation
**Version:** 0.1.0-draft
**Date:** 2026-11-08
**Author:** Samir Baladi
**Related work:** AetherGit (10.5281/zenodo.23966896), AetherFlow (10.5281/zenodo.23979129), AetherProof (10.5281/zenodo.24013124), AetherMesh (10.5281/zenodo.24053492)
**Purpose:** Determine whether a fifth architectural capability — agentic orchestration — is genuinely missing from the Aether family, or whether it is already covered by AetherFlow (workflow coordination), AetherMesh (message distribution), or a combination of the two.

> **Methodological note.** This document is a *hypothesis under investigation*, not a project proposal. It is structured to be falsified. If the analysis shows that AetherFlow's M1–M10 protocol, together with AetherMesh's gossip layer, already covers the functional boundary proposed here, then AetherOrchestrate should not be pursued as an independent project. The conclusion of this document is therefore either "gap confirmed" or "gap already covered" — not "project approved".

---

## 1. Functional Boundary

### 1.1 What AetherOrchestrate would do

AetherOrchestrate would be the **decision layer** that assigns tasks to autonomous agents in a multi-agent software ecosystem. Concretely, it would answer:

- **Assignment:** Which agent works on which task, at which time, under which constraints?
- **Delegation:** Which agent is authorized to act on behalf of which other agent, and for which scope?
- **Sequencing:** In what order should dependent tasks be executed, given partial-order constraints from the proof layer and the integration layer?
- **Conflict prevention:** How are two agents prevented from simultaneously claiming the same task or the same code region?
- **Recovery:** When an agent fails mid-task, how is the task reassigned without duplicating work or losing state?

### 1.2 What AetherOrchestrate would *not* do

To avoid conflating orchestration with adjacent functions, the following are explicitly **out of scope**:

- **Not workflow execution.** Executing a workflow (running tests, applying patches, triggering CI) is AetherFlow's function. AetherOrchestrate *decides* which workflow to run and by whom; it does not *run* it.
- **Not message distribution.** Disseminating state across peers is AetherMesh's function. AetherOrchestrate *uses* AetherMesh to disseminate its decisions; it does not implement gossip.
- **Not proof construction.** Building or checking proofs is AetherProof's function. AetherOrchestrate *consumes* proof obligations to determine which tasks are unblocked.
- **Not change storage.** Storing changesets is AetherGit's function. AetherOrchestrate *reads* the changeset log to determine the current state of the codebase.

### 1.3 The boundary question

The boundary between "deciding what to do" (orchestration) and "doing it" (workflow execution) is the central question of this document. If AetherFlow's M1–M10 protocol already includes a decision-making component (e.g., a task-assignment message, a delegation message, or a sequencing message), then the functional boundary proposed here may already be covered.

**Test:** Does any of M1–M10 carry a task-assignment, delegation, or sequencing payload? If yes, what is left for AetherOrchestrate? If no, is the absence intentional (because workflow coordination does not require assignment) or accidental (because AetherFlow assumed a single orchestrator)?

---

## 2. Existing Coverage

This section examines what each of the four existing projects provides, with specific attention to whether any of them already covers the functional boundary of §1.

### 2.1 AetherGit (Storage)

AetherGit provides an append-only changeset log with parent pointers. It does not assign tasks, delegate authority, or sequence execution. **It does not cover orchestration.**

### 2.2 AetherFlow (Integration)

AetherFlow provides a message-based protocol (M1–M10) over which agents submit changes and receive notifications. The protocol is described in AetherFlow v1.0.0 as covering post-merge verification and dynamic conflict resolution. The question is whether M1–M10 include:

| Message | AetherFlow description | Orchestration-relevant? |
|---|---|:-:|
| M1 | (to be verified from AetherFlow v1.0.0) | ? |
| M2 | (to be verified) | ? |
| M3 | (to be verified) | ? |
| M4 | (to be verified) | ? |
| M5 | (to be verified) | ? |
| M6 | (to be verified) | ? |
| M7 | (to be verified) | ? |
| M8 | (to be verified) | ? |
| M9 | (to be verified) | ? |
| M10 | (to be verified) | ? |

**Status:** The M1–M10 payloads must be extracted from AetherFlow v1.0.0 before this section can be completed. The extraction is the first research task of this study.

**Preliminary hypothesis (to be tested):** AetherFlow's protocol likely covers *submission* (agent → integration layer) and *notification* (integration layer → agent), but *not assignment* (which agent should submit which change). If this hypothesis holds, orchestration is not covered by AetherFlow.

### 2.3 AetherProof (Verification)

AetherProof provides formal definitions and proof obligations (CSR, PDG). It can tell you *what must be true* for a change to be correct, but not *who* should make the change. **It does not cover orchestration.**

### 2.4 AetherMesh (Decentralization)

AetherMesh provides CRDT-based state synchronization, epidemic gossip, and Byzantine admission. It can disseminate decisions, but it does not make them. **It does not cover orchestration.**

**Boundary note:** AetherMesh's Byzantine admission layer decides whether to *admit a received delta*. It does not decide whether to *assign a task to an agent*. These are different decisions: admission is about accepting incoming state; assignment is about allocating outgoing work. The two are orthogonal.

### 2.5 Cross-project coverage

The four projects, taken together, provide:
- A way to store changes (AetherGit).
- A way to submit and verify changes (AetherFlow).
- A way to prove that changes satisfy specifications (AetherProof).
- A way to synchronize state across peers (AetherMesh).

They do **not** provide:
- A way to decide which agent should work on which task.
- A way to delegate authority from one agent to another.
- A way to sequence dependent tasks across agents.
- A way to prevent two agents from claiming the same task.
- A way to recover from agent failure mid-task.

**If these are genuinely absent, the gap is confirmed. If any of them is present (e.g., inside M1–M10), the gap is narrower than it appears.**

---

## 3. Architectural Gap

### 3.1 The gap, stated precisely

The gap is the absence of a **task-allocation decision layer** that operates above the four existing projects. The gap is *not* the absence of message-passing (AetherMesh provides it), *not* the absence of workflow execution (AetherFlow provides it), and *not* the absence of proof checking (AetherProof provides it). It is the absence of a component that **decides** which agent does what.

### 3.2 Why the gap might be real

In a multi-agent ecosystem with autonomous agents, the following decisions must be made:
- **Which agent** should pick up an unassigned task?
- **Under which constraints** (deadline, cost, capability)?
- **With which authority** (can this agent modify this repository region)?
- **In which order** (which tasks must complete before others start)?
- **How to recover** if the assigned agent fails?

Without a decision layer, these decisions fall to ad-hoc protocols (e.g., first-come-first-served, or a human operator). A dedicated layer would make them explicit and testable.

### 3.3 Why the gap might be illusory

Three reasons the gap might not be real:

1. **AetherFlow's M1–M10 may already include assignment.** If M1 (or another message) carries a task-assignment payload, then AetherFlow already covers the boundary. *This must be verified.*

2. **AetherMesh's gossip may be sufficient for coordination.** In some multi-agent systems, coordination emerges from gossip: agents announce their intentions, and conflicts are resolved by CRDT merge. If this suffices for the workloads of interest, a dedicated orchestrator is unnecessary. *This must be tested.*

3. **The "single orchestrator" assumption.** AetherFlow was designed as an integration layer, not an orchestrator. But if its protocol is expressive enough, it can be used for orchestration without modification. The question is whether the protocol's expressiveness is accidental or intentional. *This must be verified.*

### 3.4 The gap test

The gap is real **if and only if** all three of the following hold:

- **G1:** AetherFlow's M1–M10 do **not** include task-assignment, delegation, or sequencing payloads.
- **G2:** AetherMesh's gossip is **not** sufficient for task allocation (e.g., because allocation requires global ordering that gossip cannot provide).
- **G3:** The absence of a decision layer causes **measurable harm** in realistic multi-agent workloads (e.g., duplicated work, lost tasks, deadlocks).

If any of G1–G3 fails, the gap is either covered, or not harmful enough to justify a new project.

**This document does not yet conclude that G1–G3 hold. It proposes the experiments that would test them.**

---

## 4. Interfaces

If AetherOrchestrate is pursued, it would require the following interfaces:

### 4.1 From AetherGit

| Need | Interface |
|---|---|
| Read changeset log | Append-only changeset log with parent pointers (already specified) |
| Determine current state | Query the log for the latest changeset on each branch |
| Detect conflicts | Compare changesets that touch the same region |

**Boundary:** AetherOrchestrate does not write to the log; it reads it.

### 4.2 From AetherFlow

| Need | Interface |
|---|---|
| Submit an assignment | A message type (M?) carrying (agent_id, task_id, constraints) |
| Receive completion notification | A message type (M?) carrying (task_id, result) |
| Query workflow status | A message type (M?) carrying (task_id) → status |

**Open question:** Do M1–M10 already include these message types? If yes, AetherOrchestrate does not need a new interface with AetherFlow; it can reuse the existing one. If no, a new message type must be specified — but that would be an extension of AetherFlow, not a new project.

### 4.3 From AetherProof

| Need | Interface |
|---|---|
| Determine which tasks are unblocked | Query the PDG for obligations with no unmet dependencies |
| Validate a completed task | Submit a proof obligation for the task's output |

**Boundary:** AetherOrchestrate consumes proof obligations; it does not construct them.

### 4.4 From AetherMesh

| Need | Interface |
|---|---|
| Disseminate an assignment | Use gossip to propagate the assignment to all peers |
| Detect conflicting assignments | Use CRDT merge to detect two agents claiming the same task |
| Recover from agent failure | Use gossip to detect failure and reassign |

**Boundary:** AetherOrchestrate uses AetherMesh's gossip; it does not implement its own.

### 4.5 Interface summary

| Interface | With | Required? |
|---|---|:-:|
| Read changeset log | AetherGit | Yes |
| Submit assignment | AetherFlow | Yes (or reuse M?) |
| Receive completion | AetherFlow | Yes (or reuse M?) |
| Query proof status | AetherProof | Optional |
| Disseminate assignment | AetherMesh | Yes |
| Detect conflicts | AetherMesh | Yes |

**If every required interface is already provided by the existing projects, then AetherOrchestrate is a *composition* of existing interfaces, not a new project. This is a critical distinction.**

---

## 5. Research Challenges

The following are the research challenges that AetherOrchestrate would address, if pursued.

### 5.1 Assignment under partial information

An orchestrator must decide which agent gets which task without knowing (a) every agent's full capability, (b) every agent's current load, (c) every agent's trustworthiness. **Challenge:** design an assignment algorithm that is robust to partial information and that degrades gracefully as information becomes stale.

### 5.2 Delegation without central trust

In a decentralized setting, there is no central authority to grant delegation. **Challenge:** design a delegation protocol where authority flows from agent to agent via signed chains, and where revocation propagates correctly.

### 5.3 Sequencing under partial order

Tasks have partial-order dependencies (task B cannot start until task A completes). **Challenge:** sequence tasks so that no agent waits unnecessarily and no dependency is violated.

### 5.4 Conflict prevention

Two agents may claim the same task or the same code region. **Challenge:** prevent conflicts without a global lock, and detect them when prevention fails.

### 5.5 Recovery from agent failure

An agent may fail mid-task. **Challenge:** reassign the task to another agent without duplicating work or losing state.

### 5.6 Composition with AetherMesh's admission layer

AetherMesh's Byzantine admission layer decides whether to accept a delta. AetherOrchestrate's decisions must be admitted by AetherMesh, but AetherOrchestrate's decisions are about *future* work, not *past* deltas. **Challenge:** reconcile the temporal asymmetry between admission (past) and assignment (future).

### 5.7 The single-orchestrator assumption

AetherFlow was designed as an integration layer, not as an orchestrator. If it is used for orchestration, it becomes a *single orchestrator* — which contradicts AetherMesh's decentralization goal. **Challenge:** either (a) show that a single orchestrator is acceptable for the workloads of interest, or (b) design a decentralized orchestration protocol that composes with AetherMesh.

**Note:** Challenge 5.7 is the most consequential. If a single orchestrator is unacceptable (because it contradicts AetherMesh's design), then AetherOrchestrate must be decentralized. But a decentralized orchestrator is a hard research problem in its own right. This challenge alone may justify a separate project.

---

## 6. Evaluation Metrics

The following metrics would be used to evaluate AetherOrchestrate, if pursued.

### 6.1 Throughput and latency (necessary, not sufficient)

| Metric | Definition | Why it is necessary | Why it is not sufficient |
|---|---|---|---|
| Task throughput | Tasks assigned per unit time | Measures raw capacity | Does not measure correctness |
| Assignment latency | Time from task arrival to assignment | Measures responsiveness | Does not measure conflict or recovery |

**Note:** Throughput and latency alone cannot justify a new project. A centralized scheduler can achieve high throughput and low latency; the value of a decentralized orchestrator is in its *correctness under failure*, not in its raw speed.

### 6.2 Correctness metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Assignment correctness | Fraction of tasks assigned to an agent capable of completing them | Measures whether the orchestrator's decisions are sound |
| Conflict rate | Fraction of tasks with two or more concurrent claimants | Measures whether the orchestrator prevents conflicts |
| Deadlock rate | Fraction of task sets that cannot complete due to cyclic dependencies | Measures whether the orchestrator's sequencing is correct |
| Duplicate work rate | Fraction of work performed twice because of failed recovery | Measures whether recovery is correct |

### 6.3 Recovery metrics

| Metric | Definition | Why it matters |
|---|---|---|
| Mean time to recovery | Average time from agent failure to task reassignment | Measures responsiveness to failure |
| Work preserved on failure | Fraction of an agent's work that survives its failure | Measures whether recovery loses state |
| Recovery conflict rate | Fraction of recoveries that conflict with other agents' work | Measures whether recovery introduces new conflicts |

### 6.4 Coordination cost

| Metric | Definition | Why it matters |
|---|---|---|
| Messages per assignment | Number of messages exchanged to assign one task | Measures the cost of coordination |
| State per agent | Bytes of orchestration state each agent must maintain | Measures the memory cost |
| Coordination overhead | Fraction of agent time spent on coordination vs. work | Measures the opportunity cost |

### 6.5 Comparison metrics

| Metric | Baseline | Comparison |
|---|---|---|
| Throughput | Single orchestrator | Is decentralized orchestration competitive? |
| Conflict rate | No orchestrator (ad-hoc) | Does orchestration reduce conflicts? |
| Recovery time | Manual recovery | Does orchestration speed recovery? |

**The evaluation must show that AetherOrchestrate is *better than the alternatives*, not merely *different*.**

---

## 7. Failure Conditions

This section specifies the conditions under which AetherOrchestrate should **not** be pursued. These are the conditions under which the architectural gap is not real, or not harmful enough to justify a new project.

### 7.1 F1 — AetherFlow's M1–M10 already cover assignment

**Condition:** If any of M1–M10 carries a task-assignment, delegation, or sequencing payload, then AetherFlow already covers the functional boundary of §1.

**Consequence:** AetherOrchestrate should not be pursued. Instead, AetherFlow should be extended (if necessary) to make the assignment semantics explicit.

**Test:** Extract the M1–M10 payloads from AetherFlow v1.0.0. Document each payload's fields. If any payload includes a task identifier, an agent identifier, or a delegation chain, F1 holds.

### 7.2 F2 — AetherMesh's gossip is sufficient for coordination

**Condition:** If gossip-based coordination (agents announce intentions, conflicts are resolved by CRDT merge) achieves the same correctness metrics as a dedicated orchestrator, then a dedicated orchestrator is unnecessary.

**Consequence:** AetherOrchestrate should not be pursued. Instead, the gossip-based coordination protocol should be specified as part of AetherMesh.

**Test:** Implement a gossip-based coordination protocol. Compare its correctness metrics (§6.2) to a centralized orchestrator's. If the difference is not statistically significant, F2 holds.

### 7.3 F3 — The gap is not harmful

**Condition:** If the absence of a decision layer causes no measurable harm in realistic multi-agent workloads (i.e., ad-hoc coordination is good enough), then the gap is not harmful enough to justify a new project.

**Consequence:** AetherOrchestrate should not be pursued. Instead, the existing ad-hoc protocols should be documented as acceptable.

**Test:** Run a realistic multi-agent workload (e.g., 100 agents modifying a shared codebase). Measure conflict rate, duplicate work rate, and recovery time under ad-hoc coordination. If these metrics are acceptable (e.g., conflict rate < 5%), F3 holds.

### 7.4 F4 — A single orchestrator is acceptable

**Condition:** If a single orchestrator (not decentralized) is acceptable for the workloads of interest, then the hardest research challenge (§5.7) disappears. A single orchestrator could be built as an extension of AetherFlow, not as a new project.

**Consequence:** AetherOrchestrate should not be pursued as a decentralized project. A single-orchestrator extension of AetherFlow should be pursued instead.

**Test:** Determine whether the workloads of interest tolerate a single orchestrator (e.g., because the orchestrator is replicated for fault tolerance, but not decentralized for scalability). If yes, F4 holds.

### 7.5 F5 — The interfaces are already sufficient

**Condition:** If every required interface (§4.5) is already provided by the existing projects, then AetherOrchestrate is a *composition* of existing interfaces, not a new project.

**Consequence:** AetherOrchestrate should not be pursued. Instead, the composition should be specified as a protocol extension of AetherFlow.

**Test:** For each interface in §4.5, check whether the existing project provides it. If all are provided, F5 holds.

### 7.6 Summary of failure conditions

| ID | Condition | Consequence if true |
|:-:|---|---|
| **F1** | M1–M10 already cover assignment | Extend AetherFlow, not new project |
| **F2** | Gossip is sufficient for coordination | Specify gossip protocol, not new project |
| **F3** | The gap is not harmful | Document ad-hoc protocols, not new project |
| **F4** | Single orchestrator is acceptable | Extend AetherFlow, not new project |
| **F5** | Interfaces are already sufficient | Specify composition, not new project |

**If any of F1–F5 holds, AetherOrchestrate should not be pursued as an independent project.** The gap may still be real, but it is better addressed by extending an existing project than by creating a new one.

---

## 8. Relation to the Aether Family

AetherOrchestrate's relation to the existing four projects is **not** that of a fifth layer stacked on top. The four projects are *functional dimensions*, not *hierarchical layers*:

| Project | Functional dimension |
|---|---|
| AetherGit | Storage and versioning |
| AetherFlow | Integration and operational verification |
| AetherProof | Specification and formal evidence |
| AetherMesh | Distribution and eventual consistency |

AetherOrchestrate, if pursued, would be a **fifth functional dimension** — decision-making about task allocation — not a fifth hierarchical layer. This distinction matters because:

- **If it is a layer**, it must be stacked above AetherMesh, and it must respect AetherMesh's interfaces.
- **If it is a dimension**, it can interface with each of the four projects independently, and it can be composed with any subset of them.

The latter interpretation is more faithful to the four projects' actual designs. AetherOrchestrate should be evaluated as a *dimension*, not as a *layer*.

---

## 9. Open Questions

The following questions are open and should be answered before deciding whether to pursue AetherOrchestrate.

| ID | Question |
|---|---|
| Q1 | Do AetherFlow's M1–M10 include a task-assignment payload? |
| Q2 | If not, is the absence intentional or accidental? |
| Q3 | Is gossip-based coordination sufficient for realistic multi-agent workloads? |
| Q4 | What is the conflict rate under ad-hoc coordination? |
| Q5 | Is a single orchestrator acceptable for the workloads of interest? |
| Q6 | Can a decentralized orchestrator be built that composes with AetherMesh without becoming a new coordination bottleneck? |
| Q7 | What is the minimal interface between AetherOrchestrate and each of the four projects? |
| Q8 | Does AetherOrchestrate's temporal asymmetry (assignment = future, admission = past) require a new consistency model? |
| Q9 | What is the coordination cost of AetherOrchestrate relative to a single orchestrator? |
| Q10 | Is AetherOrchestrate a *dimension* (interfaces with each project independently) or a *layer* (stacked above AetherMesh)? |

---

## 10. Status of This Document

**Status:** Architectural Hypothesis — Under Investigation

**What this document is:** A structured investigation of whether a fifth architectural capability — agentic orchestration — is genuinely missing from the Aether family.

**What this document is not:** A project proposal. It does not conclude that AetherOrchestrate should be pursued. It concludes that the question is open and that specific tests (F1–F5) must be run before a decision can be made.

**Next steps:**
1. Extract AetherFlow's M1–M10 payloads (test F1).
2. Implement a gossip-based coordination protocol (test F2).
3. Run a realistic multi-agent workload (test F3).
4. Determine whether a single orchestrator is acceptable (test F4).
5. Document the interfaces (test F5).

**Decision rule:** If any of F1–F5 holds, AetherOrchestrate should not be pursued as an independent project. If all of F1–F5 fail, the gap is real and a project is justified.

---

**End of AetherOrchestrate Study (v0.1.0-draft).**
