from src.chunker import chunk_document
from src.embedder import process_document_embeddings
from src.models import Document, Page
from src.pipeline import process_pdf_pipeline
from src.retriever import retrieve_by_text
from src.embedder import SentenceTransformerEmbedder


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_document_to_embeddings_pipeline():
    document = Document(
        pages=[
            Page(
                page_number=1,
                text="Python is a programming language. "
                     "Python is widely used in NLP.",
            )
        ]
    )

    document = chunk_document(
        document,
        chunk_size=2,
        overlap=1,
    )

    embedded_chunks = process_document_embeddings(
        document,
        FakeEmbedder(),
    )

    assert document.chunks is not None
    assert len(document.chunks) > 0
    assert len(embedded_chunks) == len(document.chunks)
    assert len(embedded_chunks[0].vector) == 3



def test_process_pdf_pipeline(monkeypatch):
    from src.pipeline import process_pdf_pipeline

    document = Document(
        pages=[
            Page(
                page_number=1,
                text="Python is useful. Python is used in NLP.",
            )
        ]
    )

    def fake_process_pdf(pdf_path):
        return document

    monkeypatch.setattr(
        "src.pipeline.process_pdf",
        fake_process_pdf,
    )

    result = process_pdf_pipeline(
        "data/test_document.pdf",
        FakeEmbedder(),
        chunk_size=2,
        overlap=1,
    )

    assert len(result) > 0
    assert len(result[0].vector) == 3
