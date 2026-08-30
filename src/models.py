from dataclasses import dataclass

@dataclass
class Page:
    page_number: int
    text: str

@dataclass
class Document:
    pages: list[Page]
