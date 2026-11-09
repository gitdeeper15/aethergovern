<div align="center">

# 🏛️ AetherRuntime

### A Falsification-First Investigation of Runtime Assurance in the Aether Family

*Monitoring, Detection, Containment, and Recovery in Multi-Agent Software Ecosystems*

<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24078477.svg)](https://doi.org/10.5281/zenodo.24078477)
[![License: MIT + CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--4.0-crimson.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![Release](https://img.shields.io/badge/Release-v0.1.0-green)](https://github.com/gitdeeper15/aetherruntime/releases/tag/v0.1.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)

[![PyPI](https://img.shields.io/badge/PyPI-0.1.0%20(pending)-gold?logo=pypi&logoColor=white)](https://pypi.org/project/aetherruntime/)
[![Tests](https://img.shields.io/badge/Tests-0%20(no%20impl)-lightgrey)](tests/)
[![Experiments](https://img.shields.io/badge/Experiments-0%20(no%20impl)-lightgrey)](experiments/)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24078477.svg)](https://doi.org/10.5281/zenodo.24078477)
[![Record ID](https://img.shields.io/badge/Record%20ID-AETHERRUNTIME--01-informational)](https://doi.org/10.5281/zenodo.24078477)
[![OSF](https://img.shields.io/badge/OSF-pending-lightgrey)](https://osf.io/)
[![Website](https://img.shields.io/badge/Website-aether--runtime.netlify.app-00C7B7?logo=netlify&logoColor=white)](https://aether-runtime.netlify.app)
[![Aether Family](https://img.shields.io/badge/Aether%20Family-6%20dimensions-purple)](https://aether--runtime.netlify.app)

<br>

**[📄 Paper](https://doi.org/10.5281/zenodo.24078477)** ·
**[🌐 Website](https://aether-runtime.netlify.app)** ·
**[📦 Releases](https://github.com/gitdeeper15/aetherruntime/releases)** ·
**[🐝 PyPI](https://pypi.org/project/aetherruntime/)** ·
**[📖 Citation](#-citation)**

</div>

---

> [!WARNING]
> **Status: v0.1.0 — Architectural Hypothesis Under Investigation.**
> This is a **specification-level investigation**, not a committed project.
> **No implementation is claimed.** No real-world deployment is evaluated.
> Propositions P1–P2 are **proof sketches**, not machine-checked; they hold only under assumptions A1–A6 (inherited from [AetherMesh](https://doi.org/10.5281/zenodo.24038038)).
> The AetherRuntime hypothesis (F1–F5) is **not falsified by argument** and **not confirmed**.
> The final project structure (single, dual, triple, or quadruple) is undetermined.
> See [Threats and Limitations](#️-threats-and-limitations) and the [Research Status Statement](#-research-status-statement).

> *"AetherRuntime is a candidate, not a result."*

> *"The evaluation design here is an invitation to such evaluation, not a substitute for it."*

---

## 📑 Table of Contents

- [Overview](#-overview)
- [v0.1.0 at a Glance](#-v010-at-a-glance)
- [Installation](#️-installation)
- [The Central Question](#-the-central-question)
- [The Six Functional Dimensions](#️-the-six-functional-dimensions)
- [The Falsification-First Methodology](#-the-falsification-first-methodology)
- [Failure Conditions F1–F5](#-failure-conditions-f1f5)
- [The Three Candidate Capabilities](#-the-three-candidate-capabilities)
- [AetherRuntime: Architecture](#️-aetherruntime-architecture)
- [Propositions](#-propositions)
- [Interfaces with the Aether Family](#-interfaces-with-the-aether-family)
- [Evaluation Design](#-evaluation-design)
- [Threats and Limitations](#️-threats-and-limitations)
- [Research Status Statement](#-research-status-statement)
- [Platforms & Mirrors](#-platforms--mirrors)
- [Project Structure](#️-project-structure)
- [Version History](#-version-history)
- [Citation](#-citation)
- [Author](#-author)
- [License](#️-license)

---

## 🔭 Overview

**AetherRuntime** is the **sixth functional dimension** (provisional) of the Aether family — a candidate architecture for **monitoring, detection, containment, halt, and recovery** of running agents in multi-agent software ecosystems.

The Aether family currently comprises **five foundational dimensions**, each published as a preprint on Zenodo (**not peer-reviewed**):

| Dimension | Focus | Question |
|---|---|---|
| **AetherGit** | Storage and versioning | How are changes stored and versioned? |
| **AetherFlow** | Integration and operational verification | How are changes integrated and verified? |
| **AetherProof** | Specification and formal evidence | How is correctness proven? |
| **AetherMesh** | Distribution and eventual consistency | How is state synchronized without a central coordinator? |
| **AetherGovern** | Authority and policy | Who is authorized to do what, under which policy? |

AetherRuntime asks whether a **sixth dimension** is needed:

> **Are agents behaving acceptably while running, and how are they halted or isolated when they are not?**

The investigation follows a **falsification-first methodology**: before describing the candidate, it states **five failure conditions (F1–F5)** whose satisfaction would show that the candidate does not deserve to exist as a separate dimension.

| Release | What it adds |
|---|---|
| **v0.1.0** | The hypothesis and the falsification-first methodology (paper) |
| *(planned)* | Reference implementation, tests, experiments, PyPI package |

---

## 📊 v0.1.0 at a Glance

| Dimension | Status |
|---|---|
| Manuscript (v0.1.0) | Complete (33 pages, PDF) |
| Formal definitions / Propositions / Layers | 4 / 2 (proof sketches) / 5 |
| Implementation | ❌ Not built (specification only) |
| Tests | ❌ None |
| Experiments | ❌ None |
| PyPI package | ⏳ Not yet published |
| Real-world deployment | ❌ Not evaluated |
| Causal claims | None (argument only) |

<p align="center">
  <img src="docs/figures/Fig1_Six_Dimensions.png"
       alt="AetherRuntime — The Six Functional Dimensions of the Aether Family"
       width="100%">
</p>

<p align="center">
  <em>Figure 1 — The Six Functional Dimensions of the Aether Family (AetherGit, AetherFlow, AetherProof, AetherMesh, AetherGovern, and the proposed hypothesis AetherRuntime). The sixth dimension is a hypothesis under investigation, not a confirmed dimension.</em>
</p>

### Contributions to the Investigation

| # | Contribution | Kind |
|:-:|---|---|
| 1 | A falsification-first procedure with five failure conditions and a decision rule, stated before the candidate is described | Methodology |
| 2 | A comparison of three candidate capabilities that could fill a gap beside the five dimensions: orchestration, governance, and runtime assurance | Analysis |
| 3 | A hypothesized five-layer runtime architecture, including monitoring, detection, containment, halt, and recovery | Specification (hypothesis) |
| 4 | Two propositions with proof sketches that bear directly on F4: local anomaly detection preserves the determinism requirement of AetherMesh, and any decentralized halt protocol leaves an irreducible halt window | Analysis (proof sketches) |
| 5 | A proposed evaluation design with metrics M1–M9, baselines B1–B5, and scenarios S1–S6 | Evaluation design |
| 6 | Twenty open questions (Q1–Q20) | Catalogue |

---

## ⚙️ Installation

> [!NOTE]
> **No implementation is available yet.** The PyPI package is planned but not published. The commands below are for reference and will not work until v1.0.0 is released.

```bash
# Planned (not yet available):
# pip install aetherruntime

# For now, clone the repository to read the paper and source:
git clone https://github.com/gitdeeper15/aetherruntime.git
cd aetherruntime
```

Requires Python 3.9+ (when implementation is released). Runtime dependency (planned): cryptography >= 41.0.

---

❓ The Central Question

Is there a body of monitoring, detection, containment, halt, and recovery requirements for multi-agent software ecosystems that (i) is not already specified by the five existing dimensions, (ii) is not reducible to verification or to governance, (iii) can be specified without reintroducing a central authority, and (iv) yields an observable benefit over existing mechanisms?

The four clauses correspond to failure conditions F1, F2 and F3 (clause ii), F4, and F5. A negative answer to any clause would show that runtime assurance, as a separate dimension, is not warranted.

---

🗺️ The Six Functional Dimensions

The word "dimension" is chosen deliberately. Earlier descriptions used "layer", which suggests a vertical stack. The relationships among the six works are not strictly hierarchical.

# Dimension Focus Question DOI
1 AetherGit Storage and versioning How are changes stored and versioned? 10.5281/zenodo.23966896
2 AetherFlow Integration and operational verification How are changes integrated and verified? 10.5281/zenodo.23979129
3 AetherProof Specification and formal evidence How is correctness proven? 10.5281/zenodo.24013124
4 AetherMesh Distribution and eventual consistency How is state synchronized without a central coordinator? 10.5281/zenodo.24038038
5 AetherGovern Authority and policy Who is authorized to do what, under which policy? 10.5281/zenodo.24054524
6 AetherRuntime (hypothesis) Monitoring and runtime assurance Are agents behaving acceptably while running? 10.5281/zenodo.24078477

<p align="center">
  <img src="docs/figures/Fig5_Runtime_vs_Verification.png"
       alt="AetherRuntime — Runtime Assurance vs. Verification"
       width="100%">
</p>

<p align="center">
  <em>Figure 5 — Runtime assurance versus verification in the Aether family. Orthogonality is a hypothesis tested as failure condition F2.</em>
</p>

---

🔬 The Falsification-First Methodology

A typical architecture paper begins from a conviction that a component is needed and then specifies it. The risk is circular. AetherRuntime adopts a falsification-first methodology:

1. No prior assumption that the gap exists.
2. No prior assumption that AetherRuntime should be a separate project.
3. Every claim is tested against failure conditions (F1–F5).
4. The final structure (single project, dual project, triple project, quadruple project, or integration protocol) is determined after comparison.

---

🧭 Failure Conditions F1–F5

ID Claim under test Falsified if… Status
F1 Non-redundancy Every requirement R1–R6 is met by existing mechanisms or by a bounded extension of a single existing dimension 🟡 Not falsified (R3, R4, R5)
F2 Orthogonality to verification Every runtime-assurance decision and trust anchor can be encoded as a verified proposition 🟡 Not falsified (narrowly)
F3 Boundary with governance Runtime assurance reduces to governance plus conventional monitoring 🟡 Not falsified (decentralized setting)
F4 Decentralizability Any design preserving the required properties needs a central authority or strong consistency 🟡 Not falsified (with residuals)
F5 Observable benefit No scenario class can be constructed in which the best existing baseline fails and runtime assurance succeeds 🔴 Untested

Requirement list R1–R6:

ID Requirement
R1 Continuous monitoring: resource use and action stream observable while an agent runs
R2 Anomaly detection: deviations flagged with bounded FP/FN rates
R3 Containment: anomalous agent isolatable with bounded restrictions
R4 Halt: agent stoppable via decentralized quorum
R5 Recovery: halted agent returnable to known-good state
R6 Partition tolerance: monitoring, detection, containment, halt possible at a disconnected node

---

🎯 The Three Candidate Capabilities

Candidate Focus Central question Redundancy risk
AetherOrchestrate Task scheduling and workflow What should agents do next? Medium
AetherGovern Authority, accountability, revocation Who may act, under which policy? Medium
AetherRuntime Live monitoring and rollback Are agents behaving acceptably while running? High

AetherRuntime is a candidate for addressing the runtime-assurance gap, provided it passes the falsification criteria (F1–F5). No claim is made that the other two candidates are weaker.

---

🏛️ AetherRuntime: Architecture

[!NOTE]
All of this is hypothesis: a specification-level description of what a runtime-assurance dimension might contain.

The Five Runtime Layers

<p align="center">
  <img src="docs/figures/Fig2_Runtime_Layers.png"
       alt="AetherRuntime — The Five Layers"
       width="100%">
</p>

<p align="center">
  <em>Figure 2 — The five layers of AetherRuntime (hypothesis). Ordering reflects conceptual dependency, not an enforcement hierarchy.</em>
</p>

Layer Question Status
1 — Monitoring What is the agent doing? Hypothesis
2 — Detection Is this behaviour anomalous? Hypothesis
3 — Containment How do we isolate the agent? Hypothesis
4 — Halt How do we stop the agent? Hypothesis
5 — Recovery How do we restore the system? Hypothesis

The Runtime Lifecycle

<p align="center">
  <img src="docs/figures/Fig3_Runtime_Lifecycle.png"
       alt="AetherRuntime — The Runtime Lifecycle"
       width="100%">
</p>

<p align="center">
  <em>Figure 3 — The runtime lifecycle in AetherRuntime (hypothesis): observe, detect, classify, contain, halt, recover. Schematic; not a protocol specification.</em>
</p>

Anomaly Detection

<p align="center">
  <img src="docs/figures/Fig4_Anomaly_Detection.png"
       alt="AetherRuntime — Anomaly Detection"
       width="100%">
</p>

<p align="center">
  <em>Figure 4 — The central challenge: distinguish true anomalies (red) from benign deviations (orange) without excessive false positives.</em>
</p>

Runtime State Machine

<p align="center">
  <img src="docs/figures/Fig6_Runtime_State_Machine.png"
       alt="AetherRuntime — Runtime State Machine"
       width="100%">
</p>

<p align="center">
  <em>Figure 6 — The runtime state machine. Each state has defined entry and exit conditions; exception transitions (dashed) represent recovery paths.</em>
</p>

---

📜 Propositions

[!NOTE]
Status: Stated with proof sketches; not machine-checked; conditional on assumptions A1–A6 (see AetherMesh).

# Proposition Statement Bears on
P1 Determinism of Local Anomaly Detection If each node evaluates anomaly predicates against a local baseline and the anomaly predicates are deterministic functions of the local state, then the anomaly-detection layer preserves AetherMesh's determinism requirement (assumption A6). F4
P2 Irreducible Halt Window Any decentralized halt protocol leaves a window Δt_window = t_halt_enforced − t_detect during which a compromised agent may continue to act. F4

Mathematical form (P1):

```
S_i(t+1) = S_i(t) ⊔ ⊔_{m ∈ M_i} m

∀ i, j, A_i(S_i) ∧ A_j(S_j) ⇒ (S_i ⊔ S_j) = (S_j ⊔ S_i)
```

Mathematical form (P2):

```
Δt_window = t_halt_enforced − t_detect
          = D_gossip(N, f) + t_queue + t_verify
```

Resource monitoring metric:

```
Ω_i(t) = ∫_0^t ( CPU_i(τ) + Memory_i(τ) + NetworkIO_i(τ) ) dτ > Θ_max
```

---

🔗 Interfaces with the Aether Family

Dimension Requires from it Provides to it Coupling
AetherGit Storage for telemetry, snapshots, recovery records State snapshot mechanism Low–medium
AetherFlow Event stream from operational verification Halt signal Medium–high
AetherProof Designation of runtime-checkable specifications Runtime evidence (telemetry traces) Medium
AetherMesh Delta replication; determinism-compatible predicate Monitoring and halt predicates High
AetherGovern Authority to halt an agent Runtime evidence for accountability High

Minimal interface (four artifacts, one rule): telemetry schema, baseline model, halt-order record, and the requirement that the halt predicate satisfy Proposition 1.

[!IMPORTANT]
If the minimal interface is all that is needed, the whole contribution might be an extension of AetherFlow's operational verification. The case for a standalone dimension rests on the layers beyond the minimal interface being separable and valuable. That is a hypothesis for which this paper has no evidence.

---

📊 Evaluation Design

[!IMPORTANT]
In the v0.1.0 paper no evaluation was performed. That section specifies how the candidate would be evaluated, in a form that fixes in advance what outcomes would count as failure. Every metric, baseline, and threshold is a proposal.

ID Metric Definition Direction
M1 Anomaly detection rate Fraction of true anomalies detected Higher is better
M2 False-positive rate Fraction of benign actions flagged as anomalous Lower is better
M3 Detection latency Time from anomaly onset to alert Lower is better
M4 Containment time Time from alert to containment Lower is better
M5 Halt window Time from detection to halt enforcement Lower is better
M6 Recovery correctness Fraction of recovered states that match ground truth Higher is better
M7 Monitoring overhead Added CPU/memory/network per agent Lower is better
M8 Halt quorum latency Time to reach quorum for a halt order Lower is better
M9 Convergence preservation Count of runs in which honest nodes diverge Must be zero if P1 holds

Baselines B1–B5:

ID Baseline What it tests
B1 No runtime assurance Value of any runtime mechanism
B2 Static thresholds Whether simple thresholds suffice (F1)
B3 Centralized monitor Cost/benefit of decentralization (F4)
B4 AetherFlow-only Whether runtime monitoring adds value (F1)
B5 Minimal runtime Whether the full five layers add value

Scenarios S1–S6: resource exhaustion, action-set drift, network anomaly, privilege escalation, Byzantine agent, false positive.

---

⚠️ Threats and Limitations

Threats to Validity

Type Threat Status
Internal Same author proposes the candidate, the failure conditions, the baselines, and the thresholds Pre-registration; invite external review
Internal Weak or straw-man baselines Include B2, B4, B5; report B3 as a ceiling
Construct "Anomaly" and "harm" are simulated by the experimenter State explicitly; M1–M2 count policy violations, not harm
Construct Recovery correctness (M6) measured against ground truth that exists only in simulation Report as an upper bound
External Simulated network, simplified adversary, synthetic workload No generalization claimed
Conclusion Few scenario classes; thresholds are proposals Report all outcomes
Literature Runtime-verification and anomaly-detection literature not reviewed in depth Acknowledge

Limitations inherited from the AetherMesh substrate

Telemetry and halt records are replicated over AetherMesh, so its limitations carry over:

· Eventual, not strong, consistency; no global order.
· Filters only predicate-detectable invalid deltas.
· Assumes a trustworthy key registry.
· The delta set grows without compaction.
· Compatibility matrix, digest form, fanout policy, forwarding policy, and compaction are underspecified.
· The determinism requirement is not enforced mechanically.
· Dynamic membership, access control beyond key registration, privacy of deltas, and integration with the other layers are not treated.

When not to use AetherRuntime

Scenario Reason
Small, co-located teams or few agents A conventional central monitor has lower complexity.
Strong consistency requirements Halting must be immediate and global; not expressible as join-semilattice updates.
Validity must hold before visibility If a halted agent's actions must be undone before any node observes them, a gate before execution is required.
Adversarial settings beyond the stated threat model Where colluding or well-funded adversaries are expected, a lightweight monitor is insufficient.
Constrained nodes Because the telemetry set grows without compaction, nodes with small storage budgets may not be able to hold replicas.

---

📋 Research Status Statement

Item Status
Document type Research article (hypothesis only)
Version / record 0.1.0, November 2026 · AETHERRUNTIME-01 · DOI 10.5281/zenodo.24078477
Implementation ❌ Not built (specification only)
Tests ❌ None
Experiments ❌ None
PyPI package ⏳ Not yet published
Real-world deployment None; no deployed system has been benchmarked
Propositions P1–P2 Stated with proof sketches; not machine-checked; conditional on A1–A6
Byzantine evaluation Not attempted
Third-party claims As reported by cited sources; not independently verified
Review status Not peer reviewed

<details>
<summary><b>Reconciliation notes (v0.1.0 departures from the supplied draft material)</b></summary>

1. Failure conditions — the definitions, the requirement list R1–R6, and the decision rule are the writer's proposals.
2. AetherMesh DOI — the supplied reference list gave 10.5281/zenodo.24053492 for AetherMesh (v2.0.0), whereas the DOI supplied for the AetherMesh paper was 10.5281/zenodo.24038038 (v1.0.0). The latter is used throughout.
3. Reference check — all 25 entries correspond to the intended publications.
4. Figures — the six supplied figures were generated for this record.
5. Layers versus dimensions — the supplied text calls the six items "dimensions" and the runtime sub-components "layers"; this usage is kept.
6. Format — the brief requested Markdown; the record is a PDF, as requested separately.

</details>

Catalogues: 20 open questions (Q1–Q20) across monitoring, detection, containment, halt, recovery, interfaces, and evaluation method. See Appendix C of the paper.

---

🌍 Platforms & Mirrors

Platform URL Role Status
GitHub gitdeeper15/aetherruntime Source code, issues, PRs ⏳ Active
GitLab gitlab.com/gitdeeper15/aetherruntime Mirror repository ⏳ Active
Codeberg codeberg.org/gitdeeper15/aetherruntime Mirror repository ⏳ Active
Bitbucket bitbucket.org/gitdeeper15/aetherruntime Mirror repository ⏳ Active
PyPI pypi.org/project/aetherruntime Python package (0.1.0) ⏳ Not yet published
Zenodo 10.5281/zenodo.24078477 Citable DOI, paper archive ✅ Published
OSF (pending) Registration ⏳ Pending
Website aether-runtime.netlify.app Live documentation ⏳ Deploying
ORCID 0009-0003-8903-0029 Author identity ✅ Active

---

🗂️ Project Structure

<details>
<summary><b>Click to expand the repository tree</b></summary>

```text
AetherRuntime/
├── src/
│   └── aetherruntime/              # Planned reference implementation
│       ├── __init__.py
│       ├── __version__.py
│       ├── models.py
│       ├── cli.py
│       └── ...
├── tests/                          # Planned test suite
├── experiments/                    # Planned experiments
├── docs/
│   ├── figures/
│   │   ├── Fig1_Six_Dimensions.png
│   │   ├── Fig2_Runtime_Layers.png
│   │   ├── Fig3_Runtime_Lifecycle.png
│   │   ├── Fig4_Anomaly_Detection.png
│   │   ├── Fig5_Runtime_vs_Verification.png
│   │   └── Fig6_Runtime_State_Machine.png
│   └── paper/
│       ├── AetherRuntime_Research_Paper.md
│       └── AetherRuntime_Research_Paper.pdf
├── PUBLICATION/
│   └── AetherRuntime_Research_Paper.pdf
├── PAPER_PARTS/                    # Paper sections (Markdown)
│   ├── 00_Title_Page.md
│   ├── 01_Abstract.md
│   ├── ...
│   └── 16_Research_Status_Statement.md
├── AUTHORS.md
├── CHANGELOG.md
├── CITATION.cff
├── CONTRIBUTING.md
├── INVENTORY.md
├── LICENSE
├── PROJECT_SUMMARY.txt
├── README.md
├── VERSION
├── manifest.json
├── netlify.toml
├── requirements.txt
└── scientific_state.json
```

</details>

---

🕓 Version History

Version Release Focus Status
v0.1.0 2026-11-09 Formalization: 5 failure conditions, 5 layers, 2 propositions, 20 open questions ✅ Released
(planned) 2027+ Reference implementation, tests, experiments ⏳ Not executed

---

📖 Citation

Primary Manuscript — AetherRuntime v0.1.0

```bibtex
@techreport{baladi2026aetherruntime,
  author       = {Baladi, Samir},
  title        = {AetherRuntime: A Falsification-First Investigation of Runtime Assurance in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24078477},
  url          = {https://doi.org/10.5281/zenodo.24078477},
  note         = {Architectural Hypothesis Under Investigation --- Not a committed project.}
}
```

---

👤 Author

Samir Baladi
Interdisciplinary AI Researcher — Ronin Institute / Rite of Renaissance

 
Research Area Distributed Systems / Software Engineering / Institutional Analysis
Research Domain Runtime Assurance, Monitoring, Anomaly Detection, Containment, Halt, Recovery, Multi-Agent Systems
Research Type Architectural Hypothesis
📧 Email gitdeeper@gmail.com
🔗 ORCID 0009-0003-8903-0029
🐙 GitHub gitdeeper15/aetherruntime
🦊 GitLab gitlab.com/gitdeeper15/aetherruntime
🟦 Codeberg codeberg.org/gitdeeper15/aetherruntime
🪣 Bitbucket bitbucket.org/gitdeeper15/aetherruntime
🐝 PyPI pypi.org/project/aetherruntime
🌐 Official Site aether-runtime.netlify.app

---

⚖️ License

Scope License
Code MIT License — Copyright © 2026 Samir Baladi
Documentation, manuscript, and figures CC-BY-4.0

<details>
<summary><b>MIT License — full text</b></summary>

```text
MIT License

Copyright (c) 2026 Samir Baladi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

</details>

---

<div align="center">

AetherRuntime — Program Manuscript v0.1.0 (Hypothesis)

© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)

Zenodo ·
OSF ·
Website ·
PyPI

</div>
