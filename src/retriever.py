import math

from src.models import EmbeddedChunk


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))

    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def retrieve(
    query_vector: list[float],
    embedded_chunks: list[EmbeddedChunk],
    top_k: int = 3,
    min_similarity: float | None = None,
) -> list[EmbeddedChunk]:

    ranked = sorted(
        embedded_chunks,
        key=lambda item: cosine_similarity(
            query_vector,
            item.vector,
        ),
        reverse=True,
    )

    if min_similarity is not None:
        ranked = [
            item
            for item in ranked
            if cosine_similarity(query_vector, item.vector)
            >= min_similarity
        ]

    return ranked[:top_k]


def retrieve_by_text(
    query: str,
    embedded_chunks: list[EmbeddedChunk],
    embedder,
    top_k: int = 3,
    min_similarity: float | None = None,
) -> list[EmbeddedChunk]:
    query_vector = embedder.embed(query)

    return retrieve(
        query_vector=query_vector,
        embedded_chunks=embedded_chunks,
        top_k=top_k,
        min_similarity=min_similarity,
    )
