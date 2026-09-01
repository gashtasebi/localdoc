import json
from urllib.request import Request, urlopen


class OllamaLLM:
    def __init__(
        self,
        model: str = "llama3.2:3b",
        url: str = "http://localhost:11434/api/generate",
    ):
        self.model = model
        self.url = url

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        request = Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))

        return result["response"]
