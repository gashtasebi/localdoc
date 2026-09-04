# LocalDoc Security Requirements

## 1. Purpose

This document defines the security requirements for LocalDoc.

LocalDoc is designed as an offline, local-first document AI application.

The security architecture must protect:

- customer documents;
- extracted text;
- chunks;
- embeddings;
- local databases;
- local models;
- application configuration;
- logs;
- licenses and licensing data.

This document is an engineering specification and does not constitute legal advice.

---

## 2. Security Principles

LocalDoc follows these principles:

1. Local processing by default.
2. Least privilege.
3. Minimal data exposure.
4. No unnecessary network communication.
5. No secrets in source code.
6. No document content in logs.
7. Explicit handling of temporary files.
8. Integrity verification for distributed components.
9. Secure deletion where technically appropriate.
10. Security-sensitive changes require review.

---

## 3. Security Boundaries

The primary security boundary is the customer's operating system.

LocalDoc assumes that the operating system provides:

- user authentication;
- filesystem permissions;
- process isolation;
- basic device security.

LocalDoc does not claim to protect data from an attacker who already has full control of the operating system.

---

## 4. Document Security

Customer documents must be treated as untrusted input.

PDF files may contain:

- malformed structures;
- unexpected content;
- malicious content;
- extremely large files;
- unusual encodings;
- embedded objects.

The PDF processing layer must therefore avoid trusting document content as executable instructions.

---

## 5. PDF Processing

PDF processing must:

- operate locally;
- avoid unnecessary network access;
- validate input paths;
- handle malformed PDFs safely;
- handle processing errors gracefully;
- avoid crashing the complete application because of one invalid document;
- avoid writing extracted content to logs.

Third-party PDF processing dependencies must be reviewed for security and licensing implications.

---

## 6. Path Handling

File paths supplied by users must be treated as untrusted input.

The application should avoid:

- unintended path traversal;
- accidental writes outside intended directories;
- overwriting unrelated files;
- following unexpected symbolic links where security-sensitive;
- exposing sensitive paths unnecessarily.

Any future import/export functionality must define an explicit filesystem boundary.

---

## 7. Database Security

LocalDoc currently uses SQLite.

The database may contain sensitive customer-derived information.

Security requirements:

- database files remain local;
- database paths must be controlled;
- SQL queries must use parameterized values where applicable;
- arbitrary SQL must never be accepted from normal users;
- database errors must not expose unnecessary sensitive information;
- database backups must be considered customer-controlled data.

---

## 8. Embedding Security

Embeddings are derived from customer documents.

They must be treated as sensitive derived data.

Requirements:

- embeddings remain local;
- embeddings are not transmitted to external APIs;
- embeddings are not written to logs;
- embeddings are not exposed through diagnostics;
- embeddings are deleted when the associated document is deleted, subject to documented storage behavior.

---

## 9. LLM Security

The local LLM must receive only the data required for the requested operation.

The application must not expose:

- filesystem secrets;
- license secrets;
- private keys;
- environment secrets

to the model unnecessarily.

The model must not be treated as a trusted application component with unrestricted system access.

---

## 10. Prompt Injection

Document content is untrusted input.

A malicious or specially crafted document may contain instructions intended to manipulate the LLM.

The application should maintain a clear separation between:

- system instructions;
- application instructions;
- document content;
- user questions.

Document text must not automatically become trusted instructions.

Future security testing should include prompt-injection test cases.

---

## 11. Network Security

Normal LocalDoc document processing should work without Internet access.

The application must not silently:

- upload documents;
- upload extracted text;
- upload chunks;
- upload embeddings;
- upload questions;
- upload answers;
- download models;
- download executable code.

Any future network functionality must be explicitly documented and reviewed.

---

## 12. Secrets Management

Secrets must never be committed to Git.

This includes:

- API keys;
- private signing keys;
- passwords;
- access tokens;
- license secrets;
- certificates containing private material.

Secrets must not be embedded directly in source code.

Development secrets must not be included in the public GitHub repository.

---

## 13. License Security

Future offline licensing may use:

- signed license files;
- device binding;
- digital signatures;
- public-key verification.

Private signing keys must never be included in the application source code or distributed with the application.

The application should contain only the information required to verify a license.

---

## 14. Code Integrity

Commercial builds should be reproducible or at minimum traceable to a known source revision.

Release records should identify:

- source commit;
- application version;
- dependency versions;
- model versions;
- build environment where appropriate;
- release artifacts.

Distributed files should be integrity-checked before release.

---

## 15. Dependency Security

Third-party dependencies must be reviewed before commercial release.

Security review should consider:

- dependency source;
- version;
- known vulnerabilities;
- license;
- whether the dependency is actually required at runtime;
- whether it is bundled into the final product.

Unnecessary dependencies should not be included in the commercial distribution.

---

## 16. Dependency Updates

Dependencies must not be updated blindly.

For each important dependency update:

1. Record the new version.
2. Review release information.
3. Review license changes.
4. Run the test suite.
5. Run relevant security checks.
6. Verify application behavior.
7. Update dependency documentation.

---

## 17. Logging Security

Logs must be designed for diagnostics without exposing customer data.

Logs must not contain:

- document contents;
- complete extracted text;
- complete chunks;
- embeddings;
- complete prompts;
- complete answers;
- passwords;
- API keys;
- private keys;
- license secrets.

Errors should be sanitized before being written to logs.

---

## 18. Error Handling

