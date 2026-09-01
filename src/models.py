from dataclasses import dataclass

@dataclass
class Page:
    page_number: int
    text: str


@dataclass
class Chunk:
    chunk_id: int
    page_number: int
    text: str


@dataclass
class Document:
    pages: list[Page]
    chunks: list[Chunk] | None = None

@dataclass
class EmbeddedChunk:
    chunk: Chunk
    vector: list[float]
