#!/usr/bin/env python3
"""
AetherGovern v2.0.0 — PyPI Uploader

Uploads the built distribution files (wheel + sdist) to PyPI.

Prerequisites:
    1. Build the distribution:
           python -m build

    2. Set your PyPI API token as an environment variable:
           export PYPI_TOKEN='pypi-AgEIcHlwaS5vcmc...'

    3. Run this script:
           python upload_aethergovern.py

    Or upload to TestPyPI first (recommended):
           export PYPI_REPOSITORY=testpypi
           python upload_aethergovern.py

Environment variables:
    PYPI_TOKEN       (required)  PyPI API token (starts with 'pypi-')
    PYPI_REPOSITORY  (optional)  'pypi' (default) or 'testpypi'

Reference:
    AetherGovern v0.1.0 paper: https://doi.org/10.5281/zenodo.24054524
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("❌ 'requests' is required. Install with: pip install requests")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

PACKAGE_NAME = "aethergovern"
VERSION = "2.0.0"
ZENODO_DOI = "10.5281/zenodo.24054524"
OSF_DOI = "10.17605/OSF.IO/TAHC8"
ORCID_URL = "https://orcid.org/0009-0003-8903-0029"

UPLOAD_URLS = {
    "pypi": "https://upload.pypi.org/legacy/",
    "testpypi": "https://test.pypi.org/legacy/",
}

DIST_DIR = Path(__file__).parent / "dist"


# =============================================================================
# Classifiers
# =============================================================================

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering",
    "Topic :: System :: Distributed Computing",
]


# =============================================================================
# Helpers
# =============================================================================

def _read_readme() -> str:
    """Read README.md for the long description."""
    path = Path(__file__).parent / "README.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return (
        "AetherGovern v2.0.0: Reference implementation of the "
        "falsification-first governance architecture."
    )


def _find_dist_files() -> list[Path]:
    """Find built wheel and sdist files in dist/."""
    if not DIST_DIR.exists():
        return []
    files: list[Path] = []
    for pattern in ("*.whl", "*.tar.gz"):
        files.extend(sorted(DIST_DIR.glob(pattern)))
    return files


def _hash_file(path: Path) -> tuple[str, str]:
    """Return (md5, sha256) hex digests of a file."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            md5.update(chunk)
            sha256.update(chunk)
    return md5.hexdigest(), sha256.hexdigest()


def _build_metadata(readme: str) -> list[tuple[str, str]]:
    """Build the metadata fields for the upload."""
    fields: list[tuple[str, str]] = [
        (":action", "file_upload"),
        ("metadata_version", "2.1"),
        ("name", PACKAGE_NAME),
        ("version", VERSION),
        ("description", readme),
        ("description_content_type", "text/markdown"),
        ("author", "Samir Baladi"),
        ("author_email", "gitdeeper@gmail.com"),
        ("license", "MIT"),
        ("summary", (
            "AetherGovern v2.0.0: Reference implementation of the "
            "falsification-first governance architecture"
        )),
        ("requires_python", ">=3.9"),
        ("requires_dist", "cryptography (>=41.0)"),
        ("keywords", (
            "governance, authorization, policy, accountability, revocation, "
            "dispute resolution, multi-agent systems, falsification, "
            "decentralized systems, aether family"
        )),
        ("project_urls", (
            f"Homepage, https://aethergovern.netlify.app\n"
            f"Repository, https://github.com/gitdeeper15/aethergovern\n"
            f"Bug Tracker, https://github.com/gitdeeper15/aethergovern/issues\n"
            f"Research Paper, https://doi.org/{ZENODO_DOI}\n"
            f"Zenodo, https://doi.org/{ZENODO_DOI}\n"
            f"OSF, https://doi.org/{OSF_DOI}\n"
            f"ORCID, {ORCID_URL}"
        )),
    ]
    for c in CLASSIFIERS:
        fields.append(("classifiers", c))
    return fields


# =============================================================================
# Upload
# =============================================================================

