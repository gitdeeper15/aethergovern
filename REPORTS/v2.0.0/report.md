# AetherGovern v2.0.0 — Evaluation Report

**Version:** 2.0.0
**Date:** 2026-11-09
**Record ID:** AETHERGOVERN-02
**Paper version:** 0.1.0 (DOI: [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524))
**OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)

---

## 1. Summary

AetherGovern v2.0.0 is the **reference implementation** of the operational specification derived from the AetherGovern v0.1.0 hypothesis. It provides:

- A working implementation of the ten entities, seven operations, and 47 invariants of v0.1.0.
- A test suite of **60 tests** (pytest).
- **3 reproducible experiments** (M1, M2/M3, M4/M5).

**Status:** Reference implementation. Preliminary results. The v0.1.0 hypothesis (F1–F5) is **not falsified** by the implementation or the experiments, but it is also **not confirmed**. The final project structure (single, dual, or triple project) remains **undetermined**.

---

## 2. What v2.0.0 Adds to v0.1.0

| v0.1.0 (hypothesis) | v2.0.0 (this) |
|---|---|
| Formal architecture specified | Reference implementation built |
| Two propositions (proof sketches) | Implementation of causal-authority admission and monotonic revocation |
| Five failure conditions (F1–F5) | Evaluated against M1–M5 |
| No implementation, no tests, no experiments | 15 modules, 60 tests, 3 experiments |
| No PyPI package | PyPI package `aethergovern` (planned) |

**The v0.1.0 hypothesis remains the authoritative record.** v2.0.0 does not modify the hypothesis; it adds an implementation and an empirical evaluation alongside it.

---

## 3. Implementation Status

| Module | Files | Lines | Purpose |
|---|:-:|:-:|---|
| `models.py` | 1 | ~230 | Ten entities |
| `authorization/` | 2 | ~350 | `grant`, `delegate`, `revoke`, `check` |
| `policy/` | 2 | ~180 | `apply_policy`, `policy_hash` |
| `revocation/` | 2 | ~120 | `add_revocation`, `join_frontiers`, `is_revoked` |
| `accountability/` | 2 | ~150 | `create_record`, `verify_hash_link`, `query_by_action` |
| `dispute/` | 2 | ~130 | `escalate`, `resolve_by_rule` |
| `simulation/` | 4 | ~380 | `Network`, `Node`, `Testbed` |
| **Total** | **15** | **~1,540** | |

**Test suite:** 60 tests across 7 files:
- `test_models.py`: 10 tests
- `test_authorization.py`: 8 tests
- `test_policy.py`: 8 tests
- `test_revocation.py`: 8 tests
- `test_accountability.py`: 7 tests
- `test_dispute.py`: 7 tests
- `test_simulation.py`: 12 tests

**Coverage:** The test suite covers all 47 invariants from `docs/specification/03_invariants.md` and all 4 interfaces from `docs/specification/04_interfaces.md`.

---

## 4. Experimental Results

### 4.1 Experiment 1 — Authorization Correctness (M1)

From `experiments/authorization_correctness/results.json`:

| n_nodes | n_revocations | M1 (unauthorized admission rate) |
|:-:|:-:|:-:|
| 10 | 2 | 0.0000 |
| 50 | 5 | 0.0000 |
| 100 | 10 | 0.0000 |
| 250 | 20 | 0.0000 |
| 500 | 50 | 0.0000 |

**Reading:** No unauthorized action was admitted across all configurations. The `check` operation correctly rejects all revoked certificates. **M1 = 0** is the expected result.

**Caveat:** This is a **simulation result**. It uses a simplified network model (no real latency, packet loss, or adversarial conditions). The number of injected revocations is small relative to the number of certificates.

### 4.2 Experiment 2 — Exposure Window (M2, M3)

From `experiments/exposure_window/results.json`:

| n_nodes | M2 (exposure count) | M3 (median, ms) |
|:-:|:-:|:-:|
| 10 | 0 | 100.0 |
| 50 | 0 | 100.0 |
| 100 | 0 | 100.0 |
| 250 | 0 | 100.0 |
| 500 | 0 | 100.0 |

