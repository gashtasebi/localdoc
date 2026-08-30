from src.pdf_parser import extract_text_from_pdf
from src.text_cleaner import clean_text

def process_pdf(pdf_path):
    pages = extract_text_from_pdf(pdf_path)

    for page in pages:
        page["text"] = clean_text(page["text"])
    return pages