def _upload_file(
    filepath: Path,
    metadata: list[tuple[str, str]],
    token: str,
    repository: str,
) -> bool:
    """Upload a single file. Returns True on success."""
    filename = filepath.name

    if filename.endswith(".tar.gz"):
        filetype = "sdist"
        pyversion = "source"
    elif filename.endswith(".whl"):
        filetype = "bdist_wheel"
        pyversion = "py3"
    else:
        print(f"   ⚠️  Skipping unknown file type: {filename}")
        return False

    md5_hex, sha256_hex = _hash_file(filepath)
    fields = list(metadata) + [
        ("filetype", filetype),
        ("pyversion", pyversion),
        ("md5_digest", md5_hex),
        ("sha256_digest", sha256_hex),
    ]

    print(f"\n   Uploading: {filename}")
    print(f"      type:    {filetype}")
    print(f"      md5:     {md5_hex}")
    print(f"      sha256:  {sha256_hex[:16]}...")

    url = UPLOAD_URLS[repository]
    try:
        with open(filepath, "rb") as f:
            response = requests.post(
                url,
                files={"content": (filename, f, "application/octet-stream")},
                data=fields,
                auth=("__token__", token),
                timeout=120,
                headers={"User-Agent": f"{PACKAGE_NAME}-uploader/{VERSION}"},
            )
    except requests.RequestException as e:
        print(f"      ❌ Request failed: {e}")
        return False

    print(f"      status:  {response.status_code}")

    if response.status_code == 200:
        print(f"      ✅ SUCCESS")
        return True
    if response.status_code == 400 and "already exists" in response.text.lower():
        print(f"      ⚠️  Already exists on {repository} (skipped)")
        return True
    print(f"      ❌ Error: {response.text[:400]}")
    return False


# =============================================================================
# Main
# =============================================================================

def main() -> int:
    print("=" * 70)
    print(f"  {PACKAGE_NAME} v{VERSION} — PyPI Upload")
    print("=" * 70)

    # --- Read environment ---
    token = os.environ.get("PYPI_TOKEN", "").strip()
    if not token:
        print("\n❌ PYPI_TOKEN is not set.")
        print("   Run: export PYPI_TOKEN='pypi-...'")
        print("\n   To get a token: https://pypi.org/manage/account/token/")
        return 1

    repository = os.environ.get("PYPI_REPOSITORY", "pypi").strip().lower()
    if repository not in UPLOAD_URLS:
        print(f"\n❌ Unknown repository: {repository}")
        print(f"   Valid values: {list(UPLOAD_URLS.keys())}")
        return 1

    print(f"\n  Target repository: {repository}")
    print(f"  Upload URL:        {UPLOAD_URLS[repository]}")

    # --- Find dist files ---
    files = _find_dist_files()
    if not files:
        print("\n❌ No distribution files found in dist/.")
        print("   Build first: python -m build")
        return 1

    print(f"\n  Found {len(files)} file(s):")
    for f in files:
        print(f"    • {f.name} ({f.stat().st_size:,} bytes)")

    # --- Read README ---
    readme = _read_readme()
    print(f"\n  README: {len(readme):,} characters")

    # --- Build metadata ---
    metadata = _build_metadata(readme)

    # --- Confirm (unless --yes) ---
    if "--yes" not in sys.argv:
        print(f"\n  ⚠️  About to upload to {repository}. Continue? [y/N] ", end="")
        answer = input().strip().lower()
        if answer not in ("y", "yes"):
            print("  Aborted.")
            return 0

    # --- Upload each file ---
    print("\n" + "=" * 70)
    success_count = 0
    for f in files:
        if _upload_file(f, metadata, token, repository):
            success_count += 1

    # --- Summary ---
    print("\n" + "=" * 70)
    if success_count == len(files):
        print(f"  ✅ All {success_count} file(s) uploaded successfully")
        if repository == "pypi":
            print(f"     https://pypi.org/project/{PACKAGE_NAME}/{VERSION}/")
        else:
            print(f"     https://test.pypi.org/project/{PACKAGE_NAME}/{VERSION}/")
        print("=" * 70)
        return 0
    else:
        print(f"  ❌ {success_count}/{len(files)} file(s) uploaded")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
