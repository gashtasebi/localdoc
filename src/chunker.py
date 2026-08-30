from src.models import Chunk, Page, Document


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
        page_chunks = chunk_page(page, chunk_size)
        all_chunks.extend(page_chunks)

    document.chunks = all_chunks

    return document
