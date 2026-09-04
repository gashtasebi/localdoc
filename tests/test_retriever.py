from src.models import Chunk, EmbeddedChunk
from src.retriever import (
    cosine_similarity,
    retrieve,
    retrieve_by_text,
    retrieve_with_scores,
)


def test_cosine_similarity():
    assert cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    ) == 1.0


def test_retrieve_returns_most_similar_chunk():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                1,
                1,
                "Python programming",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                2,
                1,
                "Machine learning",
            ),
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
            chunk=Chunk(
                1,
                1,
                "First",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                2,
                1,
                "Second",
            ),
            vector=[0.9, 0.1],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                3,
                1,
                "Third",
            ),
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
    assert cosine_similarity(
        [0.0, 0.0],
        [1.0, 0.0],
    ) == 0.0


def test_retrieve_by_text():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                1,
                1,
                "Python is a programming language.",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                2,
                1,
                "The weather is sunny today.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    class FakeEmbedder:
        def embed(
            self,
            text: str,
        ) -> list[float]:
            return [1.0, 0.0]

    result = retrieve_by_text(
        query="What is Python?",
        embedded_chunks=chunks,
        embedder=FakeEmbedder(),
        top_k=1,
    )

    assert len(result) == 1
    assert result[0].chunk.text == (
        "Python is a programming language."
    )


def test_retrieve_returns_most_relevant_chunk_first():
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
                text=(
                    "Machine M42 requires "
                    "regular maintenance."
                ),
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
                text=(
                    "Machine M42 requires "
                    "regular maintenance."
                ),
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


def test_retrieve_returns_empty_when_nothing_meets_threshold():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Python",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Machine learning",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=3,
        min_similarity=1.1,
    )

    assert result == []


def test_retrieve_handles_empty_chunks():
    result = retrieve(
        query_vector=[1.0, 0.0],
        embedded_chunks=[],
        top_k=3,
    )

    assert result == []


def test_retrieve_with_threshold_keeps_results_sorted():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Medium",
            ),
            vector=[0.8, 0.6],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="High",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=3,
                page_number=1,
                text="Low",
            ),
            vector=[0.6, 0.8],
        ),
    ]

    result = retrieve(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=3,
        min_similarity=0.5,
    )

    assert [item.chunk.text for item in result] == [
        "High",
        "Medium",
        "Low",
    ]




def test_retrieve_with_scores_returns_scores_and_chunks():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Python programming",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Machine learning",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve_with_scores(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=2,
    )

    assert len(result) == 2

    score, item = result[0]

    assert isinstance(score, float)
    assert item is chunks[0]


def test_retrieve_with_scores_is_sorted_descending():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Low",
            ),
            vector=[0.0, 1.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="High",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=3,
                page_number=1,
                text="Medium",
            ),
            vector=[0.7, 0.7],
        ),
    ]

    result = retrieve_with_scores(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=3,
    )

    scores = [
        score
        for score, _ in result
    ]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_retrieve_with_scores_respects_top_k():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="First",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Second",
            ),
            vector=[0.9, 0.1],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=3,
                page_number=1,
                text="Third",
            ),
            vector=[0.8, 0.2],
        ),
    ]

    result = retrieve_with_scores(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=2,
    )

    assert len(result) == 2


def test_retrieve_with_scores_respects_min_similarity():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Relevant",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Irrelevant",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    result = retrieve_with_scores(
        query_vector=[1.0, 0.0],
        embedded_chunks=chunks,
        top_k=5,
        min_similarity=0.5,
    )

    assert len(result) == 1

    score, item = result[0]

    assert item is chunks[0]
    assert score >= 0.5
