from pathlib import Path

from src.chunker import chunk_document
from src.embedder import process_document_embeddings
from src.file_utils import calculate_file_hash
from src.models import Document, Page
from src.pipeline import process_pdf_pipeline
from src.storage.database import LocalDatabase


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


def test_process_pdf_pipeline_stores_document(tmp_path):

    import fitz

    pdf_path = tmp_path / "document.pdf"

    pdf = fitz.open()

    page = pdf.new_page()

    page.insert_text(
        (72, 72),
        "This is a test document for LocalDoc.",
    )

    pdf.save(pdf_path)
    pdf.close()

    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    embedded_chunks = process_pdf_pipeline(
        pdf_path=pdf_path,
        embedder=FakeEmbedder(),
        chunk_size=5,
        overlap=1,
        database=database,
    )

    assert embedded_chunks

    loaded_chunks = database.load_embedded_chunks(1)

    assert loaded_chunks
    assert loaded_chunks[0].chunk.text
    assert loaded_chunks[0].vector == [0.1, 0.2, 0.3]


def test_process_pdf_pipeline_does_not_embed_existing_document(
    tmp_path,
):

    import fitz

    class CountingEmbedder:

        def __init__(self):
            self.calls = 0

        def embed(self, text):
            self.calls += 1
            return [0.1, 0.2, 0.3]

    pdf_path = tmp_path / "document.pdf"

    pdf = fitz.open()

    page = pdf.new_page()

    page.insert_text(
        (72, 72),
        "This is a test document for LocalDoc.",
    )

    pdf.save(pdf_path)
    pdf.close()

    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    embedder = CountingEmbedder()

    first_result = process_pdf_pipeline(
        pdf_path=pdf_path,
        embedder=embedder,
        chunk_size=5,
        overlap=1,
        database=database,
    )

    first_call_count = embedder.calls

    second_result = process_pdf_pipeline(
        pdf_path=pdf_path,
        embedder=embedder,
        chunk_size=5,
        overlap=1,
        database=database,
    )

    assert first_call_count > 0
    assert embedder.calls == first_call_count
    assert second_result == first_result


def test_same_file_content_is_detected_by_hash(tmp_path):

    database = LocalDatabase(
        tmp_path / "localdoc.db"
    )

    pdf_path = Path("data/test_document.pdf")

    first_hash = calculate_file_hash(
        pdf_path
    )

    second_file = tmp_path / "copy.pdf"

    second_file.write_bytes(
        pdf_path.read_bytes()
    )

    second_hash = calculate_file_hash(
        second_file
    )

    assert first_hash == second_hash

    database.initialize()

    database.save_document(
        document=None,
        embedded_chunks=[],
        file_path=str(pdf_path),
        title="test_document",
        file_hash=first_hash,
    )

    existing_document_id = (
        database.find_document_by_hash(
            second_hash
        )
    )

    assert existing_document_id == 1
