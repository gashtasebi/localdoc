# LocalDoc AI Compliance

## 1. Purpose

This document defines the engineering requirements and compliance considerations for the AI functionality of LocalDoc.

LocalDoc is an offline document AI application that uses:

- local document processing;
- local embeddings;
- local information retrieval;
- a local large language model (LLM);
- locally generated answers.

This document is an engineering and product-planning document. It is not legal advice.

---

## 2. AI System Description

The current LocalDoc AI pipeline is:

PDF
  |
  v
Text Extraction
  |
  v
Chunking
  |
  v
Embedding
  |
  v
Vector Retrieval
  |
  v
Retrieved Context
  |
  v
Local LLM
  |
  v
Generated Answer

The system is intended to operate locally on the customer's device.

---

## 3. Intended Purpose

The intended purpose of LocalDoc is:

> To help users search and ask questions about documents stored locally on their own device.

LocalDoc is not intended to:

- make autonomous decisions about people;
- determine eligibility for benefits;
- make employment decisions;
- make credit decisions;
- make medical diagnoses;
- make legal decisions;
- perform biometric identification;
- control safety-critical systems.

The product must not be marketed in a way that contradicts this intended purpose without a new compliance review.

---

## 4. Human Oversight

LocalDoc generates answers based on retrieved document content.

Users remain responsible for evaluating generated answers before relying on them for consequential decisions.

The product should make clear that:

- generated answers may be incomplete;
- retrieval may fail;
- the source document may itself contain errors;
- the LLM may generate an incorrect interpretation;
- generated output should not automatically be treated as authoritative.

Where appropriate, the user should be able to inspect the source pages used for an answer.

---

## 5. Grounding and Source Attribution

LocalDoc is designed to use retrieval-augmented generation (RAG).

The intended behavior is:

1. Retrieve relevant document chunks.
2. Provide those chunks as context to the local LLM.
3. Generate an answer using the supplied context.
4. Show the source page numbers associated with retrieved content.

The system should not claim that an answer is supported by a document when no relevant document content was retrieved.

If no relevant chunks are available, LocalDoc should return:

> The answer is not available in the provided document.

This behavior is an important reliability requirement.

---

## 6. Hallucination Control

LocalDoc must minimize unsupported generated content.

Current controls include:

- semantic retrieval;
- similarity thresholding;
- context-only prompting;
- refusal when no relevant context is available;
- source page reporting.

Future improvements may include:

- answer confidence indicators;
- citation-level source mapping;
- retrieval evaluation;
- answer evaluation datasets;
- configurable retrieval thresholds;
- detection of insufficient context.

No feature should imply that hallucination has been completely eliminated.

---

## 7. Model Execution

The intended commercial architecture uses a local LLM.

Normal document question answering should not require:

- OpenAI API;
- remote LLM API;
- cloud embedding API;
- cloud vector database;
- remote document processing service.

The application must not silently switch to a remote model.

---

## 8. AI Model Inventory

Every model distributed with or required by LocalDoc must be recorded.

The inventory should contain:

| Model | Purpose | Source | Version | License | Distribution Status |
|---|---|---|---|---|---|
| all-MiniLM-L6-v2 | Text embeddings | Hugging Face / Sentence Transformers ecosystem | Current project version | Review required | Review required |
| Local LLM | Answer generation | Model-specific source | Project-selected version | Review required | Review required |

Model licenses must be reviewed independently from Python package licenses.

A package being Apache-2.0 licensed does not automatically mean that every model used by that package has the same license.

---

## 9. Model License Requirements

Before commercial distribution of a model, verify:

1. Model license.
2. License version.
3. Commercial-use permission.
4. Redistribution permission.
5. Modification requirements.
6. Attribution requirements.
7. Notice requirements.
8. Restrictions on use.
9. Additional terms.
10. Required model card notices.
11. Source availability requirements, if applicable.
12. Whether model weights may legally be distributed with LocalDoc.

Evidence for the review should be stored in the project's compliance records.

---

## 10. Third-Party AI Services

LocalDoc should avoid mandatory third-party AI services during normal offline operation.

If a future version introduces an optional remote AI service, the feature must receive a new review covering:

- privacy;
- data transfer;
- security;
- contractual terms;
- service availability;
- data retention;
- model provider terms;
- applicable AI regulations;
- user disclosure.

Remote AI processing must never be introduced silently.

---

## 11. AI Output Transparency

Users must be able to understand when content is generated by AI.

The UI should clearly distinguish:

- source document text;
- retrieved context;
- AI-generated answer.

Generated answers should not be presented as if they were quotations from the source document unless they actually are quotations.

---

## 12. AI-Generated Content

LocalDoc may generate natural-language answers from document content.

The product should clearly identify generated answers as AI-generated where appropriate.

The UI and documentation must not falsely imply that generated answers were written directly by the document author.

---

## 13. Accuracy Requirements

LocalDoc must not claim a specific accuracy level unless supported by documented testing.

Accuracy evaluations should consider at least:

- retrieval accuracy;
- source-page accuracy;
- answer correctness;
- unsupported-answer rate;
- refusal behavior;
- multilingual behavior where supported.

Test results should identify:

- dataset;
- question set;
- model version;
- embedding model version;
- retrieval parameters;
- evaluation method.

---

## 14. Evaluation Dataset

A future evaluation dataset should contain representative document questions.

