from src.chunker import chunk_document
from src.document_processor import process_pdf
from src.embedder import process_document_embeddings
from src.models import EmbeddedChunk
from src.storage.database import LocalDatabase


def process_pdf_pipeline(
    pdf_path,
    embedder,
    chunk_size: int = 500,
    overlap: int = 1,
    database: LocalDatabase | None = None,
) -> list[EmbeddedChunk]:

    if database is not None:
        database.initialize()

        existing_document_id = database.find_document_by_path(
            str(pdf_path)
        )

        if existing_document_id is not None:
            return database.load_embedded_chunks(
                existing_document_id
            )

    document = process_pdf(pdf_path)

    document = chunk_document(
        document,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    embedded_chunks = process_document_embeddings(
        document,
        embedder,
    )

    if database is not None:
        database.save_document(
            document=document,
            embedded_chunks=embedded_chunks,
            file_path=str(pdf_path),
        )

    return embedded_chunks
