# LocalDoc

LocalDoc is a document intelligence project focused on technical documents for German SMEs.

## Vision

> Turn company documents into structured, searchable knowledge.

## Current Status

Pre-MVP — Phase 1: NLP Foundations + PDF Processing Pipeline

## MVP Goal

The initial MVP will allow a user to:

1. Upload a PDF document.
2. Extract and clean its text.
3. Split the document into searchable chunks.
4. Retrieve relevant information.
5. Ask a question about the document.
6. Receive an evidence-based answer with document and page references.

## Planned Pipeline

PDF  
↓  
Text Extraction  
↓  
Text Cleaning  
↓  
Chunking  
↓  
Embeddings  
↓  
Vector Search  
↓  
Relevant Context  
↓  
LLM  
↓  
Answer + Sources

## Technology

- Python
- PyMuPDF
- spaCy
- Sentence Transformers
- FAISS
- SQLite
- FastAPI
- Streamlit

## Project Goals

This project is also a practical learning project covering:

- Natural Language Processing
- Information Retrieval
- Semantic Search
- Embeddings
- Retrieval-Augmented Generation (RAG)
- German technical language processing
- Evaluation of AI systems

## Project Status

This project is currently under active development.

The initial focus is on building a reliable PDF processing pipeline before implementing semantic search and RAG.
