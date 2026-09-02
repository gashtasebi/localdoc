from src.models import Chunk, EmbeddedChunk
from src.retriever import cosine_similarity, retrieve, retrieve_by_text

def test_cosine_similarity():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == 1.0


def test_retrieve_returns_most_similar_chunk():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(1, 1, "Python programming"),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(2, 1, "Machine learning"),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve(
        query_vector=[0.9, 0.1],
        embedded_chunks=chunks,
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].chunk.text == "Python programming"



def test_retrieve_respects_top_k():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(1, 1, "First"),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(2, 1, "Second"),
            vector=[0.9, 0.1],
        ),
        EmbeddedChunk(
            chunk=Chunk(3, 1, "Third"),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=2,
    )

    assert len(result) == 2
    assert result[0].chunk.text == "First"
    assert result[1].chunk.text == "Second"



def test_cosine_similarity_with_zero_vector():
    assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0


def test_retrieve_by_text():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(1, 1, "Python is a programming language."),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(2, 1, "The weather is sunny today."),
            vector=[0.0, 1.0],
        ),
    ]

    class FakeEmbedder:
        def embed(self, text: str) -> list[float]:
            return [1.0, 0.0]

    result = retrieve_by_text(
        query="What is Python?",
        embedded_chunks=chunks,
        embedder=FakeEmbedder(),
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].chunk.text == "Python is a programming language."



def test_retrieve_returns_most_relevant_chunk_first():
    from src.models import Chunk, EmbeddedChunk
    from src.retriever import retrieve

    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Python is a programming language.",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=2,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve(
        query_vector=[0.0, 1.0],
        embedded_chunks=chunks,
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].chunk.text == (
        "Machine M42 requires regular maintenance."
    )



def test_retrieve_filters_by_min_similarity():
    from src.models import Chunk, EmbeddedChunk
    from src.retriever import retrieve

    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Python is a programming language.",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=2,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=3,
        min_similarity=0.9,
    )

    assert len(result) == 1
    assert result[0].chunk.text == (
        "Python is a programming language."
    )
