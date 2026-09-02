import argparse
from pathlib import Path

from src.embedder import SentenceTransformerEmbedder
from src.ollama_llm import OllamaLLM
from src.pipeline import process_pdf_pipeline
from src.qa import answer_question
from src.storage.database import LocalDatabase


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ask questions about a PDF document."
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

    database = LocalDatabase(
        "data/localdoc.db"
    )

    database.initialize()

    if args.list:
        documents = database.list_documents()

        print("\nDocument Library:")

        if not documents:
            print("No documents found.")
        else:
            for document in documents:
                print(
                    f"{document['id']}: {document['file_path']}"
                )

        return

    if args.document is not None:
        document = database.get_document(
            args.document
        )

        if document is None:
            print(
                f"Error: document with ID "
                f"{args.document} not found."
            )
            return

        try:
            pdf_path = validate_pdf_path(
                document["file_path"]
            )
        except (FileNotFoundError, ValueError) as error:
            print(f"Error: {error}")
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

    embedded_chunks = process_pdf_pipeline(
        str(pdf_path),
        embedder,
        chunk_size=5,
        overlap=1,
        database=database,
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
