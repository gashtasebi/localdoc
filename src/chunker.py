from src.models import Chunk, Page


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
