# Contributing to AetherGovern

**AetherGovern: A Falsification-First Investigation of Governance in the Aether Family**

---

## Status

This project is a **reference implementation** (`v2.0.0`) of the AetherGovern falsification-first governance architecture specified in `v0.1.0`.

The implementation includes:
- **15 modules** in `src/aethergovern/` (~1,540 lines)
- **60 tests** in `tests/`
- **3 experiments** in `experiments/`
- **5 specification documents** in `docs/specification/`

**No real-world deployment has been evaluated.** F1–F4 are not falsified by argument; F5 is untested. Propositions P1–P2 are stated with proof sketches, not machine-checked. The final project structure (single, dual, or triple project) remains undetermined.

Contributions at this stage are welcome in:

- **Implementation:** Bug fixes, new features, or improved modularity.
- **Tests:** Additional test cases, edge cases, or property-based tests.
- **Experiments:** Extensions to the simulation, new metrics, or new scenarios.
- **Specification:** Clarifications, corrections, or new invariants.
- **Documentation:** Examples, tutorials, or improved explanations.

**Not accepted at this stage:**

- Empirical claims presented as findings (no real-world deployment has been evaluated).
- Claims that "not falsified" means "confirmed" — it does not.
- Changes to the failure conditions, requirements, or propositions without a documented rationale.
- Claims that an implementation exists outside `src/aethergovern/`.

For extensions, open an issue first to discuss scope.

---

## Reporting Issues

Open an issue with:

- A one-sentence description.
- The affected file (e.g., `src/aethergovern/authorization/certificates.py`).
- A minimal reproduction or screenshot.
- Expected vs. actual behavior.
- For scientific claims: cite the specific invariant (`I*`), operation (`O*`), or proposition (`P*`) affected.

---

## Submitting Changes

```bash
git checkout -b feature/short-description
# make changes
git commit -m "feat: short description"
git push origin feature/short-description
```

Then open a pull request. Each PR should address one concern.

---

Standards

Language Standard
Python PEP 8, line length 100, ruff
Markdown markdownlint (MD013 disabled)
YAML yamllint
JSON valid JSON (verify with python3 -m json.tool)
TOML valid TOML (verify with python3 -c "import tomllib; ...")

---

Scientific Integrity Requirements

Because this is a research record with a published DOI, contributions must preserve:

1. Evidentiary status. No claim may be strengthened beyond what the manuscript supports. "Not falsified by argument" must never be read as "confirmed". Propositions 1–2 must remain labeled as proof sketches.
2. Failure condition transparency. Any claim that bears on F1–F5 must state which condition it bears on and what evidence would falsify it.
3. Limitation disclosure. Contributions that add results must also add the corresponding threats to validity.
4. Negative commitments. The following must remain explicit in all derived documents:
   · No real-world deployment has been evaluated.
   · F5 (observable benefit) is untested.
   · The final project structure (single, dual, or triple) is undetermined.
   · The paper is not peer reviewed.
5. No silent corrections to published records. The Zenodo DOI 10.5281/zenodo.24054524 archives the v0.1.0 manuscript. Corrections must be issued as a new version with its own DOI.

---

Reproducibility

The record for v0.1.0 did not include an implementation. v2.0.0 adds:

· src/aethergovern/ — the reference implementation
· tests/ — the test suite
· experiments/*/run.py — reproducible experiment scripts

To reproduce:

```bash
pip install -e ".[dev]"
pytest
python experiments/authorization_correctness/run.py
python experiments/exposure_window/run.py
python experiments/attribution_accuracy/run.py
```

---

Review Process

· All changes are reviewed by the maintainer (Samir Baladi).
· Changes to the specification, invariants, or propositions require explicit documentation in CHANGELOG.md with rationale.
· Changes that affect the published manuscript must be coordinated with a new Zenodo version, not a silent edit.

---

Contact

· Email: gitdeeper@gmail.com
· ORCID: 0009-0003-8903-0029
· Zenodo DOI: 10.5281/zenodo.24054524
· OSF Registration: 10.17605/OSF.IO/TAHC8
· Website: aethergovern.netlify.app
· GitHub: gitdeeper15/aethergovern

---

Thank you for helping improve the falsification-first investigation of governance in the Aether family.
