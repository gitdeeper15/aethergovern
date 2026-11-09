# AetherGovern — Changelog

All notable changes to this research project will be documented in this file.

## [2.0.0] — 2026-11-09

### Reference Implementation

First reference implementation of the AetherGovern architecture
specified in v0.1.0.

**Published:**
- **Zenodo DOI (v0.1.0):** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
- **OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)
- **PyPI:** `aethergovern 2.0.0` (planned)
- **Website:** [aethergovern.netlify.app](https://aethergovern.netlify.app)

### Added — Operational Specification

- `docs/specification/01_entities.md` — 10 entities, 63 fields, 33 relations, 35 invariants
- `docs/specification/02_operations.md` — 7 operations, 28 inputs, 19 errors
- `docs/specification/03_invariants.md` — 47 invariants (35 structural + 7 operational + 5 cross-cutting)
- `docs/specification/04_interfaces.md` — 4 interfaces with the Aether family
- `docs/specification/05_test_design.md` — ~60 tests across 7 files

### Added — Source Code

- `src/aethergovern/` package (15 modules, ~1,540 lines):
  - `models.py` — 10 entities, 5 enums
  - `authorization/` — `grant`, `delegate`, `revoke`, `check`
  - `policy/` — `apply_policy`, `policy_hash`
  - `revocation/` — `add_revocation`, `join_frontiers`, `is_revoked`
  - `accountability/` — `create_record`, `verify_hash_link`, `query_by_action`
  - `dispute/` — `escalate`, `resolve_by_rule`
  - `simulation/` — `Network`, `Node`, `Testbed`
  - `cli.py` — CLI (`aethergovern info|verify`)

### Added — Tests

- `tests/` package (7 files, **60 tests**):
  - `test_models.py` — 10
  - `test_authorization.py` — 8
  - `test_policy.py` — 8
  - `test_revocation.py` — 8
  - `test_accountability.py` — 7
  - `test_dispute.py` — 7
  - `test_simulation.py` — 12

### Added — Experiments

- `experiments/authorization_correctness/` — M1 (unauthorized admission rate)
- `experiments/exposure_window/` — M2, M3 (exposure count, duration)
- `experiments/attribution_accuracy/` — M4, M5 (attribution completeness, accuracy)
- All three experiments reproducible via `python experiments/*/run.py`

### Added — Reports

- `REPORTS/v2.0.0/report.md` — full evaluation report

### Added — Packaging

- `pyproject.toml` — PEP 621 build config, `[build-system]`, dependencies
- `upload_aethergovern.py` — PyPI uploader (supports PyPI + TestPyPI)
- `src/aethergovern/py.typed` — PEP 561 marker

### Changed

- `VERSION`: 0.1.0 → 2.0.0
- `CITATION.cff`: 0.1.0 → 2.0.0
- `manifest.json`: 0.1.0 → 2.0.0
- `scientific_state.json`: 0.1.0 → 2.0.0
- `PROJECT_SUMMARY.txt`: 0.1.0 → 2.0.0
- `INVENTORY.md`: 0.1.0 → 2.0.0
- `README.md`: added v2.0.0 section, implementation status, test/coverage badges
- `AUTHORS.md`: updated status to v2.0.0
- `CONTRIBUTING.md`: updated to v2.0.0
- `netlify.toml`: updated to v2.0.0
- `requirements.txt`: updated to v2.0.0

### Related Identifiers

- **Zenodo DOI (v0.1.0):** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
- **Concept DOI:** [10.5281/zenodo.24054523](https://doi.org/10.5281/zenodo.24054523)
- **OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)
- **PyPI:** `aethergovern 2.0.0` (planned)
- **GitHub Release:** [v2.0.0](https://github.com/gitdeeper15/aethergovern/releases/tag/v2.0.0)

### Status

| Dimension | Status |
|---|---|
| Manuscript (v0.1.0) | Complete (33 pages, PDF) |
| Implementation | ✅ Built (`src/aethergovern/`, 15 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed |
| PyPI Package | ⏳ Not yet published |
| Real-world deployment | ❌ Not evaluated |
| Peer review | ❌ Not reviewed |

---

## [0.1.0] — 2026-11-09

### Architectural Hypothesis Under Investigation

First public release of AetherGovern: a structured investigation of
whether a governance gap genuinely exists in the Aether family.

**Published:**
- **Zenodo DOI:** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
- **OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)
- **Website:** [aethergovern.netlify.app](https://aethergovern.netlify.app)

### Added — Manuscript

- `PUBLICATION/AetherGovern_Research_Paper.pdf` — 33-page research article
  - 4 definitions (as layers)
  - 2 propositions (with proof sketches)
  - 5 failure conditions (F1–F5)
  - 6 requirements (R1–R6)
  - 20 open questions (Q1–Q20)
  - 25 references
- `docs/figures/` — 5 figures (Fig1–Fig5)
- `docs/fifth-layer-study/` — 4 markdown files (Orchestrate, Govern, Runtime, Comparison)

### Added — Methodology

- Falsification-first approach

### Added — Documentation

- `README.md`, `AUTHORS.md`, `CONTRIBUTING.md`, `INVENTORY.md`,
  `PROJECT_SUMMARY.txt`, `CITATION.cff`, `manifest.json`,
  `scientific_state.json`, `OSF_REGISTRATION.md`

### Related Identifiers

- **Zenodo DOI:** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
- **Concept DOI:** [10.5281/zenodo.24054523](https://doi.org/10.5281/zenodo.24054523)
- **OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)
- **GitHub Release:** [v0.1.0](https://github.com/gitdeeper15/aethergovern/releases/tag/v0.1.0)
- **PyPI:** Not published (v0.1.0 claims no implementation)

---

**Last Updated:** 2026-11-09
**Current Version:** 2.0.0
