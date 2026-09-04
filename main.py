import argparse

from pathlib import Path

from src.embedder import SentenceTransformerEmbedder
from src.ollama_llm import OllamaLLM
from src.qa import answer_question
from src.services.document_service import DocumentService
from src.storage.database import LocalDatabase


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ask questions about PDF documents."
    )

    parser.add_argument(
        "pdf_path",
        nargs="?",
        help="Path to the PDF document",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List documents in the document library",
    )

    parser.add_argument(
        "--document",
        type=int,
        help="Select a document by its ID",
    )

    parser.add_argument(
        "--import",
        dest="import_path",
        help="Import a PDF document into the document library",
    )

    parser.add_argument(
        "--delete",
        type=int,
        help="Delete a document by its ID",
    )

    return parser.parse_args()


def validate_pdf_path(pdf_path: str) -> Path:
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"PDF path is not a file: {pdf_path}"
        )

    if path.suffix.lower() != ".pdf":
        raise ValueError(
            f"File is not a PDF: {pdf_path}"
        )

    return path


def main():
    args = parse_arguments()

    database = LocalDatabase("data/localdoc.db")
    database.initialize()

    document_service = DocumentService(database)

    if args.list:
        documents = document_service.list_documents()

        print("\nDocument Library:")

        if not documents:
            print("No documents found.")
        else:
            for document in documents:
                title = document["title"]

                if not title:
                    title = Path(
                        document["file_path"]
                    ).stem

                print(
                    f"\n{document['id']}: {title}"
                )

                print(
                    f"   Path: {document['file_path']}"
                )

                print(
                    f"   Pages: {document['page_count']}"
                )

                print(
                    f"   Chunks: {document['chunk_count']}"
                )

        return

    if args.import_path:
        try:
            pdf_path = validate_pdf_path(
                args.import_path
            )

            document_id = document_service.import_pdf(
                pdf_path
            )

        except (FileNotFoundError, ValueError) as error:
            print(f"Error: {error}")
            return

        print("Document imported successfully.")
        print(f"Document ID: {document_id}")

        return

    if args.delete is not None:
        deleted = document_service.delete_document(
            args.delete
        )

        if deleted:
            print(
                f"Document {args.delete} deleted successfully."
            )
        else:
            print(
                f"Error: document {args.delete} not found."
            )

        return

    embedded_chunks = None

    if args.document is not None:
        try:
            document = document_service.load_document(
                args.document
            )

        except ValueError:
            print(
                f"Error: document with ID "
                f"{args.document} not found"
            )
            return

        title = document["title"]

        if not title:
            title = Path(
                document["file_path"]
            ).stem

        print(
            f"Selected document: {title}"
        )

        try:
            embedded_chunks = (
                document_service.load_embedded_chunks(
                    args.document
                )
            )

        except ValueError:
            print(
                f"Error: document with ID "
                f"{args.document} not found"
            )
            return

    else:
        if not args.pdf_path:
            print("Error: PDF path is required.")
            return

        try:
            pdf_path = validate_pdf_path(
                args.pdf_path
            )

        except (FileNotFoundError, ValueError) as error:
            print(f"Error: {error}")
            return

    print("Loading document...")

    embedder = SentenceTransformerEmbedder()
    llm = OllamaLLM()

    if embedded_chunks is None:
        document_service.embedder = embedder

        embedded_chunks = document_service.process_pdf(
            pdf_path
        )

    print("Document loaded.")
    print("Ask questions about the document.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ")

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question.strip():
            continue

        answer = answer_question(
            question=question,
            embedded_chunks=embedded_chunks,
            embedder=embedder,
            llm=llm,
            top_k=3,
            min_similarity=0.2,
        )

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()
