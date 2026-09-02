from src.models import Chunk, EmbeddedChunk
from src.qa import answer_question, build_context


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Machine M42 requires regular maintenance."


class RecordingFakeLLM:
    def __init__(self):
        self.prompt = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "Answer"


def test_build_context_includes_page_numbers():
    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=3,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=5,
                text="Machine X10 is used for production.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    context = build_context(embedded_chunks)

    assert "[Page 3]" in context
    assert "[Page 5]" in context
    assert "Machine M42 requires regular maintenance." in context
    assert "Machine X10 is used for production." in context


def test_answer_question():
    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[1.0, 0.0],
        ),
    ]

    answer = answer_question(
        question="Which machine requires regular maintenance?",
        embedded_chunks=embedded_chunks,
        embedder=FakeEmbedder(),
        llm=FakeLLM(),
        top_k=3,
        min_similarity=0.2,
    )

    assert answer == (
        "Machine M42 requires regular maintenance.\n\n"
        "Source: Page 1"
    )


def test_answer_question_includes_multiple_source_pages():
    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=2,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[1.0, 0.0],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=5,
                text="Machine M42 is used for production.",
            ),
            vector=[1.0, 0.0],
        ),
    ]

    answer = answer_question(
        question="What is Machine M42?",
        embedded_chunks=embedded_chunks,
        embedder=FakeEmbedder(),
        llm=FakeLLM(),
        top_k=3,
        min_similarity=0.2,
    )

    assert "Source: Page 2, 5" in answer


def test_answer_question_sends_question_and_context_to_llm():
    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Python is a programming language.",
            ),
            vector=[1.0, 0.0],
        ),
    ]

    llm = RecordingFakeLLM()

    answer_question(
        question="What is Python?",
        embedded_chunks=embedded_chunks,
        embedder=FakeEmbedder(),
        llm=llm,
        top_k=3,
        min_similarity=0.2,
    )

    assert "What is Python?" in llm.prompt
    assert "Python is a programming language." in llm.prompt


def test_answer_question_returns_unavailable_when_no_chunk_passes_threshold():
    embedded_chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    llm = RecordingFakeLLM()

    answer = answer_question(
        question="What is the name of the CEO of Apple?",
        embedded_chunks=embedded_chunks,
        embedder=FakeEmbedder(),
        llm=llm,
        top_k=3,
        min_similarity=0.2,
    )

    assert answer == (
        "The answer is not available in the provided document."
    )

    assert llm.prompt is None
