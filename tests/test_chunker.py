from src.chunker import chunk_page
from src.models import Chunk, Page, Document


def test_chunk_page():
    page = Page(
        page_number=7,
        text="one two three four five six seven eight nine ten",
    )

    chunks = chunk_page(page, chunk_size=3)

    assert len(chunks) == 4

    assert isinstance(chunks[0], Chunk)

    assert chunks[0].chunk_id == 1
    assert chunks[0].page_number == 7
    assert chunks[0].text == "one two three"

    assert chunks[1].chunk_id == 2
    assert chunks[1].text == "four five six"

    assert chunks[2].chunk_id == 3
    assert chunks[2].text == "seven eight nine"

    assert chunks[3].chunk_id == 4
    assert chunks[3].text == "ten"

def test_chunk_document():
    from src.chunker import chunk_document

    document = Document(
        pages=[
            Page(
                page_number=1,
                text="one two three four",
            ),
            Page(
                page_number=2,
                text="five six seven eight",
            ),
        ]
    )

    result = chunk_document(document, chunk_size=2)

    assert result is document
    assert result.chunks is not None
    assert len(result.chunks) == 4

    assert result.chunks[0].page_number == 1
    assert result.chunks[0].text == "one two"

    assert result.chunks[1].page_number == 1
    assert result.chunks[1].text == "three four"

    assert result.chunks[2].page_number == 2
    assert result.chunks[2].text == "five six"

    assert result.chunks[3].page_number == 2
    assert result.chunks[3].text == "seven eight"
