import argparse

from src.embedder import SentenceTransformerEmbedder
from src.ollama_llm import OllamaLLM
from src.pipeline import process_pdf_pipeline
from src.qa import answer_question


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Ask questions about a PDF document."
    )

    parser.add_argument(
        "pdf_path",
        help="Path to the PDF document",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    print("Loading document...")

    embedder = SentenceTransformerEmbedder()
    llm = OllamaLLM()

    embedded_chunks = process_pdf_pipeline(
        args.pdf_path,
        embedder,
        chunk_size=5,
        overlap=1,
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
