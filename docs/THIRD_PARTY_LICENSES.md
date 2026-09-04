# LocalDoc Third-Party License Inventory

> **Internal engineering and compliance tracking document.**
>
> This document records third-party software and AI components currently
> identified in the LocalDoc development environment.
>
> It is not legal advice and is not the final legal notice for commercial
> distribution.
>
> License information must be verified against the exact package, model,
> version, revision, and distribution method used in the final release.

---

## 1. Purpose

LocalDoc is being developed as a commercial offline desktop application.

Because LocalDoc uses third-party software libraries, frameworks, runtimes,
and AI models, their licenses and redistribution conditions must be reviewed
before commercial distribution.

This document provides an engineering inventory of the currently identified
components and records the status of their commercial review.

The inventory distinguishes between:

* Direct runtime dependencies
* Transitive runtime dependencies
* Development-only dependencies
* AI models
* Build and packaging tools

A package being installed in the development environment does **not**
automatically mean that it will be included in the final commercial
application.

---

## 2. Direct Runtime Dependencies

The current LocalDoc source code directly imports the following external
packages.

| Component             | Current Version | License Status                         | Commercial Status                          | Action                                  |
| --------------------- | --------------: | -------------------------------------- | ------------------------------------------ | --------------------------------------- |
| PyMuPDF (`pymupdf`)   |          1.28.2 | AGPL-3.0 OR Artifex Commercial License | **Review required**                        | Resolve before commercial release       |
| sentence-transformers |           6.0.1 | Apache-2.0                             | **Review required for final distribution** | Verify exact package/model distribution |

### 2.1 PyMuPDF

PyMuPDF is currently used for PDF processing.

Current version:

```text
PyMuPDF 1.28.2
```

Current licensing information identified during the project review:

```text
GNU Affero General Public License 3.0
OR
Artifex Commercial License
```

Status:

```text
COMMERCIAL RELEASE BLOCKER
```

The project must not assume that PyMuPDF can simply be bundled into a
proprietary commercial desktop application without determining the
applicable licensing path.

Before commercial distribution, LocalDoc must formally select and review
one of the applicable paths:

1. Use PyMuPDF under the applicable AGPL terms and comply with all resulting
   obligations; or

2. Obtain an appropriate commercial license from Artifex.

No final commercial release should be marked READY while this decision
remains unresolved.

---

### 2.2 sentence-transformers

Current version:

```text
sentence-transformers 6.0.1
```

The package is currently used by LocalDoc to generate document and query
embeddings.

Current package license identified during the dependency review:

```text
Apache-2.0
```

The software library license and the license of the embedding model are
separate matters.

The current embedding model is tracked in Section 5.

Before commercial distribution, verify:

* Exact package version
* Exact package distribution included in the installer
* Applicable license and notices
* Transitive dependencies
* Exact embedding model
* Model license
* Model redistribution rights
* Commercial-use permission
* Required attribution

---

## 3. Transitive Runtime Dependencies

The current dependency tree contains additional packages required by the
runtime dependency chain.

These packages are not necessarily imported directly by LocalDoc source
code, but may be required by packages such as `sentence-transformers`.

The current environment includes, among others:

