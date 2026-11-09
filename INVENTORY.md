# AetherGovern — Complete Inventory

**Version:** 2.0.0 (Reference Implementation) + 0.1.0 (Formal Architecture)
**Release Date:** 2026-11-09
**Author:** Samir Baladi
**Email:** gitdeeper@gmail.com
**ORCID:** [0009-0003-8903-0029](https://orcid.org/0009-0003-8903-0029)
**License:** MIT (code) · CC-BY-4.0 (docs, manuscript, figures)
**Status:** Reference Implementation + Reproducible Experiments
**Record ID:** AETHERGOVERN-02
**DOI (Zenodo, v0.1.0):** [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524)
**Concept DOI:** [10.5281/zenodo.24054523](https://doi.org/10.5281/zenodo.24054523)
**OSF Registration:** [10.17605/OSF.IO/TAHC8](https://doi.org/10.17605/OSF.IO/TAHC8)

---

## Research Status

| Item | Status |
|---|---|
| Document type | Research article + reference implementation |
| Paper (v0.1.0) | Complete (33 pages, PDF) |
| Implementation (v2.0.0) | ✅ Built (`src/aethergovern/`, 15 modules) |
| Tests | ✅ 60 passed |
| Experiments | ✅ 3/3 completed |
| PyPI package | ⏳ Not yet published |
| Real-world deployment | None; no deployed system has been benchmarked |
| Propositions 1–2 | Stated with proof sketches; not machine-checked |
| Byzantine evaluation | Limited to malformed certificates |
| Review status | Not peer reviewed |

---

## Repository Links

| Platform | URL | Role | Status |
|----------|-----|------|--------|
| GitHub | https://github.com/gitdeeper15/aethergovern | Primary | ⏳ Active |
| GitLab | https://gitlab.com/gitdeeper15/aethergovern | Mirror | ⏳ Active |
| Codeberg | https://codeberg.org/gitdeeper15/aethergovern | Mirror | ⏳ Active |
| Bitbucket | https://bitbucket.org/gitdeeper15/aethergovern | Mirror | ⏳ Active |
| PyPI | https://pypi.org/project/aethergovern/ | Python package | ⏳ Not yet published |
| Zenodo | https://doi.org/10.5281/zenodo.24054524 | DOI (v0.1.0 paper) | ✅ Published |
| OSF | https://doi.org/10.17605/OSF.IO/TAHC8 | Registration | ✅ Published |
| Website | https://aethergovern.netlify.app | Live documentation | ✅ Active |
| ORCID | https://orcid.org/0009-0003-8903-0029 | Identity | ✅ Active |

---

## Manuscript Artifact (v0.1.0)

| File | Pages | MD5 |
|---|---|---|
| `PUBLICATION/AetherGovern_Research_Paper.pdf` | 33 | (see `PUBLICATION/`) |

---

## Root Files

| File | Purpose | Status |
|------|---------|:-:|
| `.gitignore` | Git ignore rules | ✅ |
| `AUTHORS.md` | Contributors | ✅ Updated |
| `CHANGELOG.md` | Version history (v0.1.0 + v2.0.0) | ✅ Updated |
| `CITATION.cff` | Citation metadata (v2.0.0) | ✅ Updated |
| `CONTRIBUTING.md` | Contribution guidelines | ✅ Updated |
| `INVENTORY.md` | This file | ✅ Updated |
| `LICENSE` | MIT + CC-BY-4.0 | ✅ |
| `PROJECT_SUMMARY.txt` | One-page summary (v2.0.0) | ✅ Updated |
| `README.md` | Main documentation (v2.0.0) | ✅ Updated |
| `VERSION` | `2.0.0` | ✅ Updated |
| `manifest.json` | Project manifest (v2.0.0) | ✅ Updated |
| `scientific_state.json` | Scientific state record (v2.0.0) | ✅ Updated |
| `netlify.toml` | Netlify configuration | ✅ Updated |
| `pyproject.toml` | PEP 621 build config (v2.0.0) | ✅ |
| `requirements.txt` | Python dependencies (v2.0.0) | ✅ Updated |
| `upload_aethergovern.py` | PyPI uploader | ✅ |

---

## Directories

| Directory | Contents | Status |
|-----------|----------|:-:|
| `PUBLICATION/` | AetherGovern + AetherMesh (reference) PDFs | ✅ |
| `docs/figures/` | 5 figures (Fig1–Fig5) | ✅ |
| `docs/fifth-layer-study/` | 4 markdown files | ✅ |
| `docs/specification/` | 5 operational specification files | ✅ |
| `src/aethergovern/` | Reference implementation (15 modules) | ✅ |
| `tests/` | Test suite (7 files, 60 tests) | ✅ |
| `experiments/` | 3 reproducible experiments | ✅ |
| `REPORTS/v2.0.0/` | Evaluation report | ✅ |
| `DATA/` | (empty) | — |
| `ANALYSIS/` | (empty) | — |
| `EXTERNAL_REVIEW/` | (empty) | — |
| `VALIDATION/` | (empty) | — |

---

## Source Code (`src/aethergovern/`)

| Module | File | Purpose |
|---|---|---|
| `__init__.py` | 1 | Package definition |
| `__version__.py` | 1 | Version info |
| `models.py` | 1 | 10 entities, 5 enums |
| `cli.py` | 1 | CLI (`info`, `verify`) |
| `authorization/certificates.py` | 1 | `grant`, `delegate`, `revoke`, `check` |
| `policy/enforcement.py` | 1 | `apply_policy`, `policy_hash` |
| `revocation/frontier.py` | 1 | `add_revocation`, `join_frontiers`, `is_revoked` |
| `accountability/records.py` | 1 | `create_record`, `verify_hash_link`, `query_by_action` |
| `dispute/resolution.py` | 1 | `escalate`, `resolve_by_rule` |
| `simulation/network.py` | 1 | `Network`, `PartitionSchedule` |
| `simulation/node.py` | 1 | `Node`, `create_cluster` |
| `simulation/testbed.py` | 1 | `Testbed`, `TestbedConfig` |

**Total:** 15 modules, ~1,540 lines.

---

## Test Suite (`tests/`)

| File | Tests |
|---|:-:|
| `test_models.py` | 10 |
| `test_authorization.py` | 8 |
| `test_policy.py` | 8 |
| `test_revocation.py` | 8 |
| `test_accountability.py` | 7 |
| `test_dispute.py` | 7 |
| `test_simulation.py` | 12 |
| **Total** | **60** |

---

## Experiments (`experiments/`)

| # | Directory | Metric | Results |
|:-:|---|---|:-:|
| 1 | `authorization_correctness/` | M1 (unauthorized-action admission rate) | ✅ `results.json` |
| 2 | `exposure_window/` | M2, M3 (exposure count, duration) | ✅ `results.json` |
| 3 | `attribution_accuracy/` | M4, M5 (attribution completeness, accuracy) | ✅ `results.json` |

---

## Figures

| File | Figure | Description |
|---|:-:|---|
| `docs/figures/Fig1_Five_Dimensions.png` | Fig 1 | Five functional dimensions |
| `docs/figures/Fig2_Governance_Layers.png` | Fig 2 | Five governance layers |
| `docs/figures/Fig3_Policy_Lifecycle.png` | Fig 3 | Policy lifecycle |
| `docs/figures/Fig4_Authority_Delegation.png` | Fig 4 | Authority delegation |
| `docs/figures/Fig5_Governance_vs_Verification.png` | Fig 5 | Governance vs. verification |

---

## Companion Works

AetherGovern is the **fifth functional dimension** (provisional) of the Aether family:

| # | System | Dimension | DOI |
|:-:|---|---|---|
| 1 | AetherGit | Storage | [10.5281/zenodo.23966896](https://doi.org/10.5281/zenodo.23966896) |
| 2 | AetherFlow | Integration | [10.5281/zenodo.23979129](https://doi.org/10.5281/zenodo.23979129) |
| 3 | AetherProof | Verification | [10.5281/zenodo.24013124](https://doi.org/10.5281/zenodo.24013124) |
| 4 | AetherMesh | Decentralization | [10.5281/zenodo.24053492](https://doi.org/10.5281/zenodo.24053492) |
| 5 | **AetherGovern** (provisional) | **Governance** | [10.5281/zenodo.24054524](https://doi.org/10.5281/zenodo.24054524) |

---

## Citation

### Paper (v0.1.0)

```bibtex
@techreport{baladi2026aethergovern,
  author       = {Baladi, Samir},
  title        = {AetherGovern: A Falsification-First Investigation of
                  Governance in the Aether Family},
  institution  = {Ronin Institute / Rite of Renaissance},
  type         = {Research Paper},
  year         = {2026},
  month        = {November},
  version      = {0.1.0},
  doi          = {10.5281/zenodo.24054524},
  url          = {https://doi.org/10.5281/zenodo.24054524}
}
```

Software (v2.0.0)

```bibtex
@software{baladi2026aethergovern_v2,
  author       = {Baladi, Samir},
  title        = {{AetherGovern} v2.0.0: Reference Implementation of the
                  Falsification-First Governance Architecture},
  year         = {2026},
  month        = {November},
  publisher    = {PyPI},
  version      = {2.0.0},
  doi          = {10.5281/zenodo.24054524},
  url          = {https://pypi.org/project/aethergovern/},
  note         = {Reference implementation. Available via pip install aethergovern.}
}
```

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24054524
· OSF DOI: 10.17605/OSF.IO/TAHC8
· PyPI: pypi.org/project/aethergovern
· Website: aethergovern.netlify.app
· GitHub: gitdeeper15/aethergovern

---

Last Updated: 2026-11-09
Current Version: 2.0.0
