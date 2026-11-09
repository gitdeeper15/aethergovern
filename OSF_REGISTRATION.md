# AetherGovern: A Falsification-First Investigation of Governance in the Aether Family

---

**Registration DOI:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)
**Registration Type:** OSF Preregistration
**Registry:** OSF Registries
**Date Created:** Nov 9, 2026, 1:06 AM
**Date Registered:** Nov 9, 2026, 1:06 AM
**Associated Project:** [https://osf.io/we2tm](https://osf.io/we2tm)
**Internet Archive:** [https://archive.org/details/osf-registrations-tahc8-v1](https://archive.org/details/osf-registrations-tahc8-v1)
**License:** CC-By Attribution 4.0 International
**Contributor:** Samir Baladi

---

## Data / Analytic Code / Materials / Papers / Supplements

The following files were attached to this registration:

- `AetherGovern_Research_Paper.pdf` (v0.1.0, 33 pages)

---

## Overview

### Research questions or hypotheses

AetherGovern investigates the following structural questions:

**RQ1 (Redundancy):** Do the existing four Aether dimensions — AetherGit (storage), AetherFlow (integration), AetherProof (specification), AetherMesh (decentralization) — already cover the authorization, policy, accountability, revocation, and dispute-resolution requirements of multi-agent software ecosystems, or is there a gap that warrants a fifth functional dimension?

**RQ2 (Orthogonality):** Can authorization decisions, and the trust anchors from which they derive, be reduced to proof obligations in AetherProof without loss, or is governance a genuinely orthogonal concern that cannot be subsumed by verification?

**RQ3 (Decentralizability):** Can governance be specified without a trusted central authority and without violating the determinism requirement (A6) of AetherMesh, or does any decentralized design inevitably reintroduce a central coordinator or an irreducible exposure window?

**RQ4 (Observable Benefit):** Do there exist scenario classes in which the Aether family with governance outperforms the family without it, on a pre-specified metric, or is the addition of a governance dimension structurally unnecessary?

These are structural questions about the composition of four known mechanisms (storage, integration, verification, decentralization) and a candidate fifth (governance) as a single architecture for multi-agent software ecosystems. They are not empirical hypotheses about a deployed system.

### Foreknowledge of data or evidence

Data does not yet exist. No part of the data that will be used for this analysis plan exists, and no part will be generated until after this plan is registered.

### Explanation of foreknowledge and managing unintended influences

AetherGovern is a formal investigation (v0.1.0) with no implementation and no empirical data. The investigation is argument-only.

No real-world deployment data exists. The five failure conditions (F1–F5) and the requirement list (R1–R6) were stated before the candidate was described, to prevent circularity. The provisional assessment of F1–F4 is based on argument alone; F5 (observable benefit) is untested.

To manage unintended influences:
- The failure conditions were stated before the assessment (falsification-first).
- "Not falsified" is explicitly not promoted to "confirmed".
- The five layers and two propositions are labeled as hypotheses / proof sketches.
- The final project structure (single, dual, or triple project) is explicitly left undetermined.
- No implementation, experiment, or measurement is claimed.
- The paper is not peer reviewed.

---

## Research Design

### Study type

Other: AetherGovern is an argument-based investigation, not an empirical study.

### Intention for causal interpretation

No causal relationship inferred: This study is not intended to inform a causal relationship.

### Blinding of experimental treatments

No blinding is involved.

### Study design

AetherGovern is a structured investigation of whether a governance gap genuinely exists in the Aether family. The study design has three parts.

**(1) Falsification-first methodology.** Five failure conditions (F1–F5) and a requirement list (R1–R6) are stated before the candidate is described. The decision rule maps outcomes to conclusions before any outcome is known. The five conditions are:
- F1 (Non-redundancy): every requirement R1–R6 is met by existing mechanisms or by a bounded extension of a single existing dimension.
- F2 (Orthogonality to verification): every authorization decision and trust anchor can be encoded as a verified proposition.
- F3 (Boundary with orchestration): governance reduces to task assignment plus conventional access control.
- F4 (Decentralizability): any design preserving the required properties needs a central authority or strong consistency.
- F5 (Observable benefit): no scenario class can be constructed in which the best existing baseline fails and governance succeeds.

**(2) Three candidate capabilities.** Orchestration (AetherOrchestrate), governance (AetherGovern), and runtime assurance (AetherRuntime) are compared against potential architectural overlap. AetherGovern is examined in depth because it has the largest number of fragments already present in the existing records (key registry in AetherMesh; review roles in AetherProof).

**(3) Provisional assessment.** F1–F4 are not falsified by argument, with stated residual weaknesses. F5 (observable benefit) is untested. The paper does not promote "not falsified" to "confirmed". No implementation, experiment, or measurement is reported. The evaluation design (Section 7) specifies what would be tested, not what was tested.

No human subjects, no randomization, no blinding. The unit of analysis is the architectural specification, not a population. The study is argument-based; the evaluation design (M1–M9 metrics, B1–B5 baselines) is a proposal, not a result.

The proposed architecture has five layers (Authorization, Policy, Accountability, Revocation, Dispute Resolution) and two propositions with proof sketches: (P1) causal-authority admission preserves the determinism requirement of AetherMesh (assumption A6); (P2) revocation is monotone and can be recorded without coordination, but leaves an irreducible exposure window. Neither proposition is machine-checked.

The final project structure (single, dual, or triple project) is explicitly left undetermined. It will be decided after comparison with the other two candidate capabilities.

### Randomization

Not applicable. No randomization is involved. This is an argument-based investigation.

---

## Sampling

### Data collection procedures

AetherGovern is an argument-based investigation, not an empirical study. There is no population to sample, no sampling frame, no recruitment, and no eligibility criteria.

The "data" for this investigation consists of the formal artifacts of the four existing Aether dimensions (AetherGit, AetherFlow, AetherProof, AetherMesh) and the candidate fifth dimension (AetherGovern). These artifacts are not empirical data; they are the output of formal specification work, not of data collection.

No new data is collected. No experiment is run. No measurement is made. The investigation is based on:
- The four existing preprints (Baladi 2026a–d), each published on Zenodo.
- The institutional-economics literature on governance (Hardin 1968; Ostrom 1990; North 1990; Williamson 1985; Lessig 1999; DeNardis 2014; Brousseau and Glachant 2008; Weitzner et al. 2008; Schneier 2012).
- The technical literature on distributed systems (CRDTs, gossip, BFT).

The five failure conditions (F1–F5) and the requirement list (R1–R6) are the author's proposals. The provisional assessment of F1–F4 is based on argument alone. F5 (observable benefit) is untested.

If a future stage performs the evaluation of Section 7, a separate pre-registration will be created before any data is collected.

### Sample size

Not applicable. No sample size is defined because no data is collected.

The investigation is argument-based. The "sample" is the set of four existing Aether preprints plus the candidate, not a population of subjects or events. The number of artifacts in this registration (1 manuscript, 5 figures, 4 fifth-layer studies) is determined by the scope of the investigation, not by a sampling strategy or power analysis.

If a future stage performs the evaluation of Section 7 (M1–M9 metrics, B1–B5 baselines), the sample size (number of scenario classes, number of runs, number of nodes) will be specified in a separate pre-registration before data collection begins.

### Sample size rationale

Not applicable. No sample size rationale is needed because no data is collected.

The scope of the investigation (one manuscript, five figures, four fifth-layer studies) is determined by the number of existing Aether dimensions (four) and the number of candidate capabilities (three), not by a sampling strategy or power analysis.

No power analysis is performed. No decision rule for stopping data collection is defined, because no data collection occurs.

### Starting and stopping rules

Not applicable. There are no starting or stopping rules because no data collection is performed.

The investigation was developed iteratively across four documents (the manuscript and the four fifth-layer studies). The final document (04_comparison.md, pending) will mark the end of the investigation.

Future work (v0.2.0+) will define starting and stopping rules for the evaluation of Section 7 in a separate pre-registration.

---

## Variables

### Manipulated variables

None. AetherGovern is an argument-based investigation, not an empirical study. There are no manipulated variables, no treatment arms, and no randomization.

The "variables" of the investigation are formal objects, not measured quantities:
- The five failure conditions (F1–F5).
- The six requirements (R1–R6).
- The five governance layers (Authorization, Policy, Accountability, Revocation, Dispute Resolution).
- The two propositions (P1, P2).

These are formal constructs of the specification, defined in the manuscript and in the fifth-layer studies. They are not manipulated in any experimental sense.

If a future stage performs the evaluation of Section 7, the manipulated variables (e.g., network size, fanout, revocation rate, Byzantine fraction) will be specified in a separate pre-registration before data collection begins.

### Measured variables

None. No variables are measured because no data is collected and no empirical study is performed.

The "measured variables" of the investigation are formal constructs, not measured quantities:
- The status of each failure condition (not falsified / falsified / untested).
- The residual weaknesses of each condition.
- The proof sketches of P1 and P2 (as sketches, not machine-checked).
- The interfaces between AetherGovern and the four existing dimensions.

These are not measured variables in the empirical sense. They are formal artifacts of the specification, defined in the manuscript.

If a future stage performs the evaluation of Section 7, the measured variables (M1–M9) will be specified in a separate pre-registration before data collection begins.

### Indices

Not applicable. No indices or derived variables are constructed because no empirical data is collected.

The investigation does not combine measured variables into indices. The status of each failure condition is reported individually (F1: not falsified; F2: not falsified narrowly; F3: not falsified in decentralized setting; F4: not falsified with residuals; F5: untested). These are qualitative judgements, not derived variables.

If a future stage performs the evaluation of Section 7, the indices (e.g., unauthorized-action admission rate M1, exposure count M2, attribution accuracy M5) will be specified in a separate pre-registration before data collection begins.

---

## Analysis Plan

### Statistical models

AetherGovern does not use inferential statistical models. It is an argument-based investigation, not a hypothesis test. There is no ANOVA, no regression, no SEM, and no p-values.

The "analysis" in this investigation is formal, not statistical:
- The five failure conditions (F1–F5) are stated as conditions whose satisfaction would falsify the candidate.
- The six requirements (R1–R6) are the author's proposals.
- The decision rule maps outcomes of F1–F5 to conclusions (single, dual, or triple project).
- The two propositions (P1, P2) are stated with proof sketches, not machine-checked.

The provisional assessment of F1–F4 is based on argument alone. The assessment of F5 (observable benefit) is untested.

No controls, no manipulation checks, no convergence criteria (in the statistical sense), no assumption tests. The investigation is argument-based.

If a future stage performs the evaluation of Section 7, the statistical models (e.g., comparison of M1–M9 metrics against B1–B5 baselines) will be specified in a separate pre-registration before data collection begins.

### Transformations

No transformations are applied. No data is collected, so no transformations are performed.

The formal objects in AetherGovern (failure conditions, requirements, layers, propositions) are defined by the specification, not transformed from raw data.

Categorical variables: none. The status of each failure condition is a qualitative label (not falsified / falsified / untested), not a transformed variable.

### Inference criteria

No inferential criteria are used. There are no p-values, no Bayes factors, no model fit indices, and no cutoff criteria. The investigation is argument-based.

No one-tailed or two-tailed tests. No multiple-comparison correction. No hypothesis tests are performed.

The only "criterion" is the decision rule of Section 3.3, which maps outcomes of F1–F5 to conclusions. This is a decision rule, not an inference criterion. The rule was stated before any outcome was known (falsification-first).

### Data inclusion and exclusion

No data is excluded. No data is collected, so no inclusion or exclusion criteria are defined.

The formal artifacts (one manuscript, five figures, four fifth-layer studies) are all included by design, not by a selection process.

No outlier handling. No exclusion criteria. The investigation does not use empirical data.

### Missing data

No missing data. No data is collected, so missingness is not a concern.

The formal investigation is complete as specified in v0.1.0. No data points are missing.

If a future stage performs the evaluation of Section 7, missing-data handling will be specified in a separate pre-registration before data collection begins.

### Other planned analysis

None beyond what is described above.

Possible future analyses (not planned for v0.1.0):
- Empirical evaluation of M1–M9 metrics against B1–B5 baselines (the evaluation design of Section 7).
- Comparative assessment of the other two candidate capabilities (AetherOrchestrate, AetherRuntime) against analogous failure conditions.
- Mechanized proofs of Propositions 1–2 in a proof assistant (Coq, Lean, or TLA+).
- Systematic review of access-control, capability, and trust-management literature for R1–R6.
- Decision on project structure (single, dual, or triple) after comparison with the other two candidates.

These are open questions (Q1–Q20) in the v0.1.0 paper, not part of v0.1.0.

---

## Other

### Context and additional information

AetherGovern is the fifth functional dimension (provisional) of the Aether family. The four existing dimensions are:

- AetherGit (storage and versioning): 10.5281/zenodo.23966896
- AetherFlow (integration and operational verification): 10.5281/zenodo.23979129
- AetherProof (specification and formal evidence): 10.5281/zenodo.24013124
- AetherMesh (distribution and eventual consistency): 10.5281/zenodo.24053492

The word "dimension" is chosen deliberately. Earlier descriptions used "layer", which suggests a vertical stack in which each layer depends on those below it. The relationships among the four works are not strictly hierarchical: AetherProof does not sit above AetherFlow in any enforcement sense, and AetherMesh can be adopted without AetherProof. We therefore describe them as functional dimensions, not hierarchical layers.

The investigation follows a falsification-first methodology: five failure conditions (F1–F5) and a requirement list (R1–R6) are stated before the candidate is described, and the final project structure (single, dual, or triple project) is determined after comparison.

Three candidate capabilities are compared: orchestration (AetherOrchestrate), governance (AetherGovern), and runtime assurance (AetherRuntime). AetherGovern is examined in depth because it has the largest number of fragments already present in the existing records (key registry in AetherMesh; review roles in AetherProof).

The proposed architecture has five layers: Authorization, Policy, Accountability, Revocation, and Dispute Resolution. Two propositions are stated with proof sketches: (P1) causal-authority admission preserves the determinism requirement of AetherMesh (assumption A6); (P2) revocation is monotone and can be recorded without coordination, but leaves an irreducible exposure window.

Status: Architectural Hypothesis Under Investigation (v0.1.0). No implementation is claimed. No real-world deployment has been evaluated. F1–F4 are not falsified by argument, with residual weaknesses. F5 (observable benefit) is untested. The final project structure (single, dual, or triple project) is undetermined. The paper is not peer reviewed.

DOI: 10.5281/zenodo.24054524
ORCID: 0009-0003-8903-0029

---

## Metadata

### Contributors

Samir Baladi

### Description

AetherGovern: A Falsification-First Investigation of Governance in the Aether Family

AetherGovern is a structured investigation of whether a governance gap genuinely exists in the Aether family, or whether it is already covered by the existing four dimensions:
- AetherGit (storage and versioning)
- AetherFlow (integration and operational verification)
- AetherProof (specification and formal evidence)
- AetherMesh (distribution and eventual consistency)

The investigation follows a falsification-first methodology: five failure conditions (F1–F5) are stated before the candidate is described, and the final project structure (single, dual, or triple project) is determined after comparison. Three candidate capabilities are compared: orchestration (AetherOrchestrate), governance (AetherGovern), and runtime assurance (AetherRuntime).

The proposed architecture has five layers: Authorization, Policy, Accountability, Revocation, and Dispute Resolution. Two propositions are stated with proof sketches: (P1) causal-authority admission preserves the determinism requirement of AetherMesh; (P2) revocation is monotone and can be recorded without coordination, but leaves an irreducible exposure window.

Status: Architectural Hypothesis Under Investigation (v0.1.0). No implementation is claimed. No real-world deployment has been evaluated. F1–F4 are not falsified by argument, with residual weaknesses. F5 (observable benefit) is untested. The paper is not peer reviewed.

DOI: 10.5281/zenodo.24054524
ORCID: 0009-0003-8903-0029

### Registration Type

OSF Preregistration

### Registry

OSF Registries

### Associated project

https://osf.io/we2tm

### Date Created

Nov 9, 2026, 1:06 AM

### Date registered

Nov 9, 2026, 1:06 AM

### Subjects

- Software Engineering
- Computer Sciences
- Physical Sciences and Mathematics

### Tags

- Accountability
- Aether Family
- AetherGovern
- Authority
- Cryptographic Delegation
- Decentralized Systems
- Dispute Resolution
- Falsification
- Governance
- Multi-Agent Systems
- Policy
- Policy Lifecycle
- Revocation

### Affiliated Institutions

No affiliated institutions

### Internet Archive link

https://archive.org/details/osf-registrations-tahc8-v1

### License

CC-By Attribution 4.0 International

### Registration DOI

10.17605/OSF.IO/TAHC8

---

## Citations

### APA

Baladi, S. (2026, November 9). AetherGovern: A Falsification-First Investigation of Governance in the Aether Family. OSF. https://doi.org/10.17605/OSF.IO/TAHC8

### MLA

Baladi, Samir. "AetherGovern: A Falsification-First Investigation of Governance in the Aether Family." OSF, 9 Nov. 2026. Web.

### Chicago

Baladi, Samir. 2026. "AetherGovern: A Falsification-First Investigation of Governance in the Aether Family." OSF. November 9. doi:10.17605/OSF.IO/TAHC8.

### BibTeX

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

Source: Center for Open Science · OSF Registries
Retrieved: 2026-11-09
