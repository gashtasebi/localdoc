from pdf_parser import extract_text_from_pdf

pdf_path = "data/test_document.pdf"

pages = extract_text_from_pdf(pdf_path)

for page in pages:
    print(f"---Page {page['page_number']} ---")
    print(page["text"])
