from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(text)
        return vector.tolist()


from src.models import Document, EmbeddedChunk


def embed_document(
    document: Document,
    embedder: SentenceTransformerEmbedder,
) -> list[EmbeddedChunk]:
    embedded_chunks = []

    for chunk in document.chunks or []:
        vector = embedder.embed(chunk.text)

        embedded_chunks.append(
            EmbeddedChunk(
                chunk=chunk,
                vector=vector,
            )
        )

    return embedded_chunks

def process_document_embeddings(
    document: Document,
    embedder: SentenceTransformerEmbedder,
) -> list[EmbeddedChunk]:
    return embed_document(document, embedder)