The dataset should test:

1. Questions with clear answers.
2. Questions requiring multiple chunks.
3. Questions requiring multiple pages.
4. Questions with no answer in the document.
5. Ambiguous questions.
6. Similar but incorrect passages.
7. Different document lengths.
8. Different languages where supported.

Customer documents must not be used for public evaluation datasets without appropriate authorization and review.

---

## 15. Sensitive Information

Documents processed by LocalDoc may contain sensitive information.

The AI pipeline must therefore treat:

- document text;
- chunks;
- embeddings;
- user questions;
- retrieved context;
- generated answers

as potentially sensitive customer data.

These data must remain local during normal operation.

---

## 16. Prompt Security

Document content must be treated as untrusted input.

A document may contain text that attempts to manipulate the LLM.

Examples include instructions such as:

- ignore previous instructions;
- reveal hidden information;
- execute an action;
- change system behavior.

LocalDoc must treat document text as data rather than trusted application instructions.

Future prompt-injection testing should verify that document content cannot override core system instructions.

---

## 17. Retrieval Security

Retrieved content must remain within the intended document scope.

The retrieval system must not intentionally combine documents in a way that violates the user's selected document scope.

Future multi-document functionality must explicitly define:

- document selection;
- access boundaries;
- retrieval boundaries;
- source attribution.

---

## 18. Local Model Security

Local model files are executable inputs to the AI runtime and must therefore be treated as trusted application components.

Commercial packaging should verify:

- model provenance;
- integrity;
- expected version;
- distribution rights;
- package integrity.

Models should not be downloaded automatically from arbitrary locations.

---

## 19. AI System Changes

Any change to:

- LLM;
- embedding model;
- prompt;
- retrieval algorithm;
- chunking strategy;
- similarity threshold;
- model runtime;
- AI-related dependency

should trigger an AI compliance and evaluation review.

The review should determine whether existing tests remain valid.

---

## 20. AI Risk Classification

LocalDoc's intended purpose is document assistance and information retrieval.

The current product concept does not intentionally target high-risk AI use cases such as:

- employment;
- education admissions;
- creditworthiness;
- essential public services;
- law enforcement;
- migration decisions;
- biometric identification;
- safety-critical infrastructure.

If the product scope changes toward such use cases, this document must be reviewed before implementation or marketing.

---

## 21. Prohibited Product Claims

LocalDoc should not claim:

- perfect accuracy;
- zero hallucinations;
- guaranteed legal correctness;
- guaranteed medical correctness;
- guaranteed financial correctness;
- autonomous professional decision-making.

Marketing claims must reflect the actual tested capabilities of the product.

---

## 22. User Documentation

The final product documentation should explain:

- that answers are AI-generated;
- that answers are based on retrieved document content;
- that the system can make mistakes;
- how source pages are displayed;
- how documents are stored;
- whether network access is required;
- what limitations apply to the AI system.

Documentation must match the actual implementation.

---

## 23. AI Logging

AI-related logs must not expose:

- prompts containing document content;
- retrieved chunks;
- complete generated answers;
- embeddings;
- model secrets;
- authentication credentials.

Technical metadata may be logged where necessary for troubleshooting.

---

## 24. AI Incident Handling

Future commercial versions should define a process for handling AI-related problems such as:

- incorrect answers;
- unexpected model behavior;
- prompt injection;
- model corruption;
- security vulnerabilities;
- unauthorized network communication;
- incorrect source attribution.

The incident process should preserve privacy and avoid collecting customer documents unnecessarily.

---

## 25. AI Act Review

The applicability of EU AI legislation must be reviewed against the final product, intended purpose, provider/deployer role, distribution model, and features.

This document does not classify LocalDoc legally.

The product team must verify applicable obligations before commercial release and whenever the intended purpose changes.

Particular attention should be given to transparency obligations applicable to AI systems and AI-generated content.

---

## 26. Commercial Release Gate

Before commercial release, verify:

- intended purpose documented;
- AI system architecture documented;
- model inventory completed;
- model licenses reviewed;
- commercial distribution rights verified;
- AI output disclosure implemented where required;
- source attribution tested;
- hallucination controls tested;
- prompt-injection risks evaluated;
- privacy architecture verified;
- logging reviewed;
- network behavior verified;
- documentation matches implementation;
- applicable EU AI requirements reviewed.

---

## 27. Current Status

Current AI architecture:

- local embeddings: implemented;
- local retrieval: implemented;
- similarity threshold: implemented;
- context-only prompting: implemented;
- no-context refusal: implemented;
- source page reporting: implemented;
- local LLM integration: implemented;
- remote LLM API: not part of normal operation;
- AI model license review: pending;
- AI evaluation dataset: pending;
- prompt-injection tests: pending;
- formal AI compliance review: pending.

---

## 28. Review History

### Initial AI Compliance Review

Completed:

- AI system architecture documented.
- Intended purpose documented.
- AI data flow documented.
- AI output risks identified.
- Model licensing requirements documented.
- Prompt-injection risk identified.
- AI evaluation requirements documented.
- Commercial release gate defined.

---

## 29. Next Review

Review this document whenever:

- the intended purpose changes;
- a new AI model is introduced;
- a new external AI service is introduced;
- AI output behavior materially changes;
- the product adds high-impact decision functionality;
- applicable legislation changes.
