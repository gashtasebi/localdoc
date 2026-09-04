import sys
from pathlib import Path

import pytest

from main import main
from main import parse_arguments
from main import validate_pdf_path


def test_parse_arguments_accepts_pdf_path(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "data/test_document.pdf",
        ],
    )

    args = parse_arguments()

    assert args.pdf_path == "data/test_document.pdf"


def test_parse_arguments_accepts_document_id(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--document",
            "2",
        ],
    )

    args = parse_arguments()

    assert args.document == 2


def test_validate_pdf_path_rejects_missing_file(tmp_path):
    pdf_path = tmp_path / "missing.pdf"

    with pytest.raises(
        FileNotFoundError,
        match="PDF file not found",
    ):
        validate_pdf_path(str(pdf_path))


def test_validate_pdf_path_rejects_non_pdf(tmp_path):
    file_path = tmp_path / "document.txt"

    file_path.write_text("test")

    with pytest.raises(
        ValueError,
        match="File is not a PDF",
    ):
        validate_pdf_path(str(file_path))


def test_validate_pdf_path_accepts_pdf(tmp_path):
    pdf_path = tmp_path / "document.pdf"

    pdf_path.write_bytes(b"fake pdf")

    result = validate_pdf_path(str(pdf_path))

    assert result == pdf_path


def test_main_selects_document_by_id_and_loads_embeddings(
    monkeypatch,
    capsys,
):
    class FakeDatabase:
        def __init__(self):
            self.requested_document_id = None

        def initialize(self):
            pass

    database = FakeDatabase()

    monkeypatch.setattr(
        "main.LocalDatabase",
        lambda path: database,
    )

    monkeypatch.setattr(
        "main.SentenceTransformerEmbedder",
        lambda: object(),
    )

    monkeypatch.setattr(
        "main.OllamaLLM",
        lambda: object(),
    )

    loaded_chunks = [
        "stored-chunk-1",
        "stored-chunk-2",
    ]

    load_embedded_chunks_mock = []

    class FakeDocumentService:
        def __init__(self, database):
            self.database = database

        def load_document(self, document_id):
            database.requested_document_id = document_id

            return {
                "id": document_id,
                "file_path": "data/test_document.pdf",
                "title": "Test Document",
                "file_hash": "test-hash",
            }

        def load_embedded_chunks(self, document_id):
            load_embedded_chunks_mock.append(document_id)
            return loaded_chunks

        def process_pdf(self, pdf_path):
            raise AssertionError(
                "process_pdf must not be called "
                "for a stored document."
            )

    monkeypatch.setattr(
        "main.DocumentService",
        FakeDocumentService,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--document",
            "2",
        ],
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "exit",
    )

    main()

    captured = capsys.readouterr()

    assert database.requested_document_id == 2
    assert load_embedded_chunks_mock == [2]
    assert "Selected document: Test Document" in captured.out
    assert "Goodbye!" in captured.out


def test_main_handles_missing_document(monkeypatch, capsys):
    class FakeDatabase:
        def initialize(self):
            pass

    database = FakeDatabase()

    class FakeDocumentService:
        def __init__(self, database):
            self.database = database

        def load_document(self, document_id):
            raise ValueError(
                f"Document with ID {document_id} not found."
            )

    monkeypatch.setattr(
        "main.LocalDatabase",
        lambda path: database,
    )

    monkeypatch.setattr(
        "main.DocumentService",
        FakeDocumentService,
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "main.py",
            "--document",
            "999",
        ],
    )

    main()

    captured = capsys.readouterr()

    assert "document with ID 999 not found" in captured.out
