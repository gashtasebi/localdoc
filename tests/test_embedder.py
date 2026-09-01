from src.embedder import SentenceTransformerEmbedder

class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_embedder_returns_vector():
    embedder: Embedder = FakeEmbedder()

    vector = embedder.embed("HEllo LocalDoc")

    assert isinstance(vector, list)
    assert len(vector) == 3
    assert all(isinstance(value, float) for value in vector)


def test_real_embedder_returns_vector():
    embedder = SentenceTransformerEmbedder()

    vector = embedder.embed("LocalDoc is a document question answering system.")

    assert isinstance(vector, list)
    assert len(vector) > 0
    assert all(isinstance(value, float) for value in vector)
