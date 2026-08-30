from src.models import Document, Page

def test_page_model():
    page = Page(
        page_number = 1,
        text = "Frequenzumrichter"
    )

    assert page.page_number == 1
    assert page.text == "Frequenzumrichter"


def test_document_model():
    pages = [
        Page(page_number=1, text="Maschine M42"),
        Page(page_number=2, text="Wartung")
    ]

    document = Document(pages=pages)

    assert len(document.pages) == 2
    assert document.pages[0].page_number==1
    assert document.pages[1].text== "Wartung"
