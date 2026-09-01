from src.ollama_llm import OllamaLLM


class FakeResponse:
    def read(self):
        return b'{"response": "Python is a programming language."}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def test_ollama_llm_generate(monkeypatch):
    def fake_urlopen(request):
        assert request.full_url == "http://localhost:11434/api/generate"
        return FakeResponse()

    monkeypatch.setattr(
        "src.ollama_llm.urlopen",
        fake_urlopen,
    )

    llm = OllamaLLM()

    answer = llm.generate("What is Python?")

    assert answer == "Python is a programming language."
