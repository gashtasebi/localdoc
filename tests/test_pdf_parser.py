import pymupdf

from src.pdf_parser import extract_text_from_pdf

def test_extract_text_from_multi_page_pdf(tmp_path):
    pdf_path = tmp_path / "test_document.pdf"

    document = pymupdf.open()

    page1 = document.new_page()
    page1.insert_text((72, 72), "Maschine M42")
    page1.insert_text((72, 100), "Frequenzumrichter")

    page2 = document.new_page()
    page2.insert_text((72, 72), "Wartung")
    page2.insert_text((72, 100), "Elektrische Anschlüsse")

    page3 = document.new_page()
    page3.insert_text((72, 72), "Fehlerbericht")
    page3.insert_text((72, 100), "Überhitzung")

    document.save(pdf_path)
    document.close()

    pages = extract_text_from_pdf(pdf_path)


    assert len(pages) == 3

    assert pages[0]["page_number"] == 1
    assert "Frequenzumrichter" in pages[0]["text"]

    assert pages[1]["page_number"] == 2
    assert "Elektrische Anschlüsse" in pages[1]["text"]

    assert pages[2]["page_number"] == 3
    assert "Überhitzung" in pages[2]["text"]
