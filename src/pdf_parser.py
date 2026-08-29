import fitz

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)

    try:
        document = fitz.open(pdf_path)
    except Exception as error:
        raise ValueError(f"Could not open PDF: {pdf_path}") from error

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text()

        pages.append({
            "page_number" : page_number,
            "text" : text,
        })

    document.close()
    return pages
