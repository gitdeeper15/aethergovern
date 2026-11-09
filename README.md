<div align="center">

# 🏛️ AetherGovern

### A Falsification-First Investigation of Governance in the Aether Family

*Authority, Policy, and Accountability in Multi-Agent Software Ecosystems*

<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24054524.svg)](https://doi.org/10.5281/zenodo.24054524)
[![License: MIT + CC-BY-4.0](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--4.0-crimson.svg)](LICENSE)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--8903--0029-a6ce39?logo=orcid&logoColor=white)](https://orcid.org/0009-0003-8903-0029)
[![Release](https://img.shields.io/badge/Release-v2.0.0-green)](https://github.com/gitdeeper15/aethergovern/releases/tag/v2.0.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)

[![PyPI](https://img.shields.io/badge/PyPI-2.0.0-gold?logo=pypi&logoColor=white)](https://pypi.org/project/aethergovern/)
[![Tests](https://img.shields.io/badge/Tests-60%20passed-brightgreen)](tests/)
[![Experiments](https://img.shields.io/badge/Experiments-3%2F3-brightgreen)](experiments/)

[![Zenodo](https://img.shields.io/badge/Zenodo-Published-blue)](https://doi.org/10.5281/zenodo.24054524)
[![Record ID](https://img.shields.io/badge/Record%20ID-AETHERGOVERN--02-informational)](https://doi.org/10.5281/zenodo.24054524)
[![OSF](https://img.shields.io/badge/OSF-10.17605%2FOSF.IO%2FTAHC8-blue)](https://doi.org/10.17605/OSF.IO/TAHC8)
[![Website](https://img.shields.io/badge/Website-aethergovern.netlify.app-00C7B7?logo=netlify&logoColor=white)](https://aethergovern.netlify.app)
[![Aether Family](https://img.shields.io/badge/Aether%20Family-5%20dimensions-purple)](https://aethergovern.netlify.app)

<br>

**[📄 Paper](https://doi.org/10.5281/zenodo.24054524)** ·
**[🌐 Website](https://aethergovern.netlify.app)** ·
**[📦 Releases](https://github.com/gitdeeper15/aethergovern/releases)** ·
**[⚙️ Installation](#️-installation)** ·
**[📖 Citation](#-citation)**

</div>

---

> [!WARNING]
> **Status: v2.0.0 — Reference Implementation (preliminary results).**
> A reference implementation is built (`src/aethergovern/`, 15 modules, 60 tests) and 3 experiments are completed.
> **Experiments use simulated data; no real-world deployment is evaluated.**
> Propositions P1–P2 are **proof sketches**, not machine-checked; they hold only under assumptions A1–A6 (inherited from [AetherMesh](https://doi.org/10.5281/zenodo.24038038)).
> The v0.1.0 hypothesis (F1–F5) is **not falsified** by the implementation or the experiments, but it is also **not confirmed**.
> See [Threats and Limitations](#️-threats-and-limitations) and the [Research Status Statement](#-research-status-statement).

> *"AetherGovern is a candidate, not a result."*
> — AetherGovern v0.1.0, Section 8.5

> *"The simulation results here are an invitation to such evaluation, not a substitute for it."*
> — AetherGovern v0.1.0, Section 8.5

---

## 📑 Table of Contents

- [Overview](#-overview)
- [v2.0.0 at a Glance](#-v200-at-a-glance)
- [Installation](#️-installation)
- [Experiments (v2.0.0)](#-experiments-v200)
- [The Central Question](#-the-central-question)
- [The Five Functional Dimensions](#️-the-five-functional-dimensions)
- [The Falsification-First Methodology](#-the-falsification-first-methodology)
- [Failure Conditions F1–F5](#-failure-conditions-f1f5)
- [The Three Candidate Capabilities](#-the-three-candidate-capabilities)
- [AetherGovern: Architecture](#️-aethergovern-architecture)
- [Propositions](#-propositions)
- [Interfaces with the Aether Family](#-interfaces-with-the-aether-family)
- [Evaluation Design (v0.1.0 paper)](#-evaluation-design-v010-paper)
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

**AetherGovern** is the **fifth functional dimension** (provisional) of the Aether family — a candidate architecture for **authority, policy, accountability, revocation, and dispute resolution** in multi-agent software ecosystems.

The Aether family currently comprises **four foundational dimensions**, each published as a preprint on Zenodo (**not peer-reviewed**):

| Dimension | Focus | Question |
|---|---|---|
| **AetherGit** | Storage and versioning | How are changes stored and versioned? |
| **AetherFlow** | Integration and operational verification | How are changes integrated and verified? |
| **AetherProof** | Specification and formal evidence | How is correctness proven? |
| **AetherMesh** | Distribution and eventual consistency | How is state synchronized without a central coordinator? |

AetherGovern asks whether a **fifth dimension** is needed:

> **Who is authorized to do what, under which policy, with what accountability, and how is authority revoked?**

The investigation follows a **falsification-first methodology**: before describing the candidate, it states **five failure conditions (F1–F5)** whose satisfaction would show that the candidate does not deserve to exist as a separate dimension.

| Release | What it adds |
|---|---|
| **v0.1.0** | The hypothesis and the falsification-first methodology (paper) |
| **v2.0.0** | Reference implementation (`src/aethergovern/`): 15 modules, 60 tests, 3 reproducible experiments |

---

## 📊 v2.0.0 at a Glance

| Dimension | Status |
|---|---|
| Manuscript (v0.1.0) | Complete (33 pages, PDF) |
| Formal definitions / Propositions / Layers | 4 / 2 (proof sketches) / 5 |
| Implementation | ✅ Built — `src/aethergovern/` (15 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed (simulated data) |
| PyPI package | ✅ Published |
| Real-world deployment | ❌ Not evaluated |
| Causal claims | None (argument only) |

<p align="center">
  <img src="docs/figures/Fig1_Five_Dimensions.png"
       alt="AetherGovern — The Five Functional Dimensions of the Aether Family"
       width="100%">
</p>

<p align="center">
  <em>Figure 1 — The Five Functional Dimensions of the Aether Family (AetherGit, AetherFlow, AetherProof, AetherMesh, and the proposed hypothesis AetherGovern). The fifth dimension is a hypothesis under investigation, not a confirmed dimension.</em>
</p>

### Contributions to the Investigation

| # | Contribution | Kind |
|:-:|---|---|
| 1 | A falsification-first procedure with five failure conditions and a decision rule, stated before the candidate is described | Methodology |
| 2 | A comparison of three candidate capabilities that could fill a gap beside the four dimensions: orchestration, governance, and runtime assurance | Analysis |
| 3 | A hypothesized five-layer governance architecture, including a policy lifecycle, a scoped delegation model with revocation, and a statement of how governance differs from verification | Specification (hypothesis) |
| 4 | Two propositions with proof sketches that bear directly on F4: causal-authority admission preserves the determinism requirement of AetherMesh, and revocation leaves an irreducible exposure window | Analysis (proof sketches) |
| 5 | **A reference implementation** (v2.0.0) with 15 modules, 60 tests, and 3 reproducible experiments | Implementation |
| 6 | Twenty open questions (Q1–Q20) | Catalogue |

---

## ⚙️ Installation

```bash
# From PyPI
pip install aethergovern

# From source (development)
git clone https://github.com/gitdeeper15/aethergovern.git
cd aethergovern
pip install -e ".[dev]"

# Run tests
pytest

# Run experiments
python experiments/authorization_correctness/run.py
python experiments/exposure_window/run.py
python experiments/attribution_accuracy/run.py

# CLI
aethergovern info
aethergovern verify
```

Requires **Python 3.9+**. Runtime dependency: `cryptography >= 41.0`.

> [!NOTE]
> The PyPI version (`2.0.0`) is the **reference implementation**. It is **not a production system**. The v0.1.0 paper remains the authoritative hypothesis record.

---

## 🧪 Experiments (v2.0.0)

| # | Experiment | Result | Status |
|:-:|---|---|:-:|
| 1 | Authorization Correctness (M1) | 0.0000 unauthorized admission rate (10–500 nodes) | ✅ |
| 2 | Exposure Window (M2, M3) | M2 = 0; M3 median = 100 ms | ✅ |
| 3 | Attribution Accuracy (M4, M5) | M4 = 1.0; M5 = 1.0 | ✅ |

> [!IMPORTANT]
> Experiments use **simulated data**. These are preliminary results; no real-world deployment has been evaluated. See the full [evaluation report](REPORTS/v2.0.0/report.md).

---

## ❓ The Central Question

> **Is there a body of authorization, policy, accountability, revocation, and dispute-resolution requirements for multi-agent software ecosystems that (i) is not already specified by the four existing dimensions, (ii) is not reducible to verification or to orchestration, (iii) can be specified without reintroducing a central authority, and (iv) yields an observable benefit over existing mechanisms?**

The four clauses correspond to failure conditions **F1**, **F2 and F3** (clause ii), **F4**, and **F5**. A negative answer to any clause would show that governance, as a separate dimension, is not warranted.

---

## 🗺️ The Five Functional Dimensions

The word "dimension" is chosen deliberately. Earlier descriptions used "layer", which suggests a vertical stack. The relationships among the five works are not strictly hierarchical.

| # | Dimension | Focus | Question | DOI |
|:-:|---|---|---|---|
| 1 | **AetherGit** | Storage and versioning | How are changes stored and versioned? | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| 2 | **AetherFlow** | Integration and operational verification | How are changes integrated and verified? | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| 3 | **AetherProof** | Specification and formal evidence | How is correctness proven? | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| 4 | **AetherMesh** | Distribution and eventual consistency | How is state synchronized without a central coordinator? | [10.5281/zenodo.24038038](https://doi.org/10.5281/zenodo.24038038) |
| 5 | **AetherGovern** *(hypothesis)* | Authority and policy | Who is authorized to do what, under which policy? | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) |

<p align="center">
  <img src="docs/figures/Fig5_Governance_vs_Verification.png"
       alt="AetherGovern — Governance vs. Verification"
       width="100%">
</p>

<p align="center">
  <em>Figure 5 — Governance versus verification in the Aether family. Orthogonality is a hypothesis tested as failure condition F2.</em>
</p>

---

## 🔬 The Falsification-First Methodology

A typical architecture paper begins from a conviction that a component is needed and then specifies it. The risk is circular. AetherGovern adopts a falsification-first methodology:

1. **No prior assumption** that the gap exists.
2. **No prior assumption** that AetherGovern should be a separate project.
3. **Every claim** is tested against failure conditions (F1–F5).
4. The **final structure** (single project, dual project, triple project, or integration protocol) is determined *after* comparison.

---

## 🧭 Failure Conditions F1–F5

| ID | Claim under test | Falsified if… | Status |
|:-:|---|---|:-:|
| **F1** | Non-redundancy | Every requirement R1–R6 is met by existing mechanisms or by a bounded extension of a single existing dimension | 🟡 Not falsified (R1, R3, R5) |
| **F2** | Orthogonality to verification | Every authorization decision and trust anchor can be encoded as a verified proposition | 🟡 Not falsified (narrowly) |
| **F3** | Boundary with orchestration | Governance reduces to task assignment plus conventional access control | 🟡 Not falsified (decentralized setting) |
| **F4** | Decentralizability | Any design preserving the required properties needs a central authority or strong consistency | 🟡 Not falsified (with residuals) |
| **F5** | Observable benefit | No scenario class can be constructed in which the best existing baseline fails and governance succeeds | 🔴 Untested |

**Requirement list R1–R6:**

| ID | Requirement |
|:-:|---|
| R1 | Scoped, attenuating delegation |
| R2 | Authorized policy change |
| R3 | Revocation with dependents |
| R4 | Attribution |
| R5 | Dispute handling |
| R6 | Partition tolerance |

---

## 🎯 The Three Candidate Capabilities

| Candidate | Focus | Central question | Redundancy risk |
|---|---|---|:-:|
| **AetherOrchestrate** | Task scheduling and workflow | What should agents do next? | Medium |
| **AetherGovern** | Authority, accountability, revocation | Who may act, under which policy? | Medium |
| **AetherRuntime** | Live monitoring and rollback | Are agents behaving acceptably while running? | High |

AetherGovern is a candidate for addressing the authorization gap, provided it passes the falsification criteria (F1–F5). No claim is made that the other two candidates are weaker.

---

## 🏛️ AetherGovern: Architecture

> [!NOTE]
> All of this is **hypothesis**: a specification-level description of what a governance dimension might contain.

### The Five Governance Layers

<p align="center">
  <img src="docs/figures/Fig2_Governance_Layers.png"
       alt="AetherGovern — The Five Layers"
       width="100%">
</p>

<p align="center">
  <em>Figure 2 — The five layers of AetherGovern (hypothesis). Ordering reflects conceptual dependency, not an enforcement hierarchy.</em>
</p>

| Layer | Question | Status |
|:-:|---|:-:|
| **1 — Authorization** | Who may act? | Hypothesis |
| **2 — Policy** | Under which rules? | Hypothesis |
| **3 — Accountability** | Who is responsible? | Hypothesis |
| **4 — Revocation** | How is authority withdrawn? | Hypothesis |
| **5 — Dispute Resolution** | How are conflicts resolved? | Hypothesis |

### The Policy Lifecycle

<p align="center">
  <img src="docs/figures/Fig3_Policy_Lifecycle.png"
       alt="AetherGovern — The Policy Lifecycle"
       width="100%">
</p>

<p align="center">
  <em>Figure 3 — The policy lifecycle in AetherGovern (hypothesis): creation, approval, enforcement, revocation. Schematic; not a protocol specification.</em>
</p>

### Authority Delegation

<p align="center">
  <img src="docs/figures/Fig4_Authority_Delegation.png"
       alt="AetherGovern — Authority Delegation"
       width="100%">
</p>

<p align="center">
  <em>Figure 4 — Authority delegation via cryptographic signature chains in AetherGovern (hypothesis). Verification includes scope attenuation, expiry, and a revocation check.</em>
</p>

---

## 📜 Propositions

> [!NOTE]
> *Status: Stated with proof sketches; **not machine-checked**; conditional on assumptions A1–A6 (see [AetherMesh](https://doi.org/10.5281/zenodo.24038038)).*

| # | Proposition | Statement | Bears on |
|:-:|---|---|:-:|
| **P1** | Determinism of Causal-Authority Admission | If the admission predicate for an action consists of signature, attenuation, expiry, root recognition, and revocation checks evaluated at the revocation frontier cited by the action, and the cited frontier and policy version are in the action's causal closure, then the verdict is a deterministic function of the action and its causal closure, and the predicate satisfies assumption A6 of AetherMesh. | F4 |
| **P2** | Monotonicity of Revocation | Let `valid(c, F)` denote "chain `c` is valid at frontier `F`". If `F ≤ F'` then `valid(c, F') ⇒ valid(c, F)`. Equivalently, validity is antitone in the revocation frontier, and the revocation set can be maintained as a grow-only set whose join is union. | F4 |

---

## 🔗 Interfaces with the Aether Family

| Dimension | Requires from it | Provides to it | Coupling |
|---|---|---|:-:|
| **AetherGit** | Fields for authority and policy references; append-only governance records | Authorship authorization verdict | Low–medium |
| **AetherFlow** | Admission hook before verification; role for remediation | Authorization verdicts; remediation authority | Medium |
| **AetherProof** | Designation of governed specification changes | Authority for specification change; checkable policies | Medium |
| **AetherMesh** | Delta replication of governance records; determinism-compatible predicate | Registry with delegation, rotation, revocation | High |

**Minimal interface** (four artifacts, one rule): a delegation certificate record, a revocation record, an authority-frontier reference carried in each action, and the requirement that the authorization predicate satisfy Proposition 1.

> [!IMPORTANT]
> If the minimal interface is all that is needed, the whole contribution might be an extension of AetherMesh. The case for a standalone dimension rests on the layers beyond the minimal interface being separable and valuable. **That is a hypothesis for which this paper has no evidence.**

---

## 📊 Evaluation Design (v0.1.0 paper)

> [!IMPORTANT]
> In the v0.1.0 paper **no evaluation was performed**. That section specifies how the candidate would be evaluated, in a form that fixes in advance what outcomes would count as failure. Every metric, baseline, and threshold is a proposal. The v2.0.0 experiments above cover M1–M5 in simulation only.

| ID | Metric | Definition | Direction |
|:-:|---|---|:-:|
| **M1** | Unauthorized-action admission rate | Fraction of actions by agents lacking valid authority that are admitted | Lower is better |
| **M2** | Exposure count | Number of actions citing revoked authority that are admitted after the revocation is issued | Lower is better |
| **M3** | Exposure duration | Time from revocation issue to its receipt at each honest node | Lower is better |
| **M4** | Attribution completeness | Fraction of admitted actions for which the responsible chain can be recovered | Higher is better |
| **M5** | Attribution accuracy | Fraction of recovered chains that match the ground truth | Higher is better |
| **M6** | False-rejection rate | Fraction of legitimate actions rejected by governance checks | Lower is better |
| **M7** | Dispute handling | Median time to resolve conflicting claims | Lower is better |
| **M8** | Admission overhead | Added admission latency, CPU, storage per action | Lower is better |
| **M9** | Convergence preservation | Count of runs in which honest nodes end with different admitted sets | Must be zero if P1 holds |

---

## ⚠️ Threats and Limitations

### Threats to Validity

| Type | Threat | Status |
|---|---|---|
| Internal | Same author proposes the candidate, the failure conditions, the baselines, and the thresholds | Pre-registration; invite external review |
| Internal | Weak or straw-man baselines | Include B2, B4, B5; report B3 as a ceiling |
| Construct | “Unauthorized action” and “harm” are simulated by the experimenter | State explicitly; M1–M2 count policy violations, not harm |
| Construct | Attribution accuracy (M5) measured against a ground truth that exists only in simulation | Report as an upper bound |
| External | Simulated network, simplified adversary, synthetic workload | No generalization claimed |
| Conclusion | Few scenario classes; thresholds are proposals | Report all outcomes |
| Literature | Access-control literature not reviewed | Acknowledge |

### Limitations inherited from the AetherMesh substrate

Governance records are replicated over AetherMesh, so its limitations carry over:

- Eventual, not strong, consistency; no global order.
- Filters only predicate-detectable invalid deltas.
- Assumes a trustworthy key registry.
- The delta set grows without compaction.
- Compatibility matrix, digest form, fanout policy, forwarding policy, and compaction are underspecified.
- The determinism requirement is not enforced mechanically.
- Dynamic membership, access control beyond key registration, privacy of deltas, and integration with the other layers are not treated.

### When *not* to use AetherGovern

| Scenario | Reason |
|---|---|
| Small, co-located teams or few agents | A conventional central repository has lower complexity. |
| Strong consistency requirements | Unique-name allocation, exactly-once external effects, release gating, and any operation that needs a global order are not expressible as join-semilattice updates. |
| Validity must hold before visibility | If a merged program must be known to be correct before any agent can observe it, a gate before merge is required. |
| Adversarial settings beyond the stated threat model | Where colluding or well-funded adversaries are expected, a lightweight filter is insufficient. |
| Constrained nodes | Because the delta set grows without compaction, nodes with small storage budgets may not be able to hold replicas. |

---

## 📋 Research Status Statement

| Item | Status |
|---|---|
| Document type | Research article + reference implementation |
| Version / record | 2.0.0, November 2026 · AETHERGOVERN-02 · DOI 10.5281/zenodo.24054524 |
| Implementation | ✅ Built (`src/aethergovern/`, 15 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed (simulated data) |
| PyPI package | ✅ Published |
| Real-world deployment | None; no deployed system has been benchmarked |
| Propositions P1–P2 | Stated with proof sketches; not machine-checked; conditional on A1–A6 |
| Byzantine evaluation | Limited to malformed certificates |
| Third-party claims | As reported by cited sources; not independently verified |
| Review status | Not peer reviewed |

<details>
<summary><b>Reconciliation notes (v0.1.0 departures from the supplied draft material)</b></summary>

1. **Failure conditions** — the definitions, the requirement list R1–R6, and the decision rule are the writer's proposals.
2. **AetherMesh DOI** — the supplied reference list gave 10.5281/zenodo.24053492 for AetherMesh (v2.0.0), whereas the DOI supplied for the AetherMesh paper was 10.5281/zenodo.24038038 (v1.0.0). The latter is used throughout.
3. **Reference check** — all 25 entries correspond to the intended publications.
4. **Figures** — the five supplied figures were redrawn under their supplied filenames.
5. **Layers versus dimensions** — the supplied text calls the five items "dimensions" and the governance sub-components "layers"; this usage is kept.
6. **Format** — the brief requested Markdown; the record is a PDF, as requested separately.

</details>

**Catalogues:** 20 open questions (Q1–Q20) across authorization, policy, accountability, revocation, dispute resolution, interfaces, and evaluation method. See Appendix C of the [paper](https://doi.org/10.5281/zenodo.24054524).

---

## 🌍 Platforms & Mirrors

| Platform | URL | Role | Status |
|---|---|---|:-:|
| **GitHub** | [gitdeeper15/aethergovern](https://github.com/gitdeeper15/aethergovern) | Source code, issues, PRs | ✅ Active |
| **GitLab** | [gitlab.com/gitdeeper15/aethergovern](https://gitlab.com/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **Codeberg** | [codeberg.org/gitdeeper15/aethergovern](https://codeberg.org/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **Bitbucket** | [bitbucket.org/gitdeeper15/aethergovern](https://bitbucket.org/gitdeeper15/aethergovern) | Mirror repository | ✅ Active |
| **PyPI** | [pypi.org/project/aethergovern](https://pypi.org/project/aethergovern/) | Python package (`2.0.0`) | ⏳ Publishing |
| **Zenodo** | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) | Citable DOI, paper archive | ✅ Published |
| **OSF** | [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8) · [project](https://osf.io/we2tm) | Registration | ✅ Published |
| **Website** | [aethergovern.netlify.app](https://aethergovern.netlify.app) | Live documentation | ✅ Active |
| **ORCID** | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) | Author identity | ✅ Active |

---

## 🗂️ Project Structure

<details>
<summary><b>Click to expand the repository tree</b></summary>

```text
AetherGovern/
├── src/
│   └── aethergovern/                # Reference implementation (v2.0.0)
│       ├── __init__.py
│       ├── __version__.py
│       ├── models.py                # 10 entities, 5 enums
│       ├── cli.py
│       ├── py.typed
│       ├── authorization/
│       │   └── certificates.py      # grant, delegate, revoke, check
│       ├── policy/
│       │   └── enforcement.py       # apply_policy, policy_hash
│       ├── revocation/
│       │   └── frontier.py          # add_revocation, join_frontiers, is_revoked
│       ├── accountability/
│       │   └── records.py           # create_record, verify_hash_link, query_by_action
│       ├── dispute/
│       │   └── resolution.py        # escalate, resolve_by_rule
│       └── simulation/
│           ├── network.py           # Network, PartitionSchedule
│           ├── node.py              # Node, create_cluster
│           └── testbed.py           # Testbed, TestbedConfig
├── tests/                           # 60 tests, 7 files
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_authorization.py
│   ├── test_policy.py
│   ├── test_revocation.py
│   ├── test_accountability.py
│   ├── test_dispute.py
│   └── test_simulation.py
├── experiments/                     # 3 experiments
│   ├── authorization_correctness/
│   ├── exposure_window/
│   └── attribution_accuracy/
├── docs/
│   ├── figures/
│   │   ├── Fig1_Five_Dimensions.png
│   │   ├── Fig2_Governance_Layers.png
│   │   ├── Fig3_Policy_Lifecycle.png
│   │   ├── Fig4_Authority_Delegation.png
│   │   └── Fig5_Governance_vs_Verification.png
│   ├── fifth-layer-study/           # 4 markdown files (v0.1.0)
│   └── specification/               # 5 operational specification files
├── PUBLICATION/
│   ├── AetherGovern_Research_Paper.pdf    # v0.1.0 (33 pages)
├── REPORTS/
│   └── v2.0.0/
│       └── report.md
├── DATA/
├── ANALYSIS/
├── EXTERNAL_REVIEW/
├── VALIDATION/
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
├── pyproject.toml
├── requirements.txt
├── scientific_state.json
└── upload_aethergovern.py
```

</details>

---

## 🕓 Version History

| Version | Release | Focus | Status |
|---|---|---|:-:|
| **v2.0.0** | 2026-11-09 ([release](https://github.com/gitdeeper15/aethergovern/releases/tag/v2.0.0)) | Reference implementation: 15 modules, 60 tests, 3 experiments | ✅ Released |
| **v0.1.0** | 2026-11-09 ([release](https://github.com/gitdeeper15/aethergovern/releases/tag/v0.1.0)) | Formalization: 4 definitions, 2 propositions, 5 failure conditions, 20 open questions | ✅ Released |
| *(planned)* | 2027+ | Comparative study of the three candidate capabilities; evaluation design; decision on project structure | ⏳ Not executed |

---

## 📖 Citation

### Primary Manuscript — AetherGovern v0.1.0

```bibtex
@techreport{baladi2026aethergovern,
  author       = {Baladi, Samir},
  title        = {AetherGovern: A Falsification-First Investigation of Governance in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24054524},
  url          = {https://doi.org/10.5281/zenodo.24054524},
  note         = {Architectural Hypothesis Under Investigation --- Not a committed project.}
}
```

### Software — AetherGovern v2.0.0

```bibtex
@software{baladi2026aethergovern_v2,
  author       = {Baladi, Samir},
  title        = {{AetherGovern} v2.0.0: Reference Implementation of the Falsification-First Governance Architecture},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24054524},
  url          = {https://pypi.org/project/aethergovern/},
  note         = {Reference implementation. Available via pip install aethergovern.}
}
```

### OSF Registration

```bibtex
@misc{baladi2026aethergovern_osf,
  author       = {Baladi, Samir},
  title        = {{AetherGovern: A Falsification-First Investigation of Governance in the Aether Family}},
  year         = {2026},
  month        = nov,
  day          = {9},
  publisher    = {OSF},
  doi          = {10.17605/OSF.IO/TAHC8},
  url          = {https://doi.org/10.17605/OSF.IO/TAHC8},
  note         = {OSF Preregistration. Associated project: https://osf.io/we2tm}
}
```

---

## 👤 Author

**Samir Baladi**
*Interdisciplinary AI Researcher — Ronin Institute / Rite of Renaissance*

| | |
|---|---|
| **Research Area** | Distributed Systems / Software Engineering / Institutional Analysis |
| **Research Domain** | Governance, Authority, Policy, Accountability, Revocation, Dispute Resolution, Multi-Agent Systems |
| **Research Type** | Architectural Hypothesis + Reference Implementation |
| 📧 **Email** | [gitdeeper@gmail.com](mailto:gitdeeper@gmail.com) |
| 🔗 **ORCID** | [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029) |
| 🐙 **GitHub** | [gitdeeper15/aethergovern](https://github.com/gitdeeper15/aethergovern) |
| 🦊 **GitLab** | [gitlab.com/gitdeeper15/aethergovern](https://gitlab.com/gitdeeper15/aethergovern) |
| 🟦 **Codeberg** | [codeberg.org/gitdeeper15/aethergovern](https://codeberg.org/gitdeeper15/aethergovern) |
| 🪣 **Bitbucket** | [bitbucket.org/gitdeeper15/aethergovern](https://bitbucket.org/gitdeeper15/aethergovern) |
| 🐝 **PyPI** | [pypi.org/project/aethergovern](https://pypi.org/project/aethergovern/) |
| 🌐 **Official Site** | [aethergovern.netlify.app](https://aethergovern.netlify.app) |

---

## ⚖️ License

| Scope | License |
|---|---|
| **Code** | [MIT License](LICENSE) — Copyright © 2026 Samir Baladi |
| **Documentation, manuscript, and figures** | [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode) |

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

**AetherGovern — Program Manuscript v2.0.0 (Reference Implementation)**

© 2026 Samir Baladi — Ronin Institute / Rite of Renaissance — MIT (code) + CC-BY-4.0 (docs)

[Zenodo](https://doi.org/10.5281/zenodo.24054524) ·
[OSF](https://doi.org/10.17605/OSF.IO/TAHC8) ·
[Website](https://aethergovern.netlify.app) ·
[PyPI](https://pypi.org/project/aethergovern/)

</div>