| Component         | Current Version | Identified License                            | Status          |
| ----------------- | --------------: | --------------------------------------------- | --------------- |
| torch             |          2.13.0 | Apache-2.0 and additional component licenses  | Review required |
| transformers      |          5.16.1 | Apache-2.0                                    | Review required |
| tokenizers        |          0.23.1 | Apache-2.0                                    | Review required |
| numpy             |           2.5.2 | Multiple licenses                             | Review required |
| scipy             |          1.18.1 | Multiple licenses/components                  | Review required |
| scikit-learn      |           1.9.0 | BSD-3-Clause                                  | Review required |
| joblib            |           1.6.0 | BSD-3-Clause                                  | Review required |
| threadpoolctl     |           3.6.0 | BSD-3-Clause                                  | Review required |
| huggingface-hub   |          1.29.0 | Apache-2.0                                    | Review required |
| filelock          |          3.32.5 | MIT                                           | Review required |
| fsspec            |        2026.7.0 | BSD-3-Clause                                  | Review required |
| PyYAML            |           6.0.3 | MIT                                           | Review required |
| regex             |        2026.9.3 | Apache-2.0 AND CNRI-Python                    | Review required |
| safetensors       |           0.8.0 | Apache-2.0 / Apache Software License metadata | Review required |
| tqdm              |          4.70.0 | MPL-2.0 AND MIT                               | Review required |
| packaging         |            26.3 | Apache-2.0 OR BSD-2-Clause                    | Review required |
| Jinja2            |           3.1.6 | BSD License metadata                          | Review required |
| MarkupSafe        |           3.0.3 | BSD-3-Clause                                  | Review required |
| networkx          |           3.6.1 | BSD-3-Clause                                  | Review required |
| sympy             |          1.14.0 | BSD                                           | Review required |
| mpmath            |           1.3.0 | BSD-style                                     | Review required |
| typing-extensions |          4.16.0 | PSF-2.0                                       | Review required |
| click             |           8.5.0 | BSD-3-Clause                                  | Review required |
| typer             |          0.27.2 | MIT                                           | Review required |
| rich              |          15.0.0 | MIT                                           | Review required |
| markdown-it-py    |           4.2.0 | MIT License metadata                          | Review required |
| mdurl             |           0.1.2 | MIT License metadata                          | Review required |
| Pygments          |          2.21.0 | BSD-2-Clause                                  | Review required |
| shellingham       |           1.5.4 | ISC                                           | Review required |
| annotated-doc     |           0.0.5 | MIT                                           | Review required |
| anyio             |          4.14.2 | MIT                                           | Review required |
| certifi           |       2026.7.22 | MPL-2.0                                       | Review required |
| cloudpickle       |           3.1.2 | BSD-3-Clause                                  | Review required |
| h11               |          0.16.0 | MIT                                           | Review required |
| httpcore          |           1.0.9 | BSD-3-Clause                                  | Review required |
| httpx             |          0.28.1 | BSD-3-Clause                                  | Review required |
| idna              |            3.19 | BSD-3-Clause                                  | Review required |
| hf-xet            |           1.6.0 | Apache-2.0                                    | Review required |
| narwhals          |          2.25.0 | MIT                                           | Review required |

### Important

This table is an engineering inventory, not a declaration that every listed
package will be bundled into the final product.

The final commercial dependency set must be generated from the actual
packaging/build configuration.

Before release, the final bundle must be scanned and compared against this
inventory.

---

## 4. Development and Build Dependencies

The development environment also contains packages that are used for testing,
packaging, dependency management, or development infrastructure.

These should not automatically be included in the final LocalDoc runtime.

Examples identified during the dependency review include:

| Component       |         Current Version | Purpose                            | Final Runtime     |
| --------------- | ----------------------: | ---------------------------------- | ----------------- |
| pytest          |                   9.1.1 | Automated testing                  | No                |
| pip             |                  26.2.1 | Python package management          | No                |
| pipdeptree      |                   4.2.3 | Dependency analysis                | No                |
| setuptools      |                  84.0.0 | Build infrastructure               | Not automatically |
| build           | Development environment | Package building                   | No                |
| installer       | Development environment | Package installation/build support | No                |
| pyproject_hooks | Development environment | Build infrastructure               | No                |

The final packaging configuration must explicitly distinguish runtime
dependencies from development-only dependencies.

---

## 5. AI Models

AI models are tracked separately from software libraries.

A model's license is independent from the license of the Python library used
to load or execute that model.

### 5.1 Embedding Model

Current model:

```text
all-MiniLM-L6-v2
```

Current use:

```text
Document and query embeddings
```

Status:

```text
REVIEW REQUIRED
```

Before commercial distribution, record and verify:

