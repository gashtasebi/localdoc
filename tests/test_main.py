import sys

from main import parse_arguments


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
