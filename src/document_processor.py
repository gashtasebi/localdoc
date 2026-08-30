from src.models import Page, Document
from src.pdf_parser import extract_text_from_pdf
from src.text_cleaner import clean_text

def process_pdf(pdf_path):
    pages = extract_text_from_pdf(pdf_path)

    page_objects = [
        Page(
            page_number = page["page_number"],
            text = clean_text(page["text"])
        )
        for page in pages
    ]
    return Document(pages= page_objects)
