from src.embedder import SentenceTransformerEmbedder
from src.ollama_llm import OllamaLLM
from src.pipeline import process_pdf_pipeline
from src.qa import answer_question


PDF_PATH = "data/test_document.pdf"


def main():
    print("Loading document...")

    embedder = SentenceTransformerEmbedder()
    llm = OllamaLLM()

    embedded_chunks = process_pdf_pipeline(
        PDF_PATH,
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
