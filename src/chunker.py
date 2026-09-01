import re
from src.models import Chunk, Page, Document

def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [sentence for sentence in sentences if sentence]

def chunk_page_by_sentence(
    page: Page,
    chunk_size: int = 5,
    overlap: int = 1,
) -> list[Chunk]:
    sentences = split_sentences(page.text)
    chunks = []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    start = 0

    while start < len(sentences):
        end = start + chunk_size
        chunk_sentences = sentences[start:end]

        chunk_text = " ".join(chunk_sentences)

        chunks.append(
            Chunk(
                chunk_id=len(chunks) + 1,
                page_number=page.page_number,
                text=chunk_text,
            )
        )

        if end >= len(sentences):
            break

        start = end - overlap

    return chunks


def chunk_page(page: Page, chunk_size: int = 500) -> list[Chunk]:
    words = page.text.split()
    chunks = []

    for start in range(0, len(words), chunk_size):
        chunk_words = words[start:start + chunk_size]
        chunk_text = " ".join(chunk_words)

        chunks.append(
            Chunk(
                chunk_id=len(chunks) + 1,
                page_number=page.page_number,
                text=chunk_text,
            )
        )

    return chunks


def chunk_document(
    document: Document,
    chunk_size: int = 500,
) -> Document:
    all_chunks = []

    for page in document.pages:
        page_chunks = chunk_page_by_sentence(page, chunk_size)

        for chunk in page_chunks:
            chunk.chunk_id = len(all_chunks) + 1
            all_chunks.append(chunk)

    document.chunks = all_chunks

    return document