* Exact model identifier
* Exact model revision/version
* Model license
* Copyright/authorship information
* Model source
* Redistribution permission
* Commercial-use permission
* Required attribution
* Acceptable-use restrictions
* Whether the model is bundled with LocalDoc
* Whether the model is downloaded during installation
* Whether the model is modified
* Model checksum or immutable revision where practical

The license of `sentence-transformers` must not be treated as the license of
the model itself.

---

## 6. Local LLM Runtime

LocalDoc currently uses a local LLM runtime.

Current runtime:

```text
Ollama
```

Status:

```text
REVIEW REQUIRED
```

The software runtime and the model executed by that runtime must be reviewed
separately.

Before commercial distribution, record:

* Exact Ollama version
* Ollama license
* Exact LLM model name
* Exact model version or digest
* Model license
* Commercial-use permission
* Redistribution requirements
* Attribution requirements
* Acceptable-use restrictions
* Whether the runtime is bundled
* Whether the model is bundled
* Whether the model is downloaded separately
* Whether redistribution with LocalDoc is permitted

LocalDoc must not assume that a model available through a local runtime is
automatically licensed for commercial redistribution.

---

## 7. Python Standard Library

The following components are part of Python's standard library and are not
third-party LocalDoc dependencies:

```text
argparse
dataclasses
hashlib
json
math
pathlib
re
sqlite3
urllib
```

They are currently used by LocalDoc for:

* Command-line argument handling
* Data models
* File hashing
* JSON processing
* Mathematical calculations
* File-system operations
* Regular expressions
* SQLite database access
* HTTP communication with the local LLM runtime

No separate third-party package license inventory is required for these
standard-library modules.

The Python runtime itself must nevertheless be considered in the final
distribution and packaging review.

---

## 8. LocalDoc Internal Modules

The following imports are part of the LocalDoc source code and are not
third-party dependencies:

```text
src
pdf_parser
```

They are maintained as part of the LocalDoc project.

---

## 9. Offline Distribution Requirements

The final commercial version of LocalDoc is intended to operate offline
during normal customer use.

The final product should therefore be designed so that:

* No automatic dependency downloads occur during normal runtime.
* No automatic model downloads occur during normal runtime.
* No hidden cloud API calls occur.
* No telemetry is enabled without an explicitly designed and documented
  mechanism.
* Customer documents remain local.
* Customer document contents are not sent to external services.
* All bundled third-party software is inventoried.
* All bundled AI models are inventoried.
* Required license and attribution notices are included.
* The final installer contents are documented.
* The production build process is reproducible and documented.

Offline operation does not remove the need to comply with third-party licenses
or applicable law.

---

## 10. Third-Party License Review Rules

For every dependency included in the commercial application:

1. Record the exact version.
2. Record the applicable license.
3. Record the copyright holder where required.
4. Verify whether commercial use is permitted.
5. Verify redistribution requirements.
6. Verify attribution requirements.
7. Verify notice requirements.
8. Verify whether source-code distribution obligations apply.
9. Verify whether the dependency is bundled into the installer.
10. Preserve applicable license and notice information.
11. Record the source from which the licensing information was verified.
12. Re-check the information when upgrading the dependency.

---

## 11. AI Model Review Rules

For every AI model distributed with LocalDoc:

1. Record the exact model identifier.
2. Record the exact revision/version.
3. Record the model license.
4. Verify commercial use.
5. Verify redistribution rights.
6. Verify attribution requirements.
7. Verify acceptable-use restrictions.
8. Verify whether derivative or modified models are permitted.
9. Record the model source.
10. Record the model checksum or immutable revision where practical.
11. Record whether the model is bundled or downloaded separately.
12. Re-check the license whenever the model revision changes.

---

## 12. Automated Inventory

LocalDoc contains internal tooling to reduce manual dependency tracking.

Current tools:

```text
tools/direct_imports.py
tools/license_inventory.py
tools/runtime_dependencies.py
```

### `direct_imports.py`

Identifies Python modules directly imported by the LocalDoc source tree.

### `license_inventory.py`

Reads installed package metadata and reports available license information.

The inventory uses package metadata where available, including:

1. `License-Expression`
2. `License`
3. `License ::` classifiers

