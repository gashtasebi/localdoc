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
) -> list[EmbeddedChunk]:

    ranked = sorted(
        embedded_chunks,
        key=lambda item: cosine_similarity(
            query_vector,
            item.vector,
        ),
        reverse=True,
    )

    return ranked[:top_k]
