from src.llm import generate_answer


class FakeLLM:
    def generate(self, prompt: str) -> str:
        return "Machine M42 requires regular maintenance."


def test_generate_answer():
    answer = generate_answer(
        question="Which machine requires regular maintenance?",
        context="Machine M42 requires regular maintenance.",
        llm=FakeLLM(),
    )

    assert answer == "Machine M42 requires regular maintenance."



class RecordingFakeLLM:
    def __init__(self):
        self.prompt = None

    def generate(self, prompt: str) -> str:
        self.prompt = prompt
        return "Answer"


def test_generate_answer_sends_question_and_context_to_llm():
    llm = RecordingFakeLLM()

    answer = generate_answer(
        question="What is Python?",
        context="Python is a programming language.",
        llm=llm,
    )

    assert answer == "Answer"
    assert "What is Python?" in llm.prompt
    assert "Python is a programming language." in llm.prompt