The application should fail safely.

Requirements:

- expected processing errors should be handled;
- sensitive information should not be included in error messages;
- corrupted documents should not corrupt unrelated database records;
- failed imports should not leave inconsistent database state;
- partial operations should be detectable and recoverable.

---

## 19. Temporary Data

Temporary files and intermediate data must be minimized.

Where temporary files are required:

- create them in controlled locations;
- use unique names;
- avoid predictable filenames;
- delete them after use;
- avoid storing sensitive content longer than necessary.

---

## 20. File Deletion

When a document is deleted through LocalDoc, application-managed derived data should also be removed where applicable.

Deletion should cover:

- document metadata;
- chunks;
- embeddings;
- indexes;
- temporary application-managed copies.

The implementation must be tested.

Note:

Secure destruction of data from physical storage is dependent on the storage technology and operating system and must not be overstated.

---

## 21. Access Control

LocalDoc should rely on operating-system permissions for basic local access control.

Application-created files should use appropriate permissions and must not unnecessarily become readable or writable by unrelated users.

---

## 22. Multi-User Considerations

If future versions support multiple operating-system users on the same machine, the data isolation model must be reviewed.

The application must not assume that all local users are authorized to access the same documents.

Document ownership and filesystem permissions must be explicitly defined before multi-user support is introduced.

---

## 23. Model Supply Chain

Model files are part of the application supply chain.

Before commercial distribution, verify:

- model source;
- model version;
- model integrity;
- model license;
- commercial-use rights;
- redistribution rights;
- expected file format;
- compatibility with the selected runtime.

Models must not be downloaded automatically from untrusted sources.

---

## 24. Build Security

The build environment should be separated from customer data.

Production builds must not accidentally contain:

- test documents;
- personal documents;
- development secrets;
- local databases;
- debug logs;
- credentials;
- private signing keys.

The local test PDF must never be included in the public repository or commercial release.

---

## 25. Git Security

Before every public push or release, verify that Git does not contain:

- secrets;
- private keys;
- customer documents;
- local databases;
- temporary files;
- model files that are not intended for distribution;
- build artifacts that should remain local.

The repository should maintain an appropriate `.gitignore`.

---

## 26. GitHub Security

The public repository should contain only information intended for public disclosure.

Potentially sensitive information includes:

- internal credentials;
- customer information;
- private infrastructure details;
- private signing keys;
- internal license material;
- proprietary test documents.

Public documentation must not expose confidential commercial information unnecessarily.

---

## 27. Security Testing

Future security testing should include:

### Input testing

- malformed PDFs;
- empty PDFs;
- very large PDFs;
- unusual filenames;
- unusual Unicode filenames;
- invalid paths.

### Database testing

- duplicate imports;
- failed writes;
- interrupted operations;
- deletion consistency.

### Network testing

- offline operation;
- unexpected network connections;
- model download attempts;
- external API attempts.

### AI security testing

- prompt injection;
- malicious document instructions;
- context boundary violations;
- source attribution failures.

### Logging testing

- sensitive text leakage;
- prompt leakage;
- answer leakage;
- path leakage;
- secret leakage.

---

## 28. Vulnerability Management

Security vulnerabilities discovered in LocalDoc or its dependencies should be tracked.

Each vulnerability should be evaluated for:

- affected component;
- affected versions;
- exploitability;
- impact;
- available mitigation;
- required update;
- release urgency.

Critical security issues must receive priority over non-essential feature development.

---

## 29. Security Incident Handling

A future commercial release should define a process for handling:

- security vulnerabilities;
- unauthorized network communication;
- data exposure;
- malicious documents;
- compromised dependencies;
- compromised release artifacts;
- license key compromise.

Incident handling must minimize unnecessary collection of customer data.

---

## 30. Security Documentation

Security claims in product documentation must reflect tested behavior.

The product must not claim:

- absolute security;
- complete protection from malware;
- protection against a fully compromised operating system;
- guaranteed protection against every malicious PDF;
- guaranteed elimination of AI security risks.

---

## 31. Commercial Release Security Gate

Before commercial release, verify:

- no secrets are present in the repository;
- customer/test documents are excluded;
- `.gitignore` is correct;
- runtime dependencies are reviewed;
- dependencies are checked for known security issues;
- models are verified;
- network behavior is tested;
- logs are reviewed;
- deletion behavior is tested;
- database operations are tested;
- release artifacts are integrity-checked;
- signing infrastructure is secured;
- security documentation matches implementation.

---

## 32. Current Security Status

Current architecture:

- local document processing: implemented;
- local embeddings: implemented;
- local retrieval: implemented;
- local database: implemented;
- local LLM integration: implemented;
- normal cloud processing: not required;
- telemetry: not planned;
- secret-management architecture: partially defined;
- offline license security: planned;
- model supply-chain review: pending;
- network security testing: pending;
- prompt-injection testing: pending;
- formal vulnerability management process: pending.

---

## 33. Review History

### Initial Security Review

Completed:

- security boundaries defined;
- document security requirements defined;
- network requirements defined;
- logging requirements defined;
- dependency security requirements defined;
- model supply-chain requirements defined;
- Git/GitHub security requirements defined;
- commercial release security gate defined.

---

## 34. Next Review

Review this document whenever a feature changes:

- filesystem access;
- document processing;
- database behavior;
- network behavior;
- model execution;
- authentication;
- licensing;
- packaging;
- dependencies;
- logging.
