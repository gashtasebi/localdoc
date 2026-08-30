from pathlib import Path

from src.pdf_parser import extract_text_from_pdf

def test_extract_text_from_pdf():
    pdf_path = Path("data/test_document.pdf")

    pages = extract_text_from_pdf(pdf_path)

    assert len(pages) > 0
    assert pages[0]["page_number"] == 1
    assert "Frequenzumrichter" in pages[0]["text"]