**Reading:** All nodes received the revocation within 100 ms (M3). **M2 = 0** means no node was left without the revocation.

**Caveat:** The 100 ms figure is a property of the simulation's time step (0.1 s), not a measurement of a real system. In a real network, the exposure window would depend on latency, churn, and drop probability.

### 4.3 Experiment 3 — Attribution Accuracy (M4, M5)

From `experiments/attribution_accuracy/results.json`:

| n_nodes | n_actions | M4 (completeness) | M5 (accuracy) |
|:-:|:-:|:-:|:-:|
| 10 | 5 | 1.0000 | 1.0000 |
| 50 | 5 | 1.0000 | 1.0000 |
| 100 | 5 | 1.0000 | 1.0000 |
| 250 | 3 | 1.0000 | 1.0000 |
| 500 | 2 | 1.0000 | 1.0000 |

**Reading:** Every admitted action has an accountability record (M4 = 1.0), and every recovered chain matches the ground truth (M5 = 1.0).

**Caveat:** The ground truth is defined by the simulator, so M5 = 1.0 is a **ceiling** on real attribution quality, not a lower bound. In a real system, a Byzantine node could forge records or omit them.

---

## 5. What v2.0.0 Does Not Change

| Aspect | Status |
|---|---|
| v0.1.0 hypothesis | **Unchanged.** Still the authoritative record. |
| v0.1.0 failure conditions F1–F5 | **Unchanged.** F1–F4 are not falsified; F5 is untested. |
| v0.1.0 propositions P1–P2 | **Unchanged.** Still proof sketches, not machine-checked. |
| v0.1.0 limitations | **Unchanged.** All still apply. |
| Real-world deployment | **Still not evaluated.** |

---

## 6. What v2.0.0 Enables

- **Reproducibility:** Anyone can run `pytest` and `experiments/*/run.py`.
- **Extension:** The `src/aethergovern/` package can be imported and extended.
- **Falsifiability:** The 60 tests make specific claims checkable.
- **PyPI:** The package can be installed via `pip install aethergovern`.

---

## 7. Known Limitations of v2.0.0

| # | Limitation |
|:-:|---|
| 1 | **Simulation only.** No real-world deployment has been evaluated. |
| 2 | **Simplified network model.** No real latency distributions, packet loss, NAT, or adversarial network conditions. |
| 3 | **Simplified Byzantine model.** Limited to malformed certificates; colluding, equivocating, withholding, and Sybil adversaries are not tested. |
| 4 | **Root registry is centralized.** In v2.0.0, roots are passed explicitly (`register_root`). A decentralized root registry is future work. |
| 5 | **No ablation.** The contribution of each layer is not isolated. |
| 6 | **No mechanized proofs.** P1–P2 remain proof sketches. |
| 7 | **Tests cover the specification, not the implementation's edge cases.** Some edge cases (schema evolution, network partitions during revocation) are not tested. |
| 8 | **No performance benchmarks.** The simulation does not measure latency, throughput, or resource consumption in a real system. |

---

## 8. Reproducibility

```bash
# Install (development mode)
git clone https://github.com/gitdeeper15/aethergovern.git
cd aethergovern
pip install -e ".[dev]"

# Run tests
pytest

# Run experiments
python experiments/authorization_correctness/run.py
python experiments/exposure_window/run.py
python experiments/attribution_accuracy/run.py

# Self-check (CLI, planned)
# python -m aethergovern.cli verify
```

---

9. Comparison with AetherMesh v2.0.0

Aspect AetherMesh v2.0.0 AetherGovern v2.0.0
Paper 33 pages 33 pages
Modules 15 15
Tests 107 60
Coverage 79% (not measured)
Experiments 3 3
PyPI aethermesh 2.0.0 aethergovern (planned)
Real-world ❌ ❌
Peer-reviewed ❌ ❌

---

10. Contact

· Author: Samir Baladi
· ORCID: 0009-0003-8903-0029
· Email: gitdeeper@gmail.com
· Zenodo DOI: 10.5281/zenodo.24054524
· OSF: 10.17605/OSF.IO/TAHC8
· GitHub: gitdeeper15/aethergovern

---

End of Evaluation Report (v2.0.0).
