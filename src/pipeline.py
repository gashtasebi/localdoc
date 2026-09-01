from src.chunker import chunk_document
from src.document_processor import process_pdf
from src.embedder import process_document_embeddings
from src.models import EmbeddedChunk


def process_pdf_pipeline(
    pdf_path,
    embedder,
    chunk_size: int = 500,
    overlap: int = 1,
) -> list[EmbeddedChunk]:
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

    return embedded_chunks
