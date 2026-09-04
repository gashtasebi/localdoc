# LocalDoc Privacy Architecture

## 1. Purpose

This document defines the privacy-by-design architecture of LocalDoc.

LocalDoc is designed as an offline, local-first document AI application.

The primary privacy objective is:

> User documents and document-derived data remain on the customer's device during normal operation.

This document is an engineering specification and does not constitute legal advice.

---

## 2. Privacy-by-Design Principles

LocalDoc follows these principles:

1. Local processing by default.
2. No cloud processing during normal operation.
3. No telemetry by default.
4. No analytics by default.
5. No automatic upload of documents.
6. No automatic upload of extracted text.
7. No automatic upload of embeddings.
8. No automatic upload of questions or answers.
9. No automatic model downloads during normal operation.
10. Minimize stored personal data.
11. Avoid unnecessary document duplication.
12. Avoid storing document contents in logs.
13. Make external network communication explicit.
14. Keep customer-controlled data under customer control.

---

## 3. Data Flow

The intended normal processing flow is:

PDF
  |
  v
Local PDF Processing
  |
  v
Extracted Text
  |
  v
Chunking
  |
  v
Embeddings
  |
  v
Local Storage
  |
  v
Local Retrieval
  |
  v
Local LLM
  |
  v
Answer

All stages are intended to execute locally on the customer's machine.

---

## 4. Document Data

### 4.1 Source Documents

Customer PDF files are treated as user-controlled data.

LocalDoc must not transmit source documents to an external service during normal offline operation.

### 4.2 Extracted Text

Extracted document text may contain:

- personal data
- confidential information
- business information
- financial information
- legal information
- proprietary information

Therefore extracted text must be treated with the same privacy sensitivity as the original document.

### 4.3 Chunks

Document chunks are derived from customer documents.

Chunks must be considered customer data and must not be transmitted externally during normal operation.

---

## 5. Embeddings

Embeddings are derived from customer document content.

Although embeddings are not human-readable document text, they may encode information derived from the original document.

Therefore:

- embeddings are treated as customer-derived data;
- embeddings must remain local during normal operation;
- embeddings must not be transmitted to third-party APIs;
- embeddings must not be included in diagnostic logs;
- embeddings must not be uploaded automatically.

---

## 6. Questions and Answers

User questions may themselves contain sensitive information.

LocalDoc must therefore treat:

- user questions
- retrieved context
- generated answers

as potentially sensitive local data.

These values must remain local during normal operation.

---

## 7. Local LLM

The LLM used by LocalDoc is intended to run locally.

The application must not send document content, questions, retrieved context, or generated answers to a remote LLM API during normal offline operation.

The final commercial architecture must not depend on an Internet connection for ordinary document processing and question answering.

---

## 8. Network Communication

### 8.1 Normal Operation

Normal LocalDoc operation should require no Internet connection.

The application must not silently perform network communication.

### 8.2 Explicit Network Operations

If a future version requires network communication for a specific function, that communication must be:

- explicit;
- documented;
- necessary for the feature;
- separated from normal offline document processing;
- designed so that customer document content is not transmitted unnecessarily.

### 8.3 Automatic Downloads

The final commercial application must not automatically download:

- models;
- documents;
- plugins;
- executable code;
- dependencies

during normal operation.

---

## 9. Telemetry and Analytics

LocalDoc is designed without mandatory telemetry.

The application should not automatically collect:

- document contents;
- extracted text;
- document chunks;
- embeddings;
- questions;
- answers;
- file contents;
- customer usage data

for analytics or product monitoring.

If optional diagnostics are introduced in the future, they must be designed separately from document processing.

---

## 10. Logging

Logs are required for diagnostics and troubleshooting.

However logs must not contain document contents or sensitive document-derived data by default.

### Logs should contain technical information such as:

- application version;
- operating system information;
- component name;
- operation status;
- error category;
- exception type;
- processing duration;
- document identifier where technically necessary.

### Logs should not contain:

- full PDF contents;
- extracted document text;
- complete chunks;
- embeddings;
- complete user questions;
- generated answers;
- authentication secrets;
- license private keys.

Error messages must also be reviewed to prevent accidental disclosure of sensitive data.

---

## 11. Database

LocalDoc currently uses SQLite for local storage.

The database may contain:

- document metadata;
- document identifiers;
- file paths;
- file hashes;
- chunks;
- embeddings.

These values must be treated as local customer data.

The database must remain local to the customer's device during normal operation.

Future implementation should minimize unnecessary duplication of document content.

---

## 12. File Paths

File paths may reveal information about:

- user names;
- usernames;
- directory structures;
- organization names;
- project names.

Therefore file paths should not be unnecessarily exposed in logs, diagnostics, or exported reports.

