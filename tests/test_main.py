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



import pytest

from main import validate_pdf_path


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
