from src.models import EmbeddedChunk
from src.llm import generate_answer
from src.retriever import retrieve_by_text


NO_ANSWER_MESSAGE = (
    "The answer is not available in the provided document."
)


def build_context(
    embedded_chunks: list[EmbeddedChunk],
) -> str:
    return "\n\n".join(
        f"[Page {item.chunk.page_number}]\n"
        f"{item.chunk.text}"
        for item in embedded_chunks
    )


def build_prompt(
    question: str,
    context: str,
) -> str:
    return f"""You are a document question-answering assistant.

Your task is to answer the user's question using ONLY the information
contained in the provided document context.

IMPORTANT RULES:
1. The context is the only source of truth.
2. Use only information from the context.
3. Use only information explicitly contained in the context.
4. If the context directly contains the answer, answer the question.
5. Do not use outside knowledge.
6. Do not guess or infer information.
7. Do not invent facts.
8. Do not invent page numbers.
9. Do not say that information is missing if the answer is explicitly
   stated in the context.
10. Answer in the same language as the user's question.
11. Keep the answer concise and directly answer the question.
12. If the answer cannot be found in the context, return exactly:
The answer is not available in the provided document.


DOCUMENT CONTEXT:
-----------------
{context}
-----------------

USER QUESTION:
{question}

ANSWER:"""


def is_no_answer(answer: str) -> bool:
    normalized = " ".join(
        answer.strip().lower().split()
    )

    no_answer_variants = {
        NO_ANSWER_MESSAGE.lower(),
        "the answer is not contained in the provided document.",
        "the answer is not available in the provided document.",
        "the answer is not in the provided document.",
        "the answer is not available in the document.",
        "the answer is not contained in the document.",
        "die antwort ist nicht im bereitgestellten dokument enthalten.",
        "die antwort ist nicht im bereitgestellten text enthalten.",
        "die antwort ist nicht im dokument enthalten.",
        "die antwort ist im bereitgestellten dokument nicht enthalten.",
        "die information ist nicht im bereitgestellten dokument enthalten.",
        "die information ist nicht im dokument enthalten.",
    }

    return normalized in no_answer_variants


def get_source_pages(
    embedded_chunks: list[EmbeddedChunk],
) -> list[int]:
    pages = {
        item.chunk.page_number
        for item in embedded_chunks
    }

    return sorted(pages)


def format_answer(
    answer: str,
    source_pages: list[int],
) -> str:
    cleaned_answer = answer.strip()

    if is_no_answer(cleaned_answer):
        return NO_ANSWER_MESSAGE

    if not source_pages:
        return cleaned_answer

    page_text = ", ".join(
        str(page)
        for page in source_pages
    )

    return (
        f"{cleaned_answer}\n\n"
        f"Source: Page {page_text}"
    )


def answer_question(
    question: str,
    embedded_chunks: list[EmbeddedChunk],
    embedder,
    llm,
    top_k: int = 3,
    min_similarity: float = 0.2,
) -> str:
    relevant_chunks = retrieve_by_text(
        query=question,
        embedded_chunks=embedded_chunks,
        embedder=embedder,
        top_k=top_k,
        min_similarity=min_similarity,
    )

    if not relevant_chunks:
        return NO_ANSWER_MESSAGE

    context = build_context(relevant_chunks)

    answer = generate_answer(
        question=question,
        context=context,
        llm=llm,
    )

    source_pages = get_source_pages(
        relevant_chunks
    )

    return format_answer(
        answer=answer,
        source_pages=source_pages,
    )