If reliable license metadata cannot be identified, the package must remain
subject to manual review.

### `runtime_dependencies.py`

Records the versions of the currently identified direct runtime dependencies.

Current direct runtime dependencies:

```text
pymupdf==1.28.2
sentence-transformers==6.0.1
```

These tools support the compliance process but do not replace manual legal
review.

---

## 13. Dependency Changes

Whenever a dependency is:

* Added
* Removed
* Upgraded
* Downgraded
* Replaced
* Bundled differently

the following should be reviewed:

1. Direct imports
2. Transitive dependency tree
3. Package license
4. Model license, if applicable
5. Redistribution conditions
6. Commercial-use conditions
7. Final bundle contents
8. Third-party notices

Dependency upgrades should therefore be treated as both engineering and
compliance changes.

---

## 14. Critical Commercial Release Blockers

The following items are currently considered release blockers until reviewed
and resolved.

### 14.1 PyMuPDF

```text
STATUS: BLOCKER
```

The applicable PyMuPDF licensing path must be resolved before commercial
distribution.

### 14.2 Embedding Model

```text
STATUS: REVIEW REQUIRED
```

The exact license and redistribution/commercial-use conditions of
`all-MiniLM-L6-v2` must be verified.

### 14.3 Local LLM Model

```text
STATUS: REVIEW REQUIRED
```

The exact model, version/digest, license, and redistribution rights must be
verified.

### 14.4 Ollama

```text
STATUS: REVIEW REQUIRED
```

The runtime license and final distribution method must be verified.

### 14.5 Transitive Dependencies

```text
STATUS: REVIEW REQUIRED
```

The final bundled dependency tree must be generated and reviewed before
commercial release.

---

## 15. Final Commercial Release Gate

A commercial LocalDoc release must not be marked READY until all applicable
items below are completed:

* [ ] All direct runtime dependencies have been inventoried.
* [ ] All transitive runtime dependencies have been inventoried.
* [ ] Development-only dependencies have been separated.
* [ ] All bundled AI models have been inventoried.
* [ ] Exact model revisions/digests have been recorded where practical.
* [ ] All model licenses have been verified.
* [ ] Commercial model use has been verified.
* [ ] Model redistribution rights have been verified.
* [ ] PyMuPDF licensing has been resolved.
* [ ] Ollama/runtime licensing has been verified.
* [ ] LLM model licensing has been verified.
* [ ] Required copyright notices have been identified.
* [ ] Required attribution notices have been identified.
* [ ] Required third-party licenses have been collected.
* [ ] Final installer contents have been scanned.
* [ ] Final bundled dependency versions have been recorded.
* [ ] Final third-party notices have been prepared.
* [ ] Offline-runtime behavior has been verified.
* [ ] No unintended network communication occurs during normal offline use.
* [ ] The final build process is documented.
* [ ] A final legal/compliance review has been completed where appropriate.

---

## 16. Current Project Status

Current status:

```text
DEVELOPMENT — NOT READY FOR COMMERCIAL DISTRIBUTION
```

Primary known blocker:

```text
PyMuPDF licensing decision
```

Additional review areas:

```text
AI embedding model licensing
Ollama/runtime licensing
LLM model licensing
Complete transitive dependency inventory
Final bundled dependency set
Third-party notices
Final installer review
```

This document is an engineering tracking document and does not constitute
legal advice.

---

## 17. Review History

| Date       | Change                                                 |
| ---------- | ------------------------------------------------------ |
| 2026-09-04 | Dependency and license inventory reviewed and expanded |
| 2026-09-04 | Direct import analysis added                           |
| 2026-09-04 | Runtime dependency identification added                |
| 2026-09-04 | Commercial release gates documented                    |

---

## 18. Next Review

This document must be reviewed whenever:

* A runtime dependency changes.
* An AI model changes.
* The packaging architecture changes.
* The installer/bundle contents change.
* LocalDoc begins commercial distribution.
* A dependency license changes.
* A new external service or runtime is introduced.
* The final production build process is established.

