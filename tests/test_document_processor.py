import pymupdf


from src.document_processor import process_pdf
from src.models import Document

def test_process_pdf(tmp_path):
    pdf_path = tmp_path / "test_document.pdf"

    document = pymupdf.open()

    page = document.new_page()
    page.insert_text((72, 72), "Frequenz-\numrichter")
    page.insert_text((72, 100), "Maschine      M42")

    document.save(pdf_path)
    document.close()

    result = process_pdf(pdf_path)

    assert isinstance(result, Document)
    assert len(result.pages) == 1
    assert result.pages[0].page_number == 1
    assert "Frequenzumrichter" in result.pages[0].text
    assert "Maschine M42" in result.pages[0].text
