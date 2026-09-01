from src.embedder import SentenceTransformerEmbedder
from src.models import Chunk, EmbeddedChunk

from src.embedder import embed_document
from src.models import Chunk, Document

from src.embedder import process_document_embeddings



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


def test_embedded_chunk_stores_chunk_and_vector():
    chunk = Chunk(
        chunk_id=1,
        page_number=1,
        text="LocalDoc test chunk.",
    )

    vector = [0.1, 0.2, 0.3]

    embedded_chunk = EmbeddedChunk(
        chunk=chunk,
        vector=vector,
    )

    assert embedded_chunk.chunk is chunk
    assert embedded_chunk.vector == vector


def test_embed_document_embeds_all_chunks():
    document = Document(
        pages=[],
        chunks=[
            Chunk(
                chunk_id=1,
                page_number=1,
                text="First chunk.",
            ),
            Chunk(
                chunk_id=2,
                page_number=1,
                text="Second chunk.",
            ),
        ],
    )

    class FakeEmbedder:
        def embed(self, text: str) -> list[float]:
            return [0.1, 0.2, 0.3]

    embedder = FakeEmbedder()

    embedded_chunks = embed_document(document, embedder)

    assert len(embedded_chunks) == 2
    assert embedded_chunks[0].chunk.text == "First chunk."
    assert embedded_chunks[1].chunk.text == "Second chunk."
    assert embedded_chunks[0].vector == [0.1, 0.2, 0.3]



def test_embed_document_without_chunks_returns_empty_list():
    document = Document(pages=[])

    class FakeEmbedder:
        def embed(self, text: str) -> list[float]:
            return [0.1, 0.2, 0.3]

    embedded_chunks = embed_document(document, FakeEmbedder())

    assert embedded_chunks == []



def test_process_document_embeddings():
    document = Document(
        pages=[],
        chunks=[
            Chunk(
                chunk_id=1,
                page_number=1,
                text="First chunk.",
            ),
        ],
    )

    class FakeEmbedder:
        def embed(self, text: str) -> list[float]:
            return [0.1, 0.2, 0.3]

    result = process_document_embeddings(document, FakeEmbedder())

    assert len(result) == 1
    assert result[0].chunk.text == "First chunk."
    assert result[0].vector == [0.1, 0.2, 0.3]
