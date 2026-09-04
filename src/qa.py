
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
        f"[Page {item.chunk.page_number}]\n{item.chunk.text}"
        for item in embedded_chunks
    )


def build_prompt(
    question: str,
    context: str,
) -> str:
    return f"""Answer the question using only the provided context.

Rules:
- Use only information from the context.
- Use only information explicitly contained in the context.
- Do not use outside knowledge.
- Do not guess or infer information that is not supported by the context.
- If the answer is not contained in the context, return exactly:
  "{NO_ANSWER_MESSAGE}"
- Do not mention information that is not present in the context.

Context:
{context}

Question:
{question}

Answer:"""


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
