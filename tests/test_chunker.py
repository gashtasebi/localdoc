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
                text="one. two. three. four.",
            ),
            Page(
                page_number=2,
                text="five. six. seven. eight.",
            ),
        ]
    )

    result = chunk_document(document, chunk_size=2)

    assert result is document
    assert result.chunks is not None
    assert len(result.chunks) == 6

    assert result.chunks[0].page_number == 1
    assert result.chunks[0].text == "one. two."

    assert result.chunks[1].page_number == 1
    assert result.chunks[1].text == "two. three."

    assert result.chunks[3].page_number == 2
    assert result.chunks[3].text == "five. six."

    assert result.chunks[4].page_number == 2
    assert result.chunks[4].text == "six. seven."

    assert result.chunks[0].chunk_id == 1
    assert result.chunks[1].chunk_id == 2
    assert result.chunks[2].chunk_id == 3
    assert result.chunks[3].chunk_id == 4

def test_split_sentences():
    from src.chunker import split_sentences

    text = "First sentence. Second sentence! Is this the third sentence?"

    sentences = split_sentences(text)

    assert len(sentences) == 3
    assert sentences[0] == "First sentence."
    assert sentences[1] == "Second sentence!"
    assert sentences[2] == "Is this the third sentence?"

def test_chunk_page_by_sentence():
    from src.chunker import chunk_page_by_sentence

    page = Page(
        page_number=5,
        text=(
            "Sentence one. "
            "Sentence two. "
            "Sentence three. "
            "Sentence four. "
            "Sentence five."
        ),
    )

    chunks = chunk_page_by_sentence(
        page,
        chunk_size=3,
        overlap=1,
    )

    assert len(chunks) == 2

    assert chunks[0].chunk_id == 1
    assert chunks[0].page_number == 5
    assert chunks[0].text == (
        "Sentence one. Sentence two. Sentence three."
    )

    assert chunks[1].chunk_id == 2
    assert chunks[1].page_number == 5
    assert chunks[1].text == (
        "Sentence three. Sentence four. Sentence five."
    )
