from src.models import Chunk, EmbeddedChunk
from src.qa import build_context, build_prompt


def test_build_context():
    chunks = [
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=1,
                page_number=1,
                text="Machine M42 requires regular maintenance.",
            ),
            vector=[0.1, 0.2, 0.3],
        ),
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Electrical connections must be checked.",
            ),
            vector=[0.2, 0.3, 0.4],
        ),
    ]

    context = build_context(chunks)

    assert "Machine M42 requires regular maintenance." in context
    assert "Electrical connections must be checked." in context



def test_build_prompt():
    context = "Machine M42 requires regular maintenance."
    question = "Which machine requires regular maintenance?"

    prompt = build_prompt(
        question=question,
        context=context,
    )

    assert question in prompt
    assert context in prompt
    assert "Answer:" in prompt

from src.models import Chunk, EmbeddedChunk
from src.qa import answer_question


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Machine M42 requires regular maintenance."



from src.models import Chunk, EmbeddedChunk
from src.qa import answer_question


class FakeEmbedder:
    def embed(self, text: str) -> list[float]:
        return [1.0, 0.0]


class RecordingFakeLLM:
    def __init__(self):
        self.prompt = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "Machine M42 requires regular maintenance."


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
        EmbeddedChunk(
            chunk=Chunk(
                chunk_id=2,
                page_number=1,
                text="Machine X10 is used for production.",
            ),
            vector=[0.0, 1.0],
        ),
    ]

    llm = RecordingFakeLLM()

    answer = answer_question(
        question="Which machine requires regular maintenance?",
        embedded_chunks=embedded_chunks,
        embedder=FakeEmbedder(),
        llm=llm,
        top_k=1,
    )

    assert answer == "Machine M42 requires regular maintenance."
    assert llm.prompt is not None
    assert "Which machine requires regular maintenance?" in llm.prompt
    assert "Machine M42 requires regular maintenance." in llm.prompt
    assert "Machine X10 is used for production." not in llm.prompt



from src.models import Chunk, EmbeddedChunk
from src.qa import build_context


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