---

## 13. File Hashes

LocalDoc uses SHA-256 file hashes for document identification and duplicate detection.

A hash is derived from the source file and should therefore be treated as document-related metadata.

Hashes must not be treated as automatically anonymous data.

---

## 14. Temporary Files

Temporary processing files should be minimized.

If temporary files are required:

1. They must be created locally.
2. They must have a defined lifecycle.
3. They should be deleted when no longer required.
4. They must not be uploaded automatically.
5. They must not be included in logs.

---

## 15. Data Deletion

The application must provide a reliable mechanism to delete locally stored document data.

Deletion should cover, where applicable:

- document metadata;
- chunks;
- embeddings;
- derived indexes;
- temporary processing data.

The implementation must be reviewed to ensure that deleting a document from the application does not leave unnecessary application-managed copies behind.

---

## 16. Backup Considerations

LocalDoc does not control the customer's operating-system backup system.

Customers may use:

- Time Machine;
- enterprise backup systems;
- disk snapshots;
- cloud backup services;
- other system-level backup solutions.

Therefore the product documentation should clearly distinguish:

> LocalDoc does not transmit the document to the cloud

from:

> The customer's operating system or backup software may independently copy LocalDoc data.

---

## 17. Access Control

LocalDoc should rely on the customer's operating-system account and filesystem permissions for basic local access control.

Future commercial versions may add application-level protection where required.

Sensitive local data should not be made world-readable through application-created files.

---

## 18. Security Boundary

The LocalDoc privacy architecture assumes that the customer's operating system and device are trusted at the operating-system security level.

LocalDoc does not claim to protect documents from:

- malware already controlling the machine;
- an attacker with full operating-system privileges;
- physical compromise of an unlocked device;
- malicious administrators with sufficient system privileges.

These limitations must be reflected in security documentation and product claims.

---

## 19. Privacy-Sensitive Components

The following components are considered privacy-sensitive:

| Component | Data handled | Privacy sensitivity |
|---|---|---|
| PDF processor | Source PDF / extracted text | High |
| Chunker | Document text | High |
| Embedder | Document text / embeddings | High |
| Retriever | Query / embeddings / chunks | High |
| QA | Question / context / answer | High |
| SQLite database | Metadata / chunks / embeddings | High |
| Logs | Technical diagnostics | Medium |
| File hash | Derived document identifier | Medium |
| Local LLM | Context / questions | High |

---

## 20. Privacy Requirements for Future Features

Before adding a feature that handles customer data, evaluate:

1. What data does the feature access?
2. Is the data necessary?
3. Is the data stored?
4. Where is it stored?
5. Is it transmitted?
6. Is transmission necessary?
7. Can the feature operate completely locally?
8. Could logs expose the data?
9. Could temporary files expose the data?
10. Does the feature introduce a new third-party dependency?
11. Does the dependency introduce a new license requirement?
12. Does the feature change the privacy or security boundary?

A feature that introduces external processing must receive an explicit privacy and security review before implementation.

---

## 21. Commercial Release Requirements

Before commercial release, verify:

- normal operation works offline;
- no unintended external network calls occur;
- document contents remain local;
- embeddings remain local;
- questions and answers remain local;
- telemetry is disabled by default;
- logs do not contain document contents;
- temporary files are controlled;
- deletion behavior is tested;
- third-party components are reviewed;
- privacy documentation matches actual behavior.

---

## 22. Engineering Verification

Privacy claims must be verified technically.

The project should eventually include tests and/or release checks for:

- network independence;
- absence of unexpected external API calls;
- log redaction;
- deletion behavior;
- temporary-file cleanup;
- local database behavior.

Privacy documentation must not claim behavior that has not been verified.

---

## 23. Change Management

Any feature that changes:

- data storage;
- network communication;
- logging;
- model execution;
- document processing;
- database structure;
- third-party dependencies

must trigger a review of this document.

---

## 24. Current Status

Current architecture:

- PDF processing: local
- Text extraction: local
- Chunking: local
- Embedding: local
- Retrieval: local
- SQLite storage: local
- QA: local
- LLM integration: local
- Mandatory telemetry: none planned
- Cloud document processing: not part of normal operation

This document describes the intended privacy architecture.

Actual implementation and commercial release claims must be verified against the final product.

---

## 25. Review History

### Initial Review

Status:
- Privacy-by-design architecture defined.
- Local processing principle established.
- Sensitive data categories identified.
- Logging requirements defined.
- Network communication requirements defined.
- Commercial release verification requirements defined.

---

## 26. Next Review

Review this document whenever a feature introduces:

- a new external service;
- a new network connection;
- a new database;
- a new logging mechanism;
- a new model;
- a new dependency;
- a new data export mechanism.
